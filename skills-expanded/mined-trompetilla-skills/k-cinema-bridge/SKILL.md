# k-cinema-bridge

한국 멀티플렉스(롯데시네마, CGV, 메가박스) 박스오피스 및 상영예정작 데이터를 제공하는 JSON API.
KOBIS(영화진흥위원회) 데이터로 보강된 장르, 감독, 배우 등 상세 정보를 포함한다.
데이터는 매일 00:00 UTC에 자동 갱신된다.

## API

- BASE_URL: `https://uyeong.github.io/k-cinema-bridge`
- 모든 엔드포인트는 인증 없이 GET 요청만으로 사용 가능
- info 필드가 null일 수 있으므로 반드시 null 체크 필요

| 엔드포인트 | 설명 |
|---|---|
| GET /api/boxoffice.json | 전체 소스 박스오피스 종합 (`{lotte, cgv, megabox}`) |
| GET /api/boxoffice/{source}.json | 소스별 박스오피스 (`BoxOfficeMovie[]`) |
| GET /api/upcoming.json | 전체 소스 상영예정작 종합 (`{lotte, cgv, megabox}`) |
| GET /api/upcoming/{source}.json | 소스별 상영예정작 (`UpcomingMovie[]`) |

source: `lotte` | `cgv` | `megabox`

## 데이터 구조

### BoxOfficeMovie

```
source: "lotte" | "cgv" | "megabox"
rank: number          -- 박스오피스 순위 (1부터 시작)
title: string         -- 영화 제목
rating: string        -- 관람 등급
posterUrl: string     -- 포스터 이미지 URL
info?: MovieInfo      -- KOBIS 상세 정보 (null일 수 있음)
```

### UpcomingMovie

```
source: "lotte" | "cgv" | "megabox"
title: string         -- 영화 제목
rating: string        -- 관람 등급
posterUrl: string     -- 포스터 이미지 URL
releaseDate: string   -- 개봉 예정일 (YYYY-MM-DD, 빈 문자열일 수 있음)
info?: MovieInfo      -- KOBIS 상세 정보 (null일 수 있음)
```

### MovieInfo

```
code, title, englishTitle, originalTitle: string
runtime: string (분)
productionYear, openDate (YYYYMMDD), productionStatus, type: string
nations: string[]     -- 제작 국가
genres: string[]      -- 장르
directors: {name, englishName}[]
actors: {name, englishName, role, roleEnglish}[]
showTypes: {group, name}[]
companies: {code, name, englishName, part}[]
audits: {number, grade}[]
staff: {name, englishName, role}[]
```

## 활용 가이드

### 현재 인기 영화 추천

트리거: "요즘 뭐 볼만해?", "영화 추천해줘"

GET /api/boxoffice.json으로 전체 멀티플렉스 박스오피스를 가져와 공통 상위권 영화를 파악한다.
rank가 낮을수록 상위, info.genres로 장르 안내 가능.

### 개봉 예정작 안내

트리거: "곧 개봉하는 영화 뭐 있어?", "다음 달 영화"

GET /api/upcoming.json으로 전체 상영예정작을 가져온다.
releaseDate(YYYY-MM-DD)로 날짜 필터링, info.genres/directors/actors로 상세 정보 제공.

### 장르/감독/배우 기반 검색

트리거: "액션 영화 뭐 해?", "봉준호 신작 나왔어?", "마동석 영화"

GET /api/boxoffice.json + GET /api/upcoming.json을 모두 조회 후 info 필드로 필터링.
- 장르: `movie.info?.genres.includes("액션")`
- 감독: `movie.info?.directors.some(d => d.name === "봉준호")`
- 배우: `movie.info?.actors.some(a => a.name === "마동석")`

### 관람 등급 기반 필터링

트리거: "아이랑 볼만한 영화", "전체관람가 영화 뭐 있어?"

rating 필드로 필터링. info 없이도 가능.
- "전체 관람가" | "12세 관람가" | "15세 관람가" | "청소년 관람불가"

### 특정 멀티플렉스 조회

트리거: "CGV에서 뭐 해?", "롯데시네마 상영작"

GET /api/boxoffice/{source}.json 또는 GET /api/upcoming/{source}.json
source는 "lotte" | "cgv" | "megabox".

### 멀티플렉스 간 비교

트리거: "CGV랑 메가박스 순위 차이 알려줘"

GET /api/boxoffice.json으로 종합 데이터에서 같은 title을 가진 영화의 rank를 비교한다.
