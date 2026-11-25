---
name: curated-expression-reference
description: 参考第二张图的表情，保留第一张图的人物。 用户要求参考表情迁移时使用。
license: Apache-2.0
metadata:
  nomi:
    version: 1.0.0
    label: 参考表情迁移
    selectable-in-workbench: true
    tools: []
    required-providers:
      - image
    library:
      kind: skill
      title:
        zh-CN: 参考表情迁移
        en: Match a reference expression
      summary:
        zh-CN: 参考第二张图的表情，保留第一张图的人物。
        en: Transfer the expression reference while retaining the target character identity.
      appliesTo:
        - image
      group:
        zh-CN: 角色与场景
        en: Character and scene
      slots: []
      source:
        url: https://github.com/PicoTrex/Awesome-Nano-Banana-images/blob/2558bf0bb825be150c5d1aeab918cd90004882d3/README.md
        revision: 2558bf0bb825be150c5d1aeab918cd90004882d3
        author: https://x.com/ZHO_ZHO_ZHO/status/1963156830458085674
        changes: >-
          Nomi adds Chinese task labels, reference slots and review criteria; fixed subjects are parameterized where
          noted.
        evidence:
          - https://x.com/ZHO_ZHO_ZHO/status/1963156830458085674
          - https://x.com/ZHO_ZHO_ZHO
      preview:
        path: assets/preview.jpg
        type: image
        provenance: upstream-output
        sourceUrl: https://raw.githubusercontent.com/PicoTrex/Awesome-Nano-Banana-images/main/images/case34/case.jpg
---

# 参考表情迁移

参考第二张图的表情，保留第一张图的人物。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

图一人物参考/换成图二人物的表情

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
