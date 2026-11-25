---
name: geo-kr
description: 지역+업종 AI 검색(예: "강남 허리 잘 보는 한방병원", "행복동 김밥집 추천")에서 우리 사업체가 ChatGPT·Gemini·Perplexity·구글 AI 답변에 인용되게 만드는 한국형 GEO(지역검색최적화) 방법. 사용자가 "GEO", "지역검색최적화", "지역 SEO", "로컬 SEO", "동네 검색", "지역 AI 검색", "우리 가게가 AI에 안 나온다", "네이버 플레이스 말고 챗GPT에 뜨게", "시/군/구 + 업종 검색", "지역 롱테일", "areaServed/LocalBusiness 스키마", "출장 지역 노출", "지점별 지역 노출"을 말하거나, 소상공인·자영업·병원·학원·미용실·식당 등이 광고비 없이 동네 손님을 AI 검색으로 끌어오려 할 때 발동. 전국·비지역 AI 검색 인용은 aeo-kr, 네이버 검색·스마트플레이스 노출은 naver-seo-kr 스킬 참고.
metadata:
  version: 1.0.0
---

# GEO 지역검색최적화 (한국)

당신은 한국 소상공인·1인 사업자를 위한 GEO(Generative Engine Optimization, 지역검색최적화) 전문가다. 목표는 **"지역명 + 업종"으로 AI에게 물었을 때 사용자의 사업체가 AI 답변 안에 인용·추천되도록** 페이지를 구조화하는 것이다. 광고비·유료 API·유료 툴 없이, 순수하게 페이지 구조와 텍스트·스키마만으로 실행한다.

이 스킬은 실제 국내 사례에서 검증된 구조를 방법론으로 정리한 것이다. 사용자에게 없는 실적·후기·순위를 지어내는 데 쓰지 말 것(아래 "정직성" 섹션 필수).

---

## 1. 언제 쓰나

- "우리 동네 손님이 요즘 네이버 대신 ChatGPT/제미나이한테 가게를 물어본다"
- "네이버 플레이스는 등록했는데 AI 검색에는 우리가 안 나온다"
- "지역명 + 업종(예: 대구 필라테스, 마포 필라테스)으로 검색될 때 우리가 뜨게 하고 싶다"
- 출장/방문 서비스라 여러 시·군·구를 커버해야 한다
- 지점이 여러 개라 지점별로 동네 검색을 잡아야 한다

전국·글로벌 규모의 비지역 AI 검색은 `aeo-kr` 스킬, 네이버 검색·스마트플레이스 노출은 `naver-seo-kr` 스킬을 병행 참고한다.

---

## 2. GEO가 무엇인가 (한 줄 정의)

> **GEO는 "이 동네에서 OO 잘하는 곳" 같은 지역+업종 질문에 AI가 우리 사업체를 답하게 만드는 작업이다.** 네이버 지도 순위가 아니라, ChatGPT·Gemini·Perplexity·구글 AI Overviews가 **직접 읽고 추려서 답변 문장 안에 우리 이름을 넣게** 하는 것.

핵심 차이:
- **기존 SEO / 네이버 광고** → "순위"를 산다. 광고 끄면 사라진다.
- **GEO** → AI가 "인용"하게 만든다. 페이지가 살아있는 동안 누적되는 자산. 광고비로 순서를 살 수 없다(AI 지역 추천은 광고 상품이 아직 아니다).

---

## 3. 네이버 플레이스 · 구글 비즈니스 · GEO 역할 구분

**GEO는 네이버 플레이스를 대체하지 않는다. 보완한다.** 셋 다 하는 게 정석이다.

| 채널 | 어디서 잡히나 | 반드시 할 일 | 한계 |
|------|--------------|-------------|------|
| **네이버 스마트플레이스/플레이스** | 네이버 지도·통합검색 | 무료 등록·정보 최신화(필수 기본) | 네이버 밖(ChatGPT·Gemini)에서는 거의 안 잡힘. 한 줄짜리 구조화 정보라 AI가 풍부한 답변으로 못 만듦 |
| **구글 비즈니스 프로필** | 구글 지도·로컬·AI Overviews | 무료 등록·카테고리/영업시간 정확히 | 구글 생태계 위주 |
| **GEO 지역 페이지(이 스킬)** | ChatGPT·Gemini·Perplexity·구글 AI + 웹검색 | 지역×업종 전용 페이지 + 스키마 + 직답 | 검색 반영에 1~4주 시간 필요, 폐쇄하면 답변에서도 빠짐 |

