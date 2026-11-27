"""Pre-push checks for the Layoverly site. Run: python3 check_site.py  (exit code 0 = OK)."""
import json, os, re, sys
from html.parser import HTMLParser
root = os.path.dirname(os.path.abspath(__file__)); errors = []
data = json.load(open(os.path.join(root, "guides.json")))
base = data["base_url"].rstrip("/")
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]; s.title=""; s._t=False; s.desc=None
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=="a" and a.get("href"): s.links.append(a["href"])
        if t=="title": s._t=True
        if t=="meta" and a.get("name")=="description": s.desc=a.get("content","")
    def handle_endtag(s,t):
        if t=="title": s._t=False
    def handle_data(s,d):
        if s._t: s.title+=d
# Public place names that contain a forbidden word. Allowed ONLY as these exact phrases.
ALLOWED_PHRASES = ["hamad international airport", "hamad international"]
pages = []
for dp, dirs, fs in os.walk(root):
    dirs[:] = [d for d in dirs if d != ".git"]
    pages += [os.path.join(dp, f) for f in fs if f.endswith(".html") and not f.startswith("google")]  # skip Search Console verification file
for p in pages:
    rel = os.path.relpath(p, root); html = open(p, encoding="utf-8").read(); h = P(); h.feed(html)
    if not h.title.strip(): errors.append(f"{rel}: missing <title>")
    if h.desc is None: errors.append(f"{rel}: missing meta description")
    elif len(h.desc) > 170: errors.append(f"{rel}: meta description too long ({len(h.desc)})")
    for l in h.links:
        if l.startswith("/") and not l.startswith("//"):
            target = l.split("#")[0].split("?")[0]
            path = os.path.join(root, target.lstrip("/"))
            if target.endswith("/"): path = os.path.join(path, "index.html")
            if not os.path.exists(path): errors.append(f"{rel}: broken internal link {l}")
    low = html.lower()
    for ok in ALLOWED_PHRASES: low = low.replace(ok, "")  # public place names, e.g. Doha's airport
    for bad in ["Gulf Air", "gulfair", "hamad", "523614"]:
        if bad.lower() in low: errors.append(f"{rel}: contains forbidden personal/employer text '{bad}'")
sitemap = open(os.path.join(root, "sitemap.xml")).read()
index = open(os.path.join(root, "guides", "index.html")).read()
seen = set()
for g in data["guides"]:
    s = g["slug"]
    if s in seen: errors.append(f"duplicate guide slug {s}")
    seen.add(s)
    if not os.path.exists(os.path.join(root, "guides", s + ".html")): errors.append(f"guides.json lists {s} but guides/{s}.html is missing")
    if f"/guides/{s}.html" not in index: errors.append(f"guides/index.html has no card for {s}")
    if f"{base}/guides/{s}.html" not in sitemap: errors.append(f"sitemap.xml missing {s}")
for f in os.listdir(os.path.join(root, "guides")):
    if f.endswith(".html") and f != "index.html" and f[:-5] not in seen: errors.append(f"guides/{f} exists but is not in guides.json")
if len(re.findall(r'class="card"', open(os.path.join(root, "index.html")).read())) > 6: errors.append("homepage shows more than 6 guide cards")
# --- Guide page structure (keeps every automated run consistent with guides/athens.html) ---
import datetime
notes = []
today = datetime.date.today()
slugs = [g["slug"] for g in data["guides"]]
for g in data["guides"]:
    s, f = g["slug"], os.path.join(root, "guides", g["slug"] + ".html")
    if not os.path.exists(f): continue
    html = open(f, encoding="utf-8").read(); h = P(); h.feed(html)
    try:
        pub = datetime.date.fromisoformat(g["published"]); chk = datetime.date.fromisoformat(g["last_checked"])
        if chk < pub: errors.append(f"guides.json {s}: last_checked is before published")
        if (today - chk).days > 270: notes.append(f"NOTE: {s} last checked {chk}, over 9 months ago (due for refresh)")
    except Exception: errors.append(f"guides.json {s}: published/last_checked must be YYYY-MM-DD")
    if not re.match(r"^.+ in 24–48 Hours: Itinerary, Airport Transfer & Costs \(\d{4}\) \| Layoverly$", h.title.strip()):
        errors.append(f"guides/{s}.html: title doesn't follow the rulebook format")
    if h.desc is not None and len(h.desc) >= 160: errors.append(f"guides/{s}.html: meta description must be under 160 characters ({len(h.desc)})")
    if f'<link rel="canonical" href="{base}/guides/{s}.html">' not in html: errors.append(f"guides/{s}.html: missing or wrong canonical URL")
    if "Last checked" not in html: errors.append(f"guides/{s}.html: missing 'Last checked <Month YYYY>' line")
    if "<h2>Quick answers</h2>" not in html: errors.append(f"guides/{s}.html: missing Quick answers section")
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    if not m: errors.append(f"guides/{s}.html: missing JSON-LD block")
    else:
        try:
            ld = json.loads(m.group(1)); art = [x for x in ld.get("@graph", []) if x.get("@type") == "Article"]
            if not art: errors.append(f"guides/{s}.html: JSON-LD has no Article")
            elif art[0].get("dateModified") != g["last_checked"]: errors.append(f"guides/{s}.html: JSON-LD dateModified should equal last_checked {g['last_checked']}")
        except ValueError: errors.append(f"guides/{s}.html: JSON-LD is not valid JSON")
    rm = re.search(r'<p class="related">(.*?)</p>', html, re.S)
    if len(slugs) > 1:
        if not rm: errors.append(f"guides/{s}.html: missing 'More short-stay guides' related block")
        else:
            rel_links = re.findall(r'href="/guides/([a-z0-9-]+)\.html"', rm.group(1))
            if not rel_links: errors.append(f"guides/{s}.html: related block has no guide links")
            if s in rel_links: errors.append(f"guides/{s}.html: related block links to itself")
            if len(rel_links) > 3: errors.append(f"guides/{s}.html: related block has more than 3 links")
locs = re.findall(r"<loc>(.*?)</loc>", sitemap)
if len(locs) != len(set(locs)): errors.append("sitemap.xml has duplicate URLs")
if len(data["queue"]) < 5: notes.append(f"NOTE: only {len(data['queue'])} cities left in the queue (next publishing run must add 10)")
for c in data["queue"]:
    if c.lower() in [g["city"].lower() for g in data["guides"]]: notes.append(f"NOTE: {c} is in the queue but already published")
if notes: print("\n".join(notes))
print("\n".join(errors) if errors else "OK: all checks passed"); sys.exit(1 if errors else 0)
