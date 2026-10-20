---
name: release
description: 통합 릴리스 워크플로우. 버전 관리, 문서 정리, 배포까지 한 번에 관리합니다.
---

# /release - 통합 릴리스 워크플로우

## Usage

```bash
/release <subcommand> [options]
```

### Subcommands

| Command | Description |
|---------|-------------|
| `prepare` | 릴리스 준비 (체크리스트 생성) |
| `create` | 릴리스 생성 (태그, 노트) |
| `publish` | 릴리스 배포 |

## /release prepare

릴리스를 준비합니다.

```bash
/release prepare v1.2.0 [--type major|minor|patch]
```

### 실행 과정

```
┌────────────────────────────────────────────────────────────────────┐
│                   /release prepare WORKFLOW                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. 버전 결정                                                       │
│     └── 현재 버전 확인, 다음 버전 계산                             │
│                                                                     │
│  2. Phase 완료 검증                                                 │
│     └── phase-tracker: 모든 Phase 체크리스트 확인                  │
│                                                                     │
│  3. Sprint 정리                                                     │
│     └── /sprint end: 현재 Sprint 종료                              │
│                                                                     │
│  4. Quality Gate 실행                                               │
│     └── quality-gate pre-release: 전체 검증                        │
│                                                                     │
│  5. CHANGELOG 정리                                                  │
│     └── Unreleased → v1.2.0 섹션 변환                              │
│                                                                     │
│  6. 릴리스 체크리스트 생성                                          │
│     └── docs/releases/v1.2.0-checklist.md                          │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--type` | 버전 증가 유형 | patch |
| `--skip-tests` | 테스트 건너뛰기 (비권장) | false |
| `--draft` | 릴리스 노트 초안만 생성 | false |

### Output

```
📦 RELEASE PREPARE: v1.2.0

📋 Pre-Release Checks:
   ✅ All Phase tasks complete
   ✅ Sprint 3 ended (velocity: 34 pts)
   ✅ Tests: 156/156 passed
   ✅ Coverage: 87%
   ✅ Security scan: no vulnerabilities
   ⚠️ Documentation: 2 items pending

📝 Release Summary:
   Current: v1.1.3
   Next:    v1.2.0 (MINOR)

   Features: 5
   Bug Fixes: 8
   Breaking Changes: 0

📁 Generated:
   ✅ docs/releases/v1.2.0-checklist.md
   ✅ CHANGELOG.md updated

⚠️ Action Required:
   1. Complete pending documentation
   2. Review CHANGELOG.md
   3. Run `/release create v1.2.0` when ready
```

## /release create

릴리스를 생성합니다.

```bash
/release create v1.2.0 [--notes "Release notes"]
```

### 실행 과정

```
┌────────────────────────────────────────────────────────────────────┐
│                    /release create WORKFLOW                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. 릴리스 브랜치 생성 (선택)                                       │
│     └── release/v1.2.0                                             │
│                                                                     │
│  2. 버전 업데이트                                                   │
│     └── package.json, version files 업데이트                       │
│                                                                     │
│  3. 릴리스 커밋                                                     │
│     └── chore(release): v1.2.0                                     │
│                                                                     │
│  4. Git Tag 생성                                                    │
│     └── git tag -a v1.2.0 -m "Release v1.2.0"                     │
│                                                                     │
│  5. GitHub Release 생성                                             │
│     └── gh release create v1.2.0                                   │
│                                                                     │
│  6. 릴리스 노트 자동 생성                                           │
│     └── CHANGELOG에서 추출 + PR 목록                               │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Output

```
🏷️ RELEASE CREATE: v1.2.0

📋 Version Updates:
   ✅ package.json: 1.1.3 → 1.2.0
   ✅ version.txt: updated

📝 Commits:
   ✅ chore(release): v1.2.0

🏷️ Tag Created:
   v1.2.0 (annotated)

🔗 GitHub Release:
   https://github.com/user/repo/releases/tag/v1.2.0

   ### What's New in v1.2.0

   #### Features
   - User authentication system (#32)
   - Dashboard analytics (#35)
   ...

   #### Bug Fixes
   - Login validation issue (#44)
   ...

🎉 Release v1.2.0 created! Ready to publish.
```

## /release publish

릴리스를 배포합니다.

```bash
/release publish v1.2.0 [--env production]
```

### 실행 과정

```
┌────────────────────────────────────────────────────────────────────┐
│                   /release publish WORKFLOW                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. 최종 검증                                                       │
│     └── 태그 존재, 빌드 성공 확인                                  │
│                                                                     │
│  2. 메인 브랜치 머지                                                │
│     └── release/v1.2.0 → main                                      │
│                                                                     │
│  3. 배포 트리거                                                     │
│     └── CI/CD 파이프라인 실행                                      │
│                                                                     │
│  4. Post-Release 작업                                               │
│     └── quality-gate post-release 실행                             │
│                                                                     │
│  5. 문서 아카이브                                                   │
│     └── Sprint, Phase 문서 정리                                    │
│                                                                     │
│  6. 다음 개발 준비                                                  │
│     └── develop 브랜치 업데이트, 다음 버전 설정                    │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Output

```
🚀 RELEASE PUBLISH: v1.2.0

📋 Pre-Publish Checks:
   ✅ Tag v1.2.0 exists
   ✅ Build successful
   ✅ All tests passing

🔀 Merge:
   ✅ release/v1.2.0 → main
   ✅ main → develop (back-merge)

🚀 Deployment:
   ✅ CI/CD pipeline triggered
   ✅ Production deployment started

   Monitor: https://deploy.example.com/v1.2.0

📁 Post-Release:
   ✅ Sprint 3 archived
   ✅ Phase 2 marked complete
   ✅ Retrospective generated

📊 Release Stats:
   - Duration: 3 weeks
   - Commits: 45
   - Contributors: 3
   - Features: 5
   - Bug Fixes: 8

🎉 v1.2.0 published successfully!

🔄 Next Steps:
   - Monitor deployment
   - Run `/sprint start` for next sprint
   - Update Phase 3 tasks
```

## Release Checklist Template

```markdown
# Release v1.2.0 Checklist

## Pre-Release
- [ ] All tests passing
- [ ] Coverage ≥ 80%
- [ ] Security scan clean
- [ ] Documentation complete
- [ ] CHANGELOG updated
- [ ] Version bumped

## Release
- [ ] Git tag created
- [ ] GitHub release published
- [ ] Release notes reviewed

## Post-Release
- [ ] Deployment successful
- [ ] Smoke tests passed
- [ ] Sprint archived
- [ ] Retrospective scheduled
- [ ] Next version prepared
```

## Integration Map

```
/release
    │
    ├── phase-tracker (Phase 완료 검증)
    ├── /sprint end (Sprint 종료)
    ├── quality-gate (전체 검증)
    ├── commit-helper (릴리스 커밋)
    ├── agile-sync (문서 동기화)
    └── feedback-loop (회고 생성)
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/feature` | 기능 개발 워크플로우 |
| `/bugfix` | 버그 수정 워크플로우 |
| `/sprint end` | Sprint 종료 |
| `/agile-sync` | 문서 동기화 |
