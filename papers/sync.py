#!/usr/bin/env python3
"""
papers/sync.py  —  literature management for the structural entropy survey.

Usage:
    python sync.py              # default: coverage check
    python sync.py --check      # same as default
    python sync.py --build      # regenerate awesome-structural-entropy.md
    python sync.py --dupes      # find potential duplicate entries
    python sync.py --missing    # list papers to add to refs.bib (in_bib=no)
"""

import argparse
import csv
import re
from urllib.parse import quote_plus
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT       = Path(__file__).parent
PAPERS_CSV = ROOT / "papers.csv"
REFS_BIB   = ROOT.parent / "paper" / "refs.bib"
AWESOME_MD = ROOT / "awesome-structural-entropy.md"

# ── taxonomy ──────────────────────────────────────────────────────────────────
CATEGORIES = {
    "theory":        "Theoretical Foundations",
    "algorithms":    "SE Minimisation Algorithms",
    "graph-learning":"Graph Learning & Representation",
    "rl":            "Reinforcement Learning",
    "applications":  "Domain Applications",
    "misc":          "Baselines & Related Work",
}

SUBCATEGORY_ORDER = {
    "theory":        ["foundation", "extension", "related-theory"],
    "algorithms":    ["combinatorial", "constrained", "neural"],
    "graph-learning":["structure-learning", "contrastive", "pooling",
                      "classification", "ood", "hierarchical-text",
                      "sample-selection", "survey"],
    "rl":            ["decision-making", "exploration", "marl", "offline"],
    "applications":  ["social-bot", "event-detection", "anomaly-detection",
                      "bioinformatics", "speech", "knowledge", "llm",
                      "fairness", "timeseries", "nlp", "recommendation",
                      "vision"],
    "misc":          ["baseline", "survey", "related-work", "related-theory"],
}

RESOURCE_OVERRIDES = {
    "pan2021information": {
        "paper_url": "https://openreview.net/forum?id=LPB2BFZvncQ",
    },
    "wu2022pooling": {
        "paper_url": "https://icml.cc/virtual/2022/poster/15959",
    },
    "pan2025hcsegraphs": {
        "openreview_url": "https://openreview.net/forum?id=wVoRs2K4nq",
        "tex_source_url": "https://openreview.net/forum?id=wVoRs2K4nq",
    },
    "zeng2026siamd": {
        "paper_url": "https://pubmed.ncbi.nlm.nih.gov/41428906/",
    },
}

# ── I/O helpers ───────────────────────────────────────────────────────────────
def load_papers() -> list[dict]:
    with open(PAPERS_CSV, newline="") as f:
        return list(csv.DictReader(f))


def bib_keys() -> set[str]:
    text = REFS_BIB.read_text()
    return set(re.findall(r"@\w+\{(\w[\w\-]*),", text))


def bib_meta() -> dict[str, dict[str, str]]:
    text = REFS_BIB.read_text()
    entries: dict[str, dict[str, str]] = {}
    for m in re.finditer(r"@(\w+)\{([^,]+),", text):
        start = m.start()
        key = m.group(2).strip()
        brace_depth = 0
        end = None
        for i in range(start, len(text)):
            if text[i] == "{":
                brace_depth += 1
            elif text[i] == "}":
                brace_depth -= 1
                if brace_depth == 0:
                    end = i
                    break
        if end is None:
            continue
        block = text[start:end + 1]
        meta: dict[str, str] = {}
        for field, value in re.findall(r"(\w+)\s*=\s*\{([^{}]*)\}", block, flags=re.S):
            meta[field.lower()] = " ".join(value.split())
        entries[key] = meta
    return entries


def paper_url(entry: dict, bib_entry: dict[str, str] | None) -> str | None:
    override = RESOURCE_OVERRIDES.get(entry["key"], {})
    if override.get("paper_url"):
        return override["paper_url"]
    if entry.get("paper_url"):
        return entry["paper_url"]
    if entry.get("arxiv_id"):
        return f"https://arxiv.org/abs/{entry['arxiv_id']}"
    if bib_entry:
        if bib_entry.get("eprint") and bib_entry.get("archiveprefix", "").lower() == "arxiv":
            return f"https://arxiv.org/abs/{bib_entry['eprint']}"
        if bib_entry.get("doi"):
            return f"https://doi.org/{bib_entry['doi']}"
        if bib_entry.get("url"):
            return bib_entry["url"]
    return None


