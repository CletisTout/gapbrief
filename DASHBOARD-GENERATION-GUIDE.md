# Dashboard Generation Guide

## 🎨 DASHBOARD GENERATION RULES

Das Dashboard wird **AUTOMATISCH** aus JSON Gap-Daten generiert und mit dem **Tech Innovation Theme** gestylt.

### Prozess-Ablauf:

```
gap_analyzer.py (Peec API)
    ↓
    [Erzeugt: gaps.json]
    ↓
generate_dashboard.py ← INPUT: gaps.json
    ↓
    [Erzeugt: dashboard.html]
    ↓
generate_gap_brief.py (parallel)
    ↓
    [Erzeugt: brief-*.md + schemas.json]
```

---

## 📋 DASHBOARD DESIGN SPEZIFIKATION

### Hero Section
- **Headline:** Zusammenfassung der Gaps und Top-Status
- **Impact Card:** Total Gap Impact, Gaps, URLs, Estimated Lift
- **Input:** 
  - Total Impact Score (sum of all gaps)
  - Top Gap Topic
  - Own Brand Status (ABSENT/MENTIONED/STRONG)

### Key Metrics Strip (4 Numbers)
| Position | Metrik | Quelle | Berechnung |
|----------|--------|--------|-----------|
| 1 | Top Gap Own Brand Status | `gaps[0].own_brand_visibility` | % oder ABSENT/MENTIONED |
| 2 | Dominant Competitor | Max SoV in `gaps[0].competitors` | Brand Name |
| 3 | Total Gap URLs | Sum of `urls` across all gaps | Count |
| 4 | Avg Estimated Lift | Average of all `estimated_visibility_lift` | Parse "5-8%" → 6.5% |

**Styling Rules:**
- Own Brand Status ABSENT → .warn (red)
- Own Brand Status MENTIONED → .acc (orange)
- Own Brand Status STRONG → .ok (green)

### Competitor Bar Chart
**Input:** Aggregate SoV from all gaps

```python
competitor_sov = {}
for gap in gaps:
    for brand, sov in gap.competitors.items():
        if brand not in competitor_sov:
            competitor_sov[brand] = []
        competitor_sov[brand].append(float(sov))

# Average SoV per competitor
avg_sov = {brand: sum(sov_list) / len(sov_list) for brand, sov_list in competitor_sov.items()}
```

**Sorting:** Descending by SoV  
**Styling:** Own Brand = gradient (accent + accent-2), competitors = dim

### Gap Clusters Section
**Ranking:** By impact_score (descending)

For each Gap:
```
Rank: [01], [02], etc
Topic: gap.topic
Impact Score: gap.impact_score
Tags:
  - gap.own_brand_status + gap.own_brand_visibility
  - "N URLs" (count)
  - Priority (🔴 CRITICAL, 🟡 HIGH, 🟢 MEDIUM)
URLs:
  - For each url in gap.urls:
    - Title + domain
    - Meta: retrievals, citations, top competitors
Impact Card:
  - Lift Potenzial: gap.estimated_visibility_lift
  - Top competitor: max(gap.competitors)
  - Status: gap.own_brand_status
```

### Next Steps Section
- Hardcoded workflow instructions (same for all dashboards)
- Reference to `generate_gap_brief.py` and `validate_lift.py`

### CTA (Call-to-Action)
- Installation command for Claude Code skill
- Link to GitHub repository

---

## 🔧 USAGE

### Basic Usage
```bash
python generate_dashboard.py \
  --input gaps-example.json \
  --output dashboard.html
```

### From Gap Analyzer Output
```bash
# Step 1: Generate gaps.json from Peec API
python gap_analyzer.py --project-id YOUR_PROJECT_ID

# Step 2: Generate dashboard from gaps.json
python generate_dashboard.py \
  --input gaps.json \
  --output dashboard.html
```

### In Pipeline (Automated)
```bash
#!/bin/bash

# 1. Fetch latest gaps from Peec
python gap_analyzer.py --project-id your-project-id --output gaps.json

# 2. Generate dashboard
python generate_dashboard.py --input gaps.json --output dashboard.html

# 3. Generate individual briefs
python generate_gap_brief.py --input gaps.json --auto-generate

# 4. Commit everything
git add gaps.json dashboard.html gap-briefs/
git commit -m "Auto-generate: gaps, dashboard, briefs"
```

---

## 📊 INPUT JSON SCHEMA

```json
{
  "metadata": {
    "created": "2026-04-24T12:34:56.789012",
    "total_gaps": 3,
    "source": "Peec API Gap Analysis"
  },
  "gaps": [
    {
      "gap_id": 1,
      "topic": "Sportfernseher-Kategorie",
      "urls": [
        {
          "url": "https://mediamarkt.de/...",
          "title": "Sportfernseher bei MediaMarkt",
          "retrieved_in": 156,
          "citation_count": 42
        }
      ],
      "search_queries": ["bester Fernseher für Fußball", ...],
      "priority": "🔴 CRITICAL",
      "impact_score": 85.3,
      "estimated_visibility_lift": "8-12%",
      "own_brand_status": "ABSENT",
      "own_brand_visibility": "0%",
      "competitors": {
        "LG": "60%",
        "Sony": "45%"
      }
    }
  ]
}
```

