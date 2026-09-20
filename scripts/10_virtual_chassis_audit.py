#!/usr/bin/env python3
from common import *
log=setup("virtual_chassis");nb=api();rows=[]
for vc in nb.dcim.virtual_chassis.all():
 members=sorted(nb.dcim.devices.filter(virtual_chassis_id=vc.id),key=lambda d:d.vc_position or 0)
 for d in members:rows.append({"virtual_chassis":vc.name,"master":val(vc,"master"),**device_row(d),"result":"OK" if d.vc_position else "NO_POSITION"})
log.info("%s",write_csv("virtual_chassis",rows))

