# JSON input and output

The local ranker consumes an object with as_of (YYYY-MM-DD) and topics array. Each topic must include id, title_zh, title_en, ratings and evidence. Optional editorial notes pass through unchanged.

Example structure (illustrative, NOT a real trend finding):

{
  "as_of": "2026-10-31",
  "topics": [
    {
      "id": "ai-architecture-example",
      "title_zh": "AI 与建筑师",
      "title_en": "AI and architects",
      "ratings": {
        "audience_need": 3,
        "expertise_fit": 5,
        "discussion_depth": 5,
        "originality": 4,
        "distribution": 4,
        "feasibility": 4
      },
      "evidence": [
        {
          "url": "https://example.org/editorial-example",
          "platform": "Example Global Source",
          "market": "GLOBAL",
          "observed_at": "2026-10-30",
          "claim": "Synthetic example; not evidence"
        }
      ]
    }
  ]
}

Input validation:
- id and both titles: non-empty text; topic ids unique per input.
- ratings: six integers from 0 to 5, not booleans.
- evidence: list of objects; each item requires http(s) URL with host, platform, market (CN or GLOBAL), observed_at date not after as_of, and a non-empty claim.
- No metric is inferred from source presence. The optional source fields published_at, metric_name, metric_value and metric_unit require human verification before inclusion.
- Do not submit sensitive identifiers, credentials or non-public user comments.

Output:
- as_of, methodology and ranked_topics sorted with editorial_review first and higher provisional scores next.
- Each ranked topic keeps original fields and adds score_100, review_status, source_count, distinct_platforms, market_coverage and cross_market_evidence.
- No external requests, persistence or database writes are performed.
