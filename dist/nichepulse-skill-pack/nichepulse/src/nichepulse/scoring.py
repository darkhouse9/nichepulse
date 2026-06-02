"""NichePulse — AI-Powered Niche Scoring Engine
Scores niches on 5 dimensions using live data signals.
Loads niche database from data/niche-database.json (v2.0 — 80+ niches).
"""

from dataclasses import dataclass, field
from typing import Optional
import json
import os


@dataclass
class NicheScore:
    name: str
    passion: int = 0          # 1-5: identity attachment, community engagement
    buy_frequency: int = 0    # 1-5: how often audience buys
    gift_potential: int = 0   # 1-5: gift-buying likelihood
    competition: int = 0      # 1-5: 1=saturated, 5=untapped
    trend: int = 0            # 1-5: declining to exploding
    notes: list = field(default_factory=list)
    sources: dict = field(default_factory=dict)

    @property
    def total(self) -> int:
        return self.passion + self.buy_frequency + self.gift_potential + self.competition + self.trend

    @property
    def grade(self) -> str:
        t = self.total
        if t >= 22: return "S"
        if t >= 18: return "A"
        if t >= 14: return "B"
        if t >= 10: return "C"
        return "D"

    @property
    def verdict(self) -> str:
        return {
            "S": "DOMINATE — Go all-in on this niche",
            "A": "PRIORITIZE — Strong opportunity, start immediately",
            "B": "VIABLE — Good candidate, validate with small test",
            "C": "WEAK — Only pursue if you have unique advantage",
            "D": "SKIP — Too competitive or declining",
        }[self.grade]

    @property
    def margin_estimate(self) -> str:
        """Estimated profit margin based on competition + trend."""
        if self.competition >= 4 and self.trend >= 4:
            return "45-60% (low competition + growing = premium pricing)"
        if self.competition >= 3:
            return "30-45% (moderate competition)"
        return "15-25% (high competition = price pressure)"


def score_niche(
    name: str,
    passion: int,
    buy_frequency: int,
    gift_potential: int,
    competition: int,
    trend: int,
    notes: Optional[list] = None,
) -> NicheScore:
    """Create a validated NicheScore with clamped values."""
    clamp = lambda v: max(1, min(5, int(v)))
    return NicheScore(
        name=name,
        passion=clamp(passion),
        buy_frequency=clamp(buy_frequency),
        gift_potential=clamp(gift_potential),
        competition=clamp(competition),
        trend=clamp(trend),
        notes=notes or [],
    )


def _load_niche_database() -> dict:
    """Load niche database from JSON file. Returns dict of slug -> NicheScore."""
    db_path = os.path.join(os.path.dirname(__file__), "data", "niche-database.json")
    try:
        with open(db_path, "r") as f:
            data = json.load(f)
        db = {}
        for niche in data.get("niches", []):
            slug = niche.get("slug", "").lower()
            if slug:
                db[slug] = NicheScore(
                    name=niche["name"],
                    passion=niche.get("passion", 3),
                    buy_frequency=niche.get("buy_freq", 3),
                    gift_potential=niche.get("gift", 3),
                    competition=niche.get("comp", 3),
                    trend=niche.get("trend", 3),
                    notes=niche.get("notes", []),
                    sources={
                        "avg_order": niche.get("avg_order"),
                        "etsy_results": niche.get("etsy_results"),
                        "competition_level": niche.get("competition"),
                        "top_products": niche.get("top_products"),
                        "design_angle": niche.get("design_angle"),
                    },
                )
        return db
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Load database at import time
NICHE_DATABASE = _load_niche_database()


def get_niche(keyword: str) -> Optional[NicheScore]:
    """Look up a niche by keyword (fuzzy)."""
    keyword = keyword.lower().strip()
    # Exact match
    if keyword in NICHE_DATABASE:
        return NICHE_DATABASE[keyword]
    # Fuzzy match
    for k, v in NICHE_DATABASE.items():
        if keyword in k or k in keyword:
            return v
    return None


def list_niches() -> list[NicheScore]:
    """Return all scored niches, sorted by total score descending."""
    seen = set()
    results = []
    for v in NICHE_DATABASE.values():
        if v.name not in seen:
            seen.add(v.name)
            results.append(v)
    return sorted(results, key=lambda x: x.total, reverse=True)


def compare_niches(keywords: list[str]) -> list[NicheScore]:
    """Compare multiple niches side by side."""
    results = []
    for kw in keywords:
        n = get_niche(kw)
        if n:
            results.append(n)
    return sorted(results, key=lambda x: x.total, reverse=True)