def abstract_search_url(title: str) -> str:
    return f"https://www.semanticscholar.org/search?q={quote_plus(title)}"


def paper_link(entry: dict, bib_entry: dict[str, str] | None) -> tuple[str, bool]:
    direct = paper_url(entry, bib_entry)
    if direct:
        return direct, True
    return abstract_search_url(entry["title"]), False


METHOD_BY_SUBCATEGORY = {
    "foundation": "This work develops a foundational theoretical treatment of information structure in networks or related systems.",
    "extension": "This work extends SE theory to a new mathematical setting or analytical viewpoint.",
    "combinatorial": "This paper presents a discrete clustering or partitioning method.",
    "constrained": "This paper presents a constrained or semi-supervised clustering method.",
    "neural": "This paper presents a neural or continuous optimization model for clustering.",
    "contrastive": "This paper presents a graph contrastive learning method.",
    "structure-learning": "This paper presents a graph structure learning, abstraction, or selection method.",
    "pooling": "This paper presents a hierarchical graph pooling or representation method.",
    "classification": "This paper presents a graph-based classification method.",
    "ood": "This paper presents a graph out-of-distribution detection method.",
    "hierarchical-text": "This paper presents a hierarchical text classification method.",
    "sample-selection": "This paper presents a sample selection method for efficient learning.",
    "decision-making": "This paper presents a hierarchical decision-making or state abstraction method.",
    "exploration": "This paper presents an exploration-oriented reinforcement learning method.",
    "marl": "This paper presents a multi-agent reinforcement learning method.",
    "offline": "This paper presents an offline reinforcement learning method.",
    "social-bot": "This paper presents a social-bot detection or adversarial behavior modeling method.",
    "event-detection": "This paper presents a social or multimodal event detection method.",
    "anomaly-detection": "This paper presents a graph anomaly detection method.",
    "bioinformatics": "This paper presents a bioinformatics or genomics analysis method.",
    "speech": "This paper presents a speech or audio representation method.",
    "knowledge": "This paper presents a knowledge-structure or science-of-science analysis method.",
    "llm": "This paper presents an LLM hallucination, uncertainty, or faithfulness evaluation method.",
    "fairness": "This paper presents a fairness-aware graph learning method.",
    "timeseries": "This paper presents a spatio-temporal forecasting method.",
    "nlp": "This paper presents an NLP structured prediction method.",
    "recommendation": "This paper presents a recommendation pretraining or representation method.",
    "vision": "This paper presents a vision enhancement or segmentation method.",
    "survey": "This paper surveys the surrounding literature.",
    "baseline": "This paper introduces a baseline or comparator widely used in clustering or graph learning.",
    "related-work": "This work provides adjacent context rather than proposing an SE method.",
    "related-theory": "This work provides broader theoretical context related to SE.",
}

