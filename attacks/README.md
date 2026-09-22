# Attacks

This directory will contain reference adversarial perturbations and baseline attack implementations.

Each adversarial example should preserve the intended task semantics and keep the same gold answer as its paired clean example.

Recommended fields:

- `clean_question_id`
- `attack_id`
- `attack_type`
- `clean_input`
- `adversarial_input`
- `gold_answer`
