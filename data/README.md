当前交付入口：[2026-09-25 完整数据、规范、评测与日志](../releases/beta1.0-20260925/README.md)。以下为早期目录规划；当前原始数据结构和复算方法以 release 为准。

# Data

This directory will contain JevBench data releases and intermediate processing outputs.

Planned layout:

```
data/
├── raw/             # recovered official examples
├── processed/       # normalized scenario/question records
├── clean/           # human-verified clean benchmark
└── adversarial/     # paired adversarial variants
```

Target for v0.1: roughly 10 questions per retained scenario with an overall Noul:Choice:Score ratio near 4:4:2.
