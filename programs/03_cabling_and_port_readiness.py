#!/usr/bin/env python3
"""Évalue la documentation et la disponibilité des ports par site/rack/location."""
from __future__ import annotations
import sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from common import *
log=setup("cabling_readiness");args=parser("Câblage et capacité NetBox").parse_args();nb=api();ports=[];summary=[]
for d in nb.dcim.devices.filter(**filters(args)):
 dr=device_row(d);counts=defaultdict(int)
 for i in nb.dcim.interfaces.filter(device_id=d.id):
  connected=bool(i.connected_endpoints);enabled=bool(i.enabled);documented=bool(i.description);finding="OK"
  if enabled and not connected:finding="AVAILABLE";counts["available"]+=1
  if connected and not documented:finding="CONNECTED_NO_DESCRIPTION";counts["undocumented"]+=1
  if not enabled:counts["disabled"]+=1
  if connected:counts["connected"]+=1
  ports.append({"site":dr["site"],"rack":dr["rack"],"location":dr["location"],"device":d.name,"interface":i.name,"type":val(i,"type"),"enabled":enabled,"connected":connected,"description":i.description,"cable_id":getattr(i.cable,"id","") if i.cable else "","finding":finding})
 total=len(list(nb.dcim.interfaces.filter(device_id=d.id)));summary.append({"site":dr["site"],"rack":dr["rack"],"location":dr["location"],"device":d.name,"total":total,**counts,"readiness":"WARNING" if counts["undocumented"] else "OK"})
log.info("Ports: %s",write_csv("cabling_ports",ports));log.info("Summary: %s",write_csv("cabling_readiness",summary))

