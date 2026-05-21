# Resource Schema

Use these fields when building or extending a paper tracker.

## Core Identity

- `key`
- `title`
- `authors_short`
- `authors_full`
- `year`
- `venue`
- `venue_type`
- `status` (`published`, `accepted`, `preprint`, `under_review`)
- `doi`
- `arxiv_id`
- `openreview_id`

## Resource Links

- `paper_url`
- `pdf_url`
- `bibtex`
- `code_url`
- `dataset_url`
- `weights_url`
- `project_page`
- `blog_or_demo`
- `social_url`
- `openreview_url`
- `tex_source_url`

## Survey Classification

- `category`
- `subcategory`
- `problem`
- `method_family`
- `task`
- `domain`

## Reproduction Notes

- `main_hypothesis`
- `method_summary`
- `datasets`
- `metrics`
- `baselines`
- `main_results`
- `implementation_notes`
- `release_status`

## Missing Data Convention

If a field was checked and not found, write `missing` in notes or the local schema's equivalent field. Do not silently omit the search effort.
