"""Shared helpers: inventory loading and credential handling.

Credentials are never hard-coded. They come from environment variables
(NET_USER / NET_PASS) or are prompted for once at runtime.
"""
import getpass
import os

import yaml


def get_credentials():
    user = os.environ.get("NET_USER") or input("Username: ")
    password = os.environ.get("NET_PASS") or getpass.getpass("Password: ")
    return user, password


def load_inventory(path, default_device_type=None):
    """Load devices from a YAML inventory or a plain text file (one IP per line)."""
    with open(path) as f:
        if path.endswith((".yaml", ".yml")):
            devices = yaml.safe_load(f) or []
        else:
            devices = [{"host": line.strip()} for line in f
                       if line.strip() and not line.startswith("#")]
    for dev in devices:
        dev.setdefault("name", dev["host"])
        if default_device_type:
            dev.setdefault("device_type", default_device_type)
        if "device_type" not in dev:
            raise ValueError(f"{dev['host']}: no device_type (set it in the "
                             "inventory or pass --device-type)")
    return devices


def netmiko_params(dev, user, password):
    return {"device_type": dev["device_type"], "host": dev["host"],
            "username": user, "password": password}
