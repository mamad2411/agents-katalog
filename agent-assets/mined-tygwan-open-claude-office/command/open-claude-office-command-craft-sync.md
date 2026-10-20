# /craft-sync — Sync with Portfolio

foliocraft에서 생성/배포된 프로젝트 사이트 정보를 메인 포트폴리오(`dev/portfolio`)의 데이터 파일과 동기화합니다.

## Usage

```
/craft-sync [project-name]
```

## Arguments

- `project-name`: 특정 프로젝트만 동기화 (선택). 미지정 시 workspace 내 모든 프로젝트.

## State Machine

### Guard
- `current_state == done` (deploy.yaml 존재 필수)
- deploy.url이 설정되어 있어야 함

### Event Logging
- sync 시작: `state_transition` 이벤트 (sync 시작 타임스탬프)
- 각 프로젝트 sync: `agent_complete` 이벤트 (프로젝트별 sync 결과)
- sync 완료: log에 sync 완료 타임스탬프 기록

## Portfolio 경로

기본값: `/home/coffin/dev/portfolio`
설정: `workspace/{project}/deploy.yaml`의 `portfolio_path`

## Process

### 1. 프로젝트 메타데이터 수집

각 `workspace/{project}/`에서:
- `content.json` → title, tagline, tech stack, sections
- `design-profile.yaml` → template, domain
- `deploy.yaml` → 배포 URL, 배포 대상

### 2. PortfolioSite 매핑

foliocraft의 `content.json`을 portfolio의 `PortfolioSite` 타입으로 변환:

```typescript
// content.json → PortfolioSite
{
  meta.title          → title
  meta.tagline        → desc
  tech_stack[].name   → tech[]
  deploy.url          → url
  deploy.status       → status ("production" | "active")
  features[].title    → projects[] (상위 3개)
}
```

### 3. projects.ts 업데이트

`portfolio/src/data/projects.ts`의 `portfolioSites` 배열을 업데이트:
- 이미 존재하는 프로젝트: URL, tech, status, desc 업데이트
- 새 프로젝트: 배열에 추가
- 삭제하지 않음 (foliocraft 외 수동 등록 프로젝트 보호)

### 4. resume.ts 연동 (선택)

`portfolio/src/data/resume.ts`의 `mainProjects`에서 매칭되는 프로젝트의 `live` URL 업데이트.

## Output

```
✔ Synced 3 projects to portfolio/src/data/projects.ts
  - n8n: url updated → https://tygwan.github.io/n8n/
  - DXTnavis: url updated → https://tygwan.github.io/DXTnavis/
  - bim-ontology: added (new)
```

## deploy.yaml Format

`/craft-deploy` 실행 후 자동 생성:

```yaml
# workspace/{project}/deploy.yaml
project: n8n
url: https://tygwan.github.io/n8n/
target: github-pages
deployed_at: 2026-02-21T12:00:00Z
template: sveltekit-dashboard
status: production
```

## Example

```
/craft-sync              # 모든 프로젝트 동기화
/craft-sync n8n          # n8n만 동기화
```
