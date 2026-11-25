---
name: hwpx
description: 파이썬으로 한글 문서(.hwpx)를 코드로 생성·읽기·편집·변환한다. 생성은 표·셀병합·배경색·글자모양·이미지·머리말/꼬리말·쪽번호·가로/세로 페이지 지원. 읽기는 기존 .hwp/.hwpx에서 본문·표 추출(한컴 없이)과 교정추적(변경 내용) 삽입/삭제 분리·변경 전후본 추출. 편집은 양식 hwpx의 플레이스홀더 치환·표 행 추가. 변환은 hwp→hwpx, →pdf/docx/md. 사용자가 "hwpx로 출력/저장/변환/만들어", "한글 파일/문서로 만들어", "hwp 내용 읽어/추출", "변경 내용/교정추적/뭐가 고쳐졌는지 봐줘", "hwp를 hwpx로 변환", "양식에 내용 채워줘", "시간표/회의록/표를 hwpx로" 등을 요청할 때 트리거. (Windows + 한컴오피스 설치 필요; 읽기/편집/일부 변환은 한컴 없이 동작)
---

# HWPX 생성·읽기·편집·변환 스킬

파이썬으로 `.hwpx`(한글) 문서를 **생성·읽기·편집·변환**한다. 생성은 docx→hwpx **변환에 의존하지 않고**
(한컴 설치본에 따라 자동화 Open이 외부형식에서 실패함) **템플릿 header.xml 재사용 + section0.xml 직접 생성
→ `zipfile` 재패키징 → 한글 baking**으로 완성한다. 읽기/편집은 순수 파이썬(한컴 불필요), 변환 일부는 한컴 COM을 쓴다.

전체 배경·함정·원리는 동봉 `GUIDE.md` 참조.

## 번들 파일
- `hwpxgen.py` — **생성** 엔진(단락/표/병합/색/이미지/머리말·꼬리말/쪽번호/페이지). **import해서 쓴다.**
- `hwpx_read.py` — **읽기** 엔진. .hwp(OLE 레코드)·.hwpx(zip+lxml)에서 본문·표 추출(한컴 불필요). **교정추적 분리**(`read_changes`)도 지원.
- `hwpx_edit.py` — **편집** 엔진. 기존 hwpx의 플레이스홀더 치환(find/replace)·셀 직접 채우기(`set_cell`, 빈 칸 포함)·체크박스 토글(`check_option`)·표 행 추가.
- `hwpx_convert.py` — **변환** 엔진. hwp→hwpx·→pdf(한컴 COM), →docx(python-docx)·→md/txt(순수 파이썬).
- `hwpx_bake.py` — 생성/편집한 hwpx를 한글로 열고 다시 저장(레이아웃 재계산) + 검증 PDF.
- `make_seed.py` — 기준 시드(_seed.hwpx)를 새로 만들 때(다른 PC/한글 버전).
- `_seed.hwpx` — 기준 템플릿(스타일·색 borderFill·글자 charPr 정의 보유).
- `GUIDE.md` — 상세 가이드(v7).

