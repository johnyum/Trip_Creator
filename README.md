# Trip Creator

An Airbnb-style mobile **trip-creator** prototype — a single self-contained HTML file with a live
MapLibre GL globe, a cinematic intro flight, zoom-tiered explore pins, a four-mode transport dock
(air / car / transit / walk), category "vibe" cards, NYC borough drill-down, a flight-booking flow
with arched dotted routes, and scattered Airbnb-style stay price pills.

## Files

| File | What it is |
|------|------------|
| `index.html` | Full-bleed iPhone build (same as `trip-creator-iphone.html`) — served by GitHub Pages |
| `trip-creator-iphone.html` | Full-bleed build for Add-to-Home-Screen / standalone PWA |
| `trip-creator-mobile.html` | Centered phone-card preview (nice on desktop) |
| `src/` | Build source: `build2.py` generates both HTML outputs from the embedded assets |

Both HTML files are **fully self-contained** — map screenshot base, photos, and logo are embedded as
base64, so they run from any static host with no build step.

## Run locally

Just open `trip-creator-mobile.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Rebuild from source

```bash
cd src
python3 build2.py        # writes the two HTML files
```

`src/build2.py` embeds `photos.json` (map + category imagery), `airdata.py` (explore destinations),
and `airbnb_logo.svg`. MapLibre GL is loaded from a CDN at runtime.

## Install on an iPhone

1. Host this repo (GitHub Pages, Netlify Drop, or Vercel).
2. Open the hosted URL in the **real Safari app** (not an in-app browser).
3. Tap **Share → scroll down → Add to Home Screen**.
4. Launch from the icon — it runs standalone, full-screen.

## Notes

This is a design prototype. Map tiles are real (CARTO), but flights, prices, and stay listings are
mock/procedural data — there's no real booking or live inventory behind them.
