#!/usr/bin/env python3
from common import *
log=setup("primary_ip_audit");args=parser("Audit IP primaire").parse_args();rows=[]
for d in api().dcim.devices.filter(**filters(args)):
 r=device_row(d);r["result"]="OK" if r["primary_ip"] else "NO_PRIMARY_IP";rows.append(r)
log.info("%s",write_csv("primary_ip_audit",rows))

