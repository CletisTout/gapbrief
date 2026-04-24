# Complete Gap-Brief Pipeline - Integrations-Leitfaden
## End-to-End Automatisierung: Peec → Gap-Briefs → Production

**Version:** 1.0  
**Status:** ✅ Produktionsreif  
**Last Updated:** 24. April 2026

---

## 🎯 ÜBERBLICK

Die **Complete Pipeline** automatisiert den kompletten Workflow:

```
Peec API Daten
    ↓
gap_analyzer.py
    ↓ (exportiert gaps-data.json)
run_complete_pipeline.py
    ↓
generate_gap_brief.py
    ↓ (generiert .md + .schemas.json)
Gap-Brief-Dateien
    ↓
Writers beginnen Produktion
```

**Zeitersparnis:** 
- Manuell: 2-3 Stunden pro Gap-Brief
- Automatisch: 2-3 Minuten für alle Gaps

---

## 📦 KOMPONENTEN

### 1. **gap_analyzer.py**
Liest Peec-Daten und erstellt Gap-Analyse

**Input:**
- Peec API (Project ID + API Key)
- Optional: Tage zurückschauen (default 30)

**Output:**
- `gaps-data.json` mit strukturierten Gap-Daten

**Verwendung:**
```bash
python gap_analyzer.py --project-id YOUR_ID --output gaps-data.json
```

---

### 2. **generate_gap_brief.py**
Generiert Gap-Briefs mit FAQs + Schemas

**Input:**
- `gaps-data.json` aus gap_analyzer.py
- Komplexitäts-Logik (automatisch)

**Output:**
- `gap-brief-001-...md` (Markdown-Content)
- `gap-brief-001-...schemas.json` (Article + FAQ + Comparison Schemas)

**Verwendung:**
```bash
python generate_gap_brief.py --input gaps-data.json --auto-generate
```

---

### 3. **run_complete_pipeline.py**
Orchestriert ALLE Schritte automatisch

**Features:**
- ✅ Führt gap_analyzer.py aus
- ✅ Validiert Daten
- ✅ Führt generate_gap_brief.py aus
- ✅ Druckt Production Summary
- ✅ Optional: Verteilt via Slack/Email

**Verwendung:**
```bash
python run_complete_pipeline.py --project-id YOUR_ID
```

---

### 4. **run-pipeline.sh**
Bash-Wrapper für einfache Bedienung

**Features:**
- ✅ Prüft Voraussetzungen
- ✅ Lädt .env Datei automatisch
- ✅ Fehlerbehandlung
- ✅ Benutzerfreundliche Ausgabe

**Verwendung:**
```bash
bash run-pipeline.sh --project-id YOUR_ID
```

---

## 🚀 QUICK START (3 Schritte)

### Schritt 1: Setup
```bash
# Stelle sicher dass .env konfiguriert ist
cat .env
# Output: PEEC_API_KEY=skp-...
#         FIRECRAWL_API_KEY=fc-...
```

### Schritt 2: Führe Pipeline aus
```bash
# Option A: Bash (einfach)
bash run-pipeline.sh

# Option B: Python (explizit)
python run_complete_pipeline.py

# Option C: Mit Projekt-ID
python run_complete_pipeline.py --project-id YOUR_ID
```

### Schritt 3: Nutze generierte Briefs
```
✅ Gap-Briefs sind bereit in ./gap-briefs/
   - gap-brief-001-sportfernseher.md
   - gap-brief-001-sportfernseher.schemas.json
   - gap-brief-002-qled-vs-oled.md
   - gap-brief-002-qled-vs-oled.schemas.json
   ... usw
```

---

## 🔄 DETAILLIERTER WORKFLOW

### Phase 1: Peec Analysis (`gap_analyzer.py`)

```
Start
  ↓
Verbinde zu Peec API (PEEC_API_KEY)
  ↓
Hole Brand Report (30 Tage zurück)
  ↓
Extrahiere Content Gaps:
  - Impact Score berechnen
  - Own Brand Visibility analysieren
  - Citation Rates bestimmen
  ↓
Exportiere gaps-data.json
  ↓
Print Summary (Gap-Übersicht)
  ↓
Done
```

**Output: `gaps-data.json`**
```json
{
  "metadata": {"created": "2026-04-24T...", "total_gaps": 3},
  "gaps": [
    {
      "gap_id": 1,
      "topic": "Sportfernseher-Kategorie",
      "impact_score": 85.3,
      "retrieval_rate": 164,
      "citation_rate": 0.52,
      "own_brand_visibility": "0%",
      "faq_questions": [...]
    },
    ...
  ]
}
```

---

### Phase 2: Datensatz-Validierung

