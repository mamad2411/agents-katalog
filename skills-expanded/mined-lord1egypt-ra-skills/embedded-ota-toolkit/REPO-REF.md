# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/e/embedded-ota-toolkit/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 嵌入式 OTA/Bootloader 升级链路检查与打包工具。审计侧静态扫描升级代码的防砖漏洞（每条附可直接粘贴的修复代码）：跳转 APP 未重定位中断向量表（VTOR）、跳转前未关中断、未校验 APP 有效性、升级数据无 CRC/哈希、flash 擦除地址未按页对齐、擦写期间未喂看门狗、分区地址硬编码、接收等待无超时、无防降级版本校验、升级状态未持久化、写入前未擦除、关闭看门狗后未恢复等；工具侧
