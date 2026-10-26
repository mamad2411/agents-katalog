# auto-triggers — peta maksud user → aksi

Dibaca hanya kalau tabel di `RULES.md` kurang. Jangan muat di sesi normal (hemat token).
Prinsip: **user tidak perlu mengetik `/`**. Slash command di bawah = nama intent; isinya
dikerjakan sendiri oleh AI mana pun. Hanya Claude Code yang punya file command native —
Codex/Gemini/Cursor/CodeBuddy menjalankan langkahnya langsung.

## Git & rilis
| Intent | Aksi |
|---|---|
| commit, simpan | `git status` → `git diff` → `git add -A` → commit conventional (tanpa `--no-verify`) |
| branch name | `fitur/<slug>` · `fix/<slug>` · `chore/<slug>` dari isi diff |
| PR, pull request | push branch → `gh pr create --fill` (tanya dulu sebelum push) |
| ship, rilis, deploy | test + build + `health_check` → deploy |
| worktree | `git worktree add ../<nama> <branch>` |
| bersihkan worktree | `git worktree list` → prune yang sudah merged |

## Kualitas kode
| Intent | Aksi |
|---|---|
| review | baca diff → temuan berurut risiko, `file:baris`, tanpa nit kosmetik |
| check, siap produksi? | lint + test + build, laporkan exit code apa adanya |
| refactor | jaga perilaku; test sebelum & sesudah; satu alasan per perubahan |
| clean, codebase kotor | hapus mati yang terbukti (grep 0 hit), jangan spekulasi |
| coverage | ukur dulu → tambah test di jalur paling berisiko |
| health check | build + test + deps + secret scan |
| audit, fr3k-compare | bandingkan pola nyata proyek sejenis, keluarkan gap + prioritas |
| simplify, rapikan | kurangi abstraksi; 3 baris mirip > 1 helper prematur |
| patch, perbaiki cepat | fix minimal di akar masalah, bukan gejala |
| logging, error tracking | pasang logger terstruktur, jangan `print` |
| bug, crash, gagal | reproduksi → isolasi → hipotesis → fix → test regresi |
| test gagal | baca pesan → jalankan 1 test → perbaiki sebabnya, jangan skip |
| e2e gagal | cek selector/timing dulu, bukan tambah `sleep` |

## Fitur & proyek
| Intent | Aksi |
|---|---|
| fitur baru, tambah X | AC → skema/API → kode → test → dokumentasi |
| API baru | kontrak → handler → validasi → test → contoh curl |
| implement, kerjakan | baca file nyata → plan 3-7 langkah → eksekusi → verifikasi |
| plan, rencana | 3-7 langkah satu baris, dependensi ditandai, lalu eksekusi |
| prime, kenali repo | baca README/AGENTS/docs index, ringkas 10 baris |
| dokumentasi, README, manual | tulis/ubah dokumen; jangan mengarang isi kode |
| MCP tool baru | spec → server → daftarkan → uji panggilan |
| install, setup | cek dependensi nyata → pasang → verifikasi jalan |
| chore | update deps/lockfile, jalankan test setelahnya |
| opinion, pendapat kedua | 2 sudut pandang (risiko vs kecepatan), rekomendasi tegas |
| KPI agent | hitung dari log nyata, bukan estimasi |

## Device & aset (script nyata di `~/.agents/skills-store/`)
| Intent | Script |
|---|---|
| panas, lemot, RAM, cache, baterai | `device-cool/scripts/check.sh` → `clean.sh` |
| buka web, screenshot, cek URL | `browser-use-local/scripts/browse.py "<url>"` |
| gambar/PDF dilampirkan | `baca-gambar/scripts/read.py <file>` |
| ingat, catat, lupa, memori | `linkedin-obsidian-memory-graph/scripts/{save,recall}.sh` |
| vault obsidian | `obsidian-llm-bridge` scripts |
| referensi UI sebelum koding | `framer-reference/scripts/framer-ref.sh <url>` |
| prompt berantakan | `prompt-booster/scripts/tidy.sh` |

## Cara pakai tabel ini
1. Ambil kata kerja + objek dari pesan user (`commit`, `test`, `cover`, `baterai`).
2. Cocokkan ke tabel. Tidak ada → `sk "<tugas>" -n 5` → `sk -l <nama>`.
3. Jalankan. Jangan tanya "mau saya pakai skill X?".
4. Ragu antara 2 aksi → pilih yang paling dekat, sebut 1 baris, jalan.
5. Berhenti hanya untuk aksi destruktif/keluar/biaya (lihat `RULES.md`).

## Batas yang tidak boleh dilanggar walau auto-pilot
- `push`, PR, email, posting publik, deploy produksi → konfirmasi dulu.
- Hapus permanen, `reset --hard`, `--force`, ganti kredensial → konfirmasi dulu.
- Data pribadi pihak ketiga, dokumen palsu, serangan tanpa izin → tolak, bukan "jalan".
