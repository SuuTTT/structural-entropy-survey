# TGINA Submission Todo

**Target:** Transactions on Graph Intelligence and Network Applications (TGINA)  
**Publisher:** Scilight Press — https://www.sciltp.com/journals/tgina  
**Submission portal:** https://sciflux.org/authors/submissions/add-submissions?journalCode=2052269951293444097  
**Relevant CFP deadline:** 31 July 2026 (Trustworthy Graph Intelligence for LLMs & Autonomous Agents)  
**No APC** (no article processing charge for all accepted papers)

---

## Phase 1 — Pre-writing (immediate)

- [ ] **Get official TGINA LaTeX template**
  - The journal is new; the template may not yet be public.
  - Email `info@sciltp.com` and ask for the LaTeX author template.
  - Until received, the current `paper/main.tex` uses a clean `article`-class
    12pt/A4 format with standard packages — acceptable for initial submission.

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

- [ ] **Add a `\section{Related Work}` section** comparing SE with:
  - Modularity-based methods (Louvain, Leiden)
  - Flow-based methods (Infomap)
  - Spectral methods (normalized cuts, spectral clustering)
  - Deep graph clustering (DiffPool, MinCutPool, DMoN)
  - This section is absent from the IJCAI conference version and is required
    for a full journal article.

- [ ] **Expand Introduction with a position statement**
  - Clarify SE's role within the broader graph intelligence landscape covered
    by TGINA's scope.
  - Add a paragraph on SE's relevance to LLMs / GraphRAG (relevant to the
    current TGINA CFP topic).

- [ ] **Add at least 2 new figures**
  - A proper taxonomy tree figure (currently shown as a fbox; replace with
    a TikZ `forest` diagram matching the IJCAI figure).
  - A benchmark result figure (bar chart or line plot from Section 6 results).

- [ ] **Expand the benchmark (Section 6)**
  - Add results on at least 2 real-world datasets (e.g., Cora, Citeseer,
    Amazon-Photo) to complement the synthetic SBM/Caveman results.
  - Report runtime/scalability comparison.

- [ ] **Add `\section{Discussion}` or expand existing discussions**
  - Each technical section currently ends with a Discussion paragraph;
    consolidate or expand these for journal depth.

- [ ] **Proofread and spell-check the full draft**
  - Run `aspell` or Grammarly on the compiled PDF.
  - Verify all `\cite{}` keys resolve correctly (`grep "?"` in the .log).

- [ ] **Update bibliography (`refs.bib`)**
  - Fix the bibtex warning: `can't use both volume and number fields in
    wang2023user`.
  - Add any papers published since the IJCAI camera-ready (up to
    submission date).

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
- [ ] At least one new section beyond the IJCAI version (Related Work ✓ planned)
- [ ] Benchmark with real-world datasets included
- [ ] All figures rendered properly in PDF
- [ ] Bibliography warnings resolved
- [ ] Supplementary materials prepared
- [ ] Submitted via https://sciflux.org before 31 July 2026
