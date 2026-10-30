-- OPTIONAL STANDALONE REFERENCE SCHEMA ONLY.
-- Do not execute against BLUORADA or any existing production D1 database.
-- All dates are ISO-8601 text. Store evidence without implying verified trend growth.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS podcast_topics (
  id TEXT PRIMARY KEY,
  title_zh TEXT NOT NULL,
  title_en TEXT NOT NULL,
  angle_zh TEXT NOT NULL DEFAULT '',
  angle_en TEXT NOT NULL DEFAULT '',
  topic_status TEXT NOT NULL DEFAULT 'candidate'
    CHECK (topic_status IN ('candidate','researching','editorial_review','approved','published','archived')),
  ratings_json TEXT NOT NULL DEFAULT '{}',
  score_100 INTEGER CHECK (score_100 IS NULL OR (score_100 BETWEEN 0 AND 100)),
  score_method TEXT NOT NULL DEFAULT 'editorial-provisional-v0',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS podcast_sources (
  id TEXT PRIMARY KEY,
  platform TEXT NOT NULL,
  market TEXT NOT NULL CHECK (market IN ('CN','GLOBAL')),
  original_url TEXT NOT NULL,
  publisher TEXT NOT NULL DEFAULT '',
  published_at TEXT,
  observed_at TEXT NOT NULL,
  claim TEXT NOT NULL,
  measurement_json TEXT NOT NULL DEFAULT '{}',
  UNIQUE(original_url, observed_at)
);

CREATE TABLE IF NOT EXISTS podcast_topic_evidence (
  topic_id TEXT NOT NULL REFERENCES podcast_topics(id) ON DELETE CASCADE,
  source_id TEXT NOT NULL REFERENCES podcast_sources(id) ON DELETE CASCADE,
  relationship TEXT NOT NULL DEFAULT 'supports'
    CHECK (relationship IN ('supports','contradicts','context')),
  PRIMARY KEY (topic_id, source_id)
);

CREATE TABLE IF NOT EXISTS podcast_episode_results (
  id TEXT PRIMARY KEY,
  topic_id TEXT NOT NULL REFERENCES podcast_topics(id) ON DELETE CASCADE,
  channel TEXT NOT NULL,
  published_at TEXT,
  measurement_window TEXT NOT NULL DEFAULT '',
  views INTEGER CHECK (views IS NULL OR views >= 0),
  listens INTEGER CHECK (listens IS NULL OR listens >= 0),
  comments INTEGER CHECK (comments IS NULL OR comments >= 0),
  raw_metrics_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_podcast_topics_status ON podcast_topics(topic_status);
CREATE INDEX IF NOT EXISTS idx_podcast_sources_platform_observed ON podcast_sources(platform, observed_at);
CREATE INDEX IF NOT EXISTS idx_podcast_episode_topic ON podcast_episode_results(topic_id);
