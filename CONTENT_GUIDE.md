# Layoverly publishing rulebook

This file is the single source of truth for every automated publishing run. Follow it exactly.

## Files
- `guides.json`: registry of every published guide (city, slug, region, published date, last_checked date), the site `base_url`, and the `queue` of upcoming cities.
- `check_site.py`: pre-publish checker. **Every run must end with `python3 check_site.py` passing before you push.**
- `guides/athens.html`: the reference template for structure and style.

## Which job to do this run (decide from today's date and guides.json)
**Phase 1, the build-up (while fewer than 52 guides exist):** publish ONE new guide every run.

**Phase 2, the steady state (52+ guides):**
- On the **first and third Tuesday** of the month: publish ONE new guide.
- On **every other Tuesday**: REFRESH the guides with the oldest `last_checked` date, up to 3 per run, but only guides whose `last_checked` is more than 9 months old. If none are that old, publish a new guide instead.

## Publishing a new guide
1. Pick the first city in `queue` that is not already in `guides`.
   - If the queue has fewer than 5 cities left, first add 10 more. Choose popular short-break and stopover cities worldwide that aren't covered yet, favouring major airline hubs, and add them to the end of the queue.
2. Research it fresh on the web (current year): airport-to-city options with prices and times; the top sights with ticket prices and current opening hours; a realistic 24-hour route in walking order; a second-day plan; layover advice by hours available; typical daily costs; where to eat, including Muslim-friendly places.
3. Create `guides/<slug>.html` (lowercase, hyphens) by copying the structure of `guides/athens.html` exactly: same header, sections, table styles and footer. Title format: `<City> in 24–48 Hours: Itinerary, Airport Transfer & Costs (<year>) | Layoverly`. The meta description must be under 160 characters. The canonical URL is `<base_url>/guides/<slug>.html`. Put "Last checked <Month YYYY>" in the meta line.
4. Add the card at the top of the card list in `guides/index.html`, directly below the GUIDE-CARDS comment.
5. On `index.html` ("Latest guides"), add the new card as the **first** card. If there are now more than 6 cards, remove the **last** one. Never remove cards when there are 6 or fewer.
6. Add the URL to `sitemap.xml` with today's date.
7. Add the entry to `guides` in `guides.json` (published = last_checked = today) and remove the city from `queue`.
8. Run `python3 check_site.py`, fix anything it reports, and re-run it until it passes.
9. Commit "Add <City> guide" and push to main.

## Refreshing a guide
1. Re-research every price, opening time, transport detail and restaurant on the page. Fix anything that changed, and remove places that have closed.
2. Update "Last checked <Month YYYY>" on the page and the year in the title if it changed. Update the `lastmod` date in `sitemap.xml` and `last_checked` in `guides.json`.
3. Run `python3 check_site.py` until it passes. Commit "Refresh <City> guide" and push.

## When the site reaches 30 guides
Once, add region headings (Europe, Middle East, Asia, Africa, Americas) to `guides/index.html` and group the cards under them using `region` from `guides.json`. After that, insert each new card under its own region.

## Changing the domain
If the owner moves the site to a custom domain, change `base_url` in `guides.json`, then replace the old base URL in every canonical tag, `sitemap.xml` and `robots.txt` in one commit, and run the checker.

## Content rules
- Write in plain, original English. Never copy text from other sites.
- Every price and time must come from a current source. If sources disagree, give a range or say "check on the day". Never invent anything.
- Food labels must be honest: "Advertised halal", "Partly halal: ask", or "Not confirmed". Never call a place halal without a source.
- No personal information about the site owner anywhere, and no mention of any airline employer. The checker enforces this.
- No affiliate links until the owner adds affiliate IDs to this file.
- Keep pages useful on a phone: short paragraphs and tables.
- Quality over volume: a thin or uncertain page is worse than no page. If you can't verify enough to make a useful guide for the chosen city, skip it (move it to the end of the queue) and do the next one.

## If something goes wrong
If the push is refused, the checker can't be made to pass, or the repository can't be attached, do not publish anything partial. Report the problem clearly so the owner is alerted.
