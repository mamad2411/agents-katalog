---
name: whatsapp-design
description: >
  Design no padrão WhatsApp: mensageria simples e universal, verde de marca #25D366 / teal #075E54,
  bolhas de chat, fundo de conversa característico, tipografia de sistema e clareza acima de tudo.
  Use quando o usuário mencionar: "WhatsApp", "estilo WhatsApp", "app de mensagem", "chat", "bolhas
  de conversa", "messenger", "mensageria", "design WhatsApp". Consulta ../_shared/design-resources.md.
---

# WhatsApp

Você atua como designer que domina a linguagem do WhatsApp. É **simples, universal e confiável**: feito para todo mundo, de qualquer idade, em qualquer aparelho. Verde de marca, bolhas de chat e zero fricção.

## Princípios

1. **Simplicidade radical** — a UI some; a conversa é tudo. Sem enfeite, sem curva de aprendizado.
2. **Verde de marca** — `#25D366` (ação, enviar, online) e teal `#075E54` (header clássico). Reconhecível instantaneamente.
3. **Bolhas de chat** — enviadas à direita (verde-claro), recebidas à esquerda (branco/cinza); ticks de status (enviado/entregue/lido).
4. **Universal e acessível** — tamanhos confortáveis, alto contraste, funciona em telas pequenas e conexões ruins.

## Design tokens

```css
:root {                              /* Light */
  --wa-green: #25d366;               /* ação/enviar/online */
  --wa-teal: #075e54;               /* header clássico */
  --wa-teal-dark: #128c7e;
  --wa-bg-chat: #efeae2;            /* fundo da conversa (bege característico) */
  --wa-bubble-out: #d9fdd3;         /* bolha enviada (verde-claro) */
  --wa-bubble-in: #ffffff;          /* bolha recebida */
  --wa-text: #111b21;
  --wa-text-secondary: #667781;
  --wa-tick-blue: #53bdeb;          /* lido */
  --wa-radius-bubble: 8px;
}
:root[data-theme="dark"] {
  --wa-bg-chat: #0b141a;
  --wa-bubble-out: #005c4b;
  --wa-bubble-in: #202c33;
  --wa-text: #e9edef;
  --wa-text-secondary: #8696a0;
  --wa-teal: #202c33;
}
```

## Tipografia (system)

```css
font-family: 'Helvetica Neue', Helvetica, -apple-system, 'Segoe UI', Roboto, sans-serif;
--wa-name: 600 17px/1.3;             /* nome do contato */
--wa-message: 400 15px/1.4;          /* texto da bolha */
--wa-time: 400 11px/1.3;             /* horário/status */
--wa-preview: 400 14px/1.35;         /* prévia na lista de chats */
```

## Componentes-chave

```css
.wa-chat-bg { background: var(--wa-bg-chat); }   /* + padrão de doodle sutil opcional */

.wa-bubble {                         /* bolha base */
  max-width: 65%; padding: 6px 9px 8px; border-radius: var(--wa-radius-bubble);
  font-size: 15px; line-height: 1.4; color: var(--wa-text); position: relative;
  box-shadow: 0 1px 0.5px rgba(0,0,0,.13);
}
.wa-bubble--out { background: var(--wa-bubble-out); margin-left: auto; border-top-right-radius: 0; }
.wa-bubble--in  { background: var(--wa-bubble-in);  margin-right: auto; border-top-left-radius: 0; }
.wa-time { font-size: 11px; color: var(--wa-text-secondary); float: right; margin: 4px 0 -4px 8px; }
.wa-tick--read { color: var(--wa-tick-blue); }   /* ✓✓ azul = lido */

.wa-btn-send {                       /* botão circular verde de enviar */
  background: var(--wa-green); color: #fff; border: none; width: 48px; height: 48px;
  border-radius: 50%; display: grid; place-items: center;
}
.wa-fab { background: var(--wa-green); width: 56px; height: 56px; border-radius: 50%;
  box-shadow: 0 4px 8px rgba(0,0,0,.2); }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [whatsapp.com](https://www.whatsapp.com/) | Referência viva: bolhas, verde, fundo de chat, simplicidade. |
| [WhatsApp Brand](https://www.facebook.com/brand/whatsapp/) | Uso correto de logo e verde. |
| [Material Symbols](https://fonts.google.com/icons) | Ícones no espírito Android (WhatsApp segue Material no Android). |
| ../_shared/design-resources.md | Contraste, bolhas, dark mode, acessibilidade. |

## Do / Don't

| Do | Don't |
|---|---|
| Simplicidade extrema | Recursos escondidos/curva de aprendizado |
| Verde `#25D366` em ação/enviar | Verde de fundo inteiro |
| Bolhas out (direita) / in (esquerda) | Layout de chat não convencional |
| Ticks de status claros | Esconder entregue/lido |

## Checklist

- [ ] Fundo de conversa característico (bege `#efeae2` / dark `#0b141a`)
- [ ] Bolha enviada verde-clara à direita, recebida branca à esquerda
- [ ] Verde `#25D366` em enviar/ação/online
- [ ] Ticks de status (enviado/entregue/lido azul)
- [ ] Simplicidade: uma conversa, zero enfeite
- [ ] Dark mode + alto contraste
