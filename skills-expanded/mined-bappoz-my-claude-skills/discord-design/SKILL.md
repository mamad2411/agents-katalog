---
name: discord-design
description: >
  Design no padrão Discord: dark-first, Blurple #5865F2 de marca, tipografia gg sans, cantos
  arredondados, tom lúdico de comunidade/gaming e densidade de chat (canais, roles, presença). Use
  quando o usuário mencionar: "Discord", "estilo Discord", "app de comunidade", "chat de servidor",
  "gaming chat", "canais e roles", "design Discord". Consulta ../_shared/design-resources.md.
---

# Discord

Você atua como designer que domina a linguagem do Discord. É **dark, lúdico e social**: uma casa para comunidades onde o chat é o centro, o Blurple é a assinatura e nada é sério demais.

## Princípios

1. **Dark-first** — o app vive no escuro; light mode é secundário. Fundos em cinzas-azulados profundos.
2. **Blurple é a marca** — `#5865F2` em ação primária, links, menções e branding. Nunca como fundo de tela inteira.
3. **Densidade de chat** — sidebar de servidores + canais + lista de mensagens + membros; muita informação, hierarquia por cor/peso.
4. **Tom lúdico** — cantos arredondados, emojis, empty states com humor, microinterações divertidas (sem infantilizar).

## Design tokens

```css
:root {                              /* Discord dark (novo) */
  --dcd-blurple: #5865f2;
  --dcd-blurple-hover: #4752c4;
  --dcd-bg: #313338;                 /* área de chat */
  --dcd-bg-sidebar: #2b2d31;         /* lista de canais */
  --dcd-bg-server: #1e1f22;          /* barra de servidores */
  --dcd-bg-input: #383a40;
  --dcd-text: #f2f3f5;
  --dcd-text-muted: #b5bac1;
  --dcd-green: #23a55a;              /* online */
  --dcd-red: #f23f43;               /* danger / DND */
  --dcd-yellow: #f0b232;            /* idle */
  --dcd-radius: 8px;
}
:root[data-theme="light"] {
  --dcd-bg: #ffffff; --dcd-bg-sidebar: #f2f3f5; --dcd-bg-server: #e3e5e8;
  --dcd-text: #060607; --dcd-text-muted: #4e5058;
}
```

## Tipografia (gg sans / fallback)

```css
/* gg sans é proprietária. Fallback próximo: */
font-family: 'gg sans', 'Noto Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;
--dcd-title: 700 20px/1.25;
--dcd-channel: 500 16px/1.3;         /* nome de canal */
--dcd-body: 400 16px/1.375;          /* mensagem */
--dcd-meta: 500 12px/1.3;            /* timestamp, uppercase headers */
```

## Componentes-chave

```css
.dcd-btn-primary {
  background: var(--dcd-blurple); color: #fff; border: none; border-radius: 3px;
  padding: 2px 16px; min-height: 38px; font: 500 14px/1 'gg sans'; transition: background .17s;
}
.dcd-btn-primary:hover { background: var(--dcd-blurple-hover); }

.dcd-channel {                       /* item de canal na sidebar */
  display: flex; align-items: center; gap: 6px; padding: 6px 8px; margin: 0 8px;
  border-radius: 4px; color: var(--dcd-text-muted); cursor: pointer;
}
.dcd-channel:hover { background: #35373c; color: var(--dcd-text); }
.dcd-channel--active { background: #404249; color: #fff; }

.dcd-message:hover { background: rgba(2,2,2,.06); }   /* hover discreto na mensagem */
.dcd-status { width: 10px; height: 10px; border-radius: 50%; border: 3px solid var(--dcd-bg-sidebar); }
.dcd-status--online { background: var(--dcd-green); }
.dcd-mention { background: rgba(88,101,242,.3); color: #c9cdfb; border-radius: 3px; padding: 0 2px; }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [discord.com/branding](https://discord.com/branding) | Uso do Blurple, logo, mascote, tom de voz. |
| [Discord Design (blog)](https://discord.com/blog) | Estudos de caso de produto/UI. |
| [Discord Developer — UI kit](https://discord.com/developers/docs/intro) | Componentes de bots/embeds (cores, layout). |
| ../_shared/design-resources.md | Dark mode, densidade, microinterações. |

## Do / Don't

| Do | Don't |
|---|---|
| Dark-first, cinzas azulados | Fundo branco por padrão |
| Blurple em ação/menção | Blurple de fundo inteiro |
| Status colorido (online/idle/dnd) | Presença sem cor |
| Tom lúdico com moderação | Infantilizar / poluir |

## Checklist

- [ ] Dark-first (bg `#313338`, sidebar `#2b2d31`, servidores `#1e1f22`)
- [ ] Blurple `#5865F2` só em ação/link/menção
- [ ] Canais com estado hover/ativo
- [ ] Indicadores de presença coloridos
- [ ] Cantos arredondados + tom lúdico
- [ ] Light mode como alternativa
