---
name: promovaweb-devops-review-mongodb-stack
description: Verifica a Stack do MongoDB. Além disso analisa parâmetros, rotas Traefik, volumes, recursos e conformidade do stack MongoDB de Acordo com as Recomendações da Promovaweb.
license: MIT
metadata:
  author: promovaweb
  version: "1.1"
---

# Review MongoDB Stack

Executa uma auditoria completa do arquivo `mongodb.yaml` e reporta conformidade, problemas e sugestões.

## Instruções de Execução

Quando esta skill for invocada, siga **exatamente** este roteiro:

### Passo 1 — Ler o arquivo

Leia o arquivo `mongodb.yaml` completo.

### Passo 2 — Executar todos os checks abaixo

Execute cada bloco de verificação e registre os resultados (✅ OK / ⚠️ Atenção / ❌ Erro).

### Passo 3 — Gravar o resultado

Grave o relatório completo em um arquivo chamado mongodb.audit.md.

---

## Checks de Verificação

### 1. Imagem

Verifique o anchor `x-mongodb-image`:

- A imagem deve ser `mongo:<versão>` com versão major fixada (ex: `mongo:7`, `mongo:6`)
- Alertar se estiver usando `mongo:latest` (versões major do MongoDB têm breaking changes e migrações de dados irreversíveis)
- Recomendado: fixar versão completa em produção (ex: `mongo:7.0`)

---

### 2. Variáveis de Ambiente

Verifique o anchor `x-mongodb-env`:

- `MONGO_INITDB_ROOT_USERNAME` — deve ser definido (padrão: `root`)
- `MONGO_INITDB_ROOT_PASSWORD` — deve existir e **não deve ser o placeholder `SENHA_ROOT`**
- Alertar se `MONGO_INITDB_ROOT_USERNAME` for `root` (recomendado usar nome menos óbvio em produção)
- Alertar se não houver banco e usuário específicos para cada aplicação

---

### 3. Serviço

Verifique se o serviço `mongodb` está presente e corretamente configurado.

---

### 4. Portas Expostas

- `27017:27017` — verificar se a porta está exposta externamente
- Alertar se a porta 27017 estiver exposta em produção (risco de segurança)
- Recomendar remoção da exposição de porta se acesso externo não for necessário

---

### 5. Volumes

Verifique se ambos os volumes estão configurados:

| Volume | Caminho | Obrigatório |
|---|---|---|
| `mongodb_data` | `/data/db` | Sim — dados principais |
| `mongodb_config` | `/data/configdb` | Sim — configurações |

- Ambos devem ser declarados como `external: true`
- Alertar se algum volume não for externo (dados perdidos em redeploy)

---

### 6. Réplicas

| Serviço | Réplicas Esperadas | Observação |
|---|---|---|
| `mongodb` | 1 | MongoDB standalone — não deve ter mais de 1 réplica sem configuração de Replica Set |

Alertar se houver mais de 1 réplica (pode causar corrupção de dados sem configuração de Replica Set adequada).

---

### 7. Recursos do Container

| Serviço | CPU Mínimo | Memória Máxima |
|---|---|---|
| `mongodb` | "1" | 1024M |

- Alertar se memória for inferior a 512M (MongoDB pode ser instável)
- Verificar se os limites são adequados para a carga esperada

---

### 8. Configuração de Deploy

- `mode: replicated` — deve ser `replicated`
- `placement.constraints` — deve incluir `node.role == manager`
- Verificar se há constraints adicionais de hostname para fixar o banco em um nó específico
- Verificar se há `update_config` com `failure_action: rollback`

---

### 9. Redes

- O serviço deve estar na rede `network_swarm_public`
- A rede deve ser declarada como `external: true`
- Hostname `mongodb` deve ser acessível pelos serviços dependentes via nome de serviço Docker Swarm

---

### 10. Segurança

- `MONGO_INITDB_ROOT_PASSWORD` não deve ser `SENHA_ROOT` (placeholder)
- Porta 27017 exposta externamente — alertar como risco
- Recomendado criar usuários dedicados por banco/aplicação (não usar root para acesso das aplicações)
- Verificar se a autenticação está habilitada por padrão (MONGO_INITDB_ROOT_USERNAME/PASSWORD habilita autenticação)

---

## Formato do Relatório de Saída

Ao final, produza um relatório estruturado:

```
# Relatório de Auditoria — mongodb.yaml
Data: <data atual>

## Resumo
- Total de checks: X
- ✅ OK: X
- ⚠️ Atenções: X
- ❌ Erros: X

## Resultados por Categoria

### 1. Imagem
⚠️ mongo:latest: versão não fixada — risco de breaking changes em atualizações
...

### 2. Variáveis de Ambiente
❌ MONGO_INITDB_ROOT_PASSWORD: usando placeholder SENHA_ROOT — troque antes do deploy
⚠️ Username root: considere usar nome menos óbvio em produção
...

### 3. Serviço
✅ mongodb: presente

### 4. Portas
⚠️ Porta 27017 exposta externamente — garanta que firewall está configurado
...

### 5. Volumes
✅ mongodb_data: volume externo configurado em /data/db
✅ mongodb_config: volume externo configurado em /data/configdb
...

### 6. Réplicas
✅ mongodb: 1 réplica (correto para standalone)
...

### 7. Recursos
✅ 1024M de memória configurada
...

### 8. Deploy
✅ node.role == manager: placement correto
⚠️ update_config não definido
...

### 9. Redes
✅ network_swarm_public: configurado como external
...

### 10. Segurança
❌ MONGO_INITDB_ROOT_PASSWORD: placeholder SENHA_ROOT detectado
⚠️ Porta 27017 exposta: certifique-se de que firewall bloqueia acesso externo
⚠️ Crie usuários dedicados por aplicação — não use root nas aplicações
...

## Ações Recomendadas (por prioridade)

### Crítico (fazer antes do deploy)
1. ...

### Recomendado
1. ...

### Opcional
1. ...
```