**Erforderliche Felder pro Gap:**
- `gap_id`: Integer
- `topic`: String (Gap-Beschreibung)
- `urls`: Array mit mindestens 1 URL
  - `url`: String (vollständige URL)
  - `title`: String
  - `retrieved_in`: Integer (Anzahl der Abrufe)
  - `citation_count`: Integer
- `impact_score`: Float (z.B. 85.3)
- `own_brand_status`: "ABSENT" | "MENTIONED" | "STRONG"
- `own_brand_visibility`: String mit % (z.B. "0%")
- `competitors`: Object {brand: "percentage"}
- `estimated_visibility_lift`: String (z.B. "8-12%")

**Optional aber empfohlen:**
- `priority`: Priority-Emoji + Text
- `search_queries`: Array von User-Queries
- `estimated_visibility_lift`: Modellierter Lift

---

## 🎯 COLOR & STYLING RULES

### Status Colors
| Status | CSS Class | Color | Hex |
|--------|-----------|-------|-----|
| ABSENT | .warn | Red | #ff4e5b |
| MENTIONED | .acc | Orange | #ff6b35 |
| STRONG | .ok | Green | #6bcf7f |

### Element Styling
- **Headers:** Fraunces font (serif, italic)
- **Body:** JetBrains Mono (monospace)
- **Accent:** Orange (#ff6b35) für Own Brand
- **Highlight:** Yellow (#f7d06b) für wichtige Nummern
- **Background:** Dark (#0c0c0e) mit subtle gradients

---

## ✅ VALIDATION RULES

Dashboard Generator validiert:

```python
# 1. JSON Structure
assert "gaps" in data, "Missing 'gaps' key"
assert isinstance(data["gaps"], list), "gaps must be array"

# 2. Per Gap
for gap in data["gaps"]:
    assert gap.get("gap_id"), "Missing gap_id"
    assert gap.get("topic"), "Missing topic"
    assert gap.get("urls"), "Missing urls"
    assert gap.get("impact_score") is not None, "Missing impact_score"
    
    # Per URL
    for url in gap["urls"]:
        assert url.get("url"), "Missing url"
        assert url.get("title"), "Missing title"

# 3. Data Types
assert isinstance(gap["impact_score"], (int, float)), "impact_score must be number"
assert isinstance(gap["urls"], list), "urls must be array"
```

---

## 📈 REGENERATION CYCLE

**Recommended:** Dashboard wird täglich regeneriert

```bash
# Daily via Cron:
0 8 * * * cd /path/to/gapbrief && python generate_dashboard.py --input gaps.json --output dashboard.html
```

**Trigger Events:**
- Nach `gap_analyzer.py` Ausführung
- Nach `validate_lift.py` (neue Lift-Daten)
- Wöchentlich (via CI/CD)

---

## 🚀 DEPLOYMENT

### Local Testing
```bash
python generate_dashboard.py --input gaps-example.json --output test-dashboard.html
# Öffne test-dashboard.html im Browser
```

### GitHub Pages (Optional)
```bash
# Repo-Root muss dashboard.html enthalten
# GitHub Pages deployed automatisch von main branch
# URL: https://CletisTout.github.io/gapbrief/dashboard.html
```

Oder einfach mit Raw GitHub URL:
```
https://raw.githubusercontent.com/CletisTout/gapbrief/main/dashboard.html
```

### Production (mit Peec Integration)
```bash
# In Peec-Pipeline nach gap_analyzer.py:
python generate_dashboard.py --input gaps.json --output dashboard.html
git add dashboard.html
git commit -m "Update dashboard from latest Peec data"
git push
```

---

## 🔍 TROUBLESHOOTING

### "KeyError: 'gaps'"
**Fehler:** JSON hat keine `gaps`-Key  
**Lösung:** Überprüfe JSON-Struktur, verwende gaps-example.json als Template

### "TypeError: float() argument must be a string or a number"
**Fehler:** `impact_score` ist nicht numerisch  
**Lösung:** Stelle sicher, dass `impact_score` Float/Int ist, nicht String

### Dashboard sieht falsch aus
**Fehler:** URLs oder Metriken fehlerhaft  
**Lösung:** Validiere JSON gegen Schema, prüfe competitor SoV Format (sollte "60%" sein)

---

## 📝 EXAMPLE OUTPUT FILENAMES

```
dashboard.html                    # Main dashboard (regeneriert täglich)
gaps.json                         # Source data (aus gap_analyzer.py)
gap-briefs/
├── gap-brief-001-sportfernseher.md
├── gap-brief-001-sportfernseher.schemas.json
├── gap-brief-002-qled-vs-oled.md
└── gap-brief-002-qled-vs-oled.schemas.json
```
