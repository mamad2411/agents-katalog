---
name: twitch-design
description: >
  Design no padrão Twitch: dark-first, roxo de marca #9146FF, tipografia Roobert, layout de live
  (player + chat lateral), tom de comunidade/streaming e microinterações (emotes). Use quando o
  usuário mencionar: "Twitch", "estilo Twitch", "app de streaming ao vivo", "live com chat", "player
  + chat", "gaming stream", "design Twitch". Consulta ../_shared/design-resources.md.
---

# Twitch

Você atua como designer que domina a linguagem do Twitch. É **dark, roxo e ao vivo**: o player manda, o chat pulsa ao lado, e o roxo é a energia da marca. Comunidade e tempo-real acima de tudo.

## Princípios

1. **Dark-first** — o player de vídeo domina; fundo escuro para o vídeo e o roxo brilharem.
2. **Roxo é a marca** — `#9146FF` em ação, follow, live badge e branding. Acento vibrante, não fundo.
3. **Layout de live** — player grande + chat em coluna à direita + info do canal abaixo. O chat é cidadão de primeira classe.
4. **Comunidade e tempo-real** — badges, emotes, contadores de viewers ao vivo, "LIVE" pulsante. A UI comunica presença.

## Design tokens

```css
:root {                              /* Twitch dark */
  --twh-purple: #9146ff;
  --twh-purple-hover: #772ce8;
  --twh-bg: #0e0e10;                 /* base */
  --twh-bg-alt: #18181b;             /* cards/chat */
  --twh-bg-input: #1f1f23;
  --twh-text: #efeff1;
  --twh-text-muted: #adadb8;
  --twh-border: #2a2a2d;
  --twh-live: #eb0400;              /* badge LIVE */
  --twh-radius: 4px;
}
:root[data-theme="light"] {
  --twh-bg: #ffffff; --twh-bg-alt: #f7f7f8; --twh-bg-input: #efeff1;
  --twh-text: #0e0e10; --twh-text-muted: #53535f; --twh-border: #e5e5e5;
}
```

## Tipografia (Roobert / fallback)

```css
/* Roobert é proprietária. Fallback próximo: */
font-family: 'Roobert', 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
--twh-title: 700 18px/1.3;           /* título da live */
--twh-channel: 600 14px/1.3;
--twh-body: 400 13px/1.5;            /* mensagem de chat: densa */
--twh-meta: 600 12px/1.3;
```

## Componentes-chave

```css
.twh-btn-primary {
  background: var(--twh-purple); color: #fff; border: none; border-radius: var(--twh-radius);
  padding: 0 10px; height: 30px; font: 600 13px/1 'Roobert'; transition: background .1s;
}
.twh-btn-primary:hover { background: var(--twh-purple-hover); }

.twh-live-badge {                    /* selo LIVE vermelho */
  background: var(--twh-live); color: #fff; border-radius: var(--twh-radius);
  padding: 0 4px; font: 600 10px/16px 'Roobert'; text-transform: uppercase; letter-spacing: .5px;
}
.twh-viewers { display: inline-flex; align-items: center; gap: 4px; color: var(--twh-live);
  font-size: 13px; font-weight: 600; }   /* ● 12.4K */

.twh-chat { background: var(--twh-bg-alt); border-left: 1px solid var(--twh-border); width: 340px; }
.twh-chat-msg { padding: 5px 20px; font-size: 13px; line-height: 1.5; }
.twh-chat-msg:hover { background: rgba(255,255,255,.05); }
.twh-username { font-weight: 700; }   /* cor do nick = cor escolhida pelo user */
.twh-badge { width: 18px; height: 18px; border-radius: 2px; vertical-align: middle; }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [twitch.tv](https://www.twitch.tv/) | Referência viva: player + chat, badges, LIVE, densidade do chat. |
| [Twitch Brand](https://brand.twitch.tv/) | Uso do roxo, logo (Glitch), tipografia, tom. |
| [Twitch — UX/Design (blog)](https://blog.twitch.tv/) | Padrões de produto e comunidade. |
| ../_shared/design-resources.md | Dark mode, microinterações (emotes), densidade de chat. |

## Do / Don't

| Do | Don't |
|---|---|
| Dark-first, player em foco | Fundo claro competindo com vídeo |
| Roxo `#9146FF` em ação/marca | Roxo de fundo inteiro |
| Chat como cidadão de 1ª classe | Chat espremido/secundário |
| LIVE + viewers em tempo real | Esconder estado ao vivo |

## Checklist

- [ ] Dark-first (bg `#0e0e10`, cards `#18181b`)
- [ ] Roxo `#9146FF` em follow/ação/marca
- [ ] Layout player + chat lateral (~340px)
- [ ] Badge LIVE + contador de viewers
- [ ] Nicks coloridos + badges no chat
- [ ] Chat denso (fonte ~13px) + light mode alternativo
