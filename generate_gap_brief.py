#!/usr/bin/env python3
"""
Gap Brief Generator - Automatisierte Erstellung von Gap-Brief-Dokumenten

Features:
- Peec Analysedaten Integration (Impact Score, Retrieval Rate, Citation Rate)
- Komplexitäts-adaptives Template (Simple, Medium, Complex)
- Firecrawl Content Scraping & Analyse (NEW!)
- JSON-LD Schema Generierung (Article, FAQ, Comparison)
- Deutsch-sprachige Templates

Verwendung:
    python generate_gap_brief.py --input gaps.json --auto-generate
    python generate_gap_brief.py --input gaps.json --with-firecrawl
"""

import json
import os
import sys
import requests
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class GapData:
    """Datenstruktur für Gap-Analyse"""
    gap_id: int
    topic: str
    urls: List[Dict]  # Neu: Liste statt einzelne URL
    search_queries: List[str]  # Neu: Search Queries
    priority: str
    impact_score: float
    estimated_visibility_lift: str
    retrieval_rate: int
    total_chats: int
    citation_rate: float
    own_brand_status: str
    own_brand_visibility: str
    competitors: Dict[str, str]
    target_length: str
    production_hours: str
    primary_keyword: str
    secondary_keywords: List[str]
    faq_questions: Optional[List[Dict]] = None
    has_comparison_table: bool = False
    comparison_items: Optional[List[str]] = None
    comparison_properties: Optional[Dict] = None


