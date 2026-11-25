---
name: accessibility
description: Auditar e melhorar a acessibilidade web seguindo as diretrizes WCAG 2.1. Use quando solicitado para "melhorar acessibilidade", "auditoria a11y", "conformidade WCAG", "suporte a leitor de tela", "navegação por teclado" ou "tornar acessível".
license: MIT
metadata:
  author: web-quality-skills
  version: "1.0"
---

# Acessibilidade (a11y)

Diretrizes abrangentes de acessibilidade baseadas em WCAG 2.1 e auditorias de acessibilidade do Lighthouse. Objetivo: tornar o conteúdo utilizável por todos, incluindo pessoas com deficiências.

## Princípios WCAG: POUR

| Princípio | Descrição |
|-----------|-----------|
| **P**erceptível | O conteúdo pode ser percebido através de diferentes sentidos |
| **O**perável | A interface pode ser operada por todos os usuários |
| **C**ompreensível | O conteúdo e a interface são compreensíveis |
| **R**obusto | O conteúdo funciona com tecnologias assistivas |

## Níveis de conformidade

| Nível | Requisito | Alvo |
|-------|-----------|------|
| **A** | Acessibilidade mínima | Deve passar |
| **AA** | Conformidade padrão | Deve passar (exigência legal em muitas jurisdições) |
| **AAA** | Acessibilidade aprimorada | Desejável |

---

## Perceptível

### Alternativas de texto (1.1)

**Imagens exigem texto alternativo:**
```html
<!-- ❌ Alt ausente -->
<img src="chart.png">

<!-- ✅ Alt descritivo -->
<img src="chart.png" alt="Gráfico de barras mostrando aumento de 40% nas vendas do Q3">

<!-- ✅ Imagem decorativa (alt vazio) -->
<img src="decorative-border.png" alt="" role="presentation">

<!-- ✅ Imagem complexa com descrição mais longa -->
<figure>
  <img src="infographic.png" alt="Infográfico de tendências de mercado 2024" 
       aria-describedby="infographic-desc">
  <figcaption id="infographic-desc">
    <!-- Descrição detalhada -->
  </figcaption>
</figure>
```

**Botões com ícones precisam de nomes acessíveis:**
```html
<!-- ❌ Sem nome acessível -->
<button><svg><!-- menu icon --></svg></button>

<!-- ✅ Usando aria-label -->
<button aria-label="Abrir menu">
  <svg aria-hidden="true"><!-- menu icon --></svg>
</button>

<!-- ✅ Usando texto visualmente oculto -->
<button>
  <svg aria-hidden="true"><!-- menu icon --></svg>
  <span class="visually-hidden">Abrir menu</span>
</button>
```

**Classe de texto visualmente oculto:**
```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### Contraste de cor (1.4.3, 1.4.6)

| Tamanho de texto | AA mínimo | AAA aprimorado |
|------------------|-----------|----------------|
| Texto normal (< 18px / < 14px negrito) | 4.5:1 | 7:1 |
| Texto grande (≥ 18px / ≥ 14px negrito) | 3:1 | 4.5:1 |
| Componentes de UI e gráficos | 3:1 | 3:1 |

```css
/* ❌ Contraste baixo (2.5:1) */
.low-contrast {
  color: #999;
  background: #fff;
}

/* ✅ Contraste suficiente (7:1) */
.high-contrast {
  color: #333;
  background: #fff;
}

/* ✅ Estados de foco precisam de contraste também */
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}
```

**Não dependa apenas de cor:**
```html
<!-- ❌ Apenas cor indica erro -->
<input class="error-border">
<style>.error-border { border-color: red; }</style>

<!-- ✅ Cor + ícone + texto -->
<div class="field-error">
  <input aria-invalid="true" aria-describedby="email-error">
  <span id="email-error" class="error-message">
    <svg aria-hidden="true"><!-- error icon --></svg>
    Por favor, insira um endereço de email válido
  </span>
</div>
```

### Alternativas para mídia (1.2)

```html
<!-- Vídeo com legendas -->
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt" srclang="pt" label="Português" default>
  <track kind="descriptions" src="descriptions.vtt" srclang="pt" label="Descrições">
</video>

<!-- Áudio com transcrição -->
<audio controls>
  <source src="podcast.mp3" type="audio/mp3">
</audio>
<details>
  <summary>Transcrição</summary>
  <p>Texto completo da transcrição...</p>
