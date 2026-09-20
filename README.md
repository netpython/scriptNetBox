# scriptNetBox

15 scripts Python pour exploiter NetBox comme inventaire réseau central.

| # | Script | Fonction |
|---|---|---|
| 01 | `01_device_inventory.py` | Inventaire complet des équipements |
| 02 | `02_interface_inventory.py` | Interfaces, descriptions et câblage |
| 03 | `03_ip_inventory.py` | Adresses IP, VRF et affectations |
| 04 | `04_site_summary.py` | Synthèse par site |
| 05 | `05_rack_inventory.py` | Équipements triés par rack/location |
| 06 | `06_serial_audit.py` | Séries absents ou dupliqués |
| 07 | `07_primary_ip_audit.py` | Équipements sans IP primaire |
| 08 | `08_cabling_audit.py` | Interfaces connectées/non connectées |
| 09 | `09_vlan_prefix_audit.py` | VLAN, préfixes et sites associés |
| 10 | `10_virtual_chassis_audit.py` | Stacks, membres et positions VC |
| 11 | `11_inventory_compliance.py` | Score de conformité NetBox |
| 12 | `12_meraki_netbox_compare.py` | Comparaison CSV Meraki ↔ NetBox |
| 13 | `13_sdwan_netbox_compare.py` | Comparaison CSV SD-WAN ↔ NetBox |
| 14 | `14_cache_refresh.py` | Cache JSON/SQLite pour supervision |
| 15 | `15_export_xlsx.py` | Export Excel coloré multi-onglets |

## Installation

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config.example.yml config.yml
export NETBOX_URL='https://netbox.example.com'
export NETBOX_TOKEN='votre-token'
```

## Exemples

```bash
python scripts/01_device_inventory.py --site 19
python scripts/06_serial_audit.py
python scripts/12_meraki_netbox_compare.py --source meraki_inventory.csv
python scripts/15_export_xlsx.py
```

Les identifiants sont lus depuis l'environnement. Les outils sont en lecture seule et exportent dans `outputs/`.

## Licence

MIT.

