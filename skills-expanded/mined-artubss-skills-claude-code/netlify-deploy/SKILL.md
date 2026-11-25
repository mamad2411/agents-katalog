---
name: netlify-deploy
description: Deploy projetos web para Netlify usando a Netlify CLI (`npx netlify`). Use quando o usuário solicitar fazer deploy, hospedar, publicar ou vincular um site/repositório no Netlify, incluindo deploys de preview e produção.
author: openai
---

# Skill de Deploy no Netlify

Automatize deploys no Netlify usando a Netlify CLI com detecção inteligente de configuração de projeto e contexto de deployment.

## Visão Geral

Este skill automatiza deploys no Netlify por:
- Verificar autenticação na Netlify CLI
- Detectar configuração e framework do projeto
- Vincular a sites existentes ou criar novos
- Fazer deploy para ambientes de produção ou preview

## Pré-requisitos

- **Netlify CLI**: Instalada via npx (não requer instalação global)
- **Autenticação**: Conta Netlify com sessão de login ativa
- **Projeto**: Projeto web válido no diretório atual
- Quando a sandbox bloqueia chamadas de rede do deployment, execute novamente com `sandbox_permissions=require_escalated`.
- O deployment pode levar alguns minutos. Use valores de timeout apropriados.

## Padrão de Autenticação

O skill usa a abordagem **Netlify CLI pré-autenticada**:

1. Verificar status de autenticação com `npx netlify status`
2. Se não autenticado, guiar usuário através de `npx netlify login`
3. Falhar graciosamente se a autenticação não puder ser estabelecida

A autenticação usa:
- **OAuth baseado em navegador** (primário): `netlify login` abre navegador para autenticação
- **API Key** (alternativa): Defina variável de ambiente `NETLIFY_AUTH_TOKEN`

## Fluxo de Trabalho

### 1. Verificar Autenticação na Netlify CLI

Verifique se o usuário está logado no Netlify:

```bash
npx netlify status
```

**Padrões de saída esperados**:
- ✅ Autenticado: Mostra email do usuário logado e status de vinculação do site
- ❌ Não autenticado: "Not logged into any site" ou erro de autenticação

**Se não autenticado**, guie o usuário:

```bash
npx netlify login
```

Isso abre uma janela do navegador para autenticação OAuth. Aguarde o usuário concluir o login e verifique novamente com `netlify status`.

**Autenticação alternativa: API Key**

Se a autenticação do navegador não estiver disponível, usuários podem definir:

```bash
export NETLIFY_AUTH_TOKEN=seu_token_aqui
```

Tokens podem ser gerados em: https://app.netlify.com/user/applications#personal-access-tokens

### 2. Detectar Status de Vinculação do Site

A partir da saída de `netlify status`, determine:
- **Vinculado**: Site já conectado ao Netlify (mostra nome/URL do site)
- **Não vinculado**: Precisa vincular ou criar site

### 3. Vincular a Site Existente ou Criar Novo

**Se já vinculado** → Vá para passo 4

**Se não vinculado**, tente vincular pela origem Git:

```bash
# Verifique se o projeto é baseado em Git
git remote show origin

# Se baseado em Git, extraia URL remota
# Formato: https://github.com/usuario/repo ou git@github.com:usuario/repo.git

# Tente vincular pela origem Git
npx netlify link --git-remote-url <URL_REMOTA>
```

**Se a vinculação falhar** (site não existe no Netlify):

```bash
# Criar novo site interativamente
npx netlify init
```

Isso guia o usuário através de:
1. Escolha de time/conta
2. Definição de nome do site
3. Configuração de settings de build
4. Criação de netlify.toml se necessário

### 4. Verificar Dependências

Antes de fazer deploy, garanta que as dependências do projeto estão instaladas:

```bash
# Para projetos npm
npm install

# Para outros gerenciadores de pacotes, detecte e use comando apropriado
# yarn install, pnpm install, etc.
```

### 5. Deploy para Netlify

Escolha tipo de deployment baseado no contexto:

**Deploy de Preview/Rascunho** (padrão para sites existentes):

