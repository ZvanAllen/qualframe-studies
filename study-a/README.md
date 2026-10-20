# Study A: framing the coding task

Study A asks whether the way a directed coding task is framed changes what a model codes, holding the material, codebook and models fixed.

## Material

Seventeen deidentified semi-structured interview transcripts from an implementation study. The transcripts, the human-adjudicated reference coding and all model output stay with the research team under the study's ethics approval, and are not shared here. Any set of interview transcripts with a CFIR reference coding can be used to repeat the design.

## Codebook

[`codebook/cfir2_outcomes_codebook.yaml`](codebook/cfir2_outcomes_codebook.yaml): the 115 constructs of CFIR 2.0 with the Outcomes Addendum, across six domains (Innovation, Outer Setting, Inner Setting, Individuals, Implementation Process, Outcomes Addendum). Each code carries its published definition. No study-specific guidance or examples were added.

## Design

A 2 × 2 of decision style and codebook split:

| Condition | Decision style | Codebook split | Requests per transcript |
|---|---|---|---|
| [`find-whole-codebook`](conditions/find-whole-codebook/) | Find passages | Whole codebook | 1 |
| [`decide-whole-codebook`](conditions/decide-whole-codebook/) | Decide each code | Whole codebook | 1 |
| [`find-by-domain`](conditions/find-by-domain/) | Find passages | One request per domain | 6 |
| [`decide-by-domain`](conditions/decide-by-domain/) | Decide each code | One request per domain | 6 |

`find-whole-codebook` uses QualFrame's default instructions and is the reference point for the other three. It was run first, with GPT-6.1 Sol. The other three cells were each run with Claude Sonnet 5.5 (maximum output 64,000 tokens) and GPT-6.1 Sol (reasoning effort low, maximum output 32,000 tokens). All runs used provider-default temperature.

## Measures

Each run is compared with the human-adjudicated reference and with the other runs in QualBench: code-presence agreement per transcript and code, passage agreement, run-to-run stability, requests that returned no decision, cost and time.
