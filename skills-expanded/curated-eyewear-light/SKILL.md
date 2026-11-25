---
name: curated-eyewear-light
description: 用移动光线表现镜片与镜架材质。 用户要求眼镜光轨广告时使用。
license: CC-BY-4.0
metadata:
  nomi:
    version: 1.0.0
    label: 眼镜光轨广告
    selectable-in-workbench: true
    tools: []
    required-providers:
      - video
    library:
      kind: skill
      title:
        zh-CN: 眼镜光轨广告
        en: Eyewear, Motion-Control Light Streaks
      summary:
        zh-CN: 用移动光线表现镜片与镜架材质。
        en: Adapt Eyewear, Motion-Control Light Streaks to the supplied references and check continuity.
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
          https://raw.githubusercontent.com/LichAmnesia/awesome-ad-video-prompts/main/images/eyewear-motion-control-light-streaks.png
---

# 眼镜光轨广告

用移动光线表现镜片与镜架材质。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

Acetate sunglasses rest on a polished black acrylic plinth in a dark studio threaded with thin colored light streaks, the plinth giving a crisp mirror reflection beneath. 0-2s: a motion-control macro slide tracks along the temple arm as a sweeping amber streak runs its full length, revealing tortoiseshell grain and bevel polish, the lenses mirroring the beam. 2-4s: the frame tilts to face camera while twin gradient sources — coral above, electric blue below — glide across the lenses and pull a clean horizontal anamorphic flare. 4-6s: a tight orbit lands on a hero three-quarter, the {品牌名} temple emblem catching one sharp glint. Frame holds constant shape, hinge position, and lens tint — no bending arms, smearing, or reflection artifacts. Sound: an airy synth swell, a subtle glass shimmer, one resonant chime.

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
