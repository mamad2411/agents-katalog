---
name: slack-design
description: >
  Design no padrão Slack: workspace de trabalho com sidebar aubergine #4A154B, área de mensagens
  clara, tipografia Lato, densidade de chat organizada por canais/threads e tom profissional-amigável.
  Use quando o usuário mencionar: "Slack", "estilo Slack", "app de trabalho em equipe", "chat
  corporativo", "canais e threads", "workspace", "colaboração de time", "design Slack". Consulta
  ../_shared/design-resources.md.
---

# Slack

Você atua como designer que domina a linguagem do Slack. É **profissional mas humano**: uma ferramenta de trabalho séria que não é chata. Sidebar roxo-berinjela característico, área de conversa clara, e organização por canais/threads.

## Princípios

1. **Sidebar aubergine + conteúdo claro** — a navegação vive num roxo escuro de marca; a área de mensagens é clara e legível para o dia inteiro de leitura.
2. **Organização por canais/threads** — conversas estruturadas (canais, DMs, threads) reduzem ruído. A UI deixa a hierarquia óbvia.
3. **Profissional-amigável** — emojis, reactions e tom leve, mas sem virar bagunça. Trabalho com personalidade.
4. **Densidade legível** — muita mensagem, mas com respiro, avatares e agrupamento por autor.

## Design tokens

```css
:root {
  --slk-aubergine: #4a154b;          /* sidebar / marca */
  --slk-aubergine-hover: #350d36;
  --slk-active: #1164a3;             /* item de canal ativo */
  --slk-bg: #ffffff;                 /* área de mensagens */
  --slk-text: #1d1c1d;
  --slk-text-muted: #616061;
  --slk-border: #e2e2e2;
  --slk-green: #007a5a;             /* online / botão primário */
  --slk-highlight: #ffde63;         /* menção / destaque */
  --slk-radius: 8px;
}
:root[data-theme="dark"] {
  --slk-bg: #1a1d21; --slk-text: #d1d2d3; --slk-text-muted: #ababad;
  --slk-border: #35373b; --slk-aubergine: #19171d;
}
```

## Tipografia (Lato / fallback)

```css
font-family: 'Lato', 'Slack-Lato', -apple-system, 'Segoe UI', Roboto, sans-serif;
--slk-title: 900 18px/1.3 'Lato';    /* nomes/headers em black weight */
--slk-channel: 700 15px/1.3;
--slk-body: 400 15px/1.46;           /* mensagem */
--slk-meta: 400 12px/1.3;            /* timestamp */
```

## Componentes-chave

```css
.slk-sidebar { background: var(--slk-aubergine); color: rgba(255,255,255,.7); width: 260px; }
.slk-channel { display: flex; align-items: center; gap: 8px; padding: 4px 16px;
  border-radius: 6px; margin: 0 8px; cursor: pointer; }
.slk-channel:hover { background: var(--slk-aubergine-hover); }
.slk-channel--active { background: var(--slk-active); color: #fff; font-weight: 700; }

.slk-btn-primary {                   /* verde característico */
  background: var(--slk-green); color: #fff; border: none; border-radius: var(--slk-radius);
  padding: 0 16px; height: 36px; font: 700 14px/1 'Lato'; transition: background .1s;
}
.slk-btn-primary:hover { background: #148567; }
.slk-btn { background: var(--slk-bg); color: var(--slk-text);
  border: 1px solid #868686; border-radius: var(--slk-radius); height: 36px; padding: 0 16px; font-weight: 700; }

.slk-message { display: flex; gap: 8px; padding: 8px 20px; }
.slk-message:hover { background: #f8f8f8; }
.slk-reaction { display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px;
  border: 1px solid var(--slk-border); border-radius: 12px; font-size: 12px; }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [slack.design](https://slack.design/) | Filosofia de design, estudos de caso, ilustração. |
| [Slack Brand](https://brand.slack.com/) | Uso de aubergine, logo, tipografia Lato. |
| [Slack Kit / Block Kit](https://api.slack.com/block-kit) | Componentes de UI para apps/mensagens (layout, blocks). |
| ../_shared/design-resources.md | Densidade de chat, dark mode, ícones. |

## Do / Don't

| Do | Don't |
|---|---|
| Sidebar aubergine + conteúdo claro | Tela inteira roxa |
| Verde `#007A5A` em ação primária | Roxo em botão de ação |
| Canais/threads bem hierarquizados | Timeline plana sem estrutura |
| Lato black nos títulos | Fonte fina nos headers |

## Checklist

- [ ] Sidebar aubergine `#4A154B`, área de mensagens clara
- [ ] Canal ativo destacado (`#1164A3`)
- [ ] Botão primário verde `#007A5A`
- [ ] Mensagens agrupadas por autor + reactions em pill
- [ ] Lato (black nos títulos) ou fallback
- [ ] Dark mode
