@AGENTS.md

## Gemini CLI Quick Start

1. `AGENTS.md` 로드 완료 (위 @ 포함).
2. `_wood/context/current.yaml` 읽어 현재 버전·P1 컨텍스트 파악.
3. `_wood/workflows/_PROTOCOL.md` 읽어 실행 규칙 확인.
4. 진입: "swyp-entry 워크플로우 실행해줘" 또는 `.claude/commands/swyp-entry.md` 내용 참조.

## Gemini 주의사항

- `gh` CLI 명령은 verbatim 실행. 출력 조작·요약·번역 금지.
- 역할 확인 전 이슈 생성·커밋·PR 생성 금지.
- 보호 파일(`_wood/**`, `AGENTS.md`, `.claude/**`) 편집 제안 금지.
- 불확실하면 실행 말고 사용자에게 질문.
