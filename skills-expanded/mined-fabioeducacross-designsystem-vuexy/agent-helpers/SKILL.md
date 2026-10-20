# 🎓 Skill: Doc Template System - Guia de Replicação

## 📋 Propósito

Template profissional para criar páginas de documentação consistentes no Storybook, baseado no estilo "Getting Started". Use este guia para replicar o padrão em novos componentes.

---

## 🏗️ Estrutura Base (Copy-Paste Ready)

### 1. Header do Arquivo

```javascript
/**
 * ComponentName Stories
 * 
 * Descrição breve do componente (1-2 linhas)
 * 
 * @component ComponentName
 * @category [Front-office / Category]
 * @subcategory [Modals | Forms | Lists | Media | etc]
 */

import { 
  createDocPage, 
  createExampleCard, 
  createPropsTable, 
  createUsageSection 
} from '../_helpers/docTemplate.js';

export default {
  title: 'Front-office/Category/ComponentName',
  parameters: {
    layout: 'fullscreen',
  },
  tags: ['autodocs'],
};
```

---

## 📖 Story: Documentation (PADRÃO COMPLETO)

### Template Copy-Paste

```javascript
/**
 * Documentation Page
 * Página completa de documentação com preview, código e guidelines
 */
export const Documentation = {
  parameters: {
    layout: 'fullscreen',
    docs: {
      page: () => null // Remove wrappers do Storybook
    }
  },
  render: () => createDocPage({
    // 🎯 Hero Section
    title: 'ComponentName',
    subtitle: 'Descrição clara do componente (1-2 frases sobre o que faz)',
    badge: 'Front-office / Category',
    badgeIcon: 'icon_name', // Material Symbols
    
    // 📊 Estatísticas (opcional)
    showStats: true,
    stats: {
      'Fluxos': '2',
      'Estados': '5',
      'Perfis': '4+'
    },
    
    // 🎨 Cores (opcional - use cores do componente)
    colors: {
      primary: '#667eea',   // Cor principal do componente
      secondary: '#764ba2'  // Cor secundária
    },
    
    // 📝 Conteúdo Principal
    content: `
      ${createUsageSection({
        title: 'Como Usar',
        icon: 'integration_instructions',
        steps: [
          'Passo 1: Contexto/trigger de abertura',
          'Passo 2: Estados/fluxos disponíveis',
          'Passo 3: Ações do usuário',
          'Passo 4: Feedback/resultado esperado'
        ]
      })}

      ${createExampleCard({
        title: 'Fluxo Principal',
        description: 'Descrição do caso de uso mais comum',
        showTitle: false,        // Remove título duplicado
        wrapPreview: false,       // ⭐ CENTRALIZA - use para modais/cards grandes
        preview: \`
          <style>
            /* CSS compartilhado - copie do componente Vue */
            .modal-container {
              display: flex;
              justify-content: center;
              align-items: center;
              padding: 2rem;
              background: rgba(0,0,0,0.05);
            }
          </style>
          
          <!-- HTML do componente -->
          <div class="modal-container">
            <!-- Conteúdo aqui -->
          </div>
        \`,
        codes: {
          html: \`<!-- Código HTML limpo -->\`,
          react: \`// Código React
import ComponentName from '@/components/ComponentName'

function Example() {
  return <ComponentName prop="value" />
}\`,
          vue: \`<!-- Código Vue 2 -->
<template>
  <ComponentName :prop="value" />
</template>

<script>
import ComponentName from '@/components/ComponentName'

export default {
  components: { ComponentName },
  data() {
    return { value: 'example' }
  }
}
</script>\`,
          angular: \`// Código Angular
import { Component } from '@angular/core'

@Component({
  selector: 'app-example',
  template: '<component-name [prop]="value"></component-name>'
})
export class ExampleComponent {
  value = 'example'
}\`
        }
      })}

      ${createExampleCard({
        title: 'Variação Alternativa',
        description: 'Outro caso de uso importante',
        showTitle: false,
        wrapPreview: false,
        preview: \`<!-- HTML alternativo -->\`,
        codes: { /* ... */ }
      })}
    `,
    
    // 🎁 Features (3-6 itens)
    features: [
      {
        icon: 'swap_horiz',
        title: 'Feature Principal',
        description: 'Descrição da funcionalidade chave'
      },
      {
        icon: 'shield',
        title: 'Validação',
        description: 'Como o componente valida dados'
      },
      {
        icon: 'accessibility_new',
        title: 'Acessibilidade',
        description: 'Suporte a leitores de tela e teclado'
      }
    ],
    
    // 🔗 Componentes Relacionados (4-6 itens)
    relatedComponents: [
      {
        title: 'ComponenteRelacionado',
        icon: 'icon_name',
        description: 'Como se relaciona com este componente',
        path: '?path=/story/front-office-category-component--docs'
      }
    ]
  })
};
```

---

## 🎨 Opções de Configuração

### `wrapPreview` - Quando Usar

```javascript
// ✅ wrapPreview: false - Para modais, cards grandes, componentes centralizados
wrapPreview: false,  // Remove padding cinza, componente controla layout

