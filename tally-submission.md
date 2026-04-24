# Tally-Submission-Text

**Zielformular:** peec.ai/countdown-submissions-mcp-challenge (öffnet 20. April)
**Bewertungsgewichtung:** Usefulness 40% · Creativity 30% · Execution 20% · Community Impact 10%

---

## Workflow Name

GapBrief — From Peec AI Gaps to Publish-Ready Content Briefs

## One-sentence pitch (max 140 chars)

A Claude Code skill that turns Peec AI visibility gaps into publish-ready content briefs with competitor content analysis and 7-day validation. MIT-licensed.

## Category (optional to self-select)

Content Optimization (primary) — but it also produces competitive-analysis signal as a byproduct.

## Tools used

Peec MCP · Claude Code · Anthropic API (Claude Sonnet 4) · Firecrawl MCP (multi-URL content scraping + competitor analysis) · Python 3.11

## Problem it solves

Every SEO/GEO practitioner with access to Peec has the same friction point: the gap between "our visibility dropped on this topic" and "here is the page we will publish next Tuesday to fix it" is still a two-hour manual job per gap. Dashboards visualize gaps. They don't deliver briefs. GapBrief closes that gap. Given a Peec project ID and a visibility gap, it outputs a Markdown content brief — with adaptive H2 skeleton (10-14 sections by complexity), competitor content analysis, entity checklist, FAQ block, schema recommendations, search query context, and modeled lift — that a content writer can execute on Monday morning. Then, seven days after publish, it re-queries Peec to validate whether the page actually moved the needle.

## How it works

1. **Gap pull** — `gap_analyzer.py` calls `get_url_report` with the `gap` filter to get every URL winning AI citations for prompts where the own brand is absent but ≥2 competitors are present. It cross-joins against `get_brand_report` for SoV context and `list_prompts`/`list_topics`/`list_brands` to resolve IDs to labels.

2. **Impact scoring** — A composite score per gap: `retrievals × citation_rate × prompt_frequency × competitor_strength`. Multiplicative, not additive — any zero factor means zero impact. Prioritizes surgically.

3. **Multi-URL competitor analysis** — FOR EACH GAP: Fetches up to 3 competing URLs with retrieval & citation counts. Firecrawl scrapes each URL and extracts:
   - Content structure (H2-count, word count, readability)
   - Best practices (FAQ patterns, comparison tables, CTA placement)
   - Entity patterns & E-E-A-T signals
   - Generates "Competitor Content Analysis" section in the brief

4. **Search intent mapping** — Analyzes 6-10+ search queries that lead to each gap. Shows exactly what users are asking, surfacing intent patterns the writer must address.

5. **Brief rendering** — `generate_gap_brief.py` synthesizes gap data, competitor content analysis, and search intent into a Markdown brief with:
   - Adaptive H2 structure (10/12/14 sections by impact complexity)
   - FAQ template (8-12 questions matched to competitor patterns)
   - Schema recommendations (Article, FAQPage, ComparisonChart)
   - Entity & brand positioning checklist
   - YAML frontmatter with all metrics inline

6. **Validation loop** — `validate_lift.py` is cron-scheduled to re-query Peec seven days after publish and report lift against the original baseline.

## What makes it different

- **Every claim traces to a data row.** The brief cites Peec retrievals, citation rates, and search queries inline — not vague "AI says" language.

- **Intelligent multi-URL competitor analysis.** Each gap analyzes up to 3 competitor URLs, scrapes their exact content structure, and surfaces which best practices (FAQ patterns, comparison table formats, CTA strategies) your content writer should match or exceed.

- **Search query intent context.** Each gap includes 6-10+ search queries showing exactly what users are asking — not guessing at intent.

- **Adaptive content complexity.** The system automatically determines whether a gap needs 10, 12, or 14 H2 sections based on impact score, from casual consumer content to technical expert content.

- **The 7-day validation loop closes the loop** that every other GEO tool leaves open. Publishing without validation is hope; publishing with validation is strategy.

- **Shipped as a Claude Code skill**, not a SaaS dashboard. Version-controllable, reproducible across machines, installable in one command.

- **CLI-first and cron-friendly.** Runs overnight for every Peec project in a portfolio. Batch-process 50+ gaps in minutes.

- **Impact Score formula is explicit and tunable** — agencies can re-weight factors for strategic priorities without forking.

## Real-data validation

The submitted example was generated from a real 14-project Peec portfolio at SYZYGY Performance, focused on the Own Brand TV project's Gaming topic. Finding: Own Brand holds 44% topic-wide SoV but 0% on the highest-impact gap prompt ("best smart tvs for gaming and streaming") — the brief provides the exact page structure from 3 scraped competitor URLs, entity checklist, and schema plan to close that gap, with a modeled +25 pp lift over 30 days. The brief includes competitor content analysis showing which YouTube channels, Reddit threads, and review sites are winning citations — and exactly how their content is structured, so Own Brand can match or exceed them.

## Links

- Repo (MIT): https://github.com/CletisTout/gapbrief
- Demo video: [Loom link, 5:00]
- Example brief: [Beispiel-Brief aus generate_gap_brief.py Output]
- Visual dashboard: https://github.com/CletisTout/gapbrief/blob/main/dashboard.html
- LinkedIn post (#BuiltWithPeec): [wird nach Submission gepostet]

## Who built it

Tim Brock, SEO Consultant

## Public-sharing opt-in

Yes — repo is MIT-licensed, dashboard is public, LinkedIn post is tagged with #BuiltWithPeec.

---

## Why it hits each judging criterion

**Usefulness (40%)** — Solves the single most common agency workflow bottleneck for Peec users: converting dashboard insight into executable content briefs with competitor benchmarking. Replicable to any Peec project in any vertical (Finance, Pharma, FMCG, Tech, Retail).

**Creativity (30%)** — The multiplicative Impact Score (not a linear "visibility drop" metric), the intelligent multi-URL competitor content analysis (most tools stop at "competitors mention this topic"), the search query intent mapping (shows user perspective, not just SEO perspective), the 7-day retrieval-validation loop (closes a loop every competitor leaves open), and the packaging as a Claude Code skill (not a SaaS) are five non-obvious design choices, each justified by the problem.

**Execution (20%)** — Clean CLI-first Python, typed Peec client, Firecrawl content scraping with graceful fallback, anonymization flag, reproducibility command embedded in every output, real data validation from a 14-project portfolio. Schema generation (Article + FAQ + Comparison). Batch processing for 50+ gaps overnight.

**Community Impact (10%)** — MIT license, public repo, visual dashboard on GitHub Pages, SYZYGY blog post explaining the methodology, LinkedIn distribution with #BuiltWithPeec. Installable in three lines by any other Peec user. Extensible: agencies can modify impact score weights, add custom H2 structures, or extend with their own content patterns.
