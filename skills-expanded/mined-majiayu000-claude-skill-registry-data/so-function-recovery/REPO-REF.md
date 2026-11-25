# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: bash/so-function-recovery/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 大型加固 SO 函数级还原流水线（2000+ 函数、无 .eh_frame、CFF 混淆、内嵌字节码 VM）。用台账三层筛选替代逐个读函数，用指针表交叉检查函数边界，用动态 trace 反推 VM 编码，最终产出完整逻辑闭环。当任务是"把某个 .so 的主要代码逻辑搞清楚"、要判断"分析到什么程度算完成"、或不想重复读同一批函数时使用。
