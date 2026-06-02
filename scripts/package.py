#!/usr/bin/env python3
"""Build NichePulse ZIP packages for v2.0"""
import zipfile, os, shutil

base = "/home/openclaw/nichepulse"
dist = f"{base}/dist"

for d in ["nichepulse-skill-pack", "nichepulse-pro"]:
    p = f"{dist}/{d}"
    if os.path.exists(p): shutil.rmtree(p)

def ensure_dirs(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)

def cp(src, dst):
    ensure_dirs(os.path.dirname(dst))
    shutil.copy2(src, dst)

def cptree(src, dst):
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(src, dst)

# === SKILL PACK ===
sp = f"{dist}/nichepulse-skill-pack/nichepulse"
cptree(f"{base}/skills", f"{sp}/skills")
cptree(f"{base}/src", f"{sp}/src")
cptree(f"{base}/mcp-server", f"{sp}/mcp-server")
ensure_dirs(f"{sp}/landing")
cp(f"{base}/landing/index.html", f"{sp}/landing/index.html")
cp(f"{base}/landing/tool.html", f"{sp}/landing/tool.html")
cp(f"{base}/README.md", f"{sp}/README.md")
cp(f"{base}/CLAUDE.md", f"{sp}/CLAUDE.md")
cp(f"{base}/pyproject.toml", f"{sp}/pyproject.toml")

with zipfile.ZipFile(f"{dist}/nichepulse-skill-pack-v2.0.0.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(f"{dist}/nichepulse-skill-pack"):
        dirs[:] = [d for d in dirs if d not in ("__pycache__",".venv")]
        for f in files:
            path = os.path.join(root, f)
            zf.write(path, os.path.relpath(path, dist))

sp_size = os.path.getsize(f"{dist}/nichepulse-skill-pack-v2.0.0.zip")
print(f"Skill Pack: {sp_size} bytes ({sp_size//1024}KB)")

# === PRO BUNDLE ===
pp_free = f"{dist}/nichepulse-pro/nichepulse"
shutil.copytree(f"{dist}/nichepulse-skill-pack/nichepulse", pp_free)

pp_pro = f"{dist}/nichepulse-pro/nichepulse-pro"
cp(f"{base}/skills/niche-research-pro/SKILL.md", f"{pp_pro}/niche-research/SKILL.md")
ensure_dirs(f"{pp_pro}/data")
cp(f"{base}/skills/niche-research-pro/data/niche-database.json", f"{pp_pro}/data/niche-database.json")
cp(f"{base}/skills/niche-research-pro/data/seasonal-calendar.json", f"{pp_pro}/data/seasonal-calendar.json")
ensure_dirs(f"{pp_pro}/roadmaps")
cp(f"{base}/skills/niche-research-pro/roadmaps/mushroom-foraging.md", f"{pp_pro}/roadmaps/mushroom-foraging.md")

with open(f"{pp_pro}/PRO-README.md", "w") as f:
    f.write("# NichePulse Pro — Exclusive\n\n80+ niche DB, seasonal calendars, 90-day roadmaps, design strategies.\n")

with zipfile.ZipFile(f"{dist}/nichepulse-pro-v2.0.0.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(f"{dist}/nichepulse-pro"):
        dirs[:] = [d for d in dirs if d not in ("__pycache__",".venv")]
        for f in files:
            path = os.path.join(root, f)
            zf.write(path, os.path.relpath(path, dist))

pp_size = os.path.getsize(f"{dist}/nichepulse-pro-v2.0.0.zip")
print(f"Pro Bundle: {pp_size} bytes ({pp_size//1024}KB)")
print("Done!")
