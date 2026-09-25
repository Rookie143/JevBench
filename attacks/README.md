当前交付入口：[2026-09-25 完整数据、规范、评测与日志](../releases/beta1.0-20260925/README.md)。以下为早期目录规划；当前原始数据结构和复算方法以 release 为准。

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
