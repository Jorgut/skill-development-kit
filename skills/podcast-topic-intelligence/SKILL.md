---
name: podcast-topic-intelligence
description: Research and prioritize bilingual podcast topics using traceable Chinese and international social-media evidence, editorial ratings, and a repeatable review process. Use for podcast topic discovery, trend validation, cross-market comparison, and episode research briefs.
---

# Podcast Topic Intelligence

A reusable editorial research workflow by ArchIntera. It is a Skill, not a live trend service or an MCP server. Do not claim to have monitored a platform without actually accessing sources.

## Goal
Produce evidence-backed Chinese/English podcast topic recommendations about design, architecture, HCI, AI, cities, culture and the human experience. Preserve a distinctive human editorial point of view rather than copying viral content.

## Workflow
1. **Define the episode decision.** Confirm intended audience, domain, languages and publishing window using context already available. Default to one substantive 20–30-minute episode and 2–3 derivative short clips.
2. **Gather traceable signals.** Start with official trend tools, public RSS/search, platform native discovery or authorized connectors. Prioritize fresh primary pages, then seek counter-evidence. Read references/source-policy.md. Never guess search volume, engagement, sales, platform rank, momentum or creator results.
3. **Iterative research.** Search broadly, inspect source relevance, narrow to the missing questions and stop after at most three retrieval passes. This reuses the approach documented in Jorgut/iterative-retrieval-skill; it does not require importing that repository.
4. **Separate signal types.** Label each fact as measured trend, first-hand discussion, editorial analysis, or hypothesis. An external search URL is a research path, not evidence of popularity. Capture publisher, URL, original date, observation date, market, exact supported claim and caveats.
5. **Find the conversation gap.** Compare Chinese-language and international perspectives only when both are actually observed. Describe missing market coverage explicitly. Seek an original question and a reason this host is qualified to discuss it.
6. **Rate topic candidates.** Independently assess audience need, expertise fit, depth, originality, distribution potential and production feasibility on a 0–5 editorial rubric. Weights and definitions are in references/scoring-rubric.md. Ratings are judgment, never claimed to be measured platform statistics.
7. **Run the optional local ranker.** Prepare input using references/data-contract.md. Execute: python3 skills/podcast-topic-intelligence/scripts/rank_topics.py --input topics.json --output ranked.json. The ranker reads local JSON only; it performs no web retrieval and never updates a database.
8. **Human editorial gate.** Prioritize candidates marked editorial_review. Require a checked topic angle and at least one source-backed audience question before marking an episode approved. Scores alone do not justify recording.
9. **Prepare the episode brief.** Output Chinese first then English: central question, who cares, dated source links, differentiated host perspective, argument/counterargument, 20–30-minute outline, three hooks, limitations, and next verification steps. Do not present examples as live findings.
10. **After publishing.** Record actual episode performance and corrections in an editorial log. Compare topics with the same measurement window. Learn from patterns, but do not change weights automatically without a recorded editorial decision.

## Boundaries
- This Skill has no credentials, secret handling, scraper, scheduled worker, publishing rights or authenticated platform access.
- Do not bypass platform restrictions, scrape private accounts or reuse cookies.
- Avoid ungrounded numerical scores for platform popularity or fabricated listener research.
- No production migrations: see schemas/001_podcast_research.sql for an optional standalone SQLite reference design.
- BLUORADA is a separate commerce research product. Reuse its provenance discipline and data design principles, not its production tables, D1 binding or access controls.
- PARENO remains an optional downstream writing assistant, not a source of trend statistics.
- No automatic content publication, recording or edits to other repositories.

## Quality gate
The output is useful only if a reader can open each cited source, identify the actual evidence, understand the market/time window, distinguish judgments from measurements and trace why a topic was recommended. Missing sources stay visible and block editorial-review eligibility.

## References
- references/source-policy.md: source access and quality policy
- references/scoring-rubric.md: ranking criteria
- references/data-contract.md: local input/output format
- schemas/001_podcast_research.sql: optional future storage schema
