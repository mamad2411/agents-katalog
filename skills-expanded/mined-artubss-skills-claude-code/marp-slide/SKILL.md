---
name: marp-slide
description: Crie slides de apresentação Marp profissionais com 7 temas lindos (padrão, minimalista, colorido, escuro, gradiente, tech, negócios). Use quando usuários solicitarem criação de slides, apresentações ou documentos Marp. Suporta temas personalizados, layouts de imagem e requisitos "deixe bonito" com melhorias de qualidade automática.
---

# Criador de Slides Marp

Crie slides de apresentação profissionais e visualmente atraentes com Marp, com 7 temas pré-desenhados e melhores práticas integradas.

## Quando Usar Esta Habilidade

Use esta habilidade quando o usuário:
- Solicita criar slides de apresentação ou documentos Marp
- Pede para "deixar os slides bonitos" ou "melhorar o design"
- Fornece instruções vagas como "deixe bonito" ou "deixe legal"
- Quer criar materiais de aula ou seminário
- Precisa de slides com foco em bullet points e ocasionalmente imagens

## Início Rápido

### Passo 1: Selecionar Tema

Primeiro, determine o tema apropriado baseado no tipo de conteúdo e solicitação do usuário.

**Seleção rápida de tema:**
- **Conteúdo técnico/desenvolvimento** → tema tech
- **Negócios/Corporativo** → tema business
- **Criativo/Evento** → tema colorful ou gradient
- **Acadêmico/Simples** → tema minimal
- **Geral/Incerto** → tema padrão
- **Fundo escuro preferido** → tema dark ou tech

Para orientação detalhada sobre seleção de temas, leia `references/theme-selection.md`.

### Passo 2: Criar Slides

1. **Leia as referências primeiro**:
   - Sempre comece lendo `references/marp-syntax.md` para sintaxe básica
   - Para imagens: `references/image-patterns.md` (sintaxe oficial de imagens Marpit)
   - Para recursos avançados (matemática, emoji): `references/advanced-features.md`
   - Para temas personalizados: `references/theme-css-guide.md`

2. Copie conteúdo do arquivo de template apropriado:
   - `assets/template-basic.md` - Tema padrão (mais comum)
   - `assets/template-minimal.md` - Tema minimalista
   - `assets/template-colorful.md` - Tema colorido
   - `assets/template-dark.md` - Tema modo escuro
   - `assets/template-gradient.md` - Tema gradiente
   - `assets/template-tech.md` - Tema tech/código
   - `assets/template-business.md` - Tema negócios

3. Leia `references/best-practices.md` para diretrizes de qualidade

4. Estruture o conteúdo seguindo as melhores práticas:
   - Slide de título com `<!-- _class: lead -->`
   - Títulos concisos em h2 (5-7 caracteres)
   - 3-5 bullet points por slide
   - Espaçamento adequado

5. Adicione imagens se necessário usando padrões de `references/image-patterns.md`

6. Salve no `diretório de saída do projeto` com extensão `.md`

## Temas Disponíveis

### 1. Tema Padrão
**Cores**: Fundo bege, texto azul-marinho, títulos azuis
**Estilo**: Limpo e sofisticado com linhas decorativas
**Use para**: Seminários gerais, palestras, apresentações
**Template**: `template-basic.md`

### 2. Tema Minimalista
**Cores**: Fundo branco, texto cinza, títulos pretos
**Estilo**: Decoração mínima, margens largas, fontes leves
**Use para**: Apresentações focadas em conteúdo, palestras acadêmicas
**Template**: `template-minimal.md`

### 3. Tema Colorido e Pop
**Cores**: Fundo com gradiente rosa, acentos multicoloridos
**Estilo**: Gradientes vibrantes, fontes em negrito, acentos arco-íris
**Use para**: Eventos orientados para público jovem, projetos criativos
**Template**: `template-colorful.md`

### 4. Tema Modo Escuro
**Cores**: Fundo preto, acentos ciano/roxo
**Estilo**: Tema escuro com efeitos de brilho, agradável aos olhos
**Use para**: Apresentações tech, palestras noturnas, visual moderno
**Template**: `template-dark.md`

### 5. Tema Fundo Gradiente
**Cores**: Gradientes roxo/rosa/azul/verde (varia por slide)
**Estilo**: Gradiente diferente por slide, texto branco, sombras
**Use para**: Apresentações focadas visualmente, criativas
**Template**: `template-gradient.md`

### 6. Tema Tech/Código
**Cores**: Fundo estilo GitHub escuro, acentos azul/verde
**Estilo**: Fontes de código, cabeçalhos estilo Markdown com # símbolos
**Use para**: Tutoriais de programação, meetups tech, conteúdo para desenvolvedores
**Template**: `template-tech.md`

### 7. Tema Business
**Cores**: Fundo branco, títulos azul-marinho, acentos azuis
**Estilo**: Estilo de apresentação corporativa, borda superior, suporte a tabelas
**Use para**: Apresentações de negócios, propostas, relatórios
**Template**: `template-business.md`

## Processo de Criação de Slides

### Fluxo de Trabalho Básico

1. **Entender requisitos**
   - Identificar conteúdo: título, tópicos, pontos-chave
   - Determinar público-alvo
   - Avaliar nível de formalidade