## 읽기 / 편집 / 변환 빠른 사용
```python
import hwpx_read, hwpx_edit, hwpx_convert
# 읽기 — .hwp/.hwpx 본문·표 추출(한컴 불필요)
text = hwpx_read.extract_text("RFP.hwp")            # 평문
doc  = hwpx_read.read_hwpx("양식.hwpx")             # {'blocks':[para|table], 'text'}
tables = hwpx_read.iter_tables(doc)                 # [[ [행][열] ]]
ok, errs = hwpx_read.validate("작성본.hwpx")        # 한컴 없이 손상 사전검사(raw 생성물)
ok, errs = hwpx_read.validate("baked.hwpx", pre_bake=False)  # baking된/외부 파일은 구조검사만
# 교정추적(변경 내용) — "뭐가 고쳐졌는지" 보기. .hwp는 먼저 hwpx로 변환.
clean = hwpx_read.extract_text("수정본.hwpx")        # 기본 revisions='final' → 깨끗한 최종본
ch = hwpx_read.read_changes("수정본.hwpx")           # {changes:[삽입/삭제], original, final, orphans, authors}
# orphans>0(변환이 종료마커 누락)면 권위 최종본을 오라클로 주입해 정확도↑(삽입까지 복원):
ft = hwpx_convert.accepted_text("수정본.hwp")        # 한컴 GetTextFile = 변경 적용(최종)본
ch = hwpx_read.read_changes("수정본.hwpx", final_text=ft)
# 편집 — 양식 플레이스홀더 채우기 + 셀 교체 + 표 행 추가
ed = hwpx_edit.HwpxEditor("양식.hwpx")
ed.replace_map({"{{과제명}}":"AI 인재양성", "{{금액}}":"5,000,000"})
ed.set_cell(0, row=1, col=1, text="5,000,000")     # 표0의 (col=1,row=1) 셀만 교체 (빈 칸도 채워짐)
ed.check_option(0, row=2, col=6, checked=True)     # 양식 체크박스 토글(/ 글리프)
ed.append_table_row(0, ["운영비","750,000"])
# ── 표 꾸미기(v8 추가): 답답한 양식 셀 여백·글자객체 해제·표 늘이기 ──
ed.set_cell_margin(1, (540,370))                   # 표1 모든 셀 여백 좌우540·상하370 HWPUNIT(1mm≈283). only=[(r,c)…]로 일부만
ed.set_table_float(8, treat_as_char=False)         # 표8을 '글자객체로 인식 안 함' + pageBreak='CELL'(긴 표 쪽경계서 안 잘림)
ed.stretch_table(1, total_height_mm=120)           # 표1을 세로 120mm로 끌어당겨 늘임(또는 row_height=HWPUNIT)
ed.set_cell_valign(1, 'CENTER')                    # 셀 세로 정렬 TOP/CENTER/BOTTOM (only=[(r,c)…]로 일부만)
ed.save("작성본.hwpx")                              # 이후 python hwpx_bake.py 권장
# 변환
hwpx_convert.hwp_to_hwpx("RFP.hwp")                 # .hwp → .hwpx (한컴, 표 보존)
hwpx_convert.to_pdf("작성본.hwpx")                  # → .pdf  (한컴)
hwpx_convert.to_docx("양식.hwpx")                   # → .docx (python-docx, 표 보존)
hwpx_convert.to_markdown("RFP.hwp")                 # → .md   (순수 파이썬)
```
> 받은 **.hwp RFP/양식**은 `hwp_to_hwpx`로 올린 뒤 read/edit하면 표 구조까지 다룰 수 있다.

## 작업 절차

1. **준비물 확인**: Windows + 한컴오피스, 파이썬 `openpyxl`/`pywin32`/`pyhwpx`(보안 DLL용)/`PyMuPDF`(검증).
   `_seed.hwpx`가 없으면 `python make_seed.py`로 생성(한글 자동화).

2. **작업 폴더에 복사**: `hwpxgen.py`, `hwpx_bake.py`, `_seed.hwpx`를 대상 폴더로 복사한 뒤 사용.

3. **문서 생성 스크립트 작성** — `hwpxgen`의 `HwpxDoc`로 본문을 만든다.
   ```python
   from hwpxgen import *
   d = HwpxDoc("_seed.hwpx").page(landscape=False, margin_lr_mm=16)  # 가로면 landscape=True
   navy=d.fill("1F3864"); green=d.fill("CFE9DA")     # 셀 배경색
   red =d.char(CH_SMALL,"C0392C")                    # 글자색 변형
   cw=[int(d.content_w*0.2), d.content_w-int(d.content_w*0.2)]
   rows=[[ d.cell([("항목",CH_WHITE)],0,0,cw[0],bf=navy),
           d.cell([("값", CH_CELL )],1,0,cw[1]) ]]
   body = d._para([("문단",CH_NORMAL)]) + d.table(rows,cw)
   d.save("out.hwpx","제목", body=body)
   ```
   - 스타일 상수: `CH_TITLE/CH_H1/CH_H2/CH_NORMAL/CH_SMALL/CH_WHITE/CH_CELL`, `PA_CENTER/PA_LEFT`, `BF_DATA`.
   - 임의 크기 글자: `d.char_sz(base_id, height_pt, "RRGGBB", bold=True)`.
   - 셀 병합: `d.cell(..., colspan=N, rowspan=M)` + **가려지는 칸은 생략**, `col/row`는 실제 격자 인덱스.
   - **셀 여백(v8)**: 기본값이 넉넉(`CELL_MARGIN=(510,510,312,312)`)해져 답답함 해소. `d.cell(..., margin=(lr,tb))` 또는 `int`/`(l,r,t,b)`로 셀별 지정, `d.table(..., cell_margin=...)`로 표 기본. `d.cell(..., vertAlign='TOP'/'CENTER'/'BOTTOM')`.
   - **글자객체 해제·쪽나눔(v8)**: `d.table(rows, cw, treat_as_char=False)` → 표를 글자처럼 취급 안 함. `pageBreak='CELL'`(기본)이면 한 페이지 넘는 표가 잘리지 않고 셀 단위로 나뉨('TABLE'=통째 이동, 'NONE'=안 나눔).
   - **표 늘이기/stretch(v8)**: `d.table(rows, cw, total_height_mm=120)`(행수로 등분) 또는 `row_height=HWPUNIT`로 표를 세로로 끌어당겨 늘임.
   - 이미지(인라인, 글자처럼): `body += d.image("싸인.png", width_mm=40)` — BinData 임베드+매니페스트 자동.
     크기 미지정 시 픽셀(96dpi) 기준, 한쪽만 주면 비율 유지.
   - 머리말/꼬리말/쪽번호: `d.set_header("제목")`, `d.set_footer("꼬리말", page_number=True)`,
     `d.page_number("BOTTOM_CENTER")`. (save 전에 호출; secPr 문단에 컨트롤로 주입됨)

