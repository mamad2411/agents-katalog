---
name: developer-relations
description: "Developer relations - community building, documentation, DevRel metrics."
---

# Developer Relations

## Open Source Community Management

### Community Health Scorecard

| Metrik | Saglikli | Dikkat | Kritik |
|--------|---------|--------|--------|
| Time to First Response | < 24 saat | 1-3 gun | > 3 gun |
| Issue Close Rate (monthly) | > %70 | %40-70 | < %40 |
| PR Merge Time | < 3 gun | 3-7 gun | > 7 gun |
| External Contributors | > %30 | %10-30 | < %10 |
| Bus Factor | > 3 | 2-3 | 1 |
| Release Cadence | Regular (2-4 hafta) | Duzensiz | > 3 ay |
| Documentation Coverage | > %80 | %50-80 | < %50 |

### Community Roles & Responsibilities

```
Maintainer
  |-- Core Contributor (write access)
  |     |-- Regular Contributor (frequent PRs)
  |     |     |-- Occasional Contributor (1-5 PRs)
  |     |           |-- First-time Contributor
  |-- Reviewer (code review)
  |-- Triage (issue labeling)
  |-- Community Moderator (Discord/Slack)
  |-- Documentation Contributor
```

### Issue Triage Labels

```yaml
# Issue labels taxonomy
type:
  - bug                    # Something isn't working
  - feature                # New feature request
  - enhancement            # Improvement to existing feature
  - documentation          # Documentation update
  - question               # Community question

priority:
  - critical               # Production breaking
  - high                   # Important, next release
  - medium                 # Normal priority
  - low                    # Nice to have

status:
  - needs-triage           # Awaiting maintainer review
  - confirmed              # Bug confirmed, feature accepted
  - needs-info             # Waiting for reporter input
  - in-progress            # Being worked on
  - blocked                # Dependency blocker

experience:
  - good-first-issue       # Newcomer friendly
  - help-wanted            # Community contribution welcome
  - mentor-available       # Maintainer will guide
```

### Automated Community Workflows

```yaml
# .github/workflows/community.yml
name: Community Management

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened]

jobs:
  welcome-new-contributor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/first-interaction@v1
        with:
          issue-message: |
            Welcome to the project! Thanks for opening your first issue.
            Please make sure you've filled out the issue template completely.
            A maintainer will review this shortly.
          pr-message: |
            Thanks for your first PR! A maintainer will review it soon.
            Please make sure all checks pass and you've signed the CLA.

  auto-label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: "${{ secrets.GITHUB_TOKEN }}"

  stale-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          stale-issue-message: "This issue has been inactive for 30 days. It will be closed in 7 days if no further activity occurs."
          days-before-stale: 30
          days-before-close: 7
```

## Developer Documentation Best Practices

### Documentation Architecture

```
docs/
  getting-started/
    installation.md          # 5 dakikada calistir
    quickstart.md            # Ilk basari deneyimi
    configuration.md         # Temel ayarlar
  guides/
    authentication.md        # How-to guide
    data-migration.md        # Step-by-step
    deployment.md            # Production setup
  reference/
    api/                     # Auto-generated API docs
    cli/                     # CLI commands
    configuration/           # All config options
  concepts/
    architecture.md          # Mimari aciklama
    data-model.md            # Data yapisi
  examples/
    basic/                   # Basit ornekler
    advanced/                # Ileri ornekler
    integrations/            # 3rd party entegrasyonlar
  contributing/
    CONTRIBUTING.md          # Katki rehberi
    CODE_OF_CONDUCT.md       # Davranis kurallari
    DEVELOPMENT.md           # Dev environment setup
  changelog/
    CHANGELOG.md             # Release notes
```

### Documentation Quality Checklist

| Kriter | Aciklama |
|--------|----------|
| 5-Minute Success | Yeni kullanici 5 dk'da calisan bir sey gorebilmeli |
| Copy-Paste Ready | Kod ornekleri direkt calisabilmeli |
| Up-to-Date | Kod degisince doc da guncellenecek (CI check) |
| Searchable | Arama motoru ile bulunabilir |
| Progressive Disclosure | Basit -> Orta -> Ileri siralama |
| Error Messages | Hata mesajlari doc'a linklemeli |
| Platform Coverage | macOS, Linux, Windows ornekleri |
| Language Coverage | En az 3 dilde SDK ornegi |