SE_ROLE_BY_SUBCATEGORY = {
    "foundation": "Structural entropy is itself the main object being defined, interpreted, or analyzed.",
    "extension": "Structural entropy is extended, compared, or reinterpreted in a new mathematical setting.",
    "combinatorial": "Structural entropy serves as the core optimization objective for building the partition or hierarchy.",
    "constrained": "Structural entropy is optimized under supervision, contiguity, or other domain constraints.",
    "neural": "Structural entropy is relaxed into a differentiable objective that shapes the learned representation or clustering tree.",
    "contrastive": "Structural entropy guides the view construction or structural regularization used for contrastive learning.",
    "structure-learning": "Structural entropy guides graph construction, structural abstraction, or feature/structure selection.",
    "pooling": "Structural entropy guides hierarchical pooling by favoring globally coherent graph coarsenings.",
    "classification": "Structural entropy provides class or community structure that improves prediction under limited supervision.",
    "ood": "Structural entropy is used to quantify structural irregularity or uncertainty for OOD detection.",
    "hierarchical-text": "Structural entropy regularizes hierarchy construction or smoothing over label structure.",
    "sample-selection": "Structural entropy is used to score data structure and choose informative training samples.",
    "decision-making": "Structural information or entropy builds hierarchical abstractions over states or actions for planning.",
    "exploration": "Structural information shapes exploration toward informative and stable state communities.",
    "marl": "Structural information organizes multi-agent roles or coordination hierarchies.",
    "offline": "Structural information organizes trajectory hierarchies and structural entropy regularizes offline policy learning.",
    "social-bot": "Structural entropy quantifies behavioral uncertainty and uncovers hierarchical communities that support detection or simulation.",
    "event-detection": "Structural entropy drives community discovery over posts, users, or multimodal signals to localize events.",
    "anomaly-detection": "Structural entropy exposes abnormal structural patterns relative to learned graph hierarchies.",
    "bioinformatics": "Structural entropy is used to recover biological hierarchies or partitions from genomic interaction or cell-state data.",
    "speech": "Structural entropy compresses or reorganizes audio representations into more structured codes.",
    "knowledge": "Structural entropy is used to quantify idea evolution or information structure in knowledge systems.",
    "llm": "Structural entropy or structural information is used to quantify uncertainty, faithfulness, or semantic consistency.",
    "fairness": "Structural entropy shapes community structure while balancing predictive performance and fairness.",
    "timeseries": "Structural entropy is used to uncover structured dependencies across spatial or temporal components.",
    "nlp": "Structural entropy guides graph, span, or relation partitioning in the NLP pipeline.",
    "recommendation": "Structural entropy supplies higher-order structure for pretraining or representation learning.",
    "vision": "Structural entropy is used to separate structure, degradation, or region hierarchies in visual data.",
    "survey": "Structural entropy is the organizing lens used to compare the literature.",
    "baseline": "This work is included as a baseline or comparator rather than as an SE proposal.",
    "related-work": "This work is included as adjacent context rather than as a direct SE method.",
    "related-theory": "This work provides theoretical context for interpreting SE objectives and comparisons.",
}


def summary_sentences(entry: dict) -> str:
    sub = entry.get("subcategory", "")
    cat = entry.get("category", "")
    method = METHOD_BY_SUBCATEGORY.get(
        sub,
        "This paper presents a method or perspective relevant to structural entropy research.",
    )
    se_role = SE_ROLE_BY_SUBCATEGORY.get(
        sub,
        "Structural entropy is used here as either the main object of study or the organizing principle for the method.",
    )
    if cat == "misc" and sub in {"baseline", "related-work", "related-theory"}:
        return f"{method} {se_role}"
    return f"{method} {se_role}"


# ── commands ──────────────────────────────────────────────────────────────────
def cmd_check(papers: list[dict], bib: set[str]):
    """Print full coverage report."""
    print("=" * 60)
    print("COVERAGE REPORT")
    print("=" * 60)

    csv_keys = {p["key"] for p in papers}

    # 1. keys marked in_bib=yes but absent from refs.bib
    ghost = [p for p in papers if p["in_bib"] == "yes" and p["key"] not in bib]
    if ghost:
        print(f"\n[!] {len(ghost)} entries marked in_bib=yes but key missing from refs.bib:")
        for p in ghost:
            print(f"    {p['key']:<35}  {p['year']}  {p['venue']}")

    # 2. keys in refs.bib but not catalogued in papers.csv
    uncatalogued = sorted(bib - csv_keys)
    if uncatalogued:
        print(f"\n[?] {len(uncatalogued)} refs.bib keys not in papers.csv:")
        for k in uncatalogued:
            print(f"    {k}")

    # 3. papers with in_bib=no
    to_add = [p for p in papers if p["in_bib"] == "no"]
    print(f"\n[+] {len(to_add)} papers not yet in refs.bib (run --missing for details)")

    # summary
    in_bib_count  = sum(1 for p in papers if p["in_bib"] == "yes")
    benchmarked   = sum(1 for p in papers if p["benchmarked"] == "yes")
    print("\n" + "-" * 40)
    print(f"papers.csv  : {len(papers):3d} entries  "
          f"({in_bib_count} in bib, {len(to_add)} pending, "
          f"{benchmarked} benchmarked)")
    print(f"refs.bib    : {len(bib):3d} entries")
    print(f"Uncatalogued: {len(uncatalogued):3d}")
    print("-" * 40)


