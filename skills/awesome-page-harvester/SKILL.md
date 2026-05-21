---
name: awesome-page-harvester
description: Build or update a detailed awesome page and survey tracker for a research topic. Use when the user wants structured literature curation, resource harvesting, BibTeX collection, reproducibility notes, or survey-ready per-paper summaries covering papers, code, datasets, weights, project pages, blogs, social links, OpenReview feedback, and source files.
---

# Awesome Page Harvester

Use this skill when the task is not just "find papers" but to turn a topic into a maintained research asset: an awesome page, survey tracker, paper table, or reproduction-oriented bibliography.

## Goals

For each paper, collect and normalize:

- canonical title, authors, venue, year, DOI/arXiv/OpenReview ids
- BibTeX
- paper URL and PDF/preprint URL
- code repository
- dataset links
- model weights or checkpoints
- project page, blog post, demo page
- social links if they materially help discovery or provenance
- OpenReview discussion or rebuttal links when available
- TeX/Overleaf/author source when publicly available

Also extract survey-useful content:

- main hypothesis
- method summary
- task setting
- datasets and metrics
- strongest comparison baselines
- experiment table details useful for reproduction
- implementation clues: training setup, hardware, seeds, hyperparameters, ablations, release status

## Default Workflow

1. Resolve the source of truth.
   - Prefer an existing `papers.csv`, spreadsheet, or BibTeX file if the repo already has one.
   - Do not invent a parallel tracker if a local one already exists.

2. Establish the canonical citation first.
   - Prefer official conference/journal pages, arXiv, OpenReview, DBLP, ACL Anthology, IEEE, ACM, Springer, Elsevier, or publisher DOI pages.
   - If multiple titles exist, use the final published title when available; otherwise use the most recent preprint title and mark it as preprint.

3. Harvest resources in priority order.
   - Official paper page
   - arXiv/OpenReview
   - official code repo
   - author project page
   - dataset page
   - model card or weights page
   - blog/demo/social posts only after canonical sources are captured

4. Extract reproducibility details.
   - Read abstract, method, experiment, and appendix sections if available.
   - Capture exact benchmark names, metrics, baselines, and implementation notes.
   - If a table is central to reproduction, summarize it in structured text instead of copying raw PDF formatting.

5. Update the local artifacts.
   - Tracker CSV or sheet
   - `refs.bib`
   - awesome page markdown
   - survey notes or per-paper summaries if requested

6. Verify before finishing.
   - no broken citation keys
   - no placeholder `TBD` metadata if the source was available
   - no claims about code/datasets/weights without a source

## Resource Checklist

For each paper, explicitly check:

- `paper`
- `bibtex`
- `code`
- `dataset`
- `weights`
- `project_page`
- `blog_or_demo`
- `social`
- `openreview`
- `tex_source`

If something is not found, record `missing` rather than leaving the field ambiguous.

## Output Shape

When the repo does not already define a schema, use the templates in:

- `references/resource-schema.md`
- `references/extraction-template.md`

Prefer compact structured fields over prose blobs.

## Evidence Rules

- Prefer primary sources.
- Use exact dates for preprints, conference versions, and journal versions when that distinction matters.
- Distinguish clearly between published, accepted, under review, and preprint.
- Do not mark code, weights, or datasets as available unless you found a direct source.
- If authorship or venue conflicts across sources, note the conflict and keep the most authoritative source.

## Awesome Page Guidance

- Group entries by category and subcategory that help a survey reader scan the field.
- Include the strongest resource links directly in the awesome page.
- Keep the awesome page readable; move dense reproduction notes to a tracker or appendix file if needed.
- Regenerate from source tables when the repo already has a build script instead of hand-editing generated markdown.

## Reproduction Extraction Guidance

For empirical papers, try to capture:

- benchmark datasets
- train/val/test protocol
- metrics
- baselines
- model size or backbone
- key losses or optimization tricks
- training budget or hardware
- release status of code and checkpoints

Summarize the main experimental table in plain structured text. Do not paste large copyrighted tables verbatim.

## References

- For field names and normalization rules, read `references/resource-schema.md`.
- For per-paper extraction format, read `references/extraction-template.md`.