class FirecrawlContentExtractor:
    """Extrahiert und analysiert Content von URLs mit Firecrawl"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Firecrawl Extractor

        Args:
            api_key: Firecrawl API Key (oder aus .env FIRECRAWL_API_KEY)
        """
        self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY')
        self.base_url = "https://api.firecrawl.dev/v1"
        self.available = bool(self.api_key)

    def scrape_url(self, url: str) -> Optional[Dict]:
        """
        Scraped eine einzelne URL mit Firecrawl

        Args:
            url: URL zum Scrapen

        Returns:
            Dict mit gescrapten Daten oder None bei Fehler
        """
        if not self.available:
            print(f"  ⚠️  Firecrawl nicht konfiguriert, überspringe: {url}")
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "url": url,
                "pageOptions": {
                    "onlyMainContent": True
                }
            }

            response = requests.post(
                f"{self.base_url}/scrape",
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "url": url,
                    "title": data.get("metadata", {}).get("title", "N/A"),
                    "markdown": data.get("markdown", ""),
                    "status": "success"
                }
            else:
                print(f"  ⚠️  Firecrawl Fehler für {url}: {response.status_code}")
                return None

        except Exception as e:
            print(f"  ⚠️  Scraping-Fehler für {url}: {str(e)}")
            return None

    def analyze_content(self, scraped_data: List[Dict]) -> Dict:
        """
        Analysiert gescrapte Content

        Args:
            scraped_data: Liste von gescrapten Content

        Returns:
            Analyse-Ergebnisse
        """
        analysis = {
            "analyzed_urls": [],
            "key_patterns": [],
            "missing_topics": [],
            "best_practices": [],
            "competitor_insights": []
        }

        if not scraped_data:
            return analysis

        # Analyse pro URL
        for data in scraped_data:
            if data and data.get("status") == "success":
                content = data.get("markdown", "")

                # Extrahiere Struktur
                h2_count = content.count("\n## ")
                has_faq = "faq" in content.lower() or "häufig" in content.lower()
                has_comparison = "|" in content  # Markdown-Tabellen
                has_cta = "kaufen" in content.lower() or "jetzt" in content.lower()

                analysis["analyzed_urls"].append({
                    "url": data["url"],
                    "title": data["title"],
                    "h2_sections": h2_count,
                    "has_faq": has_faq,
                    "has_comparison": has_comparison,
                    "has_cta": has_cta,
                    "word_count": len(content.split())
                })

                # Best Practices identifizieren
                if h2_count >= 10:
                    analysis["best_practices"].append(
                        "Gute Section-Struktur mit 10+ Überschriften"
                    )
                if has_faq:
                    analysis["best_practices"].append(
                        "FAQ-Section vorhanden (für Rich Snippets)"
                    )
                if has_comparison:
                    analysis["best_practices"].append(
                        "Vergleichstabellen eingebunden"
                    )
                if has_cta:
                    analysis["best_practices"].append(
                        "Klare Call-to-Action vorhanden"
                    )

        # Gemeinsamkeiten analysieren
        if analysis["analyzed_urls"]:
            avg_h2 = sum(u["h2_sections"] for u in analysis["analyzed_urls"]) / len(analysis["analyzed_urls"])
            avg_words = sum(u["word_count"] for u in analysis["analyzed_urls"]) / len(analysis["analyzed_urls"])

            analysis["key_patterns"] = [
                f"Durchschnittliche Struktur: {avg_h2:.0f} H2-Sektionen",
                f"Durchschnittliche Länge: {avg_words:.0f} Wörter",
                f"{len([u for u in analysis['analyzed_urls'] if u['has_faq']])}/{len(analysis['analyzed_urls'])} URLs haben FAQ"
            ]

        return analysis

    def generate_analysis_section(self, analysis: Dict) -> str:
        """
        Generiert einen Markdown-Section für Competitor Content Analyse

        Args:
            analysis: Analyse-Ergebnisse

        Returns:
            Markdown-Text für Gap-Brief
        """
        if not analysis.get("analyzed_urls"):
            return ""

        section = "\n## 🔍 COMPETITOR CONTENT ANALYSE (Firecrawl)\n\n"

        # URLs analysieren
        for i, url_data in enumerate(analysis["analyzed_urls"], 1):
            section += f"### URL {i}: {url_data['title']}\n"
            section += f"- **Word Count:** {url_data['word_count']:,} Wörter\n"
            section += f"- **H2 Sections:** {url_data['h2_sections']}\n"
            section += f"- **FAQ vorhanden:** {'✅ Ja' if url_data['has_faq'] else '❌ Nein'}\n"
            section += f"- **Vergleichstabelle:** {'✅ Ja' if url_data['has_comparison'] else '❌ Nein'}\n"
            section += f"- **CTA vorhanden:** {'✅ Ja' if url_data['has_cta'] else '❌ Nein'}\n\n"

        # Best Practices
        if analysis["best_practices"]:
            section += "### Best Practices (von Competitors)\n"
            for practice in analysis["best_practices"]:
                section += f"- ✅ {practice}\n"
            section += "\n"

        # Key Patterns
        if analysis["key_patterns"]:
            section += "### Erkannte Muster\n"
            for pattern in analysis["key_patterns"]:
                section += f"- 📊 {pattern}\n"
            section += "\n"

        # Empfehlungen
        section += "### Empfehlungen für unseren Content\n"
        section += "- Minimum " + (f"{min(u['h2_sections'] for u in analysis['analyzed_urls'])}-" if analysis["analyzed_urls"] else "")
        section += f"{max(u['h2_sections'] for u in analysis['analyzed_urls']) if analysis['analyzed_urls'] else '10'} H2-Sektionen einplanen\n"
        section += f"- Zieltext-Länge: {sum(u['word_count'] for u in analysis['analyzed_urls']) // len(analysis['analyzed_urls']) if analysis['analyzed_urls'] else 2500} Wörter\n"

        if not all(u['has_faq'] for u in analysis['analyzed_urls']):
            section += "- 🎯 **FAQ-Section ist ein Differenzierungsmerkmal** (nicht alle Competitors haben es)\n"

        section += "\n---\n\n"

        return section


class ComplexityLevel:
    """Bestimmt Komplexität basierend auf Impact Score"""

    @staticmethod
    def determine(impact_score: float) -> tuple:
        """
        Returns: (level_name, h2_count, word_count_min, word_count_max, faq_min, faq_max)
        """
        if impact_score >= 75:
            return ("COMPLEX", 14, 2800, 3200, 10, 12)
        elif impact_score >= 50:
            return ("MEDIUM", 12, 2600, 3000, 10, 12)
        else:
            return ("SIMPLE", 10, 2400, 2600, 8, 10)


