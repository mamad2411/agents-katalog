# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/p/pg-game-monitor/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Prometheus + Grafana 监控方案，专为**单台物理机部署多个 Java 游戏进程 + 自建 MySQL**的场景设计。Java 进程通过 jstat/jcmd 无侵入采集 JVM 运行时指标（堆内存、新生代、老年代、GC、线程、类内存），MySQL 通过 pymysql 采集（Buffer Pool、进程内存）。监控重点围绕**内存使用率**，适配游戏服高频 GC 和大内存占用的
