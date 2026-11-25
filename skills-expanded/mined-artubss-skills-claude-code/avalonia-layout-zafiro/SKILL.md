---
name: avalonia-layout-zafiro
description: Diretrizes para layout moderno de UI em Avalonia usando Zafiro.Avalonia, enfatizando estilos compartilhados, componentes genéricos e evitando redundância em XAML.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Layout Avalonia com Zafiro.Avalonia

> Domine layouts de UI em Avalonia modernos, limpos e fáceis de manter.
> **Foco em contêineres semânticos, estilos compartilhados e XAML mínimo.**

## 🎯 Regra de Leitura Seletiva

**Leia APENAS arquivos relevantes para o desafio de layout!**

---

## 📑 Mapa de Conteúdo

| Arquivo | Descrição | Quando Ler |
|---------|-----------|-----------|
| `themes.md` | Organização de temas e estilos compartilhados | Configurando ou refinando temas do app |
| `containers.md` | Contêineres semânticos (`HeaderedContainer`, `EdgePanel`, `Card`) | Estruturando views e layouts |
| `icons.md` | Uso de ícones com `IconExtension` e `IconOptions` | Adicionando e customizando ícones |
| `behaviors.md` | `Xaml.Interaction.Behaviors` e evitando Converters | Implementando interações complexas |
| `components.md` | Componentes genéricos e evitando aninhamento | Criando elementos de UI reutilizáveis |

---

## 🔗 Projeto Relacionado (Implementação Exemplar)

Para um exemplo real, consulte o projeto **Angor**:
`/mnt/fast/Repos/angor/src/Angor/Avalonia/Angor.Avalonia.sln`

---

## ✅ Checklist para Layouts Limpos

- [ ] **Usou contêineres semânticos?** (ex: `HeaderedContainer` em vez de `Border` com header manual)
- [ ] **Evitou propriedades redundantes?** Use estilos compartilhados em arquivos `axaml`.
- [ ] **Minimizou aninhamento?** Simplifique layouts usando `EdgePanel` ou componentes genéricos.
- [ ] **Ícones via extension?** Use `{Icon fa-name}` e `IconOptions` para estilo.
- [ ] **Behaviors em vez de code-behind?** Use `Interaction.Behaviors` para lógica de UI.
- [ ] **Evitou Converters?** Prefira propriedades do ViewModel ou Behaviors quando necessário.

---

## ❌ Anti-Padrões

**NÃO FAÇA:**
- Use cores ou tamanhos hardcoded (literais) em views.
- Crie aninhamento profundo de `Grid` e `StackPanel`.
- Repita propriedades visuais em múltiplos elementos (use Styles).
- Use `IValueConverter` para lógica simples que pertence ao ViewModel.

**FAÇA:**
- Use `DynamicResource` para cores e brushes.
- Extraia layouts repetidos em componentes genéricos.
- Aproveite painéis específicos de `Zafiro.Avalonia` como `EdgePanel` para padrões comuns de UI.