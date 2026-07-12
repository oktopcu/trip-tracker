#!/usr/bin/env python3
"""Build index.html from app.template.html + trip.json (+ guides-*.json packs).

Guide packs map stop keys ("d<day>s<stopIndex>") to guide objects:
  { "d2s1": { "what": "...", "see": [...], "tips": [...], "fact": "..." } }
They are merged into the embedded trip data at build time, so the deployed
app (and any export from it) carries guides inline.

Run after editing any input:  python3 build.py
"""
import json
import pathlib
import sys

root = pathlib.Path(__file__).parent
trip = json.loads((root / 'trip.json').read_text())

stops_by_key = {}
for leg in trip['legs']:
    for day in leg['days']:
        for i, stop in enumerate(day.get('stops', [])):
            stops_by_key[f'd{day["n"]}s{i}'] = stop

guide_count = 0
for pack in sorted(root.glob('guides-*.json')):
    for key, guide in json.loads(pack.read_text()).items():
        if key not in stops_by_key:
            sys.exit(f'{pack.name}: unknown stop key {key!r}')
        stops_by_key[key]['guide'] = guide
        guide_count += 1

map_count = 0
for pack in sorted(root.glob('maps-*.json')):
    for key, m in json.loads(pack.read_text()).items():
        if key not in stops_by_key:
            sys.exit(f'{pack.name}: unknown stop key {key!r}')
        if '"' in m.get('svg', ''):
            sys.exit(f'{pack.name}: {key} svg must use single-quoted attributes')
        stops_by_key[key].setdefault('guide', {})['map'] = m
        map_count += 1

tpl = (root / 'app.template.html').read_text()
payload = json.dumps(trip, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
(root / 'index.html').write_text(tpl.replace('__TRIP_JSON__', payload))
print(f'index.html written — {sum(len(l["days"]) for l in trip["legs"])} days, '
      f'{len(stops_by_key)} stops, {guide_count} guides, {map_count} maps, '
      f'{len(payload)} bytes of trip data')
