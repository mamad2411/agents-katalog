---
name: cs-doc-html
description: cs/ 디렉토리의 학습용 마크다운 가이드(난이도·선수지식·키워드·코드·Mermaid 포함)를 공유·오프라인용 자체완결 단일 HTML 파일로 변환한다. 마크다운만으로는 표·다이어그램·코드·목차가 눈에 잘 안 들어올 때, "이 cs 문서 HTML로 뽑아줘/변환해줘", "서버 안 띄우고 예쁘게 렌더링", "오프라인·슬랙으로 공유할 단일 html", "난이도 배지·키워드 칩 들어간 보기 좋은 페이지", "cs-html 생성", "카테고리 문서 일괄 html" 같은 요청에 적극 사용한다. cs/ 학습 문서를 파일 하나로 브라우저에서 보거나 남에게 보낼 때가 핵심 용도다. 단, 워크플로우 산출물(WORK-SPEC·SELF-REVIEW 등)의 HTML 생성은 html-doc 스킬이, 여러 문서를 서버로 띄워 브라우징하는 것은 cs-web이 담당하므로 그 경우엔 쓰지 않는다. 일반 웹페이지·코드 스니펫 HTML 제작, 마크다운 편집·신규 작성, PDF 변환도 대상이 아니다. 원본 .md는 건드리지 않는다.
---

# cs-doc-html — CS 학습문서 → 자체완결 HTML

`cs/` 학습 마크다운 한 개(또는 여러 개)를 외부 의존이 전혀 없는 단일 `.html`로 변환한다. 인라인 CSS/SVG, 라이트·다크 자동, 난이도 배지·선수지식·키워드 칩·자동 TOC·코드 라벨·Mermaid 인라인 SVG 렌더를 포함한다.

## 언제 쓰나 / 안 쓰나

- **쓴다**: `cs/**/*.md` 학습 문서를 브라우저에서 보기 좋게, 또는 파일 하나로 공유/오프라인 열람하고 싶을 때.
- **안 쓴다**: 워크플로우 *산출* 문서(WORK-SPEC·SELF-REVIEW 등)는 [`html-doc`](../html-doc/SKILL.md) 스킬이 담당한다. 여러 문서를 동적으로 브라우징만 하려면 `cs-web` 서버를 띄우는 편이 낫다(이 스킬은 정적 단일 파일 생성용).

## 왜 이렇게 설계했나

- **결정적 스크립트**: 같은 입력 → 같은 출력. 반복·일괄 변환이 싸고 일관적이라 LLM이 매번 HTML을 손으로 짜지 않는다.
- **자체완결**: 외부 CSS/JS/CDN 의존 0. 파일 하나만 보내면 어디서든 동일하게 렌더된다(ADR 0004의 "산출물은 자체완결 단일 파일" 정신).
- **원본 불변**: `.md`가 정본(GitHub·cs-web 렌더링용, ADR 0004). HTML은 `cs-html/`에 생성되는 *파생 산출물*이다.

## 사용법

```bash
# 단일 변환 (기본 출력: 저장소루트/cs-html/ 아래 cs/ 상대경로 미러)
python .claude/skills/cs-doc-html/scripts/convert.py cs/low-level-design/introduction.md

# 출력 경로 지정
python .claude/skills/cs-doc-html/scripts/convert.py cs/db/index.md -o /tmp/index.html

# 카테고리 일괄 변환 (내부 .md 링크가 .html로 재작성되어 서로 연결됨)
for f in cs/low-level-design/*.md; do
  python .claude/skills/cs-doc-html/scripts/convert.py "$f"
done
```

변환 후 브라우저로 열어 확인한다(사람의 수동 확인 단계).

```bash
start "" "cs-html/low-level-design/introduction.html"   # Windows
# open / xdg-open — macOS / Linux
```

## 입력 문서가 따르는 컨벤션 (CS-GUIDE)

