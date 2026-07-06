#!/usr/bin/env python3
"""Build index.html from app.template.html + trip.json.

Run after editing either file:  python3 build.py
"""
import json
import pathlib

root = pathlib.Path(__file__).parent
trip = json.loads((root / 'trip.json').read_text())
tpl = (root / 'app.template.html').read_text()
payload = json.dumps(trip, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
(root / 'index.html').write_text(tpl.replace('__TRIP_JSON__', payload))
print(f'index.html written — {len(trip["legs"])} legs, '
      f'{sum(len(l["days"]) for l in trip["legs"])} days, {len(payload)} bytes of trip data')
