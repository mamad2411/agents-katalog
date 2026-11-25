---
name: web-quality-audit
description: Auditoria abrangente de qualidade web cobrindo performance, acessibilidade, SEO e melhores práticas. Use quando solicitado para "auditar meu site", "revisar qualidade web", "executar auditoria lighthouse", "verificar qualidade de página" ou "otimizar meu website".
license: MIT
metadata:
  author: web-quality-skills
  version: "1.0"
---

# Auditoria de qualidade web

Revisão abrangente de qualidade baseada em auditorias do Google Lighthouse. Cobre Performance, Acessibilidade, SEO e Melhores Práticas em mais de 150 verificações.

## Como funciona

1. Analisar o código/projeto fornecido em busca de problemas de qualidade
2. Categorizar descobertas por severidade (Crítica, Alta, Média, Baixa)
3. Fornecer recomendações específicas e acionáveis
4. Incluir exemplos de código para correções

## Categorias de auditoria

### Performance (40% dos problemas típicos)

**Core Web Vitals** — Devem passar para boa experiência de página:
* **LCP (Largest Contentful Paint) < 2.5s.** O maior elemento visível deve renderizar rapidamente. Otimize imagens, fontes e tempo de resposta do servidor.
* **INP (Interaction to Next Paint) < 200ms.** Interações do usuário devem parecer instantâneas. Reduza o tempo de execução do JavaScript e divida tarefas longas.
* **CLS (Cumulative Layout Shift) < 0.1.** Conteúdo não deve se mover. Defina dimensões explícitas em imagens, embeds e anúncios.

**Otimização de recursos:**
* **Comprimir imagens.** Use WebP/AVIF com fallbacks. Distribua imagens redimensionadas corretamente via `srcset`.
* **Minimizar JavaScript.** Remova código não utilizado. Use code splitting. Adia scripts não críticos.
* **Otimizar CSS.** Extraia CSS crítico. Remova estilos não utilizados. Evite `@import`.
* **Fontes eficientes.** Use `font-display: swap`. Precarregue fontes críticas. Reduza a subconjuntos de caracteres necessários.

**Estratégia de carregamento:**
* **Pré-conectar a origens.** Adicione `<link rel="preconnect">` para domínios de terceiros.
* **Pré-carregar assets críticos.** Imagens LCP, fontes e CSS acima da dobra.
* **Carregamento lazy para conteúdo abaixo da dobra.** Imagens, iframes e componentes pesados.
* **Cache eficaz.** TTLs de cache longa para assets estáticos. Caching imutável para arquivos com hash.

### Acessibilidade (30% dos problemas típicos)

**Perceptível:**
* **Alternativas de texto.** Toda `<img>` tem `alt` text significativo. Imagens decorativas usam `alt=""`.
* **Contraste de cor.** Mínimo 4.5:1 para texto normal, 3:1 para texto grande (WCAG AA).
* **Não dependa apenas de cor.** Use ícones, padrões ou texto junto com indicadores de cor.
* **Legendas e transcrições.** Vídeos têm legendas. Áudio tem transcrições.

**Operável:**
* **Acessível por teclado.** Toda funcionalidade disponível via teclado. Sem armadilhas de teclado.
* **Foco visível.** Indicadores de foco claros em todos os elementos interativos.
* **Links de salto.** Forneça "Pular para conteúdo principal" para usuários de teclado.
* **Tempo suficiente.** Usuários podem estender limites de tempo. Sem conteúdo avançando automaticamente sem controles.

**Compreensível:**
* **Idioma da página.** Defina atributo `lang` em `<html>`.
* **Navegação consistente.** Mesma estrutura de navegação entre páginas.
* **Identificação de erro.** Erros de formulário descritos claramente e associados a campos.
* **Labels e instruções.** Todos os inputs de formulário têm labels associadas.

**Robusto:**
* **HTML válido.** Sem IDs duplicados. Elementos adequadamente aninhados.
* **ARIA utilizado corretamente.** Prefira elementos nativos. Roles ARIA correspondem ao comportamento.
* **Nome, role, valor.** Elementos interativos têm nomes acessíveis e roles corretos.

### SEO (15% dos problemas típicos)

