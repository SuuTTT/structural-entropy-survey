# Writing Model for `20 years of network community detection`

This file abstracts the paper into sentence-function templates we can reuse for the structural-entropy survey.

Status: provisional writing model based on one model paper. It is strong for rhetorical pacing, but it should later be cross-checked against two to four additional TGINA- or survey-style papers before we freeze our journal voice.

## Source

- Model paper: [20 years of network community detection](https://arxiv.org/abs/2208.00111)
- arXiv version used: `v2`, revised on August 2, 2022
- Journal reference: *Nature Physics* 18, 848-850 (2022)
- Analysis artifact: [model-paper.md](./model-paper.md)

## Paper Type

Short field commentary / survey-style perspective.

## Global Writing Model

1. `FIELD_CONTEXT`
2. `KEY_OBJECT_DEFINITION`
3. `HISTORICAL_ANCHOR`
4. `METHOD_TAXONOMY`
5. `CORE_TENSION_OR_LIMITATION`
6. `EVALUATION_LOGIC`
7. `SCOPE_EXPANSION`
8. `OUTLOOK`

## Section Models

## Abstract / Opening Summary

### Sentence-function order

1. `FIELD_CONTEXT`
2. `PROBLEM_DEFINITION`
3. `PURPOSE`

### Reusable sentence patterns

- `[Topic area] is a central problem in [broader field or application space].`
- `At a high level, [core concept] concerns [plain-language definition].`
- `This survey reviews [time span / scope] of progress in [subfield].`

## Introduction

### Sentence-function order

1. `FIELD_IMPORTANCE`
2. `DOMAIN_SPREAD`
3. `KEY_CONCEPT`
4. `HISTORICAL_ANCHOR`
5. `REVIEW_SCOPE`

### Reusable sentence patterns

- `[Scientific object] appears in [domain 1], [domain 2], and [domain 3].`
- `A prominent feature of these systems is [structural property], which captures [plain-language meaning].`
- `Interest in this topic accelerated after [landmark line of work], and the literature has since expanded along several fronts.`
- `Here we review [scope], focusing on [axes of organization].`

## Method Taxonomy Section

### Sentence-function order

1. `TASK_DIFFICULTY`
2. `WHY_MULTIPLE_FAMILIES_EXIST`
3. `FAMILY_1_MECHANISM`
4. `FAMILY_2_MECHANISM`
5. `FAMILY_3_MECHANISM`
6. `COMPARATIVE_NOTE`

### Reusable sentence patterns

- `[Task] is challenging partly because [core ambiguity or under-specification].`
- `As a result, the literature has developed several major families of methods.`
- `One line of work treats [object] as [optimization / coding / inference target] and solves [core subproblem].`
- `A second line interprets [structure] through [probabilistic / dynamical / learning-based lens].`
- `A third line focuses on [alternative mechanism], where [key intuition].`
- `These families often pursue similar goals but differ in [assumptions, scalability, supervision, or interpretability].`

## Limitation / Tension Section

### Sentence-function order

1. `SUCCESS_WITH_CAVEAT`
2. `PRACTICAL_LIMITATION`
3. `CONCEPTUAL_LIMITATION`
4. `NAMED_FAILURE_MODE`
5. `MITIGATION`
6. `ALTERNATIVE_DIRECTION`

### Reusable sentence patterns

- `Although these methods are effective, they often rely on [assumption or computational setting].`
- `This can be problematic when [practical condition].`
- `More fundamentally, [conceptual mismatch or undesirable implication].`
- `A representative example is [named limitation], which shows that [specific issue].`
- `Several strategies have been proposed to alleviate this issue, including [strategy 1] and [strategy 2].`
- `Another direction is to replace the global formulation with [local / hierarchical / adaptive alternative].`

## Evaluation Section

### Sentence-function order

1. `EVALUATION_NEED`
2. `STANDARD_BENCHMARK`
3. `BENCHMARK_LIMITATION`
4. `IMPROVED_PROTOCOL`
5. `METRIC_CHOICE`
6. `FAILURE_REGIME`
7. `REAL_WORLD_CAVEAT`

### Reusable sentence patterns

- `Given the diversity of methods, evaluation design becomes a central question.`
- `A common strategy is to test algorithms on [synthetic or benchmark setting] with known planted structure.`
- `However, these benchmarks may not fully reflect [important property of real data].`
- `To address this mismatch, later work introduced [better benchmark or protocol].`
- `Performance is typically summarized using [metric family].`
- `An important observation is that methods can fail in [weak-signal / noisy / distribution-shift regime] even when some structure remains present.`
- `Evaluation on real data is therefore appealing, although ground truth is often incomplete or indirect.`

## Scope Expansion Section

### Sentence-function order

1. `CLASSIC_FORMULATION`
2. `MOTIVATION_TO_EXPAND`
3. `VARIANT_A`
4. `VARIANT_B`
5. `VARIANT_C`
6. `NEIGHBORING_PARADIGM`
7. `UNIFYING_LINK`

### Reusable sentence patterns

- `The classic formulation focuses on [base task], but many real systems exhibit richer structure.`
- `This has motivated extensions toward [family of variants].`
- `[Variant A] captures [what it adds].`
- `[Variant B] allows [new capability].`
- `[Variant C] focuses on [another structural pattern].`
- `Related work on [neighboring paradigm] addresses similar questions from a different technical angle.`
- `Taken together, these directions broaden the field beyond the original discrete setting.`

## Outlook Section

### Sentence-function order

1. `ACTIVE_RESEARCH_STATUS`
2. `ALGORITHM_FRONTIER`
3. `THEORY_FRONTIER`
4. `MODEL_OR_BENCHMARK_FRONTIER`
5. `INFORMATION_OR_MEASUREMENT_FRONTIER`
6. `APPLICATION_BREADTH`

### Reusable sentence patterns

- `[Field] remains an active area of research.`
- `Current work continues to improve [accuracy, scalability, guarantees, or robustness].`
- `On the theoretical side, important questions remain about [limits, identifiability, approximation, or detectability].`
- `There is also a need for better [benchmarks, datasets, or generative models] that reflect realistic structure.`
- `Information-theoretic measures are likely to remain important for [comparison, explanation, or model selection].`
- `At the same time, applications across [domains] continue to expand the field's practical relevance.`

## Draft Transfer To Structural-Entropy Survey

## Proposed section sequence

1. `FIELD_CONTEXT`
2. `SE_DEFINITION_AND_HISTORICAL_ROOTS`
3. `MAIN_METHOD_FAMILIES`
4. `GLOBAL_VS_LOCAL_AND_DISCRETE_VS_DIFFERENTIABLE_TENSIONS`
5. `BENCHMARKS_AND_REPRODUCIBILITY`
6. `EXTENSIONS_AND_NEIGHBORING_PARADIGMS`
7. `OUTLOOK`

## Claims That Need Evidence In Our Own Paper

- exact counts of SE papers by category
- chronological claims about first use in each application area
- benchmark trends across datasets and metrics
- any statement that SE consistently outperforms modularity, SBM, InfoMap, or GNN baselines
- any claim about theoretical guarantees for differentiable SE objectives

## Integrity Notes

- Reuse the rhetorical jobs of the sentences, not the original wording.
- Keep explicit source attribution for factual metadata about the model paper.
- Mark unsupported survey claims as `NEEDS_EVIDENCE` in future drafts.
