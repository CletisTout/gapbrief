#!/bin/bash
# Complete Gap-Brief Pipeline - Bash-Wrapper
# Einfache Schnittstelle zum Ausführen der kompletten Pipeline

set -e  # Exit bei Fehler

echo ""
echo "=========================================="
echo "🚀 GAP-BRIEF COMPLETE PIPELINE"
echo "=========================================="
echo ""

# Prüfe dass Python verfügbar ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nicht gefunden. Bitte installieren Sie Python 3.8+"
    exit 1
fi

# Prüfe dass erforderliche Dateien existieren
if [ ! -f "gap_analyzer.py" ]; then
    echo "❌ gap_analyzer.py nicht gefunden"
    exit 1
fi

if [ ! -f "generate_gap_brief.py" ]; then
    echo "❌ generate_gap_brief.py nicht gefunden"
    exit 1
fi

if [ ! -f "run_complete_pipeline.py" ]; then
    echo "❌ run_complete_pipeline.py nicht gefunden"
    exit 1
fi

# Prüfe .env Datei
if [ ! -f ".env" ]; then
    echo "⚠️  .env Datei nicht gefunden"
    echo "   Bitte erstelle .env mit:"
    echo "   PEEC_API_KEY=your_key_here"
    echo "   FIRECRAWL_API_KEY=your_key_here"
    echo ""
fi

# Parse Argumente
PROJECT_ID=""
API_KEY=""
DISTRIBUTE=""
SKIP_ANALYSIS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --project-id)
            PROJECT_ID="$2"
            shift 2
            ;;
        --api-key)
            API_KEY="$2"
            shift 2
            ;;
        --distribute)
            DISTRIBUTE="$2"
            shift 2
            ;;
        --skip-analysis)
            SKIP_ANALYSIS=true
            shift
            ;;
        --help)
            echo "Verwendung: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --project-id ID      Peec Project ID"
            echo "  --api-key KEY        Peec API Key (oder nutze .env)"
            echo "  --distribute METHOD  Distribution (slack, email)"
            echo "  --skip-analysis      Skip analysis step"
            echo "  --help              Diese Hilfe anzeigen"
            echo ""
            exit 0
            ;;
        *)
            echo "❌ Unbekannte Option: $1"
            echo "   Nutze --help für Optionen"
            exit 1
            ;;
    esac
done

# Lade .env wenn vorhanden
if [ -f ".env" ]; then
    echo "📝 Lade .env Datei..."
    export $(cat .env | grep -v '#' | xargs)
fi

# Baue Python-Befehl
PYTHON_CMD="python3 run_complete_pipeline.py"

if [ -n "$PROJECT_ID" ]; then
    PYTHON_CMD="$PYTHON_CMD --project-id $PROJECT_ID"
fi

if [ -n "$API_KEY" ]; then
    PYTHON_CMD="$PYTHON_CMD --api-key $API_KEY"
fi

if [ -n "$DISTRIBUTE" ]; then
    PYTHON_CMD="$PYTHON_CMD --distribute $DISTRIBUTE"
fi

if [ "$SKIP_ANALYSIS" = true ]; then
    PYTHON_CMD="$PYTHON_CMD --skip-analysis"
fi

# Führe Pipeline aus
echo "▶️  Starten: $PYTHON_CMD"
echo ""

$PYTHON_CMD

# Prüfe Exit-Code
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ PIPELINE ERFOLGREICH"
    echo "=========================================="
    echo ""
    echo "📁 Gap-Briefs sind bereit in ./gap-briefs"
    echo "📋 Siehe PRODUCTION-ROADMAP.md für nächste Schritte"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ PIPELINE FEHLGESCHLAGEN"
    echo "=========================================="
    echo ""
    echo "🔍 Fehlerbehandlung:"
    echo "   1. Prüfe .env Datei (API Keys)"
    echo "   2. Prüfe Peec API Verbindung"
    echo "   3. Prüfe Python-Dependencies"
    echo "   4. Siehe error logs oben"
    echo ""
    exit 1
fi
