# Gold Annotation Guide

## Principle

Gold labels must be **independent of the model being evaluated**. Jev outputs may be used as annotation aids or clean baselines, but they must not define the benchmark ground truth.

## Workflow

1. Present the scenario, question, answer space, and source evidence.
2. Annotator A assigns an answer independently.
3. Annotator B assigns an answer independently.
4. Agreements become provisional gold labels.
5. Disagreements are adjudicated and documented.
6. Ambiguous questions should be revised or excluded rather than forced into a gold label.

## Question types

### Noul
Use a binary gold answer: `true` or `false`.

### Choice
Use the unique correct option identifier or value.

### Score
Define a task-specific ordinal rubric before annotation. Record the final score and the rubric version used.

## Recommended fields

- `scenario_id`
- `question_id`
- `type`
- `question`
- `options` or `score_rubric`
- `gold_answer`
- `gold_rationale`
- `annotator_1`
- `annotator_2`
- `adjudicated`
- `annotation_status`
- `source`

## Jev baseline

Store Jev's clean output separately, for example as `jev_baseline_answer`. A disagreement between the human gold label and Jev is a clean-model error, not a reason to alter the gold label.
