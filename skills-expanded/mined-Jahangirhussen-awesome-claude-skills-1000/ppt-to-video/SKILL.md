---
name: ppt-to-video
description: Use when the user wants to turn a PowerPoint/PPTX file into a narrated video with animated slide elements, or wants to re-cut/re-voice an existing presentation-style video — especially for franchise/business briefings, sales decks, or explainer videos combining slides with interview or B-roll clips.
---

# PPT to Video

새 PPTX를 받아 나레이션+PPT 요소 애니메이션이 있는 영상으로 만들거나, 기존 영상을
씬 단위로 리컷/리보이스한다. 둘은 같은 매니페스트 파이프라인의 씬 타입 배합일 뿐이다.

**핵심 원칙 — 절대 어기지 말 것: 슬라이드를 HTML로 다시 그리지 않는다.** PPTX를
PowerPoint 자체 렌더러로(COM) PNG/영상으로 뽑아 쓴다. 브랜드 자산(사진·폰트·레이아웃)을
그대로 보존하기 위함 — HTML 재현은 이 접근을 시도했던 이전 프로젝트에서 브랜드 룩이
어긋나 실패한 원인이었다.

## 최초 실행 시 — 환경 점검

**세션에서 처음 이 스킬을 쓸 때 먼저 실행:**

```bash
python scripts/check_env.py
```

`[MISSING]` 항목이 있으면 사용자에게 설치해도 되는지 먼저 물은 뒤, 출력에 나온 설치
명령을 실행한다. PowerPoint 없이도(맥/리눅스 등) `--static-slides`로 정지+푸시인
방식은 가능하지만 요소 애니메이션은 Windows+PowerPoint 전용이다.

## 워크플로우

전체 단계·매니페스트 스키마·트러블슈팅은 [references/pipeline.md](references/pipeline.md)
참고. 요약:

1. **인제스트**: `python -m revoice.deck <파일.pptx> [출력폴더]` → 슬라이드 PNG +
   `outline.json`(제목·본문·발표자 노트).
2. **나레이션 기획**: outline을 참고 자료로만 쓰고, 브랜드 나레이터 톤으로 새로 쓴다.
   발표자 노트를 그대로 베끼지 않는다(요청받은 경우가 아니면). 직접 호칭·수사적 질문·
   서스펜스를 섞어 "화면 낭독"이 아니라 "진행자가 설명하는" 톤으로.
3. **매니페스트 구성**: `SLIDE`(PPT+신규 나레이션) / `VO`(기존영상+신규 나레이션) /
   `ORIGINAL`(원음 유지) / `CLIP`(별도 영상 구간, 원음 유지) / `EXTERNAL`(범퍼) 씬을
   배합해 `manifest.json`을 만든다. 인터뷰·증언 클립은 사용 전 원 소유자 확인 게이트를
   거친다(브랜드 주장이 아니라 현장 사례로만 인용).
4. **확인**: `python -m revoice.build render --manifest <파일> --dry-run` — 무엇이
   재빌드될지, TTS가 몇 번 호출될지 API 호출 없이 미리 본다.
5. **렌더**: `python -m revoice.build render --manifest <파일>` — 변경분만 재빌드.
   `--only <씬ID>`로 특정 씬만, `--all`로 전체 강제 재빌드.

## 하지 말 것

- 슬라이드를 HTML/React로 재현 — 브랜드 룩이 어긋난다.
- 확정 안 된 수치·문구를 `⚠확인`/`[확인]` 표식 없이 그대로 나레이션에 넣기 — 렌더
  게이트가 이런 표식을 감지하면 자동 차단하니, 표식을 지우려면 실제로 사용자 확인을
  받은 뒤에만.
- 씬 하나 고칠 때 `--all`로 전체 재빌드 — TTS·PPT 애니메이션을 불필요하게 다시 만들어
  API 비용과 시간을 낭비한다. `--only`로 좁혀서.

## 알려진 제약

- **PPT 요소 애니메이션은 Windows+PowerPoint 전용.** 서버/크로스플랫폼 배포는
  `references/pipeline.md`의 "다른 환경으로 확장" 절 참고.
- **유튜브 640p 초과 화질은 PO 토큰(안티봇 인증)이 필요해 다운로드가 막힐 수 있다** —
  프로젝트 폴더에 원본 화질 로컬 파일이 있는지 먼저 찾아보고, 없으면 640p로 진행하거나
  사용자에게 브라우저 쿠키 인증을 시도할지 확인한다.
- **PowerPoint `CreateVideo`가 간헐적으로 실패한다**(콘텐츠 문제 아님, COM 자체의
  산발적 오류) — 이미 재시도 로직이 내장돼 있으니 신경 쓰지 않아도 되지만, 배치 렌더
  로그를 grep으로 좁게 필터링하면 `[deck] ... 실패` 메시지를 놓칠 수 있다. 배치 렌더
  로그는 필터링 없이 전체를 확인할 것.

## Purpose
Convert a PPTX into a narrated video with animated slide elements, or re-cut/re-voice an existing presentation video.

## When to use
The user wants a narrated video from a PowerPoint or to redo narration of a presentation video.

## When NOT to use
- Creating the slides themselves -> pptx/slides.
- Live-action video editing.

## Inputs
PPTX file, narration script or voice preference, output settings.

## Edge cases and failure handling
- Environment check fails -> fix tools before the workflow.
- Animations unsupported -> fall back to static slides and tell the user.

## Validation
- Video renders, narration aligns with slides, durations match script, audio levels are consistent.

## Output requirements
MP4 video and a short report of constraints hit.

## Example
```text
12-slide franchise deck -> script per slide -> TTS narration -> animated render -> MP4.
```

## Related skills
pptx, hyperframes, remotion-motion-graphics