**Rastreabilidade:**
* **robots.txt válido.** Não bloqueia recursos importantes.
* **Sitemap XML.** Lista todas as páginas importantes. Submetido ao Search Console.
* **URLs canônicas.** Previna problemas de conteúdo duplicado.
* **Sem noindex em páginas importantes.** Verifique meta robots e headers.

**SEO On-Page:**
* **Title tags únicos.** 50-60 caracteres. Palavra-chave primária incluída.
* **Meta descriptions.** 150-160 caracteres. Atrativas e únicas.
* **Hierarquia de headings.** Um único `<h1>`. Estrutura lógica de headings.
* **Texto de link descritivo.** Não "clique aqui" ou "leia mais".

**SEO técnico:**
* **Mobile-friendly.** Design responsivo. Alvos de toque ≥ 48px.
* **HTTPS.** Conexão segura obrigatória.
* **Carregamento rápido.** Performance impacta classificação diretamente.
* **Dados estruturados.** JSON-LD para rich snippets (Article, Product, FAQ, etc.).

### Melhores práticas (15% dos problemas típicos)

**Segurança:**
* **HTTPS em todo lugar.** Sem conteúdo misto. HSTS ativado.
* **Sem bibliotecas vulneráveis.** Mantenha dependências atualizadas.
* **Headers CSP.** Content Security Policy para prevenir XSS.
* **Source maps não expostos.** Em builds de produção.

**Padrões modernos:**
* **Sem APIs deprecadas.** Substitua `document.write`, XHR síncrono, etc.
* **Doctype válido.** Use `<!DOCTYPE html>`.
* **Charset declarado.** `<meta charset="UTF-8">` como primeiro elemento em `<head>`.
* **Sem erros do navegador.** Console limpo. Sem problemas CORS.

**Padrões UX:**
* **Sem interstitiais intrusivos.** Especialmente em mobile.
* **Requisições de permissão claras.** Peça apenas quando necessário, com contexto.
* **Sem botões enganosos.** Botões fazem o que dizem.

## Níveis de severidade

| Nível | Descrição | Ação |
|-------|-----------|------|
| **Crítica** | Vulnerabilidades de segurança, falhas completas | Corrigir imediatamente |
| **Alta** | Falhas de Core Web Vitals, barreiras de a11y maiores | Corrigir antes do lançamento |
| **Média** | Oportunidades de performance, melhorias SEO | Corrigir dentro da sprint |
| **Baixa** | Otimizações menores, qualidade de código | Corrigir quando conveniente |

## Formato de saída da auditoria

Ao executar uma auditoria, estruture as descobertas assim:

```markdown
## Resultados da auditoria

### Problemas críticos (X encontrados)
- **[Categoria]** Descrição do problema. Arquivo: `path/to/file.js:123`
  - **Impacto:** Por que isso importa
  - **Correção:** Mudança de código específica ou recomendação

### Alta prioridade (X encontrados)
...

### Resumo
- Performance: X problemas (Y críticos)
- Acessibilidade: X problemas (Y críticos)
- SEO: X problemas
- Melhores Práticas: X problemas

### Prioridade recomendada
1. Corrigir isso primeiro porque...
2. Depois abordar...
3. Finalmente otimizar...
```

## Checklist rápido

### Antes de cada deploy
- [ ] Core Web Vitals passando
- [ ] Sem erros de acessibilidade (axe/Lighthouse)
- [ ] Sem erros no console
- [ ] HTTPS funcionando
- [ ] Meta tags presentes

### Revisão semanal
- [ ] Verificar Search Console para problemas
- [ ] Revisar tendências de Core Web Vitals
- [ ] Atualizar dependências
- [ ] Testar com leitor de tela

### Deep dive mensal
- [ ] Auditoria completa do Lighthouse
- [ ] Profiling de performance
- [ ] Auditoria de acessibilidade com usuários reais
- [ ] Revisão de palavras-chave SEO

## Referências

Para diretrizes detalhadas em áreas específicas:
- [Performance Optimization](../performance/SKILL.md)
- [Core Web Vitals](../core-web-vitals/SKILL.md)
- [Accessibility](../accessibility/SKILL.md)
- [SEO](../seo/SKILL.md)
- [Best Practices](../best-practices/SKILL.md)