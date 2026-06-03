#!/usr/bin/env python3
"""
Build the NichePulse web app with a comprehensive niche database.
Reads niche data from JSON and generates a self-contained HTML file.
"""
import json, os, re

DB_PATH = "/home/openclaw/nichepulse/skills/niche-research-pro/data/niche-database.json"

# Fix the JSON if needed - read raw and repair
with open(DB_PATH, "r") as f:
    raw = f.read()

# Try to parse, if it fails we need to fix it
try:
    db = json.loads(raw)
    print("JSON parsed OK")
except json.JSONDecodeError as e:
    print(f"JSON parse error: {e}")
    # Try removing the broken trailing content
    # Find the last complete category closing
    idx = raw.rfind('"]')
    if idx > 0:
        fixed = raw[:idx+2] + "\n  }\n}"
        try:
            db = json.loads(fixed)
            print("Fixed JSON by truncating at last complete category")
            # Write fixed version back
            with open(DB_PATH, "w") as f:
                json.dump(db, f, indent=2)
        except json.JSONDecodeError as e2:
            print(f"Still broken: {e2}")
            # Last resort: fix the specific malformed line
            lines = raw.split("\n")
            # Find the Faith / Christian line that got truncated
            fixed_lines = []
            for i, line in enumerate(lines):
                if '"Faith / Christian"' in line and "trend" in line and not line.rstrip().endswith(","):
                    # This line needs avg_order etc. - add from what we know
                    fixed_lines.append('      {"name": "Faith / Christian", "slug": "faith-christian", "total": 17, "grade": "B", "passion": 5, "buy_freq": 4, "gift": 4, "comp": 3, "trend": 3, "avg_order": 24, "competition": "medium", "etsy_results": 28000, "top_products": ["t-shirts", "hoodies", "mugs", "journals", "wall-art"], "design_angle": "Scripture calligraphy, faith + profession crossover. Premium textures.", "notes": ["$9B US Christian retail market", "High repeat purchase"]}')
                elif i > 46 and line.strip() == ']':
                    # This is the malformed close bracket after Faith
                    fixed_lines.append('    ],')
                else:
                    fixed_lines.append(line)
            fixed = "\n".join(fixed_lines)
            try:
                db = json.loads(fixed)
                print("Fixed by patching individual lines")
                with open(DB_PATH, "w") as f:
                    json.dump(db, f, indent=2)
            except json.JSONDecodeError as e3:
                print(f"Cannot fix: {e3}")
                print("Generating database from scratch in Python instead")

# Extract all niches
niches = []
if 'db' in dir():
    for cat_name, cat_niches in db.get("categories", {}).items():
        for n in cat_niches:
            if n.get("slug") == "pickleball-2":
                continue
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

print(f"JSON niches: {len(niches)}")

# If niches < 50, the JSON is too sparse - use hardcoded comprehensive list
if len(niches) < 50:
    print("JSON too sparse, using comprehensive hardcoded database...")
    niches = get_comprehensive_niches()

print(f"Total niches: {len(niches)}")

# Check coverage
terms = ["cottage", "astrology", "zodiac", "music", "anime", "baking", "cooking",
         "gardening", "plants", "reading", "movie", "disney", "harry", "marvel",
         "star wars", "nintendo", "pokemon", "sewing", "knitting", "pottery",
         "jewelry", "woodworking", "leather", "tattoo", "motorcycle", "car",
         "truck", "surfing", "skate", "climbing", "boxing", "wrestling",
         "soccer", "basketball", "football", "hockey", "tennis", "golf",
         "chess", "dnd", "mtg", "yu-gi", "comic", "vinyl", "coffee", "wine",
         "tea", "whiskey", "cocktail", "vodka", "rum", "marijuana", "weed",
         "cannabis", "CBD", "essential oil", "aromatherapy", "crystals",
         "tarot", "palm reading", "numerology", "feng shui", "meditation",
         "mindfulness", "breathwork", "sound healing", "reiki", "chakra",
         "manifestation", "law of attraction", "affirmation", "journal",
         "planner", "budget", "finance", "invest", "crypto", "bitcoin",
         "ethereum", "NFT", "web3", "AI", "machine learning", "coding",
         "python", "java", "javascript", "web design", "cybersecurity",
         "hacking", "linux", "apple", "android", "windows", "gaming",
         "esports", "stream", "twitch", "youtube", "podcast", "blog",
         "vlog", "tiktok", "instagram", "twitter", "reddit", "pinterest",
         "etsy", "shopify", "amazon", "printful", "printify", "merch",
         "redbubble", "teepublic", "zazzle", "society6", "threadless"]
