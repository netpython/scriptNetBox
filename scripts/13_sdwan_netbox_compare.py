#!/usr/bin/env python3
import argparse,csv
from common import *
log=setup("sdwan_compare");p=argparse.ArgumentParser();p.add_argument("--source",required=True);args=p.parse_args();nb=api();rows=[]
with open(args.source,encoding="utf-8-sig") as f:
 for x in csv.DictReader(f):
  serial=(x.get("serial") or x.get("uuid") or "").strip();matches=list(nb.dcim.devices.filter(serial=serial)) if serial else [];d=matches[0] if matches else None;rows.append({"sdwan_hostname":x.get("hostname") or x.get("device"),"serial":serial,"netbox_device":d.name if d else "","site":val(d,"site") if d else "","primary_ip":str(d.primary_ip or "") if d else "","result":"OK" if d else "ABSENT_NETBOX"})
log.info("%s",write_csv("sdwan_netbox_compare",rows))

