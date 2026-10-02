#!/usr/bin/env python3
"""Render device configs from YAML variables + a Jinja2 template.

Same idea as a golden-config template: the template holds the structure,
the YAML file holds what is different per device.

Example:
    python render_config.py vars/R1.yaml templates/bgp_vlan.j2 -o configs/
"""
import argparse
import pathlib

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vars", nargs="+", help="one or more device vars files")
    ap.add_argument("template")
    ap.add_argument("-o", "--outdir", default="configs")
    args = ap.parse_args()

    tpl_path = pathlib.Path(args.template)
    env = Environment(loader=FileSystemLoader(tpl_path.parent),
                      undefined=StrictUndefined,  # fail loudly on a missing variable
                      trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(tpl_path.name)

    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for var_file in args.vars:
        data = yaml.safe_load(pathlib.Path(var_file).read_text())
        out = outdir / f"{data['hostname']}_config.txt"
        out.write_text(template.render(**data))
        print(f"rendered {out}")


if __name__ == "__main__":
    main()