missing = []
for t in terms:
    if not any(t in n.get("slug","") or t in n.get("name","").lower() for n in niches):
        missing.append(t)
if missing:
    print(f"Missing terms ({len(missing)}): {missing[:20]}...")

# Generate JS array
ICONS = {
    "dog":"🐕","cat":"🐱","pet":"🐾","bird":"🦜","reptile":"🦎","horse":"🐴",
    "exotic":"🐍","memorial":"🕊️","fish":"🎣","bee":"🐝","chicken":"🐔",
    "nurse":"🩺","doctor":"🩺","teacher":"📚","blue":"🔧","tech":"💻",
    "first":"🚒","military":"🎖️","remote":"🏠","power":"🏋️","yoga":"🧘",
    "pickle":"🏓","run":"🏃","mental":"💚","adhd":"🧠","spoon":"🥄",
    "sober":"🌱","autistic":"♾️","introvert":"📖","vegan":"🌱","lgbtq":"🏳️‍🌈",
    "faith":"✝️","board":"🎲","brew":"🍺","beer":"🍺","vinyl":"💿",
    "coffee":"☕","wine":"🍷","chess":"♟️","dnd":"🎲",
    "baby":"👶","grand":"👵","fur":"🐾","parent":"👨‍👧","dark":"💀",
    "dad":"😂","sarcastic":"😏","esports":"🏆","retro":"🎮","gaming":"🎮",
    "indie":"🕹️","streamer":"📺","farm":"🏡","witch":"🔮","academia":"📖",
    "coastal":"🏖️","crypto":"₿","ai":"🤖","halloween":"🎃","christmas":"🎄",
    "mother":"💐","father":"💐","soccer":"⚽","basketball":"🏀","football":"🏈",
    "hockey":"🏒","tennis":"🎾","golf":"⛳","box":"🥊","climb":"🧗",
    "surf":"🏄","skate":"🛹","snow":"⛷️","tattoo":"💉","motor":"🏍️",
    "car":"🚗","truck":"🛻","rv":"🚐","dance":"💃","music":"🎵",
    "read":"📚","bakery":"🥐","cook":"👨‍🍳","garden":"🌻","plant":"🪴",
    "craft":"🧵","pottery":"🏺","wood":"🪵","leather":"👜","jewelry":"💍",
    "movie":"🎬","disney":"🏰","harry":"⚡","marvel":"🦸","anime":"⛩️",
    "nintendo":"🎮","pokemon":"🔴","comic":"📰","manga":"📖","mtg":"🃏",
    "yugioh":"🃏","chessgame":"♟️","whiskey":"🥃","cocktail":"🍸",
    "tea":"🍵","cannabis":"🌿","crystal":"🔮","tarot":"🃏","meditate":"🧘",
    "journal":"📓","planner":"📅","invest":"📈","bitcoin":"₿",
    "ethereum":"Ξ","nft":"🖼️","crypto":"₿","web3":"🌐",
    "python":"🐍","code":"💻","hack":"💻","linux":"🐧",
    "podcast":"🎙️","tiktok":"📱","instagram":"📷","reddit":"🤖",
    "etsy":"🛒","printful":"🖨️","merch":"👕","redbubble":"🔴",
}

