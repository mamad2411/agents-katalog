---
name: curated-product-turntable
description: 保持鞋型和细节，完成转台环绕展示。 用户要求转台产品广告时使用。
license: CC-BY-4.0
metadata:
  nomi:
    version: 1.0.0
    label: 转台产品广告
    selectable-in-workbench: true
    tools: []
    required-providers:
      - video
    library:
      kind: skill
      title:
        zh-CN: 转台产品广告
        en: Sneaker, 360 Turntable Studio
      summary:
        zh-CN: 保持鞋型和细节，完成转台环绕展示。
        en: Adapt Sneaker, 360 Turntable Studio to the supplied references and check continuity.
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
          https://raw.githubusercontent.com/LichAmnesia/awesome-ad-video-prompts/main/images/sneaker-360-turntable-studio.png
---

# 转台产品广告

保持鞋型和细节，完成转台环绕展示。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

A single hero sneaker rests on an invisible acrylic turntable inside a seamless graphite cyclorama, dust motes drifting in the light. 0-2s: low hero angle, slow dolly-in as a hard top light rakes the knit upper, every stitch and the matte-to-gloss midsole gradient resolving crisply. 2-4s: the shoe makes a controlled 180-degree turntable rotation on its long axis while a magenta-to-teal gel sweep travels the outsole lugs. 4-6s: the spin eases to a clean three-quarter front, the sole flexing once with a subtle natural bounce, the {品牌名} heel logo tack-sharp. Upper keeps the same lace pattern, colorway, and silhouette across the full turn — no warping, smearing, duplicated eyelets, or temporal flicker. Sound: airy whoosh, faint rubber squeak, a deep sub hit on the lock.

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
