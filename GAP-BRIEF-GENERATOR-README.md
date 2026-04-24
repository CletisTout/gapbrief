# Gap-Brief Generator - Automatisiertes System
## Automatische Erstellung von Content-Gap-Dokumenten mit FAQs & Schema-Daten

**Version:** 1.0  
**Created:** 24. April 2026  
**Status:** ✅ Produktionsreif

---

## 📋 ÜBERBLICK

Das **Gap-Brief Generator System** automatisiert die Erstellung von strukturierten Content-Gap-Dokumenten. Für jeden neu entdeckten Content Gap wird automatisch generiert:

✅ **Markdown-Datei** mit vollständiger Content-Strategie  
✅ **FAQ-Sektion** mit 8-12 Fragen (je nach Komplexität)  
✅ **Schema-Markups** (JSON-LD) für:
- Article Schema (SEO)
- FAQPage Schema (Rich Snippets)
- ComparisonChart Schema (wenn Vergleiche vorhanden)

---

## 🛠️ KOMPONENTEN

### 1. **generate_gap_brief.py**
Python-Script das automatisch Gap-Briefs generiert

**Features:**
- ✅ Komplexitäts-Level Bestimmung (SIMPLE/MEDIUM/COMPLEX)
- ✅ Adaptive H2-Strukturen (10, 12, oder 14 Sections)
- ✅ FAQ-Template Generation (Consumer vs. Technical)
- ✅ Schema-Markup Generierung (Article + FAQ + Comparison)
- ✅ Batch-Verarbeitung (JSON Input)
- ✅ Mehrere URLs pro Gap (bis zu 3 für bessere Kontext)
- ✅ Search Queries/Prompts Display (zeigt, was Nutzer suchen)
- ✨ **NEW: Firecrawl Content Analysis** - Scraped URLs und analysiert Competitor-Content!

### 2. **gaps-example.json**
Example-Datei mit 3 vorgefüllten Gaps

**Enthält:**
- Gap #1: Kategorie mit hohem Suchvolumen
- Gap #2: Vergleichsabfragen und Feature-Focus
- Gap #3: Innovation und Zukunfts-Themen

Jeder Gap mit:
- **Vollständigen Peec-Metriken** (Impact Score, Citation Rate, etc.)
- **3 URLs pro Gap** mit Retrieval & Citation Counts
- **6 Search Queries** die zu diesem Gap führen (zeigt Nutzer-Intent)
- **FAQ-Fragen mit Antworten** (8-12 je nach Komplexität)
- **Vergleichstabellen-Daten** (für Product-Comparisons)
- **Entity-Strategien** (Konkurrenz-Analyse)

---

## 🚀 VERWENDUNG

### Szenario A: Batch-Generierung aller Gaps aus JSON

```bash
cd /sessions/affectionate-dazzling-pasteur/mnt/Peec\ AI\ MCP\ Projekt/

python generate_gap_brief.py \
  --input gaps-example.json \
  --auto-generate \
  --output-dir ./generated-gap-briefs
```

**Output:**
```
✅ Gap-Brief erstellt: ./generated-gap-briefs/gap-brief-001-kategorie-suchvolumen.md
✅ Schema-Markups erstellt: ./generated-gap-briefs/gap-brief-001-kategorie-suchvolumen.schemas.json
✅ Gap-Brief erstellt: ./generated-gap-briefs/gap-brief-002-vergleichsabfragen.md
✅ Schema-Markups erstellt: ./generated-gap-briefs/gap-brief-002-vergleichsabfragen.schemas.json
✅ Gap-Brief erstellt: ./generated-gap-briefs/gap-brief-003-innovation-zukunft.md
✅ Schema-Markups erstellt: ./generated-gap-briefs/gap-brief-003-innovation-zukunft.schemas.json
✅ 3 Gap-Briefe generiert!
```

### Szenario B: Einzelne Gap generieren

```bash
python generate_gap_brief.py \
  --gap-id 4 \
  --topic "Gaming TV Kaufleitfaden" \
  --impact 62.5 \
  --url "example.com/gaming-tv" \
  --output-dir .
```

### Szenario C: Mit Firecrawl Content-Analyse (NEU!)

Scraped automatisch die Competitor-URLs und analysiert ihren Content:

```bash
python generate_gap_brief.py \
  --input gaps-example.json \
  --output-dir ./gap-briefs \
  --with-firecrawl
```

**Was Firecrawl macht:**
- 📄 Scraped jede URL (bis zu 3 pro Gap)
- 📊 Analysiert Content-Struktur (H2-Zahl, Word Count)
- ✅ Erkennt Best Practices (FAQ, Vergleichstabellen, CTAs)
- 🎯 Generiert Recommendations für deine Content
- 📋 Erstellt "Competitor Content Analyse" Section im Gap-Brief

