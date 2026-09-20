#!/usr/bin/env python3
from common import *
log=setup("ip_inventory");nb=api();rows=[]
for x in nb.ipam.ip_addresses.all():rows.append({"address":str(x.address),"status":val(x,"status"),"vrf":val(x,"vrf"),"tenant":val(x,"tenant"),"dns_name":x.dns_name,"assigned_type":str(x.assigned_object_type or ""),"assigned_object":str(x.assigned_object or "")})
log.info("%s",write_csv("ip_inventory",rows))

