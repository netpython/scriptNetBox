#!/usr/bin/env python3
from collections import Counter
from common import *
log=setup("site_summary");nb=api();rows=[]
for s in nb.dcim.sites.all():
 ds=list(nb.dcim.devices.filter(site_id=s.id));c=Counter(val(d,"status") for d in ds);rows.append({"site":s.name,"slug":s.slug,"devices":len(ds),**{f"status_{k}":v for k,v in c.items()}})
log.info("%s",write_csv("site_summary",rows))

