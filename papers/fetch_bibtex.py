#!/usr/bin/env python3
"""
papers/fetch_bibtex.py  —  auto-fetch BibTeX for in_bib=no papers and append
to paper/refs.bib.

Sources tried per paper (in priority order):
  1. DBLP search API   https://dblp.org/search/publ/api?q=...&format=bib
  2. arXiv API         http://export.arxiv.org/api/query?id_list={arxiv_id}
  3. Semantic Scholar  https://api.semanticscholar.org/graph/v1/paper/search
     (metadata only → constructs BibTeX locally)

After fetching the entry the script:
  • Rewrites the BibTeX key to match the key in papers.csv
  • Appends the entry to paper/refs.bib  (skip if key already present)
  • Marks in_bib=yes in papers.csv

Usage:
    python3 fetch_bibtex.py                     # all in_bib=no papers
    python3 fetch_bibtex.py --key huang2024sec  # single paper
    python3 fetch_bibtex.py --dry-run           # print BibTeX without writing
    python3 fetch_bibtex.py --skip-tbd          # skip placeholder (TBD) keys
"""

import argparse
import csv
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT       = Path(__file__).parent
PAPERS_CSV = ROOT / "papers.csv"
REFS_BIB   = ROOT.parent / "paper" / "refs.bib"

SLEEP_S = 1.5
UA      = "se-survey-bibtex-fetcher/1.0 (research; contact via GitHub)"

# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _get_text(url: str, params: dict | None = None) -> str | None:
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        if e.code not in (404,):
            print(f"    [warn] HTTP {e.code}: {url[:80]}")
    except Exception as e:
        print(f"    [warn] {type(e).__name__}: {url[:80]}")
    return None


def _get_json(url: str, params: dict | None = None) -> dict | list | None:
    raw = _get_text(url, params)
    if raw:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass
    return None


# ── BibTeX key rewriter ───────────────────────────────────────────────────────

def rekey_bib_entry(bib: str, new_key: str) -> str:
    """Replace the BibTeX entry key with new_key."""
    return re.sub(
        r"(@\w+\{)\s*[\w:\-/]+\s*,",
        lambda m: f"{m.group(1)}{new_key},",
        bib.strip(),
        count=1,
    )


def existing_keys(refs_path: Path) -> set[str]:
    text = refs_path.read_text(encoding="utf-8")
    return set(re.findall(r"@\w+\{(\w[\w\-]*),", text))


# ── source 1: DBLP ───────────────────────────────────────────────────────────

def fetch_dblp(title: str, authors_short: str = "", year: str = "") -> str | None:
    """
    Query DBLP and return a single raw BibTeX entry, or None.
    We ask for up to 5 hits and pick the one whose year matches best.
    """
    # Strip special chars that confuse DBLP and keep first 8 keywords
    clean_title = re.sub(r"[^\w\s]", " ", title)
    title_words = clean_title.split()[:8]

    query_parts = title_words[:]
    if authors_short and authors_short not in ("TBD", ""):
        # first author surname: first capitalised word before "et al." or ","
        first_chunk = re.split(r"[,&]", authors_short)[0].strip()
        # remove "et al." / "et al" / "etal" suffix
        first_chunk = re.sub(r"\bet\.?\s*al\.?\b.*", "", first_chunk, flags=re.I).strip()
        # first word is the surname (e.g. "Huang")
        first = first_chunk.split()[0] if first_chunk else ""
        if first:
            query_parts.append(first)
    if year:
        query_parts.append(year)

    raw = _get_text(
        "https://dblp.org/search/publ/api",
        params={"q": " ".join(query_parts), "h": 5, "format": "bib"},
    )
    time.sleep(SLEEP_S)
    if not raw or "@" not in raw:
        return None

    entries = re.findall(r"@\w+\{[^@]+\}", raw, re.DOTALL)
    if not entries:
        return None

    # Prefer the entry whose year matches
    if year:
        for e in entries:
            if f"year = {{{year}" in e or f"year={{{year}" in e:
                return e.strip()

    return entries[0].strip()


# ── source 2: arXiv API ───────────────────────────────────────────────────────

