# Repo Ref
- source: https://github.com/aws-samples/sample-oh-my-aidlcops (path: plugins/agenticops/skills/autopilot-deploy/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Agent 또는 skill의 프로덕션 배포를 canary 1% → 10% → 50% → 100% 4단계로 자동 진행한다. 각 단계는 continuous-eval 통과와 SLO 준수를 gate로 하며 circuit breaker가 SLO 위반을 감지하면 즉시 이전 단계로 자동 롤백한다. 100% 승격은 사람 승인이 필수다.
