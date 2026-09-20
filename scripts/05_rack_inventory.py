#!/usr/bin/env python3
from common import *
log=setup("rack_inventory");args=parser("Inventaire racks").parse_args();rows=[device_row(d) for d in api().dcim.devices.filter(**filters(args))];rows.sort(key=lambda x:(x["site"],x["rack"] or "ZZZ",x["location"],x["name"]));log.info("%s",write_csv("rack_inventory",rows))

