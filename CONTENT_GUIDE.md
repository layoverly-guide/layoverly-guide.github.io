# Layoverly publishing rulebook

This file is the single source of truth for every automated publishing run. Follow it exactly.

## Files
- `guides.json`: registry of every published guide (city, slug, region, published date, last_checked date), the site `base_url`, and the `queue` of upcoming cities.
- `check_site.py`: pre-publish checker. **Every run must end with `python3 check_site.py` passing before you push.**
- `guides/athens.html`: the reference template for structure and style.
- `MAINTENANCE_LOG.md`: notes from the weekly maintenance run. Read the latest entry before publishing; it may flag something for this run.
- `404.html`: the site's "page not found" page. Leave it out of `sitemap.xml` and the guide cards.

## Which job to do this run (decide from today's date and guides.json)
"Guides" means the number of entries in `guides` in `guides.json`. If a run starts on a day other than Tuesday (a delayed or manual run), decide as if it were the most recent Tuesday, and still do only ONE job.

**Phase 1, the build-up (while fewer than 52 guides exist):** publish ONE new guide every run.

**Phase 2, the steady state (52+ guides):**
- On the **first and third Tuesday** of the month: publish ONE new guide.
- On **every other Tuesday**: REFRESH the guides with the oldest `last_checked` date, up to 3 per run, but only guides whose `last_checked` is more than 9 months old. If none are that old, publish a new guide instead.

## Publishing a new guide
1. Pick the first city in `queue` that is not already in `guides`.
   - If the queue has fewer than 5 cities left, first add 10 more. Choose popular short-break and stopover cities worldwide that aren't covered yet, favouring major airline hubs, and add them to the end of the queue.
2. Research it fresh on the web (current year): airport-to-city options with prices and times; the top sights with ticket prices and current opening hours; a realistic 24-hour route in walking order; a second-day plan; layover advice by hours available; typical daily costs; where to eat, including Muslim-friendly places.
3. Create `guides/<slug>.html` (lowercase, hyphens) by copying the structure of `guides/athens.html` exactly: same header, sections, table styles and footer. Title format: `<City> in 24–48 Hours: Itinerary, Airport Transfer & Costs (<year>) | Layoverly`. The meta description must be under 160 characters. The canonical URL is `<base_url>/guides/<slug>.html`. Put "Last checked <Month YYYY>" in the meta line. Keep the Open Graph tags, the JSON-LD block (Article + BreadcrumbList, with correct dates and URLs; `dateModified` = `last_checked`) and a "Quick answers" section of 4–6 real traveller questions with short, factual answers, exactly as in guides/athens.html.
   - Related guides: keep the `<!-- RELATED ... -->` comment and the `<p class="related">` line just above "Official sites". Link 1–3 other published guides: same `region` first (newest first), then the newest guides from other regions. Link text: `<City> in 24–48 hours`.
   - Then, for each guide in the same region that has fewer than 3 related links, add a link to the new guide to its related line (no other changes to that page, and don't change its `last_checked`).
   - Tables: at most 4 columns, so they fit on a phone.
4. Add the card at the top of the card list in `guides/index.html`, directly below the GUIDE-CARDS comment.
5. On `index.html` ("Latest guides"), add the new card as the **first** card. If there are now more than 6 cards, remove the **last** one. Never remove cards when there are 6 or fewer.
6. Add the URL to `sitemap.xml` with today's date.
7. Add the entry to `guides` in `guides.json` (published = last_checked = today) and remove the city from `queue`.
8. Run `python3 check_site.py`, fix anything it reports, and re-run it until it passes.
9. Commit "Add <City> guide" and push to main.

## Refreshing a guide
The year in a guide's title is the year it was last checked. Don't change titles just because a new calendar year starts; only a refresh updates it.

1. Re-research every price, opening time, transport detail and restaurant on the page. Fix anything that changed, and remove places that have closed.
2. Update "Last checked <Month YYYY>" on the page and the year in the title if it changed. Update the `lastmod` date in `sitemap.xml` and `last_checked` in `guides.json`.
3. Run `python3 check_site.py` until it passes. Commit "Refresh <City> guide" and push.

## Regions
`region` in `guides.json` must be exactly one of: Europe, Middle East, Asia, Africa, Americas, Oceania. Istanbul and the rest of Turkey count as Europe. Egypt and the Gulf states count as Middle East. Russia counts as Europe. Central Asia counts as Asia.

## When the site reaches 30 guides
Once, add region headings (Europe, Middle East, Asia, Africa, Americas, Oceania; only those that have guides) to `guides/index.html` and group the cards under them using `region` from `guides.json`. After that, insert each new card under its own region.

## When Phase 2 starts (52 guides)
In the same run, change the intro line on `guides/index.html` from "A new city is added every week." to "New cities are added every month."

## Changing the domain
If the owner moves the site to a custom domain, change `base_url` in `guides.json`, then replace the old base URL in every canonical tag, `sitemap.xml` and `robots.txt` in one commit, and run the checker.

## Never delete
- `google527523d80f86532c.html`: the Google Search Console verification file. Deleting it breaks the traffic reporting.
- `58d96af23e9044d0b00933f3d541510f.txt`: the IndexNow key file (tells Bing and other search engines about new pages). If the OpenSEO connector is available, call its submit_indexnow_urls tool (project "Layoverly") with every new or refreshed page URL after each push.

## Content rules
- Write in plain, original English. Never copy text from other sites.
- Every price and time must come from a current source. If sources disagree, give a range or say "check on the day". Never invent anything.
- Food labels must be honest: "Advertised halal", "Partly halal: ask", or "Not confirmed". Never call a place halal without a source.
- No personal information about the site owner anywhere, and no mention of any airline employer. The checker enforces this.
  - Exception: Doha's airport is a public place name, so write it exactly as "Hamad International Airport" (code DOH). The checker allows only that exact phrase; never shorten it to the first word alone.
- No affiliate links until the owner adds affiliate IDs to this file.
- Keep pages useful on a phone: short paragraphs and tables.
- Quality over volume: a thin or uncertain page is worse than no page. If you can't verify enough to make a useful guide for the chosen city, skip it (move it to the end of the queue) and do the next one.

## If something goes wrong
If the push is refused, the checker can't be made to pass, or the repository can't be attached, do not publish anything partial. Report the problem clearly so the owner is alerted.

## PDF editions (Gumroad shop "Layoverly")
- Athens PDF is live at https://layoverly.gumroad.com/l/athens ($7, pay-what-you-want, min $7).
- When a city has a live PDF, its guide page's "Want it offline?" box ends with:
  `<br><a class="cta" href="https://layoverly.gumroad.com/l/<slug>" rel="noopener">Get the PDF guide – $7</a>`
- Cities without a PDF keep "<i>PDF edition coming soon.</i>". Never link to a product that isn't published.

## Photos
- Use only Hamad's own photos (never copied web images). Store in /assets/img/<slug>/, max 900x1200, JPEG q78, ALL metadata stripped (no GPS/EXIF).
- No identifiable strangers' faces; no photos showing Hamad himself or his workplace.
- Pattern (see athens.html): hero <figure> after the intro, descriptive alt text, caption ending "Photo: Layoverly.", og:image + twitter "summary_large_image" pointing to the hero.
