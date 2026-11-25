# status

Show the my-friends-claude plugin status dashboard.

## Usage
`/my-friends-claude:status`

## Instructions

When this skill is invoked:

1. Read `config/config.json`
2. Check which style files exist in `styles/` directory
3. Display a status dashboard:

```
🔌 my-friends-claude 플러그인 상태
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 플러그인 로드됨
📝 활성 스타일: {activeStyle}
🌐 언어: {language}
👤 페르소나: {persona.name}

📁 사용 가능한 스타일:
  {list each .md file in styles/ directory}

🪝 등록된 Hooks:
  • SessionStart — 세션 시작 인사
  • UserPromptSubmit — 페르소나 주입
  • Stop — 세션 종료 인사
  • PreToolUse — 도구 사용 피드백
  • Notification — 알림 커스터마이즈

✽ 스피너 동사:
  활성화: {spinnerVerbs.enabled}
  동사 수: {spinnerVerbs.verbs 배열 길이}개
  적용 상태: ~/.claude/settings.json에 spinnerVerbs 키 존재 여부 확인

🎯 사용 가능한 명령:
  /my-friends-claude:set-style      — 스타일 변경
  /my-friends-claude:show-config    — 설정 조회
  /my-friends-claude:set-message    — 메시지 변경
  /my-friends-claude:apply-spinner  — 스피너 동사 적용/원복
  /my-friends-claude:status         — 이 대시보드
```

Use Glob to find style files and Read to get config values.
