# beta1.0 / ADbeta1.0 完整实验

[完整结果报告](results/report.md)、[机器可读汇总](results/summary.json)、[攻击框架](spec/攻击框架表.md) 和 [本次实际使用的 Prompt](spec/扰动生成prompt-en.md)。

## 数据与结果

- beta1.0：66 个场景、812 道题，314 Noul / 337 Choice / 161 Score。

- ADbeta1.0：从原题全新生成 9,744 条候选，每题 Q1–P3 共 12 类。
  
- 当前评测：模型 jev-1.13.0，9,744 次攻击调用 + 812 次新 clean 对照；总错误 1,648/9,744（16.91%）；原题错误 79/812（9.73%）。

## 获取完整 JSON 和全部日志

在仓库根目录运行（仅 Python 标准库；不会调用 API）：

```sh
python3 releases/beta1.0-20260925/restore_and_verify.py --output restored
python3 releases/beta1.0-20260925/recompute_results.py restored
```

恢复后的内容：

| 路径 | 内容 |
|---|---|
| restored/data/beta1.0.json | 原始基准完整 JSON |
| restored/data/ADbeta1.0.json | 当前完整对抗数据，原文件字节不变 |
| restored/eval/results.jsonl | 全部 10,556 条逐题评分和答案 |
| restored/eval/responses/ | 全部 10,556 条 API 响应记录，含答案、usage、尝试次数、HTTP 状态、请求 ID、时间和请求体哈希 |
| restored/eval/manifest.json | 问题 ID、原标签、任务与原始 question 文本索引 |
| restored/eval/run-config.json、wave-*.json | 并发配置与全部 11 批运行记录 |
| restored/baseline-history/ | 原题基线输出、标签和构建相关记录 |
| restored/review-history/ | 审核事件及历史尝试记录 |

请求 State 在数据集中保存，原始 question 文本在样本/manifest 中保存，复算脚本重建每次请求并核对 SHA-256。响应记录是评测器保存的 JSON 记录，不包含 Authorization 请求头或服务端内部推理。输入 token、模型答案、评分、真实执行后果需分别解释。

`archive-index.json` 校验分卷与合并归档，`evidence-files.json` 校验全部解压原文件。复算脚本核对每次请求体哈希及全部严格评分。原 JSON 不适配仓库早期 schemas/question.schema.json；应按数据内实际结构读取。

## 代码与可复现边界

`code/` 保存本轮生成、评测、报告及依赖代码。`run.py` 专门替换为只读取环境变量 TYPESAFE_API_KEY 的可移植凭据适配器，未上传密钥或本机环境文件。其他脚本保留此次实际实现；其目录假设和生成时钟仍来自研究工作区，不应直接在仓库根目录执行后声称同种子精确复现。生成种子及文件哈希见 generation-validation.json 和 ADbeta1.0.generation_spec。

上述两条离线命令已验证，可以完整恢复与复算本轮结果。重新调用模型会产生费用及采样差异，需按代码中的 SOURCE/OUT 配置路径、安装 code/requirements.txt，并自行设置环境变量。不要通过执行旧修订脚本覆盖当前 prompt。

本交接包含当前 release 和其标签/基线来源证据，不声称包含整个工作区所有历史攻击实验。旧 S3 数组、重复键、收窄实验另见 jevpaper 历史材料；这些不是本轮方法，不能混合统计。完整性校验不等于独立语义审核。
