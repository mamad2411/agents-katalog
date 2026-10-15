---
name: peach-markitdown
description: |
  PDF/PPTX/DOCX/XLSX/HTML/CSV/JSON/XML/ZIP/EPUB/이미지 같은 문서파일을 md로 변환할 때 사용한다. "문서 md 변환", "pdf를 markdown", "pptx를 markdown", "docx를 markdown", "문서 추출", "백업솔루션 md 변환" 요청에서 사용한다. markitdown 설치 확인, HWPX 추출 환경 설치, 단일 파일 또는 폴더 변환, 오류 로그 생성을 함께 처리한다.
---

# 문서파일 md 변환 스킬

`MarkItDown`과 `python-hwpx`를 조합해 문서파일을 `md`로 변환한다.

- `MarkItDown` 공식 범위 중 이 스킬이 채택한 입력: `PDF`, `PowerPoint`, `Word`, `Excel`, `HTML`, `CSV`, `JSON`, `XML`, `ZIP`, `EPUB`, 이미지
- 이 스킬의 별도 처리: `HWPX`
- 처리 방식: 단일 파일 변환 + 폴더 일괄 변환

- `PDF`, `PPTX`, `DOCX`, `XLSX`, `HTML`, `CSV`, `JSON`, `XML`, `ZIP`, `EPUB`, 이미지: `markitdown`
- `HWPX`: `python-hwpx` 기반 내장 추출기
- 출력: 별도 폴더
- 실패: 로그 파일

## 범위

이 스킬은 아래만 처리한다.

- `markitdown` 설치/확인
- `.venv` 생성 및 `python-hwpx`, `lxml` 설치/확인
- 단일 파일 -> `md` 변환
- 문서파일 묶음 폴더 일괄 변환
- 결과 요약과 실패 로그 작성

이 스킬은 아래를 처리하지 않는다.

- YouTube transcript 추출
- 음성 파일 전사
- 화자 분리
- 문서 편집
- 문서 -> PDF 변환
- OCR 품질 개선
- HWP/HWPX 고충실도 레이아웃 복원

## 실행 순서

### 1. 환경 준비

현재 작업 프로젝트 루트에서 실행한다.

```bash
bash <skill-dir>/scripts/bootstrap.sh
```

### 2. 단일 파일 변환

```bash
python3 <skill-dir>/scripts/convert_one.py \
  --source "/절대경로/입력파일" \
  --output "/절대경로/출력파일.md"
```

예시:

```bash
python3 <skill-dir>/scripts/convert_one.py \
  --source "$PWD/sample.docx" \
  --output "$PWD/output/sample.md"
```

### 3. 폴더 일괄 변환

```bash
python3 <skill-dir>/scripts/convert_folder.py \
  --input-dir "/절대경로/입력폴더" \
  --output-dir "/절대경로/출력폴더"
```

예시:

```bash
python3 <skill-dir>/scripts/convert_folder.py \
  --input-dir "$PWD/백업솔루션/원본" \
  --output-dir "$PWD/백업솔루션/md"
```

## 처리 규칙

| 확장자 | 처리 방식 |
|--------|-----------|
| `.pdf`, `.pptx`, `.docx`, `.xlsx`, `.xls` | `markitdown` |
| `.html`, `.csv`, `.json`, `.xml`, `.zip`, `.epub` | `markitdown` |
| 이미지 계열 확장자 | `markitdown` |
| `.hwpx` | `extract_hwpx.py --format markdown` |
| 기타 | 스킵 + 로그 |

참고:
- 일부 포맷은 upstream 상태에 따라 성공 여부가 달라질 수 있다.
- YouTube transcript는 `baoyu-youtube-transcript` 스킬을 사용한다.
- 음성 전사와 화자 분리는 `NotebookLM` 또는 별도 음성 전사 경로를 사용한다.

## 공식 지원 vs 현재 검증

구분해서 봐야 한다.

- `MarkItDown` 공식 지원 범위는 더 넓지만, 이 스킬은 문서파일과 이미지에만 한정한다
- 이 스킬의 현재 자동화 범위: 위 포맷을 `markitdown`에 위임하고, `HWPX`는 별도 추출기로 처리
- 이 환경에서 실제 검증 완료:
  - `PDF`, `PPTX`, `HWPX` 폴더 일괄 변환 성공
- 이 환경에서 주의가 필요한 항목:
  - 새 포맷은 실무 적용 전 단건 검증이 필요하다

실무 원칙:
- “공식 지원”과 “현재 검증 완료”를 같은 의미로 말하지 않는다.
- 새 포맷을 실무에 쓰기 전에는 `convert_one.py`로 먼저 단건 검증한다.
- YouTube transcript는 `baoyu-youtube-transcript`를 기본값으로 쓴다.
- 음성 전사와 화자 분리는 `NotebookLM` 또는 별도 STT 경로로 분리한다.

## 결과물

출력 폴더에 아래 파일을 남긴다.

- 변환된 `.md`
- `conversion-summary.json`
- `conversion-errors.log`

## 운영 원칙

- 원본 파일은 절대 수정하지 않는다.
- 출력은 항상 별도 폴더에 쓴다.
- 같은 이름의 결과가 있으면 기본적으로 덮어쓴다.
- 지원하지 않는 파일은 실패로 중단하지 않고 로그만 남긴다.