지도 등록은 "핀 꽂기", GEO는 "AI가 읽을 문서 만들기"다. 지도만으로 AI 답변에 못 들어가는 이유는, 지도 데이터가 사업체당 한 줄짜리 필드라 AI가 근거로 인용할 서술형 콘텐츠가 없기 때문이다.

---

## 4. 실행 6단계 개요

```
1) 지역×업종 자연어 검색어 매트릭스 설계
2) 지역×업종 전용 페이지 제작 (한 페이지 = 한 지역+업종)
3) 직답 블록(Direct Answer) 심기
4) Schema.org 구조화 데이터(LocalBusiness·areaServed·FAQ) 삽입
5) 시·군·구 커버리지 전략 적용
6) AI 크롤러 허용 + llms.txt + 색인 요청
```

아래 사업체가 가상의 **"행복동 김밥집"**(경기도 OO시 행복동 소재)이라고 가정하고 예시를 든다. 실제 작업 시 지역·업종·사업체 정보로 치환한다.

---

### 1단계 — 지역×업종 자연어 검색어 매트릭스 설계

사람은 딱딱한 키워드로 안 묻는다. **자기 상황과 감정을 그대로** 묻는다. 이 자연어 롱테일을 먼저 수십 개 뽑는 게 GEO의 절반이다.

**롱테일 공식:**
```
[지역 표현] + [업종/메뉴] + [상황·감정·조건] + [의도]
```
- 지역 표현: 시 / 구 / 동 / 역 / 인근 랜드마크 (사람마다 부르는 단위가 다르다 → 다층으로)
- 상황·감정: "처음 가도 편한", "가족이랑 가도 안 후회하는", "안 속이고 정직하게", "새벽에 급하게", "혼밥 눈치 안 보이는"
- 의도: 추천 / 후기 / 가격 / 예약 / 포장 / 주차

**매트릭스 예시 (행복동 김밥집):**

| 자연어 검색어 | 숨은 상황(페르소나) |
|--------------|-------------------|
| "행복동에서 아침 일찍 하는 김밥집" | 출근길 직장인, 문 연 곳 급함 |
| "OO역 근처 혼밥하기 편한 분식집" | 혼밥 눈치 싫은 대학생 |
| "행복동 아이 데리고 가도 되는 김밥집" | 어린 자녀 부모 |
| "OO동 포장 빠른 김밥 추천" | 점심시간 5분 |
| "행복동 야채 많은 건강한 김밥" | 다이어트/건강식 |
| "OO시 단체 주문 되는 분식집" | 회사 간식 담당 |

30~50개를 목표로 한다. 지역 단위(시/구/동/역)를 바꿔가며 곱하면 금방 늘어난다.

> **관광지·외국인 상권 팁:** 여행객·외국인은 ChatGPT로 가게를 찾는 비율이 높다. "제주 현지인이 가는 흑돼지집", "Hongdae restaurant English menu" 같은 영문/여행객 자연어도 매트릭스에 넣는다.

---

### 2단계 — 지역×업종 전용 페이지 (한 페이지 = 한 지역+업종)

**원칙: 한 페이지에 여러 지역을 욱여넣지 않는다.** 지역별·지점별로 페이지를 분리해야 각 지역 검색에 또렷하게 잡힌다.

한 지역 페이지가 담아야 할 것:
1. **지역명이 들어간 제목/H1** — "행복동 김밥집 | OO시 행복동 아침·포장·단체주문"
2. **직답 블록**(3단계)
3. **그 지역 사람이 묻는 자연어 질문에 답하는 본문** — 위 매트릭스를 H2/H3 제목으로 전개
4. **사실 정보 표** — 영업시간, 위치/접근성(가까운 역·랜드마크), 주차, 포장/배달, 메뉴·가격대, 결제수단
5. **지역 맥락** — 주변 상권, 인근 동·역, (해당 시) 출장/배달 가능 범위
6. **FAQ** — 자연어 질문 6~12개 (4단계 스키마와 짝)
7. **구조화 데이터**(4단계)

메타 태그(head)에 지역 신호를 넣는다:
```html
<meta name="geo.region" content="KR-41"><!-- 시도 ISO 코드 -->
<meta name="geo.placename" content="경기도 OO시 행복동">
<link rel="canonical" href="https://example.com/happy-gimbap.html">
```

---

### 3단계 — 직답 블록 (Direct Answer)

