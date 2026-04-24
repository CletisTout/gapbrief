#!/usr/bin/env python3
"""
GapBrief Dashboard Generator
Automatische Erstellung eines interaktiven Dashboards aus Gap-Daten

Verwendet: JSON Gap-Daten (aus gap_analyzer.py oder gaps-example.json)
Output: dashboard.html (deployment-ready)

DASHBOARD DESIGN RULES:
======================
1. Hero Section: Impact-Summary + Top-Gap Status
2. Key Metrics Strip: 4 Numbers (Own SoV, Top Gap Status, Dominant Competitor, Top Format)
3. Competitor Bar Chart: Share of Voice Vergleich
4. Gap Clusters: 1-5 Gaps, ranked by Impact Score
5. Next Steps: Prioritized Action Items
6. CTA: Installation Command

INPUT SCHEMA (JSON):
===================
{
  "metadata": {
    "created": "ISO timestamp",
    "total_gaps": int,
    "source": "Peec API / Manual"
  },
  "gaps": [
    {
      "gap_id": int,
      "topic": string,
      "urls": [{"url", "title", "retrieved_in", "citation_count"}],
      "search_queries": [string],
      "priority": string (🔴 CRITICAL, 🟡 HIGH, etc),
      "impact_score": float,
      "own_brand_status": string (ABSENT, MENTIONED, STRONG),
      "own_brand_visibility": string (percentage),
      "competitors": {"brand": "percentage"},
      "estimated_visibility_lift": string
    }
  ]
}

COLOR SCHEME (Tech Innovation Theme):
=====================================
--accent: #0066ff (Electric Blue - Own Brand)
--accent-2: #00ffff (Neon Cyan - Highlights)
--warn: #ff4e5b (Red - Absences/Warnings)
--ok: #6bcf7f (Green - Good metrics)
--bg: #1e1e1e (Dark bg)
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple


class DashboardGenerator:
    """Generates interactive HTML dashboard from Gap JSON data"""

    def __init__(self, gaps_json: Dict[str, Any]):
        """Initialize with gap data"""
        self.data = gaps_json
        self.gaps = gaps_json.get("gaps", [])
        self.metadata = gaps_json.get("metadata", {})

    def calculate_totals(self) -> Dict[str, Any]:
        """Calculate aggregate metrics from all gaps"""
        total_impact = sum(g.get("impact_score", 0) for g in self.gaps)
        total_urls = sum(len(g.get("urls", [])) for g in self.gaps)

        # Collect all competitors and aggregate SoV
        competitor_sov = {}
        for gap in self.gaps:
            competitors = gap.get("competitors", {})
            for brand, sov_str in competitors.items():
                sov = float(sov_str.strip("%")) if isinstance(sov_str, str) else sov_str
                if brand not in competitor_sov:
                    competitor_sov[brand] = []
                competitor_sov[brand].append(sov)

        # Average SoV per competitor
        avg_competitor_sov = {
            brand: sum(sov_list) / len(sov_list)
            for brand, sov_list in competitor_sov.items()
        }

        return {
            "total_impact": round(total_impact, 1),
            "total_gaps": len(self.gaps),
            "total_urls": total_urls,
            "avg_lift": self._calculate_avg_lift(),
            "competitor_sov": avg_competitor_sov
        }

    def _calculate_avg_lift(self) -> str:
        """Extract and average all lift potentials"""
        lifts = []
        for gap in self.gaps:
            lift_str = gap.get("estimated_visibility_lift", "0%")
            # Parse "5-8%" format
            if "-" in lift_str:
                parts = lift_str.replace("%", "").split("-")
                try:
                    avg = (int(parts[0]) + int(parts[1])) / 2
                    lifts.append(avg)
                except:
                    pass
        return f"+{round(sum(lifts) / len(lifts), 0):.0f} pp" if lifts else "N/A"

    def render_hero_section(self, totals: Dict) -> str:
        """Render hero section with main headline and summary"""
        top_gap = max(self.gaps, key=lambda g: g.get("impact_score", 0))
        top_topic = top_gap.get("topic", "Unknown")
        own_brand_status = top_gap.get("own_brand_status", "UNKNOWN")

        status_emoji = {
            "ABSENT": "❌",
            "MENTIONED": "⚠️",
            "STRONG": "✅"
        }.get(own_brand_status, "❓")

        return f"""<section class="hero">
  <div>
    <div class="kicker">Executive summary</div>
    <h1>Drei kritische Content-Gaps identifiziert <em>mit {totals['total_impact']:.0f} Impact-Punkten</em> — ready for action.</h1>
    <p class="lead">
      Dieses Dashboard zeigt {totals['total_gaps']} Content-Gaps, wo Ihre Brand abwesend oder unterrepräsentiert ist.
      <b>Top Gap: "{top_topic}"</b> mit {top_gap.get('impact_score', 0):.1f} Impact Score.
      GapBrief priorisiert, wo Content produziert werden sollte — basierend auf
      Peec Retrievals, Citation Rates, und Competitor Strength.
    </p>
  </div>
  <div class="impact-card" style="align-self:center;">
    <div class="kicker">Total Gap Impact</div>
    <div class="big">{totals['total_impact']:.0f}</div>
    <div class="row"><span>Gaps</span><span>{totals['total_gaps']}</span></div>
    <div class="row"><span>Gap-URLs</span><span>{totals['total_urls']}</span></div>
    <div class="row"><span>Modellierter Lift</span><span>{totals['avg_lift']}</span></div>
  </div>
