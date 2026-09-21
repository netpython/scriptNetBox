#!/usr/bin/env python3
"""Détecte doublons de séries, noms, IP et positions de virtual chassis."""
from __future__ import annotations
import sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from common import *
log = setup('duplicates_conflicts')
nb = api()
findings = []
indexes = {k: defaultdict(list) for k in ('serial', 'name', 'primary_ip', 'vc_position')}
for d in nb.dcim.devices.all():
    r = device_row(d)
    for key in ('serial', 'name', 'primary_ip'):
        if r[key]:
            indexes[key][str(r[key]).strip().lower()].append(r)
    if r['vc'] and r['vc_position']:
        indexes['vc_position'][f"{r['vc']}:{r['vc_position']}"].append(r)
for field, index in indexes.items():
    for value, items in index.items():
        if len(items) > 1:
            for r in items:
                findings.append({'conflict_type': field, 'conflict_value': value, 'device': r['name'], 'site': r['site'], 'status': r['status'], 'severity': 'CRITICAL' if field in {'serial', 'primary_ip', 'vc_position'} else 'WARNING'})
log.info('%s', write_csv('duplicates_conflicts', findings))