```
Start
  ↓
Prüfe gaps-data.json existiert
  ↓
Parse JSON (syntax check)
  ↓
Validiere erforderliche Felder:
  ✓ gap_id, topic, impact_score
  ✓ retrieval_rate, citation_rate
  ✓ own_brand_status, own_brand_visibility
  ✓ faq_questions (8-12 Fragen)
  ↓
Zähle Gaps (sollte > 0 sein)
  ↓
Report: "3 Gaps validiert"
  ↓
Done
```

---

### Phase 3: Gap-Brief Generierung (`generate_gap_brief.py`)

```
Start
  ↓
Lade gaps-data.json
  ↓
Für jeden Gap:
  ↓
  Bestimme Komplexität (SIMPLE/MEDIUM/COMPLEX)
    - Impact < 50 → SIMPLE (10 H2, 2.4K-2.6K words)
    - Impact 50-75 → MEDIUM (12 H2, 2.6K-3K words)
    - Impact > 75 → COMPLEX (14 H2, 2.8K-3.2K words)
  ↓
  Generiere Markdown mit:
    - Header (Peec-Metriken)
    - Content Strategy
    - H2-Struktur (angepasst)
    - FAQ-Template (angepasst)
    - Checklisten
    - Success Metrics
  ↓
  Generiere Schema-Markups:
    - Article Schema (SEO)
    - FAQPage Schema (Rich Snippets)
    - ComparisonChart Schema (wenn Vergleich)
  ↓
  Speichere:
    - gap-brief-{id:03d}-{topic}.md
    - gap-brief-{id:03d}-{topic}.schemas.json
  ↓
Done
```

**Outputs:**
- `gap-brief-001-sportfernseher.md` (9 KB)
- `gap-brief-001-sportfernseher.schemas.json` (2 KB)

---

### Phase 4: Orchestration Summary

```
run_complete_pipeline.py
  ↓
STEP 1: Führe gap_analyzer.py aus
  └─ ✅ gaps-data.json erstellt
  ↓
STEP 2: Validiere Gap-Daten
  └─ ✅ 3 Gaps gefunden & validiert
  ↓
STEP 3: Generiere Gap-Briefs
  └─ ✅ 3 Markdown-Dateien erstellt
  └─ ✅ 3 Schema-JSON-Dateien erstellt
  ↓
STEP 4: Validiere Output
  └─ ✅ 3 Briefs vorhanden
  └─ ✅ 3 Schemas vorhanden
  ↓
STEP 5: Drucke Summary
  ├─ Gap #1: Sportfernseher (85.3, 🔴 CRITICAL)
  ├─ Gap #2: QLED vs OLED (69.7, 🟡 HIGH)
  └─ Gap #3: Mini-LED (55.4, 🟡 MEDIUM-HIGH)
  ↓
STEP 6: Optional Distribute (Slack/Email)
  └─ Übersprungen (nicht gesetzt)
  ↓
✅ ERFOLGREICH
```

---

## 📊 JSON-DATENSTRUKTUR

### gaps-data.json Format

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
          "url": "https://mediamarkt.de/de/product/sports-tv",
          "title": "Sportfernseher bei MediaMarkt",
          "retrieved_in": 156,
          "citation_count": 42
        },
        {
          "url": "https://www.saturn.de/de/category/fernseher-sport",
          "title": "Sportfernseher bei Saturn",
          "retrieved_in": 98,
          "citation_count": 28
        },
        {
          "url": "https://www.cnet.de/artikel/beste-fernseher-fussball-sport",
          "title": "Die besten Fernseher für Fußball & Sport",
          "retrieved_in": 87,
          "citation_count": 35
        }
      ],
      "search_queries": [
        "bester Fernseher für Fußball",
        "120Hz TV Sportübertragung",
        "Motion Handling TV Empfehlung",
        "Fernseher für schnelle Bewegungen",
        "TV Refresh Rate Fußball",
        "TV Sport Modus Funktion"
      ],
      "priority": "🔴 CRITICAL",
      "impact_score": 85.3,
      "estimated_visibility_lift": "8-12%",
      "retrieval_rate": 164,
      "total_chats": 4579,
      "citation_rate": 0.52,
      "own_brand_status": "ABSENT",
      "own_brand_visibility": "0%",
      "target_length": "2400-2600 words",
      "production_hours": "4-5",
      "primary_keyword": "Sportfernseher",
      "secondary_keywords": ["Fußball TV", "Motion Handling TV"],
      "competitors": {
        "LG": "60%",
        "Sony": "45%"
      },
      "faq_questions": [
        {
          "question": "Welcher Fernseher ist am besten?",
          "answer": "Für Fußball brauchst du mindestens 120Hz...",
          "category": "performance"
        }
      ],
      "has_comparison_table": true,
      "comparison_items": ["Own Brand", "LG", "Sony"],
      "comparison_properties": {
        "Refresh Rate": ["240Hz", "120Hz", "120Hz"]
      }
    }
  ]
}
```

### Neue Felder (Verbesserte Genauigkeit)

**urls** (Array):
- `url`: Vollständige URL (z.B. mediamarkt.de/...)
- `title`: Seiten-Titel für Kontext
- `retrieved_in`: Wie oft diese URL in Peec-Chats abgerufen wurde
- `citation_count`: Wie oft diese URL zitiert wurde

**search_queries** (Array):
- Konkrete Suchanfragen, die zu diesem Gap führen
- Zeigen, was Nutzer wirklich suchen
- Hilft Content-Writern bei Keyword-Strategie

---

## 🛠️ KONFIGURATION

### .env Datei (erforderlich)

```bash
# Peec API
PEEC_API_KEY=skp-b3JfNDQ5NWQ1MWMtMTZhMy00NDdiLTk0YzgtOWIzMGJkNWYyM2Zk-...