4. **baking + 검증**:
   ```bash
   python hwpx_read.py --validate out.hwpx   # (선택) baking 전 손상 사전검사(한컴 불필요)
   python hwpx_bake.py out.hwpx              # 한글로 열고 재저장(필수) + _verify_out.pdf 생성
   ```
   그 후 PyMuPDF로 PDF를 이미지 렌더해 눈으로 확인하고, **span size가 0.12pt면 charPr 버그**.
   `validate()`는 표 id 중복·셀주소·열너비합 등 구조 손상을 baking 전에 잡는다(외부/baking된 파일은 `--baked`).

## 반드시 지킬 함정 (자세한 건 GUIDE.md)
- **baking 필수**: 빈 `linesegarray`는 한글이 "열 때" 계산 → 안 하면 **글자가 안 보임**.
- **charPr**: ratio/relSz=100, fontRef 유효값, 색은 `#RRGGBB`(# 필수). 엔진이 시드 로드 시 자동 교정.
- **페이지 방향**: width/height는 항상 세로기준, 방향은 `landscape` 속성(WIDELY=세로, NARROWLY=가로).
- **가로 인쇄폭**: 한글 실제 가로폭 ≈67176 HWPUNIT(≈237mm). 표가 넓으면 오른쪽 열이 잘림 → 너비 실측·축소.
- **재패키징**: 파이썬 `zipfile`만(쉘 zip 금지), 원본 `infolist()` 순서 유지.
- **header.xml은 추가만**(itemCnt 갱신), 기존 항목 수정 금지.
- **교정추적 평문 추출 주의**: `revisions='merge'`(옛 동작)·.hwp 바이너리 리더는 삽입+삭제를 한 흐름으로 이어붙여 번호가 겹쳐 보인다(예: 재번호 중 `[7]`→`[34]`가 `"[347]"`로). 깨끗한 본문은 `revisions='final'`(기본). "뭐가 바뀌었나"는 `read_changes`.
- **COM 변환이 종료마커를 누락**시킬 수 있음(`insertBegin` n개 / `insertEnd` n-1개). `read_changes`의 `orphans>0`가 신호. 이땐 `hwpx_convert.accepted_text`(한컴 GetTextFile=최종본)를 `final_text=`로 주입해 보정. 한컴 GetTextFile은 보기모드와 무관하게 늘 최종본을 주고, 자동화의 변경수락/거부 액션은 no-op이라 '원본(거부)본'은 `read_changes(...)['original']`로만 얻는다.

## 엑셀 데이터 → 표 예시
구조화 데이터(예: 시간표 xlsx)는 `openpyxl`로 읽어 격자/트랙을 계산한 뒤,
시작 셀에 `rowspan/colspan`을 주고 가려진 칸을 생략해 병합 표를 만든다.
(원본 프로젝트 `build_timetable_hwpx.py`/`build_minutes_hwpx.py` 패턴 참고.)
