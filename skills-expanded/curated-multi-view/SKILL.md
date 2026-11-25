---
name: curated-multi-view
description: 把同一主体整理成一致的多面设定。 用户要求多视图设定时使用。
license: Apache-2.0
metadata:
  nomi:
    version: 1.0.0
    label: 多视图设定
    selectable-in-workbench: true
    tools: []
    required-providers:
      - image
    library:
      kind: skill
      title:
        zh-CN: 多视图设定
        en: Multiple views
      summary:
        zh-CN: 把同一主体整理成一致的多面设定。
        en: Generate consistent views of the same subject from a reference image.
      appliesTo:
        - image
      group:
        zh-CN: 角色与场景
        en: Character and scene
      slots: []
      source:
        url: https://github.com/PicoTrex/Awesome-Nano-Banana-images/blob/2558bf0bb825be150c5d1aeab918cd90004882d3/README.md
        revision: 2558bf0bb825be150c5d1aeab918cd90004882d3
        author: https://x.com/Error_HTTP_404/status/1960405116701303294
        changes: >-
          Nomi adds Chinese task labels, reference slots and review criteria; fixed subjects are parameterized where
          noted.
        evidence:
          - https://x.com/Error_HTTP_404/status/1960405116701303294
          - https://x.com/Error_HTTP_404
      preview:
        path: assets/preview.jpg
        type: image
        provenance: upstream-output
        sourceUrl: https://raw.githubusercontent.com/PicoTrex/Awesome-Nano-Banana-images/main/images/case23/output.jpg
---

# 多视图设定

把同一主体整理成一致的多面设定。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

在白色背景上生成前、后、左、右、上、下视图。均匀分布。一致的主体。等距透视等效

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
