"""Core keyword research logic for generating SEO content ideas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence
import json
import csv
from pathlib import Path


@dataclass
class KeywordIdea:
    """Structured data for a keyword suggestion."""

    keyword: str
    intent: str
    difficulty: float
    opportunity: float
    angles: List[str]

    def as_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "intent": self.intent,
            "difficulty": round(self.difficulty, 2),
            "opportunity": round(self.opportunity, 2),
            "angles": self.angles,
        }


class KeywordResearcher:
    """Generate keyword and content ideas from a set of seeds."""

    def __init__(self, modifiers: Sequence[str] | None = None):
        self.modifiers = list(modifiers or self.default_modifiers())

    @staticmethod
    def default_modifiers() -> List[str]:
        return [
            "best",
            "top",
            "near me",
            "for beginners",
            "vs",
            "review",
            "alternatives",
            "how to",
            "ideas",
            "guide",
            "template",
            "checklist",
            "examples",
        ]

    def generate_variations(self, seeds: Iterable[str]) -> List[str]:
        variations: List[str] = []
        normalized = [seed.strip().lower() for seed in seeds if seed.strip()]
        for seed in normalized:
            variations.append(seed)
            for mod in self.modifiers:
                variations.extend(
                    {
                        f"{mod} {seed}",
                        f"{seed} {mod}",
                        f"{seed} {mod} 2024",
                    }
                )
        return sorted(set(variations))

    def intent_for(self, keyword: str) -> str:
        lowered = keyword.lower()
        informational_markers = ("how", "guide", "what", "why", "tips", "ideas", "checklist")
        transactional_markers = ("best", "top", "deal", "buy", "price", "vs", "review", "alternatives")
        local_markers = ("near me", "in ")

        if any(marker in lowered for marker in informational_markers):
            return "informational"
        if any(marker in lowered for marker in transactional_markers):
            return "transactional"
        if any(marker in lowered for marker in local_markers):
            return "local"
        return "general"

    def difficulty_score(self, keyword: str) -> float:
        words = keyword.split()
        length_penalty = max(1, len(words))
        question_bonus = -0.5 if any(word in {"how", "what", "why"} for word in words) else 0
        modifier_bonus = -0.2 if any(mod in keyword for mod in self.modifiers) else 0
        base = 5.0 + len(keyword) * 0.05
        return max(1.0, base / length_penalty + question_bonus + modifier_bonus)

    def opportunity_score(self, keyword: str, difficulty: float) -> float:
        long_tail_bonus = max(0, (len(keyword.split()) - 2) * 1.2)
        freshness_bonus = 1.5 if "2024" in keyword else 0
        informational_bonus = 1.0 if self.intent_for(keyword) == "informational" else 0
        return max(0.5, 10 - difficulty + long_tail_bonus + freshness_bonus + informational_bonus)

    def angles_for(self, keyword: str) -> List[str]:
        base = [
            f"Answer common questions about {keyword}",
            f"Create a comparison table for {keyword}",
            f"Provide step-by-step tutorial for {keyword}",
            f"Share expert roundup quotes on {keyword}",
            f"Add downloadable checklist for {keyword}",
        ]
        if "near me" in keyword:
            base.append(f"Include local maps and directories for {keyword}")
        if "vs" in keyword:
            base.append(f"Highlight the pros, cons, and use-cases of each item in {keyword}")
        return base

    def research(self, seeds: Iterable[str], top_n: int = 50) -> List[KeywordIdea]:
        variations = self.generate_variations(seeds)
        ideas: List[KeywordIdea] = []
        for keyword in variations:
            intent = self.intent_for(keyword)
            difficulty = self.difficulty_score(keyword)
            opportunity = self.opportunity_score(keyword, difficulty)
            angles = self.angles_for(keyword)
            ideas.append(
                KeywordIdea(
                    keyword=keyword,
                    intent=intent,
                    difficulty=difficulty,
                    opportunity=opportunity,
                    angles=angles,
                )
            )
        return sorted(ideas, key=lambda idea: idea.opportunity, reverse=True)[:top_n]

    @staticmethod
    def export_csv(ideas: Sequence[KeywordIdea], path: str | Path) -> None:
        fieldnames = ["keyword", "intent", "difficulty", "opportunity", "angles"]
        with Path(path).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for idea in ideas:
                row = idea.as_dict()
                row["angles"] = "; ".join(idea.angles)
                writer.writerow(row)

    @staticmethod
    def export_json(ideas: Sequence[KeywordIdea], path: str | Path) -> None:
        with Path(path).open("w", encoding="utf-8") as handle:
            json.dump([idea.as_dict() for idea in ideas], handle, indent=2)
