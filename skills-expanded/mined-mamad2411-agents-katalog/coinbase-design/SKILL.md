---
name: coinbase-design
description: >
  Design no padrão Coinbase: fintech/cripto que transmite confiança, azul #0052FF, tipografia
  Coinbase Sans, dados/gráficos claros, muito espaço em branco e sobriedade. Use quando o usuário
  mencionar: "Coinbase", "estilo Coinbase", "app de cripto", "exchange", "carteira de cripto",
  "fintech de investimento", "trading UI confiável", "design Coinbase". Consulta
  ../_shared/design-resources.md.
---

# Coinbase

Você atua como designer que domina a linguagem do Coinbase. Em cripto, o desafio é **confiança**: o design precisa parecer seguro, claro e institucional — o oposto do estereótipo "cripto caótico". Azul sólido, dados legíveis, sobriedade.

## Princípios

1. **Confiança acima de tudo** — clareza de saldo, preço e taxas; nada escondido. Um design "de banco sério" para reduzir a ansiedade de lidar com dinheiro/cripto.
2. **Azul institucional** — `#0052FF` como âncora de marca e ação; base neutra e limpa.
3. **Dados legíveis** — gráficos de preço, variação %, números grandes bem tipografados. Verde/vermelho para alta/baixa, com semântica consistente.
4. **Espaço em branco** — respiro generoso; uma decisão por tela (comprar, vender, enviar).

## Design tokens

```css
:root {                              /* Light */
  --cb-blue: #0052ff;                /* marca / ação */
  --cb-blue-hover: #0043cc;
  --cb-bg: #ffffff;
  --cb-bg-alt: #f5f8ff;             /* seções sutis */
  --cb-text: #0a0b0d;
  --cb-text-muted: #5b616e;
  --cb-border: #e3e8ef;
  --cb-positive: #05b169;           /* alta */
  --cb-negative: #cf202f;           /* baixa */
  --cb-radius: 12px;
}
:root[data-theme="dark"] {
  --cb-bg: #0a0b0d; --cb-bg-alt: #141519; --cb-text: #ffffff;
  --cb-text-muted: #8a919e; --cb-border: #2c2f36; --cb-blue: #578bfa;
}
```

## Tipografia (Coinbase Sans / fallback)

```css
/* Coinbase Sans é proprietária. Fallback próximo: */
font-family: 'Coinbase Sans', 'Inter', -apple-system, system-ui, sans-serif;
/* números: 'Coinbase Mono' para preços alinhados */
--cb-display: 700 40px/1.1;          /* saldo / preço grande */
--cb-title: 600 24px/1.25;
--cb-body: 400 16px/1.5;
--cb-mono: 500 16px/1.4 'Coinbase Mono', monospace;   /* valores/preços */
```

## Componentes-chave

```css
.cb-btn-primary {
  background: var(--cb-blue); color: #fff; border: none; border-radius: 100px;  /* pill */
  padding: 0 24px; height: 56px; font: 600 16px/1 'Coinbase Sans'; width: 100%;
  transition: background .12s;
}
.cb-btn-primary:hover { background: var(--cb-blue-hover); }
.cb-btn-secondary { background: var(--cb-bg-alt); color: var(--cb-blue);
  border: none; border-radius: 100px; height: 56px; padding: 0 24px; font-weight: 600; }

.cb-asset-row {                      /* linha de ativo: ícone + nome + preço + variação */
  display: flex; align-items: center; gap: 12px; padding: 16px 0;
  border-bottom: 1px solid var(--cb-border);
}
.cb-change--up { color: var(--cb-positive); font-variant-numeric: tabular-nums; }
.cb-change--down { color: var(--cb-negative); }
.cb-card { background: var(--cb-bg); border: 1px solid var(--cb-border);
  border-radius: var(--cb-radius); padding: 20px; }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [coinbase.com](https://www.coinbase.com/) | Referência viva: confiança, azul, dados, espaço em branco. |
| [Coinbase Design (Medium)](https://medium.com/the-coinbase-blog) | Estudos de caso de produto/design. |
| [Coinbase Brand](https://www.coinbase.com/press) | Uso de logo e azul. |
| [dataviz (skill)](../../../README.md) | Padrões de gráficos de preço acessíveis. |
| ../_shared/design-resources.md | Cor semântica alta/baixa, tabular-nums, dark mode. |

## Do / Don't

| Do | Don't |
|---|---|
| Sobriedade que transmite segurança | Estética "cripto neon" caótica |
| Azul `#0052FF` de marca/ação | Arco-íris de cores |
| Números com `tabular-nums` | Preços desalinhados |
| Taxas e saldo transparentes | Esconder custos |

## Checklist

- [ ] Estética sóbria/institucional (confiança)
- [ ] Azul `#0052FF` em marca/ação; botões pill 56px
- [ ] Verde/vermelho semânticos para alta/baixa
- [ ] Preços em mono/`tabular-nums` alinhados
- [ ] Taxas e saldos transparentes
- [ ] Espaço em branco generoso + dark mode