```bash
npx netlify deploy
```

Isso cria um deploy preview com URL única para testes.

**Deploy de Produção** (para novos sites ou deploys de produção explícitos):

```bash
npx netlify deploy --prod
```

Isso faz deploy para a URL de produção ativa.

**Processo de deployment**:
1. CLI detecta settings de build (de netlify.toml ou solicita ao usuário)
2. Compila o projeto localmente
3. Envia assets compilados ao Netlify
4. Retorna URL do deployment

### 6. Relatar Resultados

Após deployment, reporte ao usuário:
- **URL de Deploy**: URL única para este deployment
- **URL do Site**: URL de produção (se deployment de produção)
- **Logs de Deploy**: Link para dashboard do Netlify para logs
- **Próximos passos**: Sugira `netlify open` para visualizar site ou dashboard

## Tratamento de netlify.toml

Se um arquivo `netlify.toml` existir, a CLI o usará automaticamente. Se não, a CLI solicitará:
- **Comando de build**: ex., `npm run build`, `next build`
- **Diretório de publicação**: ex., `dist`, `build`, `.next`

Padrões comuns de framework:
- **Next.js**: comando de build `npm run build`, publicar `.next`
- **React (Vite)**: comando de build `npm run build`, publicar `dist`
- **HTML Estático**: sem comando de build, publicar diretório atual

O skill deve detectar framework a partir de `package.json` se possível e sugerir settings apropriadas.

## Exemplo de Fluxo Completo

```bash
# 1. Verificar autenticação
npx netlify status

# Se não autenticado:
npx netlify login

# 2. Vincular site (se necessário)
# Tente vinculação baseada em Git primeiro
git remote show origin
npx netlify link --git-remote-url https://github.com/usuario/repo

# Se nenhum site existe, criar novo:
npx netlify init

# 3. Instalar dependências
npm install

# 4. Deploy (preview para teste)
npx netlify deploy

# 5. Deploy para produção (quando pronto)
npx netlify deploy --prod
```

## Tratamento de Erros

Problemas comuns e soluções:

**"Not logged in"**
→ Execute `npx netlify login`

**"No site linked"**
→ Execute `npx netlify link` ou `npx netlify init`

**"Build failed"**
→ Verifique comando de build e diretório de publicação em netlify.toml ou prompts da CLI
→ Verifique se dependências estão instaladas
→ Revise logs de build para erros específicos

**"Publish directory not found"**
→ Verifique se comando de build executou com sucesso
→ Verifique se caminho do diretório de publicação está correto

## Solução de Problemas

### Acesso de Rede Escalado

Se o deployment falhar por problemas de rede (timeouts, erros DNS, reset de conexão), execute novamente o deploy com permissões escaladas (use `sandbox_permissions=require_escalated`). O deploy requer acesso de rede escalado quando a sandbox bloqueia requisições de saída.

Exemplo de orientação ao usuário:

```
O deploy precisa de acesso de rede escalado para fazer deploy no Netlify. Posso executar o comando novamente com permissões escaladas—quer que eu prossiga?
```

## Variáveis de Ambiente

Para secrets e configuração:

1. Nunca faça commit de secrets no Git
2. Defina no dashboard do Netlify: Site Settings → Environment Variables
3. Acesse em builds via `process.env.VARIABLE_NAME`

## Dicas

- Use `netlify deploy` (sem `--prod`) primeiro para testar antes de produção
- Execute `netlify open` para visualizar site no dashboard do Netlify
- Execute `netlify logs` para visualizar logs de função (se usando Netlify Functions)
- Use `netlify dev` para desenvolvimento local com Netlify Functions

## Referência

- Docs Netlify CLI: https://docs.netlify.com/cli/get-started/
- Referência netlify.toml: https://docs.netlify.com/configure-builds/file-based-configuration/

## Referências Agrupadas (Carregue Conforme Necessário)

- [CLI commands](references/cli-commands.md)
- [Deployment patterns](references/deployment-patterns.md)
- [netlify.toml guide](references/netlify-toml.md)