class SchemaGenerator:
    """Generiert JSON-LD Schema Markups für SEO"""

    @staticmethod
    def generate_article_schema(gap_id: int, topic: str, word_count: int) -> Dict:
        """Generiert Article Schema"""
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": f"GapBrief #{gap_id}: {topic}",
            "description": f"Detaillierte Content Gap Analyse für {topic}",
            "datePublished": datetime.now().isoformat(),
            "dateModified": datetime.now().isoformat(),
            "author": {
                "@type": "Organization",
                "name": "Gap Brief Generator"
            },
            "wordCount": word_count
        }

    @staticmethod
    def generate_faq_schema(faqs: List[Dict]) -> Dict:
        """Generiert FAQPage Schema"""
        main_entity = []
        for faq in faqs[:12]:
            main_entity.append({
                "@type": "Question",
                "name": faq.get("question", ""),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq.get("answer", "")
                }
            })

        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": main_entity
        }

    @staticmethod
    def generate_comparison_schema(items: List[str], properties: Dict) -> Dict:
        """Generiert Comparison Schema"""
        compare_items = []
        for item in items:
            compare_items.append({
                "@type": "Product",
                "name": item
            })

        return {
            "@context": "https://schema.org",
            "@type": "ComparisonChart",
            "itemsCompared": compare_items,
            "properties": properties
        }


class GapBriefGenerator:
    """Hauptklasse für Gap-Brief-Generierung"""

    def __init__(self, use_firecrawl: bool = False):
        self.use_firecrawl = use_firecrawl
        self.firecrawl = FirecrawlContentExtractor() if use_firecrawl else None

    def generate_brief(self, gap: GapData) -> tuple:
        """
        Generiert Gap-Brief und Schemas

        Returns:
            (markdown_content, schema_json)
        """
        complexity_level, h2_count, word_min, word_max, faq_min, faq_max = ComplexityLevel.determine(gap.impact_score)

        # Firecrawl Content-Analyse (optional)
        firecrawl_section = ""
        if self.use_firecrawl and self.firecrawl and self.firecrawl.available:
            print(f"  🔄 Scraping URLs mit Firecrawl...")
            scraped_content = []
            for url_info in gap.urls[:3]:  # Max 3 URLs
                scraped = self.firecrawl.scrape_url(url_info["url"])
                if scraped:
                    scraped_content.append(scraped)

            if scraped_content:
                print(f"  ✅ {len(scraped_content)} URLs gescraped")
                analysis = self.firecrawl.analyze_content(scraped_content)
                firecrawl_section = self.firecrawl.generate_analysis_section(analysis)

        # Markdown generieren
        urls_section = self._generate_urls_section(gap.urls, gap.search_queries)
        h2_structure = self._generate_h2_structure(h2_count, gap.topic)
        faq_section = self._generate_faq_section(gap.faq_questions, faq_min, faq_max)

        markdown = f"""# GapBrief #{gap.gap_id}: {gap.topic}
## Content Gap Analyse & Strategie

**Gap ID:** #{gap.gap_id}
**Priority:** {gap.priority}
**Impact Score:** {gap.impact_score}
**Geschätzte Visibility Steigerung:** {gap.estimated_visibility_lift}
**Erstellt:** {datetime.now().strftime('%d. %B %Y')}

---

## 📊 GAP OVERVIEW

### Peec-Metriken
- **Retrieval-Rate:** {gap.retrieval_rate} / {gap.total_chats} Chats ({gap.retrieval_rate/gap.total_chats*100:.1f}%)
- **Citation-Rate:** {gap.citation_rate} pro Abruf
- **Own Brand Status:** {gap.own_brand_status} ({gap.own_brand_visibility})

### Relevante URLs & Queries
{urls_section}

---

{firecrawl_section}

## 🎯 CONTENT STRATEGY

### Article Goal
- Objektive, detaillierte Erklärung
- Konkrete Use-Cases
- Own Brand Positioning
- Konkrete Kaufempfehlungen

### Spezifikationen
- **Zieltext-Länge:** {word_min:,}-{word_max:,} Wörter
- **H2 Sections:** {h2_count}
- **Komplexität-Level:** {complexity_level}
- **FAQ-Fragen:** {faq_min}-{faq_max}
- **Produktionszeit:** {gap.production_hours} Stunden

### Recommended H2 Structure
{h2_structure}

## 💬 FAQ SECTION

{faq_section}

## 🎯 KEYWORDS

**Hauptkeyword:** {gap.primary_keyword}

**Secondary Keywords:**
{', '.join(gap.secondary_keywords)}

---

## 📋 PRE-PUBLICATION CHECKLIST

- [ ] Word Count: {word_min:,}-{word_max:,} Wörter
- [ ] H2 Sections: Alle {h2_count} vorhanden
- [ ] FAQ Block: Mindestens {faq_min} Fragen
- [ ] Schema Markup: Article + FAQPage
- [ ] Internal Links: 5-8
- [ ] External Links: 3-5
- [ ] Bilder: 5-7

---

*Generiert: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}*
"""

        # Schemas generieren
        schemas = {
            "article": SchemaGenerator.generate_article_schema(gap.gap_id, gap.topic, word_max),
            "faq": SchemaGenerator.generate_faq_schema(gap.faq_questions or []),
            "comparison": SchemaGenerator.generate_comparison_schema(
                gap.comparison_items or [],
                gap.comparison_properties or {}
            ) if gap.has_comparison_table else None
        }

        return markdown, schemas

    def _generate_urls_section(self, urls: List[Dict], queries: List[str]) -> str:
        """Generiert URLs und Queries Section"""
        section = "### Primary URLs\n"
        for i, url_info in enumerate(urls[:3], 1):
            section += f"{i}. **{url_info['title']}**\n"
            section += f"   - URL: {url_info['url']}\n"
            section += f"   - Retrieval-Count: {url_info.get('retrieved_in', 'N/A')}\n"
            section += f"   - Citation-Count: {url_info.get('citation_count', 'N/A')}\n"

        section += "\n### Search Queries (Nutzer-Intent)\n"
        for query in queries[:6]:
            section += f"- {query}\n"

        return section

    def _generate_h2_structure(self, count: int, topic: str) -> str:
        """Generiert H2-Struktur"""
        generic_h2s = [
            "Einführung & Überblick",
            "Warum dieses Thema wichtig ist",
            "Grundkonzepte erklären",
            "Praktische Anwendungen",
            "Häufige Fragen",
            "Best Practices",
            "Häufige Fehler vermeiden",
            "Tipps & Tricks",
            "Vergleiche & Alternativen",
            "Zukunftstrends",
            "Häufig gestellte Fragen (FAQ)",
            "Fazit & Empfehlung",
            "Nächste Schritte",
            "Weitere Ressourcen"
        ]

        structure = "```\n"
        for i, h2 in enumerate(generic_h2s[:count], 1):
            structure += f"{i}. ## {h2}\n"
        structure += "```"

        return structure

    def _generate_faq_section(self, faqs: Optional[List[Dict]], min_count: int, max_count: int) -> str:
        """Generiert FAQ-Sektion"""
        if not faqs:
            return f"*Erstelle {min_count}-{max_count} Fragen basierend auf Nutzer-Intent*"

        section = ""
        for i, faq in enumerate(faqs[:max_count], 1):
            section += f"**{i}. {faq.get('question', '')}**\n"
            section += f"{faq.get('answer', '')}\n\n"

        return section


