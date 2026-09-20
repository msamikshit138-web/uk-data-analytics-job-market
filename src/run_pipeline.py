"""Convenience runner for public and optional Adzuna pipelines."""

from __future__ import annotations
import argparse
import subprocess
import sys


def run(script: str) -> None:
    subprocess.run([sys.executable, script], check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", action="store_true", help="Run public Indeed pipeline")
    parser.add_argument("--adzuna", action="store_true", help="Run Adzuna live-vacancy pipeline")
    args = parser.parse_args()

    if not args.public and not args.adzuna:
        parser.error("Choose at least one of --public or --adzuna")

    if args.public:
        run("src/download_public_data.py")
        run("src/analyse_public_market.py")

    if args.adzuna:
        run("src/collect_adzuna.py")
        run("src/clean_adzuna.py")


if __name__ == "__main__":
    main()