### API Documentation Template

```markdown
## Create User

Creates a new user account.

### Request

`POST /api/v1/users`

#### Headers

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |
| Content-Type | Yes | application/json |

#### Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Valid email address |
| name | string | Yes | Full name (2-100 chars) |
| role | string | No | "admin" or "member" (default: "member") |

#### Example

\```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "Jane Smith",
    "role": "member"
  }'
\```

### Response

#### 201 Created

\```json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "name": "Jane Smith",
  "role": "member",
  "created_at": "2026-01-15T10:30:00Z"
}
\```

#### 400 Bad Request

\```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format"
  }
}
\```

#### 409 Conflict

\```json
{
  "error": {
    "code": "DUPLICATE_EMAIL",
    "message": "A user with this email already exists"
  }
}
\```
```

## Tutorial ve Workshop Olusturma

### Tutorial Structure

```
1. WHAT: Ne yapacagiz? (1 paragraf, 30 saniye okuma)
2. WHY: Neden onemli? (1 paragraf)
3. PREREQUISITES: Nelere ihtiyac var? (liste)
4. STEPS: Adim adim (her adim bitmis, calisan bir sey)
   - Step 1: Setup (copy-paste)
   - Step 2: Basic usage (calisan output goster)
   - Step 3: Build something (gercek problem coz)
   - Step 4: Advanced (opsiyonel)
5. NEXT STEPS: Sonra ne yapabilirim? (linkler)
6. TROUBLESHOOTING: Yaygın sorunlar ve cozumleri
```

### Workshop Format (90 Dakika)

```
00:00 - 00:10  Giris ve motivasyon (demo goster)
00:10 - 00:20  Setup kontrolu (herkes calisiyor mu?)
00:20 - 00:40  Guided exercise 1 (birlikte yapariz)
00:40 - 00:50  Solo exercise 1 (kendiniz yapin)
00:50 - 01:00  Ara + sorular
01:00 - 01:20  Guided exercise 2 (ileri seviye)
01:20 - 01:30  Solo exercise 2
01:30 - 01:40  Showcase (katilimcilar gosterir)
01:40 - 01:50  Q&A + next steps
```

## Conference Talk Preparation

### Talk Structure Template

```
Title: [Catchy, specific, searchable]
Duration: [15/25/40 min]
Audience Level: [Beginner/Intermediate/Advanced]

OUTLINE:
1. Hook (2 min)
   - Surprising stat or demo
   - "How many of you have...?"

2. Problem (3 min)
   - Pain point everyone recognizes
   - Why existing solutions fall short

3. Solution (Main Content) (60% of time)
   - Core concept explanation
   - Live demo or code walkthrough
   - Before/After comparison

4. Deep Dive (20% of time)
   - Technical details
   - Architecture decisions
   - Performance numbers

5. Takeaways (3 min)
   - 3 actionable items
   - Resources & links
   - QR code to slides/repo
```

### Speaker Checklist

| Asama | Kontrol |
|-------|---------|
| Proposal | CFP'ye uygun mu? Abstract compelling mi? |
| Slides | Max 1 nokta per slide, buyuk font (24pt+) |
| Demo | Offline calisir mi? Backup video var mi? |
| Timing | Prova yapildi mi? %10 buffer biraktin mi? |
| Setup | Adaptor, clicker, backup laptop? |
| After | Slides paylastin mi? Repo public mi? |

## Developer Advocate Programi

### Advocate Tipleri

| Tip | Odak | Ciktilar |
|-----|------|---------|
| Content Advocate | Blog, video, tutorial | Haftalik icerik |
| Community Advocate | Forum, Discord, events | Gunluk etkilesim |
| Technical Advocate | SDK, samples, integrations | Kod + doc |
| Field Advocate | Customer visits, workshops | Aylik workshop |
| Product Advocate | Feedback loop, beta testing | Feature requests |

### Advocate Program Metrics