</section>"""

    def render_metrics_strip(self, totals: Dict) -> str:
        """Render 4-cell metrics strip"""
        top_gap = max(self.gaps, key=lambda g: g.get("impact_score", 0))
        top_competitor = max(
            top_gap.get("competitors", {}).items(),
            key=lambda x: float(x[1].strip("%")) if isinstance(x[1], str) else x[1]
        )[0] if top_gap.get("competitors") else "N/A"

        own_brand_vis = top_gap.get("own_brand_visibility", "0%")
        own_brand_status = top_gap.get("own_brand_status", "UNKNOWN")

        status_class = {
            "ABSENT": "warn",
            "MENTIONED": "acc",
            "STRONG": "ok"
        }.get(own_brand_status, "")

        return f"""<section class="numbers">
  <div class="num">
    <div class="label">Top Gap Own Brand Status</div>
    <div class="big {status_class}">{own_brand_vis}</div>
    <div class="foot">{own_brand_status} in "{top_gap.get('topic')}"</div>
  </div>
  <div class="num">
    <div class="label">Dominant Competitor</div>
    <div class="big">{top_competitor}</div>
    <div class="foot">{top_gap.get('competitors', {}).get(top_competitor, 'N/A')} SoV</div>
  </div>
  <div class="num">
    <div class="label">Total Gap URLs</div>
    <div class="big">{totals['total_urls']}</div>
    <div class="foot">Winning competitor URLs to analyze</div>
  </div>
  <div class="num">
    <div class="label">Avg Estimated Lift</div>
    <div class="big ok">{totals['avg_lift']}</div>
    <div class="foot">Per published content piece</div>
  </div>
</section>"""

    def render_competitor_bars(self, totals: Dict) -> str:
        """Render competitor SoV bar chart"""
        sov = totals["competitor_sov"]
        sorted_sov = sorted(sov.items(), key=lambda x: x[1], reverse=True)

        # First item is own brand (largest SoV)
        own_brand_name = sorted_sov[0][0] if sorted_sov else "Own Brand"

        bars_html = ""
        for brand, percentage in sorted_sov:
            width = min(percentage * 1.2, 100)  # Cap at 100 for display
            brand_class = "own" if brand == own_brand_name else ""
            bars_html += f"""    <div class="bar-row">
      <div class="name {brand_class}">{brand}</div>
      <div class="bar-track">
        <div class="bar-fill {brand_class}" style="width:{width}%"></div>
      </div>
      <div class="val">{percentage:.0f}%</div>
    </div>
