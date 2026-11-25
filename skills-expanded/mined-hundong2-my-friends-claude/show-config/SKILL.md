# show-config

Display the current my-friends-claude plugin configuration.

## Usage
`/my-friends-claude:show-config`

## Instructions

When this skill is invoked:

1. Read `config/config.json` from the plugin directory
2. Display the configuration in a readable format:

```
📋 my-friends-claude 설정
━━━━━━━━━━━━━━━━━━━━━━━━
언어: {language}
활성 스타일: {activeStyle}
페르소나: {persona.name}
이모지: {persona.emoji}

💬 메시지 설정:
  시작 인사: {messages.session_start}
  종료 인사: {messages.session_end}
  작업중: {messages.working}
  생각중: {messages.thinking}
  에러: {messages.error_occurred}
  완료: {messages.task_complete}
  Git Push 경고: {messages.git_push_warning}
  테스트 통과: {messages.test_passed}
  테스트 실패: {messages.test_failed}

📊 상태바:
  모델 표시: {statusLine.show_model}
  브랜치 표시: {statusLine.show_git_branch}
  비용 표시: {statusLine.show_cost}
  컨텍스트 표시: {statusLine.show_context_remaining}
  접두사: {statusLine.custom_prefix}
```

Replace `{...}` with actual values from config.json.
