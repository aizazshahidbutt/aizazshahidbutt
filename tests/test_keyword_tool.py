from seo_tool.keyword_research import KeywordResearcher


def test_generate_variations():
    researcher = KeywordResearcher(modifiers=["best", "guide"])
    variations = researcher.generate_variations(["python blogging"])
    assert "python blogging" in variations
    assert "best python blogging" in variations
    assert "python blogging guide 2024" in variations


def test_intent_and_scoring():
    researcher = KeywordResearcher()
    kw = "how to start a food blog"
    intent = researcher.intent_for(kw)
    difficulty = researcher.difficulty_score(kw)
    opportunity = researcher.opportunity_score(kw, difficulty)

    assert intent == "informational"
    assert difficulty < 10
    assert opportunity > difficulty


def test_top_results_sorted():
    researcher = KeywordResearcher()
    ideas = researcher.research(["budget travel"], top_n=5)
    assert len(ideas) == 5
    assert ideas[0].opportunity >= ideas[-1].opportunity
