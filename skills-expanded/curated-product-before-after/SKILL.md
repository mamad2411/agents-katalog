---
name: curated-product-before-after
description: 通过擦镜转场展示同一产品的清洁变化。 用户要求清洁前后对比时使用。
license: CC-BY-4.0
metadata:
  nomi:
    version: 1.0.0
    label: 清洁前后对比
    selectable-in-workbench: true
    tools: []
    required-providers:
      - video
    library:
      kind: skill
      title:
        zh-CN: 清洁前后对比
        en: Sneaker Out Of Mud
      summary:
        zh-CN: 通过擦镜转场展示同一产品的清洁变化。
        en: Adapt Sneaker Out Of Mud to the supplied references and check continuity.
      appliesTo:
        - video
      group:
        zh-CN: 广告
        en: Advertising
      slots:
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
        sourceUrl: https://raw.githubusercontent.com/LichAmnesia/awesome-ad-video-prompts/main/images/sneaker-out-of-mud.png
---

# 清洁前后对比

通过擦镜转场展示同一产品的清洁变化。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

Studio-to-hero transformation, 1:1. Open on a battered white sneaker caked in dried mud under harsh flat overcast — scuffed, gray, joyless. [0-2s] locked low-angle hero shot, dust motes drifting, fully desaturated. [2-3s] a passing cloth swipes the lens for a fast whip-pan wipe transition, motion-blur smearing the frame. [3-6s] the wipe clears to reveal the same {产品名} silhouette spotless and crisp — knit texture sharp, midsole bright white, a soft rim light tracing the laces against clean studio key. [6-8s] slow orbit around the heel, micro-reflections gliding across fresh mesh, ground shadow tight and grounded. The shoe keeps identical proportions, logo placement, eyelet count, and lace pattern across both states — no deformation, morphing, or invented detailing. Implied sound: a stiff brush sweep, the clean snap of laces pulled tight.

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
