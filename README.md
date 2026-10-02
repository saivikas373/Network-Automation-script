# Network Automation Scripts

Python and Ansible tools I use for day-to-day multi-vendor network operations: bulk show commands, BGP health checks, and config generation from templates.

Built on [Netmiko](https://github.com/ktbyers/netmiko), so they work across Cisco IOS/XE/XR/NX-OS, Juniper, Arista, A10, F5, and more.

## Tools

| Script | What it does | Real-world use |
|---|---|---|
| `show_to_csv.py` | Runs one show command on many devices **in parallel** and writes one CSV row per device | Pre/post-change snapshots, software version audits, `show bootimage` across a load-balancer fleet |
| `bgp_health.py` | Pulls `show ip bgp summary` (global or per-VRF), parses every neighbor, and flags any session that isn't Established | Fast BGP health check after a maintenance window |
| `render_config.py` | Renders configs from per-device YAML + a Jinja2 template | Building consistent VLAN and BGP configs for new devices |
| `ansible/generate_configs.yml` | The same rendering done with Ansible | Teams that standardize on Ansible |

## Quick start

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp inventory.example.yaml inventory.yaml    # add your devices
```

Credentials are **never stored in code or inventory**. Export them, or the script will prompt:

```bash
export NET_USER=admin
export NET_PASS='...'     # or leave unset to be prompted securely
```

## Examples

**Bulk show command → CSV**
```bash
python show_to_csv.py -i inventory.yaml -c "show version" -o versions.csv
python show_to_csv.py -i lb_ips.txt --device-type a10 -c "show bootimage" -w 20
```

**BGP health check**
```bash
python bgp_health.py -i inventory.yaml
python bgp_health.py -i inventory.yaml --vrf CUSTOMER_A -o bgp_report.csv
```
```
checked lab-core-01: 4 neighbors
DOWN    lab-core-01 -> 198.51.100.6 (AS 65003) state=Idle
DOWN    lab-core-01 -> 2001:DB8::2 (AS 65005) state=Active

2 neighbor(s) not Established. Full report: bgp_report.csv
```
The parser is tested against the sample output in [`examples/sample_bgp_summary.txt`](examples/sample_bgp_summary.txt) and handles both IPv4 and IPv6 neighbors.

**Config from template**
```bash
python render_config.py vars/R1.yaml vars/R2.yaml templates/bgp_vlan.j2 -o configs/
```
See the rendered result in [`examples/R1_config.txt`](examples/R1_config.txt).

## Design choices

- **Parallel by default.** Runs 10 devices at a time (`-w` to change), so a 200-device audit takes minutes, not an hour.
- **One bad device doesn't stop the run.** Failures are logged in the CSV, and the run continues.
- **StrictUndefined templates.** A missing variable fails the render instead of silently producing a broken config.
- **Vendor-neutral.** The inventory decides `device_type`; the scripts don't care.

All IPs and ASNs in this repo are documentation ranges (RFC 5737 / RFC 3849, private ASNs).

## About

**Saivikas Bedudhuri**, Network Engineer with 7 years in multi-vendor data-center networking, VXLAN/EVPN, BGP, and Python automation.
