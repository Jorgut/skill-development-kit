"""Python standard-library tests for editorial ranking and isolated SQLite design."""
import sqlite3
import unittest
from pathlib import Path

import importlib.util

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "rank_topics.py"
spec = importlib.util.spec_from_file_location("podcast_ranker", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
rank_topics, WEIGHTS = module.rank_topics, module.WEIGHTS

def candidate():
    return {
        "id": "example",
        "title_zh": "测试主题",
        "title_en": "Test topic",
        "ratings": {field: 4 for field in WEIGHTS},
        "evidence": [],
    }

class RankTopicsTests(unittest.TestCase):
    def test_needs_evidence_without_sources(self):
        result = rank_topics({"as_of": "2026-10-31", "topics": [candidate()]})
        row = result["ranked_topics"][0]
        self.assertEqual(row["score_100"], 80)
        self.assertEqual(row["review_status"], "needs_evidence")
        self.assertFalse(row["cross_market_evidence"])

    def test_two_markets_and_platforms(self):
        topic = candidate()
        topic["evidence"] = [
            {"url": "https://example.org/a", "platform": "Example A", "market": "CN", "observed_at": "2026-10-29", "claim": "synthetic"},
            {"url": "https://example.net/b", "platform": "Example B", "market": "GLOBAL", "observed_at": "2026-10-30", "claim": "synthetic"},
        ]
        row = rank_topics({"as_of": "2026-10-31", "topics": [topic]})["ranked_topics"][0]
        self.assertEqual(row["review_status"], "editorial_review")
        self.assertTrue(row["cross_market_evidence"])
        self.assertEqual(row["source_count"], 2)

    def test_same_platform_not_review_eligible(self):
        topic = candidate()
        topic["evidence"] = [
            {"url": "https://example.org/a", "platform": "Same", "market": "CN", "observed_at": "2026-10-30", "claim": "synthetic"},
            {"url": "https://example.net/b", "platform": "Same", "market": "CN", "observed_at": "2026-10-30", "claim": "synthetic"},
        ]
        row = rank_topics({"as_of": "2026-10-31", "topics": [topic]})["ranked_topics"][0]
        self.assertEqual(row["review_status"], "needs_evidence")

    def test_reject_invalid_score(self):
        topic = candidate()
        topic["ratings"]["originality"] = 7
        with self.assertRaises(ValueError):
            rank_topics({"as_of": "2026-10-31", "topics": [topic]})

    def test_reject_future_observation(self):
        topic = candidate()
        topic["evidence"] = [
            {"url": "https://example.org/a", "platform": "Test", "market": "GLOBAL", "observed_at": "2026-11-01", "claim": "synthetic"}
        ]
        with self.assertRaises(ValueError):
            rank_topics({"as_of": "2026-10-31", "topics": [topic]})

    def test_reject_duplicate_topic_ids(self):
        with self.assertRaises(ValueError):
            rank_topics({"as_of": "2026-10-31", "topics": [candidate(), candidate()]})

    def test_schema_is_standalone_and_idempotent(self):
        sql_path = Path(__file__).resolve().parents[1] / "schemas" / "001_podcast_research.sql"
        sql = sql_path.read_text(encoding="utf-8")
        db = sqlite3.connect(":memory:")
        db.executescript(sql)
        db.executescript(sql)
        tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertTrue({"podcast_topics", "podcast_sources", "podcast_topic_evidence", "podcast_episode_results"} <= tables)
        self.assertFalse({"research_items", "waitlist", "rooms"} & tables)
        db.close()

if __name__ == "__main__":
    unittest.main()
