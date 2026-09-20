#!/usr/bin/env python3
from common import *
log=setup("interfaces");args=parser("Inventaire interfaces").parse_args();nb=api();devs=list(nb.dcim.devices.filter(**filters(args)));rows=[]
for d in devs:
 for i in nb.dcim.interfaces.filter(device_id=d.id): rows.append({**device_row(d),"interface":i.name,"description":i.description,"type":val(i,"type"),"enabled":i.enabled,"mtu":i.mtu or "","connected":bool(i.connected_endpoints),"cable":getattr(i.cable,"id","") if i.cable else ""})
log.info("%s",write_csv("interfaces",rows))

