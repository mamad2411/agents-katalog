# Repo Ref
- source: https://github.com/cxcscmu/skilllearnbench (path: skills/b3-teacher-feedback-claude-haiku-4-5/fix-security-bug/run3_Input-Stream-Validation-Before-Jackson-Deserialization/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: Validate and sanitize raw JSON input at the point where it enters Jackson's deserialization pipeline, before any ObjectMapper.readValue() call processes it, to prevent bypass attacks using empty keys.
