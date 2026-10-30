#!/usr/bin/env python3
"""Offline, evidence-gated editorial ranking. No live trend collection or DB writes."""
import argparse
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

WEIGHTS = {
    "audience_need": 25,
    "expertise_fit": 20,
    "discussion_depth": 20,
    "originality": 15,
    "distribution": 10,
    "feasibility": 10,
}

def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be non-empty text")
    return value.strip()

def parse_date(value, label):
    nonempty(value, label)
    try:
        result = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be YYYY-MM-DD") from exc
    if result.isoformat() != value:
        raise ValueError(f"{label} must be YYYY-MM-DD")
    return result

def review_topic(item, as_of):
    if not isinstance(item, dict):
        raise ValueError("topics must contain objects")
    topic_id = nonempty(item.get("id"), "topic.id")
    nonempty(item.get("title_zh"), f"{topic_id}.title_zh")
    nonempty(item.get("title_en"), f"{topic_id}.title_en")
    ratings = item.get("ratings")
    if not isinstance(ratings, dict) or set(ratings) != set(WEIGHTS):
        raise ValueError(f"{topic_id}.ratings needs exactly six rubric fields")
    for field, value in ratings.items():
        if type(value) is not int or value < 0 or value > 5:
            raise ValueError(f"{topic_id}.ratings.{field} must be an integer from 0 to 5")
    evidence = item.get("evidence")
    if not isinstance(evidence, list):
        raise ValueError(f"{topic_id}.evidence must be a list")
    seen_urls, platforms, markets = set(), set(), set()
    for index, source in enumerate(evidence):
        label = f"{topic_id}.evidence[{index}]"
        if not isinstance(source, dict):
            raise ValueError(f"{label} must be an object")
        url = nonempty(source.get("url"), f"{label}.url")
        split = urlsplit(url)
        if split.scheme not in ("http", "https") or not split.hostname or split.username or split.password:
            raise ValueError(f"{label}.url must be a public HTTP(S) URL without credentials")
        platform = nonempty(source.get("platform"), f"{label}.platform").casefold()
        market = source.get("market")
        if market not in ("CN", "GLOBAL"):
            raise ValueError(f"{label}.market must be CN or GLOBAL")
        observed = parse_date(source.get("observed_at"), f"{label}.observed_at")
        if observed > as_of:
            raise ValueError(f"{label}.observed_at must not be after as_of")
        nonempty(source.get("claim"), f"{label}.claim")
        if "published_at" in source and source["published_at"] not in (None, ""):
            parse_date(source["published_at"], f"{label}.published_at")
        seen_urls.add(url)
        platforms.add(platform)
        markets.add(market)
    score = sum(WEIGHTS[field] * ratings[field] // 5 for field in WEIGHTS)
    status = "editorial_review" if len(seen_urls) >= 2 and len(platforms) >= 2 else "needs_evidence"
    return {
        **item,
        "score_100": score,
        "review_status": status,
        "source_count": len(seen_urls),
        "distinct_platforms": len(platforms),
        "market_coverage": sorted(markets),
        "cross_market_evidence": markets == {"CN", "GLOBAL"},
    }

def rank_topics(payload):
    if not isinstance(payload, dict):
        raise ValueError("input must be an object")
    as_of_value = payload.get("as_of")
    as_of = parse_date(as_of_value, "as_of")
    topics = payload.get("topics")
    if not isinstance(topics, list):
        raise ValueError("topics must be a list")
    results = [review_topic(topic, as_of) for topic in topics]
    ids = [x["id"] for x in results]
    if len(ids) != len(set(ids)):
        raise ValueError("topic IDs must be unique")
    results.sort(key=lambda x: (x["review_status"] != "editorial_review", -x["score_100"], x["id"]))
    return {
        "as_of": as_of_value,
        "methodology": "Provisional human-rated editorial score, not measured platform demand",
        "ranked_topics": results,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Input JSON file")
    parser.add_argument("--output", type=Path, help="Output JSON file; omit to print to stdout")
    args = parser.parse_args()
    try:
        report = rank_topics(json.loads(args.input.read_text(encoding="utf-8")))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Input error: {exc}\n")
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

if __name__ == "__main__":
    main()