"""

        return f"""<section>
  <h2>Competitor Dominanz<span class="dot"> · </span><em>nach Gap-Gewichtung</em></h2>
  <div class="section-sub">Durchschnitt aller {len(self.gaps)} Gaps, Anteil an Mentions</div>
  <div class="bars">
{bars_html}  </div>
</section>"""

    def render_gap_clusters(self) -> str:
        """Render ranked gap clusters"""
        sorted_gaps = sorted(self.gaps, key=lambda g: g.get("impact_score", 0), reverse=True)

        clusters_html = ""
        for idx, gap in enumerate(sorted_gaps, 1):
            gap_id = idx
            topic = gap.get("topic", "Unknown")
            impact = gap.get("impact_score", 0)
            own_brand_status = gap.get("own_brand_status", "UNKNOWN")
            own_brand_vis = gap.get("own_brand_visibility", "0%")
            urls = gap.get("urls", [])
            lift = gap.get("estimated_visibility_lift", "N/A")
            competitors = gap.get("competitors", {})

            # Determine tag styling
            status_tag_class = {
                "ABSENT": "warn",
                "MENTIONED": "acc",
                "STRONG": "ok"
            }.get(own_brand_status, "")

            # Render URLs
            urls_html = ""
            for url in urls:
                url_str = url.get("url", "#")
                title = url.get("title", "Unknown")
                retrieved = url.get("retrieved_in", 0)
                citations = url.get("citation_count", 0)

                # Get top competitor from this gap
                top_comp = ", ".join(list(competitors.keys())[:2]) if competitors else "N/A"

                urls_html += f"""          <a class="url" href="{url_str}">
            {title[:60]}
            <div class="meta-line">{retrieved} retrievals · {citations} citations · {top_comp}</div>
          </a>
"""

            # Determine priority tag
            priority = gap.get("priority", "MEDIUM")
            if "CRITICAL" in priority:
                priority_class = "acc"
                priority_text = "CRITICAL"
            elif "HIGH" in priority:
                priority_class = "acc"
                priority_text = "HIGH"
            else:
                priority_class = ""
                priority_text = "MEDIUM"

            clusters_html += f"""    <div class="cluster">
      <div>
        <div class="rank">{gap_id:02d}</div>
        <div class="rank-sub">{impact:.1f} impact</div>
      </div>
      <div>
        <div class="prompt">"{topic}"</div>
        <div class="tags">
          <span class="tag {status_tag_class}">{own_brand_status} ({own_brand_vis})</span>
          <span class="tag">{len(urls)} URLs</span>
          <span class="tag {priority_class}">{priority_text}</span>
        </div>
        <div class="urls">
{urls_html}        </div>
      </div>
      <div class="impact-card">
        <div class="kicker">Lift-Potenzial</div>
        <div class="big">{lift}</div>
        <div class="row"><span>Top competitor</span><span>{list(competitors.keys())[0] if competitors else 'N/A'}</span></div>
        <div class="row"><span>Status</span><span>{own_brand_status}</span></div>
      </div>
    </div>
