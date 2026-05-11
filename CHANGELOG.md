# Changelog

## 2026-05-11

### Code Agent Summary

Created the structural entropy survey repository scaffold and vendored a local
snapshot of `/workspace/glass-jax` into `code/glass-jax/` so the survey can ship
with reproducibility and benchmark support.

The snapshot source commit is:

```text
ab7d49d refactor the doc/, add doc for  integrating with tdmpc
```

The original active implementation remains `/workspace/glass-jax`. This project
copy is a survey companion snapshot, not the canonical development location.

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
- Use `code/glass-jax/` to support a representative reproducibility benchmark,
  not a full leaderboard claim.
- Decide whether the released library is described as a companion artifact,
  benchmark infrastructure, or independent software contribution.

