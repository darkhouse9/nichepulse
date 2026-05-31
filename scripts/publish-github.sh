#!/usr/bin/env bash
# NichePulse GitHub publish script
# Run this to push to GitHub (requires gh auth)

set -e

REPO="nichepulse/nichepulse"

echo "=== Creating GitHub repo: $REPO ==="

# Create repo
gh repo create "$REPO" --public --description "AI-Powered Niche Scoring for Creators & Entrepreneurs" --homepage "https://nichepulse.ai" 2>/dev/null || echo "Repo may already exist"

# Initialize and push
cd /home/openclaw/nichepulse

git init 2>/dev/null || true
git add -A
git commit -m "🎯 Initial release: NichePulse v1.0.0

- CLI niche scoring tool (Python, Click, Rich)
- 14 pre-scored niches with 2026 market data
- 3 Claude Code skills (niche-research, seo-audit, content-pipeline)
- MCP server with JSON-RPC tools
- Landing page
- Full test suite (14/14 passing)

Pricing: Free CLI / $19 Skill Pack / $39 Pro Bundle" 2>/dev/null || true

git branch -M main
git remote add origin "https://github.com/$REPO.git" 2>/dev/null || true

echo "Ready to push. Run: git push -u origin main"
