# QualFrame studies

Study designs and configuration for two evaluations of large language models in directed (deductive) qualitative content analysis. Both were run with [QualFrame](https://github.com/ZvanAllen/qualframe) 0.11.0 ([Zenodo archive](https://doi.org/10.5281/zenodo.23442027)).

This repository shares **methods only**: the codebooks, the coding conditions, the model settings and the list of inputs needed to repeat the work. It does not contain interview data, coded output or results. Results will be reported in the accompanying methods paper.

## The two studies

| | Study A | Study B |
|---|---|---|
| **Material** | 17 deidentified interview transcripts (not shared) | 95 published smoking-cessation intervention reports from the Human Behaviour-Change Project (HBCP) corpus |
| **Framework** | CFIR 2.0 with the Outcomes Addendum: 115 codes in 6 domains | BCT Taxonomy v1 as annotated by HBCP: 94 techniques in 16 groups |
| **Question** | How does the way the coding task is framed change what a model codes? | How closely do current models match expert human annotation? |
| **Conditions** | 2 decision styles × 2 ways of splitting the codebook | Pilot: 2 decision styles × 3 splits on 5 papers. Full study: one chosen condition, 4 models |
| **Models** | Claude Sonnet 5.5, GPT-6.1 Sol | Claude Haiku 5.5, GPT-6 Luna, GPT-6.1 Sol, Claude Sonnet 5.5 |
| **Reference coding** | Human-adjudicated coding (not shared) | HBCP expert annotations (fetched from the source, not redistributed here) |

### Settings shared by both studies

- **Evidence:** every code must be supported by a unique, exact quotation from the source text, which QualFrame locates and checks.
- **Context:** the model sees one sentence before and after each passage.
- **Coding:** multi-label, overlapping passages allowed, passages proposed by the model.
- **Review:** complete human review is required before any coding counts as final.

### The conditions

- **Decision style.** *Find passages*: the model reads the text and proposes passages with the codes they support. *Decide each code*: the model returns a present or absent decision, with evidence, for every code in the request.
- **Codebook split.** *Whole codebook*: all codes in one request per document. *By domain* or *by group*: one request per CFIR domain (Study A) or per taxonomy group (Study B). Study B's pilot also tests *five parts* of similar size, built from whole groups ([`study-b/partitions.json`](study-b/partitions.json)).

### How runs are compared

Runs are compared with QualFrame's QualBench module. It reports agreement on which codes apply (F1, kappa, MCC, balanced accuracy) at code and group level, agreement on the passages behind them, run-to-run stability, cost and time. Intervals come from a document-level bootstrap. See the [QualBench guide](https://github.com/ZvanAllen/qualframe/blob/main/docs/guide.md).

## Repository layout

```
study-a/
  codebook/cfir2_outcomes_codebook.yaml   CFIR 2.0 + Outcomes Addendum codebook
  conditions/<condition>/                 project.yaml and method.yaml for each of the 4 cells
study-b/
  codebook/bct_hbcp94_codebook.yaml       94 techniques with BCT Ontology definitions, 16 groups
  partitions.json                         the five-part and sixteen-group splits
  cohorts.csv                             papers, cohort flags and simple text statistics
  pilot/<condition>/method.yaml           the six pilot conditions
  full/                                   project.yaml and method.yaml for the four-model study
  scripts/fetch_inputs.py                 downloads and rebuilds the papers and reference coding
```

`project.yaml` files are the study definitions QualFrame used. Paths inside them are relative to a QualFrame workspace. Cost and pricing snapshots were removed because they are specific to one account and date.

## Reproducing

1. Install QualFrame 0.11.0 by following its [getting-started guide](https://github.com/ZvanAllen/qualframe/blob/main/docs/getting-started.md).
2. Create a study, import your source texts and the codebook, and apply one condition's `method.yaml`.
3. Run each model with the settings in the condition's `project.yaml` (`provider` block).
4. Compare runs with QualBench, for example:

   ```
   python scripts/qualbench.py compare --study /path/to/project.yaml --run RUN1 --run RUN2 --reference REFERENCE --bootstrap 2000 --seed 42
   ```

Study A needs your own transcripts and reference coding. Study B instructions are in [`study-b/README.md`](study-b/README.md).

## Licences and credit

Code and configuration in this repository: MIT. Third-party framework content keeps its own licence; see [NOTICE.md](NOTICE.md).

Built with AI coding agents (Claude Code and Codex) under Zack van Allen's direction. Study design, codebook decisions and interpretation are his.
