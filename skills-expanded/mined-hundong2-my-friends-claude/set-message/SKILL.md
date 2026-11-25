# set-message

Change a specific message in the my-friends-claude plugin configuration.

## Usage
`/my-friends-claude:set-message <message_key> <new_message>`

## Instructions

When this skill is invoked:

1. Parse the arguments to extract `message_key` and `new_message`
2. Valid message keys:
   - `session_start` — 세션 시작 인사말
   - `session_end` — 세션 종료 인사말
   - `working` — 작업중 메시지
   - `thinking` — 생각중 메시지
   - `error_occurred` — 에러 발생 메시지
   - `task_complete` — 작업 완료 메시지
   - `git_push_warning` — Git Push 경고 메시지
   - `test_passed` — 테스트 통과 메시지
   - `test_failed` — 테스트 실패 메시지

3. If no arguments provided, show available keys and ask which one to change
4. If only key provided, ask for the new message
5. Update `config/config.json` using the Edit tool — change the value of `messages.<key>` to the new message
6. Confirm: "메시지가 변경되었습니다! {key}: {new_message}"

## Example
```
/my-friends-claude:set-message session_start "야호! 오늘도 코딩 시작이다!"
```