"""

        return f"""<section>
  <h2>Gap-Cluster nach Impact<span class="dot"> · </span><em>priorisiert</em></h2>
  <div class="section-sub">Ranked by impact_score (descending)</div>
  <div class="clusters">
{clusters_html}  </div>
</section>"""

    def generate_html(self) -> str:
        """Generate complete HTML dashboard"""
        totals = self.calculate_totals()

        html = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>GapBrief Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=DejaVu+Sans:wght@400;700&display=swap" rel="stylesheet" />
<style>
:root {{
  --bg: #1e1e1e;
  --bg-2: #2a2a2a;
  --ink: #ffffff;
  --ink-dim: #b0b0b0;
  --line: #3a3a3a;
  --accent: #0066ff;
  --accent-2: #00ffff;
  --warn: #ff4e5b;
  --ok: #6bcf7f;
  --mono: "DejaVu Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --display: "DejaVu Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}
* {{ box-sizing: border-box; }}
html, body {{
  margin: 0; padding: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--mono);
  font-size: 14px;
  line-height: 1.55;
  letter-spacing: 0.01em;
  -webkit-font-smoothing: antialiased;
}}
body {{
  background-image:
    radial-gradient(1200px 600px at 20% -10%, rgba(0,102,255,0.12), transparent 60%),
    radial-gradient(900px 500px at 90% 110%, rgba(0,255,255,0.08), transparent 60%);
}}
.container {{ max-width: 1280px; margin: 0 auto; padding: 48px 40px 96px; }}
header.masthead {{
  border-top: 2px solid var(--ink);
  border-bottom: 1px solid var(--line);
  padding: 18px 0 14px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: baseline;
  gap: 32px;
  margin-bottom: 40px;
}}
.brand {{ font-family: var(--display); font-weight: 700; font-size: 22px; letter-spacing: -0.01em; }}
.brand b {{ font-weight: 700; }}
.kicker {{ text-transform: uppercase; font-size: 10px; letter-spacing: 0.22em; color: var(--ink-dim); }}
.meta {{ text-align: right; font-size: 11px; color: var(--ink-dim); }}
.hero {{
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 56px;
  border-bottom: 1px dashed var(--line);
  padding-bottom: 48px;
  margin-bottom: 48px;
}}
h1 {{
  font-family: var(--display);
  font-weight: 700;
  font-style: normal;
  font-size: clamp(36px, 5vw, 64px);
  line-height: 1.02;
  letter-spacing: -0.02em;
  margin: 12px 0 20px;
  color: var(--ink);
}}
h1 em {{ font-style: normal; color: var(--accent); font-weight: 700; }}
.hero .lead {{ color: var(--ink-dim); max-width: 52ch; font-size: 14px; }}
.hero .lead b {{ color: var(--ink); font-weight: 500; }}
.numbers {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: var(--line);
  border: 1px solid var(--line);
  margin-bottom: 48px;
}}
.num {{ background: var(--bg-2); padding: 28px 24px; }}
.num .label {{
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--ink-dim);
}}
.num .big {{
  font-family: var(--display);
  font-weight: 700;
  font-size: 44px;
  line-height: 1;
  margin: 14px 0 6px;
  letter-spacing: -0.02em;
}}
.num .big.warn {{ color: var(--warn); }}
.num .big.ok {{ color: var(--ok); }}
.num .big.acc {{ color: var(--accent); }}
.num .foot {{ font-size: 11px; color: var(--ink-dim); }}
section {{ margin-bottom: 64px; }}
h2 {{
  font-family: var(--display);
  font-weight: 700;
  font-style: normal;
  font-size: 28px;
  letter-spacing: -0.01em;
  margin: 0 0 8px;
}}
h2 .dot {{ color: var(--accent); font-style: normal; font-weight: 700; }}
.section-sub {{
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.22em;
  color: var(--ink-dim);
  margin-bottom: 28px;
  border-bottom: 1px solid var(--line);
  padding-bottom: 12px;
}}
.bars {{ display: grid; gap: 14px; }}
.bar-row {{
  display: grid;
  grid-template-columns: 110px 1fr 60px;
  align-items: center;
  gap: 16px;
  font-family: var(--mono);
}}
.bar-row .name {{ font-size: 13px; }}
.bar-row .name.own {{ color: var(--accent); font-weight: 500; }}
.bar-track {{ height: 22px; background: var(--bg-2); border: 1px solid var(--line); position: relative; }}
.bar-fill {{ height: 100%; background: var(--ink-dim); }}
.bar-fill.own {{ background: linear-gradient(90deg, var(--accent), var(--accent-2)); }}
.bar-row .val {{ text-align: right; font-size: 12px; color: var(--ink-dim); }}
.clusters {{ display: grid; gap: 0; border-top: 1px solid var(--line); }}
.cluster {{
  border-bottom: 1px solid var(--line);
  padding: 24px 0;
  display: grid;
  grid-template-columns: 80px 1fr 220px;
  gap: 32px;
  align-items: start;
}}
.cluster .rank {{
  font-family: var(--display);
  font-weight: 700;
  font-size: 40px;
  line-height: 0.9;
  color: var(--accent);
}}
.cluster .rank-sub {{
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--ink-dim);
  margin-top: 6px;
}}
.cluster .prompt {{
  font-family: var(--display);
  font-size: 22px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 10px;
}}
.cluster .tags {{
  display: flex; gap: 8px; flex-wrap: wrap;
  margin-bottom: 14px;
}}
.tag {{
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  padding: 3px 9px;
  border: 1px solid var(--line);
  color: var(--ink-dim);
  background: var(--bg-2);
}}
.tag.warn {{ color: var(--warn); border-color: rgba(255,78,91,0.3); }}
.tag.acc {{ color: var(--accent); border-color: rgba(0,102,255,0.3); }}
.cluster .urls {{ font-size: 12px; color: var(--ink-dim); }}
.cluster .urls .url {{
  display: block;
  padding: 4px 0;
  border-bottom: 1px dotted var(--line);
  color: var(--ink);
  text-decoration: none;
}}
.cluster .urls .url:hover {{ color: var(--accent); }}
.cluster .urls .meta-line {{ font-size: 10px; color: var(--ink-dim); margin-top: 2px; }}
.impact-card {{
  background: var(--bg-2);
  border: 1px solid var(--line);
  padding: 16px;
}}
.impact-card .big {{
  font-family: var(--display);
  font-weight: 700;
  font-size: 40px;
  line-height: 1;
  margin: 4px 0 10px;
  color: var(--accent-2);
}}
.impact-card .row {{
  display: flex; justify-content: space-between;
  font-size: 11px; color: var(--ink-dim);
  padding: 3px 0;
  border-bottom: 1px dotted var(--line);
}}
.impact-card .row:last-child {{ border: 0; }}
.cta {{
  border-top: 2px solid var(--ink);
  border-bottom: 2px solid var(--ink);
  padding: 36px 0;
  margin-top: 48px;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
  align-items: center;
}}
.cta h3 {{
  font-family: var(--display);
  font-style: normal;
  font-weight: 700;
  font-size: 32px;
  margin: 0 0 6px;
  letter-spacing: -0.01em;
}}
.cta h3 em {{ font-style: normal; color: var(--accent); font-weight: 700; }}
.cta p {{ color: var(--ink-dim); margin: 0; max-width: 60ch; }}
.cmd {{
  font-family: var(--mono);
  background: var(--bg-2);
  border: 1px solid var(--line);
  padding: 16px;
  font-size: 12px;
  color: var(--accent-2);
  overflow-x: auto;
  white-space: pre;
}}
footer {{
  margin-top: 64px;
  padding-top: 24px;
  border-top: 1px solid var(--line);
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--ink-dim);
  text-transform: uppercase;
  letter-spacing: 0.22em;
}}
@media (max-width: 900px) {{
  .hero {{ grid-template-columns: 1fr; gap: 24px; }}
  .numbers {{ grid-template-columns: repeat(2, 1fr); }}
  .cluster {{ grid-template-columns: 1fr; }}
  .cluster .rank {{ font-size: 28px; }}
  .cta {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>
<div class="container">

<header class="masthead">
  <div class="brand">Gap<b>Brief</b></div>
  <div class="kicker">Dashboard · Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
  <div class="meta">Example Data<br/>v1.0</div>
</header>

{self.render_hero_section(totals)}

{self.render_metrics_strip(totals)}

{self.render_competitor_bars(totals)}

{self.render_gap_clusters()}

<section>
  <h2>Nächste Schritte<span class="dot"> · </span><em>GapBrief Workflow</em></h2>
  <div class="section-sub">Ausführung basierend auf Impact-Ranking</div>
  <ol style="padding-left:24px;color:var(--ink-dim);line-height:1.9;">
    <li><strong style="color:var(--ink)">Phase 1:</strong> Für jedes Gap: <code>python generate_gap_brief.py --gap-id X</code> ausführen. Output: Markdown Brief mit H2-Struktur, FAQ, Schema.</li>
    <li><strong style="color:var(--ink)">Phase 2:</strong> Content Writer nimmt Briefs und produziert Artikel basierend auf Struktur & Competitor Analysis.</li>
    <li><strong style="color:var(--ink)">Phase 3:</strong> 7 Tage nach Publish: <code>python validate_lift.py --gap-id X</code> gegen Peec re-Query.</li>
    <li><strong style="color:var(--ink)">Iteration:</strong> Dashboard wird täglich neu generiert mit neuesten Peec Daten.</li>
  </ol>
</section>

<div class="cta">
  <div>
    <h3>Run <em>GapBrief</em> on your project</h3>
    <p>MIT-licensed. Installable as Claude Code skill. Fully automated with Peec MCP.</p>
  </div>
  <div class="cmd">$ python generate_dashboard.py \\
  --input gaps.json \\
  --output dashboard.html</div>
</div>

<footer>
  <div>#BuiltWithPeec · Example Data</div>
  <div>github.com/CletisTout/gapbrief</div>
</footer>

</div>
</body>
</html>"""

        return html


def main():
    """CLI Entry Point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate GapBrief Dashboard from JSON gap data"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input JSON file (gap data from gap_analyzer.py or gaps-example.json)"
    )
    parser.add_argument(
        "--output",
        default="dashboard.html",
        help="Output HTML file (default: dashboard.html)"
    )

    args = parser.parse_args()

    # Load JSON
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            gap_data = json.load(f)
    except Exception as e:
        print(f"ERROR: Could not load {args.input}: {e}")
        sys.exit(1)

    # Generate dashboard
    try:
        generator = DashboardGenerator(gap_data)
        html = generator.generate_html()

        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ Dashboard generated: {args.output}")
        print(f