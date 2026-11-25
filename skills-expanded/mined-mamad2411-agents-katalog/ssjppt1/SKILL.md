---
name: ssjppt1
description: |
  신성진(CDSA) 스타일의 편집 가능한 실제 PowerPoint 강의안 PPTX 생성 스킬. cdsa-lecture-wiki가 회수한 강의 원장이나 첨부 자료를
  잉크블랙·다크브라운·크림의 에디토리얼 모노톤 + 카멜 단일 액센트,
  Pretendard(sans) 제목 + Noto Serif KR(장식 숫자)로 실습 중심 강의 슬라이드를 pptxgenjs로 찍어낸다.
  검증된 정본(assets/reference_deck.js, 39슬라이드)의 헬퍼와 슬라이드 패턴을 그대로 재사용해,
  내용 문자열만 새 주제로 교체하는 방식. 사용자가 "ssjppt1", "신성진 스타일 강의안", "강의안 PPT/pptx",
  "강의 슬라이드/deck을 PPTX로 만들어줘", "편집 가능한 파워포인트 강의안"을 요청하면 사용한다. HTML 산출물은 lecture-deck 또는 ssjhtml3을 사용한다.
  (문서형 한글 서식은 cdsa-hwptemp, 고밀도 레이아웃 규칙은 스킬에 내장되어 있다(slide-density 헌장 동일).)
---

# ssjppt1 — 신성진 스타일 강의안 PPTX

**`assets/reference_deck.js` 가 곧 표준이다.** 이 파일은 한국보건복지인재원 「AI 데이터 챔피언 양성교육(마라토너)」용으로 실제로 잘 나온 39슬라이드 강의안 생성기다(렌더 결과: `assets/reference_render.pdf`). 새 강의안은 **이 정본을 복사해 내용 문자열만 교체**하고, 생성 → PDF 렌더 → `slide-density` 검증까지 수행한다. 밑바닥부터 새 레이아웃을 설계하지 않는다 — 여백·그리드·겹침 방지·톤이 이미 정본에 녹아 있다.

## 워크플로우 (이 순서 그대로)

1. **작업 폴더 + 설치**
   ```bash
   mkdir -p work && cd work && npm init -y && npm install pptxgenjs
   ```
2. **정본 복사** — `assets/reference_deck.js` → `work/deck.js`, 그리고 `assets/dia_agent.png`·`dia_assist.png`도 같은 폴더로 복사(에이전트/어시스트 도식 슬라이드가 사용). 새 도식이 필요하면 아래 SVG→PNG로 만든다.
3. **내용 교체** — 헬퍼(rule/box/kicker/footer/header/blockLabel/card/sectionBreak/practice)와 팔레트 `C`·폰트 `F`/`SR`는 **건드리지 않는다**. 각 슬라이드 IIFE 안의 **문자열(제목·키커·본문·표 데이터)만** 새 주제로 바꾼다. 필요 없는 슬라이드는 IIFE 통째로 삭제, 새 슬라이드는 가장 비슷한 패턴을 복사해 만든다. `footer`의 과정명, `header`의 `CDSA`, 커버/클로징의 기관·발표자도 새 강의에 맞게 교체.
4. **출력 경로** — 맨 끝 `pptx.writeFile({fileName:'./강의안.pptx'})`를 원하는 경로로.
5. **생성** — `node deck.js` → `강의안.pptx`
6. **PPTX 수리 (필수 — 파워포인트 '복구' 오류 방지)** — pptxgenjs 산출물은 PowerPoint에서 "콘텐츠에 문제가 있습니다 → 복구"를 띄우는 경우가 있다(LibreOffice는 관대해서 통과시키므로 반드시 PowerPoint 기준으로 잡는다). 원인은 ① `[Content_Types].xml`이 실제로 없는 파트(`slideMaster2.xml`~`slideMasterN.xml`, 슬라이드마다 1개씩 잘못 등록)를 Override로 선언, ② zip 내 빈 디렉터리 항목. 생성 직후 수리 스크립트를 돌린다.
   ```bash
   python <이 스킬>/assets/fix_pptx.py 강의안.pptx      # 제자리 수리(원본은 .orig 백업)
   ```
   검증: `python -c "import zipfile,re; z=zipfile.ZipFile('강의안.pptx'); f=set(z.namelist()); from xml.etree import ElementTree as E; ns='{http://schemas.openxmlformats.org/package/2006/content-types}'; ct=E.fromstring(z.read('[Content_Types].xml')); print('없는Override:', [o.get('PartName') for o in ct.findall(ns+'Override') if o.get('PartName').lstrip('/') not in f])"` → `없는Override: []` 여야 정상.
