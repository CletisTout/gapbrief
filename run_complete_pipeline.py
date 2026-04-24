#!/usr/bin/env python3
"""
Complete Gap-Brief Pipeline - End-to-End Orchestration

Orchestriert den kompletten Workflow:
1. gap_analyzer.py     → Peec-Daten sammeln & als JSON exportieren
2. generate_gap_brief.py → Gap-Briefs + Schema-Markups generieren
3. Distribute          → Briefs an Team verteilen (optional)

Verwendung:
    python run_complete_pipeline.py --project-id YOUR_ID
    python run_complete_pipeline.py --project-id YOUR_ID --distribute slack
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from typing import Optional, List


class PipelineOrchestrator:
    """Orchestriert den kompletten Gap-Brief-Generierungs-Workflow"""

    def __init__(self, project_id: Optional[str] = None, api_key: Optional[str] = None):
        self.project_id = project_id or os.getenv('PEEC_PROJECT_ID')
        self.api_key = api_key or os.getenv('PEEC_API_KEY')
        self.output_dir = "./gap-briefs"
        self.gaps_json = "gaps-data.json"

        # Stelle sicher dass Output-Dir existiert
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self, distribute: Optional[str] = None, skip_analysis: bool = False) -> bool:
        """
        Führt kompletten Pipeline aus

        Args:
            distribute: Optionale Distribution Method (slack, email, etc.)
            skip_analysis: Skip analysis step (nutze existierende gaps-data.json)

        Returns:
            True if erfolgreich, False if Fehler
        """
        print("\n" + "="*70)
        print("🚀 GAP-BRIEF COMPLETE PIPELINE")
        print("="*70)

        try:
            # STEP 1: Analyse
            if not skip_analysis:
                print("\n⏳ STEP 1: Analysiere Content Gaps (Peec API)...")
                if not self._run_analysis():
                    print("❌ Gap-Analyse fehlgeschlagen")
                    return False
            else:
                print("\n⏭️  STEP 1: Überspringe Gap-Analyse (nutze existierende Daten)")

            # STEP 2: Validiere Gap-Daten
            print("\n⏳ STEP 2: Validiere Gap-Daten...")
            if not self._validate_gaps_json():
                print("❌ Gap-Daten Validierung fehlgeschlagen")
                return False

            # STEP 3: Generiere Gap-Briefs
            print("\n⏳ STEP 3: Generiere Gap-Briefs mit FAQs & Schemas...")
            if not self._run_generation():
                print("❌ Gap-Brief-Generierung fehlgeschlagen")
                return False

            # STEP 4: Validiere Output
            print("\n⏳ STEP 4: Validiere generierte Gap-Briefs...")
            briefs = self._validate_generated_briefs()
            if not briefs:
                print("❌ Generierte Briefs Validierung fehlgeschlagen")
                return False

            # STEP 5: Drucke Summary
            print("\n⏳ STEP 5: Generiere Production Summary...")
            self._print_summary(briefs)

            # STEP 6: Optional Distribute
            if distribute:
                print(f"\n⏳ STEP 6: Verteile Briefs via {distribute}...")
                if not self._distribute(briefs, distribute):
                    print(f"⚠️  Distribution via {distribute} fehlgeschlagen (nicht kritisch)")

            print("\n" + "="*70)
            print("✅ PIPELINE ERFOLGREICH ABGESCHLOSSEN")
            print("="*70)
            print(f"\n📁 Gap-Briefs sind bereit in: {self.output_dir}")
            print(f"   - {len(briefs)} Markdown-Dateien")
            print(f"   - {len(briefs)} Schema-JSON-Dateien")
            print(f"\n🎯 Nächster Schritt: Verteile Briefs an Writers und starten Sie die Produktion")

            return True

        except Exception as e:
            print(f"\n❌ Pipeline Fehler: {e}")
            return False

    def _run_analysis(self) -> bool:
        """Führt gap_analyzer.py aus"""
        try:
            cmd = [
                "python", "gap_analyzer.py",
                "--output", self.gaps_json,
                "--summary"
            ]

            if self.project_id:
                cmd.extend(["--project-id", self.project_id])
            if self.api_key:
                cmd.extend(["--api-key", self.api_key])

            print(f"   Befehl: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("   ✅ Gap-Analyse abgeschlossen")
                return True
            else:
                print(f"   ❌ Fehler: {result.stderr}")
                return False

        except Exception as e:
            print(f"   ❌ Fehler beim Ausführen gap_analyzer.py: {e}")
            return False

    def _validate_gaps_json(self) -> bool:
        """Validiert dass gaps-data.json vorhanden und gültig ist"""
        if not os.path.exists(self.gaps_json):
            print(f"   ❌ {self.gaps_json} nicht gefunden")
            return False

        try:
            with open(self.gaps_json, 'r', encoding='utf-8') as f:
                data = json.load(f)

            gaps = data.get('gaps', [])
            if not gaps:
                print(f"   ❌ Keine Gaps in {self.gaps_json}")
                return False

            print(f"   ✅ {len(gaps)} Gaps in {self.gaps_json} gefunden und validiert")
            return True

        except json.JSONDecodeError as e:
            print(f"   ❌ JSON Parse-Fehler in {self.gaps_json}: {e}")
            return False

    def _run_generation(self) -> bool:
        """Führt generate_gap_brief.py aus"""
        try:
            cmd = [
                "python", "generate_gap_brief.py",
                "--input", self.gaps_json,
                "--auto-generate",
                "--output-dir", self.output_dir
            ]

            print(f"   Befehl: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("   ✅ Gap-Briefs generiert")
                return True
            else:
                print(f"   ❌ Fehler: {result.stderr}")
                return False

        except Exception as e:
            print(f"   ❌ Fehler beim Ausführen generate_gap_brief.py: {e}")
            return False

    def _validate_generated_briefs(self) -> List[str]:
        """Validiert dass alle Gap-Briefs und Schemas generiert wurden"""
        if not os.path.exists(self.output_dir):
            print(f"   ❌ Output-Verzeichnis {self.output_dir} nicht gefunden")
            return []

        briefs = []
        schema_files = []

        for filename in os.listdir(self.output_dir):
            if filename.endswith('.md'):
                briefs.append(os.path.join(self.output_dir, filename))
            elif filename.endswith('.schemas.json'):
                schema_files.append(os.path.join(self.output_dir, filename))

        if not briefs:
            print(f"   ❌ Keine Gap-Briefs in {self.output_dir} gefunden")
            return []

        print(f"   ✅ {len(briefs)} Gap-Briefs (.md) generiert")
        print(f"   ✅ {len(schema_files)} Schema-Dateien (.json) generiert")

        return briefs

    def _print_summary(self, briefs: List[str]):
        """Druckt Production Summary"""
        print("\n" + "="*70)
        print("📊 PRODUCTION SUMMARY")
        print("="*70)

        # Laden Gap-Daten für Info
        with open(self.gaps_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            gaps = data.get('gaps', [])

        print(f"\n📈 Gaps analysiert: {len(gaps)}")
        for gap in gaps:
            print(f"\n  Gap #{gap['gap_id']}: {gap['topic']}")
            print(f"    Priority: {gap['priority']}")
            print(f"    Impact Score: {gap['impact_score']}")
            print(f"    Visibility Lift: {gap['estimated_visibility_lift']}")
            print(f"    Own Brand Status: {gap['own_brand_status']} ({gap['own_brand_visibility']})")

        print(f"\n📁 Generierte Dateien: {len(briefs)}")
        for brief in briefs:
            filename = os.path.basename(brief)
            size_kb = os.path.getsize(brief) / 1024
            print(f"    ✅ {filename} ({size_kb:.1f} KB)")

        print(f"\n⏱️  Geschätzte Produktionszeiten:")
        total_hours = 0
        for gap in gaps:
            hours = int(gap['production_hours'].split('-')[1])
            total_hours += hours
            print(f"    Gap #{gap['gap_id']}: {gap['production_hours']} hours")
        print(f"    Total: ~{total_hours} hours (3-4 Wochen mit Team)")

        print(f"\n🎯 Nächste Schritte:")
        print(f"    1. Verteile Gap-Briefs an zuständige Writers")
        print(f"    2. Nutze PRODUCTION-ROADMAP.md für Timeline")
        print(f"    3. Nutze DAILY-CHECKLIST.md für Daily-Tracking")
        print(f"    4. Starten Sie Produktion am {datetime.now().strftime('%d. %B %Y')}")

        print("\n" + "="*70)

    def _distribute(self, briefs: List[str], method: str) -> bool:
        """
        Verteilt Gap-Briefs (optional)

        Args:
            briefs: Liste der generierten Brief-Dateien
            method: Distribution-Methode (slack, email, etc.)

        Returns:
            True if erfolgreich
        """
        if method == "slack":
            return self._distribute_slack(briefs)
        elif method == "email":
            return self._distribute_email(briefs)
        else:
            print(f"   ⚠️  Unbekannte Distribution-Methode: {method}")
            return False

    def _distribute_slack(self, briefs: List[str]) -> bool:
        """Verteilt via Slack (Placeholder)"""
        print("   ℹ️  Slack Distribution noch nicht implementiert")
        print("   📋 Manuelle Alternative: Kopiere .md Dateien zu Slack Channel")
        return True

    def _distribute_email(self, briefs: List[str]) -> bool:
        """Verteilt via Email (Placeholder)"""
        print("   ℹ️  Email Distribution noch nicht implementiert")
        print("   📋 Manuelle Alternative: Sende .md Dateien per Email")
        return True


def main():
    """Hauptfunktion für CLI-Nutzung"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Complete Gap-Brief Pipeline - End-to-End Orchestration'
    )
    parser.add_argument('--project-id', help='Peec Project ID (optional)')
    parser.add_argument('--api-key', help='Peec API Key (oder nutze PEEC_API_KEY in .env)')
    parser.add_argument('--distribute', choices=['slack', 'email'],
                      help='Optional: Verteile Briefs nach Generierung')
    parser.add_argument('--skip-analysis', action='store_true',
                      help='Skip analysis step (nutze existierende gaps-data.json)')

    args = parser.parse_args()

    # Führe Pipeline aus
    orchestrator = PipelineOrchestrator(
        project_id=args.project_id,
        api_key=args.api_key
    )

    success = orchestrator.run(
        distribute=args.distribute,
        skip_analysis=args.skip_analysis
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    m