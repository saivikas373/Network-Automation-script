#!/usr/bin/env python3
"""Check BGP neighbor state across devices and flag anything not Established.

Parses Cisco IOS / IOS-XE / NX-OS 'show ip bgp summary' style output.
In that table the last column is either a prefix count (session is up)
or a state word such as Idle / Active / Connect (session is down).

Example:
    python bgp_health.py -i inventory.yaml
    python bgp_health.py -i inventory.yaml --vrf CUSTOMER_A -o bgp_report.csv
"""
import argparse
import csv
import re

from netmiko import ConnectHandler

from common import get_credentials, load_inventory, netmiko_params

NEIGHBOR_LINE = re.compile(
    r"^(?P<neighbor>[0-9a-fA-F.:]+)\s+\d+\s+(?P<asn>[\d.]+)\s+.*\s"
    r"(?P<updown>\S+)\s+(?P<state>\S+)\s*$")


def parse_summary(text):
    rows = []
    for line in text.splitlines():
        m = NEIGHBOR_LINE.match(line.strip())
        if not m:
            continue
        state = m["state"]
        up = state.isdigit()
        rows.append({
            "neighbor": m["neighbor"],
            "remote_as": m["asn"],
            "up_down": m["updown"],
            "state": "Established" if up else state,
            "prefixes": state if up else "0",
            "healthy": up,
        })
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-i", "--inventory", required=True)
    ap.add_argument("--vrf", help="check a VRF instead of the global table")
    ap.add_argument("-o", "--output", default="bgp_report.csv")
    ap.add_argument("--device-type")
    args = ap.parse_args()

    command = (f"show ip bgp vpnv4 vrf {args.vrf} summary" if args.vrf
               else "show ip bgp summary")
    devices = load_inventory(args.inventory, args.device_type)
    user, password = get_credentials()

    down = 0
    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["device", "neighbor", "remote_as", "up_down",
                         "state", "prefixes"])
        for dev in devices:
            try:
                with ConnectHandler(**netmiko_params(dev, user, password)) as conn:
                    rows = parse_summary(conn.send_command(command))
            except Exception as exc:
                print(f"FAILED  {dev['name']}: {str(exc).splitlines()[0]}")
                continue
            for r in rows:
                writer.writerow([dev["name"], r["neighbor"], r["remote_as"],
                                 r["up_down"], r["state"], r["prefixes"]])
                if not r["healthy"]:
                    down += 1
                    print(f"DOWN    {dev['name']} -> {r['neighbor']} "
                          f"(AS {r['remote_as']}) state={r['state']}")
            print(f"checked {dev['name']}: {len(rows)} neighbors")
    print(f"\n{down} neighbor(s) not Established. Full report: {args.output}")


if __name__ == "__main__":
    main()
