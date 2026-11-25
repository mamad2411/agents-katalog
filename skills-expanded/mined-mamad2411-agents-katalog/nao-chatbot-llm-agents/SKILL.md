# chatbot_llm Agent Notes

- Keep this package as user-facing dialogue and route owner.
- Planner handoff is optional and must remain deterministic (structured payloads, no hidden side effects).
- Publish structured turn trace events for observability instead of relying on rosout parsing.
- Preserve social-turn dialogue routing unless explicit action intent is present.
- Do not embed plan objects in user_intent payloads; planner_llm owns plan generation.
- Keep planner handoff contracts free of legacy seams (`goal_token`, planner `ack_mode`, planner `ack_text`, `world_model_*` payloads).
- Build planner `grounded_context` with Hybrid Minimal T0 only (`knowledge_snapshot`, `scene_summary`, `state_t0`).
