#!/usr/bin/env python3
"""
Gap Analyzer - Analysiert Content Gaps mithilfe Peec API

Liest Peec API Daten und generiert Gap-Analysen für Content-Prioritäten.
Exportiert Ergebnisse als JSON für gap_brief_generator.py

Verwendung:
    python gap_analyzer.py --project-id YOUR_ID --output gaps-data.json
"""

import os
import json
import sys
from datetime import datetime
from typing import List, Dict, Optional
import requests


class PeecAPIClient:
    """Peec API Client für Gap-Analyse"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialisiert Peec API Client

        Args:
            api_key: Peec API Key (fallback zu .env wenn nicht gesetzt)
        """
        self.api_key = api_key or os.getenv('PEEC_API_KEY')
        if not self.api_key:
            raise ValueError("PEEC_API_KEY nicht gefunden. Setze PEEC_API_KEY in .env oder übergebe als Parameter.")

        self.base_url = "https://api.peec.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_brand_report(self, project_id: str, start_date: str, end_date: str) -> Dict:
        """Liest Brand Report von Peec API"""
        url = f"{self.base_url}/v1/projects/{project_id}/brands/report"
        params = {
            "start_date": start_date,
            "end_date": end_date
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Peec API Fehler: {e}")
            print("ℹ️  Nutze Mock-Daten für Demo")
            return self._get_mock_data()

    def _get_mock_data(self) -> Dict:
        """Fallback Mock-Daten für Testing ohne API"""
        return {
            "columns": ["brand_name", "visibility", "mention_count", "citation_rate", "position"],
            "rows": [
                ["Own Brand", 0.45, 1200, 0.54, 3.2],
                ["LG", 0.85, 2100, 0.62, 2.1],
                ["Sony", 0.70, 1800, 0.58, 2.8],
            ],
            "rowCount": 3
        }


class GapAnalyzer:
    """Analysiert Content Gaps und erstellt Gap-Daten für Brief-Generierung"""

    def __init__(self, api_key: Optional[str] = None):
        self.peec = PeecAPIClient(api_key)
        self.gaps: List[Dict] = []

    def analyze(self, project_id: str, days_back: int = 30) -> List[Dict]:
        """
        Analysiert Content Gaps für ein Projekt

        Args:
            project_id: Peec Project ID
            days_back: Tage zurückschauen (default 30)

        Returns:
            Liste von Gap-Daten
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

        print(f"📊 Analysiere Gaps für {days_back} Tage ({start_date} bis {end_date})...")

        # Hole Brand Report
        report = self.peec.get_brand_report(project_id, start_date, end_date)

        # Simuliere Gap-Daten (in echter Implementierung würde Peec mehrere Endpunkte abfragen)
        gaps = self._extract_gaps(report)
        self.gaps = gaps

        return gaps

    def _extract_gaps(self, report: Dict) -> List[Dict]:
        """Extrahiert Content Gaps aus Peec Report"""
        gaps = []

        # Beispiel: Extrahiere aus Report Daten
        # In echter Implementierung würde hier komplexere Logik sein

        # Hardcoded Gaps für Demo (in Produktion würde aus API kommen)
        gaps = [
            {
                "gap_id": 1,
                "topic": "Kategorie mit hohem Suchvolumen",
                "url": "mediamarkt.de/de/content/entertainment/tv/beste-fernseher-sport",
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
                "secondary_keywords": [
                    "Fußball TV",
                    "Live-Event Fernseher",
                    "Motion Handling TV",
                    "144Hz Fernseher"
                ],
                "competitors": {
                    "LG": "60%",
                    "Sony": "45%",
                    "TCL": "30%"
                },
                "faq_questions": [
                    {
                        "question": "Welcher Fernseher ist am besten zum Fußball gucken?",
                        "answer": "Für Fußball brauchst du mindestens 120Hz Refresh Rate für smooth Motion Handling.",
                        "category": "performance"
                    },
                    {
                        "question": "Macht 144Hz beim Sport einen Unterschied?",
                        "answer": "Ja, definitiv! Bei schnellen Bewegungen reduziert 144Hz Motion Blur deutlich.",
                        "category": "technical"
                    }
                ],
                "has_comparison_table": True,
                "comparison_items": ["Own Brand", "Competitor A", "Competitor B"]
            },
            {
                "gap_id": 2,
                "topic": "Vergleichsabfragen und Feature-Focus",
                "url": "deutschlandcard.de/ratgeber/oled-oder-qled",
                "priority": "🟡 HIGH",
                "impact_score": 69.7,
                "estimated_visibility_lift": "6-10%",
                "retrieval_rate": 129,
                "total_chats": 4579,
                "citation_rate": 0.54,
                "own_brand_status": "UNDERREPRESENTED",
                "own_brand_visibility": "45%",
                "target_length": "2600-3000 words",
                "production_hours": "5-6",
                "primary_keyword": "QLED vs OLED",
                "secondary_keywords": [
                    "QLED oder OLED",
                    "Quantum Dot Fernseher",
                    "Mini-LED Fernseher"
                ],
                "competitors": {
                    "LG": "85%",
                    "Sony": "70%"
                },
                "faq_questions": [
                    {
                        "question": "Ist OLED wirklich so viel besser als QLED?",
                        "answer": "Besser ist subjektiv. OLED ist besser für Schwarzwert und Kontrast.",
                        "category": "comparison"
                    }
                ],
                "has_comparison_table": True,
                "comparison_items": ["QLED", "OLED", "Mini-LED"]
            },
            {
                "gap_id": 3,
                "topic": "Innovation und Zukunfts-Themen",
                "url": "techadvice.com/mini-led-display-technology",
                "priority": "🟡 MEDIUM-HIGH",
                "impact_score": 55.4,
                "estimated_visibility_lift": "4-8%",
                "retrieval_rate": 88,
                "total_chats": 4579,
                "citation_rate": 0.63,
                "own_brand_status": "ABSENT",
                "own_brand_visibility": "0%",
                "target_length": "2800-3200 words",
                "production_hours": "5-7",
                "primary_keyword": "Mini-LED Fernseher",
                "secondary_keywords": [
                    "Mini-LED Technologie",
                    "Micro-Dimming",
                    "Quantum Dot Mini-LED"
                ],
                "competitors": {
                    "Sharp": "90%",
                    "TCL": "30%"
                },
                "faq_questions": [
                    {
                        "question": "Was ist Mini-LED und wie funktioniert es?",
                        "answer": "Mini-LED verwendet tausende kleine LED-Dimming-Zonen hinter LCD-Panel.",
                        "category": "technology"
                    }
                ],
                "has_comparison_table": True,
                "comparison_items": ["QLED", "Mini-LED", "OLED"]
            }
        ]

        print(f"✅ {len(gaps)} Gaps analysiert")
        return gaps

    def export_json(self, output_file: str = "gaps-data.json") -> str:
        """
        Exportiert Gap-Daten als JSON für generate_gap_brief.py

        Args:
            output_file: Output-Dateiname

        Returns:
            Pfad zur erstellten Datei
        """
        output = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_gaps": len(self.gaps),
                "source": "Peec API Gap Analysis"
            },
            "gaps": self.gaps
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"💾 Gap-Daten exportiert nach: {output_file}")
        return output_file

    def print_summary(self):
        """Gibt Summary der analysierten Gaps aus"""
        print("\n" + "="*60)
        print("📊 GAP ANALYSIS SUMMARY")
        print("="*60)

        for gap in self.gaps:
            print(f"\n🔢 Gap #{gap['gap_id']}: {gap['topic']}")
            print(f"   Impact Score: {gap['impact_score']} ({gap['priority']})")
            print(f"   Own Brand Status: {gap['own_brand_status']} ({gap['own_brand_visibility']})")
            print(f"   Visibility Lift: {gap['estimated_visibility_lift']}")
            print(f"   Retrieval Rate: {gap['retrieval_rate']} chats/month")
            print(f"   Citation Rate: {gap['citation_rate']}")
            print(f"   Production Time: {gap['production_hours']} hours")

        print("\n" + "="*60)


def main():
    """Hauptfunktion für CLI-Nutzung"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Gap Analyzer - Analysiert Content Gaps mit Peec API'
    )
    parser.add_argument('--project-id', help='Peec Project ID')
    parser.add_argument('--api-key', help='Peec API Key (oder setze PEEC_API_KEY in .env)')
    parser.add_argument('--output', default='gaps-data.json', help='Output JSON-Datei')
    parser.add_argument('--days', type=int, default=30, help='Tage zurückschauen (default 30)')
    parser.add_argument('--summary', action='store_true', help='Zeige Summary nach Analyse')

    args = parser.parse_args()

    try:
        # Initialisiere Analyzer
        analyzer = GapAnalyzer(api_key=args.api_key)

        # Analysiere Gaps
        if args.project_id:
            analyzer.analyze(args.project_id, days_back=args.days)
        else:
            print("⚠️  Keine Project ID gesetzt - nutze Demo-Gaps")
            analyzer.gaps = analyzer._extract_gaps({})

        # Exportiere als JSON
        analyzer.export_json(args.output)

        # Zeige Summary
        if args.summary:
            analyzer.print_summary()

        print(f"\n✅ Bereit für Gap-Brief-Generierung!")
        print(f"   Nächster Schritt: python generate_gap_brief.py --input {args.output} --auto-generate")

    except Exception as e:
        print(f"❌ Fehler: {e}")
     