AI는 페이지가 아니라 **문장(passage)**을 인용한다. 페이지 맨 위에 질문의 답을 40~60자로 **자기완결적으로** 박아둔다. 앞뒤 문맥 없이도 그 문장만 떼어 쓸 수 있어야 한다.

```html
<section>
  <h2>한 줄 답변</h2>
  <p><strong>행복동 김밥집은 OO시 행복동에서 아침 7시부터 문을 여는 분식집으로,
  포장·단체주문·아이 동반 식사가 가능합니다.</strong>
  OO역에서 도보 5분, 매장 앞 주차 2대.</p>
</section>
```

각 H2 섹션도 "직답 먼저, 설명 나중" 순서로 쓴다. 결론을 문단 끝에 숨기지 않는다.

---

### 4단계 — Schema.org 구조화 데이터 (JSON-LD)

지역 사업체의 핵심은 **LocalBusiness + areaServed(AdministrativeArea) + FAQPage + BreadcrumbList**를 `@graph`로 묶는 것. `<head>`나 `</body>` 직전에 넣는다.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "LocalBusiness",
      "@id": "https://example.com/happy-gimbap.html#business",
      "name": "행복동 김밥집",
      "description": "OO시 행복동의 분식집. 아침 영업·포장·단체주문 가능.",
      "url": "https://example.com/happy-gimbap.html",
      "telephone": "+82-31-000-0000",
      "priceRange": "₩",
      "image": "https://example.com/images/store.jpg",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "행복로 00",
        "addressLocality": "OO시",
        "addressRegion": "경기도",
        "postalCode": "00000",
        "addressCountry": "KR"
      },
      "geo": { "@type": "GeoCoordinates", "latitude": 37.0, "longitude": 127.0 },
      "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
        "opens": "07:00", "closes": "20:00"
      }],
      "areaServed": [
        { "@type": "AdministrativeArea", "name": "OO시 행복동" },
        { "@type": "AdministrativeArea", "name": "OO시 이웃동" },
        { "@type": "City", "name": "OO시" }
      ],
      "hasMap": "https://map.naver.com/...",
      "sameAs": [
        "https://map.naver.com/...",
        "https://www.google.com/maps/..."
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "행복동 김밥집은 아침 몇 시부터 하나요?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "평일·토요일 오전 7시에 문을 엽니다. 출근길 포장 주문이 많아 아침 시간대도 대기 없이 빠르게 준비됩니다."
          }
        },
        {
          "@type": "Question",
          "name": "단체 주문이나 회사 간식 대량 주문 되나요?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "가능합니다. 전날 또는 당일 오전 예약 주문을 받으며, 20인분 이상은 배달 범위를 전화로 안내합니다."
          }
        }
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type":"ListItem","position":1,"name":"홈","item":"https://example.com/"},
        {"@type":"ListItem","position":2,"name":"행복동 김밥집","item":"https://example.com/happy-gimbap.html"}
      ]
    }
  ]
}
</script>
```

**규칙:**
- `LocalBusiness`는 업종에 맞는 하위 타입으로 바꾸면 더 좋다: 식당 `Restaurant`, 미용실 `HairSalon`, 병원 `MedicalClinic`/`Dentist`, 카페 `CafeOrCoffeeShop`, 헬스장 `HealthClub`, 학원 `EducationalOrganization`, 정비소 `AutoRepair`, 변호사 `LegalService`, 부동산 `RealEstateAgent`, 숙박 `LodgingBusiness`.
- **출장/방문 서비스**면 `areaServed`에 실제 커버하는 시·군·구를 나열한다. AI가 "그 지역까지 가능하다"를 읽는다.
- **FAQ 스키마 텍스트와 화면에 보이는 FAQ 문구가 일치**해야 한다. 화면에 없는 걸 스키마에만 넣지 말 것(구글 위반).
- **없는 사실을 스키마에 넣지 않는다.** `aggregateRating`은 실제 검증 가능한 리뷰가 있을 때만.
- 검증: 구글 Rich Results Test(search.google.com/test/rich-results), Schema.org Validator(validator.schema.org) — 둘 다 무료.

---

### 5단계 — 시·군·구 커버리지 전략

| 상황 | 전략 |
|------|------|
| **대도시·광역시(서울/부산/대구 등)** | 시 단위로는 경쟁이 심해 인용이 어렵다. **구·동·역 단위로 쪼개서** 각각 페이지/섹션을 만든다. "강남 X"보다 "역삼동 X", "선릉역 X"가 더 또렷하게 잡힌다 |
| **중소도시·군·읍면** | 경쟁자가 적어 **시 단위 단독 인용**이 쉽다. 노출 효과가 더 빠르게 나타난다. 여기가 오히려 GEO 가성비 최고 구간 |
| **다지점** | 지점마다 **별도 페이지**. 지점별로 지역명·특화 메뉴·접근성을 다르게 쓴다. 한 페이지로 묶으면 어느 동네에도 안 잡힌다 |
| **출장/방문 서비스** | 서비스 반경 시·군·구를 `areaServed`에 나열 + 본문에도 "OO시·OO군 출장 가능" 명시 |
| **관광지** | 여행객 자연어(현지인 맛집, 오션뷰, 가족 펜션)와 생활권 검색을 분리 설계 |

인구가 적은 동네라고 포기하지 않는다. 지역+업종 검색은 **"지금 당장 갈 곳"을 찾는 검색**이라 전환율이 일반 검색보다 훨씬 높다.

---

### 6단계 — AI 크롤러 허용 + llms.txt + 색인 요청

**AI 봇을 막아두면 그 AI는 절대 우리를 인용 못 한다.** `robots.txt`에서 다음이 `Disallow` 안 됐는지 확인한다(모두 무료):

```
# robots.txt — AI 크롤러 허용 (역할 3분류)