7. **PDF 렌더 + 밀도 검증 (필수)**
   ```bash
   "/c/Program Files/LibreOffice/program/soffice.exe" --headless --convert-to pdf 강의안.pptx
   python -c "import fitz; d=fitz.open('강의안.pdf'); [d[i].get_pixmap(dpi=90).save(f'p{i+1:02d}.png') for i in range(len(d))]"
   for f in p*.png; do python ~/.claude/skills/slide-density/scripts/check_fill.py "$f"; done
   ```
   콘텐츠 슬라이드에 하단/내부 빈 밴드가 12% 초과면 → 본문을 늘리거나 박스 높이를 재분배해 PASS까지 반복. 표지·섹션브레이크·클로징은 의도적 여백이라 예외.

## 디자인 시스템

### 팔레트 (에디토리얼 모노톤 — 브라운 단색 + 크림 + 카멜 단일 액센트)
정본의 `C` 객체와 동일. **알록달록 금지**(파랑·초록·보라로 카드를 구분하지 않는다). 위계는 브라운 명도로만.

| 토큰 | HEX | 쓰임 |
|------|-----|------|
| `ink` | `1C1714` | 표지·섹션 배경, 강조/실습 박스 |
| `ink2` | `2A231D` | 본문 텍스트 |
| `esp` | `352720` | 표 헤더, 카드 제목, 배지 |
| `coffee` | `5C4733` | 보조 강조, 페이지번호 |
| `camel` / `camelLt` | `9C7B4D` / `C8A86E` | 유일한 포인트 액센트(룰·상단선·키커) |
| `cream` / `paper` | `F4EEE1` / `FBF8F1` | 강조 밴드 / 카드 배경 |
| `line` / `line2` | `DCD2C1` / `C9BC9E` | 보더·헤어라인 |
| `muted` / `faint` | `6E6253` / `9A8C7B` | 캡션·푸터 |

### 폰트
- **제목·본문 = `Pretendard`(sans)**, 굵기 `bold:true`. 제목에 세리프를 깔지 않는다.
- **`Noto Serif KR`(SR)는 장식 숫자에만** — 표지 대형 워터마크 숫자, 카드 01·02, 섹션 칩 번호. 그 외 세리프 남발 금지.
- 시스템에 Pretendard·Noto Serif KR이 설치돼 있어야 LibreOffice 렌더에 반영된다(미설치 시 대체). PPTX 파일 자체는 fontFace 이름을 담으므로 폰트가 있는 PC의 PowerPoint에서 정상 표시.

### 레이아웃 상수 (정본과 동일)
- 캔버스 16:9 = 13.33 × 7.5인치. 좌우 마진 `ML=0.55`, 콘텐츠 폭 `CW=12.23`.
- **헤더** `y 0.45~1.86`: 카멜 사각(0.16) + 키커(대문자·자간 2.5) + 25pt sans 제목 + 12.5pt 이탤릭 디스크립터 + 카멜 헤어라인. 우상단 `CDSA`.
- **콘텐츠** `y 2.05~6.95`. **푸터** `y 7.07`: 헤어라인 + 기관/과정명 + 페이지번호(우측 coffee).
- 하단 강조 밴드(cream 또는 ink)가 푸터와 겹치지 않게 끝 y 확인.


## 밀도·캔버스 채움 규칙 (slide-density 헌장 내장 — 이 절만으로 적용 가능)

**콘텐츠/데이터 장표에 강제 적용.** 표지·키노트 명제형·섹션 구분 같은 히어로 장표는 여백 예외(단, 콘텐츠가 캔버스 중앙에 균형 잡혀야 하며 한쪽으로 쏠리면 안 된다).
가장 흔한 위반 증상 = "상단 절반에 콘텐츠가 몰리고 하단이 비는 것".

1. **캔버스 역설계 (흐름 사고 금지)** — 13.33×7.5in(16:9) 고정 캔버스를 꽉 채우도록 역산해 배치한다.
   위에서부터 쌓다가 멈추지 않는다. 상·하 여백은 동일하게(각 4~6%).
2. **하단 앵커 먼저** — 앵커 바·푸터 등 하단 고정 요소부터 좌표를 잡아, 여백이 바닥에 고일 자리를 없앤다.
3. **세로 그리드 강제 (1행 금지)** — 세로를 3~5개 밴드로 나누고 각 밴드에 명시적 height를 할당한다.
   "헤더 + 1행 3열"로 끝내지 말 것. 상단=데이터(표·차트·매트릭스), 하단=인사이트/로드맵/액션/권고.
   1장당 의미 단위(exhibit) 4~7개.
4. **요소 stretch** — 표·차트·카드를 자연 크기로 두지 않는다. 배정된 밴드 높이를 꽉 채우도록
   행 높이·차트 높이를 키운다. 표 행 높이 = 밴드 높이 ÷ 행 수.
