# Structural Entropy Survey

A decade survey of structural entropy (SE) since the 2016 IEEE TIT paper,
covering theory, optimization, graph clustering, GNNs, dynamics, reinforcement
learning, and reproducibility.  Targeting the **TGINA** journal (deadline 31 Jul 2026).

## Directory Structure

```
structural-entropy-survey/
├── papers/                    ← literature hub (source of truth)
│   ├── papers.csv             ← every paper: key, venue, category, in_bib, …
│   ├── sync.py                ← check coverage · detect dupes · build awesome MD
│   └── awesome-structural-entropy.md   ← generated; commit after --build
│
├── paper/                     ← LaTeX journal paper
│   ├── main.tex               ← root; compile with pdflatex → bibtex → pdflatex×2
│   ├── refs.bib               ← BibTeX; keys must match papers.csv
│   └── sections/
│
├── benchmark/                 ← all empirical work
│   ├── runners/               ← Python benchmark scripts
│   └── results/               ← JSON / Markdown outputs
│
├── code/                      ← companion library (glass.seclust)
│   └── survey_support/
│
├── ijcai/                     ← IJCAI 2025 camera-ready zip
├── docs/                      ← internal notes and analysis
└── SUBMIT_TODO.md             ← journal submission checklist
```

## Literature Workflow

**Add a new paper:**
```bash
# 1. append a row to papers/papers.csv  (key = proposed BibTeX key)
# 2. add the BibTeX entry to paper/refs.bib
# 3. set in_bib=yes in the CSV row
cd papers && python sync.py --check   # verify zero gaps
cd papers && python sync.py --build   # regenerate awesome MD
git add papers/papers.csv paper/refs.bib papers/awesome-structural-entropy.md
```

**Key naming convention:** `{surname}{year}{2-3wordabbrev}` — e.g. `sun2024lsenet`, `yang2024incremental`.  
For preprint→published: use the published year+venue key; put arXiv ID in the `arxiv_id` column.

**Current status (auto from `sync.py`):**
- `papers.csv` : 88 entries · 76 in refs.bib · 12 pending · 7 benchmarked
- Known duplicates: `sunli2024lsente` = `sun2024lsenet`; `zou2024multispans` = `zou2024transformer`

## Compile Paper

```bash
cd paper
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