# ① 검색 노출용 봇 — AI 답변 인용에 핵심 (허용 권장)
User-agent: OAI-SearchBot     # OpenAI/ChatGPT 검색
Allow: /
User-agent: PerplexityBot     # Perplexity 검색
Allow: /
User-agent: Claude-SearchBot  # Claude 검색
Allow: /

# ② 사용자 요청용 봇 — 사용자가 그 링크를 열어달라 할 때 (허용 권장)
User-agent: ChatGPT-User      # ChatGPT 사용자 요청
Allow: /
User-agent: Claude-User       # Claude 사용자 요청
Allow: /

# ③ 모델 학습용 봇 — 내 콘텐츠를 학습에 줄지 여부 '선택'
User-agent: GPTBot            # OpenAI 학습
Allow: /
User-agent: Google-Extended   # Gemini 학습·grounding (※Google 일반검색 랭킹과 무관)
Allow: /
User-agent: ClaudeBot         # Anthropic 학습
Allow: /

Sitemap: https://example.com/sitemap.xml
```

**AI 크롤러는 역할이 3가지로 나뉜다 — 뭉뚱그리면 안 된다:**

- **① 검색 노출용(허용 권장)** — AI가 실시간으로 웹을 검색해 답변에 인용할 때 쓰는 봇. **AI 검색 인용의 핵심.** `OAI-SearchBot`(OpenAI/ChatGPT 검색), `PerplexityBot`(Perplexity 검색), `Claude-SearchBot`(Claude 검색) 등.
- **② 사용자 요청용(허용 권장)** — 사용자가 AI에게 "이 링크 열어줘"라고 할 때 해당 페이지를 가져오는 봇. `ChatGPT-User`, `Claude-User`.
- **③ 모델 학습용(허용은 '선택')** — 내 콘텐츠를 AI 모델 **학습에 줄지 여부**의 문제로, 검색 인용과는 별개다. `GPTBot`(OpenAI 학습), `Google-Extended`(Gemini 학습·grounding — ※Google 일반검색 랭킹과는 무관), `ClaudeBot`(Anthropic 학습).

> **핵심:** AI 검색 인용을 노리면 **`OAI-SearchBot`·`PerplexityBot` 같은 '검색봇' 허용이 핵심**이고, **`GPTBot`·`Google-Extended` '학습봇' 허용은 별개의 선택**이다. 검색봇을 막으면 그 AI는 실시간 검색에서 우리를 절대 인용하지 못한다. 학습봇 허용은 브랜드가 모델 지식에 녹아드는 데 도움이 될 수 있으나 필수는 아니다.

**`/llms.txt`** (사이트 루트, 무료): 사업체가 뭐 하는 곳인지·주요 지역 페이지 링크를 마크다운으로 정리.
```markdown
# 행복동 김밥집
경기도 OO시 행복동 분식집. 아침 영업·포장·단체주문.

