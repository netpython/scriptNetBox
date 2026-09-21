#!/usr/bin/env python3
"""Compare un export externe Meraki/SD-WAN/SSH avec NetBox, champ par champ."""
from __future__ import annotations
import argparse, csv, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from common import *
p = argparse.ArgumentParser(description='Comparaison source de vérité')
p.add_argument('--source', required=True)
p.add_argument('--source-name', default='external')
p.add_argument('--serial-column', default='serial')
p.add_argument('--hostname-column', default='hostname')
args = p.parse_args()
nb = api()
rows = []
with open(args.source, encoding='utf-8-sig', newline='') as f:
    for ext in csv.DictReader(f):
        serial = (ext.get(args.serial_column) or '').strip()
        hostname = (ext.get(args.hostname_column) or ext.get('device') or ext.get('name') or '').strip()
        matches = list(nb.dcim.devices.filter(serial=serial)) if serial else list(nb.dcim.devices.filter(name=hostname)) if hostname else []
        d = matches[0] if matches else None
        issues = []
        if not d:
            issues.append('ABSENT_NETBOX')
        else:
            if serial and d.serial.strip().lower() != serial.lower():
                issues.append('SERIAL_MISMATCH')
            if hostname and d.name.lower() != hostname.lower():
                issues.append('HOSTNAME_MISMATCH')
            if ext.get('model') and val(d, 'device_type').lower() != ext['model'].lower():
                issues.append('MODEL_MISMATCH')
            if ext.get('ip') and str(d.primary_ip or '').split('/')[0] != ext['ip'].split('/')[0]:
                issues.append('IP_MISMATCH')
        rows.append({'source': args.source_name, 'external_hostname': hostname, 'external_serial': serial, 'netbox_device': d.name if d else '', 'site': val(d, 'site') if d else '', 'role': val(d, 'role') if d else '', 'status': val(d, 'status') if d else '', 'result': 'OK' if not issues else 'CRITICAL' if 'ABSENT_NETBOX' in issues else 'WARNING', 'issues': ','.join(issues)})
log = setup('source_compare')
log.info('%s', write_csv('source_of_truth_compare', rows))
