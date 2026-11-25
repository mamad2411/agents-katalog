---
name: skill-commit
description: (heropy) Use when committing changes in this project. Analyzes changes to generate appropriate commit messages and bumps skill versions in frontmatter when SKILL.md files are modified.
license: MIT
metadata:
  author: ParkYoungWoong
  version: 1.1.1
---

# Commit with Version

이 프로젝트에서 커밋할 때 변경사항을 분석하여 적절한 커밋 메시지를 작성하고, 수정된 스킬의 버전을 자동으로 업데이트하는 스킬.

## 동작 흐름

### 1단계: 변경사항 분석

`git status`와 `git diff`를 실행하여 변경된 파일과 내용을 확인한다.

### 2단계: 스킬 버전 업데이트

변경된 파일 중 `skills/*/SKILL.md`가 포함되어 있으면, 해당 SKILL.md의 프론트매터에서 `version` 값을 패치(patch) 버전으로 올린다.

버전 규칙 (Semantic Versioning):
- **patch** (x.y.Z): 오타 수정, 문구 변경, 설정값 변경 등 기존 동작에 영향 없는 수정
- **minor** (x.Y.0): 새로운 단계/기능 추가, 기존 동작을 유지하면서 확장
- **major** (X.0.0): 스킬의 전체 구조 변경, 기존 동작과 호환되지 않는 변경

기본적으로 patch 버전을 올리되, 변경 규모에 따라 minor 또는 major로 판단한다.

### 3단계: README.md 갱신

변경된 파일 중 `skills/*/SKILL.md`가 포함되어 있으면, 프로젝트 루트의 `README.md`도 함께 갱신한다.

갱신 규칙:
- **스킬 추가**: `## 스킬 목록` 섹션에 새 스킬의 항목을 추가한다 (제목, 설명, 설치 명령어, 주요 기능 목록)
- **스킬 수정**: 해당 스킬의 설명이나 기능 목록이 변경되었으면 README.md의 내용도 일치하도록 수정한다
- **스킬 삭제**: README.md에서 해당 스킬 항목을 제거한다
- 기존 README.md의 포맷과 스타일을 유지한다

### 4단계: 커밋 메시지 작성

최근 커밋 로그(`git log`)의 스타일을 참고하여 커밋 메시지를 작성한다.

커밋 메시지 규칙:
- 한국어로 작성
- 첫 줄은 변경 내용을 간결하게 요약 (50자 이내 권장)
- 필요시 빈 줄 후 상세 설명 추가
- 여러 스킬이 동시에 수정된 경우, 주요 변경 내용을 기준으로 메시지를 작성

### 5단계: 커밋 실행

변경된 파일을 스테이징하고 커밋한다. README.md가 갱신된 경우 함께 포함한다. 사용자가 푸시를 요청한 경우 푸시도 함께 실행한다.

## 주의사항

- 버전 업데이트 자체로 인한 변경은 별도 커밋으로 분리하지 않고, 원래 변경사항과 함께 커밋한다
- `SKILL.md` 외의 파일만 변경된 경우(예: `README.md`, `package.json`)에는 버전 업데이트를 하지 않는다
- 이미 현재 커밋에서 버전이 수동으로 변경된 경우, 추가로 버전을 올리지 않는다
