---
name: render-deploy
description: Implante aplicações no Render analisando bases de código, gerando Blueprints render.yaml e fornecendo deeplinks do Dashboard. Use quando o usuário deseja implantar, hospedar, publicar ou configurar sua aplicação na plataforma de nuvem do Render.
author: openai
---

# Implantar no Render

O Render suporta serviços **respaldados por Git** e serviços **com imagem Docker pré-construída**.

Esta habilidade cobre fluxos **respaldados por Git**:
1. **Método Blueprint** - Gere render.yaml para implantações Infrastructure-as-Code
2. **Criação Direta** - Crie serviços instantaneamente via ferramentas MCP

Blueprints também podem executar uma **imagem Docker pré-construída** usando `runtime: image`, mas o `render.yaml` ainda deve estar em um repositório Git.

Se não houver um remote Git, interrompa e peça ao usuário para:
- Criar/fazer push de um remote Git (pode ser mínimo se apenas o Blueprint for necessário), ou
- Usar o Dashboard/API do Render para implantar uma imagem Docker pré-construída (MCP não pode criar serviços com suporte de imagem).

## Pré-requisitos

- Quando a sandbox bloqueia as chamadas de rede de implantação, execute novamente com `sandbox_permissions=require_escalated`.
- A implantação pode levar alguns minutos. Use valores de timeout apropriados.

## Quando Usar Esta Habilidade

Ative esta habilidade quando os usuários desejam:
- Implantar uma aplicação no Render
- Criar um arquivo Blueprint render.yaml
- Configurar implantação do Render para seu projeto
- Hospedar ou publicar sua aplicação na plataforma de nuvem do Render
- Criar bancos de dados, trabalhos cron ou outros recursos do Render

## Caminho Feliz (Usuários Novos)

Use esta sequência de prompt curta antes da análise profunda para reduzir fricção:
1. Pergunte se desejam implantar a partir de um repositório Git ou de uma imagem Docker pré-construída.
2. Pergunte se o Render deve provisionar tudo o que a app precisa (com base no que parece provável da descrição do usuário) ou apenas a app enquanto trazem sua própria infra. Se as dependências não estiverem claras, faça um acompanhamento curto para confirmar se precisam de banco de dados, workers, cron ou outros serviços.

Então prossiga com o método apropriado abaixo.

## Escolha Seu Caminho de Origem

**Caminho de Repositório Git:** Obrigatório para Blueprint e Criação Direta. O repositório deve ser feito push para GitHub, GitLab ou Bitbucket.

**Caminho de Imagem Docker Pré-construída:** Suportado pelo Render via serviços com suporte de imagem. Isso **não** é suportado por MCP; use o Dashboard/API. Peça:
- URL da imagem (registry + tag)
- Autenticação do registry (se privado)
- Tipo de serviço (web/worker) e porta

Se o usuário escolher uma imagem Docker, guie-o pelo fluxo de implantação de imagem do Dashboard do Render ou peça para adicionar um remote Git (para que você possa usar um Blueprint com `runtime: image`).

## Escolha Seu Método de Implantação (Repositório Git)

Ambos os métodos exigem um repositório Git feito push para GitHub, GitLab ou Bitbucket. (Se usar `runtime: image`, o repositório pode ser mínimo e conter apenas `render.yaml`.)

| Método | Melhor Para | Vantagens |
|--------|-------------|-----------|
| **Blueprint** | Apps com múltiplos serviços, fluxos IaC | Controle de versão, reproduzível, suporta configurações complexas |
| **Criação Direta** | Serviços únicos, implantações rápidas | Criação instantânea, nenhum arquivo render.yaml necessário |

### Heurística de Seleção de Método

Use esta regra de decisão por padrão, a menos que o usuário solicite um método específico. Analise a base de código primeiro; pergunte apenas se a intenção de implantação for pouco clara (p. ex., DB, workers, cron).

**Use Criação Direta (MCP) quando TODOS forem verdadeiros:**
- Serviço único (uma app web ou um site estático)
- Sem serviços worker/cron separados
- Sem bancos de dados ou Key Value anexados
- Apenas vars de env simples (sem grupos de env compartilhados)
Se este caminho se encaixa e MCP ainda não está configurado, interrompa e guie a configuração do MCP antes de prosseguir.

