"""Tests for NichePulse scoring engine."""

import pytest
from nichepulse.scoring import score_niche, get_niche, list_niches, compare_niches, NICHE_DATABASE


class TestScoreNiche:
    def test_perfect_score(self):
        n = score_niche("Test", 5, 5, 5, 5, 5)
        assert n.total == 25
        assert n.grade == "S"
        assert n.verdict == "DOMINATE — Go all-in on this niche"

    def test_minimum_score(self):
        n = score_niche("Test", 1, 1, 1, 1, 1)
        assert n.total == 5
        assert n.grade == "D"

    def test_clamping_high(self):
        n = score_niche("Test", 10, 10, 10, 10, 10)
        assert n.total == 25

    def test_clamping_low(self):
        n = score_niche("Test", -5, -5, -5, -5, -5)
        assert n.total == 5

    def test_grade_boundaries(self):
        assert score_niche("A", 5, 5, 4, 4, 3).grade == "A"  # 21 → A
        assert score_niche("B", 4, 4, 3, 3, 3).grade == "B"  # 17 → B
        assert score_niche("C", 3, 2, 2, 2, 1).grade == "C"  # 10 → C

    def test_margin_estimate(self):
        high = score_niche("High", 5, 5, 5, 5, 5)
        assert "45-60%" in high.margin_estimate
        low = score_niche("Low", 1, 1, 1, 1, 1)
        assert "15-25%" in low.margin_estimate


class TestGetNiche:
    def test_exact_match(self):
        n = get_niche("pickleball")
        assert n is not None
        assert "Pickleball" in n.name
        assert n.total >= 20

    def test_fuzzy_match(self):
        n = get_niche("adhd")
        assert n is not None

    def test_no_match(self):
        n = get_niche("xyznonexistent123")
        assert n is None


class TestListNiches:
    def test_returns_sorted(self):
        niches = list_niches()
        assert len(niches) >= 10
        for i in range(len(niches) - 1):
            assert niches[i].total >= niches[i + 1].total

    def test_no_duplicates(self):
        niches = list_niches()
        names = [n.name for n in niches]
        assert len(names) == len(set(names))


class TestCompareNiches:
    def test_orders_by_score(self):
        results = compare_niches(["adhd-neurodivergent", "pickleball", "blue-collar"])
        assert len(results) >= 2
        for i in range(len(results) - 1):
            assert results[i].total >= results[i + 1].total

    def test_filters_invalid(self):
        results = compare_niches(["xyznonexistent"])
        assert len(results) == 0


class TestDatabase:
    def test_all_have_valid_scores(self):
        seen = set()
        for k, v in NICHE_DATABASE.items():
            if v.name not in seen:
                seen.add(v.name)
                assert 5 <= v.total <= 25, f"{v.name}: total {v.total}"
                assert v.grade in ("S", "A", "B", "C", "D")
