# Blogging SEO Keyword Research Tool

A lightweight Python tool to brainstorm untapped keyword ideas and content angles for blogging sites. It expands seed topics with SEO modifiers, scores opportunities, and suggests outlines you can turn into posts.

## Features
- Generates long-tail variations around your seed keywords using proven modifiers.
- Labels keywords by search intent (informational, transactional, local, or general).
- Heuristic difficulty and opportunity scoring to surface quick-win topics.
- Content angle suggestions for each keyword to accelerate brief writing.
- Exportable CSV/JSON reports for prioritization.

## Quick start
1. **Install dependencies**: the tool only needs Python 3.11+ and the standard library.
2. **Run from the command line**:

```bash
python cli.py --seed "budget travel" "meal prep" --top 10 --csv report.csv
```

You can also provide seeds from a file:

```bash
python cli.py --seed-file seeds.txt --json ideas.json
```

## Library usage

```python
from seo_tool import KeywordResearcher

researcher = KeywordResearcher()
ideas = researcher.research(["budget travel", "meal prep"], top_n=15)
for idea in ideas:
    print(idea.keyword, idea.intent, idea.opportunity)
```

## Running tests

```bash
python -m pytest
```