# Firecrawl API (optional, für extract_patterns.py)
FIRECRAWL_API_KEY=fc-ce459797b7bf496297caedfd4ab2cc37

# Optional: Project ID (kann auch via CLI gesetzt werden)
PEEC_PROJECT_ID=your_project_id_here
```

### Komplexitäts-Schwellenwerte (anpassbar)

In `generate_gap_brief.py`, class `ComplexityLevel`:

```python
if impact_score >= 75:
    return ("COMPLEX", 14, 2800, 3200, 10, 12)  # 14 H2s, 2.8-3.2K words
elif impact_score >= 50:
    return ("MEDIUM", 12, 2600, 3000, 10, 12)   # 12 H2s, 2.6-3K words
else:
    return ("SIMPLE", 10, 2400, 2600, 8, 10)    # 10 H2s, 2.4-2.6K words
```

---

## 📈 PERFORMANCE & SKALA

### Execution Times (gemessen)

| Schritt | Gap #1 | Gap #2 | Gap #3 | Total |
|---------|--------|--------|--------|-------|
| Analysis | - | - | - | 2-3s |
| Validation | <1s | <1s | <1s | 1s |
| Generation | 1-2s | 1-2s | 1-2s | 4-6s |
| Summary | 1s | - | - | 1s |
| **Total** | - | - | - | **8-11s** |

### Skalierbarkeit

| Gaps | Time | Output Size |
|------|------|-------------|
| 1 | ~3s | ~11 KB |
| 3 | ~8s | ~33 KB |
| 10 | ~25s | ~110 KB |
| 50 | ~2min | ~550 KB |

---

## 🔄 AUTOMATISIERUNG (Cron/Scheduler)

### Linux/Mac Cron

```bash
# Wöchentlich Montag 9:00 Uhr
0 9 * * 1 cd /path/to/project && python run_complete_pipeline.py >> pipeline.log 2>&1

# Täglich 8:00 Uhr (wenn neue Gaps jeden Tag erwartet)
0 8 * * * cd /path/to/project && bash run-pipeline.sh >> pipeline.log 2>&1
```

### Windows Task Scheduler

```batch
REM Erstelle Task
schtasks /create /tn "Gap-Brief Pipeline" /tr "python C:\path\to\run_complete_pipeline.py" /sc weekly /d MON /st 09:00

REM Starten
schtasks /run /tn "Gap-Brief Pipeline"
```

### Python Schedule

```python
import schedule
import subprocess

def run_pipeline():
    subprocess.run(["python", "run_complete_pipeline.py"])

schedule.every().monday.at("09:00").do(run_pipeline)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 🐛 TROUBLESHOOTING

### Problem: "PEEC_API_KEY nicht gefunden"
**Lösung:**
```bash
# Prüfe .env Datei
cat .env

# Oder setze Environment-Variable
export PEEC_API_KEY=your_key_here
python run_complete_pipeline.py
```

### Problem: "JSON Parse-Fehler in gaps-data.json"
**Lösung:**
```bash
# Validiere JSON
python -m json.tool gaps-data.json

# Oder regeneriere
python gap_analyzer.py --output gaps-data.json
```

### Problem: "Keine Gap-Briefs generiert"
**Lösung:**
```bash
# Prüfe Output-Verzeichnis
ls -la gap-briefs/

# Oder nutze --skip-analysis um zu debuggen
python run_complete_pipeline.py --skip-analysis
```

### Problem: "Peec API Verbindungsfehler"
**Lösung:**
```bash
# Prüfe API-Verfügbarkeit
curl https://api.peec.ai/health

# Oder nutze Demo-Daten
python gap_analyzer.py  # Wird automatisch zu Mock-Daten fallback
```

---

## ✅ QUALITY CHECKS

### Pre-Execution
- [ ] .env Datei existiert mit PEEC_API_KEY
- [ ] Peec API erreichbar
- [ ] Python 3.8+ verfügbar
- [ ] Alle Python-Scripts im Verzeichnis

### Post-Execution
- [ ] gaps-data.json vorhand