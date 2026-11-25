# Git Workflow Skill

SENTIENT'nın gelişmiş Git iş akışı yönetimi.

## Özellikler

Bu skill, OpenClaw'ın Git entegrasyonu ve oh-my-codex'ın workflow pattern'inden adapte edilmiştir.

### Desteklenen İşlemler

#### 1. Smart Commit
```bash
sentient skill run git-workflow --action commit
```
- Otomatik diff analizi
- Conventional commits formatı
- Değişkenlik skoru hesaplama

#### 2. Branch Yönetimi
```bash
sentient skill run git-workflow --action branch --branch_name feature/auth
```
- Semantic branch naming
- Branch template'leri

#### 3. Pull Request
```bash
sentient skill run git-workflow --action pr --base_branch main
```
- Otomatik PR açıklaması
- Code review template
- Label önerileri

#### 4. Merge Conflict Çözümü
```bash
sentient skill run git-workflow --action conflict-resolve
```
- AI destekli conflict çözümü
- 3-way merge analizi
- Güvenli çözüm önerileri

### Conventional Commits

```
<type>(<scope>): <subject>

Types:
- feat: Yeni özellik
- fix: Bug düzeltmesi
- docs: Dokümantasyon
- style: Format değişikliği
- refactor: Kod refactor
- perf: Performans iyileştirmesi
- test: Test ekleme/düzeltme
- chore: Build/config değişikliği
```

### Örnek Kullanım

```bash
# Akıllı commit
sentient skill run git-workflow --action commit
# Çıktı: feat(auth): add JWT token validation

# PR oluştur
sentient skill run git-workflow --action pr --base_branch main
# Çıktı: PR #42 oluşturuldu
```

### Güvenlik

- `--force` flag'i SOVEREIGN.md tarafından engellenir
- Kritik branch'ler (main, master) korunur
- Pre-commit hook'ları otomatik çalışır

---
*SENTIENT - The She-Wolf That Guards Your Empire*
