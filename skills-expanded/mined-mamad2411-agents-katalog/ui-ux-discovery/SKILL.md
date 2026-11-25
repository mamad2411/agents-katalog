---
name: ui-ux-discovery
description: Padrões centralizados para descoberta de UI/UX em projetos. Perguntas granulares por aspecto visual (cores, tipografia, layout, efeitos, logo). Validação híbrida manter vs. modernizar.
---

# UI/UX Discovery Patterns

> **Single Source of Truth** para todos os workflows que definem Design System.

---

## 🎯 PROPÓSITO

Garantir consistência em:
1. **Extração de Identidade** - Analisar identidade visual existente
2. **Perguntas Granulares** - Decisões por aspecto (não tudo ou nada)
3. **Integração** - Sempre usar `/ui-ux-pro-max` para recomendações
4. **Consolidação** - Combinar decisões mantidas + modernizadas

---

## 🔗 QUANDO USAR?

| Workflow | Fase | Trigger |
|----------|------|---------|
| `/legacy-project` | Phase 5.5 | Após TDD Reverso |
| `/new-project` | Phase 2.5, 5.3 | Após TDD / Implementação |
| `/new-task` | Styling | Quando inclui mudanças visuais |

---

## 📊 PROCESSO COMPLETO (5 Passos)

### PASSO 1: Extrair Identidade Visual Atual

> **Pulado se:** Projeto é novo (sem código existente)

Analisar código existente e extrair:

```markdown
## 📊 Identidade Visual Atual (Extraída)

### Cores Principais
| Uso | Cor | Hex |
|-----|-----|-----|
| Primária | {cor} | #XXXXXX |
| Secundária | {cor} | #XXXXXX |
| Acento | {cor} | #XXXXXX |
| Background | {cor} | #XXXXXX |
| Texto | {cor} | #XXXXXX |

### Tipografia Atual
- Heading: {fonte}
- Body: {fonte}

### Elementos Visuais
- Logo: {descrição}
- Ícones: {tipo}
- Layout: {descrição}
```

---

### PASSO 1.5: Armazenar Referências Visuais (Se Fornecidas) ⭐

> **Trigger:** Usuário envia imagens de referência para Design System

> [!IMPORTANT]
> **OBRIGATÓRIO:** Se o usuário fornecer imagens de referência, copiá-las para o projeto ANTES de gerar MASTER.md.

**Ações:**

1. **Criar pasta de referências:**
   ```bash
   # PowerShell
   New-Item -ItemType Directory -Force -Path "design-system/{projeto}/references/"
   
   # Bash
   mkdir -p design-system/{projeto}/references/
   ```

2. **Copiar imagens para o projeto:**
   ```bash
   # PowerShell
   Copy-Item "{path_da_imagem}" "design-system/{projeto}/references/" -Force
   
   # Bash
   cp "{path_da_imagem}" "design-system/{projeto}/references/"
   ```

3. **Documentar no MASTER.md:**
   Adicionar seção após a geração:
   ```markdown
   ## 📸 Reference Images
   
   Imagens de referência fornecidas pelo usuário:
   - ![ref_001](./references/{nome_arquivo_1}.png)
   - ![ref_002](./references/{nome_arquivo_2}.png)
   ```

**Estrutura Final:**
```
design-system/
├── {projeto}/
│   ├── MASTER.md          ← Source of Truth
│   ├── references/        ← NEW: Imagens de referência
│   │   ├── ref_001.png
│   │   └── ref_002.png
│   └── pages/
│       └── ...
```

> [!CAUTION]
> **NÃO** deixar imagens de referência apenas no brain/conversation. **SEMPRE** copiar para o projeto.

---

### PASSO 2: Executar `/ui-ux-pro-max`


> [!IMPORTANT]
> **OBRIGATÓRIO:** Sempre executar para ter recomendações profissionais.

```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "{tipo} {indústria}" --design-system -p "{Projeto}"
```

**Capturar:**
- Style moderno sugerido
- Paleta de cores recomendada
- Tipografia moderna
- Efeitos visuais

---

### PASSO 3: Perguntas Granulares (OBRIGATÓRIO) ⭐

> [!CAUTION]
> **BLOQUEADOR:** ANTES de definir Design System, fazer estas perguntas ao usuário.
> NÃO assumir que vai manter tudo ou renovar tudo.

**Template de Perguntas:**

