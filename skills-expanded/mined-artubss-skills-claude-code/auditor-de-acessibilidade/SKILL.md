---
name: Auditor de Acessibilidade
description: Especialista em acessibilidade web para conformidade WCAG, implementação ARIA e design inclusivo. Use ao auditar sites para problemas de acessibilidade, implementar padrões WCAG 2.1 AA/AAA, testar com leitores de tela ou garantir conformidade ADA. Especialista em HTML semântico, navegação por teclado e compatibilidade com tecnologia assistiva.
---

# Auditor de Acessibilidade

Orientação abrangente para criar experiências web acessíveis que estejam em conformidade com padrões WCAG e atendam efetivamente usuários de todas as habilidades.

## Quando Usar Esta Habilidade

Use esta habilidade quando:
- Auditar sites para conformidade de acessibilidade
- Implementar padrões WCAG 2.1 Nível AA ou AAA
- Corrigir violações e erros de acessibilidade
- Testar com leitores de tela (NVDA, JAWS, VoiceOver)
- Garantir que a navegação por teclado funcione corretamente
- Implementar atributos ARIA e marcos de página
- Preparar auditorias de conformidade ADA ou Section 508
- Projetar experiências de usuário inclusivas

## Princípios WCAG 2.1 (POUR)

### 1. Perceptível
Os usuários devem ser capazes de perceber as informações sendo apresentadas.

### 2. Operável
Os usuários devem ser capazes de operar a interface.

### 3. Compreensível
Os usuários devem ser capazes de compreender as informações e a interface.

### 4. Robusto
O conteúdo deve ser robusto o suficiente para funcionar com tecnologias atuais e futuras.

## Problemas Comuns de Acessibilidade e Soluções

### 1. Falta de Texto Alternativo para Imagens

**❌ Problema:**
```html
<img src="/products/shoes.jpg">
```

**✅ Solução:**
```html
<!-- Imagem informativa -->
<img src="/products/shoes.jpg" alt="Tênis de corrida Nike Air Max vermelho com swoosh branco">

<!-- Imagem decorativa -->
<img src="/decorative-pattern.svg" alt="" role="presentation">

<!-- Logo que funciona como link -->
<a href="/">
  <img src="/logo.png" alt="Nome da Empresa - Início">
</a>
```

**Regras:**
- Imagens informativas: Descreva o conteúdo/função
- Imagens decorativas: Use alt vazio (alt="")
- Imagens funcionais: Descreva a ação
- Imagens complexas: Forneça descrição detalhada próxima

### 2. Contraste de Cor Baixo

**❌ Problema:**
```css
/* Taxa de contraste 2.5:1 - Falha em WCAG */
.text {
  color: #767676;
  background: #ffffff;
}
```

**✅ Solução:**
```css
/* Taxa de contraste 4.5:1+ - Passa AA */
.text {
  color: #595959;
  background: #ffffff;
}

/* Taxa de contraste 7:1+ - Passa AAA */
.text-high-contrast {
  color: #333333;
  background: #ffffff;
}
```

**Requisitos:**
- Texto normal (< 18px): 4.5:1 mínimo (AA), 7:1 aprimorado (AAA)
- Texto grande (≥ 18px ou ≥ 14px em negrito): 3:1 mínimo (AA), 4.5:1 aprimorado (AAA)
- Componentes UI e gráficos: 3:1 mínimo

### 3. HTML Não Semântico

**❌ Problema:**
```html
<div class="button" onclick="submitForm()">Enviar</div>
<div class="heading">Título da Página</div>
<div class="nav-menu">...</div>
```

**✅ Solução:**
```html
<button type="submit" onclick="submitForm()">Enviar</button>
<h1>Título da Página</h1>
<nav aria-label="Navegação principal">...</nav>
```

**Elementos Semânticos:**
- `<button>` para botões
- `<a>` para links
- `<h1>` - `<h6>` para títulos (hierárquico)
- `<nav>`, `<main>`, `<aside>`, `<article>`, `<section>` para marcos
- `<ul>`, `<ol>`, `<li>` para listas
- `<table>`, `<th>`, `<td>` para dados tabulares

### 4. Rótulos de Formulário Ausentes

**❌ Problema:**
```html
<input type="email" placeholder="Digite seu email">
```

**✅ Solução:**
```html
<!-- Rótulo explícito -->
<label for="email">Endereço de Email</label>
<input type="email" id="email" name="email">

<!-- Rótulo implícito -->
<label>
  Endereço de Email
  <input type="email" name="email">
</label>

<!-- Rótulo oculto (para layouts compactos) -->
<label for="search" class="sr-only">Buscar</label>
<input type="text" id="search" placeholder="Buscar...">
```

