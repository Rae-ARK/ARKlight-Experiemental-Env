"""Stage 0 CLI: `arklight-native-env inspect <site.py>`.

Deliberately the only subcommand at this stage. It proves the IR is
reachable and legible; it does not render anything, native or
otherwise. See docs/ARCHITECTURE.md, "Implementation staging".
"""

from __future__ import annotations

import argparse
import sys

from .ir_loader import IRLoadError, dump_ir, load_ir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="arklight-native-env",
        description=(
            "Stage 0 scaffold for ARKlight's experimental native "
            "environment. Currently supports only IR inspection -- "
            "no rendering."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="Load a site source's IR via arklight and print it as JSON.",
    )
    inspect_parser.add_argument("site_source", help="Path to an ARKlight site .py file")

    args = parser.parse_args(argv)

    if args.command == "inspect":
        try:
            ir = load_ir(args.site_source)
        except IRLoadError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(dump_ir(ir))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
