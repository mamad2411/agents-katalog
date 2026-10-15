---
name: write-todo
description: PRD 문서를 사용자가 볼 수 있는(user-visible) 작업 순서로 나눠 `TODO.md`를 작성하거나 업데이트한다. 사용자가 "TODO 만들어줘", "작업 쪼개줘", "다음에 뭘 만들지 정리해줘"라고 할 때 사용한다.
---

# TODO 작성 (Write TODO)

목표: `PRD.md`를 구현 순서가 보이는 `TODO.md`로 바꾼다.

GitHub 이슈(issue)를 만들지 않는다. 기술 계층(layer)별 작업으로 쪼개지 않는다. 사용자가 볼 수 있는 행동 단위로 쓴다.

## 진행 절차 (Workflow)

1. `PRD.md`를 읽는다. 없으면 `/write-prd`부터 하자고 말한다.
2. `docs/agents/starter-skills.md`가 있으면 실행 환경과 접속 방식을 확인한다.
3. `CONTEXT.md`가 있으면 용어를 따른다.
4. TODO 초안(draft)을 `지금 할 일(Now)`, `다음 할 일(Next)`, `나중에 할 일(Later)`로 나눈다.
5. `지금 할 일(Now)`에는 바로 구현할 가장 작은 사용자가 볼 수 있는 작업(user-visible task) 하나만 둔다.
6. 사용자에게 순서가 맞는지 확인한다. 질문은 짧게 한다.
7. 승인되면 `TODO.md`를 작성하거나 업데이트한다.
8. 완료 기준(Done Rule)을 `TODO.md` 상단에 유지한다.

## 좋은 TODO (Good TODOs)

- [ ] 사용자가 이름을 입력하고 추가 버튼을 누르면 목록에 표시된다.
- [ ] 빈 값으로 추가하면 안내 문구가 보인다.
- [ ] 새로고침해도 방금 추가한 항목이 남아 있다.

## 나쁜 TODO (Bad TODOs)

- [ ] DB 스키마(schema) 만들기
- [ ] API 만들기
- [ ] 프론트엔드(frontend) 만들기
- [ ] 라이브러리 설치하기

이런 기술 작업은 필요하면 구현 중에 에이전트(agent)가 알아서 한다. `TODO.md`에는 사용자가 볼 수 있는 결과(user-visible outcome)를 쓴다.

## TODO.md 형식 (TODO.md Format)

```markdown
# TODO

## 완료 기준 (Done Rule)

TODO는 다음 조건을 만족하기 전까지 완료가 아니다.

- 앱을 로컬에서 실행했다.
- 바뀐 동작을 UI 또는 가장 가까운 인터페이스(interface)에서 확인했다.
- 결과를 쉬운 말로 보고했다.
- 확인하지 못한 것은 명확히 적었다.
- 화면이 있는 앱이면 `http://<network IPv4>:3000` 형식의 사용자 URL을 확인했다. `localhost`만 확인하고 완료라고 하지 않는다.

## 지금 할 일 (Now)

- [ ] 사용자가 볼 수 있는 작은 작업 하나.

## 다음 할 일 (Next)

- [ ] 그다음 사용자가 볼 수 있는 작은 작업 하나.

## 나중에 할 일 (Later)

- [ ] 선택 사항이거나 더 큰 아이디어.
```

## 완료 후

마지막에 다음 한 줄을 덧붙인다.

> 구현은 TODO 번호로 요청하세요. 예: "TODO 1번 해줘."
