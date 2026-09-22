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
