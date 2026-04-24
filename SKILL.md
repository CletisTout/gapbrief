---
name: gapbrief
description: Generates GEO content briefs from Peec AI visibility gaps. Use this skill whenever the user wants to (1) analyze where their brand is losing AI search visibility, (2) produce content briefs informed by LLM citation data, (3) audit gaps between their brand and competitors across AI engines (ChatGPT, Gemini, Perplexity, Google AIO, Claude), or (4) turn Peec project data into actionable SEO/GEO work. Trigger on phrases like "find my AI gaps", "where is [brand] missing in ChatGPT", "build a GEO brief", "what should I write to rank in AI Overviews", or anytime the user mentions Peec alongside content strategy. Also trigger when user provides a Peec project ID and asks for content recommendations.
---

# GapBrief — From Peec AI Gaps to Content Briefs

A repeatable workflow that turns AI visibility gaps into ready-to-execute content briefs.

**Built by [SYZYGY Performance](https://syzygy.de) for the Peec MCP Challenge 2026.**

## What this skill does

Given a Peec project ID, GapBrief:

1. Pulls **URL-level gap data** from the Peec MCP — pages that win AI citations where the own brand is absent but ≥2 competitors appear.
2. Clusters gaps by **prompt, topic, and winning competitor** to surface the highest-leverage targets.
3. Fetches the top-winning pages via Firecrawl/web_fetch and extracts the **entities, argument patterns, and format signals** that LLMs reward.
4. Generates a **publish-ready content brief** in Markdown (optionally Google Doc / Notion) with: target prompts, entity checklist, H2 skeleton, FAQ slots, internal linking candidates, schema recommendations, and a *modeled visibility lift*.
5. Closes the loop by scheduling a **7-day retrieval check** that re-queries Peec to verify whether the published content actually moved the needle.

## When to use

Trigger this skill when the user:
- Has a Peec project and asks "what should we write next?"
- Mentions "gap analysis", "GEO brief", "content brief for AI search", "LLM citations"
- Asks to turn Peec data into agency deliverables (client-facing briefs)
- Wants to prioritize SEO/content work based on AI search signal, not keyword volume

## Workflow

### Step 1 — Scope

Ask the user (or infer from context):
- Which Peec project? (use `Peec AI MCP:list_projects` if unclear)
- Date range (default: last 30 days)
- Focus: whole project, a single topic, a single tag, or a single prompt?
- Minimum competitor threshold (default: gap ≥ 2)
- Output format (Markdown / Google Doc / Notion)

If the user names a brand/client but no project ID, list projects and match by name.

### Step 2 — Pull gap data

Call `scripts/gap_analyzer.py`:

```bash
python scripts/gap_analyzer.py \
  --project-id <peec_project_id> \
  --start-date <YYYY-MM-DD> \
  --end-date <YYYY-MM-DD> \
  --topic-id <optional> \
  --min-gap 2 \
  --output examples/<project>/gaps.json
```

This script:
- Calls `Peec AI MCP:get_url_report` with `filters: [{field: "gap", operator: "gte", value: 2}]` and `dimensions: ["prompt_id"]`
- Calls `Peec AI MCP:get_brand_report` for context (own brand visibility per prompt)
- Calls `Peec AI MCP:list_prompts`, `list_brands`, `list_topics` to resolve IDs → labels
- Computes an **Impact Score** per gap URL:

  ```
  impact = retrievals × citation_rate × prompt_frequency × competitor_strength
  ```

  where `competitor_strength` is the mean SoV of competitors mentioned in that URL.
- Outputs a ranked JSON of gap clusters (grouped by prompt, then by winning URL).

### Step 3 — Extract winning content patterns

For each top-ranked gap prompt, call `scripts/extract_patterns.py`:

```bash
python scripts/extract_patterns.py \
  --gaps examples/<project>/gaps.json \
  --top-n 5 \
  --output examples/<project>/patterns.json
```

This fetches the top 5 winning URLs per prompt (via `web_fetch`) and asks Claude to extract:
- **Entities** (products, specs, technologies) with frequency counts
- **Argument structure** (what claims are made, in what order)
- **Format** (listicle / comparison / how-to / discussion)
- **E-E-A-T signals** (author bio, test methodology, first-hand data)
- **FAQ patterns** (recurring questions)
- **Schema hints** (visible structured data or likely schema.org types)

### Step 4 — Generate the brief

Call `scripts/brief_generator.py`:

```bash
python scripts/brief_generator.py \
  --gaps examples/<project>/gaps.json \
  --patterns examples/<project>/patterns.json \
  --own-brand <brand_id> \
  --output examples/<project>/brief-<slug>.md
```

The script renders the brief using `assets/brief-template.md` with sections:

1. **Context** — which prompts, which models, current own-brand visibility
2. **Competitive Landscape** — who wins this prompt cluster, with what URLs, at what citation rate
3. **Required Entities** — must-mention entities, prioritized by frequency across winning sources
4. **Recommended Structure** — H2 skeleton based on winning-source patterns
5. **FAQ Block** — questions the content must answer
6. **E-E-A-T Requirements** — author, methodology, evidence standards
7. **Internal Linking** — candidate own-domain URLs to link from/to
8. **Schema Recommendations** — schema.org types and properties
9. **Modeled Lift** — predicted visibility change, based on current gap size
10. **Validation Plan** — automatic 7-day re-check via Peec

### Step 5 — Schedule validation

Write a cron entry or GitHub Action that re-runs `gap_analyzer.py` 7 days after publish and diffs against the original gaps.json to report lift. See `scripts/validate_lift.py`.

## Scripts

- `scripts/peec_client.py` — Thin wrapper around the Peec MCP tool calls (via the MCP HTTP API when running outside an MCP-enabled host).
- `scripts/gap_analyzer.py` — Gap pulling + Impact Score computation.
- `scripts/extract_patterns.py` — Winning-URL fetch + pattern extraction via Claude.
- `scripts/brief_generator.py` — Final brief rendering.
- `scripts/validate_lift.py` — 7-day retrieval check.

## Output contract

Every brief must include:
- A **YAML front-matter block** with `project_id`, `prompt_ids`, `generated_at`, `own_brand`, `impact_score`, `expected_lift`.
- **Numeric citations** for every claim (which Peec row / which URL / which model).
- A **reproducibility command** at the bottom: the exact CLI invocation that regenerates this brief.

See `examples/project-1/brief-gaming-streaming.md` for a full reference output.

## Safety & anonymization

When sharing briefs publicly (e.g., contest submissions, case studies), strip:
- Client names (unless explicitly approved)
- Internal pricing or strategy notes from linked documents
- Any competitor URL list that identifies specific deal data

The `--anonymize` flag on `brief_generator.py` replaces real brand names with `[Brand A/B/C]` placeholders.

## Related

- Peec MCP docs: https://docs.peec.ai/mcp/introduction
- GEO methodology: see SYZYGY's GEO service model (Exploration → Mapping → Strategie → Brand → Iteration)
- Community hashtag: `#BuiltWithPeec`
