# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/c/canvas-render-optimize/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Canvas 2D大规模渲染优化方案。当Canvas需要渲染大量元素（5000+）导致掉帧、卡顿时使用。包含三层渲染管线（OffscreenCanvas静态层+脏矩形动态层+UI叠加层）、空间哈希视口裁剪、LOD细节层次、requestAnimationFrame帧调度。适用于晶圆图(WaferMap)、热力图、散点图、地图标注、甘特图等场景。实测100k元素从1fps优化到55fps。
