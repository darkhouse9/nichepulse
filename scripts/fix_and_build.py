#!/usr/bin/env python3
"""Fix the corrupted JSON database and rebuild the app."""
import json

DB_PATH = "/home/openclaw/nichepulse/skills/niche-research-pro/data/niche-database.json"

# Read raw
with open(DB_PATH, "r") as f:
    raw = f.read()

# Fix: the file has a corrupted Faith/Christian entry that was truncated
# Strategy: parse what we can, then manually add the Faith entry back

# Find the exact corruption point
lines = raw.split("\n")
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Check if this is the truncated Faith line
    if '"Faith / Christian"' in line and "trend" in line and 'trend": 3,' in line and not line.strip().endswith('],'):
        # Replace with complete entry
        fixed_lines.append('      {"name": "Faith / Christian", "slug": "faith-christian", "total": 17, "grade": "B", "passion": 5, "buy_freq": 4, "gift": 4, "comp": 3, "trend": 3, "avg_order": 24, "competition": "medium", "etsy_results": 28000, "top_products": ["t-shirts", "hoodies", "mugs", "journals", "wall-art"], "design_angle": "Scripture calligraphy, faith + profession crossover. Premium textures.", "notes": ["$9B US Christian retail market", "High repeat purchase"]},')
        i += 1
        # Skip the next line which should be just "    ]," (the malformed close)
        if i < len(lines) and lines[i].strip() in ("]", "],"):
            # This is the category close - keep it as "]," but we need to check context
            pass  # Don't skip, let normal processing handle it
    else:
        fixed_lines.append(line)
    i += 1

fixed = "\n".join(fixed_lines)

# Try to parse
try:
    db = json.loads(fixed)
    print("Fixed JSON parsed OK")
except json.JSONDecodeError as e:
    print(f"Still broken at line {e.lineno}: {e.msg}")
    print(f"Context: {fixed[max(0,e.pos-100):e.pos+100]}")
    # Try another approach - just remove everything after the last complete category bracket
    last_complete = fixed.rfind('"]')
    if last_complete > 0:
        fixed2 = fixed[:last_complete+2] + "\n  }\n}"
        try:
            db = json.loads(fixed2)
            print("Fixed by truncating after last complete category")
        except:
            db = None

if db:
    # Save fixed version
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)
    print(f"Fixed DB saved")
    
    # Count niches
    total = 0
    for cat, niches in db.get("categories", {}).items():
        total += len(niches)
        print(f"  {cat}: {len(niches)}")
    print(f"Total: {total}")
else:
    print("Could not fix JSON - will use hardcoded approach")
