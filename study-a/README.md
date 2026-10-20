# Study A: recoding CFIR interviews

Study A asks how current models' coding compares with an established CFIR coding of the same interviews, how much runs repeat, and how two design choices change agreement: the instruction package and how the codebook is divided across requests.

## Material

Seventeen de-identified semi-structured interview transcripts. The transcripts, the reference coding and all model output stay with the research team under the study's ethics approval, and are not shared here. Any set of interviews with a CFIR coding that records explicit absences can be used to repeat the design.

## Reference

The reference is the coding produced by the original human-in-the-loop workflow's coding stage, run with an earlier model. It is model-assisted, and item-level review was recorded for only some transcripts, so agreement with it is agreement with an established coding, not with independent human ground truth. Analysts' review judgements on the reviewed transcripts allow a second, corrected reference for a sensitivity analysis.

## Codebook

[`codebook/cfir2_outcomes_codebook.yaml`](codebook/cfir2_outcomes_codebook.yaml): the 115 codes of CFIR 2.0 with the Outcomes Addendum, across six domains (Innovation, Outer Setting, Inner Setting, Individuals, Implementation Process, Outcomes Addendum). Each code carries its published definition. No study-specific guidance or examples were added.

## Instruction packages

- **Workflow prompts:** the original workflow's coding prompt, which QualFrame offers as its CFIR preset. It codes one CFIR domain per request and requires a decision on every construct, either a verbatim quotation or "No relevant quote found".
- **Find passages:** a general QualFrame package. The model finds passages that fit a code, is told not to force a code, and favours well-supported codings over coverage.
- **Decide every code:** QualFrame's generalisation of the workflow's design. The model gives a decision on every code, with exact quotations when it applies and an explicit absence when it does not.

The packages differ in emphasis, wording and output format as well as in the decision requirement, so comparisons between them compare packages.

## Configurations

| Configuration | Instruction package | Codebook per request | Models | Transcripts × runs |
|---|---|---|---|---|
| [`workflow-prompts`](conditions/workflow-prompts/) | Workflow prompts | One domain (6 requests) | Sonnet 5.5, Haiku 5.5, GPT-6.1 Sol, GPT-6 Luna | 17 × 1 |
| Repeats (same configuration) | Workflow prompts | One domain | Sonnet 5.5, GPT-6.1 Sol | 4 × 2 more |
| [`find-whole-codebook`](conditions/find-whole-codebook/) | Find passages | Whole codebook (1 request) | Sonnet 5.5, GPT-6.1 Sol | 17 × 1 |
| [`find-by-domain`](conditions/find-by-domain/) | Find passages | One domain | Sonnet 5.5, GPT-6.1 Sol | 17 × 1 |
| [`decide-whole-codebook`](conditions/decide-whole-codebook/) | Decide every code | Whole codebook | Sonnet 5.5, GPT-6.1 Sol | 17 × 1 |
| [`decide-by-domain`](conditions/decide-by-domain/) | Decide every code | One domain | Sonnet 5.5, GPT-6.1 Sol | 17 × 1 |

The repeats reran four transcripts (the shortest, the longest and two near the median) twice more. `find-whole-codebook` ran first, as an exploratory test of QualFrame's general instructions. The other three 2 × 2 cells were added after it showed a large drop in coding. Within the 2 × 2, the cells differ only in instruction package and codebook division. Only the first stage of the workflow's pipeline, coding, was run.

Model settings: Claude models with maximum output 64,000 tokens; OpenAI models with QualFrame's presets (GPT-6.1 Sol with low reasoning effort, maximum output 32,000 tokens). Provider-default temperature throughout.

## Measures

Units are transcript × code. Units with neither a coding nor a recorded absence in the reference are treated as not assessed and left out. Balanced accuracy and the Matthews correlation coefficient (MCC) are primary, alongside sensitivity, specificity, precision, F1, Cohen's kappa and two rules that read nothing (every code present, every code absent). Intervals come from 2,000 bootstrap replicates in two stages: cases are sampled with replacement, then transcripts within each sampled case. Evidence, repeatability, cost and time are measured as described in the main [README](../README.md).