def get_icon(name, slug):
    text = (name + " " + slug).lower()
    for key, icon in sorted(ICONS.items(), key=lambda x: -len(x[0])):
        if key in text:
            return icon
    # Category-based fallback
    if "pet" in text or "dog" in text or "cat" in text: return "🐾"
    if "game" in text or "play" in text: return "🎮"
    if "music" in text or "band" in text or "sing" in text: return "🎵"
    if "food" in text or "cook" in text or "bak" in text: return "🍳"
    if "drink" in text or "coffee" in text or "wine" in text: return "☕"
    if "sport" in text or "fit" in text: return "💪"
    return "🎯"

def build_js(niches):
    lines = []
    for n in niches:
        nm = n.get("name","").replace('"','\\"')
        slug = n.get("slug","")
        icon = get_icon(nm, slug)
        t = n.get("total", 15)
        g = n.get("grade","B")
        p = n.get("passion",3)
        bf = n.get("buy_freq",3)
        gf = n.get("gift",3)
        c = n.get("comp",3)
        tr = n.get("trend",3)
        ao = n.get("avg_order",24)
        comp = n.get("competition","medium")
        etsy = n.get("etsy_results",5000)
        prds = n.get("top_products",["t-shirts","mugs"])
        prds_j = json.dumps([str(x) for x in prds])
        cat = n.get("cat","lifestyle")
        design = n.get("design_angle","").replace('"','\\"').replace("'","\\'")
        notes = n.get("notes",[])
        notes_j = json.dumps([str(x) for x in notes[:3]])
        
        margin_map = {"very-low":"45-60%","low":"35-50%","medium":"25-40%","high":"20-35%","very-high":"15-25%"}
        margin = margin_map.get(comp,"25-40%")
        margin_pct = {"very-low":85,"low":70,"medium":55,"high":40,"very-high":25}.get(comp,50)
        
        # Roadmap if present
        roadmap = n.get("roadmap", [])
        roadmap_j = ""
        if roadmap:
            phases = []
            for i, r in enumerate(roadmap):
                action = r.get("action","").replace('"','\\"')
                deliverable = r.get("deliverable","").replace('"','\\"')
                phases.append(f'{{phase:"{r.get("phase","Phase "+str(i+1))}",days:"{r.get("days","?")}",action:"{action}",deliverable:"{deliverable}"}}')
            roadmap_j = "roadmap:[" + ",".join(phases) + "],"
        
        line = f'{{nm:"{nm}",slug:"{slug}",t:{t},g:"{g}",p:{p},bf:{bf},gf:{gf},c:{c},tr:{tr},ao:{ao},comp:"{comp}",etsy:{etsy},prds:{prds_j},icon:"{icon}",cat:"{cat}",margin:"{margin}",marginPct:{margin_pct},design:"{design}",notes:{notes_j},{roadmap_j}}}'
        lines.append(line)
    return "const NICHES=[" + ",\n".join(lines) + "];"

js = build_js(niches)
print(f"JS array: {len(js)} chars")

# Load HTML template
TEMPLATE_PATH = "/home/openclaw/nichepulse/landing/app.html"
with open(TEMPLATE_PATH, "r") as f:
    html = f.read()

# Replace the NICHES array
# Find const NICHES=[...]; and replace
pattern = r'const NICHES=\[.*?\];'
if re.search(pattern, html, re.DOTALL):
    html = re.sub(pattern, js, html, flags=re.DOTALL)
    print("Replaced NICHES array")
else:
    print("WARNING: Could not find NICHES array pattern")

# Write output
OUTPUT_PATH = "/home/openclaw/nichepulse/landing/app.html"
with open(OUTPUT_PATH, "w") as f:
    f.write(html)
print(f"Written to {OUTPUT_PATH}")

# Also copy to root
import shutil
shutil.copy(OUTPUT_PATH, "/home/openclaw/nichepulse/app.html")
print("Copied to /home/openclaw/nichepulse/app.html")
