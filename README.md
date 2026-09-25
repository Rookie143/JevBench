# JevBench

beta1.0是干净数据库，ADbeta是我们做的对抗数据，均在data文件夹下
[beta1.0 / ADbeta1.0 ](releases/beta1.0-20260925/README.md)

已上传完整 beta1.0（812 题）、ADbeta1.0（9,744 候选）、英文 Prompt [结果报告](releases/beta1.0-20260925/results/report.md) 和 [汇总 JSON](releases/beta1.0-20260925/results/summary.json)。

对抗错误率 16.86%，原题错误率 9.98%。

[生成prompt内容](releases/beta1.0-20260925/spec/扰动生成prompt-en.md)。

JevBench is a benchmark for evaluating the **clean performance and adversarial robustness of Jev-style typed decision models**.

## Scope

The first release focuses on **officially provided Jev example scenarios**. We will first recover the largest available scenario set, then expand and standardize questions, annotate human-verified gold answers, and construct paired adversarial variants.

### Target benchmark design

- ~60–70 scenarios after light deduplication and quality filtering
- ~10 questions per scenario
- Target question mix: **Noul : Choice : Score = 4 : 4 : 2**
- Human-verified gold labels
- Clean and adversarially perturbed versions share the same gold answer
- Main evaluation: clean performance, performance under attack, performance degradation, and conditional flip ASR

## Repository structure

```
JevBench/
├── data/           # benchmark data and intermediate releases
├── annotations/    # annotation files and adjudication records
├── attacks/        # adversarial perturbation definitions and baselines
├── schemas/        # data schemas
├── scripts/        # preprocessing and evaluation scripts
└── docs/           # plans, guidelines, and benchmark documentation
```

## Current plan

1. Recover the **maximum official scenario set** and audit question coverage.
2. Expand each retained scenario toward ~10 questions while keeping the overall 4:4:2 Noul/Choice/Score ratio.
3. Create human-verified gold answers and release the first clean benchmark.
4. Build paired adversarial variants and evaluate robustness.

## Community evaluation references

The following community resources provide existing Jev-related evaluations and are useful references when designing JevBench:

- [Open-Jev — Benchmark results and scope](https://zefan-cai.github.io/open-jev/benchmarks/)
- [Jev alternatives & benchmark — JevBench v1.3.0 | Benchmark Heaven](https://benchmarkheaven.com/jev-models)
- [Jev benchmarks: separate author-reported workloads | jevmodel.ai](https://jevmodel.ai/benchmarks/)

These are listed as **community evaluation references** for comparison and context; they are not part of the JevBench v0.1 dataset.

## Status

**beta1.0 数据与完整评测快照已交付；独立语义审核和后续基准完善继续进行。**

This repository is currently private while the first benchmark release is being prepared.

