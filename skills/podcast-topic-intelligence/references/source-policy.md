# Source policy and connector roadmap

This document describes preferred sources and access methods, not live connections. Verify availability and usage permissions before any integration.

| Market | Platform / source | Initial access | What it can establish | What it does not establish |
| --- | --- | --- | --- | --- |
| Global | Google Trends | Official interface, exports and public RSS where available | Relative search interest or individual trending entries in their documented time scope | Overall social conversation or podcast listens |
| Global | YouTube | Public search and documented YouTube Data API with authorized quota | Public video metadata, counts and creator competition at capture time | Unique audience demand or causality |
| Global | Reddit | Permitted public pages and documented access paths | User wording, recurring discussion questions | Representative population statistics |
| Global | TikTok | Official Creative Center and permitted access | Advertised trend and video indicators in the product's stated scope | Unrestricted global search volume |
| China | Douyin | Official indices and approved access | Chinese-language interest within the published metric definitions | Unrestricted raw user data |
| China | Xiaohongshu | Public pages or authorized exports; manual checking first | Visible posts, questions, comments and qualitative concerns | Full platform coverage or verified demand |
| China | Bilibili | Public pages and authorized platform APIs | Video discussions and public metadata | Search demand outside the platform |
| China | Baidu Index | Official interface | Search-index movement for selected terms | Actual absolute search counts unless explicitly provided |
| Multisource | RSSHub | Feeds allowed by supported routes and origin sites | Article/entry discovery with dates and links | A complete, unbiased platform firehose |

## Connector selection

Phase 1: manually collected official/public source URLs. Reuse ideas from BLUORADA's source records and Google Trends RSS parser, with attribution to its own implementation; do not copy commerce logic directly.

Phase 2: add a provider adapter only after confirming API terms, permissions, request quota, rate limits, costs, freshness, and sample output. Store the original URL and timestamp independently of provider formatting. Accept a nullable value for every unsupported metric.

Phase 3: optionally automate recurring collection. Record each run's successes, failures, source coverage and observation time; do not silently infer zero interest from a failed connector.

## Evidence rules

- Use absolute HTTP(S) source URLs, observed-on dates, exact attributed claims and a platform/market.
- Check the original publication date; observed-on is not the same as published-on.
- At least two distinct source URLs on two distinct named platforms are required for the local ranker's editorial_review gate. This establishes research breadth, not that a trend is statistically verified.
- Cross-market claims require actual Chinese and global evidence. Otherwise explicitly state only the observed market.
- Treat comments and self-selected discussion communities as nonrepresentative.
- Popularity growth requires comparable measurements across time or a clearly defined platform-provided growth indicator. Never infer growth from two anecdotes.
- Distinguish verified source existence from verified audience demand. Preserve counter-evidence and uncertainty.
