#!/usr/bin/env python3
"""Upgrade stub repo-refs that skills actually depend on (per skills-repo-map.json)
to full trees via codeload tarballs — same proven method as vercel_ai.
Keeps STUB.md (index/link tooling reads it), regenerates TREE.txt (maxdepth 2),
updates meta.json with method + timestamp. No .git anywhere. Sequential + sleep
to stay cool on CPU/network. State persisted to upgrade-demand-log.json."""
import json, os, tarfile, time, shutil, tempfile, subprocess

HOME = os.path.expanduser('~')
AG = os.path.join(HOME, '.agents')
REFS = os.path.join(AG, 'repo-refs')
MAP = os.path.join(AG, 'skills-repo-map.json')
LOG = os.path.join(AG, 'upgrade-demand-log.json')


def log_write(state):
    with open(LOG, 'w') as f:
        json.dump(state, f, indent=1)


def kind(d):
    p = os.path.join(REFS, d)
    if not os.path.isdir(p):
        return 'missing'
    try:
        n = len(os.listdir(p))
    except Exception:
        return 'missing'
    return 'real' if n > 5 else 'stub'


def tree_txt(repo_dir):
    out = subprocess.run(['find', repo_dir, '-maxdepth', '2', '-mindepth', '1'],
                         capture_output=True, text=True)
    ents = []
    for line in out.stdout.splitlines():
        rel = line[len(repo_dir):].lstrip('/')
        if rel == '.git' or rel.startswith('.git/'):
            continue
        ents.append(('/' if os.path.isdir(line) else '') + rel)
    ents.sort()
    return '\n'.join(ents) + '\n'


def upgrade(name, state):
    dest = os.path.join(REFS, name)
    owner, repo = name.split('_', 1)
    url = f'https://codeload.github.com/{owner}/{repo}/tar.gz/HEAD'
    state['current'] = name
    state['started'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    log_write(state)
    td = tempfile.mkdtemp(prefix='upg-')
    tg = os.path.join(td, 't.tar.gz')
    try:
        subprocess.run(['curl', '-sL', '--max-time', '900', '-o', tg, url],
                       check=True, timeout=920)
        if os.path.getsize(tg) < 100:
            raise RuntimeError('tarball too small (404/private/empty)')
        with tarfile.open(tg, 'r:gz') as tf:
            root0 = tf.getnames()[0].split('/')[0]
            tf.extractall(td)
        src = os.path.join(td, root0)
        if not os.path.isdir(src):
            raise RuntimeError('unexpected tarball layout')
        for ent in os.listdir(src):
            if ent == '.git':
                continue
            s = os.path.join(src, ent)
            d = os.path.join(dest, ent)
            if os.path.exists(d):
                if os.path.isdir(d) and os.path.isdir(s):
                    subprocess.run(['ditto', s, d], check=True)
                else:
                    os.remove(d)
                    shutil.move(s, d)
            else:
                shutil.move(s, d)
        with open(os.path.join(dest, 'TREE.txt'), 'w') as f:
            f.write(tree_txt(dest))
        meta_p = os.path.join(dest, 'meta.json')
        meta = {}
        if os.path.exists(meta_p):
            try:
                meta = json.load(open(meta_p))
            except Exception:
                meta = {}
        meta.update({
            'name': name,
            'source': f'https://github.com/{owner}/{repo}',
            'method': 'codeload tarball HEAD -> full tree (no .git)',
            'upgraded': time.strftime('%Y-%m-%dT%H:%M:%S'),
        })
        with open(meta_p, 'w') as f:
            json.dump(meta, f, indent=1)
        state['ok'].append(name)
        return True
    except Exception as e:
        state['fail'][name] = str(e)[:200]
        return False
    finally:
        shutil.rmtree(td, ignore_errors=True)
        state['done'] += 1
        state['current'] = None
        state['last_finished'] = time.strftime('%Y-%m-%dT%H:%M:%S')
        log_write(state)


def main():
    m = json.load(open(MAP))['map']
    targets = sorted({r for r in set(m.values()) if kind(r) == 'stub'})
    state = json.load(open(LOG)) if os.path.exists(LOG) else {'ok': [], 'fail': {}, 'done': 0}
    # keep past successes, retry past failures on this run
    state['fail'] = {}
    state['done'] = 0
    state['total'] = len(targets)
    log_write(state)
    print(f'upgrading {len(targets)} demanded stub repos', flush=True)
    for name in targets:
        if name in set(state['ok']):
            continue
        upgrade(name, state)
        time.sleep(3)
    state['finished'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    log_write(state)
    print('DONE', flush=True)


if __name__ == '__main__':
    main()
