#!/bin/bash
# Install NichePulse skills into any Claude Code / Cursor project
SKILLS_DIR="${1:-.claude/skills}"
mkdir -p "$SKILLS_DIR/nichepulse-niche-research"
mkdir -p "$SKILLS_DIR/nichepulse-seo-audit"
mkdir -p "$SKILLS_DIR/nichepulse-content-pipeline"
cp skills/niche-research/SKILL.md "$SKILLS_DIR/nichepulse-niche-research/SKILL.md"
cp skills/seo-audit/SKILL.md "$SKILLS_DIR/nichepulse-seo-audit/SKILL.md"
cp skills/content-pipeline/SKILL.md "$SKILLS_DIR/nichepulse-content-pipeline/SKILL.md"
echo "✅ NichePulse 3 skills installed to $SKILLS_DIR"
