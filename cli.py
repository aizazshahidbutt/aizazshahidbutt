"""Command-line interface for the SEO keyword research tool."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from seo_tool import KeywordResearcher


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate untapped keyword research and content angles for blogs",
    )
    parser.add_argument(
        "--seed",
        nargs="*",
        default=[],
        help="Seed keywords to expand (space separated)",
    )
    parser.add_argument(
        "--seed-file",
        type=Path,
        help="Optional path to a text file with one seed per line",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=25,
        help="Number of keyword ideas to keep (sorted by opportunity)",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        help="Path to export a CSV report",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Path to export a JSON report",
    )
    return parser.parse_args()


def load_seeds(seed_args: List[str], seed_file: Path | None) -> List[str]:
    seeds = list(seed_args)
    if seed_file and seed_file.exists():
        seeds.extend(line.strip() for line in seed_file.read_text().splitlines())
    if not seeds:
        raise SystemExit("Provide at least one --seed or --seed-file")
    return seeds


def main() -> None:
    args = parse_args()
    seeds = load_seeds(args.seed, args.seed_file)
    researcher = KeywordResearcher()
    ideas = researcher.research(seeds, top_n=args.top)

    for idea in ideas:
        print(
            f"{idea.keyword} | intent: {idea.intent} | difficulty: {idea.difficulty:.2f} | "
            f"opportunity: {idea.opportunity:.2f}"
        )
        for angle in idea.angles:
            print(f"  - {angle}")
        print()

    if args.csv:
        researcher.export_csv(ideas, args.csv)
        print(f"Saved CSV report to {args.csv}")
    if args.json:
        researcher.export_json(ideas, args.json)
        print(f"Saved JSON report to {args.json}")


if __name__ == "__main__":
    main()
