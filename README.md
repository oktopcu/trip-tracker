# Trip Tracker — The Grand Western Loop

A phone-first, offline-capable travel companion (PWA). Itinerary, checklists,
booking deadlines, GPS distance to your next stop, and one-tap navigation into
Apple Maps / Google Maps.

## Files

| File | What it is |
|---|---|
| `index.html` | **The app** (generated — don't edit directly) |
| `app.template.html` | App source: UI + logic, with a `__TRIP_JSON__` placeholder |
| `trip.json` | The itinerary data (see format below) |
| `build.py` | Injects `trip.json` into the template → writes `index.html` |
| `sw.js` | Service worker — makes the app work offline (dead zones!) |
| `manifest.webmanifest`, `icon-*.png` | PWA install metadata |
| `grand-western-loop-itinerary.html` | The original printable itinerary page (unchanged) |

After editing `trip.json` or `app.template.html`, run `python3 build.py`.

## Putting it on your iPhone

The app needs to be served over **HTTPS** (required for GPS + offline caching +
Add to Home Screen). Any static host works — there is no backend:

1. Host this folder somewhere: GitHub Pages, Cloudflare Pages, or Netlify
   (drag-and-drop the folder at https://app.netlify.com/drop).
2. Open the URL in **Safari** on the iPhone.
3. Tap **Share → Add to Home Screen**.

That's it: full-screen app, custom icon, works with no signal after the first
load. Progress (checkboxes) lives in the phone's local storage.

> Why not an `.ipa` + Sideloadly? Free-account sideloaded apps expire after
> **7 days** and must be re-signed from a computer — mid-trip that means a dead
> app in Yellowstone. The PWA never expires.

## The `trip-tracker/v1` format

The app renders any JSON with this shape — paste a new trip into
**Info → Trip data → Import** on the phone, or replace `trip.json` and rebuild.

```jsonc
{
  "format": "trip-tracker/v1",
  "meta": {
    "id": "unique-trip-id",          // progress is stored per id
    "name": "Trip name",
    "tagline": "optional subtitle",
    "start": "2026-07-05",           // ISO dates; the app auto-selects
    "end": "2026-07-29",             // "today" from the device clock
    "stats": [["24","nights"], ...]  // optional header stats
  },
  "todos": [                          // bookings & deadlines
    { "id": "t1", "title": "...", "due": "2026-07-03",
      "note": "...", "url": "https://..." }
  ],
  "legs": [
    { "name": "Leg 1 · ...", "dates": "Jul 5 – 8",
      "days": [
        { "n": 1, "date": "2026-07-05", "title": "A → B",
          "drive": "570 mi · ~8 h",   // chips (all optional)
          "wx": "Sunny, 34°C",
          "rest": "Easy day",
          "desc": "Free-text notes for the day.",
          "stops": [                   // ordered checklist; lat/lng power
            { "name": "Falls Park",    // GPS distance + navigation buttons
              "lat": 43.5586, "lng": -96.7226,
              "note": "optional", "optional": true }
          ],
          "stay": { "place": "Sioux Falls", "cost": "~$120",
                    "lat": 43.546, "lng": -96.731 },
          "routeUrl": "https://www.google.com/maps/dir/?api=1&..." // full-day route
        }
      ]
    }
  ],
  "budget": { "rows": [["Item","Detail","≈ $X"], ...],
              "total": ["Trip total","note","≈ $Y"] },
  "tips":   [ { "t": "Title", "d": "Body" } ]
}
```

Behavior notes:

- **Next stop** = the first unchecked, non-`optional` stop from today onward.
  "✓ Arrived" checks it and advances.
- Todos with a `due` on/before today surface as alerts on the Today tab and
  as the red badge on the To-Do tab.
- All progress is `localStorage`, keyed by `meta.id` — switching trips keeps
  each trip's progress separate. Export/Import lives in the Info tab.

## Local development

```sh
python3 build.py
python3 -m http.server 8734   # then open http://localhost:8734
```