**Use Blueprint quando QUALQUER FOR verdadeiro:**
- Múltiplos serviços (web + worker, API + frontend, etc.)
- Bancos de dados, Redis/Key Value ou outros datastores são necessários
- Trabalhos cron, workers em background ou serviços privados
- Você quer IaC reproduzível ou um render.yaml commitado no repositório
- Monorepo ou configuração multi-env que precisa de configuração consistente

Se incerto, faça uma pergunta de esclarecimento rápida, mas padrão para Blueprint por segurança. Para um serviço único, prefira fortemente Criação Direta via MCP e guie a configuração do MCP se necessário.

## Verificação de Pré-requisitos

Ao iniciar uma implantação, verifique esses requisitos em ordem:

**1. Confirme Caminho de Origem (Git vs Docker)**

Se usar métodos baseados em Git (Blueprint ou Criação Direta), o repositório deve ser feito push para GitHub/GitLab/Bitbucket. Blueprints que referenciam uma imagem pré-construída ainda exigem um repositório Git com `render.yaml`.

```bash
git remote -v
```

- Se nenhum remote existir, interrompa e peça ao usuário para criar/fazer push de um remote **ou** mudar para implantação de imagem Docker.

**2. Verifique Disponibilidade de Ferramentas MCP (Preferido para Serviço Único)**

As ferramentas MCP fornecem a melhor experiência. Verifique se estão disponíveis tentando:
```
list_services()
```

Se as ferramentas MCP estiverem disponíveis, você pode pular a instalação do CLI para a maioria das operações.

**3. Verifique Instalação do Render CLI (para validação do Blueprint)**
```bash
render --version
```
Se não estiver instalado, ofereça para instalar:
- macOS: `brew install render`
- Linux/macOS: `curl -fsSL https://raw.githubusercontent.com/render-oss/cli/main/bin/install.sh | sh`

**4. Configuração MCP (se MCP não estiver configurado)**

Se `list_services()` falhar porque MCP não está configurado, pergunta se desejam configurar MCP (preferido) ou continuar com fallback do CLI. Se escolherem MCP, pergunte qual ferramenta de IA estão usando, depois forneça as instruções correspondentes abaixo. Sempre use a chave API deles.

### Cursor

Caminhe o usuário através destas etapas:

1) Obtenha uma chave API do Render:
```
https://dashboard.render.com/u/*/settings#api-keys
```

2) Adicione isto a `~/.cursor/mcp.json` (substitua `<YOUR_API_KEY>`):
```json
{
  "mcpServers": {
    "render": {
      "url": "https://mcp.render.com/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_API_KEY>"
      }
    }
  }
}
```

3) Reinicie o Cursor, depois tente novamente `list_services()`.

### Claude Code

Caminhe o usuário através destas etapas:

1) Obtenha uma chave API do Render:
```
https://dashboard.render.com/u/*/settings#api-keys
```

2) Adicione o servidor MCP com Claude Code (substitua `<YOUR_API_KEY>`):
```bash
claude mcp add --transport http render https://mcp.render.com/mcp --header "Authorization: Bearer <YOUR_API_KEY>"
```

3) Reinicie o Claude Code, depois tente novamente `list_services()`.

### Codex

Caminhe o usuário através destas etapas:

1) Obtenha uma chave API do Render:
```
https://dashboard.render.com/u/*/settings#api-keys
```

2) Defina-a no seu shell:
```bash
export RENDER_API_KEY="<YOUR_API_KEY>"
```

3) Adicione o servidor MCP com a CLI do Codex:
```bash
codex mcp add render --url https://mcp.render.com/mcp --bearer-token-env-var RENDER_API_KEY
```

4) Reinicie o Codex, depois tente novamente `list_services()`.

### Outras Ferramentas

Se o usuário estiver em outra app de IA, direcione-o para a documentação MCP do Render para etapas de configuração e método de instalação dessa ferramenta.

### Seleção de Workspace