**Boas Práticas:**
- Cada campo de formulário deve ter um rótulo associado
- Rótulos devem ser visíveis (não dependa de placeholder)
- Use aria-label apenas quando o rótulo visual não for possível
- Agrupe campos relacionados com `<fieldset>` e `<legend>`

### 5. Problemas de Navegação por Teclado

**❌ Problema:**
```html
<div onclick="handleClick()">Clique em mim</div>
<a href="javascript:void(0)" onclick="doSomething()">Ação</a>
```

**✅ Solução:**
```html
<!-- Use botão apropriado -->
<button onclick="handleClick()">Clique em mim</button>

<!-- Se div for necessária, torne-a acessível -->
<div
  role="button"
  tabindex="0"
  onclick="handleClick()"
  onkeydown="handleKeyPress(event)"
>
  Clique em mim
</div>

<script>
function handleKeyPress(event) {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    handleClick();
  }
}
</script>
```

**Requisitos de Teclado:**
- Todos os elementos interativos devem ser acessíveis por teclado
- Indicadores de foco visíveis (outline ou estilo personalizado)
- Ordem de tabulação lógica (corresponde ao fluxo visual)
- Links para pular conteúdo repetitivo
- Sem armadilhas de teclado (usuários podem navegar para fora)

### 6. Marcos ARIA Ausentes

**❌ Problema:**
```html
<div class="header">...</div>
<div class="main-content">...</div>
<div class="sidebar">...</div>
<div class="footer">...</div>
```

**✅ Solução:**
```html
<header role="banner">
  <nav aria-label="Navegação principal">...</nav>
</header>

<main role="main">
  <h1>Título da Página</h1>
  <article>...</article>
</main>

<aside role="complementary" aria-label="Artigos relacionados">
  ...
</aside>

<footer role="contentinfo">
  ...
</footer>
```

**Marcos Comuns:**
- `banner` - Cabeçalho do site
- `navigation` - Menus de navegação
- `main` - Conteúdo principal (um por página)
- `complementary` - Conteúdo suplementar
- `contentinfo` - Rodapé do site
- `search` - Funcionalidade de busca
- `form` - Regiões de formulário

### 7. Modais/Diálogos Inacessíveis

**❌ Problema:**
```html
<div class="modal">
  <div class="content">
    Conteúdo do modal
    <button onclick="closeModal()">Fechar</button>
  </div>
</div>
```

**✅ Solução:**
```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-desc"
>
  <h2 id="modal-title">Confirmar Ação</h2>
  <p id="modal-desc">Tem certeza que deseja excluir este item?</p>

  <button onclick="confirmAction()">Confirmar</button>
  <button onclick="closeModal()">Cancelar</button>
</div>

<script>
// Gerenciamento de foco
function openModal() {
  const modal = document.querySelector('[role="dialog"]');
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );

  // Armazene o foco anterior
  previousFocus = document.activeElement;

  // Coloque o foco no primeiro elemento
  focusableElements[0].focus();

  // Prenda o foco
  modal.addEventListener('keydown', trapFocus);
}

function closeModal() {
  // Retorne o foco
  if (previousFocus) previousFocus.focus();
}

function trapFocus(event) {
  if (event.key !== 'Tab') return;

  const focusableElements = Array.from(
    modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')
  );

  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  if (event.shiftKey && document.activeElement === firstElement) {
    lastElement.focus();
    event.preventDefault();
  } else if (!event.shiftKey && document.activeElement === lastElement) {
    firstElement.focus();
    event.preventDefault();
  }
}
</script>
```

**Requisitos de Modal:**
- `role="dialog"` ou `role="alertdialog"`
- `aria-modal="true"` para indicar comportamento modal
- `aria-labelledby` apontando para o título
- `aria-describedby` para descrição (opcional)
- Gerenciamento de foco (prender e restaurar)
- Fechar com tecla Escape
- Evitar rolagem de fundo

### 8. Links para Pular Ausentes

**✅ Solução:**
```html
<a href="#main-content" class="skip-link">
  Pular para conteúdo principal
</a>

<header>
  <nav>...</nav>
</header>

<main id="main-content" tabindex="-1">
  <!-- Conteúdo da página -->
</main>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
</style>
```

## Boas Práticas ARIA

### Referência de Atributos ARIA

**Estados:**
- `aria-checked` - Estado de checkbox/radio
- `aria-disabled` - Estado desabilitado
- `aria-expanded` - Estado expandido/recolhido
- `aria-hidden` - Oculto da tecnologia assistiva
- `aria-pressed` - Estado de botão toggle
- `aria-selected` - Estado selecionado

