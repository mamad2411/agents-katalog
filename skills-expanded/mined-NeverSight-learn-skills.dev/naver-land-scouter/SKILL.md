---
name: naver-land-scouter
description: "네이버 부동산 데이터 탐색과 분석을 위한 스킬. 지도 기반 단지 탐색, 단지 심층 분석, 매물 비교, 투자 지표 산출, 학군/교통 요약 리포트 생성에 사용한다. Keywords: 네이버 부동산, 매물 찾기, 시세 분석, 단지 정보, 부동산 임장 보고서, naver land, complex, article, price, school, transportation"
---

# Naver Land Scouter

## 언제 이 스킬을 쓰는가
- 네이버 부동산 기준으로 단지, 매물, 실거래를 탐색해야 할 때 사용한다.
- `"구성역 주변 3억대 아파트"`처럼 위치 이름과 조건을 함께 다뤄야 할 때 사용한다.
- 여러 역세권이나 여러 중심점을 한 번에 스캔해 하나의 JSON으로 합쳐야 할 때 사용한다.
- 현재 호가가 최근 실거래 대비 비싼지 싼지를 빠르게 판단해야 할 때 사용한다.

## 이 스킬의 기본 원칙
1. 에이전트 후속 처리용 결과는 기본적으로 `--format json --output-file <path>`를 사용한다.
2. 위치가 문자열이면 먼저 `search` 또는 `discover --near`를 사용하고, 좌표를 외부에서 따로 찾으려 하지 않는다.
3. `"역 주변"` 여부는 이름이 아니라 `distanceMeters` 또는 `lat/lon` 기준으로 판단한다.
4. 결과가 0건이면 추측하지 말고 `filterStats`를 먼저 확인한다.
5. 세대수, 준공년도, 주차대수처럼 단지 메타데이터가 꼭 필요할 때만 `--enrich complex-summary`를 켠다.
6. `401/403/429`가 나와도 바로 실패로 끝내지 말고 세션 전략을 확인한다. 기본값 `auto`가 1차 대응이다.

## 먼저 고를 것
1. 위치를 찾는가
- `search`
2. 한 지점을 중심으로 단지를 찾는가
- `discover`
3. 여러 지점 결과를 합치는가
- `scan`
4. 특정 단지의 매물을 보는가
- `listings`
5. 특정 매물의 현재 호가와 실거래를 비교하는가
- `history`
6. 여러 매물을 직접 비교하는가
- `compare`
7. 갭, 수익률 같은 투자 지표가 필요한가
- `invest`

## 표준 작업 순서
1. 위치 확정
- `search "구성역"` 또는 `discover --near 구성역 --radius 500m`
2. 단지 후보 탐색
- `discover`
3. 단지별 매물 수집
- `listings --complex-no ...`
4. 필요 시 비교/해석
- `compare`, `history`, `invest`, `complex`
5. 여러 위치를 합쳐야 하면
- `scan`

## 출력 규칙
- 사람이 읽는 보고서가 필요하면 기본 하이브리드 출력을 사용한다.
- 에이전트가 다음 단계에서 다시 읽어야 하면 `--format json`을 사용한다.
- 결과가 길어질 수 있으면 반드시 `--output-file <path>`를 사용한다.
- `--output-file`을 쓰면 stdout에는 전체 payload 대신 파일 경로와 건수 요약만 출력된다.

JSON 최상위 키 규칙:
- `search` → `searchResult`
- `discover` → `discoveryResult`
- `listings` → `listingResult`
- `scan` → `scanResult`
- `history` → `historyResult`
- `complex` → `complexReport`
- `compare` → `comparisonResult`
- `invest` → `investmentIndicatorResult`

## 데이터 처리 규칙
1. 가격
- 모든 내부 계산과 JSON 값은 `만원 단위 int`로 처리한다.
- 예: `10억 5천` → `105000`

2. 면적
- `1평 = 3.3058㎡`
- 사용자가 `평`으로 말하면 내부적으로 `㎡`로 변환한다.
- 결과 보고 시에는 가능하면 `평`과 `㎡`를 함께 보여준다.

3. 향
- 코드: `S`, `SE`, `SW`, `E`, `W`, `N`, `NE`, `NW`
- 다중 선택은 `:`로 결합한다.
- 예: `S:SW:SE`

4. 거리
- `distanceMeters`는 기준 좌표가 있을 때만 신뢰한다.
- `"역 주변"` 같은 판단은 이름이 아니라 `distanceMeters` 기준으로 해야 한다.

