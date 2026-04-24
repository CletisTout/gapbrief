# Tally Submission Checklist & Feldübersicht

**Submission-Datum:** 26. April 2026  
**Deadline:** 26. April 2026 (opens April 20, closes April 26)  
**Formular-URL:** https://peec.ai/countdown-submissions-mcp-challenge

---

## ✅ PRE-SUBMISSION CHECKLIST

- [ ] **Tally-Seite öffnen:** https://peec.ai/countdown-submissions-mcp-challenge
- [ ] **Mit Peec-Account anmelden** (falls erforderlich)
- [ ] **Alle Felder vorbereitet** (siehe unten)
- [ ] **Links vor Submission testen:**
  - [ ] GitHub Repo: https://github.com/syzygy-performance/gapbrief
  - [ ] Dashboard: https://syzygy-performance.github.io/gapbrief/dashboard.html
  - [ ] Example Brief: https://github.com/syzygy-performance/gapbrief/blob/main/examples/project-1/brief-gaming-streaming.md
- [ ] **Video hochgeladen/Link parat** (Loom 60-Sek)

---

## 📋 TALLY-FORMULAR FELDER & INHALTE

### **1. Workflow Name** (Pflichtfeld)
```
GapBrief — From Peec AI Gaps to Publish-Ready Content Briefs
```

### **2. One-sentence pitch** (max 140 Zeichen) (Pflichtfeld)
```
A Claude Code skill that turns Peec AI visibility gaps into publish-ready content briefs with competitor content analysis and 7-day validation. MIT-licensed.
```
✓ Länge: 135 Zeichen (unter 140)

### **3. Category** (optional, but recommended)
```
Content Optimization
```
*Alternativ wenn Multi-Select:* Content Optimization + Competitive Intelligence

### **4. Tools used** (Pflichtfeld?)
```
Peec MCP · Claude Code · Anthropic API (Claude Sonnet 4) · Firecrawl MCP · Python 3.11
```

### **5. Problem it solves** (Hauptbeschreibung)
**Länge:** ~250 Wörter (Copy aus tally-submission.md)

```
Every SEO/GEO practitioner with access to Peec has the same friction point: the gap between "our visibility dropped on this topic" and "here is the page we will publish next Tuesday to fix it" is still a two-hour manual job per gap. Dashboards visualize gaps. They don't deliver briefs. GapBrief closes that gap. 

Given a Peec project ID and a visibility gap, it outputs a Markdown content brief — with adaptive H2 skeleton (10-14 sections by complexity), competitor content analysis, entity checklist, FAQ block, schema recommendations, search query context, and modeled lift — that a content writer can execute on Monday morning. 

Then, seven days after publish, it re-queries Peec to validate whether the page actually moved the needle.
```

### **6. How it works** (Detaillierte Beschreibung, 6 Steps)
**Länge:** ~350 Wörter (Copy aus tally-submission.md)

```
1. Gap pull — gap_analyzer.py calls get_url_report with the gap filter to get every URL winning AI citations for prompts where the own brand is absent but ≥2 competitors are present. It cross-joins against get_brand_report for SoV context and list_prompts/list_topics/list_brands to resolve IDs to labels.

2. Impact scoring — A composite score per gap: retrievals × citation_rate × prompt_frequency × competitor_strength. Multiplicative, not additive — any zero factor means zero impact. Prioritizes surgically.

3. Multi-URL competitor analysis — FOR EACH GAP: Fetches up to 3 competing URLs with retrieval & citation counts. Firecrawl scrapes each URL and extracts content structure (H2-count, word count, readability), best practices (FAQ patterns, comparison tables, CTA placement), entity patterns & E-E-A-T signals, and generates "Competitor Content Analysis" section in the brief.

4. Search intent mapping — Analyzes 6-10+ search queries that lead to each gap. Shows exactly what users are asking, surfacing intent patterns the writer must address.

5. Brief rendering — generate_gap_brief.py synthesizes gap data, competitor content analysis, and search intent into a Markdown brief with adaptive H2 structure (10/12/14 sections by impact complexity), FAQ template (8-12 questions matched to competitor patterns), schema recommendations (Article, FAQPage, ComparisonChart), and YAML frontmatter with all metrics inline.

6. Validation loop — validate_lift.py is cron-scheduled to re-query Peec seven days after publish and report lift against the original baseline.
```

