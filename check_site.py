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
    for bad in ["Gulf Air", "gulfair", "hamad", "523614"]:
        if bad.lower() in html.lower(): errors.append(f"{rel}: contains forbidden personal/employer text '{bad}'")
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
print("\n".join(errors) if errors else "OK: all checks passed"); sys.exit(1 if errors else 0)