</details>
```

---

## Operável

### Acessível por teclado (2.1)

**Toda funcionalidade deve ser acessível por teclado:**
```javascript
// ❌ Apenas manipula click
element.addEventListener('click', handleAction);

// ✅ Manipula click e teclado
element.addEventListener('click', handleAction);
element.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    handleAction();
  }
});
```

**Sem armadilhas de teclado:**
```javascript
// Gerenciamento de foco do modal
function openModal(modal) {
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];
  
  // Prender foco dentro do modal
  modal.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    }
    if (e.key === 'Escape') {
      closeModal();
    }
  });
  
  firstElement.focus();
}
```

### Foco visível (2.4.7)

```css
/* ❌ Nunca remova contornos de foco */
*:focus { outline: none; }

/* ✅ Use :focus-visible para foco apenas por teclado */
:focus {
  outline: none;
}

:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* ✅ Ou estilos de foco personalizados */
button:focus-visible {
  box-shadow: 0 0 0 3px rgba(0, 95, 204, 0.5);
}
```

### Links para pular (2.4.1)

```html
<body>
  <a href="#main-content" class="skip-link">Pular para conteúdo principal</a>
  <header><!-- navigation --></header>
  <main id="main-content" tabindex="-1">
    <!-- main content -->
  </main>
</body>
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px 16px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### Timing (2.2)

```javascript
// Permita que usuários estendam limites de tempo
function showSessionWarning() {
  const modal = createModal({
    title: 'Sessão expirando',
    content: 'Sua sessão expirará em 2 minutos.',
    actions: [
      { label: 'Estender sessão', action: extendSession },
      { label: 'Sair', action: logout }
    ],
    timeout: 120000 // 2 minutos para responder
  });
}
```

### Movimento (2.3)

```css
/* Respeite a preferência de movimento reduzido */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## Compreensível

### Idioma da página (3.1.1)

```html
<!-- ❌ Sem idioma especificado -->
<html>

<!-- ✅ Idioma especificado -->
<html lang="pt-BR">

<!-- ✅ Mudanças de idioma dentro da página -->
<p>A palavra em inglês para olá é <span lang="en">hello</span>.</p>
```

### Navegação consistente (3.2.3)

```html
<!-- A navegação deve ser consistente entre páginas -->
<nav aria-label="Principal">
  <ul>
    <li><a href="/" aria-current="page">Início</a></li>
    <li><a href="/products">Produtos</a></li>
    <li><a href="/about">Sobre</a></li>
  </ul>
</nav>
```

### Rótulos de formulário (3.3.2)

```html
<!-- ❌ Sem associação de rótulo -->
<input type="email" placeholder="Email">

<!-- ✅ Rótulo explícito -->
<label for="email">Endereço de email</label>
<input type="email" id="email" name="email" 
       autocomplete="email" required>

<!-- ✅ Rótulo implícito -->
<label>
  Endereço de email
  <input type="email" name="email" autocomplete="email" required>
</label>

<!-- ✅ Com instruções -->
<label for="password">Senha</label>
<input type="password" id="password" 
       aria-describedby="password-requirements">
<p id="password-requirements">
  Deve ter pelo menos 8 caracteres com um número.
</p>
```

### Tratamento de erros (3.3.1, 3.3.3)

```html
<!-- Anuncie erros para leitores de tela -->
<form novalidate>
  <div class="field" aria-live="polite">
    <label for="email">Email</label>
    <input type="email" id="email" 
           aria-invalid="true"
           aria-describedby="email-error">
    <p id="email-error" class="error" role="alert">
      Por favor, insira um endereço de email válido (ex: nome@exemplo.com)
    </p>
  </div>
</form>
```

```javascript
// Foque no primeiro erro ao enviar
form.addEventListener('submit', (e) => {
  const firstError = form.querySelector('[aria-invalid="true"]');
  if (firstError) {
    e.preventDefault();
    firstError.focus();
    
    // Anuncie resumo de erro
    const errorSummary = document.getElementById('error-summary');
    errorSummary.textContent = `${errors.length} erros encontrados. Por favor, corrija-os e tente novamente.`;
    errorSummary.focus();
  }
});
```

---

## Robusto

### HTML válido (4.1.1)

```html
<!-- ❌ IDs duplicados -->
<div id="content">...</div>
<div id="content">...</div>

