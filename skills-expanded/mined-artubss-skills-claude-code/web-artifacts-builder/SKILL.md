---
name: web-artifacts-builder
description: Suite de ferramentas para criar artefatos HTML elaborados e multi-componentes no claude.ai usando tecnologias modernas de frontend (React, Tailwind CSS, shadcn/ui). Use para artefatos complexos que exigem gerenciamento de estado, roteamento ou componentes shadcn/ui - não para artefatos HTML/JSX simples em arquivo único.
license: Termos completos em LICENSE.txt
---

# Web Artifacts Builder

Para criar poderosos artefatos de frontend no claude.ai, siga estas etapas:
1. Inicialize o repositório frontend usando `scripts/init-artifact.sh`
2. Desenvolva seu artefato editando o código gerado
3. Agrupe todo o código em um único arquivo HTML usando `scripts/bundle-artifact.sh`
4. Exiba o artefato ao usuário
5. (Opcional) Teste o artefato

**Stack**: React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui

## Diretrizes de Design e Estilo

MUITO IMPORTANTE: Para evitar o que geralmente é chamado de "AI slop", evite usar layouts excessivamente centralizados, gradientes roxos, cantos arredondados uniformes e fonte Inter.

## Início Rápido

### Passo 1: Inicializar Projeto

Execute o script de inicialização para criar um novo projeto React:
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

Isso cria um projeto totalmente configurado com:
- ✅ React + TypeScript (via Vite)
- ✅ Tailwind CSS 3.4.1 com sistema de temas shadcn/ui
- ✅ Aliases de caminho (`@/`) configurados
- ✅ 40+ componentes shadcn/ui pré-instalados
- ✅ Todas as dependências Radix UI incluídas
- ✅ Parcel configurado para bundling (via .parcelrc)
- ✅ Compatibilidade com Node 18+ (detecta e fixa versão do Vite automaticamente)

### Passo 2: Desenvolver Seu Artefato

Para construir o artefato, edite os arquivos gerados. Veja **Tarefas Comuns de Desenvolvimento** abaixo para orientação.

### Passo 3: Agrupar em Arquivo HTML Único

Para agrupar a aplicação React em um único artefato HTML:
```bash
bash scripts/bundle-artifact.sh
```

Isso cria `bundle.html` - um artefato autossuficiente com todo JavaScript, CSS e dependências incorporadas. Este arquivo pode ser compartilhado diretamente em conversas do Claude como um artefato.

**Requisitos**: Seu projeto deve ter um `index.html` no diretório raiz.

**O que o script faz**:
- Instala dependências de bundling (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- Cria configuração `.parcelrc` com suporte a alias de caminho
- Faz build com Parcel (sem source maps)
- Incorpora todos os assets em um único HTML usando html-inline

### Passo 4: Compartilhar Artefato com Usuário

Por fim, compartilhe o arquivo HTML agrupado na conversa com o usuário para que ele possa visualizá-lo como um artefato.

### Passo 5: Testar/Visualizar o Artefato (Opcional)

Observação: Este é um passo completamente opcional. Execute apenas se necessário ou solicitado.

Para testar/visualizar o artefato, use as ferramentas disponíveis (incluindo outras Skills ou ferramentas integradas como Playwright ou Puppeteer). Em geral, evite testar o artefato antecipadamente, pois adiciona latência entre a solicitação e quando o artefato finalizado puder ser visto. Teste depois, após apresentar o artefato, se solicitado ou se problemas surgirem.

## Referência

- **Componentes shadcn/ui**: https://ui.shadcn.com/docs/components