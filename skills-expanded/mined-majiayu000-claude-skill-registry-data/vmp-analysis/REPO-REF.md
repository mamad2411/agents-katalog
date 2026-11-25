# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: security/vmp-analysis/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 字节码 VM / VMP 壳逆向的执行流水线：从"确认是 VM"到"反汇编出可读指令"的 8 步固定流程。用 profile 描述编码模型（换壳只换 JSON），用动态 trace 反推 opcode 编码，用命中率 > 95% 验收。当目标是"业务方法在 .text 里找不到、JNI_OnLoad 只启动解释器"、或已有 opcode 表但不知道指令怎么解时使用。SO 层深挖的单步能力，入口仍在
