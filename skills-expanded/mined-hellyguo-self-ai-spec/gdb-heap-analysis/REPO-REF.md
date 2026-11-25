# Repo Ref
- source: https://github.com/hellyguo/self-ai-spec (path: skills/gdb-heap-analysis/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 使用 GDB 分析 core dump 中的 glibc ptmalloc 堆与 arena，定位内存泄漏、内存占用异常与堆损坏；覆盖 arena chunk 链与 IS_MMAPPED/mmap 分配。触发场景：内存泄漏分析、core dump 排查、arena 与 malloc_state 分析、glibc 堆调试、malloc 内部结构问题、mmap 大块分配统计。"