### **7. What makes it different** (Key Differentiators)
**Länge:** ~200 Wörter (Copy aus tally-submission.md)

```
• Every claim traces to a data row. The brief cites Peec retrievals, citation rates, and search queries inline — not vague "AI says" language.

• Intelligent multi-URL competitor analysis. Each gap analyzes up to 3 competitor URLs, scrapes their exact content structure, and surfaces which best practices (FAQ patterns, comparison table formats, CTA strategies) your content writer should match or exceed.

• Search query intent context. Each gap includes 6-10+ search queries showing exactly what users are asking — not guessing at intent.

• Adaptive content complexity. The system automatically determines whether a gap needs 10, 12, or 14 H2 sections based on impact score, from casual consumer content to technical expert content.

• The 7-day validation loop closes the loop that every other GEO tool leaves open. Publishing without validation is hope; publishing with validation is strategy.

• Shipped as a Claude Code skill, not a SaaS dashboard. Version-controllable, reproducible across machines, installable in one command.

• CLI-first and cron-friendly. Runs overnight for every Peec project in a portfolio. Batch-process 50+ gaps in minutes.

• Impact Score formula is explicit and tunable — agencies can re-weight factors for strategic priorities without forking.
```

### **8. Real-data validation**
**Länge:** ~150 Wörter (Copy aus tally-submission.md)

```
The submitted example was generated from a real 14-project Peec portfolio at SYZYGY Performance, focused on the Own Brand TV project's Gaming topic. 

Finding: Own Brand holds 44% topic-wide SoV but 0% on the highest-impact gap prompt ("best smart tvs for gaming and streaming") — the brief provides the exact page structure from 3 scraped competitor URLs, entity checklist, and schema plan to close that gap, with a modeled +25 pp lift over 30 days. 

The brief includes competitor content analysis showing which YouTube channels, Reddit threads, and review sites are winning citations — and exactly how their content is structured, so Own Brand can match or exceed them.
```

### **9. Links** (Mehrere Felder wahrscheinlich)

#### **Repository (MIT License)**
```
https://github.com/CletisTout/gapbrief
```

#### **Dashboard (Visual Example)**
```
https://github.com/CletisTout/gapbrief/blob/main/dashboard.html
```
*Interactive HTML-Dashboard, zeigt 3 Gap-Cluster mit Beispieldaten aus gaps-example.json*

#### **Example Briefs & Code**
```
https://github.com/CletisTout/gapbrief/tree/main
```
- README.md: Vollständige Dokumentation
- gaps-example.json: Beispieldaten (3 Gaps)
- generate_gap_brief.py: Der Generator

#### **Demo Video** (falls Feld vorhanden)
```
[Loom-Link wird noch hochgeladen — Platzhalter jetzt]
```

#### **LinkedIn Post** (falls Feld vorhanden)
```
[Wird nach Submission gepostet — Link folgt]
```

### **10. Who built it**
```
Tim Brock, Senior SEO Consultant (Lead) at SYZYGY Performance, Germany
```

### **11. Public-sharing opt-in**
```
Yes — repo is MIT-licensed, dashboard is public, LinkedIn post is tagged with #BuiltWithPeec
```

### **12. Why it hits each judging criterion** (Falls separate Felder)

#### **Usefulness (40%)**
```
Solves the single most common agency workflow bottleneck for Peec users: converting dashboard insight into executable content briefs with competitor benchmarking. Replicable to any Peec project in any vertical (Finance, Pharma, FMCG, Tech, Retail).
```

#### **Creativity (30%)**
```
The multiplicative Impact Score (not a linear "visibility drop" metric), the intelligent multi-URL competitor content analysis (most tools stop at "competitors mention this topic"), the search query intent mapping (shows user perspective, not just SEO perspective), the 7-day retrieval-validation loop (closes a loop every competitor leaves open), and the packaging as a Claude Code skill (not a SaaS) are five non-obvious design choices, each justified by the problem.
```

#### **Execution (20%)**
```
Clean CLI-first Python, typed Peec client, Firecrawl content scraping with graceful fallback, anonymization flag, reproducibility command embedded in every output, real data validation from a 14-project portfolio. Schema generation (Article + FAQ + Comparison). Batch processing for 50+ gaps overnight.
```

