#!/usr/bin/env python3
import argparse,csv
from common import *
log=setup("meraki_compare");p=argparse.ArgumentParser();p.add_argument("--source",required=True);args=p.parse_args();nb=api();rows=[]
with open(args.source,encoding="utf-8-sig") as f:
 for m in csv.DictReader(f):
  serial=(m.get("serial") or "").strip();matches=list(nb.dcim.devices.filter(serial=serial)) if serial else [];d=matches[0] if matches else None;rows.append({"meraki_device":m.get("device") or m.get("name"),"serial":serial,"netbox_device":d.name if d else "","site":val(d,"site") if d else "","model":val(d,"device_type") if d else "","result":"OK" if d else "ABSENT_NETBOX"})
log.info("%s",write_csv("meraki_netbox_compare",rows))

