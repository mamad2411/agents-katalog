---
name: reddit-design
description: >
  Design no padrão Reddit: comunidade e conteúdo em feed de cards, laranja de marca #FF4500, votos
  (up/down), cantos arredondados, light e dark, tom casual. Use quando o usuário mencionar:
  "Reddit", "estilo Reddit", "fórum", "feed de comunidade", "votos up/down", "threads de comentários",
  "agregador de links", "subreddit", "design Reddit". Consulta ../_shared/design-resources.md.
---

# Reddit

Você atua como designer que domina a linguagem do Reddit. É **comunitário e conteúdo-primeiro**: milhares de comunidades (subreddits), feed de posts votáveis e threads de comentários aninhados. UI neutra que deixa o conteúdo e a discussão liderarem.

## Princípios

1. **Conteúdo em cards votáveis** — cada post é um card com votos, título, comunidade e ações. O voto (up/down) é central: define o que sobe.
2. **Laranja de marca** — `#FF4500` (upvote/marca) como acento energético; base neutra clara ou escura.
3. **Comunidade visível** — subreddit, autor, karma, flair. A UI comunica "de qual comunidade isso vem".
4. **Comentários aninhados** — threads com indentação e linhas de conexão; hierarquia de discussão clara.
5. **Casual e acessível** — tom leve, cantos arredondados, funciona em light/dark.

## Design tokens

```css
:root {                              /* Light */
  --rd-orange: #ff4500;              /* marca / upvote */
  --rd-upvote: #ff4500;
  --rd-downvote: #7193ff;
  --rd-bg: #dae0e6;                 /* fundo do feed (cinza-azulado) */
  --rd-surface: #ffffff;            /* card */
  --rd-text: #1a1a1b;
  --rd-text-muted: #7c7c7c;
  --rd-border: #ccc;
  --rd-blue: #0079d3;              /* links / ação */
  --rd-radius: 8px;
}
:root[data-theme="dark"] {
  --rd-bg: #030303; --rd-surface: #1a1a1b; --rd-text: #d7dadc;
  --rd-text-muted: #818384; --rd-border: #343536; --rd-blue: #4fbcff;
}
```

## Tipografia (system / IBM Plex-ish)

```css
font-family: 'IBM Plex Sans', -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
--rd-post-title: 500 18px/1.3;
--rd-body: 400 14px/1.5;
--rd-meta: 400 12px/1.4;             /* r/sub • u/user • 5h */
```

## Componentes-chave

```css
.rd-post {                           /* card de post com coluna de votos */
  display: flex; background: var(--rd-surface); border: 1px solid var(--rd-border);
  border-radius: var(--rd-radius); overflow: hidden;
}
.rd-votes { display: flex; flex-direction: column; align-items: center; gap: 4px;
  padding: 8px; background: #f8f9fa; }
.rd-vote-btn { background: none; border: none; color: var(--rd-text-muted); cursor: pointer; }
.rd-vote-btn--up.active { color: var(--rd-upvote); }
.rd-vote-btn--down.active { color: var(--rd-downvote); }
.rd-score { font-weight: 700; font-size: 12px; }

.rd-btn-primary {                    /* botões do Reddit são bem pill */
  background: var(--rd-blue); color: #fff; border: none; border-radius: 100px;
  padding: 0 16px; height: 32px; font: 700 14px/1 inherit;
}
.rd-flair { display: inline-block; padding: 2px 8px; border-radius: 20px;
  background: #edeff1; color: var(--rd-text); font-size: 12px; font-weight: 500; }
.rd-comment { border-left: 2px solid var(--rd-border); padding-left: 12px; margin-left: 8px; }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [reddit.com](https://www.reddit.com/) | Referência viva: cards votáveis, feed, comentários aninhados. |
| [Reddit Brand](https://www.redditinc.com/brand) | Uso do laranja, Snoo, logo, tom. |
| [Reddit — RPL (design system, dev docs)](https://www.reddit.com/dev/) | Componentes e padrões. |
| ../_shared/design-resources.md | Densidade, dark mode, ícones, acessibilidade. |

## Do / Don't

| Do | Don't |
|---|---|
| Voto up/down bem visível | Esconder o mecanismo de voto |
| Laranja `#FF4500` em marca/upvote | Laranja de fundo |
| Comunidade/flair visíveis | Post sem contexto de origem |
| Comentários aninhados com linha | Thread plana sem hierarquia |

## Checklist

- [ ] Feed de cards com coluna de votos (up/down)
- [ ] Laranja `#FF4500` marca/upvote; azul-roxo downvote
- [ ] Subreddit/autor/flair visíveis
- [ ] Comentários aninhados com indentação/linha
- [ ] Botões pill; cantos arredondados
- [ ] Light + dark mode
