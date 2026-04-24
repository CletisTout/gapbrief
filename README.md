# GapBrief

> **From Peec AI gaps to publish-ready content briefs — in one command.**
>
> A Claude Code skill that turns LLM visibility gaps into GEO briefs your
> content team can execute on Monday morning.

[![Built with Peec](https://img.shields.io/badge/Built%20with-Peec-5b21b6)](https://peec.ai)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-d97706)](https://docs.claude.com/en/docs/build-with-claude/claude-code)
[![License MIT](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)

**Built by [SYZYGY Performance](https://syzygy.de) for the [Peec MCP Challenge
2026](https://peec.ai/mcp-challenge).**

---

## What it does

Modern brands don't just need to rank in Google — they need to be retrieved
and cited by ChatGPT, Gemini, Perplexity, Claude, and Google AI Overviews.
Peec AI tracks that visibility. **GapBrief turns that data into action.**

Given a Peec project ID, GapBrief:

1. Pulls every URL that wins AI citations for prompts where your brand is
   absent but competitors are present (the **gap set**).
2. Ranks those gaps by a composite **Impact Score** — retrievals, citation
   rate, prompt frequency, competitor strength.
3. Fetches the top winning URLs and extracts the entities, argument
   structure, format, and E-E-A-T signals they use.
4. Renders a Markdown content brief with an H2 skeleton, FAQ block, entity
   checklist, schema recommendations, and a modeled visibility lift.
5. Schedules a **7-day validation run** that re-queries Peec to check whether
   the published page actually moved the needle.

## Why it's different

| Other GEO tools | GapBrief |
|---|---|
| Dashboards you stare at | Briefs your writers execute |
| "Your visibility dropped" | "Here's the page that took your citations, and the structure of your reply" |
| Averages across topics | Prompt-level surgical targets |
| One-shot LLM prompt | Repeatable `python` + cron workflow |
| Proprietary tool | MIT-licensed Claude Code skill |

## Quick start

### 1. Install

```bash
git clone https://github.com/syzygy-performance/gapbrief
cd gapbrief
pip install -r requirements.txt
export PEEC_API_KEY=pk_...
export ANTHROPIC_API_KEY=sk-ant-...
export FIRECRAWL_API_KEY=fc-...  # optional, falls back to requests
```

### 2. Install as a Claude Code skill

```bash
claude code skill install ./gapbrief
```

Then in any Claude Code session:

> "Build a GEO brief for my Peec project, Topic X."

Claude picks up the skill, runs the three scripts, and drops the brief into
your workspace.

### 3. Or run the pipeline by hand

```bash
# Step 1 — pull gaps and compute Impact Score
python scripts/gap_analyzer.py \
  --project-id or_4495d51c-... \
  --start-date 2026-03-18 --end-date 2026-04-16 \
  --topic-id to_88664c56-... \
  --output examples/project-1/gaps.json

# Step 2 — fetch winning URLs and extract patterns
python scripts/extract_patterns.py \
  --gaps examples/project-1/gaps.json \
  --top-n 5 \
  --output examples/project-1/patterns.json

# Step 3 — generate the brief
python scripts/brief_generator.py \
  --gaps examples/project-1/gaps.json \
  --patterns examples/project-1/patterns.json \
  --cluster-index 0 \
  --output examples/project-1/brief-gaming-streaming.md

# Step 4 (one week later) — validate lift
python scripts/validate_lift.py \
  --baseline examples/project-1/gaps.json \
  --project-id or_4495d51c-... \
  --prompt-id pr_2ee86e30-... \
  --output examples/project-1/lift-report-week1.md
```

## Impact Score, explained

```
impact = retrievals × citation_rate × prompt_frequency × competitor_strength
```

| Factor | Why it's in the formula |
|---|---|
| **retrievals** | A URL has to actually be pulled by the LLM to matter. |
| **citation_rate** | Being retrieved but not cited = low signal. Cited = strong signal. |
| **prompt_frequency** | Winning a rare prompt is worth less than winning a common one. |
| **competitor_strength** | Getting beaten by heavy hitters matters more than by a niche player. |

The multiplicative form means *any* factor at zero zeros out the score —
which is exactly right. A URL with 100 retrievals but 0 citation rate is
noise, not signal.

## Example output

See the generated briefs in `examples/project-1/` for full examples generated
from real Peec data.

Key metrics from a typical brief:
- Project-wide own brand SoV in a topic: **44%**
- Own brand mention rate on a specific gap prompt: **0%** (competitors dominate)
- Modeled lift from publishing the briefed page: **+15–25 pp** visibility
  on the target prompt over 30 days

## Repository layout

```
gapbrief/
├── SKILL.md                      # Claude Code skill definition
├── scripts/
│   ├── peec_client.py            # Peec MCP HTTP wrapper
│   ├── gap_analyzer.py           # Gap pull + Impact Score
│   ├── extract_patterns.py       # Winning-URL pattern extraction
│   ├── brief_generator.py        # Brief rendering
│   └── validate_lift.py          # 7-day retrieval check
├── examples/
│   └── samsung-tv/
│       ├── gaps.json             # Real gap data (anonymizable)
│       ├── patterns.json         # Extracted patterns
│       └── brief-gaming-streaming.md
├── docs/
│   ├── dashboard.html            # Visual gap dashboard (optional)
│   └── methodology.md            # Impact Score derivation
└── assets/
    └── brief-template.md         # Brief skeleton
```

## Extending it

- **Swap the pattern-extractor**: `extract_patterns.py` accepts any markdown
  source — plug in your own fetch if Firecrawl is blocked.
- **Custom Impact weighting**: override `build_gap_rows()` in
  `gap_analyzer.py` to emphasize citation_rate over competitor_strength (or
  vice versa) to match your strategic priorities.
- **Output to Google Docs / Notion**: replace `write_text()` in
  `brief_generator.py` with a Google Docs API call or a
  [Notion MCP](https://github.com/makenotion/notion-mcp-server) call.
- **Scheduled runs**: the whole pipeline is CLI-first and cron-friendly. Run
  it weekly on all your Peec projects and ship briefs as PRs.

## Who this is for

- **SEO / GEO agencies** running multi-brand Peec portfolios that need to
  convert dashboard insights into brief-shaped deliverables for clients.
- **In-house content teams** that already have Peec but want a repeatable
  link from "where are we losing?" to "here's what we'll write next".
- **Developers** who want a reference implementation of the Peec MCP server
  in a real workflow.

## Contributing

PRs welcome. Please keep scripts single-file and CLI-first — the whole point
of this tool is that it survives a move between machines.

## License

MIT. See [LICENSE](./LICENSE).

## Credits

- [Peec AI](https://peec.ai) for the MCP server and the challenge that
  prompted this build.
- [Anthropic](https://anthropic.com) for Claude Code.
- [Firecrawl](https://firecrawl.dev) for robust page extraction.

---

Built with **#BuiltWithPeec** · [SYZYGY Performance](https://syzygy.de)
