---
name: git-commit-push
description: Use ONLY when the user explicitly invokes /git-commit-push or directly asks to commit and push. NEVER run this automatically after completing code changes.
---

# Git Commit & Push

## 발동 조건 (MANDATORY)

이 스킬은 **반드시 사용자가 명시적으로 호출한 경우에만** 실행할 것.

허용되는 발동:
- 사용자가 `/git-commit-push`를 직접 입력한 경우
- 사용자가 "커밋해줘", "푸시해줘", "커밋하자" 등 명시적으로 요청한 경우

**금지되는 발동:**
- 코드 작업 완료 후 자동으로 실행하지 말 것
- Claude의 판단으로 "작업이 끝났으니 커밋도 해야겠다"며 실행하지 말 것
- Bash 도구로 `git commit`, `git push`를 직접 실행하지 말 것

## Workflow

아래 동작을 한 번 수행하고, 별도 instruction이 없으면 반복하지 말 것.
Claude Code가 변경한 내역이 아니더라도 사용자가 수정하거나 추가한 모든 변경 사항을 포함하여 진행할 것.

```bash
# 1. 전체 스테이징
git add .

# 2. 커밋 대상 확인
git status
```

커밋 파일 목록과 메시지 초안을 보여주고 **사용자 승인을 대기할 것**.

```bash
# 3. 승인 후 커밋
git commit -m "<emoji> <message>" -m "<description>"

# 4. 푸시
git push
```

> **GPG 서명**: 서명 팝업이 뜰 수 있음. 사용자 action을 기다릴 것. `--no-gpg-sign`으로 우회 금지.

### upstream 미설정 시

```bash
git push --set-upstream origin <branch_name>
```

### 푸시 후 PR 링크

`git push` 출력에 아래와 같은 PR 생성 URL이 포함된 경우 사용자에게 공유:

```
remote: Create a pull request for '...' on GitHub by visiting:
remote:      https://github.com/.../pull/new/<branch>
```

출력에서 URL을 추출하여 응답에 포함. 없으면 생략.

## Commit Message 형식

```
<emoji> <message>

<description>
```

- `<emoji>`: 유니코드 emoji (`✨`), shortcode(`:sparkles:`) 금지
- `<message>`: 영어 imperative, **50자 이내**, 한 줄 요약
- `<description>`: 변경 내용 한국어 요약, **불릿 포인트 3줄 이내**. 장황한 설명 금지. 없으면 생략 가능.

### Bad Example

```
🔧 Update zshrc configuration and gitconfig settings to deprecate old aliases and add main as default branch

- zshrc에서 더 이상 사용하지 않는 Python 관련 로컬 설정들을 정리하고,
  pyenv 초기화 로직이 중복 실행되던 문제를 수정함. 또한 direnv 관련
  설정도 함께 추가하여 프로젝트별 환경 변수 자동 로드가 가능하도록 함.
- gitconfig에서 기존 master를 default branch로 사용하던 설정을 main으로
  변경하고, 관련 alias들도 함께 업데이트함.
```

### Good Example

```
🎨 Deprecate old configs, set main as default branch

- zshrc: Python 로컬 설정 제거, direnv 추가
- gitconfig: default branch master → main 변경
```

## Emoji Quick Reference

| 상황 | Emoji |
|------|-------|
| 새 기능 | ✨ |
| 버그 수정 | 🐛 |
| 긴급 핫픽스 | 🚑️ |
| 리팩토링 | ♻️ |
| 테스트 | ✅ |
| 문서 | 📝 |
| 설정 파일 | 🔧 |
| 빌드/스크립트 | 🔨 |
| 성능 개선 | ⚡️ |
| 보안 수정 | 🔒️ |
| 코드·파일 삭제 | 🔥 |
| 아키텍처 변경 | 🏗️ |
| 의존성 추가/제거 | ➕ / ➖ |
| 의존성 업그레이드 | ⬆️ |
| 타입 추가/변경 | 🏷️ |
| 브랜치 병합 | 🔀 |
| 배포 | 🚀 |
| 프로젝트 시작 | 🎉 |
| WIP | 🚧 |
| 린터/컴파일 경고 수정 | 🚨 |
| 코드 구조/포맷 개선 | 🎨 |
| 로그 추가/제거 | 🔊 / 🔇 |
| 데드코드 제거 | ⚰️ |
| 비즈니스 로직 | 👔 |

적절한 것이 없다면 `gitmoji --list` 실행하여 참조할 것. 그래도 없으면 `✨`로 통일할 것.
