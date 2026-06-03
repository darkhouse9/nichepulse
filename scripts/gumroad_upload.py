#!/usr/bin/env python3
"""Upload v2 ZIPs to Gumroad and update product descriptions"""
import http.client, json, os, urllib.request

TOKEN = "OXbK_kOTU5LINEzaYIsNM3_XxpY0esiFcZHiL-ACnFo"
TOKEN="O_ID = "kbmx7R-TdqIgjttIJYuqMw=="   # Pro Bundle
SKILL_ID = "B1MNe_LnBessczoXzAL0Hg=="  # Skill Pack
BASE = "/home/openclaw/nichepulse/dist"

def presign(filename, file_size):
    conn = http.client.HTTPSConnection("api.gumroad.com")
    conn.request("POST", "/v2/files/presign",
        body=json.dumps({"filename": filename, "file_size": file_size}).encode(),
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    return json.loads(conn.getresponse().read())

def upload_s3(url, filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    req = urllib.request.Request(url, data=data,
        headers={"Content-Type": "application/zip"}, method="PUT")
    return urllib.request.urlopen(req).status

def complete(upload_id, key):
    conn = http.client.HTTPSConnection("api.gumroad.com")
    conn.request("POST", "/v2/files/complete",
        body=json.dumps({"upload_id": upload_id, "key": key,
            "parts": [{"part_number": 1, "etag": ""}]}).encode(),
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    return json.loads(conn.getresponse().read())

def update_desc(product_id, desc):
    conn = http.client.HTTPSConnection("api.gumroad.com")
    conn.request("PUT", "/v2/products/" + product_id,
        body=json.dumps({"description": desc}).encode(),
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    return json.loads(conn.getresponse().read())

# Skill Pack v2
sp = BASE + "/nichepulse-skill-pack-v2.0.0.zip"
sz = os.path.getsize(sp)
print("Skill Pack v2:", sz, "bytes")
p = presign("nichepulse-skill-pack-v2.0.0.zip", sz)
print("Presign:", p["success"])
print("S3 upload:", upload_s3(p["parts"][0]["presigned_url"], sp))
print("Complete:", complete(p["upload_id"], p["key"]).get("success"))

# Pro Bundle v2
pp = BASE + "/nichepulse-pro-v2.0.0.zip"
sz2 = os.path.getsize(pp)
print("\nPro Bundle v2:", sz2, "bytes")
p2 = presign("nichepulse-pro-v2.0.0.zip", sz2)
print("Presign:", p2["success"])
print("S3 upload:", upload_s3(p2["parts"][0]["presigned_url"], pp))
print("Complete:", complete(p2["upload_id"], p2["key"]).get("success"))

# Update descriptions
sp_desc = "<h2>AI-Powered Niche Scoring for Creators &amp; Entrepreneurs</h2><p>Stop guessing. Start scoring.</p><h3>What You Get</h3><p><strong>1. Niche Research Skill</strong> — Score any niche on 5 dimensions. Includes 20+ niches across ALL major POD categories (pets, gaming, professions, fitness, mental health, hobbies, humor, seasonal, tech).</p><p><strong>2. SEO Audit Skill</strong> — Complete SEO analysis.</p><p><strong>3. Content Pipeline Skill</strong> — Multi-platform content.</p><p><strong>4. Interactive Niche Tool</strong> — Web-based niche selector with live scoring and design recommendations.</p><p><strong>Also included:</strong> CLI tool (pip install nichepulse), MCP server.</p><p><strong>Upgrade to Pro ($39)</strong> for 80+ niches, seasonal calendars, 90-day roadmaps.</p>"

pp_desc = "<h2>NichePulse Pro Bundle — v2.0</h2><p>Everything in the Skill Pack ($19) <strong>plus exclusive Pro-only content</strong>:</p><h3>Pro-Only Exclusives</h3><ul><li><strong>80+ Niche Database</strong> — 10 categories: pets, gaming, professions, fitness, mental health, faith, hobbies, seasonal, humor, tech (free version has 20)</li><li><strong>Seasonal Launch Calendar</strong> — Know exactly WHEN to launch each niche</li><li><strong>90-Day Launch Roadmaps</strong> — Day-by-day action plans for top niches</li><li><strong>Design Angle Guide</strong> — What visual style converts for each niche</li><li><strong>Sub-Niche Playbook</strong> — Go 3 levels deep for 10x less competition</li></ul><p><strong>30-day money-back guarantee. Lifetime updates.</strong></p>"

print("\nSkill Pack desc updated:", update_desc(SKILL_ID, sp_desc).get("success"))
print("Pro Bundle desc updated:", update_desc(PRO_ID, pp_desc).get("success"))
print("\nDONE!")