Após MCP estar configurado, peça ao usuário para definir o workspace ativo do Render com um prompt como:

```
Defina meu workspace do Render para [WORKSPACE_NAME]
```

**5. Verifique Autenticação (fallback do CLI apenas)**

Se MCP não estiver disponível, use a CLI em vez disso e verifique se você pode acessar sua conta:
```bash
# Verifique se o usuário está conectado (use -o json para modo não interativo)
render whoami -o json
```

Se `render whoami` falhar ou retornar dados vazios, a CLI não está autenticada. A CLI nem sempre solicitará automaticamente, então solicite explicitamente ao usuário que se autentique:

Se nenhum estiver configurado, pergunte ao usuário qual método prefere:
- **Chave API (CLI)**: `export RENDER_API_KEY="rnd_xxxxx"` (Obtenha em https://dashboard.render.com/u/*/settings#api-keys)
- **Login**: `render login` (Abre navegador para OAuth)

**6. Verifique Contexto do Workspace**

Verifique o workspace ativo:
```
get_selected_workspace()
```

Ou via CLI:
```bash
render workspace current -o json
```

Para listar workspaces disponíveis:
```
list_workspaces()
```

Se o usuário precisar mudar de workspaces, ele deve fazer isso via Dashboard ou CLI (`render workspace set`).

Depois que os pré-requisitos forem atendidos, prossiga com o fluxo de trabalho de implantação.

---

# Método 1: Implantação Blueprint (Recomendado para Apps Complexas)

## Fluxo de Trabalho do Blueprint

### Passo 1: Analise a Base de Código

Analise a base de código para determinar framework/runtime, comandos de build e start, vars de env necessárias, datastores e vinculação de porta. Use as listas de verificação detalhadas em [references/codebase-analysis.md](references/codebase-analysis.md).

### Passo 2: Gere render.yaml

Crie um arquivo Blueprint `render.yaml` seguindo a especificação do Blueprint.

Especificação completa: [references/blueprint-spec.md](references/blueprint-spec.md)

**Pontos-chave:**
- Sempre use `plan: free` a menos que o usuário especifique o contrário
- Inclua TODAS as variáveis de env que a app precisa
- Marque secrets com `sync: false` (usuário preenche no Dashboard)
- Use tipo de serviço apropriado: `web`, `worker`, `cron`, `static` ou `pserv`
- Use runtime apropriado: [references/runtimes.md](references/runtimes.md)

**Estrutura Básica:**
```yaml
services:
  - type: web
    name: my-app
    runtime: node
    plan: free
    buildCommand: npm ci
    startCommand: npm start
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: postgres
          property: connectionString
      - key: JWT_SECRET
        sync: false  # Usuário preenche no Dashboard

databases:
  - name: postgres
    databaseName: myapp_db
    plan: free
```

**Tipos de Serviço:**
- `web`: Serviços HTTP, APIs, aplicações web (publicamente acessíveis)
- `worker`: Processadores de trabalhos em background (não publicamente acessíveis)
- `cron`: Tarefas agendadas que executam em cronograma cron
- `static`: Sites estáticos (HTML/CSS/JS servidos via CDN)
- `pserv`: Serviços privados (apenas internos, dentro da mesma conta)

Detalhes dos tipos de serviço: [references/service-types.md](references/service-types.md)
Opções de runtime: [references/runtimes.md](references/runtimes.md)
Exemplos de template: [assets/](assets/)

### Passo 2.5: Próximos Passos Imediatos (Sempre Forneça)

Após criar `render.yaml`, sempre dê ao usuário uma checklist curta e explícita e execute validação imediatamente quando o CLI estiver disponível:
1. **Autentique (CLI)**: execute `render whoami -o json` (se não conectado, execute `render login` ou defina `RENDER_API_KEY`)
2. **Valide (recomendado)**: execute `render blueprints validate`
   - Se a CLI não estiver instalada, ofereça para instalar e forneça o comando.
3. **Commit + push**: `git add render.yaml && git commit -m "Add Render deployment configuration" && git push origin main`
4. **Abra Dashboard**: Use o deeplink do Blueprint e complete OAuth do Git se solicitado
5. **Preencha secrets**: Defina vars de env marcadas com `sync: false`
6. **Implante**: Clique "Apply" e monitore a implantação

### Passo 3: Valide a Configuração

Valide o arquivo render.yaml para capturar erros antes da implantação. Se a CLI estiver instalada, execute os comandos diretamente; apenas solicite ao usuário se a CLI estiver ausente:

```bash
render whoami -o json  # Garanta que a CLI está autenticada (nem sempre solicitará)
render blueprints validate
```

Corrija quaisquer erros de validação antes de prosseguir. Problemas comuns:
- Campos obrigatórios faltando (`name`, `type`, `runtime`)
- Valores de runtime inválidos
- Sintaxe YAML incorreta
- Referências de variável de env inválidas

Guia de configuração: [references/configuration-guide.md](references/configuration-guide.md)

### Passo 4: Commit e Push

**IMPORTANTE:** Você deve fazer merge do arquivo `render.yaml` no seu repositório antes de implantar.

Garanta que o arquivo `render.yaml` seja commitado e feito push para seu remote Git:

```bash
git add render.yaml
git commit -m "Add Render deployment configuration"
git push origin main
```

Se não houver remote Git ainda, interrompa aqui e guie o usuário para criar um repositório GitHub/GitLab/Bitbucket, adicionar como `origin` e fazer push antes de continuar.

**Por que isto importa:** O deeplink do Dashboard lerá o render.yaml do seu repositório. Se o arquivo não estiver mergeado e feito push, o Render não encontrará a configuração e a implantação falhará.

Verifique se o arquivo está no seu repositório remoto antes de prosseguir para o próximo passo.

### Passo 5: Gere Deeplink

Obtenha a URL do repositório Git:

```bash
git remote get-url origin
```

Isto retornará uma URL do seu provedor Git. **Se a URL estiver em formato SSH, converta para HTTPS:**

| Formato SSH | Formato HTTPS |
|-------------|---------------|
| `git@github.com:user/repo.git` | `https://github.com/user/repo` |
| `git@gitlab.com:user/repo.git` | `https://gitlab.com/user/repo` |
| `git@bitbucket.org:user/repo.git` | `https://bitbucket.org/user/repo` |

**Padrão de conversão:** Substitua `git@<host>:` por `https://<host>/` e remova o sufixo `.git`.

Formate o deeplink do Dashboard usando a URL do repositório HTTPS:
```
https://dashboard.render.com/blueprint/new?repo=<REPOSITORY_URL>
```

Exemplo:
```
https://dashboard.render.com/blueprint/new?repo=https://github.com/username/repo-name
```

### Passo 6: Guie o Usuário

**CRÍTICO:** Garanta que o usuário tenha mergeado e feito push do arquivo render.yaml para seu repositório antes de clicar no deeplink. Se o arquivo não estiver no repositório, o Render não pode ler a configuração do Blueprint e a implantação falhará.

Forneça o deeplink ao usuário com estas instruções:

1. **Verifique se render.yaml está mergeado** - Confirme se o arquivo existe no seu repositório no GitHub/GitLab/Bitbucket
2. Clique no deeplink para abrir o Dashboard do Render
3. Complete OAuth do provedor Git se solicitado
4. Nomeie o Blueprint (ou use padrão do render.yaml)
5. Preencha variáveis de env secretas (marcadas com `sync: false`)
6. Revise a configuração de serviços e bancos de dados
7. Clique "Apply" para implantar

A implantação começará automaticamente. Os usuários podem monitorar progresso no Dashboard do Render.

### Passo 7: Verifique a Implantação

Após o usuário implantar via Dashboard, verifique se tudo está funcionando.

**Verifique status de implantação via MCP:**
```
list_deploys(serviceId: "<service-id>", limit: 1)
```
Procure por `status: "live"` para confirmar implantação bem-sucedida.

**Verifique erros de runtime (aguarde 2-3 minutos após implantação):**
```
list_logs(resource: ["<service-id>"], level: ["error"], limit: 20)
```

**Verifique métricas de saúde do serviço:**
```
get_metrics(
  resourceId: "<service-id>",
  metricTypes: ["http_request_count", "cpu_usage", "memory_usage"]
)
```

Se erros forem encontrados, prossiga para a seção **Verificação pós-implantação e triagem básica** abaixo.

---

# Método 2: Criação de Serviço Direto (Implantações Rápidas de Serviço Único)

Para implantações simples sem Infrastructure-as-Code, crie serviços diretamente via ferramentas MCP.

## Quando Usar Criação Direta

- Serviço web único ou site estático
- Protótipos rápidos ou demos
- Quando você não precisa de arquivo render.yaml no seu repositório
- Adicionando bancos de dados ou trabalhos cron a projetos existentes

## Pré-requisitos para Criação Direta

**O repositório deve ser feito push para um provedor Git.** O Render clona seu repositório para compilar e implantar serviços.

```bash
git remote -v  # Verifique se remote existe
git push origin main  # Garanta que código está feito push
```

Provedores suportados: GitHub, GitLab, Bitbucket

Se nenhum remote existir, interrompa e peça ao usuário para criar/fazer push de um remote ou mudar para implantação de imagem Docker.

**Nota:** MCP não suporta criar serviços com suporte de imagem. Use o Dashboard/API para implantações de imagem Docker pré-construída.

## Fluxo de Trabalho de Criação Direta

Use os passos concisos abaixo e consulte [references/direct-creation.md](references/direct-creation.md) para exemplos completos de comandos MCP e configuração de acompanhamento.

### Passo 1: Analise a Base de Código
Use [references/codebase-analysis.md](references/codebase-analysis.md) para determinar runtime, comandos build/start, vars de env e datastores.

### Passo 2: Crie Recursos via MCP
Crie o serviço (web ou estático) e quaisquer bancos de dados ou key-value stores necessários. Veja [references/direct-creation.md](references/direct-creation.md).

Se MCP retornar um erro sobre credenciais Git faltando ou acesso ao repositório, interrompa e guie o usuário para conectar seu provedor Git no Dashboard do Render, depois tente novamente.

### Passo 3: Configure Variáveis de Ambiente
Adicione vars de env necessárias via MCP após criação. Veja [references/direct-creation.md](references/direct-creation.md).

Lembre o usuário de que secrets podem ser definidos no Dashboard se preferirem não passá-los via MCP.

### Passo 4: Verifique a Implantação
Verifique status de implantação, logs e métricas. Veja [references/direct-creation.md](references/direct-creation.md).

---

Para descoberta de serviço, detalhes de configuração, comandos rápidos e problemas comuns, veja [references/deployment-details.md](references/deployment-details.md).

---

# Verificação pós-implantação e triagem básica (Todos os Métodos)

Mantenha isto curto e repetível. Se qualquer verificação falhar, corrija antes de reimplantar.

1. Confirme se a implantação mais recente está `live` e servindo tráfego
2. Acesse o endpoint de saúde (ou root) e verifique resposta 200
3. Verifique logs de erro recentes para uma assinatura clara de falha
4. Verifique vars de env necessárias e vinculação de porta (`0.0.0.0:$PORT`)

Checklist detalhado e comandos: [references/post-deploy-checks.md](references/post-deploy-checks.md)

Se o serviço falhar ao iniciar ou health checks sofrem timeout, use o guia de triagem básica:
[references/troubleshooting-basics.md](references/troubleshooting-basics.md)

## Solução de Problemas

### Acesso de Rede Escalado

Se a implantação falhar devido a problemas de rede (timeouts, erros DNS, conexões resetadas), execute a implantação novamente com permissões escaladas (use `sandbox_permissions=require_escalated`). A implantação requer acesso de rede escalado quando a sandbox bloqueia requisições outbound.

Exemplo de orientação ao usuário:

```
A implantação precisa de acesso de rede escalado para implantar no Render. Posso executar o comando novamente com permissões escaladas—deseja que eu prossiga?
```

Opcional: Se você precisar de diagnósticos mais profundos (verificações de métricas/DB/catálogo de erros), sugira instalar a habilidade `render-debug`. Ela não é necessária para o fluxo de implantação principal.