**Voraussetzung:**
```bash
# In .env:
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
```

Ohne API Key: Skript läuft ohne Content-Analyse (graceful fallback)

---

## 📄 JSON Input Format

```json
{
  "gaps": [
    {
      "gap_id": 1,
      "topic": "Kategorie mit hohem Suchvolumen",
      "url": "example.com/category-page",
      "priority": "🔴 CRITICAL",
      "impact_score": 85.3,
      "estimated_visibility_lift": "8-12%",
      "retrieval_rate": 164,
      "total_chats": 4579,
      "citation_rate": 0.52,
      "own_brand_status": "ABSENT",
      "own_brand_visibility": "0%",
      "primary_keyword": "Kategorie Keyword",
      "secondary_keywords": ["Feature 1", "Feature 2"],
      "competitors": {
        "Competitor A": "Strong Position",
        "Competitor B": "Moderate Position"
      },
      "faq_questions": [
        {
          "question": "What's the best option?",
          "answer": "Top brands in this category...",
          "category": "performance"
        }
      ],
      "has_comparison_table": true,
      "comparison_items": ["Own Brand", "Competitor A", "Competitor B"],
      "comparison_properties": {
        "Key Feature": ["Strong", "Good", "Good"]
      }
    }
  ]
}
```

### Erforderliche Felder

| Feld | Typ | Beispiel | Beschreibung |
|------|-----|---------|-------------|
| `gap_id` | int | 1 | Eindeutige Gap-ID |
| `topic` | string | "Category Topic" | Gap Topic/Titel |
| `url` | string | "example.com/..." | Ziel-URL |
| `impact_score` | float | 85.3 | Peec Impact Score |
| `retrieval_rate` | int | 164 | Chats pro Monat |
| `citation_rate` | float | 0.52 | Zitationen pro Abruf |
| `own_brand_status` | string | "ABSENT" | ABSENT/UNDERREPRESENTED |
| `own_brand_visibility` | string | "0%" | Own Brand Visibilität |
| `primary_keyword` | string | "Main Keyword" | Haupt-Keyword |
| `faq_questions` | array | [...] | FAQ-Fragen & -Antworten |

---

## 📊 Output Format

### Markdown-Datei (`gap-brief-001-...md`)

```markdown
# GapBrief #1: Category Topic
## Content Gap Analyse & Strategie

**Gap ID:** #1
**Priority:** 🔴 CRITICAL
**Impact Score:** 85.3
**Geschätzte Visibility Steigerung:** 8-12%

---

## 📊 GAP OVERVIEW
[Peec-Metriken, Why This Gap Matters]

## 🎯 CONTENT STRATEGY
[Article Goal, Target Audience]

## 📐 CONTENT STRUCTURE
[H2-Structure, FAQ-Template, Entity Strategy]

## 💬 FAQ SECTION
[Alle FAQ-Fragen & Antworten integriert]

## 📋 PRE-PUBLICATION CHECKLIST
[Vollständige Validierungs-Checkliste]

## 🚀 PRODUCTION TIMELINE
[Timeline mit Owner Assignments]

## 📈 SUCCESS METRICS
[30-Day & 90-Day Goals]
```

### Schema-Datei (`gap-brief-001-...schemas.json`)

```json
{
  "article_schema": {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "GapBrief #1: Category Topic Gap Analysis",
    "datePublished": "2026-04-24T...",
    "wordCount": 2500
  },
  "faq_schema": {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "What's the best option in this category?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Top brands include..."
        }
      }
    ]
  },
  "comparison_schema": {
    "@type": "ComparisonChart",
    "compareItem": [
      {"@type": "Thing", "name": "Own Brand"},
      {"@type": "Thing", "name": "Competitor A"}
    ]
  }
}
```

---

## 🎯 KOMPLEXITÄTS-LEVEL

Das System bestimmt automatisch die Komplexität basierend auf Impact Score:

### SIMPLE (Impact < 50)
- **H2 Sections:** 10
- **Word Count:** 2.400-2.600
- **FAQ:** 8-10 Fragen
- **Audience:** Casual Consumer
- **Beispiel:** Nischentopic mit niedrigem Impact

### MEDIUM (Impact 50-75)
- **H2 Sections:** 12
- **Word Count:** 2.600-3.000
- **FAQ:** 10-12 Fragen
- **Audience:** Tech-Enthusiasts
- **Beispiel:** QLED vs OLED (69.7)