<!-- ❌ Aninhamento inválido -->
<a href="/"><button>Clique</button></a>

<!-- ✅ IDs únicos -->
<div id="main-content">...</div>
<div id="sidebar-content">...</div>

<!-- ✅ Aninhamento apropriado -->
<a href="/" class="button-link">Clique</a>
```

### Uso de ARIA (4.1.2)

**Prefira elementos nativos:**
```html
<!-- ❌ Função ARIA em div -->
<div role="button" tabindex="0">Clique</div>

<!-- ✅ Botão nativo -->
<button>Clique</button>

<!-- ❌ Caixa de seleção ARIA -->
<div role="checkbox" aria-checked="false">Opção</div>

<!-- ✅ Caixa de seleção nativa -->
<label><input type="checkbox"> Opção</label>
```

**Quando ARIA é necessária:**
```html
<!-- Componente de abas personalizado -->
<div role="tablist" aria-label="Informações do produto">
  <button role="tab" id="tab-1" aria-selected="true" 
          aria-controls="panel-1">Descrição</button>
  <button role="tab" id="tab-2" aria-selected="false" 
          aria-controls="panel-2" tabindex="-1">Avaliações</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  <!-- Conteúdo do painel -->
</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  <!-- Conteúdo do painel -->
</div>
```

### Regiões dinâmicas (4.1.3)

```html
<!-- Atualizações de status -->
<div aria-live="polite" aria-atomic="true" class="status">
  <!-- O conteúdo atualizado é anunciado para leitores de tela -->
</div>

<!-- Alertas urgentes -->
<div role="alert" aria-live="assertive">
  <!-- Interrompe o anúncio atual -->
</div>
```

```javascript
// Anuncie mudanças de conteúdo dinâmico
function showNotification(message, type = 'polite') {
  const container = document.getElementById(`${type}-announcer`);
  container.textContent = ''; // Limpe primeiro
  requestAnimationFrame(() => {
    container.textContent = message;
  });
}
```

---

## Checklist de testes

### Testes automatizados
```bash
# Auditoria de acessibilidade do Lighthouse
npx lighthouse https://example.com --only-categories=accessibility

# axe-core
npm install @axe-core/cli -g
axe https://example.com
```

### Testes manuais

- [ ] **Navegação por teclado:** Tab em toda a página, use Enter/Space para ativar
- [ ] **Leitor de tela:** Teste com VoiceOver (Mac), NVDA (Windows) ou TalkBack (Android)
- [ ] **Zoom:** Conteúdo utilizável com zoom de 200%
- [ ] **Contraste alto:** Teste com Modo de Contraste Alto do Windows
- [ ] **Movimento reduzido:** Teste com `prefers-reduced-motion: reduce`
- [ ] **Ordem de foco:** Lógica e segue a ordem visual

### Comandos do leitor de tela

| Ação | VoiceOver (Mac) | NVDA (Windows) |
|------|-----------------|----------------|
| Iniciar/Parar | ⌘ + F5 | Ctrl + Alt + N |
| Próximo item | VO + → | ↓ |
| Item anterior | VO + ← | ↑ |
| Ativar | VO + Space | Enter |
| Lista de headings | VO + U, depois setas | H / Shift + H |
| Lista de links | VO + U | K / Shift + K |

---

## Problemas comuns por impacto

### Críticos (corrigir imediatamente)
1. Rótulos de formulário ausentes
2. Texto alternativo de imagem ausente
3. Contraste de cor insuficiente
4. Armadilhas de teclado
5. Sem indicadores de foco

### Sérios (corrigir antes do lançamento)
1. Idioma da página ausente
2. Estrutura de heading ausente
3. Texto de link não descritivo
4. Mídia reproduzida automaticamente
5. Links para pular ausentes

### Moderados (corrigir em breve)
1. Rótulos ARIA ausentes em ícones
2. Navegação inconsistente
3. Identificação de erro ausente
4. Timing sem controles
5. Regiões landmark ausentes

## Referências

- [WCAG 2.1 Referência Rápida](https://www.w3.org/WAI/WCAG21/quickref/)
- [Práticas de Autoria WAI-ARIA](https://www.w3.org/WAI/ARIA/apg/)
- [Regras do axe do Deque](https://dequeuniversity.com/rules/axe/)
- [Auditoria de Qualidade Web](../web-quality-audit/SKILL.md)