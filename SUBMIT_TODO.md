# TGINA Submission Todo

**Target:** Transactions on Graph Intelligence and Network Applications (TGINA)  
**Manuscript status:** This is a TGINA journal survey. IJCAI 2025 is only the
prior conference version that must be disclosed and cited where required.  
**Publisher:** Scilight Press — https://www.sciltp.com/journals/tgina  
**Submission portal:** https://sciflux.org/authors/submissions/add-submissions?journalCode=2052269951293444097  
**Relevant CFP deadline:** 31 July 2026 (Trustworthy Graph Intelligence for LLMs & Autonomous Agents)  
**No APC** (no article processing charge for all accepted papers)

---

## Phase 1 — Pre-writing (immediate)

- [x] **Get official TGINA LaTeX template**
  - Template received at `/Users/suu/Downloads/TGINA-Template-LaTeX.zip`.
  - Archive contains `TGINA template.tex`, `scilight.bst`, journal header/logo
    images, and a compiled sample PDF.

- [ ] **Migrate the survey manuscript into the official TGINA template**
  - Copy the template assets into `paper/` or a dedicated `paper/tgina/`
    directory.
  - Adapt `paper/main.tex` to the TGINA front matter, page headers/footers,
    line-numbering, caption style, and `scilight.bst` bibliography style.
  - Preserve the disclosure that this TGINA submission expands the IJCAI 2025
    conference paper.
  - Compile a first TGINA-formatted PDF and inspect layout before content
    expansion.

- [x] **Install a local LaTeX toolchain and compile the current first draft**
  - Working compiler: `/Users/suu/Library/TinyTeX/bin/universal-darwin/pdflatex`.
  - Current article-format draft compiles to `paper/main.pdf`.
  - Compile log has no unresolved citations, undefined references, or oversized
    float warnings.

- [ ] **Check copyright of the IJCAI-2025 paper**
  - Determine who holds copyright (IJCAI / IJCAI Organization).
  - If IJCAI holds copyright, request written permission to reuse content in an
    expanded journal version.
  - Reference: IJCAI proceedings are published by the International Joint
    Conferences on Artificial Intelligence Organization.

- [ ] **Obtain co-author confirmation**
  - Confirm all four authors (Dingli Su, Hao Peng, Yicheng Pan, Angsheng Li)
    agree to submit to TGINA.
  - Confirm corresponding author: Yicheng Pan (`yichengp@buaa.edu.cn`).

---

## Phase 2 — Paper content expansion (before submission)

- [x] **Add a `\section{Related Work}` section** comparing SE with:
  - Modularity-based methods (Louvain, Leiden)
  - Flow-based methods (Infomap)
  - Spectral methods (normalized cuts, spectral clustering)
  - Deep graph clustering (DiffPool, MinCutPool, DMoN)
  - This section is absent from the IJCAI conference version and is required
    for a full journal article.

- [x] **Expand Introduction with a position statement**
  - Clarify SE's role within the broader graph intelligence landscape covered
    by TGINA's scope.
  - Add a paragraph on SE's relevance to LLMs / GraphRAG (relevant to the
    current TGINA CFP topic).

- [x] **Add at least 2 new figures**
  - A proper taxonomy tree figure (currently shown as a fbox; replace with
    a TikZ `forest` diagram matching the IJCAI figure).
  - A benchmark result figure (bar chart or line plot from Section 6 results).

- [x] **Expand the benchmark (Section 6)**
  - Add results on at least 2 real-world datasets (e.g., Cora, Citeseer,
    Amazon-Photo) to complement the synthetic SBM/Caveman results.
  - Report runtime/scalability comparison.

- [x] **Add `\section{Discussion}` or expand existing discussions**
  - Each technical section currently ends with a Discussion paragraph;
    consolidate or expand these for journal depth.

- [x] **Proofread and spell-check the full draft**
  - LaTeX log checked: no unresolved citations or undefined references.
  - Remaining language/layout pass should be repeated after TGINA template
    migration.

- [x] **Update bibliography (`refs.bib`)**
  - Fixed the bibtex warning for `wang2023user`.
  - Added missing related-work references used by the new journal section.
  - The literature tracker still lists pending uncited papers for the final
    pre-submission literature sweep.

---

## Phase 3 — Submission preparation

- [ ] **Write cover letter** (required by TGINA)
  - Disclose this is an expanded conference paper (IJCAI 2025).
  - Cite the original IJCAI paper in the cover letter.
  - State clearly what has been added/changed vs. the conference version
    (use the itemized list in `paper/sections/conclusion.tex`).
  - Include statement that copyright permission has been obtained (if applicable).
  - Mention alignment with the current CFP: "Trustworthy Graph Intelligence
    for Large Language Models and Autonomous Agents" (if submitting before
    31 July 2026).

- [ ] **Check first-page footnote / disclosure**
  - Ensure the journal paper's first page contains:
    *"This article is an expanded version of the conference paper
    'A Survey of Structural Entropy…', IJCAI 2025."*
  - Currently handled via `\date{}` in `main.tex` — move to a proper
    `\thanks{}` or footnote for the journal version.

- [ ] **Prepare author information**
  - ORCID iDs for all authors (required by most modern journals).
  - Current affiliations (all: Beihang University, Beijing, China).
  - Funding acknowledgments — already in `main.tex`.

- [ ] **Format compliance check**
  - Once the official TGINA template is received, reformat `main.tex`
    accordingly.
  - Typical journal requirements: 12pt, double-column or single-column,
    A4, line numbers for review, no author names in blind review.
  - Target length: ≥12 pages (to satisfy "size of a research article"
    requirement).  Current: **20 pages** ✓

- [ ] **Supplementary material (optional but recommended)**
  - Upload `glass-jax` library zip or link to GitHub repo as supplementary.
  - Include raw benchmark CSV data.

- [ ] **Register at Sciflux** (submission portal)
  - URL: https://sciflux.org — create an account if not already done.

---

## Phase 4 — Post-submission

- [ ] Monitor submission status at https://sciflux.org
- [ ] Respond to reviewer comments within 30 days (typical turnaround)
- [ ] Per CFP timeline (if submitted to the trustworthy AI special issue):
  - First review decision: **31 August 2026**
  - Final decision: **30 September 2026**
  - Expected publication: **15 October 2026**

---

## Key files

| File | Purpose |
|------|---------|
| `paper/main.tex` | Journal paper root LaTeX file |
| `paper/sections/*.tex` | Individual sections |
| `paper/refs.bib` | Full bibliography (copied from IJCAI camera-ready + self-cite) |
| `paper/main.pdf` | Compiled first draft (20 pages) |
| `SESurvey_IJCAI25__Camera_ready__250618.zip` | IJCAI conference version source |

---

## Submission checklist (final gate)

- [ ] All 4 authors have approved the final manuscript
- [ ] Copyright permission from IJCAI obtained (or confirmed not required)
- [ ] Cover letter written and disclosures included
- [ ] Official TGINA template applied (if available)
- [x] At least one new section beyond the IJCAI version (Related Work added)
- [x] Benchmark with real-world datasets included
- [x] All figures rendered properly in PDF
- [x] Bibliography warnings resolved
- [ ] Supplementary materials prepared
- [ ] Submitted via https://sciflux.org before 31 July 2026
