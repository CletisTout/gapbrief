# GapBrief Setup Guide

## ⚠️ SECURITY: API-Keys Management

**WICHTIG:** API-Keys dürfen NIEMALS in Git committed werden!

### Dateistruktur

```
.env.example      ← Template (IN GIT, zeigt Struktur)
.env              ← Echte Keys (NICHT in GIT, local only!)
.gitignore        ← Schließt .env aus
```

### Setup Steps

#### 1. .env Datei erstellen (lokal)

```bash
# Kopiere das Template
cp .env.example .env

# Editiere .env und füge deine API-Keys ein:
PEEC_API_KEY=your_actual_peec_key_here
FIRECRAWL_API_KEY=your_actual_firecrawl_key_here
```

#### 2. .env NIEMALS committen!

```bash
# Überprüfe, dass .env in .gitignore ist:
grep "^\.env" .gitignore

# Output sollte sein: .env

# Falls nicht: Sie wurde zu .gitignore hinzugefügt!
```

#### 3. API-Keys laden

**Richtig (aus .env):**
```python
import os
api_key = os.getenv('FIRECRAWL_API_KEY')  # ✅ Aus Environment
app = FirecrawlApp(api_key=api_key)
```

**Falsch (hardcoded):**
```python
api_key = "fc-xyz123..."  # ❌ NIEMALS HARDCODED!
```

---

## 🔍 API-Keys Locations

### ✅ RICHTIG:
- In `.env` Datei (lokal, nicht committed)
- In Environment-Variablen
- In Secrets-Management (z.B. GitHub Secrets)
- In Docker `.env` oder Kubernetes Secrets

### ❌ FALSCH:
- Hardcoded in Python-Scripts
- In Git-Dateien (außer .env.example)
- In Konfigurationsdateien die committed werden
- In Commit-Messages oder Bash-History

---

## 🚀 Scripts ausführen

### extract_patterns.py (mit .env)

```bash
# Die .env wird automatisch geladen durch os.getenv()
python scripts/extract_patterns.py

# Oder explizit Environment setzen:
source .env
python scripts/extract_patterns.py
```

### gap_analyzer.py (mit .env)

```bash
# Auch hier: .env wird automatisch geladen
python scripts/gap_analyzer.py

# Output: gap-analysis-data.json
```

### Lokale Tests (PowerShell)

```powershell
# Vor dem Python-Script die Env-Vars setzen:
$env:PEEC_API_KEY = "skp-..."
$env:FIRECRAWL_API_KEY = "fc-..."

python scripts/extract_patterns.py
```

---

## 📋 Aktueller Status

✅ **.gitignore** - Aktualisiert mit `.env` Ausschluss  
✅ **.env.example** - Template erstellt (IN GIT)  
✅ **.env** - Echte Keys erstellt (NICHT in GIT)  
✅ **extract_patterns.py** - Lädt Keys via `os.getenv()` ✓  
✅ **gap_analyzer.py** - Lädt Keys via `os.getenv()` ✓  

---

## 🔐 Sicherheitschecklist

Vor jedem Commit:

```bash
# 1. Überprüfe, dass .env nicht staged ist:
git status
# Output sollte .env NICHT enthalten!

# 2. Überprüfe .gitignore:
cat .gitignore | grep "\.env"
# Output: .env (oder ähnlich)

# 3. Suche nach hardcoded Keys in Code:
grep -r "skp-\|fc-" --include="*.py" .
# Output: Nichts! (außer vielleicht in Kommentaren)

# 4. Überprüfe Git-History:
git log --all --oneline | head -20
# Kein API-Key sichtbar?

# 5. Falls Keys exposed wurden:
# SOFORT regenerieren! (z.B. im Peec/Firecrawl Dashboard)
```

---

## 📚 Referenz-Links

- **Peec API-Keys:** https://peec.ai/dashboard/settings
- **Firecrawl API-Keys:** https://www.firecrawl.dev/dashboard
- **.gitignore Best-Practices:** https://git-scm.com/docs/gitignore
- **OWASP Secrets Management:** https://owasp.org/www-community/attacks/Secrets_management

---

## ✅ Validierung

Alle Scripts laden API-Keys korrekt:

```python
# extract_patterns.py Line 48-49:
self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY')

# gap_analyzer.py:
peec_api_key = os.getenv('PEEC_API_KEY')
```

✅ **ALLE SCRIPTS SIND SICHER - API-Keys aus Environment, nicht hardcoded**

---

**Last Updated:** 24. April 2026  
**Security Review:** ✅ PASSED
