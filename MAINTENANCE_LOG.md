# Layoverly maintenance log

Notes from the weekly maintenance run, newest first. Publishing runs: read the latest entry before you start.

## 2026-11-27

**Checked**
- `check_site.py`: passed at start.
- Tuesday publishing run: done ("Add Istanbul guide", 2026-11-24).
- GitHub Pages build status: not available from the maintenance environment (API path blocked), skipped.
- Guide review (Athens, Istanbul): structure matches the template, no empty sections, no personal or employer text. Prices are all from November 2026. Istanbul has no photos yet, which is expected because it has no owner photos.
- Mobile: Istanbul overflowed sideways on a 360 px phone (the airport table with long words like "Gayrettepe").

**Fixed**
- `assets/style.css`: table cells now wrap long words, with slightly tighter tables on phones. All pages now fit at 360 px.
- `check_site.py`: the forbidden-word check would have failed the Doha guide (queue position 7, due around mid-January) because "Hamad International Airport" contains a blocked word. That exact public place name is now allowed. The rulebook says to write it in full.

**Improved**
- Internal links: Athens and Istanbul now link to each other in a "More short-stay guides" line. The rulebook says how future guides fill this line.
- Added a custom `404.html` (noindex) that links back to the guides.
- Added a canonical tag to `about.html`.
- `check_site.py` now also checks each guide's title format, meta description length (under 160), canonical URL, "Last checked" line, Quick answers, JSON-LD validity and `dateModified`, related links and duplicate sitemap URLs. It prints NOTE lines (without failing) when a guide is over 9 months old or the queue is low.
- `CONTENT_GUIDE.md`: made clearer which job to do on a delayed or non-Tuesday run, gave a fixed list of regions (including Oceania, with Turkey, Egypt and the Gulf states placed), explained when the year in a guide's title changes, added the Phase 2 change to the guides page intro line, capped tables at 4 columns, and listed this log and the 404 page.

**Watch next week**
- The queue has 19 cities, which is plenty for now. No guide is close to the 9-month refresh (the first is due around August 2027).
- A leftover remote branch `tmp-upload` still exists. It does no harm and can be deleted from GitHub when convenient.
- The homepage has 2 of the 6 card slots in use, so the card trimming won't start until the 7th guide.