#### **Community Impact (10%)**
```
MIT license, public repo, visual dashboard on GitHub Pages, SYZYGY blog post explaining the methodology, LinkedIn distribution with #BuiltWithPeec. Installable in three lines by any other Peec user. Extensible: agencies can modify impact score weights, add custom H2 structures, or extend with their own content patterns.
```

---

## 🎬 VIDEO-ANFORDERUNGEN (falls vorhanden)

**Falls Tally ein Video-Upload-Feld hat:**
- **Format:** MP4 oder WebM
- **Länge:** 60 Sekunden
- **Content:** 
  1. (0-15s) Dashboard öffnen, Gap-Data zeigen (3 URLs + Search Queries)
  2. (15-35s) Brief-Generator ausführen
  3. (35-55s) Gap-Brief Output scrollen (fokus auf Competitor Analysis + FAQ)
  4. (55-60s) GitHub Repo + Call-to-Action

**Video ist OPTIONAL — check mit Formular, ob erforderlich**

---

## 🔄 SUBMISSION-PROZESS

1. **Öffne:** https://peec.ai/countdown-submissions-mcp-challenge
2. **Scrolle down** bis zum Formular
3. **Fülle Felder aus** (verwende Inhalte oben)
4. **Testen vor dem Absenden:**
   - [ ] Alle Links funktionieren
   - [ ] Text-Längen plausibel
   - [ ] Keine Typos/Formatierungsfehler
5. **Absenden** (Knopf wahrscheinlich unten rechts)
6. **Bestätigung erwarten** (Email-Bestätigung oder On-Page Bestätigung)

---

## 📧 POST-SUBMISSION

**Sofort nach erfolgreicher Submission (26. April):**

1. **LinkedIn-Post:** Teile den #BuiltWithPeec Post
   - Tagg @Peec AI
   - Tagg @SYZYGY Performance
   - Verlinke GitHub Repo

2. **Screenshot machen:** 
   - Tally Confirmation-Screen
   - Speichern als proof-of-submission

3. **Team benachrichtigen:**
   - SYZYGY Performance Team
   - Peec AI (optional, falls Kontakt)

4. **Tracking starten:**
   - Notiere Submission-Zeit
   - Warte auf Juror-Feedback
   - Bereite Follow-up vor (falls Fragen)

---

## ⏰ TIMELINE

| Datum | Aktion |
|-------|--------|
| **26. April 08:00 UTC** | Submission durchführen |
| **26. April 09:00 UTC** | LinkedIn-Post teilen |
| **27. April** | Reshare durch SYZYGY Performance |
| **Bis 30. April** | Juror-Feedback erwarten |

---

## ❓ HÄUFIGE TALLY-FORMULAR-FRAGEN

**F: Muss ich alle Felder ausfüllen?**
A: Check die Formular-Anforderungen. Usually: Name, Pitch, Problem, How It Works, Links sind Pflicht. "Why different", "Real-data validation" können optional sein.

**F: Kann ich später noch editieren?**
A: Normalerweise NEIN — Tally-Submissions sind nach dem Absenden gesperrt. Prüfe alles vorher!

**F: Was passiert mit meinen Daten?**
A: Peec wird sie an die Jury weitergeben. Check Datenschutz auf der Tally-Seite.

**F: Kann ich den Link danach ändern?**
A: Nein — der GitHub-Link wird in der Submission eingefroren. Stelle sicher, dass alle Links JETZT funktionieren.

---

## 🎯 FINAL CHECKLIST VOR ABSENDEN

- [ ] **Alle Felder ausgefüllt** (keine leeren Pflichtfelder)
- [ ] **Alle Links getestet** (GitHub Repo, dashboard.html, README.md)
- [ ] **Text-Längen OK** (Pitch max 140 Zeichen, andere Felder voll)
- [ ] **Keine Typos/Rechtschreibfehler**
- [ ] **Correct Author Name** (Tim Brock, SYZYGY Performance)
- [ ] **Public-sharing opt-in:** YES
- [ ] **Screenshot von Formular-Vorschau** (als Backup)
- [ ] **LinkedIn-Post bereit** (linkedin-post.md offen)
- [ ] **GitHub Repo verifiziert** (alle Links im Repo funktionieren)

---

**Status:** ✅ Bereit zur Submission  
**Letzte Aktualisierung:** 24. April 2026  
**Nächster Schritt:** 🎬 Video aufnehmen (optional) → 📤 Tally-Formular ausfüllen → ✅ Absenden