def main():
    """Hauptfunktion"""
    import argparse

    parser = argparse.ArgumentParser(description='Gap-Brief Generator')
    parser.add_argument('--input', required=True, help='Input JSON file')
    parser.add_argument('--output-dir', default='./gap-briefs', help='Output directory')
    parser.add_argument('--with-firecrawl', action='store_true', help='Use Firecrawl for content analysis')

    args = parser.parse_args()

    # Lade Gaps
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Erstelle Output-Verzeichnis
    os.makedirs(args.output_dir, exist_ok=True)

    # Generator
    generator = GapBriefGenerator(use_firecrawl=args.with_firecrawl)

    print(f"\n🚀 Generiere Gap-Briefs...")
    print(f"📁 Output: {args.output_dir}")
    print(f"🔄 Firecrawl: {'✅ Aktiv' if args.with_firecrawl else '⏭️  Übersprungen'}\n")

    for gap_data in data.get('gaps', []):
        gap = GapData(**gap_data)

        print(f"📝 Gap #{gap.gap_id}: {gap.topic}")

        markdown, schemas = generator.generate_brief(gap)

        # Speichere Markdown
        md_file = os.path.join(args.output_dir, f"gap-brief-{gap.gap_id:03d}-{gap.topic.lower().replace(' ', '-')}.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"  ✅ Markdown: {os.path.basename(md_file)}")

        # Speichere Schemas
        schema_file = os.path.join(args.output_dir, f"gap-brief-{gap.gap_id:03d}-{gap.topic.lower().replace(' ', '-')}.schemas.json")
        with open(schema_file, 'w', encoding='utf-8') as f:
            json.dump(schemas, f, indent=2, ensure_ascii=False)
        print(f"  ✅ Schemas: {os.path.basename(schema_file)}")

    print(f"\n✅ Fertig! {len(data.get('gaps', []))} Gap-Briefs generiert.\n")


if __name__ == '__main__':
    main()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                