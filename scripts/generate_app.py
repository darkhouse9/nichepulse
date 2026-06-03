#!/usr/bin/env python3
"""Generate app.html by injecting the full niche database from JSON into the template."""
import json

# Load the full database
with open("/home/openclaw/nichepulse/skills/niche-research-pro/data/niche-database.json") as f:
    db = json.load(f)

# Flatten categories into a single list
niches = []
for cat_name, cat_niches in db.get("categories", {}).items():
    for n in cat_niches:
        if n.get("slug","") == "pickleball-2":  # skip duplicate
            continue
        # Map category name to cat slug
        cat_map = {
            "Pets & Animals": "pets", "Gaming & Esports": "culture",
            "Professions & Careers": "professions", "Health & Fitness": "fitness",
            "Lifestyle & Identity": "lifestyle", "Hobbies & Micro-Passions": "hobbies",
            "Family & Milestones": "family", "Humor & Meme Culture": "culture",
            "Home & Decor": "home", "Tech & Crypto": "tech",
            "Seasonal & Holidays": "seasonal"
        }
        n["cat"] = cat_map.get(cat_name, "lifestyle")
        niches.append(n)

print(f"Total niches: {len(niches)}")

# Check coverage
slugs = [n.get("slug","") for n in niches]
print(f"Has cottagecore: {'cottagecore' in slugs or any('cottage' in s for s in slugs)}")
print(f"Has astrology: {any('astro' in s or 'zodiac' in s for s in slugs)}")
print(f"Has soccer: {any('soccer' in s or 'football' in s for s in slugs)}")

# Check for common POD terms
terms = ["cottage","astrology","zodiac","music","soccer","football","movies","anime","reading","books","baking","cooking","gardening","plants","yoga","running","golf","tennis","cowboy","western"]
for t in terms:
    found = [n["name"] for n in niches if t in n.get("slug","") or t in n.get("name","").lower()]
    if found:
        print(f"  {t}: {found}")
    else:
        print(f"  {t}: MISSING")

# Generate JS array
def make_icon(name):
    name_lower = name.lower()
    icon_map = {
        "dog":"🐕","cat":"🐱","pet":"🐾","bird":"🦜","reptile":"🦎",
        "horse":"🐴","exotic":"🐍","memorial":"🕊️",
        "nurse":"🩺","teacher":"📚","blue":"🔧","tech":"💻","first":"🚒",
        "military":"🎖️","remote":"🏠",
        "power":"🏋️","yoga":"🧘","pickleball":"🏓","mental":"💚",
        "adhd":"🧠","spoon":"🥄","sober":"🌱","autistic":"♾️",
        "introvert":"📖","vegan":"🌱","lgbtq":"🏳️‍🌈","faith":"✝️",
        "board":"🎲","brew":"🍺","beer":"🍺","vinyl":"💿","coffee":"☕",
        "wine":"🍷","fish":"🎣",
        "baby":"👶","grand":"👵","fur":"🐾","parent":"👨‍👧",
        "dark":"💀","dad":"😂","sarcastic":"😏","esports":"🏆",
        "retro":"🎮","gaming":"🎮","indie":"🕹️","streamer":"📺",
        "farm":"🏡","witch":"🔮","academia":"📖","coastal":"🏖️",
        "crypto":"₿","ai":"🤖",
        "halloween":"🎃","christmas":"🎄","mother":"💐","father":"💐",
        "equestrian":"🐴"
    }
    for key, icon in icon_map.items():
        if key in name_lower:
            return icon
    return "🎯"

lines = []
for i, n in enumerate(niches):
    name = n.get("name","").replace('"','\\"')
    slug = n.get("slug","")
    icon = make_icon(name)
    total = n.get("total", 15)
    grade = n.get("grade","B")
    p = n.get("passion",3)
    bf = n.get("buy_freq",3)
    gf = n.get("gift",3)
    c = n.get("comp",3)
    tr = n.get("trend",3)
    ao = n.get("avg_order",24)
    comp = n.get("competition","medium")
    etsy = n.get("etsy_results",5000)
    prds = n.get("top_products",["t-shirts","mugs"])
    prds_json = json.dumps(prds)
    cat = n.get("cat","lifestyle")
    design = n.get("design_angle","").replace('"','\\"').replace("'","\\'")
    notes = n.get("notes",[])
    notes_json = json.dumps(notes).replace('"','\\"')
    
    # Build scores object
    scores_obj = f"{{passion:{p},buy_freq:{bf},gift:{gf},competition:{c},trend:{tr}}}"
    
    line = f'{{nm:"{name}",slug:"{slug}",t:{total},g:"{grade}",p:{p},bf:{bf},gf:{gf},c:{c},tr:{tr},ao:{ao},comp:"{comp}",etsy:{etsy},prds:{prds_json},icon:"{icon}",cat:"{cat}",scores:{scores_obj},design:"{design}",notes:{notes_json}}}'
    lines.append(line)

js_array = "const NICHES=[" + ",\n".join(lines) + "];"

print(f"\nJS array: {len(js_array)} chars, {len(lines)} niches")

# Write to a temp file
with open("/tmp/niches_js.txt","w") as f:
    f.write(js_array)

print("Written to /tmp/niches_js.txt")
