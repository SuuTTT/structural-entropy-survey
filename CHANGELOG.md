# Changelog

## 2026-05-11

### Code Agent Summary

Created the structural entropy survey repository scaffold. Initially a full
`glass-jax` copy was vendored, then it was replaced with a clean curated subset
for survey reproducibility and benchmark support.

The snapshot source commit is:

```text
ab7d49d refactor the doc/, add doc for  integrating with tdmpc
```

The current subset is:

- objective implementations,
- SEClust utilities needed by representative benchmarks,
- spectral solver support,
- same-protocol and differentiable benchmark scripts,
- selected design/math/LSEnet/result-summary docs.

The original active implementation remains `/workspace/glass-jax`. This project
copy is a survey companion subset, not the canonical development location.

### Current Scope

This project should frame the journal survey as:

```text
Ten years of structural entropy: theory, algorithms, learning, dynamics, and
reproducibility.
```

The IJCAI survey should be placed under `docs/ijcai_survey/`, while the journal
extension should live under `docs/journal_extension/`.

### TODO

- Add the existing IJCAI survey source/PDF/reviews to `docs/ijcai_survey/`.
- Write `docs/journal_extension/delta_from_ijcai.md`.
- Build a taxonomy table covering objective type, data type, optimizer,
  supervision setting, and evaluation protocol.
- Use `code/survey_support/` to support a representative reproducibility
  benchmark, not a full leaderboard claim.
- Decide whether the released library is described as a companion artifact,
  benchmark infrastructure, or independent software contribution.
