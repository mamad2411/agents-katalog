---
name: curated-product-unboxing
description: 按揭盖、取出和定格组织一次开箱。 用户要求产品开箱时使用。
license: CC-BY-4.0
metadata:
  nomi:
    version: 1.0.0
    label: 产品开箱
    selectable-in-workbench: true
    tools: []
    required-providers:
      - video
    library:
      kind: skill
      title:
        zh-CN: 产品开箱
        en: Glass Serum Unbox
      summary:
        zh-CN: 按揭盖、取出和定格组织一次开箱。
        en: Adapt Glass Serum Unbox to the supplied references and check continuity.
      appliesTo:
        - video
      group:
        zh-CN: 广告
        en: Advertising
      slots:
        - token: '{品牌名}'
          reference: text
        - token: '{产品名}'
          reference: subject
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
        sourceUrl: https://raw.githubusercontent.com/LichAmnesia/awesome-ad-video-prompts/main/images/glass-serum-unbox.png
---

# 产品开箱

按揭盖、取出和定格组织一次开箱。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

Top-down macro on a fingertip-smooth matte-white box for {品牌名} {产品名}, a hydrating face serum, resting on cool gray riverstone. 0-2s: two thumbs press the magnetic lid, which lifts with a soft pneumatic sigh as a thin ribbon of breath-mist curls out of the cold interior. 2-4s: the frosted glass dropper bottle is drawn straight up out of its die-cut cradle, amber liquid sloshing in slow viscous waves, condensation beading and trailing down the chilled glass. 4-6s: the rubber bulb compresses and one fat golden droplet swells at the pipette tip, hangs trembling, then falls and ripples outward across a black mirror surface. Diffused overhead softbox, dewy specular highlights, faint room tone with a single wet pluck on the droplet impact. The bottle holds a consistent shape, label typography, and frosted finish across every frame; no deformation, drift, melting, duplicate droppers, or warped text.

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
