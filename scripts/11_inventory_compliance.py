#!/usr/bin/env python3
from common import *
log=setup("inventory_compliance");rows=[]
for d in api().dcim.devices.all():
 r=device_row(d);checks={"serial":bool(r["serial"]),"primary_ip":bool(r["primary_ip"]),"site":bool(r["site"]),"role":bool(r["role"]),"model":bool(r["model"])};score=round(100*sum(checks.values())/len(checks));r.update({f"check_{k}":"OK" if v else "KO" for k,v in checks.items()});r["score"]=score;r["compliance"]="OK" if score==100 else "WARNING" if score>=60 else "CRITICAL";rows.append(r)
log.info("%s",write_csv("inventory_compliance",rows))

