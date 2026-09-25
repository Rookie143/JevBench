"""Offline: restore complete evidence and verify every original byte; no API calls."""
import argparse,hashlib,json,tarfile,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('restored'));a=p.parse_args();here=Path(__file__).resolve().parent
idx=json.loads((here/'archive-index.json').read_text());a.output.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory() as temp:
 archive=Path(temp)/'evidence.tar.xz'
 with archive.open('wb') as out:
  for part in idx['parts']:
   f=here/part['file'];assert f.stat().st_size==part['bytes'] and sha(f)==part['sha256'],part['file'];out.write(f.read_bytes())
 assert sha(archive)==idx['archive_sha256']
 with tarfile.open(archive,'r:xz') as tf:
  for member in tf.getmembers():
   target=(a.output/member.name).resolve();assert target.is_relative_to(a.output.resolve()) and member.isfile()
   if target.exists():assert hashlib.sha256(tf.extractfile(member).read()).hexdigest()==sha(target),'Refusing to overwrite changed file: '+str(target)
   else:
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(tf.extractfile(member).read())
manifest=json.loads((here/'evidence-files.json').read_text())
for f in manifest:
 path=a.output/f['path'];assert path.stat().st_size==f['bytes'] and sha(path)==f['sha256'],f['path']
print(json.dumps({'verified_files':len(manifest),'output':str(a.output.resolve()),'current_responses':idx['current_response_count']},indent=2))
