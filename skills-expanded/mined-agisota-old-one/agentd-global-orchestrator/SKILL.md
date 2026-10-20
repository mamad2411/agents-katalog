---
name: agentd-global-orchestrator
description: "Единый глобальный оркестратор AgentD для полного автопилота: принимает один prompt и сам делает планирование, dispatch subagents, skill-routing, MCP-подключение, проверки, визуальную выдачу и опции следующих шагов. Использовать когда пользователь просит \"сделай всё сам\", \"автопилот\", \"единый агент\", \"single command workflow\", \"one-shot pipeline\", \"AgentD\"."
see-also: [autopilot]
triggers:
  keywords: [agentd, orchestrator, autopilot, do everything, single command, one-shot, pipeline]
  intent: [orchestration, planning]
activation: forced
priority: 80
packs: [orchestration, planning]
---