```typescript
interface AdvocateMetrics {
  content: {
    blog_posts: number;
    videos: number;
    tutorials: number;
    total_views: number;
    avg_engagement_rate: number;
  };
  community: {
    questions_answered: number;
    avg_response_time_hours: number;
    community_satisfaction: number;   // 1-5
    new_members_influenced: number;
  };
  events: {
    talks_given: number;
    workshops_run: number;
    attendees_reached: number;
    post_event_signups: number;
  };
  product: {
    feedback_submitted: number;
    features_influenced: number;
    beta_testers_recruited: number;
    sdk_contributions: number;
  };
}
```

## Community Metrics

### GitHub Community Health

```typescript
interface GitHubHealth {
  stars: number;
  star_growth_weekly: number;
  forks: number;
  open_issues: number;
  closed_issues_30d: number;
  open_prs: number;
  merged_prs_30d: number;
  contributors_total: number;
  contributors_new_30d: number;
  avg_issue_close_time_hours: number;
  avg_pr_merge_time_hours: number;
  releases_90d: number;
  commit_frequency_weekly: number;
  code_frequency: { additions: number; deletions: number };
}

// GitHub API ile metrikleri cek
async function fetchGitHubHealth(owner: string, repo: string): Promise<GitHubHealth> {
  const headers = { Authorization: `token ${process.env.GITHUB_TOKEN}` };

  const [repoData, issues, prs, contributors, releases] = await Promise.all([
    fetch(`https://api.github.com/repos/${owner}/${repo}`, { headers }).then(r => r.json()),
    fetch(`https://api.github.com/repos/${owner}/${repo}/issues?state=all&per_page=100`, { headers }).then(r => r.json()),
    fetch(`https://api.github.com/repos/${owner}/${repo}/pulls?state=all&per_page=100`, { headers }).then(r => r.json()),
    fetch(`https://api.github.com/repos/${owner}/${repo}/contributors?per_page=100`, { headers }).then(r => r.json()),
    fetch(`https://api.github.com/repos/${owner}/${repo}/releases?per_page=10`, { headers }).then(r => r.json()),
  ]);

  return {
    stars: repoData.stargazers_count,
    star_growth_weekly: 0, // weekly delta hesapla
    forks: repoData.forks_count,
    open_issues: repoData.open_issues_count,
    closed_issues_30d: issues.filter((i: any) => i.state === "closed").length,
    open_prs: prs.filter((p: any) => p.state === "open").length,
    merged_prs_30d: prs.filter((p: any) => p.merged_at).length,
    contributors_total: contributors.length,
    contributors_new_30d: 0,
    avg_issue_close_time_hours: 0,
    avg_pr_merge_time_hours: 0,
    releases_90d: releases.length,
    commit_frequency_weekly: 0,
    code_frequency: { additions: 0, deletions: 0 },
  };
}
```

### Community Growth Metrics

| Metrik | Tanim | Hedef |
|--------|-------|-------|
| Stars / Week | Haftalik yeni star | +50/hafta |
| Fork-to-Star Ratio | forks / stars | > %10 |
| Contributor Growth | Aylik yeni contributor | +5/ay |
| Issue Activity | Acilan + kapanan issue | Kapanan > Acilan |
| PR External Ratio | external_prs / total_prs | > %30 |
| Time to First Response | Ilk yanit suresi | < 24 saat |
| Community NPS | Net Promoter Score | > 50 |

## Discord/Slack Community Setup

### Channel Structure

```
# Discord / Slack Channel Yapisi
general/
  #announcements         # Sadece admin yazabilir, onemli duyurular
  #introductions         # Yeni uyeler kendini tanitir
  #general-chat          # Serbest sohbet

support/
  #help                  # Teknik sorular
  #bug-reports           # Bug raporlari
  #feature-requests      # Feature istekleri

development/
  #contributing          # Katki rehberi, PR tartismalari
  #architecture          # Tasarim tartismalari
  #releases              # Release duyurulari (webhook)

showcase/
  #show-and-tell         # Topluluk projeleri
  #blog-and-content      # Icerik paylasimi

moderation/
  #mod-log               # Moderasyon kayitlari (sadece mod)
  #reports               # Kural ihlali raporlari