### COMPLEX (Impact > 75)
- **H2 Sections:** 14
- **Word Count:** 2.800-3.200
- **FAQ:** 10-12 Fragen (technisch)
- **Audience:** Engineers & Experts
- **Beispiel:** Sports TV (85.3), Mini-LED (55.4)

---

## 💡 WORKFLOW INTEGRATION

### Schritt 1: Peec-Daten sammeln
```bash
# Aus Peec API, gap_analyzer.py oder manuelle Research
# → Exportiere als JSON nach gaps-data.json
```

### Schritt 2: Gap-Briefs generieren
```bash
python generate_gap_brief.py \
  --input gaps-data.json \
  --auto-generate \
  --output-dir ./gap-briefs
```

### Schritt 3: Briefs an Team verteilen
```
📁 gap-briefs/
├── gap-brief-001-category-topic.md
├── gap-brief-001-category-topic.schemas.json
├── gap-brief-002-comparison-focus.md
├── gap-brief-002-comparison-focus.schemas.json
└── ...
```

### Schritt 4: Writers produzieren Content
- Öffnen assigned Gap-Brief
- Folgen H2-Struktur & FAQ-Template
- Liefern finalen Content (29. April)

### Schritt 5: SEO/Dev integrieren Schemas
- JSON-LD Schemas in `<head>` tag einbinden
- Article + FAQ + Comparison Schemas aktivieren
- PageSpeed & Mobile Responsiveness testen

---

## 📋 FAQ - HÄUFIGE FRAGEN

**F: Wie viele FAQs werden generiert?**  
A: Der Markdown hat FAQ-Template mit Platzhaltern. Script speichert echte FAQ-Daten in JSON. Dein Team füllt die FAQ-Antworten basierend auf Template.

**F: Kann ich die H2-Struktur anpassen?**  
A: Ja - im Script `get_h2_structure()` die Templates anpassen. Oder JSON mit custom `h2_structure` Feld erweitern.

**F: Werden die Schemas automatisch in die HTML eingebunden?**  
A: Nein - JSON wird generiert. Dein Team bindet JSON-LD in `<head>` tag manuell oder via CMS ein.

**F: Kann ich die Sprache wechseln?**  
A: Ja - alle String-Templates sind parametrisch. German Deutsch-Variablen verwenden.

**F: Was ist mit Vergleichstabellen?**  
A: JSON speichert `comparison_items` und `comparison_properties`. Script generiert Markdown-Struktur, Team füllt finale Tabelle.

**F: Wie oft sollte ich den Generator laufen?**  
A: Wann immer neue Gaps entdeckt werden. Produktionsreif für automatisierte Ausführung (z.B. weekly via Cron).

---

## 🔧 ANPASSUNGEN & ERWEITERUNGEN

### Custom H2-Struktur hinzufügen
```python
# In generate_gap_brief.py, class GapBriefTemplate
structures = {
    "MY_CUSTOM": """1. Intro
    2. Custom Section 1
    3. Custom Section 2
    ..."""
}
```

### Neue Schema-Typen hinzufügen
```python
# In generate_gap_brief.py, class SchemaGenerator
@staticmethod
def generate_product_schema(products):
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        ...
    }
```

### FAQ-Kategorien erweitern
```json
{
  "question": "...",
  "answer": "...",
  "category": "custom_category",
  "schema_importance": "high"
}
```

---

## ✅ QUALITY ASSURANCE

### Pre-Generation Checks
- [ ] JSON valid (use JSONValidator)
- [ ] Impact Scores korrekt
- [ ] Peec URLs erreichbar
- [ ] FAQ-Anzahl korrekt (8-12)

### Post-Generation Checks
- [ ] Markdown valid (kein broken formatting)
- [ ] H2-Anzahl korrekt (10, 12, oder 14)
- [ ] FAQ-Schema valid JSON
- [ ] Keine fehlenden Felder

### Content Checks
- [ ] Own brand positiv positioniert
- [ ] Competitors fair erwähnt
- [ ] Keinen Spam-Content
- [ ] Readability score simulierbar

---

## 🚀 DEPLOYMENT

### Local Testing
```bash
python generate_gap_brief.py \
  --input gaps-example.json \
  --auto-generate \
  --output-dir ./test-output
```

### Production Execution
```bash
# Via Cron (weekly bei neuen Gaps):
0 9 * * 1 cd /path/to/project && python generate_gap_brief.py --input latest-gaps.json --auto-generate --output-dir ./gap-briefs

# Oder manuell via Script:
./generate-gaps.sh
```

### CI/CD Integration
```yaml
# .github/workflows/generate-gaps.yml
name: Auto-Generate Gap Briefs
on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly Monday 9am
jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate Gap Briefs
        run: python generate_gap_brief.py --input 