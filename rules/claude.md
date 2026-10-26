## Claude Code — tambahan

**Auto-skill (tanpa slash):** routing sekali per pesan, maks 2 kandidat, muat via
`bash ~/.agents/skill-load-lite.sh <nama>` (≤2 KB) — jangan baca SKILL.md penuh.
Trigger khusus:
- pesan berantakan → `~/.agents/skills-store/prompt-booster/scripts/tidy.sh`
- ingat/catat/lupa/linkedin/obsidian/memori → `linkedin-obsidian-memory-graph/scripts/{save,recall}.sh` (VAULT `~/Documents/AgentsMemory`)
- panas/lemot/ram/cache → `device-cool/scripts/check.sh|clean.sh`
- buka web/screenshot → `browser-use-local/scripts/browse.py "URL"`
- kirim gambar/PDF → `baca-gambar/scripts/read.py FILE`

**Package-first:** sebelum menulis kode, cari paket yang sudah ada (agent `sherlock`).
Jangan hand-roll. Ikon pakai library, bukan emoji di kode.

**Visual-first:** proses kompleks → diagram ASCII; opsi → tree; progres → indikator.

**Agent domain:** bugsy=error/crash · fronty=React/Next · gitty=git · murphy=config/deps ·
opinion=review · scribe=dokumen · sherlock=riset/API · validation=requirement · gopher=Go ·
jsmaster=JS/Node · nextking=Next.js · thesnake=Python · reactlord=React · typegod=TS · vuelord=Vue.
Satu agent kalau satu domain; paralel kalau lintas domain (kode+config+dokumen).

**Workflow:** riset (baca file nyata) → plan → implement → test → validasi → lapor jujur.
Status tugas: `todo → coding_done → validated → complete` (loop `needs_fixes`).
Agent bahasa/bugsy tidak boleh menandai `complete`; hanya approval manusia.

**Fail fast:** dilarang "kalau X gagal coba Y" tanpa izin user, workaround tanpa validasi,
atau solusi cadangan saat akar masalah bisa diperbaiki.
Security wajib: query parameterized, password bcrypt/argon2 ≥12 rounds, validasi input,
jangan log secret.

**Sering gagal:** menganggap isi file (baca dulu) · mengarang API (verifikasi) ·
skip test (jalankan). Stuck → sederhanakan, lalu tanya arah.
