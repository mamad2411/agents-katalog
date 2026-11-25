---
name: curated-product-exploded-view
description: 让部件分离展示后归位，保持产品结构。 用户要求产品爆炸视图时使用。
license: CC-BY-4.0
metadata:
  nomi:
    version: 1.0.0
    label: 产品爆炸视图
    selectable-in-workbench: true
    tools: []
    required-providers:
      - video
    library:
      kind: skill
      title:
        zh-CN: 产品爆炸视图
        en: Earbuds, Exploded-View Levitation
      summary:
        zh-CN: 让部件分离展示后归位，保持产品结构。
        en: Adapt Earbuds, Exploded-View Levitation to the supplied references and check continuity.
      appliesTo:
        - video
      group:
        zh-CN: 广告
        en: Advertising
      slots:
        - token: '{品牌名}'
          reference: text
      source:
        url: >-
          https://github.com/LichAmnesia/awesome-ad-video-prompts/blob/ac5b61177a81343e958f63212c4df7f25dc4c265/README.md
        revision: ac5b61177a81343e958f63212c4df7f25dc4c265
        author: LichAmnesia
        changes: >-
          Nomi adds Chinese task labels, reference slots and review criteria; fixed subjects are parameterized where
          noted.
        evidence:
          - >-
            https://github.com/LichAmnesia/awesome-ad-video-prompts/blob/ac5b61177a81343e958f63212c4df7f25dc4c265/README.md
      preview:
        path: assets/preview.png
        type: image
        provenance: upstream-output
        sourceUrl: >-
          https://raw.githubusercontent.com/LichAmnesia/awesome-ad-video-prompts/main/images/earbuds-exploded-view-levitation.png
---

# 产品爆炸视图

让部件分离展示后归位，保持产品结构。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

Wireless earbuds and their charging case float in exploded-view layout against a deep-navy gradient void, lit by one soft overhead box. 0-2s: components drift apart in zero gravity — lid, both buds, and silicone tips suspended and slowly rotating, brushed-metal and matte-plastic surfaces catching crisp specular highlights. 2-4s: a parallax orbit left as a cyan accent edge-light traces every seam, micro-reflections rolling along the glossy stems. 4-6s: the parts magnetically draw back together and seat with a clean close, {品牌名} etched on the hinge. Each part holds constant geometry, scale, and finish — no jitter, duplication, intersection clipping, or warping. Sound: weightless hum, a magnetic click, soft confirmation chime.

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
