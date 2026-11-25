---
name: curated-candle-mood
description: 用点火、暖光与烟雾营造安静氛围。 用户要求烛光氛围短片时使用。
license: CC-BY-4.0
metadata:
  nomi:
    version: 1.0.0
    label: 烛光氛围短片
    selectable-in-workbench: true
    tools: []
    required-providers:
      - video
    library:
      kind: skill
      title:
        zh-CN: 烛光氛围短片
        en: Candle, Ambient Slow Ignite
      summary:
        zh-CN: 用点火、暖光与烟雾营造安静氛围。
        en: Adapt Candle, Ambient Slow Ignite to the supplied references and check continuity.
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
          https://raw.githubusercontent.com/LichAmnesia/awesome-ad-video-prompts/main/images/candle-ambient-slow-ignite.png
---

# 烛光氛围短片

用点火、暖光与烟雾营造安静氛围。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

An amber-glass soy candle sits on a linen-draped oak table in a dim cozy room, dusk-blue window light behind and string lights bokeh-soft in the back. 0-2s: extreme macro on the cotton wick as a match touches it, the flame catches, sparks scatter in slow motion, and the glass begins to glow from within. 2-4s: a slow pull-back and crane-up, the flame mirrored in the molten wax pool while a thin ribbon of fragrant smoke rises and curls. 4-6s: a gentle orbit reveals the {品牌名} kraft label as the warm glow deepens. 6-8s: the move settles, the flame steadies, ambient amber light filling the frame. Candle keeps consistent vessel shape, wax level, and label across the shot — no flame teleporting, label distortion, or drift. Sound: a match strike, a soft crackle, a quiet ambient hush.

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