## 자연어 해석 규칙
1. 가격 표현
- `"3억대"`는 기본적으로 `30000 ~ 39999`로 해석한다.
- `"3억 +- 5000"`은 `25000 ~ 35000`로 해석한다.
- `"5억 이하"`는 `price-max 50000`으로 해석한다.

2. 면적 표현
- `"20평대"`는 기본적으로 `20평 ~ 29평`으로 해석한다.
- `"30~40평"`, `"100-120m2"`, `"30 40"` 같은 범위 표현은 그대로 범위 필터로 넣는다.
- 단위가 생략된 범위 표현은 기본적으로 `평`으로 간주한다.

3. 역세권 표현
- `"역 주변"`은 기본적으로 `500m` 반경으로 시작한다.
- 결과가 너무 적으면 `700m`, `1000m` 순으로 넓힌다.

## 에이전트 판단 규칙
1. `0건` 해석
- `listings` 또는 `scan`에서 `filterStats.beforeCount = 0`이면 서버 응답 자체에 후보가 없다는 뜻이다.
- `filterStats.beforeCount > 0`이고 `afterCount = 0`이면 스킬 후처리 필터가 전부 제외한 것이다.
- `discover`에서 `filterStats`가 없으면 반경 후처리가 적용되지 않았거나, 서버가 이미 결과를 좁혀 준 상황으로 본다.

2. 조건 완화 순서
- 1차: 반경 확대 `500m -> 700m -> 1000m`
- 2차: 가격 범위 확대
- 3차: 공급면적 조건 완화
- 4차: 전용면적 후처리 필터 완화
- 위 순서를 바꾸지 않는다. 면적부터 먼저 풀면 사용자의 핵심 의도를 쉽게 잃는다.

3. 포함/제외 기본값
- 현재 `APT` 조회는 네이버가 `APT`로 돌려주는 항목을 그대로 수용한다.
- 따라서 `(도시형)` 같은 이름이 포함된 단지도 결과에 들어올 수 있다.
- 사용자가 `"일반 아파트"`를 명시하면 이름에 `(도시형)`이 붙은 항목과 명백한 비선호 유형을 설명 단계에서 제외한다.
- 사용자가 제외 조건을 주지 않았다면 결과는 우선 보존하고, 설명에서 유형을 명시한다.

4. 중복 처리
- `articleNo`가 있으면 `articleNo` 기준으로 중복 제거한다.
- `articleNo`가 없으면 `complexNo + price + exclusiveArea + floorInfo` 조합을 임시 키로 사용한다.
- `scan` 결과를 요약할 때는 같은 매물이 반복되더라도 먼저 dedupe한 뒤 추천 후보를 뽑는다.

5. 추천 정렬
- 탐색 단계 기본 정렬은 `distanceMeters asc -> price asc`다.
- 실거래 비교까지 끝난 추천 단계 기본 정렬은 `distanceMeters asc -> premiumRate asc -> price asc`다.
- `premiumRate`가 없으면 다시 `distanceMeters asc -> price asc`로 돌아간다.

## 세션 전략
- `auto`
  - 기본값
  - 먼저 공개 페이지 방문으로 익명 세션을 만들고, `401/403/429`가 나면 브라우저 부트스트랩으로 승격한다.
- `http`
  - 공개 페이지 방문만 수행한다.
- `browser`
  - 처음부터 Playwright 기반 브라우저 세션을 사용한다.
- `none`
  - 세션 부트스트랩을 하지 않는다.

추가 규칙:
- `articles/*` 계열은 익명 `Authorization: Bearer ...` 헤더가 필요한 경우가 있다.
- `auto`와 `browser`는 이 헤더를 브라우저 요청에서 캡처해 재사용한다.
- 브라우저 모드가 필요하면 한 번 `uv run playwright install chromium`이 필요할 수 있다.

## 명령 선택 가이드

### `search`
- 문자열 위치를 좌표 후보로 해석할 때 사용한다.
- `"구성역"`, `"기흥역"`, `"구갈동"`처럼 시작점이 문자열일 때 가장 먼저 고려한다.
- 기본 반경은 `700m`다.
- 결과에는 후보 좌표와, 단일 후보로 해석되면 주변 단지도 함께 포함될 수 있다.

권장 예시:
```bash
uv run --project . python -m scripts.cli \
  --format json \
  search 구성역
```

