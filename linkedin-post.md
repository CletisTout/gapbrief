# LinkedIn-Post — Entwurf

**Plattform:** LinkedIn · **Sprache:** Deutsch · **Länge:** ~280 Wörter
**Medien:** 60-sekündiges Screencast-Video des Dashboards + Brief-Generators, plus Screenshot des Briefs.
**Hashtags:** #BuiltWithPeec #GEO #AISearch #ContentStrategy

---

## Variante A — „Starker Opener, Daten + Multi-URL-Analyse"

Own Brand hat im Peec-Projekt „Own Brand TV" im Topic **Gamer** eine Sichtbarkeit von **44 %**.

Klingt gut. Ist es nicht.

Weil auf der meistgesuchten Query des Topics — „beste smart tvs für gaming und streaming" — die Mention-Rate **0 %** ist. Alle drei Quellen, die ChatGPT und Gemini dafür zitieren, listen LG, TCL und Hisense. Kein Own Brand-Modell dabei.

Das ist das Problem mit Durchschnitts-Metriken im GEO: Sie verschleiern die Prompts, die tatsächlich wichtig sind.

Für die Peec MCP Challenge habe ich einen Claude-Code-Skill gebaut, der genau das adressiert: **GapBrief**. Ein Python-Tool, das Peec MCP abfragt, pro Prompt einen Impact-Score berechnet, die **Top-3 gewinnenden Konkurrenz-URLs scraped**, deren Content-Struktur (H2-Gerüst, FAQ-Muster, Vergleichstabellen) analysiert, und daraus einen **publish-reifen Content-Brief** erzeugt.

Das Wichtigste: Der Brief zeigt nicht nur, dass Own Brand fehlt — er zeigt, **wie die Konkurrenz gewinnt**: Welche YouTube-Kanäle, Reddit-Threads, Review-Sites werden zitiert, und wie ist ihr Content strukturiert? Welche Modelle werden genannt, in welcher Reihenfolge, in welchem Kontext?

Der Brief beinhaltet:
- Entity-Checkliste (welche Konkurrenz-Modelle müssen genannt werden)
- H2-Gerüst angepasst an Komplexität (10–14 Sections)
- Schema-Empfehlung (FAQ, Comparison, Article)
- **6–10 echte Search Queries**, die zu diesem Gap führen
- **Modellierter Lift**: +25 pp visibility in 30 Tagen

Plus: Ein 7-Tage-Retrieval-Check, der automatisch prüft, ob die neue Seite den Gap tatsächlich geschlossen hat.

Kompletter Flow ist MIT-lizenziert auf GitHub. Wer Peec nutzt, kann das in unter 5 Minuten auf eigene Projekte (Finance, Pharma, FMCG, Tech) anwenden.

→ Repo: github.com/CletisTout/gapbrief
→ Dashboard mit Beispieldaten: blob/main/dashboard.html

#BuiltWithPeec #GEO #AISearch

---

## Variante B — „Reflective, Meta-Take + Multi-URL"

Der interessanteste Teil an der Peec MCP Challenge war nicht der Code. Es war die Erkenntnis, dass **Share of Voice eine Lüge erzählt**.

Own Brand hat 44 % SoV im Gaming-Topic meines Test-Projekts. Auf der wichtigsten einzelnen Query: 0 %.

Warum? Weil die Gewinner-Quellen dieser Query zwei YouTube-Vergleichsvideos und eine Reddit-Diskussion sind. Alle drei nennen LG-Modelle, TCL-Modelle, Hisense-Modelle. Own Brand taucht in keiner einzigen auf.

Das ist kein Visibility-Problem. Das ist ein **Modell-Nennungs-Problem auf Prompt-Ebene** — und es wird von jedem Dashboard verdeckt, das SoV über Topics mittelt.

Mein Submission zur Challenge: **GapBrief**. Ein Claude-Code-Skill, der Peec-Gap-Daten in Content-Briefs übersetzt, die ein Writer am Montag morgen umsetzen kann. Aber nicht als One-Shot-Prompt. Sondern als **cron-fähiges Python-Tool** mit echten Competitor-Insights:

- **Multi-URL-Analyse**: Scraped die Top-3 Konkurrenz-URLs und zeigt, wie sie gewinnen
- **Content-Dekonstruktion**: H2-Struktur, FAQ-Muster, Entity-Nennung der Konkurrenz — alles analysiert
- **Search Intent**: 6–10 echte User-Queries, nicht erraten
- **7-Tage-Validation**: Misst am Nächsten Montag, ob die Seite den Gap tatsächlich geschlossen hat

Open source. MIT-lizenziert. Extensibel.

Repo und Beispiel-Brief in den Kommentaren. Feedback und PRs willkommen — besonders von Leuten, die GapBrief in Finance, Pharma oder FMCG testen.

#BuiltWithPeec #GEO

---

## Kommentar zum Pinning (Call-to-Action)

→ github.com/syzygy-performance/gapbrief
→ Dashboard-Preview: [link zu dashboard.html auf Github Pages]
→ Beispiel-Brief: examples/project-1/brief-gaming-streaming.md im Repo
→ Screencast (60 sec): [Loom-Link]

Feedback, Questions, PRs willkommen. Wer Peec in anderen Branchen/Märkten nutzt — testet den Skill und schreibt mir direkt. Interesse an erweiterten Features (Multi-Language, Custom H2 Templates, Lift Forecasting)?

---

## Notizen für Posting

- Posten am Tag der Submission (26. April), spätestens 27. April morgens DE-Zeit
- Video: 60-Sek-Loom mit (1) Dashboard öffnen, (2) Gap-Data (mit 3 URLs + Search Queries) zeigen, (3) Brief-Generator laufen lassen, (4) Brief-Output scrollen (fokus auf Competitor Analysis + FAQ). Kein Voiceover; Text-Overlays reichen.
- @Peec AI taggen — Malte Landwehr ist Juror, darf ruhig mitlesen
- Nach 24h: Post bei @SYZYGY Performance resharen lassen
- Bei ≥50 Kommentaren: Follow-up-Post mit Lift-Report-Screenshot (falls Retrieval-Check schon Daten liefert) + Angebot für Einzelgespräche
- Optional: Tag @Claude (@Anthropic) für MCP-Sichtbarkeit