**Propriedades:**
- `aria-label` - Nome acessível
- `aria-labelledby` - Referência de ID para rótulo
- `aria-describedby` - Referência de ID para descrição
- `aria-live` - Atualizações de região dinâmica
- `aria-required` - Campo obrigatório
- `aria-invalid` - Estado de validação

### Regiões Dinâmicas

```html
<!-- Polite: Aguarde pausa na fala -->
<div aria-live="polite" aria-atomic="true">
  Item adicionado ao carrinho
</div>

<!-- Assertive: Interrompa imediatamente -->
<div aria-live="assertive" role="alert">
  Erro: Pagamento falhou
</div>

<!-- Mensagem de status -->
<div role="status" aria-live="polite">
  Salvando alterações...
</div>
```

### Componentes Personalizados

**Acordeão:**
```html
<div class="accordion">
  <button
    aria-expanded="false"
    aria-controls="panel-1"
    id="accordion-1"
  >
    Seção 1
  </button>
  <div id="panel-1" role="region" aria-labelledby="accordion-1" hidden>
    Conteúdo do painel
  </div>
</div>
```

**Abas:**
```html
<div role="tablist" aria-label="Seções de conteúdo">
  <button
    role="tab"
    aria-selected="true"
    aria-controls="panel-1"
    id="tab-1"
  >
    Aba 1
  </button>
  <button
    role="tab"
    aria-selected="false"
    aria-controls="panel-2"
    id="tab-2"
    tabindex="-1"
  >
    Aba 2
  </button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  Conteúdo do painel 1
</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Conteúdo do painel 2
</div>
```

## Checklist de Testes

### Testes Automatizados
- [ ] Execute axe DevTools ou extensão de navegador WAVE
- [ ] Verifique validação de HTML (Validador W3C)
- [ ] Teste taxas de contraste de cor
- [ ] Verifique hierarquia de títulos
- [ ] Procure por texto alternativo ausente

### Testes Manuais
- [ ] Navegue por todo o site usando apenas teclado (Tab, Enter, Escape, teclas de seta)
- [ ] Teste com leitor de tela (NVDA, JAWS ou VoiceOver)
- [ ] Verifique se os indicadores de foco são visíveis
- [ ] Verifique se as mensagens de validação de formulário são anunciadas
- [ ] Teste aprisionamento de foco em modal
- [ ] Verifique se os links para pular funcionam
- [ ] Teste com zoom do navegador em 200%
- [ ] Verifique o refluxo de página em diferentes tamanhos de viewport
- [ ] Desabilite JavaScript e verifique funcionalidade essencial
- [ ] Teste com modo de Alto Contraste do Windows

### Testes com Leitor de Tela

**VoiceOver (Mac):**
- Ativar: Cmd + F5
- Navegar: Control + Option + teclas de seta
- Ler tudo: Control + Option + A

**NVDA (Windows):**
- Navegar: Teclas de seta (modo navegação) ou Tab (modo foco)
- Ler tudo: NVDA + seta para baixo
- Lista de elementos: NVDA + F7

**Cenários de Teste:**
- Os usuários conseguem entender a estrutura da página?
- Os títulos são descritivos e hierárquicos?
- Os rótulos de formulário são claros e associados?
- As mensagens de erro são anunciadas?
- Os usuários conseguem completar tarefas essenciais sem visão?

## Declaração de Acessibilidade

Inclua no website:

```markdown
# Declaração de Acessibilidade

Estamos comprometidos em garantir a acessibilidade digital para pessoas com deficiência. Melhoramos continuamente a experiência do usuário para todos e aplicamos padrões de acessibilidade relevantes.

## Status de Conformidade
Este website está parcialmente em conformidade com WCAG 2.1 Nível AA. "Parcialmente conforme" significa que algumas partes do conteúdo não estão totalmente em conformidade com o padrão de acessibilidade.

## Comentários
Acolhemos seus comentários sobre a acessibilidade deste site. Entre em contato:
- Email: acessibilidade@exemplo.com.br
- Telefone: +55 11 0000-0000

## Problemas Conhecidos
- [Liste quaisquer problemas de acessibilidade conhecidos e correções planejadas]

Última atualização: [Data]
```

## Recursos

**Ferramentas:**
- axe DevTools (extensão de navegador)
- WAVE (ferramenta de avaliação de acessibilidade web)
- Lighthouse (Chrome DevTools)
- Analisador de Contraste de Cor
- Leitores de tela: NVDA, JAWS, VoiceOver

**Diretrizes:**
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- Práticas de Autoria ARIA: https://www.w3.org/WAI/ARIA/apg/

Acessibilidade não é opcional—é um requisito fundamental para criar experiências web inclusivas. Priorize-a desde o início de cada projeto, não como uma reflexão tardia.