### `discover`
- 지도 중심점 또는 `--near` 문자열 기준으로 단지 목록을 찾을 때 사용한다.
- `--near`를 쓰면 내부 `search` 결과를 이용해 중심점을 잡는다.
- `--radius`는 bbox가 아니라 `직선거리 반경`으로 후처리된다.
- 기본 반경은 `500m`다.
- `--enrich complex-summary`를 주면 세대수, 준공년도, 주차대수를 보강한다.

권장 예시:
```bash
uv run --project . python -m scripts.cli \
  --format json \
  --output-file ./results/guseong-discover.json \
  discover \
  --near 구성역 \
  --radius 500m \
  --real-estate-type APT \
  --enrich complex-summary
```

### `listings`
- 특정 단지의 매물 목록이 필요할 때 사용한다.
- `--complex-no`가 필요하다.
- `--area-min/max`는 공급면적 기준 검색이다.
- `--exclusive-area-min/max`는 전용면적 기준 후처리 필터다.
- 결과가 0건이거나 예상보다 적으면 `filterStats`를 확인한다.

권장 예시:
```bash
uv run --project . python -m scripts.cli \
  --format json \
  --output-file ./results/complex-11084-listings.json \
  listings \
  --complex-no 11084 \
  --real-estate-type APT \
  --trade-type A1 \
  --price-min 25000 \
  --price-max 35000 \
  --area-min 20평 \
  --area-max 29평 \
  --exclusive-area-min 15평 \
  --exclusive-area-max 20평
```

### `scan`
- 여러 역이나 여러 중심점 결과를 한 번에 합칠 때 사용한다.
- `--near`를 여러 번 넣는다.
- 가격/면적/거래유형 필터를 함께 주면 단지 탐색 후 매물까지 확장한다.
- 에이전트가 벨트형 지역을 스캔할 때 가장 먼저 고려해야 하는 명령이다.

권장 예시:
```bash
uv run --project . python -m scripts.cli \
  --format json \
  --output-file ./results/giheung-belt.json \
  scan \
  --near 구성역 \
  --near 기흥역 \
  --near 어정역 \
  --radius 500m \
  --real-estate-type APT \
  --trade-type A1 \
  --price-min 25000 \
  --price-max 35000
```

### `history`
- 특정 매물 또는 단지의 실거래 추이를 볼 때 사용한다.
- 현재 호가 대비 실거래 기준 판단이 필요하면 가장 먼저 사용한다.
- 기본 비교 구간은 `1년`이다.
- 보조 지표로 `3년`, `10년` 요약을 함께 반환한다.
- `premiumSummary`는 현재 호가와 최근 `1년` 평균 실거래가 차이를 요약한다.

권장 예시:
```bash
uv run --project . python -m scripts.cli \
  --format json \
  history \
  --article-no 2612380492
```

### `complex`
- 단지 개요, 시세, 실거래, 학군, 교통을 한 번에 요약할 때 사용한다.
- 단지 리포트가 필요할 때 사용하고, 대량 스캔의 기본 명령으로 쓰지는 않는다.

### `compare`
- 선택된 여러 매물을 같은 기준으로 비교할 때 사용한다.
- 후보가 2개 이상으로 좁혀진 뒤 추천 근거를 만들 때 사용한다.

### `invest`
- 매매가와 전세가 차이, 수익률 같은 투자 지표가 필요할 때 사용한다.
- 현재는 투자 판단의 보조 지표로 사용하고, 위치 적합성 판단을 대신하지는 않는다.

## 에이전트가 따라야 하는 기본 워크플로우

### 1. `"구성역 주변 아파트"`처럼 위치가 문자열인 경우
1. `search 구성역`
2. 후보가 2개 이상이면 더 구체적인 질의로 다시 검색한다.
3. 단일 후보면 `discover --near 구성역 --radius 500m`
4. 필요한 단지에만 `listings --complex-no ...`

### 2. `"기흥구 3억대 역세권 아파트"`처럼 여러 역을 함께 봐야 하는 경우
1. `scan --near 구성역 --near 기흥역 --near 어정역 ...`
2. JSON 결과를 거리순, 가격순으로 정렬한다.
3. 상위 후보에만 `history` 또는 `compare`를 추가 호출한다.

### 3. `"이 매물이 실거래 대비 비싼가"`를 판단하는 경우
1. `history --article-no ...`
2. `premiumSummary.premiumRate`를 본다.
3. `windowSummaries`의 `1년`, `3년`, `10년` 흐름을 같이 본다.
4. 표본 수가 적으면 과도한 결론을 내리지 않는다.

