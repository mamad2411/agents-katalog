import json, os
fid = fl = None
try:
    for e in json.load(open('/tmp/agents-dirs.json')):
        if e.get('Name') == 'agents':
            fid = e['ID']; break
except Exception: pass
try:
    for e in json.load(open('/tmp/agents-files.json')):
        if e.get('Name') == 'agents.zip':
            fl = e['ID']; break
except Exception: pass
out = []
if fid:
    out += ['Folder: https://drive.google.com/drive/folders/%s' % fid]
if fl:
    out += ['File: https://drive.google.com/file/d/%s/view' % fl,
            'Download langsung: https://drive.google.com/uc?export=download&id=%s' % fl]
open(os.path.expanduser('~/.agents/upload-links.txt'), 'w').write('\n'.join(out) + '\n')
