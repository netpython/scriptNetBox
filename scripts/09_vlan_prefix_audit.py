#!/usr/bin/env python3
from common import *
log=setup("vlan_prefix_audit");nb=api();rows=[]
for v in nb.ipam.vlans.all():rows.append({"type":"VLAN","id":v.vid,"name":v.name,"site":val(v,"site"),"tenant":val(v,"tenant"),"status":val(v,"status")})
for p in nb.ipam.prefixes.all():rows.append({"type":"PREFIX","id":str(p.prefix),"name":p.description,"site":val(p,"site"),"tenant":val(p,"tenant"),"status":val(p,"status"),"vlan":val(p,"vlan")})
log.info("%s",write_csv("vlan_prefix_audit",rows))

