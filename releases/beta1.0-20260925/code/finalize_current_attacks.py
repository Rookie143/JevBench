import json,hashlib,shutil,collections,statistics
from pathlib import Path
from datetime import datetime
import eval_adbeta_jev as b
P=b.HERE/'exports';receipt=json.loads((P/'current-attack-run.json').read_text());run=Path(receipt['run_dir']);e=run/'eval';data=json.loads((run/'ADbeta1.0.json').read_text());source=json.loads((P/'beta1.0-20260923.json').read_text())
assert hashlib.sha256((run/'ADbeta1.0.json').read_bytes()).hexdigest()==receipt['dataset_sha256']
for a,c in zip(source['scenarios'],data['scenarios']):
 assert {k:v for k,v in c.items() if k!='questions'}=={k:v for k,v in a.items() if k!='questions'}
 for typ,rr in a['questions'].items():
  for orig,new in zip(rr,c['questions'][typ]):assert {k:v for k,v in new.items() if k!='adversarial'}==orig
rows=[json.loads(x) for x in (e/'results.jsonl').read_text().splitlines()];assert len(rows)==10556
clean={r['question_id']:r for r in rows if r['category']=='clean'};bykey={(r['question_id'],r['category']):r for r in rows};verified=0
for sc in data['scenarios']:
 for rr in sc['questions'].values():
  for rec in rr:
   entries=[('clean',rec['adversarial']['original_question_text'],sc['state'])]+[(s['id'],s['perturbed_question_text'],s['perturbed_state']) for s in rec['adversarial']['samples']]
   for cat,raw,state in entries:
    row=bykey[rec['question_id'],cat];resp=json.loads((e/'responses'/ (row['response_job_id']+'.json')).read_text())
    assert b.digest(b.request_bytes(state,[(row['item_id'],raw)]))==resp['body_sha256']
    _,ok,_=b.score(row,row['jev_answer']);assert ok==row['strict_correct'];verified+=1
summary=json.loads((e/'summary.json').read_text());token={}
for cat in summary['by_category']:
 rs=[r for r in rows if r['category']==cat];ds=[r['input_tokens']-clean[r['question_id']]['input_tokens'] for r in rs]
 token[cat]={'same':sum(x==0 for x in ds),'increased':sum(x>0 for x in ds),'decreased':sum(x<0 for x in ds),'median_difference':statistics.median(ds)}
summary['token_difference_by_category']=token
(e/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
conclusion='''
## 本轮结论

1. T2 是本轮模板中新增严格错误最多的类别：152/733（20.74%）；P1 为 133/733（18.14%），P2 为 125/733（17.05%），T3 为 107/733（14.60%）。这些是原题答对后变错的条件比例，不是所有题的总错误率。
2. T2 的新增错误由 Noul 19、Choice 52、Score 81 构成；T3 分别为 6、33、68。个人观点和假设类比放进 State 后，即便不冒充官方权威，仍与明显的判断变化相伴。但本轮没有完全相同输入的重复对照，不能排除数值波动；生成候选尚待独立语义审核。
3. S3 的 812 个请求输入 token 数全部与对应原题一致。其总错误率 9.98% 接近原题 9.73%，仅新增 7 个严格错误。这与辅助字段被服务端忽略/过滤的解释相容；没有模型输入日志，不能确定具体机制，也不能声称模型成功识别了这些观点。
4. S1/S2 同样应结合传输与模型输入暴露解释，不能只看低错误率就宣布鲁棒性。
5. Score 原题本身已有 66/161（40.99%）严格数值不匹配。所有容差保持原标准；T2/T3 的高总错误率不能全部理解成方向性或灾难性错误。建议优先人工复查新增 Choice/Noul 错误，再解释 Score 的偏移量与任务意义。
6. 此轮得到的是“当前模板实现”的结果：Q1 采用空格扰动，Q2 采用保留原问题文字的句式改写，S3/T2 采用主观结论模板，T3 采用明确的假设类比模板。不是这些攻击家族的能力上限，也未验证人类是否会被骗。
'''
with (e/'report.md').open('a') as f:f.write(conclusion+'\n完整 token 诊断见 summary.json 的 token_difference_by_category。\n')
verification={'passed':True,'request_hashes_and_strict_scores_verified':verified,'original_records_and_label_provenance_unchanged':True,'unique_output_items':len(bykey),'failed_requests':len(summary['failed_or_missing']),'dataset_sha256':receipt['dataset_sha256']}
(e/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
backup=P/('ADbeta1.0-before-current-'+datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir()
for name in ['ADbeta1.0.json','ADbeta1.0-validation.json','ADbeta1.0-README.md']:
 if (P/name).exists():shutil.copy2(P/name,backup/name)
shutil.copy2(run/'ADbeta1.0.json',P/'ADbeta1.0.json');shutil.copy2(run/'validation.json',P/'ADbeta1.0-validation.json')
(P/'ADbeta1.0-README.md').write_text('# ADbeta1.0 当前版\n\n采用最新英文 prompt，全新从 beta1.0 生成 9,744 条候选。S3-personal-opinion-v1；T-nonauthoritative-v1。\n\n完整快照与结果：'+str(run)+'\n\n本轮 9,744 个候选及 812 个原题已分别调用一次 Jev，10,556 次均成功；评分严格，语义审核 pending。生成器 generate_current_attacks.py；评测器 eval_current_attacks.py。旧版本已备份，历史实验不能当作当前版本结果。\n')
print(json.dumps({'verification':verification,'token_diagnostics':token,'backup':str(backup)},ensure_ascii=False))
