# Study B: models against expert BCT annotation

Study B applies the same approach as Study A to a different framework with a human reference: it compares four current models with the Human Behaviour-Change Project's (HBCP) expert annotations of behaviour change techniques (BCTs) in published trial reports.

## Material

The open-access HBCP smoking-cessation corpus (OA-HBCP Corpus version 1.0): 97 published intervention reports with text. There is no participant data. [`cohorts.csv`](cohorts.csv) lists every report and its cohort flags:

- **Presence cohort, 95 reports:** every report with at least one BCT annotation. Etter (2004) and Myles (1996) have none and are excluded.
- **Passage cohort, 20 reports:** reports whose text is complete and in which at least 90% of the annotated phrases can be located, after normalizing whitespace and quotation marks.
- **Pilot, 5 reports:** drawn from the passage cohort.

## Reference

The annotations are the export `Smoking_AllAnnotations_01Apr19.json`: 703 coding records with 724 annotated phrases, combined across study arms. Every annotation counts towards presence whether or not its phrase could be located in the text. Two annotations for Burke (1994) point to a different report (ICRF 1993); they are kept and flagged.

The annotators' task and the models' task differ, so agreement is concordance with a historical reference whose scope only partly matches:

- The export does not record which BCTs were assessed for each report, so an unannotated unit is not a confirmed absence.
- The HBCP release prioritised 12 BCTs (1.1, 1.2, 1.4, 2.2, 2.3, 3.1, 4.1, 4.5, 5.1, 5.3, 11.1, 11.2), although the export also holds records for other BCTs.
- The annotation guidance excluded the Discussion and BCTs unrelated to the target behaviour. The models read the whole report and were asked about every BCT.

## Codebook

[`codebook/bct_hbcp94_codebook.yaml`](codebook/bct_hbcp94_codebook.yaml): the 94 codes used in HBCP annotation (the 93 BCTTv1 techniques plus 4.5 "Advise to change behaviour"), with definitions copied from the BCT Ontology, under 16 taxonomy groups. Groups are parents only and are never coded, so code-level measures use the 94 techniques and group-level measures merge codes into their groups. The codebook has no examples.

## Design

**Pilot (5 reports, Claude Haiku 5.5 and GPT-6 Luna).** Two instruction packages × three codebook divisions:

| Condition | Instruction package | Codebook per request | Requests per report |
|---|---|---|---|
| [`find-passages-full-codebook`](pilot/find-passages-full-codebook/) | Find passages | Whole codebook | 1 |
| [`find-passages-five-parts`](pilot/find-passages-five-parts/) | Find passages | Five parts | 5 |
| [`find-passages-sixteen-groups`](pilot/find-passages-sixteen-groups/) | Find passages | One per group | 16 |
| [`decide-each-code-full-codebook`](pilot/decide-each-code-full-codebook/) | Decide every code | Whole codebook | 1 |
| [`decide-each-code-five-parts`](pilot/decide-each-code-five-parts/) | Decide every code | Five parts | 5 |
| [`decide-each-code-sixteen-groups`](pilot/decide-each-code-sixteen-groups/) | Decide every code | One per group | 16 |

**Main study (95 reports, 8,930 report × BCT units).** Based on the pilot, all four models coded every report with "decide every code" and the whole codebook, one request per report ([`full/method.yaml`](full/method.yaml)). Runs went cheapest first:

| Model | Settings |
|---|---|
| Claude Haiku 5.5 | maximum output 64,000 tokens |
| GPT-6 Luna | QualFrame preset |
| GPT-6.1 Sol | QualFrame preset |
| Claude Sonnet 5.5 | maximum output 64,000 tokens |

Unannotated units are treated as negative reference labels. Two sensitivity analyses leave out the five pilot reports and restrict the comparison to the 12 prioritised BCTs (1,140 units).

## Measures

QualBench compares each model with the annotations, and the models with each other, at the report × BCT level and at taxonomy-group level (1,520 units). The measures are balanced accuracy and MCC (primary), sensitivity, specificity, precision, F1, kappa and the every-code-present and every-code-absent rules. The 95% intervals use 2,000 bootstrap replicates (seed 1) that resample whole reports. QualBench also reports quotation fidelity, passage agreement (in the passage cohort, any-overlap matching, since annotated phrases are short), cost and time.

## Getting the inputs

The reports and annotations come from HBCP's public [Info-extract](https://github.com/HumanBehaviourChangeProject/Info-extract) repository and are not copied here (licences in [NOTICE.md](../NOTICE.md)). One script downloads them, pinned to the commit the study used, and rebuilds the inputs:

```
python study-b/scripts/fetch_inputs.py
```

It needs only Python 3.10 or later and writes to `study-b/data/` (git-ignored):

- `texts/`: plain text of the 95 presence-cohort reports, built from the corpus JSON by joining text blocks and flattening table cells
- `reference_table.csv`: the 724 annotation rows (`Document`, `Code`, `Quotation`, `Note`) in QualFrame's reference format

Each download and output is checked against the hashes in [`scripts/expected_sha256.json`](scripts/expected_sha256.json), so a successful run reproduces the study inputs byte for byte. Import the texts and the reference table into a QualFrame study, then apply a condition's `method.yaml` and the codebook.
