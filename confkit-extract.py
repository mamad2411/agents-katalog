#!/usr/bin/env python3
"""Ekstrak kit non-teknis (CONF/TAX-EINVOICE/SUEDE/RSUN) dari SEMUA STYLE-<CAT>.md
menjadi 4 file STYLE-kit mandiri — idempotent, verifikasi jumlah ketat.
Sumber kebenaran: skills-index.db (total 26731, bukan file MD yang bisa drift).
"""
import re, sqlite3, os, sys
AG = os.path.expanduser('~/.agents')
con = sqlite3.connect(AG + '/skills-index.db')
CONF = re.compile(r'^[a-z]{2,12}-(rebuttal|submission|supplementary|topic-selection|camera-ready|author-response|artifact-evaluation|referee-strategy|experiments|paper-formatting|review-process|program-committee|style-files-reviewer|style-files-creator|abstract-enhancer|title-optimizer|related-work|supplement-materials|response-letter|appendix-formatter|references-manager|competing-interests|data-code-availability|acknowledgements-writer|retraction-handler|misconduct-screener|statistical-reviewer|cover-letter|manuscript-assessor|editorial-assessment|guest-editor|special-issue|book-proposal)')
KITS = {
    'CONF-ACADEMIC-JOURNAL': (lambda n: bool(CONF.match(n)),
        'Kit penulisan & publikasi jurnal/konferensi akademik',
        'brycewang-stanford/awesome-journal-skills (1135 stars) — 200+ jurnal: AER, QJE, Nature, Cell, dsb. Skill per jurnal: rebuttal, submission, supplementary, topic-selection, camera-ready, dst.'),
    'TAX-EINVOICE': (lambda n: 'einvoice' in n or 'income-tax' in n,
        'Kit pajak & e-invoice lintas negara',
        'openaccountants/openaccountants (391 stars, direview CPA/CA/EA) — 1000+ panduan pajak 190+ yurisdiksi + e-invoice.'),
    'SUEDE-SEO-MARKETING': (lambda n: n.startswith('suede-'),
        'Kit SEO, AI search visibility, copywriting, marketing',
        'jasoncolapietro/suede-creator-skills (123 stars) — SEO, AI search visibility, conversion copy, marketing strategy.'),
    'RSUN-WORKFLOW': (lambda n: n.startswith('rsun-'),
        'Kit workflow TDD/ADR/PRD (campuran EN+ZH)',
        'claude-plugin-ronsunai-os — disiplin vertical-slice TDD, ADR, PRD, planning. Catatan: campuran bahasa Inggris+Mandarin.'),
}
# 1) kumpulkan anggota kit dari db + catat (name -> kit, kategori asal)
rows = con.execute('select name, tier, category, description, path from skills').fetchall()
member = {}
for n, t, c, d, p in rows:
    for kit, (pred, _, _) in KITS.items():
        if pred(n):
            member[n] = (kit, t, c or '(tanpa)', d or '', p or '')
            break
print('anggota kit: %d (CONF=%d TAX=%d SUEDE=%d RSUN=%d)' % (len(member),
    sum(1 for v in member.values() if v[0]=='CONF-ACADEMIC-JOURNAL'),
    sum(1 for v in member.values() if v[0]=='TAX-EINVOICE'),
    sum(1 for v in member.values() if v[0]=='SUEDE-SEO-MARKETING'),
    sum(1 for v in member.values() if v[0]=='RSUN-WORKFLOW')))
# 2) tulis 4 file kit
from collections import defaultdict
bykit = defaultdict(list)
for n, (kit, t, c, d, p) in member.items():
    bykit[kit].append((n, t, c, d, p))
for kit, (pred, desc, src) in KITS.items():
    ents = sorted(bykit.get(kit, []))
    cur = [e for e in ents if e[1] == 'curated']
    L = ['# STYLE-%s — %s (%d skill)' % (kit, desc, len(ents)), '',
         '> SUMBER: %s' % src,
         '> Untuk AI: tugas seputar topik kit ini -> daftar di bawah (bintang curated = default). JANGAN cari di file kategori teknis — sudah dipindah ke sini semua.', '']
    if cur:
        L.append('## Bintang curated (%d)' % len(cur))
        for n, t, c, d, p in cur[:20]:
            L.append('- ' + n + ' [' + c + ']' + ((' - ' + d[:100]) if d else ''))
        if len(cur) > 20: L.append('- ... (+%d curated lain di bawah)' % (len(cur) - 20))
        L.append('')
    L.append('## SEMUA skill kit ini (%d)' % len(ents))
    for n, t, c, d, p in ents:
        L.append('- ' + n + ' [' + t + '/' + c + ']' + (((' - ' + d[:90]) if d else '')) + ' | ' + p)
    open(AG + '/STYLE-' + kit + '.md', 'w').write('\n'.join(L) + '\n')
    print('tulis STYLE-%s.md: %d' % (kit, len(ents)))
# 3) buang anggota kit dari SEMUA STYLE-<CAT>.md (semua kategori, bukan cuma yg tercemar)
import glob
total_buang = 0
for f in glob.glob(AG + '/STYLE-*.md'):
    base = os.path.basename(f)
    if re.match(r'^STYLE-(CONF-ACADEMIC-JOURNAL|TAX-EINVOICE|SUEDE-SEO-MARKETING|RSUN-WORKFLOW|TOKEN-SAVER|DESIGN-QUALITY|DOC-SPEC-PRD-BRD)\.md$', base):
        continue
    lines = open(f, encoding='utf-8', errors='ignore').read().splitlines()
    kept, buang = [], 0
    for l in lines:
        m = re.match(r'^- ([a-z0-9][a-z0-9\-_/ ]*?) \[', l)
        if m and m.group(1).strip() in member:
            buang += 1
            continue
        kept.append(l)
    if buang:
        open(f, 'w', encoding='utf-8').write('\n'.join(kept) + '\n')
        total_buang += buang
        print('buang %d dari %s' % (buang, base))
print('total dibuang:', total_buang)
# 4) VERIFIKASI: kit + sisa kategori == db total
sisa = 0
for f in glob.glob(AG + '/STYLE-*.md'):
    base = os.path.basename(f)
    if re.match(r'^STYLE-(CONF-ACADEMIC-JOURNAL|TAX-EINVOICE|SUEDE-SEO-MARKETING|RSUN-WORKFLOW|TOKEN-SAVER|DESIGN-QUALITY|DOC-SPEC-PRD-BRD)\.md$', base):
        continue
    for l in open(f, encoding='utf-8', errors='ignore'):
        if l.startswith('- ') and ' | ' in l:
            sisa += 1
kit_n = len(member)
db_n = con.execute('select count(*) from skills').fetchone()[0]
print('VERIFIKASI: kit(%d) + sisa full-list(%d) = %d vs db %d -> %s' % (kit_n, sisa, kit_n + sisa, db_n, 'OK' if kit_n + sisa == db_n else 'MISMATCH!'))
