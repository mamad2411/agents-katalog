---
name: duolingo-design
description: >
  Design no padrão Duolingo: gamificação amigável, verde Feather #58CC02, botões 3D com sombra
  inferior, cantos bem arredondados, mascote e feedback lúdico que motiva. Use quando o usuário
  mencionar: "Duolingo", "estilo Duolingo", "app gamificado", "gamificação", "app de aprendizado",
  "streak", "mascote", "UI divertida e motivadora", "design Duolingo". Consulta
  ../_shared/design-resources.md.
---

# Duolingo

Você atua como designer que domina a linguagem do Duolingo. É **divertido, gamificado e encorajador**: cores vivas, botões que parecem apertáveis (3D), mascote presente e feedback que celebra cada acerto. O design faz o usuário querer voltar amanhã.

## Princípios

1. **Gamificação motivadora** — streaks, XP, ligas, corações. A UI transforma estudo em jogo (progresso visível recompensa o retorno).
2. **Botões 3D "chunky"** — a assinatura visual: sombra sólida embaixo que "afunda" ao apertar. Convida ao toque.
3. **Amigável, nunca punitivo** — erro é gentil (Duo triste, não bronca); acerto é celebrado (som, confete, animação).
4. **Cor viva com propósito** — verde Feather para acerto/ação; cada elemento gamificado tem sua cor (streak laranja, gems azul).
5. **Mascote como guia** — Duo (a coruja) dá personalidade, reage, motiva e lembra de voltar.

## Design tokens

```css
:root {
  --duo-green: #58cc02;              /* Feather Green: ação/acerto */
  --duo-green-shadow: #58a700;       /* sombra 3D do botão verde */
  --duo-blue: #1cb0f6;               /* gems / info */
  --duo-blue-shadow: #1899d6;
  --duo-red: #ff4b4b;                /* erro (gentil) */
  --duo-orange: #ff9600;             /* streak / fogo */
  --duo-yellow: #ffc800;             /* XP / estrelas */
  --duo-text: #3c3c3c;
  --duo-text-muted: #afafaf;
  --duo-bg: #ffffff;
  --duo-border: #e5e5e5;
  --duo-radius: 16px;
}
:root[data-theme="dark"] {
  --duo-bg: #131f24; --duo-text: #f1f7fb; --duo-text-muted: #52656d; --duo-border: #37464f;
}
```

## Tipografia (din-round / Feather Bold, fallback arredondado)

```css
/* Duolingo usa 'din-round' / 'Feather'. Fallback arredondado: */
font-family: 'din-round', 'Nunito', 'Baloo 2', system-ui, sans-serif;
--duo-display: 800 28px/1.2;         /* muito bold, arredondado */
--duo-title: 700 19px/1.3;
--duo-body: 500 17px/1.4;
--duo-button: 700 15px/1;            /* uppercase nos CTAs */
```

## Componentes-chave

```css
/* Botão 3D "chunky" — a assinatura Duolingo */
.duo-btn {
  background: var(--duo-green); color: #fff; border: none;
  border-radius: var(--duo-radius); padding: 14px 20px; width: 100%;
  font: 700 15px/1 'din-round'; text-transform: uppercase; letter-spacing: .8px;
  box-shadow: 0 4px 0 var(--duo-green-shadow);   /* a "espessura" 3D */
  transition: transform .1s, box-shadow .1s; cursor: pointer;
}
.duo-btn:active {                    /* afunda ao apertar */
  transform: translateY(4px); box-shadow: 0 0 0 var(--duo-green-shadow);
}
.duo-btn--secondary { background: var(--duo-bg); color: var(--duo-blue);
  border: 2px solid var(--duo-border); box-shadow: 0 4px 0 var(--duo-border); }

.duo-card {                          /* card de lição arredondado */
  background: var(--duo-bg); border: 2px solid var(--duo-border);
  border-radius: var(--duo-radius); padding: 16px; box-shadow: 0 2px 0 var(--duo-border);
}
.duo-streak { display: inline-flex; align-items: center; gap: 4px; color: var(--duo-orange);
  font-weight: 800; }   /* 🔥 27 */
.duo-progress { height: 16px; border-radius: 999px; background: var(--duo-border); overflow: hidden; }
.duo-progress__fill { height: 100%; background: var(--duo-green); border-radius: 999px; }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [duolingo.com](https://www.duolingo.com/) | Referência viva: botões 3D, streaks, mascote, celebração. |
| [Duolingo Design (blog)](https://blog.duolingo.com/tag/design/) | Estudos de caso de gamificação e craft. |
| [Duolingo Brand](https://design.duolingo.com/) | Cores, mascote Duo, tom, ilustração. |
| [LottieFiles](https://lottiefiles.com/pt/) | Animações de celebração/mascote (confete, reações). |
| ../_shared/design-resources.md | Fontes arredondadas, animação, microinterações. |

## Do / Don't

| Do | Don't |
|---|---|
| Botão 3D com sombra inferior | Botão flat sem profundidade |
| Erro gentil (mascote triste) | Bronca/punição por errar |
| Celebrar acerto (som/animação) | Feedback seco |
| Cores vivas com função (streak/xp/gems) | Cor aleatória sem significado |

## Checklist

- [ ] Botões 3D "chunky" (sombra inferior sólida, afunda ao apertar)
- [ ] Verde Feather `#58CC02` em ação/acerto
- [ ] Cantos bem arredondados (16px)
- [ ] Gamificação visível (streak, XP, progresso, ligas)
- [ ] Feedback lúdico: erro gentil, acerto celebrado
- [ ] Fonte arredondada + mascote/personalidade + dark mode