스크립트는 아래를 헤더 chrome으로 분리하고, 나머지를 본문으로 렌더한다. 컨벤션을 안 따라도 동작하지만(해당 칸이 비워짐), 따르면 풍부하게 렌더된다.

| 요소 | 마크다운 형태 | 렌더 결과 |
|------|--------------|----------|
| 제목 | 첫 `# 제목` | 그라디언트 헤더 H1 |
| 난이도·선수지식 | `> \`[N] 레벨\` · 선수 지식: [..](..)` | 색상 배지(N=1초록~4빨강) + 선수지식 링크 |
| 한 줄 정의 | 그다음 `> 정의` | 헤더 설명문 |
| 키워드 | `` `#태그` `#Tag` `` 라인 | 키워드 칩 |
| 출처 | `> 출처: [..](..)` | 출처 링크 |

## 동작 방식 (scripts/convert.py)

1. **메타 분리**: 첫 H1~첫 `##` 사이에서 난이도/선수지식/정의/키워드/출처를 추출하고 본문에서 제거(중복 방지).
2. **Mermaid 사전 렌더**: ` ```mermaid ` 블록을 `mmdc`(Mermaid CLI)로 SVG 변환해 `<figure class="diagram">`로 인라인. `mmdc`가 없거나 실패하면 소스를 `<pre>`로 폴백(깨지지 않음).
3. **본문 변환**: `python-markdown`(extra·tables·fenced_code·toc) → H2/H3로 TOC 자동 생성.
4. **이미지 인라인**: 로컬 `![](images/x.svg)`는 인라인 `<svg>`로, `.png/.jpg`는 base64 data URI로 임베드해 자체완결성을 지킨다(외부 URL은 보존).
5. **링크 재작성**: 본문·헤더의 상대 `.md` 링크를 `.html`로(외부 URL·앵커는 보존). 카테고리 일괄 변환 시 문서 간 링크가 맞물린다.
6. **시각 위계 강화** (글 밀도 완화):
   - **섹션 카드화**: 각 `##` 섹션을 아이콘 달린 `<section class="card">`로 분리해 스캔성을 높인다(H2 키워드별 이모지 자동 배정).
   - **쉽게 이해하기 강조**: "쉽게 이해하기" 섹션은 💡 초록 특별 카드(`.card.easy`)로 부각.
   - **ASCII 다이어그램화**: 박스 드로잉 문자(`─│┌┐▼` 등)가 든 코드 블록을 `<figure class="ascii">` 다이어그램 패널로 전환.
   - **권장/비권장 콜아웃**: `**권장 (O)**`/`**비권장 (X)**` 문단을 초록/빨강 콜아웃으로.
7. **조립**: `assets/template.html`의 `{{...}}` 자리를 채워 출력.

## 의존성

- **필수**: Python 3 + `markdown` 패키지(`pip install markdown`).
- **선택**: `mmdc`(`npm i -g @mermaid-js/mermaid-cli`) — 있으면 Mermaid를 SVG로 렌더, 없으면 소스 표시로 폴백.

## 주의

- 생성물(`cs-html/`)은 빌드 산출물이다. 버전 관리에 넣고 싶지 않으면 `.gitignore`에 `cs-html/`를 추가한다(호스팅·공유 목적이면 커밋해도 됨 — 사용자 선택).
- 디자인 토큰은 [`html-doc`](../html-doc/references/template.html)에서, **타이포 스케일**(본문 1.0625rem·h2 1.5rem·h3 1.25rem)은 같은 cs 문서를 렌더링하는 `cs-web` 뷰어(`cs-web/.../custom.css`)에서 차용해 위계를 일치시켰다. 디자인 변경 시 `assets/template.html`을 함께 갱신한다.

## 참조

- `scripts/convert.py` — 변환기(결정적, CLI)
- `assets/template.html` — 출력 HTML 스켈레톤(인라인 CSS, `{{PLACEHOLDER}}`)
