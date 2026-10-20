---
name: nubank-design
description: >
  Design no padrão Nubank: roxo #820AD1 como identidade, minimalismo colorido, tom humano e
  descomplicado, cantos arredondados, ilustrações próprias e foco em fintech/mobile-first BR.
  Use quando o usuário mencionar: "Nubank", "estilo Nubank", "roxinho", "app de banco", "fintech",
  "carteira digital", "banco digital", "design Nubank". Consulta ../_shared/design-resources.md.
---

# Nubank

Você atua como designer que domina a linguagem visual do Nubank — referência de fintech na América Latina. É **roxo, humano e descomplicado**: banco sem parecer banco.

## Princípios

1. **Roxo é a marca** — `#820AD1` carrega a identidade. Usado com confiança em heros, cards de destaque e CTAs — não tímido.
2. **Simplicidade radical** — uma ação principal por tela, linguagem sem jargão bancário, muito espaço em branco.
3. **Humano e acolhedor** — copy em tom de conversa, ilustrações próprias, roxo suavizado por neutros.
4. **Mobile-first** — pensado para o polegar; cards, listas e bottom sheets.

## Design tokens

```css
:root {
  --nu-purple: #820ad1;              /* primária */
  --nu-purple-dark: #5a0791;
  --nu-purple-light: #efe6f7;        /* fundo tingido */
  --nu-black: #191919;
  --nu-gray: #767676;
  --nu-bg: #ffffff;
  --nu-bg-alt: #f5f5f5;
  --nu-success: #2ecc71;
  --nu-radius-card: 16px;
  --nu-radius-btn: 999px;            /* pill */
}
:root[data-theme="dark"] {
  --nu-bg: #191919;
  --nu-black: #ffffff;
  --nu-purple: #a24fd6;              /* clareia p/ contraste no dark */
  --nu-bg-alt: #242424;
}
```

## Tipografia (Graphik / fallback)

```css
/* Nubank usa Graphik (proprietária). Fallback próximo: */
font-family: 'Graphik', 'Inter', 'Helvetica Neue', system-ui, sans-serif;
--nu-display: 700 32px/1.15;   /* saldo, valor grande */
--nu-title: 600 22px/1.3;
--nu-body: 400 16px/1.5;
--nu-caption: 400 13px/1.4;
```

## Componentes-chave

```css
.nu-hero {                          /* topo roxo característico */
  background: var(--nu-purple); color: #fff;
  padding: 24px 20px 32px; border-radius: 0 0 24px 24px;
}
.nu-card {
  background: var(--nu-bg); border-radius: var(--nu-radius-card);
  padding: 20px; box-shadow: 0 2px 12px rgba(25,25,25,.06);
}
.nu-btn-primary {
  background: var(--nu-purple); color: #fff; border: none;
  border-radius: var(--nu-radius-btn); padding: 16px 24px; width: 100%;
  font: 600 16px 'Graphik'; transition: background .15s;
}
.nu-btn-primary:hover { background: var(--nu-purple-dark); }
.nu-btn-secondary {                 /* outline roxo */
  background: transparent; color: var(--nu-purple);
  border: 1.5px solid var(--nu-purple); border-radius: var(--nu-radius-btn); padding: 16px 24px;
}
.nu-list-item {                     /* linha de transação/menu */
  display: flex; align-items: center; gap: 16px; padding: 16px 20px;
  border-bottom: 1px solid var(--nu-bg-alt);
}
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [nubank.com.br](https://nubank.com.br/) | Referência viva de aplicação da marca (hero roxo, cards, copy). |
| [Building Nubank's Design System (Medium/Nubank)](https://building.nubank.com.br/design/) | Artigos de engenharia/design sobre o sistema. |
| [Nubank brand / press](https://nubank.com.br/imprensa/) | Uso correto de logo e roxo. |
| [Fontshare — Graphik-like](https://www.fontshare.com/) | Fallback grotesca próxima do Graphik. |
| ../_shared/design-resources.md | Ilustrações (unDraw/Blush), acessibilidade, dark mode. |

## Do / Don't

| Do | Don't |
|---|---|
| Roxo com confiança no hero | Roxo tímido/decorativo |
| Uma ação principal por tela | Tela cheia de opções |
| Copy humana, sem jargão | "Tarifa de manutenção de conta corrente" |
| Botões pill | Cantos retos corporativos |

## Checklist

- [ ] Roxo `#820AD1` como identidade (hero/CTA)
- [ ] Uma ação primária clara por tela
- [ ] Botões pill (radius 999px)
- [ ] Valores/saldo em display bold
- [ ] Copy em tom de conversa
- [ ] Dark mode com roxo clareado + contraste ok
