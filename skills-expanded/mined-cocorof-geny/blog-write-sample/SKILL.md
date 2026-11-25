---
name: blog-write-sample
description: Sample skill — external delegation template. Copy this to ~/.geny/skills/ and adapt for your own external API delegation tools.
allowed_tools:
  - blog_agent_delegate
  - blog_agent_status
  - blog_agent_cancel
  - blog_agent_list_posts
  - blog_agent_get_post
model_override: claude-sonnet-4-6
execution_mode: inline
category: example
effort: medium
examples:
  - "Write a sample blog post about LangGraph"
  - "Show progress on my last delegated task"
---

# Blog Write — Sample / Template

> **이 파일은 학습용 샘플입니다.** 실제로 사용하려면:
> 1. SkillsTab → CUSTOM 샘플 섹션 → "Copy to my skills" 버튼으로 `~/.geny/skills/` 로 복사
> 2. 복사된 파일의 `name`을 자기 슬러그로 바꾸기 (예: `my-blog-write`)
> 3. `allowed_tools` 의 도구 이름과 본문의 호출 예시를 자기 시나리오에 맞게 수정
> 4. SkillsTab 상단에서 `user_skills_enabled` 토글이 ON 인지 확인 — Off면 user-skills 자체가 로드되지 않습니다

이 샘플은 [`blog_write`](../bundled/blog_write/SKILL.md) (Geny-bundled) 와 동일한 동작을 하지만, **외부 API 위임 패턴을 직접 따라 쓰기 위한 주석이 풍부한 버전**입니다.

---

## 핵심 패턴 — **fire-and-poll 위임**

이 패턴은 다음 3가지 조건을 만족하는 외부 시스템에 적합합니다:

1. **시간이 걸리는 작업** (5초 이상): 답이 즉시 안 옴.
2. **사용자가 결과를 기다림**: 사용자는 알림이 필요.
3. **외부 시스템이 SSE / webhook 등으로 완료를 알릴 수 있음**: Geny의 inbox 로 결과 도착 가능.

블로그 위임은 위 3가지를 다 만족. 만약 본인이 만들 도구가 동기적으로 답하면(예: 단순 GET API), 굳이 이 패턴을 쓸 필요 없고 그냥 직접 호출 → paraphrase 하면 됩니다.

---

## A. 새 작업 위임

```
<your_delegate_tool>(
  task="<외부 AI 에게 줄 지시문 — 자세히>",
  task_summary="<사용자에게 들려줄 한 줄, 5단어 이내>"
)
```

위임 후:
- 사용자에게는 **"맡겼어. 잠깐만 기다려."** 정도로만.
- **당신의 turn 은 여기서 종료**. 백그라운드 진행.
- 끝나면 `[EXTERNAL_TASK_RESULT]` 메시지가 새 turn 에서 도착 → 그때 결과를 paraphrase.

## B. 진행 상황 확인

사용자가 묻기 전에 status 를 폴링하지 말 것. **사용자가 물을 때만** 호출하고, JSON / task_id 를 노출하지 말고 자연어로:

```
<your_status_tool>(task_id="...")
→ 결과의 progress_hint, elapsed_s, last_event_age_s 를 보고 1-2 문장으로 답
```

## C. 취소

사용자가 명시적으로 "취소", "그만" 등을 표현하면:

```
<your_cancel_tool>(task_id="...")
```

## D. 참고 조회

읽기 전용 lookup 도구 (이 sample 의 `list_posts` / `get_post`)는 사용자가 **명시적으로** 요청할 때만 호출. 위임의 사전 조사로 자동 호출하지 말 것 — 지연만 늘어남.

---

## 자신만의 외부 위임 skill 만들 때 체크리스트

- [ ] `allowed_tools` 에 외부 시스템의 모든 도구 이름이 들어갔는가?
- [ ] `task_summary` 길이 제한이 description 에 명시되어 있나?
- [ ] turn 종료 시점이 명확한가? (delegate 직후 종료, 결과 도착 시 paraphrase)
- [ ] 사용자에게 내부 식별자 (task_id, UUID 등) 노출 금지를 명시했나?
- [ ] 동시 위임 상한 / 중복 호출 금지가 description 에 있나?

## 추가 자료

- [docs/custom_tools.md](../../../docs/custom_tools.md) — 외부 API 자체를 도구로 등록하는 방법 (HTTP backend)
- [docs/skills.md](../../../docs/skills.md) — SKILL.md 형식과 LLM 노출 메커니즘
- 실제 동작 참고: [blog_write SKILL.md](../bundled/blog_write/SKILL.md)
