#!/usr/bin/env python3
"""Run one show command on many devices in parallel and save results to CSV.

Example:
    python show_to_csv.py -i inventory.yaml -c "show version" -o versions.csv
    python show_to_csv.py -i ips.txt --device-type a10 -c "show bootimage"
"""
import argparse
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

from netmiko import ConnectHandler

from common import get_credentials, load_inventory, netmiko_params


def run(dev, command, user, password):
    try:
        with ConnectHandler(**netmiko_params(dev, user, password)) as conn:
            output = conn.send_command(command)
        return dev, "ok", output.strip()
    except Exception as exc:  # report and keep going with other devices
        return dev, "failed", str(exc).splitlines()[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-i", "--inventory", required=True,
                    help="inventory.yaml or a .txt file with one IP per line")
    ap.add_argument("-c", "--command", required=True)
    ap.add_argument("-o", "--output", default="output.csv")
    ap.add_argument("--device-type", help="Netmiko type when the inventory lacks one")
    ap.add_argument("-w", "--workers", type=int, default=10,
                    help="devices to run at the same time (default 10)")
    args = ap.parse_args()

    devices = load_inventory(args.inventory, args.device_type)
    user, password = get_credentials()

    with ThreadPoolExecutor(max_workers=args.workers) as pool, \
            open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "host", "status", "output"])
        jobs = [pool.submit(run, d, args.command, user, password) for d in devices]
        for job in as_completed(jobs):
            dev, status, output = job.result()
            writer.writerow([dev["name"], dev["host"], status, output])
            print(f"{status:7} {dev['name']} ({dev['host']})")
    print(f"Saved {len(devices)} results to {args.output}")


if __name__ == "__main__":
    main()