def fetch_arxiv(arxiv_id: str) -> str | None:
    """Fetch metadata from arXiv Atom API and construct a BibTeX @article."""
    raw = _get_text(
        "http://export.arxiv.org/api/query",
        params={"id_list": arxiv_id, "max_results": 1},
    )
    time.sleep(SLEEP_S)
    if not raw:
        return None

    # Strip namespace for simpler regex
    raw = raw.replace(' xmlns="http://www.w3.org/2005/Atom"', "")

    title_m   = re.search(r"<title>(.*?)</title>",   raw, re.DOTALL)
    authors_m = re.findall(r"<name>(.*?)</name>",     raw, re.DOTALL)
    year_m    = re.search(r"<published>(\d{4})-(\d{2})", raw)

    if not title_m or not authors_m:
        return None

    raw_title = title_m.group(1).strip()
    if raw_title.lower().startswith("arxiv query"):
        return None  # API returned the feed title, not a paper title

    title_clean = re.sub(r"\s+", " ", raw_title)
    authors_str = " and ".join(a.strip() for a in authors_m)
    year        = year_m.group(1) if year_m else "2025"
    month       = year_m.group(2) if year_m else ""

    # Derive a candidate key (will be overwritten by caller)
    surname   = authors_m[0].strip().split()[-1].lower()
    word1     = re.sub(r"[^a-z]", "", title_clean.lower().split()[0])[:8]
    draft_key = f"{surname}{year}{word1}"

    lines = [
        f"@article{{{draft_key},",
        f"  title     = {{{{{title_clean}}}}},",
        f"  author    = {{{{{authors_str}}}}},",
        f"  year      = {{{year}}},",
    ]
    if month:
        lines.append(f"  month     = {{{month}}},")
    lines += [
        f"  journal   = {{arXiv preprint arXiv:{arxiv_id}}},",
        f"  eprint    = {{{arxiv_id}}},",
        f"  archivePrefix = {{arXiv}},",
        "}",
    ]
    return "\n".join(lines)


# ── source 3: Semantic Scholar (metadata → construct BibTeX) ─────────────────

def fetch_s2(title: str, year: str) -> str | None:
    """Search Semantic Scholar and construct a BibTeX entry from metadata."""
    data = _get_json(
        "https://api.semanticscholar.org/graph/v1/paper/search",
        params={
            "query": title[:120],
            "fields": "title,authors,year,venue,publicationVenue,externalIds,journal",
            "limit": 5,
        },
    )
    time.sleep(SLEEP_S)
    if not data or not data.get("data"):
        return None

    title_words = set(re.sub(r"[^a-z0-9 ]", "", title.lower()).split())
    for hit in data["data"]:
        hit_words = set(re.sub(r"[^a-z0-9 ]", "", hit.get("title", "").lower()).split())
        overlap   = len(title_words & hit_words) / max(len(title_words), 1)
        if overlap < 0.55:
            continue
        hit_year = hit.get("year")
        if year and hit_year and abs(int(hit_year) - int(year)) > 2:
            continue

        authors = hit.get("authors") or []
        author_str = " and ".join(
            a.get("name", "Unknown") for a in authors
        )
        title_s2  = hit.get("title", title)
        year_s2   = str(hit.get("year") or year)
        venue     = hit.get("venue", "")

        ext     = hit.get("externalIds") or {}
        arxiv   = ext.get("ArXiv", "")
        doi     = ext.get("DOI", "")
        acl     = ext.get("ACL", "")

        # Decide entry type heuristically
        venue_lc = venue.lower()
        if any(t in venue_lc for t in ("conf", "proceedings", "workshop",
                                        "symposium", "icml", "neurips", "aaai",
                                        "iclr", "acl", "emnlp", "cvpr", "iccv")):
            entry_type  = "inproceedings"
            venue_field = "booktitle"
        else:
            entry_type  = "article"
            venue_field = "journal"

        # Draft key (will be overwritten by caller)
        surname   = (authors[0].get("name", "unknown").split()[-1].lower()
                     if authors else "unknown")
        word1     = re.sub(r"[^a-z]", "", title_s2.lower().split()[0])[:8]
        draft_key = f"{surname}{year_s2}{word1}"

        lines = [
            f"@{entry_type}{{{draft_key},",
            f"  title     = {{{{{title_s2}}}}},",
            f"  author    = {{{{{author_str}}}}},",
            f"  year      = {{{year_s2}}},",
            f"  {venue_field} = {{{{{venue}}}}},",
        ]
        if doi:
            lines.append(f"  doi       = {{{doi}}},")
        if arxiv:
            lines.append(f"  eprint    = {{{arxiv}}},")
            lines.append(f"  archivePrefix = {{arXiv}},")
        if acl:
            lines.append(f"  note      = {{ACL Anthology: {acl}}},")
        lines.append("}")
        return "\n".join(lines)

    return None


# ── CSV helpers ───────────────────────────────────────────────────────────────

