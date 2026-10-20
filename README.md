# QualFrame studies

Study designs and configuration for two evaluations of large language models in directed (deductive) qualitative content analysis. Both were run with [QualFrame](https://github.com/ZvanAllen/qualframe) 0.11.0 ([Zenodo archive](https://doi.org/10.5281/zenodo.23442027)) and compared with its QualBench report.

This repository shares **methods only**: the codebooks, the instruction packages and codebook divisions, the model settings and the inputs needed to repeat the work. It does not contain interview data or coded output. Results will be reported in the accompanying methods paper.

## The two studies

| | Study A | Study B |
|---|---|---|
| **Material** | 17 de-identified interview transcripts (not shared) | 95 published smoking-cessation trial reports from the open-access Human Behaviour-Change Project (HBCP) corpus |
| **Framework** | CFIR 2.0 with the Outcomes Addendum: 115 codes in 6 domains | BCT Taxonomy v1 as used by HBCP: 94 techniques in 16 groups |
| **Reference** | The original workflow's model-assisted coding, partly reviewed (not shared) | HBCP's historical expert annotations (fetched from the source) |
| **Comparisons** | Original workflow prompts with four models; repeat runs; 2 instruction packages × 2 codebook divisions | Pilot of 2 instruction packages × 3 codebook divisions on 5 reports; then four models |
| **Models** | Claude Sonnet 5.5, Claude Haiku 5.5, GPT-6.1 Sol, GPT-6 Luna | the same four |

### Settings shared by both studies

- **Evidence:** every coding must cite an exact quotation, which QualFrame locates in the source text.
- **Coding:** multi-label, overlapping passages allowed, passages proposed by the model.
- **Logging:** each run saves its model settings, prompts, codebook and a hash of every input, and records every request with its token use and cost.
- **Review:** the evaluation compares the models' coding proposals before any human review.

### Design choices tested

- **Instruction package.** *Find passages*: the model finds passages that fit a code and is told not to force one. *Decide every code*: the model gives a decision on every code, with a quotation when it applies and an explicit absence when it does not. Study A also tests the original *workflow prompts*.
- **Codebook division.** The whole codebook in one request, or one part per request: one CFIR domain (Study A), or five parts of similar size or one taxonomy group (Study B pilot; see [`study-b/partitions.json`](study-b/partitions.json)).

### How runs are compared

QualBench compares each set of coding proposals with a reference at the document × code level. Balanced accuracy and the Matthews correlation coefficient (MCC) are primary, reported with sensitivity, specificity, precision, F1, kappa and two rules that read nothing (every code present, every code absent), so that results can be read against code prevalence. Intervals come from 2,000 bootstrap replicates that resample whole documents. QualBench also reports quotation fidelity, passage agreement, run-to-run repeatability, cost and time. See the [QualBench guide](https://github.com/ZvanAllen/qualframe/blob/main/docs/guide.md).

## Repository layout

```
study-a/
  codebook/cfir2_outcomes_codebook.yaml   CFIR 2.0 + Outcomes Addendum codebook
  conditions/<configuration>/             project, method (and pipeline) files for each configuration
study-b/
  codebook/bct_hbcp94_codebook.yaml       94 techniques with BCT Ontology definitions, 16 groups
  partitions.json                         the five-part and sixteen-group divisions
  cohorts.csv                             reports, cohort flags and simple text statistics
  pilot/<condition>/method.yaml           the six pilot conditions
  full/                                   project and method files for the four-model study
  scripts/fetch_inputs.py                 downloads and rebuilds the reports and reference coding
```

`project.yaml` files are the study definitions QualFrame used. Paths inside them are relative to a QualFrame workspace. Cost and pricing snapshots were removed because they are specific to one account and date.

## Reproducing

1. Install QualFrame 0.11.0 by following its [getting-started guide](https://github.com/ZvanAllen/qualframe/blob/main/docs/getting-started.md).
2. Create a study, import the source texts and the codebook, and apply one configuration's `method.yaml`.
3. Run each model with the settings in the configuration's `project.yaml` (`provider` block).
4. Import the reference and compare runs with QualBench, for example:

   ```
   python scripts/qualbench.py compare --study /path/to/project.yaml --run RUN1 --run RUN2 --reference REFERENCE --bootstrap 2000 --seed 1
   ```

Study A needs your own transcripts and reference coding; see [`study-a/README.md`](study-a/README.md). Study B can be repeated in full from public data; see [`study-b/README.md`](study-b/README.md).

## Licences and credit

Code and configuration in this repository: MIT. Third-party framework content and data keep their own licences; see [NOTICE.md](NOTICE.md).

Built with AI coding agents (Codex and Claude Code) under Zack van Allen's direction. Study design, codebook decisions and interpretation are the authors'.