5. **빈 영역 금지 (정량 기준)** — 슬라이드 면적의 12%를 넘는 단일 빈 영역(특히 하단) 금지.
   가로로 10~20등분했을 때 어떤 띠도 비어 있으면 안 된다.
6. **렌더 후 자가검증 [필수]** — 만든 즉시 PNG로 렌더하고
   `python <이 스킬>/scripts/check_fill.py <png>` 실행(동일 스크립트가 `~/.claude/skills/slide-density/scripts/`에도 있다).
   FAIL이면 밴드 추가·높이 재분배 후 재렌더 → PASS까지 반복. "비었다"를 말로만 넘기지 않는다.

## 헬퍼 API (정본 상단에 정의)
| 함수 | 시그니처 | 그리는 것 |
|------|----------|-----------|
| `rule` | `(s,x,y,w,color?,h?)` | 얇은 가로 룰/헤어라인 |
| `box` | `(s,x,y,w,h,{fill,border,bw,r,topAccent,leftAccent})` | 라운드 박스(+ 상단/좌측 카멜 액센트) |
| `kicker` | `(s,x,y,text,color?,w?)` | 대문자·자간 넓은 소제목 |
| `header` | `(s,kicker,title,desc)` | 슬라이드 표준 헤더 한 세트 |
| `footer` | `(s,pageNo)` | 헤어라인 + 기관/과정명 + 페이지 |
| `blockLabel` | `(s,x,y,text,w?)` | 카멜 세로바 + 굵은 라벨(밴드 제목) |
| `card` | `(s,x,y,w,h,no,title,body,fill?)` | 번호(세리프)+제목+구분선+본문 카드 |
| `sectionBreak` | `(part,krTitle,enTitle,[[칩제목,칩설명]…])` | 다크 파트 전환 슬라이드(자동 addSlide+footer) |
| `practice` | `(s,x,y,w,h,lines)` | 잉크 박스 🎯 실습 (좌측 카멜 액센트) |

## 슬라이드 패턴 카탈로그 (정본에서 복사해 쓸 것)
- **표지**(L~52): 잉크 배경 + 대형 세리프 워터마크 숫자 + 카멜 배지 + 46pt 대제목 + 카멜 룰 + 발표자.
- **과정 개요**(그리드): 4열×n 카드(번호+제목+한줄) + 하단 cream 밴드 `blockLabel`.
- **타임테이블**: `addTable` 헤더 esp/흰글자, 교대행 paper, 하단 잉크 산출물 바.
- **섹션 브레이크**: `sectionBreak(...)` — PART·DAY 키커 + 38pt 대제목 + 4칩.
- **3카드 콘텐츠**(card ×3) + 하단 cream/ink 인사이트 밴드 — 가장 표준적인 콘텐츠 장표.
- **5단계 워크플로**: 5박스 + `›` 화살표 + 하단 실무핵심 밴드.
- **계층 리스트**(7계층): 한 줄=배지+제목+설명, 교대 배경.
- **2단 비교**: 좌우 box(topAccent camel/coffee) + 하단 잉크 선택기준 밴드.
- **5요소 필 로우**: 좁은 박스 5개 균등 + 아래 2단 보조 박스 + `practice`.
- **개념도**: `addImage(dia_*.png)` 좌 + 설명 box 우 + 하단 캡션.
- **실전 프롬프트**: 다크 카드(라벨 배지 + 예문) 2열×3행.
- **안전 4카드 / 클로징**: 마무리 장표.

## SVG → PNG 개념도 (필요할 때만)
도식 슬라이드용 이미지는 SVG만 담은 HTML을 Chrome으로 캡처해 만든다.
```bash
DW="$(pwd -W)"
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless --disable-gpu \
  --user-data-dir="$DW/_c" --screenshot="$DW/dia.png" --window-size=760,400 \
  --default-background-color=00000000 "file:///$DW/dia.html"
```

## 주의
- **Chrome print-to-pdf/스크린샷의 file:// URL은 반드시 Windows 경로**(`$(pwd -W)`). POSIX `/c/...`를 넣으면 빈 페이지가 나온다. 브라우저가 실행 중이면 고유 `--user-data-dir`로 새 인스턴스.
- pptxgenjs 색상은 6자리 HEX만(빈 문자열·3자리 금지).
- 분량은 요청에 맞춘다 — 짧은 특강이면 정본에서 파트·슬라이드를 덜어내고, 종합 교육이면 패턴을 복제해 늘린다.

## 참고 파일
- `assets/reference_deck.js` — 표준 생성기(39슬라이드, 헬퍼+모든 패턴). **복사해서 시작.**
- `assets/reference_render.pdf` — 정본 렌더 결과(디자인 눈으로 확인).
- `assets/dia_agent.png` · `assets/dia_assist.png` — 개념도 슬라이드용 이미지.
