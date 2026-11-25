---
name: i18n-localization
description: Padrões de internacionalização e localização. Detectando strings hardcoded, gerenciando traduções, arquivos de locale, suporte a RTL.
allowed-tools: Read, Glob, Grep
---

# i18n & Localização

> Melhores práticas de Internacionalização (i18n) e Localização (L10n).

---

## 1. Conceitos Fundamentais

| Termo | Significado |
|-------|-------------|
| **i18n** | Internacionalização - tornar o app traduzível |
| **L10n** | Localização - traduções reais |
| **Locale** | Idioma + Região (en-US, tr-TR) |
| **RTL** | Idiomas da direita para esquerda (Árabe, Hebraico) |

---

## 2. Quando Usar i18n

| Tipo de Projeto | i18n Necessário? |
|-----------------|-----------------|
| App web público | ✅ Sim |
| Produto SaaS | ✅ Sim |
| Ferramenta interna | ⚠️ Talvez |
| App de região única | ⚠️ Considere futuro |
| Projeto pessoal | ❌ Opcional |

---

## 3. Padrões de Implementação

### React (react-i18next)

```tsx
import { useTranslation } from 'react-i18next';

function Welcome() {
  const { t } = useTranslation();
  return <h1>{t('welcome.title')}</h1>;
}
```

### Next.js (next-intl)

```tsx
import { useTranslations } from 'next-intl';

export default function Page() {
  const t = useTranslations('Home');
  return <h1>{t('title')}</h1>;
}
```

### Python (gettext)

```python
from gettext import gettext as _

print(_("Welcome to our app"))
```

---

## 4. Estrutura de Arquivos

```
locales/
├── en/
│   ├── common.json
│   ├── auth.json
│   └── errors.json
├── tr/
│   ├── common.json
│   ├── auth.json
│   └── errors.json
└── ar/          # RTL
    └── ...
```

---

## 5. Melhores Práticas

### FAÇA ✅

- Use chaves de tradução, não texto bruto
- Organize traduções por feature
- Suporte pluralização
- Trate formatos de data/número por locale
- Planeje suporte a RTL desde o início
- Use formato de mensagem ICU para strings complexas

### NÃO FAÇA ❌

- Hardcode strings em componentes
- Concatene strings traduzidas
- Assuma tamanho de texto (Alemão é 30% mais longo)
- Esqueça do layout RTL
- Misture idiomas no mesmo arquivo

---

## 6. Problemas Comuns

| Problema | Solução |
|----------|---------|
| Tradução faltante | Fallback para idioma padrão |
| Strings hardcoded | Use linter/script verificador |
| Formato de data | Use Intl.DateTimeFormat |
| Formato de número | Use Intl.NumberFormat |
| Pluralização | Use formato de mensagem ICU |

---

## 7. Suporte a RTL

```css
/* Propriedades Lógicas de CSS */
.container {
  margin-inline-start: 1rem;  /* Não margin-left */
  padding-inline-end: 1rem;   /* Não padding-right */
}

[dir="rtl"] .icon {
  transform: scaleX(-1);
}
```

---

## 8. Checklist

Antes de fazer deploy:

- [ ] Todas as strings visíveis ao usuário usam chaves de tradução
- [ ] Arquivos de locale existem para todos os idiomas suportados
- [ ] Formatação de data/número usa API Intl
- [ ] Layout RTL testado (se aplicável)
- [ ] Idioma fallback configurado
- [ ] Sem strings hardcoded em componentes

---

## Script

| Script | Propósito | Comando |
|--------|-----------|---------|
| `scripts/i18n_checker.py` | Detectar strings hardcoded e traduções faltantes | `python scripts/i18n_checker.py <project_path>` |