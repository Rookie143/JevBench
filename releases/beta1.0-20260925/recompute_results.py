"""Recompute strict scores and request digests offline from restored evidence."""
import sys,json,hashlib
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else 'restored');here=Path(__file__).resolve().parent
sys.path.insert(0,str(here/'code'));import eval_adbeta_jev as b
b.SOURCE=root/'data/ADbeta1.0.json';b.OUT=root/'eval';b.RESPONSES=b.OUT/'responses'
data,sha,items,groups=b.load_items();lookup={x['item_id']:x for x in items};counts={};n=0
for group in groups.values():
 for iid,raw in group['items']:
  result=json.loads((b.RESPONSES/('job-'+iid+'.json')).read_text());assert result['status']=='ok'
  assert result['body_sha256']==b.digest(b.request_bytes(group['state'],[(iid,raw)]))
  item=lookup[iid];_,ok,_=b.score(item,result['answers'][iid]);c=counts.setdefault(item['category'],{'answered':0,'errors':0});c['answered']+=1;c['errors']+=not ok;n+=1
expected=json.loads((root/'eval/summary.json').read_text())
for cat,v in counts.items():
 old=expected['clean'] if cat=='clean' else expected['by_category'][cat]
 assert v['answered']==old['answered'] and v['errors']==old['strict_errors']
print(json.dumps({'verified_requests':n,'dataset_sha256':sha,'counts':counts},indent=2))
