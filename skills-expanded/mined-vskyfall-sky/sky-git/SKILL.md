---
name: sky-git
description: >-
  Git iş akışı ve kurtarma: dal stratejisi (trunk-based, kısa ömürlü dallar), Conventional
  Commits ve iyi commit mesajı, küçük ve atomik commit'ler, rebase vs merge, interaktif olmayan
  geçmiş düzeltme (fixup, autosquash), çakışma çözme, stash, worktree, bisect ile hatalı
  commit'i bulma, reflog ile kayıp işi kurtarma, geri alma (revert/reset farkları), .gitignore,
  büyük dosyalar (LFS), imzalı commit ve PR açıklaması yazma. Git ile ilgili her işte kullan.
disable-model-invocation: true
---

# Sky · Git

## Dal stratejisi

- **Trunk-based**: `main` her zaman dağıtılabilir; kısa ömürlü özellik dalları (1–3 gün), küçük PR'lar, feature flag ile yarım işler (bkz. `sky-feature-flags`).
- Dal adı: `feat/online-randevu`, `fix/ics-saat-dilimi`, `chore/deps`.
- `main`'e doğrudan push kapalı; PR + CI + (ekipte) onay.

## Commit mesajı (Conventional Commits)

```
feat(booking): allow rescheduling from reminder SMS

Reminder messages now include a signed link that opens the reschedule
screen without login. Link expires 2 hours before the appointment.

Closes #142
```
- Tür: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `chore`, `ci`, `build`; kırıcı değişiklik `feat!:` veya gövdede `BREAKING CHANGE:`.
- Başlık ≤ 72 karakter, emir kipi, nokta yok; gövde **neden**'i anlatır (ne değiştiği diff'te zaten var).
- Dil: projenin geçmişine uy (genelde İngilizce).
- Bir commit = bir mantıksal değişiklik; biçimlendirme/taşıma ile mantık değişikliğini ayır.

## Günlük komutlar

```bash
git switch -c feat/x                 # yeni dal
git add -p                           # parça parça sahnele (karışık değişikliği böl)
git commit --fixup=<sha>             # önceki commit'e düzeltme
git rebase --autosquash main         # fixup'ları birleştir (interaktif olmayan yol: GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash main)
git pull --rebase                    # gereksiz merge commit'i yok
git push --force-with-lease          # kendi dalında güvenli zorla push (asla paylaşılan/main dalda)
git stash push -m "yarım iş"         # geçici sakla; git stash pop
git worktree add ../app-hotfix main  # aynı repoda ikinci çalışma klasörü (acil düzeltme için dal değiştirmeden)
```

## Rebase mi merge mi?

- Kendi özellik dalını güncel tutmak: **rebase** (temiz, doğrusal geçmiş).
- Paylaşılan dalı rebase etme (başkalarının geçmişini yeniden yazar).
- PR birleştirme: squash (küçük PR'larda temiz `main`) veya merge commit (geçmişi korur) — repo kuralına uy.

## Çakışma çözme

1. `git status` → çakışan dosyalar. 2. İşaretleri (`<<<<<<<`, `=======`, `>>>>>>>`) **anlayarak** çöz — iki tarafın niyetini birleştir, birini körlemesine seçme.
3. Testleri çalıştır. 4. `git add` + `git rebase --continue` / `git commit`.
Kilit dosyaları (`pnpm-lock.yaml`) elle düzeltme: bir tarafı al, `pnpm install` ile yeniden üret.

## Geri alma

| Durum | Komut |
|---|---|
| Push edilmiş commit'i geri al | `git revert <sha>` (yeni ters commit — güvenli) |
| Yerel son commit'i geri al, değişiklikler kalsın | `git reset --soft HEAD~1` |
| Sahnelemeyi geri al | `git restore --staged <dosya>` |
| Dosyadaki değişiklikleri at | `git restore <dosya>` (kalıcı — dikkat) |
| Her şeyi yerel olarak sıfırla | `git reset --hard` (kaydedilmemiş iş kaybolur — önce stash) |

## Kurtarma: reflog

"Commit'imi kaybettim / yanlış reset yaptım" → `git reflog` HEAD'in her hareketini tutar (~90 gün):
`git reflog` → doğru satırı bul → `git switch -c kurtarma <sha>`. Commit edilmiş hiçbir şey kolay kolay kaybolmaz; commit edilmemiş değişiklikler kaybolabilir — sık commit at.

## bisect: hatayı getiren commit

```bash
git bisect start
git bisect bad                      # şu an bozuk
git bisect good v1.4.0              # bu sürüm iyiydi
git bisect run pnpm test -- booking # otomatik: testin geçip geçmediğine göre ikiye böler
git bisect reset
```

## Diğer

- `.gitignore`: `node_modules`, build çıktıları, `.env*` (`.env.example` hariç), OS dosyaları; zaten izlenen dosyayı yok saymak için `git rm --cached`.
- Sır commit'lendiyse: **önce sırrı döndür** (geçersiz kıl), sonra geçmişten temizle (`git filter-repo`) — geçmişi temizlemek yetmez, kopyalar olabilir.
- Büyük ikili dosyalar: Git LFS veya depolamaya koy.
- İmzalı commit (SSH anahtarıyla): `git config commit.gpgsign true`, `gpg.format ssh`.
- Takma adlar: `git config --global alias.lg "log --oneline --graph --decorate -20"`.

## PR açıklaması

```
## Ne
Hatırlatma SMS'inden giriş yapmadan erteleme.
## Neden
No-show oranı yüksek; müşteriler ertelemek için arıyor (#142).
## Nasıl
İmzalı token (2 saat geçerli), yeni /r/[token] sayfası, slot motoru yeniden kullanıldı.
## Test
Birim: token süresi/imza. E2E: SMS bağlantısı → erteleme → onay. 375px ekran görüntüsü ekte.
## Risk / geri alma
Flag: reschedule-from-sms. Migration yok.
```