```

### Community Bot Commands

```typescript
const botCommands = {
  "/help": "Yardim menusu goster",
  "/docs <topic>": "Dokumantasyon linki gonder",
  "/issue <title>": "GitHub issue olustur",
  "/faq": "Sikca sorulan sorular",
  "/status": "Servis durumunu goster",
  "/version": "Son surum bilgisi",
  "/search <query>": "Docs + issues + discussions ara",
  "/feedback <message>": "Anonim geri bildirim gonder",
};
```

## Newsletter ve Blog Stratejisi

### Content Calendar Template

| Hafta | Blog | Newsletter | Social | Community |
|-------|------|-----------|--------|-----------|
| 1 | Tutorial | Monthly digest | Thread | Office hours |
| 2 | Case study | - | Tips thread | - |
| 3 | Technical deep dive | - | Demo video | Community call |
| 4 | Changelog/Release | - | Announce | Feedback survey |

### Blog Post Types & Frequency

| Tip | Frekans | Hedef | Uzunluk |
|-----|---------|-------|---------|
| Tutorial | Haftalik | Yeni kullanicilar | 1500-2500 kelime |
| Technical Deep Dive | 2 haftada 1 | Ileri seviye | 2000-3500 kelime |
| Case Study | Aylik | Social proof | 1000-1500 kelime |
| Release Notes | Her release | Mevcut kullanicilar | 500-1000 kelime |
| Opinion / Thought Leadership | Aylik | SEO + authority | 1500-2500 kelime |

## Developer Experience (DX) Measurement

### DX Scorecard

| Boyut | Metrik | Olcum |
|-------|--------|-------|
| Time to Hello World | Ilk calisan ornek suresi | < 5 dakika |
| Error Message Quality | Hatadan cozume sure | Anket + gozlem |
| SDK Ergonomics | API calls per task | Kod analizi |
| Documentation Findability | Arama -> cozum suresi | Kullanici testi |
| Support Response Time | Ilk yanit suresi | Otomatik olcum |
| Breaking Changes | Major version upgrade suresi | Anket |

### DX Survey Template

```
1. Urunumuzu kullanmaya baslamak ne kadar kolay? (1-5)
2. Dokumantasyonumuz ihtiyacinizi ne kadar karsiyor? (1-5)
3. Hata mesajlari problemi cozmekte ne kadar yardimci? (1-5)
4. SDK/API'miz ne kadar sezgisel? (1-5)
5. Destek ekibimizin yanit suresi nasil? (1-5)
6. En buyuk engel nedir? (acik ucu)
7. Bizi baska developer'lara onerir misiniz? (0-10, NPS)
```

## CONTRIBUTING.md Template

```markdown
# Contributing to [Project Name]

Thank you for your interest in contributing!

## How to Contribute

### Reporting Bugs
- Use the bug report template
- Include reproduction steps
- Include environment details (OS, runtime version)

### Suggesting Features
- Check existing issues first
- Use the feature request template
- Explain the use case, not just the solution

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`npm test`)
5. Run linting (`npm run lint`)
6. Commit with conventional commits (`feat: add amazing feature`)
7. Push to your fork
8. Open a Pull Request

### Development Setup
\```bash
git clone https://github.com/org/project.git
cd project
npm install
cp .env.example .env
npm run dev
\```

### Coding Standards
- TypeScript strict mode
- ESLint + Prettier formatting
- 80% test coverage minimum
- Conventional commits

### Review Process
1. Automated checks must pass (CI)
2. At least 1 maintainer approval
3. No unresolved comments
4. Squash merge to main

## Code of Conduct
This project follows the [Contributor Covenant](https://www.contributor-covenant.org/).
Be respectful, inclusive, and constructive.
```

## Anti-Patterns

| Anti-Pattern | Dogru Yol |
|-------------|-----------|
| "Build it and they will come" | Aktif community management yap |
| Sadece star sayisina bakmak | Contributor diversity ve engagement olc |
| Doc'u bir kere yazip unutmak | CI'da doc freshness check koy |
| Tek kanal community | Multi-platform varlik (GitHub + Discord + Twitter) |
| Sadece ingilizce | i18n doc + lokal community |
| PR'lari haftalarca bekletmek | 72 saat iceinde ilk review |
| Negativity'yi ignore etmek | Code of Conduct + aktif moderasyon |
| Feedback almamak | Duzeli anket + office hours |
