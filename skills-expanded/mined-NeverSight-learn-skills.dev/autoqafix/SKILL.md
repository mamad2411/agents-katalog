---
name: autoqafix
description: 트리거 `/autoqafix` — autoqafix 엔진 폴더에 동거하는 자기 자신의 doctor를 1회 실행한다. smarthome 등 개별 repo의 autofix.bat(린트 스크립트)와 무관하다.
---

# /autoqafix — Claude Code 트리거

이 스킬은 autoqafix 엔진 폴더 안에 동거하는 트리거다 — 자기 폴더 자체가 엔진이다. 사용자가 `/autoqafix`를 입력하면 아래 절차만 따른다.

## 절차

1. **엔진 위치 해석**:
   - 이 SKILL.md가 있는 폴더 = 엔진 폴더다. 즉 자기 스킬 폴더 자체가 `<엔진 폴더>`다. 설치본이면 symlink의 원본을, 클론이면 그 폴더를 그대로 사용한다.
   - 자기 폴더 안에 `autoqafix-doctor.py`가 있는지 확인한다. 없으면 사용자에게 "autoqafix 엔진 위치를 알려달라"고 질문하고 진행을 중단한다.

2. **cwd 검증**: 현재 작업 디렉토리(cwd)가 대상 앱 repo의 루트인지 확인한다. 판정 기준은 `.git/`이 cwd 바로 아래에 있는지다. 아니면 중단하고 `autoqafix 스킬은 대상 앱 repo 루트에서 실행해야 합니다 — cwd: <현재 경로>`라고 안내한다.

3. **엔진 실행**: `<자기 스킬 폴더>/autoqafix-doctor.py --repo <cwd>`를 다음 형태로 실행한다:

   ```
   uv -q run "<자기 스킬 폴더>/autoqafix-doctor.py" --repo "$(pwd)"
   ```

4. **출력 요약 보고**: 결과를 사용자에게 요약한다. 특히 다음 토큰을 명시한다:
   - `[원인] ...` — 결함 원인
   - `[조치] ...` — 권장 조치
   - `FAIL <항목>` 줄이 있으면 그 항목을 모두 나열
   - `WARN <항목>` 줄은 별도로 표시 (FAIL은 아님)
   - `OK <항목>` 요약

## 금지

이 스킬은 issue 본문을 작성하거나 코드를 직접 고치는 일을 하지 않는다. doctor는 진단만 할 뿐 어떤 파일도 만들거나 고치지 않는다.

## 충돌 방지

이 `/autoqafix` 트리거는 smarthome 등 개별 repo에 들어 있는 `autofix.bat`(린트 스크립트)와 무관하다. 그쪽이 LLM 스크립트인지 단순 lint인지와 관계없이 본 스킬은 autoqafix 엔진만 호출한다.