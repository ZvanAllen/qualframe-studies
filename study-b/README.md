# Study B: models against expert annotation

Study B compares four current models with expert human annotation of behaviour change techniques (BCTs) in published intervention reports.

## Material

Published smoking-cessation intervention reports from the Human Behaviour-Change Project (HBCP) corpus, with HBCP's expert BCT annotations as the reference. There is no participant data. [`cohorts.csv`](cohorts.csv) lists every paper and its cohort flags:

- **Presence cohort, 95 papers:** every paper with at least one annotation. Etter (2004) and Myles (1996) have none and are excluded.
- **Passage cohort, 20 papers:** papers whose text is complete and in which at least 90% of the annotated quotations can be located exactly, after normalizing whitespace and quotation marks. Only these papers are used for passage-level agreement.
- **Pilot, 5 papers:** drawn from the passage cohort.

Two annotations for Burke (1994) point to a different report (ICRF 1993). They are kept and flagged, so they can be left out in a sensitivity analysis.

## Codebook

[`codebook/bct_hbcp94_codebook.yaml`](codebook/bct_hbcp94_codebook.yaml): the 94 techniques used in HBCP annotation, including 4.5, with BCT Ontology definitions, under 16 taxonomy groups. Groups are parents only and are never coded, so every agreement measure uses the 94 techniques.

## Design

**Pilot (5 papers, Claude Haiku 5.5 and GPT-6 Luna).** Two decision styles × three codebook splits, chosen before the full study:

| Condition | Decision style | Codebook split | Requests per paper |
|---|---|---|---|
| [`find-passages-full-codebook`](pilot/find-passages-full-codebook/) | Find passages | Whole codebook | 1 |
| [`find-passages-five-parts`](pilot/find-passages-five-parts/) | Find passages | Five parts | 5 |
| [`find-passages-sixteen-groups`](pilot/find-passages-sixteen-groups/) | Find passages | One per group | 16 |
| [`decide-each-code-full-codebook`](pilot/decide-each-code-full-codebook/) | Decide each code | Whole codebook | 1 |
| [`decide-each-code-five-parts`](pilot/decide-each-code-five-parts/) | Decide each code | Five parts | 5 |
| [`decide-each-code-sixteen-groups`](pilot/decide-each-code-sixteen-groups/) | Decide each code | One per group | 16 |

**Full study (95 papers).** The chosen condition, decide each code with the whole codebook ([`full/method.yaml`](full/method.yaml)), run once per model, cheapest first:

| Model | Settings |
|---|---|
| Claude Haiku 5.5 | maximum output 64,000 tokens |
| GPT-6 Luna | provider preset |
| GPT-6.1 Sol | provider preset |
| Claude Sonnet 5.5 | maximum output 64,000 tokens |

## Measures

Each run is compared with the HBCP reference in QualBench: technique presence per paper (F1, kappa, MCC, balanced accuracy, with document-level bootstrap intervals), passage agreement in the passage cohort, agreement between models, requests with no decision, cost and time. Unanchored reference quotations still count for presence but not for passage agreement.

## Getting the inputs

The papers and expert annotations come from HBCP's public [Info-extract](https://github.com/HumanBehaviourChangeProject/Info-extract) repository (Apache 2.0). They are not copied here. One script downloads them, pinned to the commit the study used, and rebuilds the inputs:

```
python study-b/scripts/fetch_inputs.py
```

It needs only Python 3.10 or later and writes to `study-b/data/` (git-ignored):

- `texts/`: plain text of the 95 presence-cohort papers, built from the corpus JSON by joining text blocks and flattening table cells
- `reference_table.csv`: the 724 annotation rows (`Document`, `Code`, `Quotation`, `Note`) in QualFrame's reference format, taken from the April 2019 annotation snapshot

Each download and output is checked against the hashes in [`scripts/expected_sha256.json`](scripts/expected_sha256.json), so a successful run reproduces the study inputs byte for byte. Import the texts and the reference table into a QualFrame study, then apply a condition's `method.yaml` and the codebook.
