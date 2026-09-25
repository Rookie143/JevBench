# beta1.0 / ADbeta1.0 修正版完整实验

本目录替换先前结果，采用最终英文 prompt，S3 恢复为外层非权威观点字段 `S3-personal-opinion-v1`，不采用将备注移入 instructions 的探索方案。

[完整报告](results/report.md) · [修正说明](results/correction-notes.md) · [汇总 JSON](results/summary.json) · [12 类完整例子](results/twelve-method-example.json) · [实际使用的 Prompt](spec/扰动生成prompt-en.md)

- beta1.0：66 场景、812 题（314 Noul / 337 Choice / 161 Score）。
- ADbeta1.0：9,744 个从原题重新生成的独立候选。Q1 为 73 个同义替换和 739 个空格扰动；Q2 为 115 个句子改写和 697 个实质词汇改写；T3 使用具体假设案例。
- 模型 jev-1.13.0：9,744 次攻击调用、812 次原题调用、812 次相同原题重复对照，合计 11,368 次均成功。主测试峰值并发 1,000。
- 对抗严格错误 1,643/9,744（16.86%）；原题错误 81/812（9.98%）。相同原题重复有 4/731 次由对变错。
- Score 仍严格相等（仅浮点表示误差 1e-9），原闭区间不变。143 human_review、669 jev_default；独立语义审核 pending。
- S1/S3 外层新增字段的模型暴露未证实；不能将低错误率称为模型成功防御。S2 解码后字段名相同。详见报告。

## 完整 JSON 与日志

在仓库根目录运行，使用新的空输出目录：

```sh
python3 releases/beta1.0-20260925/restore_and_verify.py --output restored-corrected
python3 releases/beta1.0-20260925/recompute_results.py restored-corrected
```

仅使用 Python 标准库，离线恢复与复算，不调用 API。恢复路径：`data/beta1.0.json`、`data/ADbeta1.0.json`、`eval/results.jsonl`、`eval/responses/`（10,556 条）、`clean-repeat/responses/`（812 条）、`baseline-history/`、`review-history/`。评测 manifest 和原始数据共同保留每次请求的输入；响应记录包含模型答案、token 用量、状态、请求 ID 和请求体哈希，不包含凭据或服务端内部推理。

归档与每个原始文件均有 SHA-256 校验，复算脚本核对请求体哈希和严格评分。旧版本可由 Git 历史恢复；请勿混用旧解压目录和新分卷。

## 代码与边界

`code/` 保存实际生成和评测实现，凭据适配器仅从环境变量 TYPESAFE_API_KEY 读取密钥。在线重跑需按代码配置路径并安装 requirements.txt，会产生新调用及采样差异；不承诺从任意工作目录直接运行可精确重现生成数据。生成种子和依赖哈希保存在数据与 generation-validation.json 中。不得运行历史修订脚本覆盖当前 prompt。

本次只替换主实验交付，未将另一次“只新增到已有对象”探索实验混入 ADbeta 或本轮指标。