2. **Selecionar tema**
   - Use as regras de seleção rápida acima
   - Se incerto, consulte `references/theme-selection.md`
   - Padrão para tema padrão se ainda incerto

3. **Aplicar template**
   - Carregue o template apropriado de `assets/`
   - CSS já está incorporado - não precisa de arquivos externos
   - Mantenha a estrutura do template

4. **Estruturar conteúdo**
   - Slide de título: `<!-- _class: lead -->` + h1
   - Slides de conteúdo: título h2 + bullet points
   - Mantenha títulos com 5-7 caracteres
   - Use 3-5 bullet points por slide

5. **Refinar qualidade**
   - Leia `references/best-practices.md`
   - Garanta espaçamento adequado
   - Mantenha consistência
   - Mantenha texto conciso (15-25 caracteres por linha)

6. **Adicionar imagens**
   - Se necessário, consulte `references/image-patterns.md`
   - Comum: `![bg right:40%](image.png)` para imagens ao lado
   - Use sintaxe própria de imagem Marp

7. **Arquivo de saída**
   - Salve no `diretório de saída do projeto`
   - Use nome descritivo como `presentation.md`

## Tratamento de Requisitos "Deixe Bonito"

Quando usuários dão instruções vagas como "deixe bonito", "deixe legal" ou similares:

1. **Deduza o tema do conteúdo**:
   - Conteúdo de negócios → tema business
   - Conteúdo técnico → tema tech ou dark
   - Conteúdo criativo → tema gradient ou colorful
   - Geral → tema padrão

2. **Aplique as melhores práticas automaticamente**:
   - Encurte títulos para 5-7 caracteres
   - Limite bullet points a 3-5 itens
   - Adicione espaçamento adequado
   - Use estrutura consistente

3. **Melhore a hierarquia visual**:
   - Use h3 para sub-seções quando apropriado
   - Divida texto denso em múltiplos slides
   - Garanta fluxo lógico (intro → corpo → conclusão)

4. **Mantenha tom profissional**:
   - Alinhe formalidade ao conteúdo
   - Use estrutura paralela em listas
   - Mantenha termos técnicos consistentes

## Integração de Imagens

Para slides com imagens, consulte `references/image-patterns.md` para sintaxe detalhada.

Padrões comuns:
- **Imagem ao lado**: `![bg right:40%](image.png)` - Imagem à direita, texto à esquerda
- **Centralizada**: `![w:600px](image.png)` - Centralizada com largura específica
- **Fundo cheio**: `![bg](image.png)` - Fundo em tela inteira
- **Múltiplas imagens**: Múltiplas declarações `![bg]`

Exemplo de padrão de aula:
```markdown
## Título do Slide

![bg right:40%](diagram.png)

- Ponto de explicação 1
- Ponto de explicação 2
- Ponto de explicação 3
```

## Saída de Arquivo

Sempre salve o arquivo Marp final no `diretório de saída do projeto` com extensão `.md`:
- `presentation.md`
- `seminar-slides.md`
- `lecture-materials.md`

## Checklist de Qualidade

Antes de entregar os slides, verifique:
- [ ] Tema selecionado apropriadamente para o conteúdo
- [ ] CSS do tema está incorporado no arquivo
- [ ] Slide de título usa `<!-- _class: lead -->`
- [ ] Todos os títulos h2 são concisos (5-7 caracteres)
- [ ] Bullet points são 3-5 itens por slide
- [ ] Imagens usam sintaxe Marp apropriada
- [ ] Arquivo salvo no diretório de saída
- [ ] Conteúdo segue as melhores práticas

## Referências

### Documentação Principal
- **Sintaxe Marp**: `references/marp-syntax.md` - Sintaxe básica Marp/Marpit (diretivas, frontmatter, paginação, etc.)
- **Padrões de imagem**: `references/image-patterns.md` - Sintaxe oficial de imagem (bg, filtros, fundos divididos)
- **Guia CSS de tema**: `references/theme-css-guide.md` - Como criar temas personalizados baseado em especificação Marpit
- **Recursos avançados**: `references/advanced-features.md` - Matemática, emoji, listas fragmentadas, CLI Marp, VS Code
- **Temas oficiais**: `references/official-themes.md` - Documentação temas default, gaia, uncover

### Guias de Qualidade e Seleção
- **Seleção de tema**: `references/theme-selection.md` - Como escolher o tema certo para o conteúdo
- **Melhores práticas**: `references/best-practices.md` - Diretrizes de qualidade para slides "legais"

### Templates e Assets
- **Templates**: `assets/template-*.md` - Pontos de partida com CSS incorporado para cada tema (7 temas)
- **CSS independente**: `assets/theme-*.css` - Arquivos CSS para referência (já incorporado em templates)

### Links Externos Oficiais
- **Site Oficial Marp**: https://marp.app/
- **Diretivas Marpit**: https://marpit.marp.app/directives
- **Sintaxe de Imagem Marpit**: https://marpit.marp.app/image-syntax
- **CSS de Tema Marpit**: https://marpit.marp.app/theme-css
- **GitHub Marp Core**: https://github.com/marp-team/marp-core
- **GitHub CLI Marp**: https://github.com/marp-team/marp-cli