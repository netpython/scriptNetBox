#!/usr/bin/env python3
from common import *
log=setup("device_inventory");args=parser("Inventaire équipements").parse_args();rows=[device_row(d) for d in api().dcim.devices.filter(**filters(args))];rows.sort(key=lambda x:(x["site"],x["rack"],x["location"],x["name"]));log.info("%s",write_csv("devices",rows))

