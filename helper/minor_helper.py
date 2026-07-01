"""Minor helper utilities for the shorts generator."""

import os
import random


FINANCE_FACTS = [
    "Warren Buffett bought his first stock at age 11.",
    "The New York Stock Exchange was founded in 1792 under a buttonwood tree.",
    "Apple was founded in a garage by Steve Jobs and Steve Wozniak in 1976.",
    "The first credit card was introduced in 1950 by Diners Club.",
    "The US dollar was created by the Coinage Act of 1792.",
    "The term 'bull market' comes from the way a bull thrusts its horns upward.",
    "The world's first stock exchange opened in Amsterdam in 1602.",
    "Compound interest is called the eighth wonder of the world by Einstein.",
    "The Great Depression caused the US stock market to drop 89 percent.",
    "Bitcoin was created in 2009 by the mysterious Satoshi Nakamoto.",
    "The Federal Reserve was established in 1913 to stabilize the economy.",
    "The first ATM was installed in London in 1967.",
    "The US national debt first exceeded one trillion dollars in 1981.",
    "Penny stocks are shares trading below five dollars per share.",
    "The Dow Jones Industrial Average started with just 12 companies in 1896.",
    "Inflation erodes purchasing power over time silently.",
    "The Rule of 72 estimates how long it takes to double your money.",
    "A 401k is named after a section of the US tax code.",
    "The first IPO was the Dutch East India Company in 1602.",
    "Credit scores range from 300 to 850 in the FICO model.",
    "The S and P 500 tracks 500 of the largest US companies.",
    "Day trading requires buying and selling within the same day.",
    "The gold standard was abandoned by the US in 1971.",
    "Diversification reduces risk by spreading investments across assets.",
    "A bear market is defined as a 20 percent decline from recent highs.",
    "The richest one percent own more than half of global wealth.",
    "Index funds were invented by John Bogle in 1975.",
    "The FDIC insures bank deposits up to 250,000 dollars.",
    "Stock buybacks reduce shares outstanding and boost earnings per share.",
    "The SEC was created after the 1929 stock market crash.",
]


def pick_random_fact() -> str:
    """Return a random finance fact from the local dictionary."""
    return random.choice(FINANCE_FACTS)


def split_into_cards(text: str, max_cards: int = 4) -> list[str]:
    """Split a fact into 3-4 script cards for sequential display."""
    words = text.split()
    total_words = len(words)
    if total_words <= 3:
        return [text]

    # Determine number of cards (3 or 4)
    num_cards = min(max_cards, max(3, (total_words + 2) // 3))
    base = total_words // num_cards
    remainder = total_words % num_cards

    cards = []
    idx = 0
    for i in range(num_cards):
        size = base + (1 if i < remainder else 0)
        card_words = words[idx : idx + size]
        cards.append(" ".join(card_words))
        idx += size

    return cards


def ensure_dir(path: str) -> None:
    """Create directory if it does not exist."""
    os.makedirs(path, exist_ok=True)
