#!/usr/bin/env python3
import sqlite3
from common import *
log=setup("cache_refresh");CACHE.mkdir(exist_ok=True);rows=[device_row(d) for d in api().dcim.devices.all()];write_json("../cache/netbox_devices",rows);db=sqlite3.connect(CACHE/"netbox.db");db.execute("DROP TABLE IF EXISTS devices");db.execute("CREATE TABLE devices (id INTEGER,name TEXT,site TEXT,role TEXT,manufacturer TEXT,model TEXT,serial TEXT,status TEXT,primary_ip TEXT,tenant TEXT)")
db.executemany("INSERT INTO devices VALUES (:id,:name,:site,:role,:manufacturer,:model,:serial,:status,:primary_ip,:tenant)",[{k:r.get(k,"") for k in ("id","name","site","role","manufacturer","model","serial","status","primary_ip","tenant")} for r in rows]);db.commit();db.close();log.info("Cache actualisé: %s équipements",len(rows))

