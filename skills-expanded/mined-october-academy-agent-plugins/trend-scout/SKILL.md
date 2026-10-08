---
name: trend-scout
description: "Reddit, HN, GitHub, RSS, npm, Bluesky, Mastodon, 한국 커뮤니티까지 어제~오늘 뜨는 빌더/AI/오픈소스 시그널을 수집하고 Threads 포스트용으로 큐레이션. GitHub는 gh CLI 우선, 없으면 공개 REST API로 폴백. '지금 뜨는 것'을 넓게 스캔해 후보를 뽑는 큐레이션 전용 스킬이다. 특정 주제를 다각도로 파고드는 심층 리서치는 이 스킬이 아니라 deep-research(다중 소스 fact-check 리포트)·last30days(한 주제의 최근 30일 여론) 영역이다. 트리거: '트렌드', '인기글', 'trend scout', '쓰레드 리서치', 'threads 소재', '오늘 뭐 올리지', '콘텐츠 소재', 'reddit 인기글', 'HN 인기글', '깃허브 트렌드', '오픈소스 소재', '해커뉴스', '트렌드 스카우트', 'github trending', 'what is hot on hacker news', 'open source radar', 'reddit trending', 'trending packages', 'daily tech digest', 'tech news today', 'developer trends'. /trend-scout로 실행."
user-invocable: true
---

# Trend Scout

`insane-search`의 공개 소스 전략을 벤치마킹해서, "지금 뜨는 것"을 Threads 포스트 후보로 정리한다.

이 스킬은 여러 소스를 넓게 스캔해 오늘의 소재 후보를 뽑는 **큐레이션 전용**이다. 특정
주제 하나를 깊게 파고드는 리서치는 범위가 아니다 — 다중 소스 fact-check 리포트가
필요하면 `deep-research`, 한 주제의 최근 30일 여론·반응이 필요하면 `last30days`로 라우팅한다.

## Workflow

### 1. 데이터 수집

```bash
bash {SKILL_DIR}/scripts/fetch-trends.sh day 15
```

결과:
- `/tmp/trend-scout/all.json` — 정규화 + 중복 제거 + `trend_score` 정렬 결과
- `/tmp/trend-scout/{source}.json` — 소스별 raw 응답
- stdout — `all.json`과 동일한 통합 JSON

### 2. 1차 선별

기본은 `topics[]`를 본다. 호환용으로 `items[]`도 동일 내용을 가진다.

- `source`: 어떤 채널에서 왔는지 (`reddit`, `hackernews`, `clien`, `npm`, `bluesky` 등)
- `channel`: 서브레딧/피드/태그/보드
- `trend_score`: 교차 소스 비교용 가중 점수
- `summary`: selftext/description/본문 요약

소스별 해석과 벤치마킹 메모는 [references/sources.md](references/sources.md) 참고.

### 3. 부족한 경우에만 보강

기본 큐로 부족할 때만 Exa 같은 외부 검색을 덧댄다.

- 특정 버티컬만 더 필요할 때
- 기본 큐에 없는 사이트를 명시적으로 섞어 달라고 했을 때
- `insane-search`식 URL 우회/추출 계층이 필요한 경우

### 4. 필터링

기준:

- Reddit upvote 10+ (소규모 서브레딧 5+)
- HN score 50+
- Lobsters score 8+
- dev.to reactions 20+
- GitHub 신규 repo stars floor 적용
- 한국 커뮤니티/RSS는 위치 점수 + 주제성으로 선별
- 제외: 스팸, 구인글, 공지, 구체성 없는 동기부여 글

큐레이션 우선순위:
1. 실제 숫자 (MRR, 유저 수, 매출, 다운로드)
2. 반직관적 인사이트
3. 실행 가능한 전략
4. 실패/교훈 사례

### 5. Threads 포스트 작성

포맷은 [references/threads-format.md](references/threads-format.md) 참고.

핵심:
- 500자 이내
- 한국어 대화체
- 핵심부터
- 숫자/맥락 포함
- 원문 링크 1개

### 6. 출력

추천 포스트 3-5개:

```text
## 추천 #1: {주제}
- 소스: {source} | {channel} | score {trend_score}
- 링크: {URL}

### Threads 초안
{500자 이내 한국어 포스트}

### 큐레이션 이유
{1줄}
```

## 날짜 범위

- `day`: 최근 24시간
- `week`: 최근 7일