// ✅ wrapPreview: true (default) - Para componentes inline, botões, forms
wrapPreview: true,   // Adiciona fundo cinza e padding
```

### `showTitle` - Quando Usar

```javascript
// ✅ showTitle: false - Remove título duplicado do createExampleCard
showTitle: false,  // Use quando já tem título no createDocPage

// ✅ showTitle: true (default) - Mostra título da seção
showTitle: true,   // Use para seções múltiplas
```

### `codes` - Formatos Disponíveis

```javascript
codes: {
  html: `<!-- HTML básico -->`,
  react: `// React Component`,
  vue: `<!-- Vue 2 Component -->`,
  angular: `// Angular Component`
}
```

---

## 📊 Stories Complementares (PADRÃO)

### Story: Default

```javascript
/**
 * Story: Default
 * Estado padrão do componente com dados básicos
 */
export const Default = {
  parameters: {
    docs: {
      description: {
        story: `Estado padrão do componente com configuração inicial.`
      }
    }
  },
  render: () => `
    <style>${componentStyles}</style>
    <div class="container py-4">
      <!-- HTML básico -->
    </div>
  `
};
```

### Story: WithInteraction (se aplicável)

```javascript
/**
 * Story: Interactive
 * Versão interativa com JavaScript funcional
 */
export const Interactive = {
  parameters: {
    docs: {
      description: {
        story: `Versão interativa com handlers de eventos e validação.`
      }
    }
  },
  loaders: [
    async () => {
      // Carregar dependências se necessário
      if (!window.bootstrap) {
        return new Promise((resolve) => {
          const script = document.createElement('script');
          script.src = '/vuexy/js/bootstrap.js';
          script.onload = () => resolve({ bootstrapLoaded: true });
          document.head.appendChild(script);
        });
      }
      return {};
    }
  ],
  render: () => {
    setTimeout(() => {
      if (window.bootstrap?.Modal) {
        // Inicializar modals
        document.querySelectorAll('[data-bs-toggle="modal"]').forEach(el => {
          new bootstrap.Modal(el);
        });
      }
    }, 100);
    
    return `
      <style>${componentStyles}</style>
      <!-- HTML interativo -->
    `;
  }
};
```

---

## 🎯 Ícones Material Symbols

### Ícones Comuns por Categoria

```javascript
// Modais
badgeIcon: 'door_open'           // Acesso/entrada
badgeIcon: 'delete'              // Exclusão
badgeIcon: 'content_copy'        // Copiar/duplicar
badgeIcon: 'share'               // Compartilhar

// Formulários
badgeIcon: 'edit'                // Edição
badgeIcon: 'add_circle'          // Adicionar
badgeIcon: 'fact_check'          // Validação
badgeIcon: 'toggle_on'           // Seleção

// Mídia
badgeIcon: 'image'               // Imagens
badgeIcon: 'play_circle'         // Vídeo/áudio
badgeIcon: 'photo_library'       // Galeria
badgeIcon: 'file_present'        // Arquivo

// Listas/Tabelas
badgeIcon: 'view_list'           // Lista
badgeIcon: 'table_chart'         // Tabela
badgeIcon: 'grid_view'           // Grid
badgeIcon: 'reorder'             // Ordenação

// Feedback
badgeIcon: 'notifications'       // Alertas
badgeIcon: 'check_circle'        // Sucesso
badgeIcon: 'error'               // Erro
badgeIcon: 'info'                // Informação

