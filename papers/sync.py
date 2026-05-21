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


def compact_note(note: str, limit: int = 56) -> str:
    text = " ".join(note.split())
    if not text:
        return ""
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


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
    paper_links = 0
    code_links = 0
    project_links = 0
    dataset_links = 0
    weight_links = 0
    openreview_links = 0

    for p in papers:
        b = meta.get(p["key"], {})
        if paper_url(p, b):
            paper_links += 1
        if p.get("code_url"):
            code_links += 1
        if p.get("project_url"):
            project_links += 1
        if p.get("dataset_url"):
            dataset_links += 1
        if p.get("weights_url"):
            weight_links += 1
        if p.get("openreview_url"):
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
        "`[P]` paper/preprint · `[C]` code · `[PJ]` project page · "
        "`[D]` dataset · `[W]` weights · `[OR]` OpenReview · `[T]` TeX source · "
        "`★` in survey `refs.bib` · `⚗` benchmarked in this survey",
        "",
        f"**Resource Coverage**: papers `{paper_links}/{total}` · "
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
            lines.append("| Title | Authors | Venue | Year | Resources | Notes |")
            lines.append("|-------|---------|-------|------|-----------|-------|")

            for e in sorted(entries, key=lambda x: x["year"], reverse=True):
                title   = e["title"]
                authors = e["authors_short"]
                venue   = e["venue"]
                year    = e["year"]
                bib_entry = meta.get(e["key"], {})

                badges = []
                p_url = paper_url(e, bib_entry)
                if p_url:
                    badges.append(f"[P]({p_url})")
                if e.get("code_url"):
                    badges.append(f"[C]({e['code_url']})")
                if e.get("project_url"):
                    badges.append(f"[PJ]({e['project_url']})")
                if e.get("dataset_url"):
                    badges.append(f"[D]({e['dataset_url']})")
                if e.get("weights_url"):
                    badges.append(f"[W]({e['weights_url']})")
                if e.get("openreview_url"):
                    badges.append(f"[OR]({e['openreview_url']})")
                if e.get("tex_source_url"):
                    badges.append(f"[T]({e['tex_source_url']})")
                if e["in_bib"] == "yes" or e["key"] in bib:
                    badges.append("★")
                if e["benchmarked"] == "yes":
                    badges.append("⚗")
                if e.get("notes") and "DUPLICATE" in e["notes"].upper():
                    badges.append("⚠ dup")
                badge_str = " ".join(badges)
                note_str = compact_note(e.get("notes", ""))

                lines.append(
                    f"| {title} | {authors} | {venue} | {year} | {badge_str} | {note_str} |"
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
