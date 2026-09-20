#!/usr/bin/env python3
from collections import Counter
from common import *
log=setup("serial_audit");devices=[device_row(d) for d in api().dcim.devices.all()];counts=Counter(x["serial"].strip().upper() for x in devices if x["serial"].strip());rows=[]
for x in devices:
 key=x["serial"].strip().upper();x["result"]="EMPTY" if not key else "DUPLICATE" if counts[key]>1 else "OK";rows.append(x)
log.info("%s",write_csv("serial_audit",rows))