// Navegação
badgeIcon: 'menu'                // Menu
badgeIcon: 'arrow_back'          // Voltar
badgeIcon: 'home'                // Início
badgeIcon: 'search'              // Busca
```

**Ver todos os ícones**: https://fonts.google.com/icons

---

## ✅ Checklist de Replicação

### Antes de Começar

- [ ] Ler componente Vue original em `educacross-frontoffice/src/components/`
- [ ] Identificar props, eventos e estados
- [ ] Listar casos de uso principais (2-3 exemplos)
- [ ] Escolher ícone Material Symbols adequado

### Durante a Criação

- [ ] Copiar template base deste documento
- [ ] Substituir `ComponentName` pelo nome real
- [ ] Preencher `title`, `subtitle`, `badge`
- [ ] Adicionar CSS do componente original
- [ ] Criar 2-3 `createExampleCard` com casos de uso reais
- [ ] Configurar `wrapPreview: false` para modais/cards grandes
- [ ] Adicionar code tabs (html, react, vue, angular)
- [ ] Definir 3-6 features relevantes
- [ ] Listar 4-6 componentes relacionados

### Validação Final

- [ ] Preview renderiza corretamente (sem overlap de código)
- [ ] Code tabs funcionam e mostram código limpo
- [ ] Features descrevem funcionalidades reais
- [ ] Links de componentes relacionados funcionam
- [ ] CSS não vaza para fora do componente
- [ ] Responsivo (mobile, tablet, desktop)
- [ ] Sem erros no console do navegador

---

## 🎓 Exemplos de Referência

### Componentes Bem Documentados

1. **[AcceptOrRejectAccess.stories.js](../src/stories/educacross-components-v2/AcceptOrRejectAccess.stories.js)**
   - Modal de decisão com 2 fluxos (aceitar/recusar)
   - Usa `wrapPreview: false` corretamente
   - Code tabs completos
   - Features bem definidas

2. **[DocTemplateExample.stories.js](../src/stories/_helpers/DocTemplateExample.stories.js)**
   - Exemplo oficial do template system
   - Mostra todas as opções disponíveis
   - 3 variações (completo, minimal, custom colors)

3. **[CopyLink.stories.js](../src/stories/educacross-components-v2/CopyLink.stories.js)**
   - Modal de compartilhamento
   - Múltiplos exemplos (toast, QR code, guide link)
   - Interactive story com Bootstrap JS

### Padrões de CSS

```javascript
// CSS compartilhado - extrair do componente Vue original
const componentStyles = `
  /* Estilos específicos do componente */
  .component-class {
    /* ... */
  }
  
  /* Media queries se necessário */
  @media (max-width: 768px) {
    .component-class {
      /* ... */
    }
  }
`;
```

---

## 🚨 Erros Comuns e Soluções

### ❌ Problema: Preview e código na mesma linha

```javascript
// ERRADO
wrapPreview: true,  // Cria padding cinza que compete com modal
```

```javascript
// CORRETO
wrapPreview: false,  // Modal controla seu próprio layout
```

### ❌ Problema: Título duplicado

```javascript
// ERRADO
createDocPage({ title: 'Modal' })  // Título principal
createExampleCard({ 
  title: 'Modal Example',  // Título duplicado
  showTitle: true  // Default, mostra título
})
```

```javascript
// CORRETO
createDocPage({ title: 'Modal' })
createExampleCard({ 
  title: 'Modal Example',
  showTitle: false  // Remove título da card
})
```

### ❌ Problema: CSS vazando

```javascript
// ERRADO - CSS global afeta outros componentes
<style>
  .modal { /* afeta TODOS os modais */ }
</style>
```

```javascript
// CORRETO - CSS escoped
<style>
  .my-component-modal { /* apenas este componente */ }
</style>
```

---

## 📚 Recursos Adicionais

- **[DOC_TEMPLATE_README.md](../src/stories/_helpers/DOC_TEMPLATE_README.md)** - API completa do template system
- **[DOC_TEMPLATE_GUIDE.md](./DOC_TEMPLATE_GUIDE.md)** - Guia detalhado com exemplos
- **[LOADER_PATTERNS.md](./LOADER_PATTERNS.md)** - Padrões para loaders JavaScript
- **[PIPELINE_RECONSTRUCAO.md](./PIPELINE_RECONSTRUCAO.md)** - Pipeline completo de reconstrução

---

## 🎯 Próximo Passo

**Aplicar este template em componente real:**

1. Escolher componente da lista em [tarefas.md](./tarefas.md)
2. Copiar estrutura desta skill
3. Preencher com dados reais do componente
4. Validar visualmente no Storybook
5. Marcar como completo na lista

**Comando para rodar Storybook:**
```bash
npm run storybook
```

**URL para testar:**
```
http://localhost:6006/?path=/story/front-office-category-componentname--documentation
```

---

**Última atualização**: 06/02/2026
**Versão**: 1.0
**Criado por**: AI Agent (baseado em DocTemplateExample.stories.js)