def load_papers() -> tuple[list[dict], list[str]]:
    with open(PAPERS_CSV, newline="") as f:
        reader = csv.DictReader(f)
        rows   = list(reader)
        cols   = list(reader.fieldnames) if reader.fieldnames else list(rows[0].keys())
    return rows, cols


def save_papers(papers: list[dict], cols: list[str]) -> None:
    with open(PAPERS_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for row in papers:
            w.writerow(row)


def append_bib(bib_entry: str, refs_path: Path) -> None:
    """Append a BibTeX entry to refs.bib with a blank-line separator."""
    current = refs_path.read_text(encoding="utf-8")
    sep     = "\n" if current.endswith("\n") else "\n\n"
    refs_path.write_text(current + sep + bib_entry + "\n", encoding="utf-8")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--key",       help="fetch BibTeX for a single paper key")
    parser.add_argument("--dry-run",   action="store_true",
                        help="print fetched BibTeX without writing to disk")
    parser.add_argument("--skip-tbd",  action="store_true",
                        help="skip papers whose key contains 'tbd' or authors_short is TBD")
    args = parser.parse_args()

    papers, cols  = load_papers()
    present_keys  = existing_keys(REFS_BIB)
    idx_by_key    = {p["key"]: i for i, p in enumerate(papers)}

    targets = [p for p in papers if p.get("in_bib") == "no"]

    if args.key:
        targets = [p for p in targets if p["key"] == args.key]
        if not targets:
            # Maybe it's already in bib — check
            match = next((p for p in papers if p["key"] == args.key), None)
            if match:
                print(f"Paper '{args.key}' already has in_bib={match['in_bib']}.")
            else:
                print(f"Key not found in papers.csv: {args.key}")
            return

    if args.skip_tbd:
        targets = [p for p in targets
                   if p.get("authors_short", "TBD") != "TBD"
                   and "tbd" not in p["key"].lower()]

    if not targets:
        print("No pending papers to fetch.")
        return

    print(f"Fetching BibTeX for {len(targets)} papers …\n")
    fetched = 0
    skipped = 0

    for p in targets:
        key         = p["key"]
        title       = p["title"]
        year        = p.get("year", "")
        authors_short = p.get("authors_short", "")
        arxiv_id    = p.get("arxiv_id", "").strip()

        print(f"→ {key}  ({year})  {title[:65]}")

        if key in present_keys:
            print(f"   [skip] key already in refs.bib\n")
            # Mark in_bib=yes if it was somehow missed
            if not args.dry_run:
                papers[idx_by_key[key]]["in_bib"] = "yes"
            skipped += 1
            continue

        bib: str | None = None

        # 1. DBLP  (best for published conference / journal papers)
        print(f"   [1/3] DBLP …", end=" ", flush=True)
        bib = fetch_dblp(title, authors_short, year)
        if bib:
            print("found")
        else:
            print("miss")

        # 2. arXiv API  (for preprints or when arxiv_id is available)
        if not bib and arxiv_id:
            print(f"   [2/3] arXiv ({arxiv_id}) …", end=" ", flush=True)
            bib = fetch_arxiv(arxiv_id)
            if bib:
                print("found")
            else:
                print("miss")

        # 3. Semantic Scholar  (fallback, constructs entry from metadata)
        if not bib:
            print(f"   [3/3] Semantic Scholar …", end=" ", flush=True)
            bib = fetch_s2(title, year)
            if bib:
                print("found")
            else:
                print("miss")

        if not bib:
            print(f"   ✗ Could not find BibTeX — add manually.\n")
            continue

        # Rewrite key to match papers.csv key
        bib = rekey_bib_entry(bib, key)

        if args.dry_run:
            print(f"\n   --- BibTeX (dry-run) ---\n{bib}\n   ---\n")
        else:
            append_bib(bib, REFS_BIB)
            papers[idx_by_key[key]]["in_bib"] = "yes"
            present_keys.add(key)  # avoid double-appending in same run
            fetched += 1
            print(f"   ✓ Appended to refs.bib  (in_bib → yes)\n")

    # Save updated papers.csv
    if not args.dry_run and (fetched + skipped) > 0:
        save_papers(papers, cols)
        print(f"Summary: {fetched} new entries appended, {skipped} already present.")
        print("Next steps:")
        print("  1. Review paper/refs.bib — check author names, titles, venue accuracy.")
        print("  2. python3 sync.py --check    # verify zero ghost / zero uncatalogued")
        print("  3. python3 sync.py --build    # rebuild awesome-structural-entropy.md")
    elif args.dry_run:
        print(f"[dry-run] Would fetch {fetched} entries.")


if __name__ == "__main__":
    main()