```markdown
## 🎨 Decisões de Design System

Analisei o projeto e tenho recomendações modernas.
Por favor, decida **para cada aspecto** o que deseja:

---

### 1. 🎨 CORES

**Atual:** {cores extraídas ou "N/A para projeto novo"}
**Recomendação:** {paleta do ui-ux-pro-max}

Qual direção?
- [ ] A) **Manter cores atuais** (sem alteração)
- [ ] B) **Manter primária/secundária**, modernizar o resto
- [ ] C) **Renovar completamente** (usar recomendação)
- [ ] D) **Definir manualmente** (me informe as cores)

---

### 2. ✏️ TIPOGRAFIA

**Atual:** {fontes extraídas ou "N/A"}
**Recomendação:** {fontes do ui-ux-pro-max}

Qual direção?
- [ ] A) **Manter fontes atuais**
- [ ] B) **Modernizar** (usar recomendação)
- [ ] C) **Definir manualmente** (me informe as fontes)

---

### 3. 📐 LAYOUT E ESTRUTURA

**Atual:** {descrição do layout ou "N/A"}
**Recomendação:** {layout moderno do ui-ux-pro-max}

Qual direção?
- [ ] A) **Manter estrutura similar** (mesmas seções)
- [ ] B) **Reorganizar** seguindo tendências modernas
- [ ] C) **Definir manualmente** (me descreva a estrutura)

---

### 4. ✨ EFEITOS VISUAIS

**Atual:** {efeitos atuais ou "nenhum"}
**Recomendação:** {glassmorphism, gradients, shadows, micro-animations}

Quais efeitos incluir? (marque todos que deseja)
- [ ] Glassmorphism (transparência com blur)
- [ ] Gradients sutis
- [ ] Shadows modernas
- [ ] Micro-animations (hover, loading)
- [ ] Dark mode
- [ ] Nenhum efeito especial

---

### 5. 🖼️ LOGO E BRANDING

Qual direção?
- [ ] A) **Manter logo atual** exatamente como está
- [ ] B) **Manter logo**, atualizar aplicação (cores, tamanhos)
- [ ] C) **Novo logo** será fornecido depois
- [ ] D) **N/A** (projeto sem logo definido ainda)

---

Por favor, responda com as letras/opções de cada aspecto.
Exemplo: "1-B, 2-B, 3-B, 4-Glassmorphism+Animations+Dark, 5-A"
```

---

### PASSO 4: Consolidar Decisões

Baseado nas respostas:

1. Combinar elementos mantidos + modernizados
2. Aplicar recomendações do `/ui-ux-pro-max` conforme decisões
3. Gerar `design-system/{projeto}/MASTER.md` com escolhas híbridas

**Template de Consolidação:**

```markdown
## design-system/{projeto}/MASTER.md

> Gerado via `/ui-ux-pro-max` + decisões do usuário em {data}

### Decisões Tomadas
| Aspecto | Decisão | Resultado |
|---------|---------|-----------|
| Cores | {A/B/C/D} | {descrição} |
| Tipografia | {A/B/C} | {descrição} |
| Layout | {A/B/C} | {descrição} |
| Efeitos | {lista} | {descrição} |
| Logo | {A/B/C/D} | {descrição} |

---

### Cores
- Primary: {cor final}
- Secondary: {cor final}
- Accent: {cor final}
- Background: {cor final}
- Surface: {cor final}
- Text: {cor final}

### Tipografia
- Heading: {fonte final}
- Body: {fonte final}
- Mono: {fonte para código}

### Layout
- {descrição do layout escolhido}

### Efeitos Visuais
- {lista de efeitos escolhidos}

### Logo
- {descrição}
```

---

### PASSO 5: Validar e Aprovar

- **AGUARDAR** aprovação humana do Design System consolidado

---

## ✅ GATE DE SAÍDA

```
[ ] Identidade visual atual extraída (se projeto existente)
[ ] Referências visuais armazenadas em design-system/{projeto}/references/ (se fornecidas)
[ ] /ui-ux-pro-max executado
[ ] Perguntas granulares respondidas pelo usuário
[ ] Design System consolidado com decisões híbridas
[ ] Design System aprovado pelo humano
```

---

## 📋 VARIAÇÕES POR CONTEXTO

### Projeto Novo (sem código existente)

- **Pular** Passo 1 (extração)
- **Opções A)** nas perguntas ficam como "N/A - projeto novo"
- Foco em escolher entre recomendações ou definir manual

### Projeto Legado (com código)

- **Executar** todos os 5 passos
- Permitir decisões híbridas (manter primárias + modernizar resto)

### Enhancement (projeto ativo)

- Verificar se já existe `design-system/{projeto}/MASTER.md`
- Se existe: Apenas validar/atualizar aspectos afetados
- Se não existe: Executar processo completo

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow | Quando Referenciar |
|----------|-------------------|
| `/legacy-project` | Phase 5.5 - Design System |
| `/new-project` | Phase 2.5 e Phase 5.3 |
| `/new-task` | Quando envolve mudanças visuais |
| `/ui-ux-pro-max` | Como complemento às recomendações |

---

## 🔴 REGRAS CRÍTICAS

1. **SEMPRE** usar `/ui-ux-pro-max` para recomendações
2. **NUNCA** assumir tudo ou nada - perguntar por aspecto
3. **AGUARDAR** resposta do usuário antes de consolidar
4. **DOCUMENTAR** decisões tomadas no Design System
5. **VALIDAR** com usuário antes de prosseguir

