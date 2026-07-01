"""Orchestrate the YouTube Shorts generation pipeline."""

import os
import sys

# Ensure project root is on path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helper.minor_helper import pick_random_fact, split_into_cards, ensure_dir
from automation.shorts_maker_FFmpeg import build_short


OUTPUT_DIR = "output"
DEFAULT_CARD_DURATION = 2  # seconds per card


def main() -> None:
    """Run the full pipeline: pick fact, split into cards, generate video."""
    print("=" * 50)
    print("YouTube Shorts Generator - Starting Pipeline")
    print("=" * 50)

    # Step 1: Pick a random finance fact
    fact = pick_random_fact()
    print(f"\nSelected fact: {fact}")

    # Step 2: Split into script cards
    cards = split_into_cards(fact)
    print(f"\nGenerated {len(cards)} script card(s):")
    for i, card in enumerate(cards, 1):
        print(f"  Card {i}: {card}")

    # Step 3: Assign durations
    durations = [DEFAULT_CARD_DURATION] * len(cards)
    print(f"\nDurations: {durations}")

    # Step 4: Ensure output directory exists
    ensure_dir(OUTPUT_DIR)

    # Step 5: Build the short
    print("\nGenerating frames and rendering video with FFmpeg...")
    output_path = build_short(cards, durations, OUTPUT_DIR)

    print(f"\nDone! Video saved to: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    print("=" * 50)


if __name__ == "__main__":
    main()