## 지역 페이지
- [행복동 김밥집](https://example.com/happy-gimbap.html): 영업시간·메뉴·위치·FAQ
```

**색인 요청(무료):**
- 구글 서치 콘솔 → URL 검사 → 색인 요청
- 네이버 서치어드바이저 → 웹페이지 수집 요청
- `sitemap.xml`에 모든 지역 페이지 등록

---

## 5. 지역 페이지 HTML 골격 (복사용)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>행복동 김밥집 | OO시 행복동 아침·포장·단체주문 분식집</title>
  <meta name="description" content="OO시 행복동 김밥집. 오전 7시 오픈, 포장·단체주문·아이 동반 가능. OO역 도보 5분, 주차 가능.">
  <meta name="geo.region" content="KR-41">
  <meta name="geo.placename" content="경기도 OO시 행복동">
  <link rel="canonical" href="https://example.com/happy-gimbap.html">
  <!-- 4단계 JSON-LD @graph 여기 -->
</head>
<body>
  <main>
    <h1>행복동 김밥집 — OO시 행복동 아침·포장 분식</h1>

    <section><h2>한 줄 답변</h2>
      <p><strong>행복동 김밥집은 OO시 행복동에서 오전 7시부터 여는 분식집으로,
      포장·단체주문·아이 동반이 가능합니다.</strong> OO역 도보 5분, 주차 2대.</p>
    </section>

    <section><h2>행복동에서 아침 일찍 하는 김밥집을 찾는다면</h2>
      <p>직답 먼저, 그다음 근거·정보.</p></section>

    <section><h2>위치·영업시간·주차</h2>
      <table>
        <tr><th>주소</th><td>OO시 행복로 00 (행복동)</td></tr>
        <tr><th>영업시간</th><td>월~토 07:00–20:00</td></tr>
        <tr><th>가까운 역</th><td>OO역 도보 5분</td></tr>
        <tr><th>주차</th><td>매장 앞 2대</td></tr>
        <tr><th>포장/단체</th><td>포장 가능, 20인분+ 예약주문</td></tr>
      </table>
    </section>

    <section><h2>자주 묻는 질문</h2>
      <details><summary>아침 몇 시부터 하나요?</summary>
        <p>평일·토요일 오전 7시에 엽니다. 출근길 포장도 대기 없이 준비됩니다.</p></details>
      <details><summary>단체 주문 되나요?</summary>
        <p>가능합니다. 당일 오전 예약 주문을 받고, 20인분 이상은 배달 범위를 전화로 안내합니다.</p></details>
    </section>
  </main>
</body>
</html>
```

무료로 만들 수 있는 곳: GitHub Pages, Cloudflare Pages, Netlify(무료 티어), 또는 기존 홈페이지/블로그에 페이지 추가. 워드프레스면 Yoast/Rank Math 무료 플러그인으로 스키마 삽입 가능.

---

## 6. 한국 현실 체크 (네이버·카카오·한국어)

- **네이버 플레이스/구글 비즈니스 먼저.** GEO는 그 위에 얹는 것. 지도 등록 없이 GEO만 하지 말 것.
- **한국어 자연어는 조사·구어체가 다양하다.** "~잘하는 곳", "~괜찮은 데", "~어디가 나아?", "~추천 좀" 같은 변형을 매트릭스에 넣는다.
- **동네 부르는 단위가 사람마다 다르다.** 시·구·동·역·아파트단지·랜드마크(예: "OO초 근처")를 다층으로.
- **문의 채널은 카카오톡 채널이 현실적이다.** 페이지에 카톡 채널/전화를 눈에 보이게(전화번호는 스키마 `telephone`에도).
- **자바스크립트로만 렌더링되는 정보는 AI가 못 읽는다.** 핵심 정보(영업시간·주소·메뉴)는 HTML 텍스트로 보이게.

---

## 7. 정직성 · 표시광고법 (반드시 지킬 것)

GEO는 없는 걸 지어내는 기술이 아니다. 한국 **표시·광고의 공정화에 관한 법률**과 각 업종 광고 규정을 위반하면 페이지가 문제되고 AI 신뢰도도 떨어진다.

- **근거 없는 최상급 금지.** "최고", "1위", "유일", "전국 No.1", "확실히 낫는다"를 객관적 근거 없이 쓰지 않는다. 근거가 있어도 출처·기준·시점을 함께 밝힌다.
- **가짜 후기·별점·실적 창작 금지.** 리뷰 스키마(`aggregateRating`)는 실제 검증 가능한 리뷰가 있을 때만. AI는 과장·거짓을 걸러내고, 발각 시 신뢰를 잃는다.
- **의료·법률·금융은 결과 단정 금지.** "완치", "무조건 승소", "수익 보장" 대신 "상담 가능", "진료 안내" 톤. 의료광고는 사전심의·과장금지 규정을 따른다.
- **부풀린 수치 금지.** "손님 300% 증가" 같은 숫자는 실측 근거 없이 쓰지 않는다.
- **사실 위주로.** 영업시간·위치·메뉴·전문 분야 같은 검증 가능한 사실이 오히려 AI 인용률을 높인다(구체 정보 +citation).

> 정직한 구체 정보 = 표시광고법도 안전 + AI 인용도 잘 됨. 두 마리 토끼가 같은 방향이다.

---

## 8. 최종 체크리스트

지역 페이지마다 확인:

- [ ] 제목·H1에 **지역명 + 업종**이 들어갔다
- [ ] 맨 위에 40~60자 **직답 블록**(자기완결 문장)이 있다
- [ ] 그 지역 사람의 **자연어 질문**이 H2/H3와 FAQ로 30~50개 반영됐다
- [ ] 영업시간·주소·접근성·주차·가격대 등 **사실 정보 표**가 있다
- [ ] **LocalBusiness + areaServed + FAQPage + BreadcrumbList** JSON-LD가 있다
- [ ] 스키마와 화면 텍스트가 **일치**한다 / 없는 사실을 넣지 않았다
- [ ] 광역시는 **구·동 단위**로 쪼갰다 / 다지점은 **페이지 분리**했다
- [ ] `robots.txt`에서 **AI 봇을 안 막았다**
- [ ] `llms.txt` + `sitemap.xml` 있고, 구글·네이버에 **색인 요청**했다
- [ ] 네이버 플레이스·구글 비즈니스 **등록·최신화**돼 있다
- [ ] **표시광고법**: 근거 없는 최상급·가짜 후기·결과 단정 없음
- [ ] Rich Results Test / Schema Validator **통과**

---

## 9. 하지 말아야 할 것

1. **한 페이지에 모든 지역 몰아넣기** — 어느 동네에도 안 잡힌다. 지역별 분리.
2. **키워드 도배** — 오히려 AI 가시성을 떨어뜨린다. 자연스러운 문장으로.
3. **네이버 플레이스 건너뛰기** — GEO는 보완재지 대체재가 아니다.
4. **AI 봇 차단** — 막으면 그 AI는 영원히 인용 못 한다.
5. **JS로만 렌더되는 정보** — AI·크롤러가 빈 페이지로 본다.
6. **가짜 실적·후기·순위 창작** — 표시광고법 위반이자 AI 신뢰 상실.
7. **지도 등록으로 끝내기** — 한 줄 데이터라 AI가 인용할 서술이 없다.

---

## 10. 무료 모니터링 (DIY, 유료 툴 0원)

한 달에 한 번:
1. 우리 지역+업종 자연어 질문 10~20개를 고른다.
2. 각각을 **ChatGPT·Gemini·Perplexity·구글**에 직접 물어본다(PC/모바일 둘 다, 지역 키워드 포함).
3. 기록한다: 우리가 인용됐나? 누가 인용됐나? 어느 페이지가 근거로 걸렸나?
4. 스프레드시트에 월별로 추적하고, 안 잡힌 질문은 그 자연어를 페이지 H2/FAQ로 보강한다.

반영에는 보통 1~4주 걸린다. 안 잡히면 (1) 직답 블록이 그 질문에 정확히 답하는지 (2) 스키마가 유효한지 (3) AI 봇이 안 막혔는지 순서로 점검한다.

---

## 관련 스킬

- **aeo-kr**: 지역이 아닌 전국·비지역 AI 답변엔진(AEO) 인용 최적화
- **naver-seo-kr**: 네이버 검색·스마트플레이스 노출 최적화 (GEO의 필수 기반 채널)
- **local-customer-finder-kr**: 지역 고객 발굴·유입 채널 확장

---

## 참고자료 (references/)

아래 파일들은 **범용 AI가 흔히 틀리는 정확한 한국 사실·정책·데이터**를 담고 있다. 정확한 조문·수치·절차·코드가 필요할 때는 기억이 아니라 이 파일을 근거로 삼아라.

- `references/지역-업종-롱테일-패턴.md` — 전국 17개 시도 × 업종별 자연어 지역검색 질문 패턴 카탈로그(1단계 매트릭스 설계 시 지역·업종별 실제 롱테일 근거로 사용).
- `references/localbusiness-스키마.md` — LocalBusiness + areaServed 지역 세분화 스키마 완성 예시(4단계 JSON-LD 작성 시 areaServed·업종 하위타입·행정구역 구조의 정확한 레퍼런스).
