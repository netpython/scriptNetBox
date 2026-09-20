#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,logging,os,sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any
import pynetbox,yaml

ROOT=Path(__file__).resolve().parents[1]; OUTPUT=ROOT/"outputs"; LOGS=ROOT/"logs"; CACHE=ROOT/"cache"
def setup(name:str):
    OUTPUT.mkdir(exist_ok=True); LOGS.mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s",handlers=[logging.FileHandler(LOGS/f"{name}.log"),logging.StreamHandler()]); return logging.getLogger(name)
def api():
    url=os.getenv("NETBOX_URL"); token=os.getenv("NETBOX_TOKEN")
    if not url or not token: raise SystemExit("Définir NETBOX_URL et NETBOX_TOKEN.")
    nb=pynetbox.api(url,token=token); nb.http_session.verify=os.getenv("NETBOX_VERIFY_SSL","true").lower()=="true"; return nb
def parser(text:str):
    p=argparse.ArgumentParser(description=text); p.add_argument("--site"); p.add_argument("--role"); p.add_argument("--manufacturer"); p.add_argument("--status"); return p
def filters(args): return {k:v for k,v in vars(args).items() if k in {"site","role","manufacturer","status"} and v}
def val(obj:Any,attr:str,default=""):
    x=getattr(obj,attr,None)
    if x is None:return default
    return getattr(x,"name",getattr(x,"display",str(x)))
def device_row(d):
    return {"id":d.id,"name":d.name,"site":val(d,"site"),"location":val(d,"location"),"rack":val(d,"rack"),"role":val(d,"role"),"manufacturer":val(getattr(d,"device_type",None),"manufacturer"),"model":val(d,"device_type"),"serial":d.serial or "","status":val(d,"status"),"primary_ip":str(d.primary_ip or ""),"tenant":val(d,"tenant"),"vc":val(d,"virtual_chassis"),"vc_position":d.vc_position or "","tags":",".join(str(t) for t in d.tags)}
def stamp():return datetime.now().strftime("%Y%m%d_%H%M%S")
def write_csv(name,rows):
    path=OUTPUT/f"{name}_{stamp()}.csv"; fields=sorted({k for r in rows for k in r}) or ["result"]
    with path.open("w",newline="",encoding="utf-8-sig") as f:w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(rows)
    return path
def write_json(name,data):
    path=OUTPUT/f"{name}_{stamp()}.json";path.write_text(json.dumps(data,ensure_ascii=False,indent=2,default=str),encoding="utf-8");return path

