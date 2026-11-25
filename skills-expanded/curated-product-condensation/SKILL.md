---
name: curated-product-condensation
description: 用微距、水滴和环绕镜头展示产品质感。 用户要求凝露产品广告时使用。
license: CC-BY-4.0
metadata:
  nomi:
    version: 1.0.0
    label: 凝露产品广告
    selectable-in-workbench: true
    tools: []
    required-providers:
      - video
    library:
      kind: skill
      title:
        zh-CN: 凝露产品广告
        en: Frost-Glass Serum, Condensation Macro
      summary:
        zh-CN: 用微距、水滴和环绕镜头展示产品质感。
        en: Adapt Frost-Glass Serum, Condensation Macro to the supplied references and check continuity.
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
          https://raw.githubusercontent.com/LichAmnesia/awesome-ad-video-prompts/main/images/frost-glass-serum-condensation-macro.png
---

# 凝露产品广告

用微距、水滴和环绕镜头展示产品质感。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

A frosted-glass serum bottle stands on wet black slate, half-buried in low-rolling cold fog, a single cool key light raking from camera-left. 0-2s: extreme macro push-in across the condensation field, beads trembling and sliding, dewy texture razor-sharp at f2.8 with creamy fall-off. 2-4s: the mist thins on a slow exhale, the glass pipette lifts and one amber drop releases in slow motion, surface tension holding a perfect bead before it lands. 4-6s: a 30-degree clockwise orbit wraps a warm rim light around the {品牌名} label, the glass throwing a faint prismatic edge. Bottle holds constant shape, fill level, and matte finish throughout — no deformation, drift, melting, or flicker. Implied sound: low room tone, a soft glass tick, one droplet plink.

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
