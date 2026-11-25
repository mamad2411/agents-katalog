# Repo Ref
- source: https://github.com/liushengjia-aal/shengjia (path: denso-rh850-map-inventory/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 从 ECU【代码】里扫出全表清单——不是盲扫形态猜地址，而是找到通用查表例程(reader)、扫出所有调用点，让 ECU 自己的解析逻辑告诉你每张表的描述符/维度/轴/行距/移位量/调用者数。主用于 DENSO Renesas RH850·V850（丰田/雷克萨斯），同套方法可迁移到任何"自描述表对象"式 ECU。当用户说"这个 DENSO/丰田 bin 有哪些表""帮我把这个 ECU 的 map
