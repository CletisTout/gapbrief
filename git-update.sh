#!/bin/bash

# GapBrief Git Update Script
# Synchronisiert alle neuen Komponenten mit GitHub

echo "🔄 Starting GapBrief Git Update..."
echo ""

# 1. Check Git Status
echo "📊 Current Git Status:"
git status
echo ""

# 2. Add all changes
echo "➕ Staging changes..."
git add -A
echo "✅ Files staged"
echo ""

# 3. Show what will be committed
echo "📝 Changes to commit:"
git status --short
echo ""

# 4. Commit mit aussagekräftiger Message
echo "💾 Committing..."
git commit -m "feat: Add Dashboard Generator + Rules

- Add generate_dashboard.py (automated HTML dashboard from gaps.json)
- Add DASHBOARD-GENERATION-GUIDE.md (design specs & rules)
- Update dashboard.html (now based on gaps-example.json data)
- Update tally-submission.md (GitHub URL: CletisTout/gapbrief)
- Update linkedin-post.md (with dashboard links)
- Update TALLY-SUBMISSION-CHECKLIST.md (dashboard workflow)

Dashboard is now part of the automated pipeline:
gap_analyzer.py → gaps.json → generate_dashboard.py → dashboard.html

Ready for Tally submission (April 26, 2026)"

echo ""
echo "✅ Commit successful"
echo ""

# 5. Show commit log
echo "📜 Latest commits:"
git log --oneline -3
echo ""

# 6. Push to remote
echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ All done! Repository updated."
echo ""
echo "GitHub: https://github.com/CletisTout/gapbrief"
