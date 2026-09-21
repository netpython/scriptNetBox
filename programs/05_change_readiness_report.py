#!/usr/bin/env python3
"""Mesure si les données NetBox sont suffisantes avant une migration réseau."""
from __future__ import annotations
import sys
from pathlib import Path
from openpyxl import Workbook
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from common import *
log=setup("change_readiness");args=parser("Préparation changement réseau").parse_args();nb=api();rows=[]
for d in nb.dcim.devices.filter(**filters(args)):
 r=device_row(d);ints=list(nb.dcim.interfaces.filter(device_id=d.id));cabled=sum(bool(i.connected_endpoints) for i in ints);described=sum(bool(i.description) for i in ints);checks={"management_ip":bool(r["primary_ip"]),"serial":bool(r["serial"]),"rack_location":bool(r["rack"] or r["location"]),"interfaces_documented":not ints or described/len(ints)>=.8,"cabling_present":cabled>0};score=round(100*sum(checks.values())/len(checks));rows.append({**r,"interfaces":len(ints),"cabled":cabled,"described":described,"score":score,"readiness":"READY" if score>=90 else "REVIEW" if score>=60 else "BLOCKED",**{f"check_{k}":"PASS" if v else "FAIL" for k,v in checks.items()}})
rows.sort(key=lambda x:(x["site"],x["rack"],x["location"],x["name"]));wb=Workbook();ws=wb.active;ws.title="Readiness";headers=list(rows[0]) if rows else ["result"];ws.append(headers)
for r in rows:ws.append([r.get(h,"") for h in headers])
ws.freeze_panes="A2";ws.auto_filter.ref=ws.dimensions;path=OUTPUT/f"change_readiness_{stamp()}.xlsx";wb.save(path);log.info("%s",path)

