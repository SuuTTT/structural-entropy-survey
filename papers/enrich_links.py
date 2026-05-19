#!/usr/bin/env python3
"""
papers/enrich_links.py  —  fetch code / project-page / resource URLs for papers.

Sources tried per paper (in priority order):
  1. Papers With Code API   https://paperswithcode.com/api/v1/papers/?q=...
  2. arXiv abstract page    https://arxiv.org/abs/{arxiv_id}  (regex for GitHub)
  3. Semantic Scholar API   https://api.semanticscholar.org/graph/v1/paper/search

Updates papers.csv:  code_url, arxiv_id (if missing).
Then run  python3 sync.py --build  to regenerate awesome-structural-entropy.md.

Usage:
    python3 enrich_links.py                     # all papers with empty code_url
    python3 enrich_links.py --key huang2024sec  # single paper
    python3 enrich_links.py --missing-only      # only in_bib=no papers
    python3 enrich_links.py --dry-run           # print findings, no writes
    python3 enrich_links.py --force             # re-check even if code_url set
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

SLEEP_S   = 1.2   # seconds between API calls (be polite)
UA        = "se-survey-enricher/1.0 (research; contact via GitHub)"

# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _http_get_text(url: str, params: dict | None = None, extra_headers: dict | None = None) -> str | None:
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": UA}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        if e.code not in (404, 429):
            print(f"    [warn] HTTP {e.code}: {url[:80]}")
    except Exception as e:
        print(f"    [warn] {type(e).__name__}: {url[:80]}")
    return None


def _http_get_json(url: str, params: dict | None = None, extra_headers: dict | None = None) -> dict | list | None:
    raw = _http_get_text(url, params, extra_headers)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


# ── source: Papers With Code ──────────────────────────────────────────────────

def _pwc_search(title: str, year: str) -> dict:
    """Return dict with code_url, project_url, dataset_urls (any found)."""
    data = _http_get_json(
        "https://paperswithcode.com/api/v1/papers/",
        params={"q": title[:120], "items_per_page": 3},
    )
    time.sleep(SLEEP_S)
    if not data or not data.get("results"):
        return {}

    title_words = set(re.sub(r"[^a-z0-9 ]", "", title.lower()).split())
    for hit in data["results"]:
        hit_title = hit.get("title", "")
        hit_words = set(re.sub(r"[^a-z0-9 ]", "", hit_title.lower()).split())
        overlap = len(title_words & hit_words) / max(len(title_words), 1)
        if overlap < 0.45:
            continue

        out: dict = {}
        repo = hit.get("repository")
        if repo and repo.get("url"):
            out["code_url"] = _clean_github_url(repo["url"])
        proj = hit.get("project_page") or hit.get("url_abs")
        if proj and proj.startswith("http"):
            out["project_url"] = proj
        return out
    return {}


# ── source: arXiv abstract page ───────────────────────────────────────────────

_GH_PATTERN = re.compile(
    r'https?://github\.com/([\w\-]+/[\w\-\.]+?)(?:\.git)?(?=["\s<>)\]]|$)'
)


def _clean_github_url(url: str) -> str:
    url = url.rstrip("/")
    url = re.sub(r"\.git$", "", url)
    return url


def _arxiv_github_links(arxiv_id: str) -> list[str]:
    html = _http_get_text(f"https://arxiv.org/abs/{arxiv_id}")
    time.sleep(SLEEP_S)
    if not html:
        return []
    links: list[str] = []
    seen: set[str] = set()
    for m in _GH_PATTERN.finditer(html):
        clean = f"https://github.com/{m.group(1)}"
        parts = clean.split("/")
        # must be github.com/owner/repo — no deeper paths
        if len(parts) != 5:
            continue
        # skip common false positives
        if any(s in clean.lower() for s in ("shields.io", "actions/", "badge")):
            continue
        if clean not in seen:
            seen.add(clean)
            links.append(clean)
    return links


# ── source: Semantic Scholar ──────────────────────────────────────────────────

def _s2_search(title: str, year: str) -> dict:
    data = _http_get_json(
        "https://api.semanticscholar.org/graph/v1/paper/search",
        params={
            "query": title[:120],
            "fields": "title,year,openAccessPdf,externalIds,publicationTypes",
            "limit": 3,
        },
    )
    time.sleep(SLEEP_S)
    if not data or not data.get("data"):
        return {}

    title_words = set(re.sub(r"[^a-z0-9 ]", "", title.lower()).split())
    for hit in data["data"]:
        hit_words = set(re.sub(r"[^a-z0-9 ]", "", hit.get("title", "").lower()).split())
        overlap = len(title_words & hit_words) / max(len(title_words), 1)
        if overlap < 0.5:
            continue
        if year and hit.get("year") and abs(int(hit["year"]) - int(year)) > 2:
            continue

        out: dict = {}
        ext = hit.get("externalIds") or {}

        # arXiv ID (useful if papers.csv is missing it)
        if ext.get("ArXiv"):
            out["arxiv_id"] = ext["ArXiv"]
        # ACL Anthology link as project_url
        if ext.get("ACL"):
            out["project_url"] = f"https://aclanthology.org/{ext['ACL']}"
        # Open-access PDF
        if hit.get("openAccessPdf") and hit["openAccessPdf"].get("url"):
            out["pdf_url"] = hit["openAccessPdf"]["url"]
        return out
    return {}


# ── CSV helpers ───────────────────────────────────────────────────────────────

def load_papers() -> tuple[list[dict], list[str]]:
    with open(PAPERS_CSV, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cols = list(reader.fieldnames) if reader.fieldnames else list(rows[0].keys())
    return rows, cols


def save_papers(papers: list[dict], cols: list[str]) -> None:
    with open(PAPERS_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for row in papers:
            w.writerow(row)


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--key",          help="enrich a single paper by key")
    parser.add_argument("--missing-only", action="store_true",
                        help="only process papers with in_bib=no")
    parser.add_argument("--dry-run",      action="store_true",
                        help="print results without writing to papers.csv")
    parser.add_argument("--force",        action="store_true",
                        help="re-query even if code_url is already set")
    args = parser.parse_args()

    papers, cols = load_papers()

    # build index for O(1) lookup
    idx_by_key = {p["key"]: i for i, p in enumerate(papers)}

    targets = papers
    if args.key:
        targets = [p for p in papers if p["key"] == args.key]
        if not targets:
            print(f"Key not found: {args.key}")
            return
    if args.missing_only:
        targets = [p for p in targets if p.get("in_bib") == "no"]

    if not args.force:
        targets = [p for p in targets if not p.get("code_url", "").strip()]

    if not targets:
        print("Nothing to enrich (all targeted papers already have code_url).")
        print("Use --force to re-query anyway.")
        return

    print(f"Enriching {len(targets)} papers …\n")
    changed = 0

    for p in targets:
        key      = p["key"]
        title    = p["title"]
        year     = p.get("year", "")
        arxiv_id = p.get("arxiv_id", "").strip()

        print(f"→ {key}  ({year})  {title[:65]}")
        found: dict = {}

        # --- 1. Papers With Code ---
        pwc = _pwc_search(title, year)
        if pwc:
            print(f"   [PwC]   {pwc}")
            found.update(pwc)

        # --- 2. arXiv page (if arxiv_id known) ---
        if arxiv_id and not found.get("code_url"):
            gh_links = _arxiv_github_links(arxiv_id)
            if gh_links:
                print(f"   [arXiv] GitHub: {gh_links[0]}")
                found["code_url"] = gh_links[0]

        # --- 3. Semantic Scholar ---
        s2 = _s2_search(title, year)
        if s2:
            if "arxiv_id" not in found:
                found.update({k: v for k, v in s2.items()
                               if k == "arxiv_id" and not arxiv_id})
            print(f"   [S2]    {s2}")
            if "project_url" in s2 and "project_url" not in found:
                found["project_url"] = s2["project_url"]

        # --- apply findings ---
        if found:
            i = idx_by_key[key]
            updates: list[str] = []

            if found.get("code_url") and not papers[i].get("code_url"):
                if not args.dry_run:
                    papers[i]["code_url"] = found["code_url"]
                updates.append(f"code_url={found['code_url'][:60]}")

            if found.get("arxiv_id") and not papers[i].get("arxiv_id"):
                if not args.dry_run:
                    papers[i]["arxiv_id"] = found["arxiv_id"]
                updates.append(f"arxiv_id={found['arxiv_id']}")

            if updates:
                changed += 1
                tag = "[dry-run] would set" if args.dry_run else "✓"
                print(f"   {tag}: {', '.join(updates)}")
        else:
            print("   — no links found")

        print()

    if not args.dry_run and changed:
        save_papers(papers, cols)
        print(f"Updated {changed} papers in papers.csv.")
        print("Next: python3 sync.py --build  (rebuild awesome MD)")
    elif args.dry_run:
        print(f"[dry-run] Would update {changed} papers.")
    else:
        print("No new links found.")


if __name__ == "__main__":
    main()