## 에이전트가 바로 사용할 핵심 필드

### `discover` / `listings`
- `complexNo`
- `articleNo`
- `complexName`
- `articleName`
- `price`
- `supplyArea`
- `exclusiveArea`
- `dongName`
- `latitude`
- `longitude`
- `distanceMeters`
- `totalHouseholdCount`
- `completionYear`
- `parkingCount`
- `filterStats.beforeCount`
- `filterStats.afterCount`
- `filterStats.dropReasons`

### `search`
- `candidates`
- `nearbyComplexes`

### `scan`
- `targets`
- `items`
- `filterStats`

### `history`
- `currentAskingPrice`
- `premiumSummary.referenceTradeAveragePrice`
- `premiumSummary.premiumAmount`
- `premiumSummary.premiumRate`
- `premiumSummary.judgement`
- `windowSummaries`

## 실패 시 대처 규칙
1. `0건`
- `filterStats`를 먼저 본다.
- 전용면적, 반경, 가격 조건이 너무 좁은지 확인한다.

2. `401/403/429`
- 먼저 `--bootstrap-mode auto`인지 확인한다.
- 계속 막히면 `--bootstrap-mode browser`를 시도한다.
- 그래도 막히면 `--cookie`, `--header`, 환경 변수 주입을 사용한다.

3. 위치가 모호함
- `search` 결과 후보가 여러 개면 임의 선택하지 않는다.
- `"구성역 수인분당선"`처럼 더 구체적인 질의로 다시 검색한다.

4. 출력이 너무 큼
- `--output-file`을 사용한다.
- stdout 전체를 파싱하려 하지 않는다.

5. `--enrich complex-summary`가 느림
- 대량 스캔의 기본값으로 켜지 않는다.
- 상위 후보 단지에만 다시 호출한다.

## 빠른 시작 예시

### 역 주변 단지 찾기
```bash
uv run --project . python -m scripts.cli \
  --format json \
  --output-file ./results/guseong-discover.json \
  discover \
  --near 구성역 \
  --radius 500m \
  --real-estate-type APT
```

### 조건 매물 찾기
```bash
uv run --project . python -m scripts.cli \
  --format json \
  --output-file ./results/guseong-listings.json \
  listings \
  --complex-no 11084 \
  --real-estate-type APT \
  --trade-type A1 \
  --price-min 25000 \
  --price-max 50000 \
  --area-min 20평 \
  --area-max 29평
```

### 여러 역세권 통합 검색
```bash
uv run --project . python -m scripts.cli \
  --format json \
  --output-file ./results/giheung-scan.json \
  scan \
  --near 구성역 \
  --near 기흥역 \
  --radius 500m \
  --real-estate-type APT \
  --trade-type A1 \
  --price-min 25000 \
  --price-max 35000
```

### 현재 호가 vs 실거래 비교
```bash
uv run --project . python -m scripts.cli \
  --format json \
  history \
  --article-no 2612380492
```

## 추가 인증 주입 예시
```bash
uv run --project . python -m scripts.cli \
  --cookie "NID_SES=..." \
  --cookie "NID_AUT=..." \
  --header "Referer:https://new.land.naver.com/" \
  --header "User-Agent:Mozilla/5.0 ..." \
  listings \
  --complex-no 11084 \
  --real-estate-type APT \
  --trade-type A1
```

```bash
export NAVER_LAND_HEADERS='{"Referer":"https://new.land.naver.com/","User-Agent":"Mozilla/5.0 ..."}'
export NAVER_LAND_COOKIES='NID_SES=...; NID_AUT=...'
uv run --project . python -m scripts.cli \
  --format json \
  search 구성역
```

## 필요할 때만 읽을 참고 문서
- 엔드포인트 구조가 필요하면 `/Users/dhkim/workspace/toyprojects/ai-agent-skills/skills/naver-land-scouter/references/api_endpoints.md`
- 파라미터 코드가 필요하면 `/Users/dhkim/workspace/toyprojects/ai-agent-skills/skills/naver-land-scouter/references/param_dictionary.md`
- 차단/운영 정책이 필요하면 `/Users/dhkim/workspace/toyprojects/ai-agent-skills/skills/naver-land-scouter/references/ops_policies.md`
- 더 긴 시나리오 예시가 필요하면 `/Users/dhkim/workspace/toyprojects/ai-agent-skills/skills/naver-land-scouter/references/workflows.md`
