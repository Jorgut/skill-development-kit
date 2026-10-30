# Skill Development Kit

Toolkit for creating, discovering, and configuring AI coding assistant skills — from extracting patterns to marketplace search.

## Skills

| Skill | Description |
|---|---|
| **skill-from-github** | Create skills by learning from high-quality GitHub projects |
| **skill-from-masters** | Create high-quality skills from real-world case studies |
| **skill-from-notebook** | Extract methodologies from documents/examples to create executable skills |
| **search-skill** | Search and recommend AI coding assistant skills from trusted marketplaces |
| **project-guidelines-example** | Template for documenting project architecture and coding patterns |
| **podcast-topic-intelligence** | Bilingual, evidence-gated China/global podcast research, editorial ranking, and episode briefing |

## Install

```bash
# OpenCode
ln -s "$PWD/skills/skill-from-github" ~/.config/opencode/skills/
```

## License

MIT

## Podcast Topic Intelligence

A source-agnostic Skill for evaluating Chinese and international discussions without fabricating trend metrics. It includes a local Python editorial ranker, tests, a source-access policy, and an optional isolated SQLite schema. No live platform data connections or production migrations are enabled.

See [Skill instructions](skills/podcast-topic-intelligence/SKILL.md).
