# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: data/system-test-integration/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: System 테스트 작성 및 실행. pytest 기반, docker-compose.acceptance.yml 필수, 4단계 순서(infra→component→integration→scenarios). 네이밍 test_{대상}_{시나리오}_{예상결과}. poetry run pytest system-tests/ 실행. Fail Fast - 모든 응답 필드/타입
