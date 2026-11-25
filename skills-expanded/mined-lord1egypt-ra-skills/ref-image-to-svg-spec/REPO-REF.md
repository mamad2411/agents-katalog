# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/r/ref-image-to-svg-spec/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 把一张栅格参考图（图标表、牌面表、UI 截图、设计稿切图）复刻成 SVG / Canvas 手绘图形时，用像素级测量代替目测：自动切分网格、按色系采样真色、连通域量出每个元素的位置尺寸并换算成 viewBox 坐标，最后生成「参考图 vs 本项目」并排对照页验证，再用结构计数断言（n 个点 = n 个圆）把结果钉死。当用户说「按这张图的图案改」「照着这个图做图标」「复刻这套牌面 / 表情 / 图标
