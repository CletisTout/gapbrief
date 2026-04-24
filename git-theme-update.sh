#!/bin/bash

# GapBrief Dashboard Theme Update Script
# Aktualisiert das Dashboard mit Tech Innovation Theme und committed alle Änderungen

echo "🎨 GapBrief Dashboard Theme Update"
echo "Theme: Tech Innovation (Electric Blue + Neon Cyan)"
echo ""

# 1. Check Git Status
echo "📊 Current Git Status:"
git status
echo ""

# 2. Add all changes (including dashboard.html with new theme)
echo "➕ Staging changes..."
git add -A
echo "✅ Files staged"
echo ""

# 3. Show what will be committed
echo "📝 Changes to commit:"
git status --short
echo ""

# 4. Commit mit aussagekräftiger Message
echo "💾 Committing dashboard theme update..."
git commit -m "style: Apply Tech Innovation theme to dashboard

Dashboard Styling:
- Colors: Electric Blue (#0066ff) primary + Neon Cyan (#00ffff) secondary
- Background: Dark Gray (#1e1e1e) with White text (#ffffff)
- Typography: DejaVu Sans Bold for headers (font-weight: 700)
- Theme: Tech Innovation for cutting-edge MCP presentation
- Contrast: Enhanced for improved readability

Documentation:
- Updated DASHBOARD-GENERATION-GUIDE.md with theme specifications
- CSS variables documented for consistent styling
- Theme colors and typography documented for reproduction

Files Modified:
- dashboard.html (color palette, fonts, gradients)
- DASHBOARD-GENERATION-GUIDE.md (theme section with full specs)
- git-theme-update.sh (this workflow script)

Ready for Tally submission (April 26, 2026)"

echo ""
echo "✅ Commit successful"
echo ""

# 5. Show commit log
echo "📜 Latest commits:"
git log --oneline -5
echo ""

# 6. Push to remote
echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Dashboard theme update complete!"
echo ""
echo "Theme Details:"
echo "  - Primary: Electric Blue (#0066ff)"
echo "  - Secondary: Neon Cyan (#00ffff)"
echo "  - Background: Dark Gray (#1e1e1e)"
echo "  - Fonts: DejaVu Sans (modern tech aesthetic)"
echo ""
echo "GitHub: https://github.com/CletisTout/gapbrief"
echo "Dashboard: https://github.com/CletisTout/gapbrief/blob/main/dashboard.html"
