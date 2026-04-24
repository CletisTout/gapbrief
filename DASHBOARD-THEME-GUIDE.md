# Dashboard Theme Integration Guide

## 🎨 Theme: Tech Innovation

Das GapBrief Dashboard wird mit dem **Theme Factory - Tech Innovation** Theme gestylt. Dieses Theme ist optimiert für moderne, technische Präsentationen.

---

## 📋 Quick Start: Theme anwenden

### 1️⃣ Theme aus Theme Factory Repo kopieren

```bash
# Theme-Spezifikation ansehen (bereits integriert)
cat DASHBOARD-THEME-GUIDE.md
```

### 2️⃣ Dashboard mit Theme regenerieren

```bash
# Standard: Dashboard aus gaps.json mit Theme
python generate_dashboard.py \
  --input gaps.json \
  --output dashboard.html \
  --theme tech-innovation
```

### 3️⃣ Änderungen zu Git committen

```bash
# Option A: Automatisiertes Update-Skript
bash git-theme-update.sh

# Option B: Manuell
git add dashboard.html DASHBOARD-GENERATION-GUIDE.md
git commit -m "style: Update dashboard theme"
git push origin main
```

---

## 🎨 Theme Spezifikation

### Farbpalette

**Tech Innovation** - Modern, bold, high-contrast:

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Electric Blue** | `#0066ff` | 0, 102, 255 | Primärer Akzent (Rankings, Links) |
| **Neon Cyan** | `#00ffff` | 0, 255, 255 | Sekundärer Akzent (Impact-Metriken) |
| **Dark Gray** | `#1e1e1e` | 30, 30, 30 | Hintergrund (Tech-clean) |
| **White** | `#ffffff` | 255, 255, 255 | Haupttext (max Kontrast) |
| **Dim Gray** | `#b0b0b0` | 176, 176, 176 | Sekundärtext (Labels) |
| **Line Gray** | `#3a3a3a` | 58, 58, 58 | Borders & dividers |
| **Red** | `#ff4e5b` | 255, 78, 91 | Warning/Status ABSENT |
| **Green** | `#6bcf7f` | 107, 207, 127 | Success/Status OK |

### CSS Root Variables

```css
:root {
  --bg: #1e1e1e;           /* Haupthintergrund */
  --bg-2: #2a2a2a;         /* Panel/Card Hintergrund */
  --ink: #ffffff;          /* Haupttext */
  --ink-dim: #b0b0b0;      /* Dimmed text (labels) */
  --line: #3a3a3a;         /* Border & divider lines */
  --accent: #0066ff;       /* Electric Blue – primary */
  --accent-2: #00ffff;     /* Neon Cyan – secondary */
  --warn: #ff4e5b;         /* Warning/ABSENT status */
  --ok: #6bcf7f;           /* Success/OK status */
}
```

### Typography

**Font-Familie:** `DejaVu Sans`

| Element | Weight | Size | Usage |
|---------|--------|------|-------|
| Body text | 400 (Regular) | 14px | Fließtext, Labels |
| Headers (h2, h3) | 700 (Bold) | 22-28px | Abschnittsti­tel |
| Rank numbers | 700 (Bold) | 40px | Gap rankings |
| Big metrics | 700 (Bold) | 40-44px | Impact scores |
| Brand logo | 700 (Bold) | 22px | Header branding |

### Gradient Backgrounds

Subtile Hintergründe mit Theme-Farben:

```css
body {
  background-image:
    radial-gradient(1200px 600px at 20% -10%, 
      rgba(0,102,255,0.12),           /* Electric Blue */
      transparent 60%),
    radial-gradient(900px 500px at 90% 110%, 
      rgba(0,255,255,0.08),           /* Neon Cyan */
      transparent 60%);
}
```

---

## 🔧 Theme Anpassen

### Farbe ändern

1. **CSS Variable ändern** in `dashboard.html`:

```html
<style>
:root {
  --accent: #0066ff;      /* Change to new color */
  --accent-2: #00ffff;
  /* ... */
}
</style>
```

2. **Dashboard regenerieren** (falls aus gaps.json):

```bash
python generate_dashboard.py --input gaps.json --output dashboard.html
```

3. **Änderungen committen**:

```bash
git add dashboard.html
git commit -m "style: Update dashboard accent colors"
git push origin main
```

### Font ändern

1. Ändere Font-Familie im `<style>` Block:

```css
:root {
  --display: "YourFont", sans-serif;  /* Header font */
  --mono: "YourFont", sans-serif;     /* Body font */
}
```

2. Stelle sicher, dass Font aus Google Fonts importiert wird (oder lokal verfügbar):

```html
<link href="https://fonts.googleapis.com/css2?family=YourFont:wght@400;700&display=swap" rel="stylesheet" />
```

3. Teste im Browser und committe.

---

## 📊 Dashboard Elements mit Theme

### Hero Section
- **Headline (h1)**: DejaVu Sans Bold, 36-64px, White
- **Accent text**: Electric Blue (#0066ff)
- **Lead text**: Dim Gray (#b0b0b0)
- **Impact Card**: Dark Gray background, Neon Cyan metrics

### Key Metrics Strip (4 Numbers)
- **Labels**: Dim Gray, uppercase
- **Big numbers**: Bold, 44px, color coded:
  - Status colors (Red = ABSENT, Green = OK)
  - Accent colors (Blue for competitors, Cyan for lift)

### Competitor Bar Chart
- **Names**: White text, 13px
- **Own brand (Own Brand)**: Electric Blue gradient
- **Competitors**: Dim Gray
- **Bar background**: Dark Gray panel

### Gap Clusters
- **Rank numbers**: Electric Blue, Bold, 40px
- **Topic title**: White, Bold, 22px
- **Tags**: Border with color coding
  - Red border: ABSENT status
  - Blue border: CRITICAL priority
- **URLs**: White, underline on hover (Blue)
- **Impact Card**: Dark Gray background, Cyan metrics

### CTA Section
- **Headline**: White, Bold, 32px
- **Accent**: Electric Blue
- **Command box**: Dark Gray background, Cyan text
- **Border**: White top/bottom

---

## 🚀 Deployment Checklist

- [ ] Dashboard mit Theme lokal getestet
- [ ] Farben in allen Browsern überprüft
- [ ] Kontrast ausreichend (WCAG AA minimum)
- [ ] Responsive Design getestet (mobil, tablet, desktop)
- [ ] git add dashboard.html
- [ ] git commit -m "style: Apply theme"
- [ ] git push origin main
- [ ] GitHub-Seite geladen und Theme überprüft

---

## 📚 Referenzen

- **Theme Factory**: Dokumentation siehe `DASHBOARD-GENERATION-GUIDE.md`
- **Color Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Google Fonts**: https://fonts.google.com/
- **Dashboard Code**: `dashboard.html` im GitHub Repo

---

## 🎯 Nächste Schritte

1. ✅ Theme angewendet: **Tech Innovation** (Electric Blue + Neon Cyan)
2. ⚙️ Workflow-Dokumentation: **DASHBOARD-GENERATION-GUIDE.md** aktualisiert
3. 🔄 Git-Integration: **git-theme-update.sh** erstellt
4. 📤 Tally-Submission: Neues Theme-Dashboard bereit

---

**Status:** ✅ Theme Applied & Documented  
**Last Updated:** 2026-04-24  
**Theme:** Tech Innovation  
**Ready for:** Tally Submission (April 26, 2026)
