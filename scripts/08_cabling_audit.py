#!/usr/bin/env python3
from common import *
log=setup("cabling_audit");args=parser("Audit câblage").parse_args();nb=api();rows=[]
for d in nb.dcim.devices.filter(**filters(args)):
 for i in nb.dcim.interfaces.filter(device_id=d.id):rows.append({"site":val(d,"site"),"device":d.name,"interface":i.name,"description":i.description,"enabled":i.enabled,"connected":bool(i.connected_endpoints),"cable_id":getattr(i.cable,"id","") if i.cable else "","result":"OK" if (not i.enabled or i.connected_endpoints) else "ENABLED_UNCABLED"})
log.info("%s",write_csv("cabling_audit",rows))

