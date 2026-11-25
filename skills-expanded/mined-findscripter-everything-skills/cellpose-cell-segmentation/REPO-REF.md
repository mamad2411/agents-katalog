# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 09-verticals/cellpose-cell-segmentation/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当需要在荧光/明场显微图像中分割单个细胞或细胞核、且阈值法因强度不均或细胞贴边而失效时使用；用 Cellpose 预训练流场模型（cyto3/nuclei/tissuenet）免调参产出整数标签掩膜（每细胞唯一 ID），可批处理、3D、并接 regionprops 量形态学；不适用于细胞分得开且阈值/分水岭已够（用 scikit-image watershed）、星凸核优化（用 StarDist）