def cmd_missing(papers: list[dict]):
    """List all papers not yet in refs.bib, with suggested keys."""
    to_add = [p for p in papers if p["in_bib"] == "no"]
    if not to_add:
        print("All papers are already in refs.bib.")
        return
    print(f"{'KEY':<35} {'YEAR':<6} {'VENUE':<22} TITLE")
    print("-" * 100)
    for p in to_add:
        print(f"{p['key']:<35} {p['year']:<6} {p['venue']:<22} {p['title'][:55]}")


def cmd_dupes(papers: list[dict]):
    """Detect potential duplicate entries (same normalised title prefix)."""
    by_norm = defaultdict(list)
    for p in papers:
        norm = re.sub(r"[^a-z0-9]", "", p["title"].lower())[:55]
        by_norm[norm].append(p)

    found = False
    for _, group in by_norm.items():
        if len(group) > 1:
            found = True
            print("POTENTIAL DUPLICATE:")
            for p in group:
                print(f"  {p['key']:<35}  {p['year']}  {p['title'][:60]}")
            print()
    if not found:
        print("No duplicates detected.")


def cmd_build(papers: list[dict]):
    """Regenerate awesome-structural-entropy.md from papers.csv."""
    bib = bib_keys()
    meta = bib_meta()

    # group papers
    cat_map: dict[str, dict[str, list[dict]]] = {
        cat: defaultdict(list) for cat in CATEGORIES
    }
    for p in papers:
        cat  = p.get("category", "misc")
        sub  = p.get("subcategory", "")
        if cat not in cat_map:
            cat = "misc"
        cat_map[cat][sub].append(p)

    total = len(papers)
    today = date.today().isoformat()
    direct_paper_links = 0
    abstract_fallback_links = 0
    code_links = 0
    project_links = 0
    dataset_links = 0
    weight_links = 0
    openreview_links = 0

    for p in papers:
        b = meta.get(p["key"], {})
        _, is_direct = paper_link(p, b)
        override = RESOURCE_OVERRIDES.get(p["key"], {})
        if is_direct:
            direct_paper_links += 1
        else:
            abstract_fallback_links += 1
        if p.get("code_url") or override.get("code_url"):
            code_links += 1
        if p.get("project_url") or override.get("project_url"):
            project_links += 1
        if p.get("dataset_url") or override.get("dataset_url"):
            dataset_links += 1
        if p.get("weights_url") or override.get("weights_url"):
            weight_links += 1
        if p.get("openreview_url") or override.get("openreview_url"):
            openreview_links += 1

    lines = [
        "# Awesome Structural Entropy Papers",
        "",
        "> A curated, living bibliography for the survey on **Structural Entropy",
        "> and Structural Information Theory** (TGINA journal version).",
        ">",
        f"> Source of truth: [`papers.csv`](papers.csv) · "
        f"Generated by [`sync.py`](sync.py) · Last updated: {today}",
        "",
        "**Legend**: "
        "`[P]` direct paper/abstract page · `[A]` abstract-search fallback · `[C]` code · `[PJ]` project page · "
        "`[D]` dataset · `[W]` weights · `[OR]` OpenReview · `[T]` TeX source · "
        "`★` in survey `refs.bib` · `⚗` benchmarked in this survey",
        "",
        f"**Resource Coverage**: direct paper links `{direct_paper_links}/{total}` · "
        f"fallback abstract links `{abstract_fallback_links}/{total}` · "
        f"code `{code_links}/{total}` · project pages `{project_links}/{total}` · "
        f"datasets `{dataset_links}/{total}` · weights `{weight_links}/{total}` · "
        f"OpenReview `{openreview_links}/{total}`",
        "",
        "---",
        "",
        "## Table of Contents",
        "",
    ]
    for cat_key, cat_title in CATEGORIES.items():
        n = sum(len(v) for v in cat_map[cat_key].values())
        lines.append(f"- [{cat_title}](#{cat_key.replace('-','')}) ({n})")
    lines += ["", f"*{total} papers total.*", "", "---", ""]

    for cat_key, cat_title in CATEGORIES.items():
        sub_map = cat_map[cat_key]
        n = sum(len(v) for v in sub_map.values())
        anchor = cat_key.replace("-", "")
        lines.append(f'## {cat_title} <a name="{anchor}"></a>')
        lines.append("")

        if not sub_map:
            lines += ["_No entries yet._", "", "---", ""]
            continue

        # iterate subcategories in defined order, then any leftovers
        ordered_subs = SUBCATEGORY_ORDER.get(cat_key, [])
        all_subs = ordered_subs + [s for s in sub_map if s not in ordered_subs]

        for sub in all_subs:
            entries = sub_map.get(sub)
            if not entries:
                continue
            sub_label = sub.replace("-", " ").title() if sub else "General"
            lines.append(f"### {sub_label}")
            lines.append("")
            lines.append("| Title | Authors | Venue | Year | Resources | Summary |")
            lines.append("|-------|---------|-------|------|-----------|---------|")

            for e in sorted(entries, key=lambda x: x["year"], reverse=True):
                title   = e["title"]
                authors = e["authors_short"]
                venue   = e["venue"]
                year    = e["year"]
                bib_entry = meta.get(e["key"], {})

                badges = []
                p_url, is_direct = paper_link(e, bib_entry)
                if is_direct:
                    badges.append(f"[P]({p_url})")
                else:
                    badges.append(f"[A]({p_url})")
                if e.get("code_url"):
                    badges.append(f"[C]({e['code_url']})")
                override = RESOURCE_OVERRIDES.get(e["key"], {})
                project_url = e.get("project_url") or override.get("project_url")
                dataset_url = e.get("dataset_url") or override.get("dataset_url")
                weights_url = e.get("weights_url") or override.get("weights_url")
                openreview_url = e.get("openreview_url") or override.get("openreview_url")
                tex_source_url = e.get("tex_source_url") or override.get("tex_source_url")
                if project_url:
                    badges.append(f"[PJ]({project_url})")
                if dataset_url:
                    badges.append(f"[D]({dataset_url})")
                if weights_url:
                    badges.append(f"[W]({weights_url})")
                if openreview_url:
                    badges.append(f"[OR]({openreview_url})")
                if tex_source_url:
                    badges.append(f"[T]({tex_source_url})")
                if e["in_bib"] == "yes" or e["key"] in bib:
                    badges.append("★")
                if e["benchmarked"] == "yes":
                    badges.append("⚗")
                if e.get("notes") and "DUPLICATE" in e["notes"].upper():
                    badges.append("⚠ dup")
                badge_str = " ".join(badges)
                summary = summary_sentences(e)

                lines.append(
                    f"| {title} | {authors} | {venue} | {year} | {badge_str} | {summary} |"
                )
            lines.append("")

        lines += ["---", ""]

    lines.append("_Auto-generated by `papers/sync.py`. "
                 "To add a paper: edit `papers.csv`, then run `python sync.py --build`._")

    AWESOME_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {AWESOME_MD}  ({total} entries, {today})")


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check",   action="store_true", help="coverage report (default)")
    parser.add_argument("--build",   action="store_true", help="regenerate awesome MD")
    parser.add_argument("--dupes",   action="store_true", help="find duplicate entries")
    parser.add_argument("--missing", action="store_true", help="list papers not in refs.bib")
    args = parser.parse_args()

    papers = load_papers()
    bib    = bib_keys()

    if args.build:
        cmd_build(papers)
    elif args.dupes:
        cmd_dupes(papers)
    elif args.missing:
        cmd_missing(papers)
    else:
        cmd_check(papers, bib)


if __name__ == "__main__":
    main()
