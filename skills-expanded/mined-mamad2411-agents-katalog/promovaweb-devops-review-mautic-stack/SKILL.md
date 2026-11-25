---
name: promovaweb-devops-review-mautic-stack
description: Verifica a Stack do Mautic. Além disso analisa parâmetros, rotas Traefik, volumes, recursos e conformidade do stack Mautic de Acordo com as Recomendações da Promovaweb.
license: MIT
metadata:
  author: promovaweb
  version: "1.1"
---

# Review Mautic Stack

Executa uma auditoria completa do arquivo `mautic.yaml` e reporta conformidade, problemas e sugestões.

## Instruções de Execução

Quando esta skill for invocada, siga **exatamente** este roteiro:

### Passo 1 — Ler os arquivos

Leia o arquivo `mautic.yaml` completo. Leia também `mysql.yaml` para verificar a consistência das credenciais de banco.

### Passo 2 — Executar todos os checks abaixo

Execute cada bloco de verificação e registre os resultados (✅ OK / ⚠️ Atenção / ❌ Erro).

### Passo 3 — Gravar o resultado

Grave o relatório completo em um arquivo chamado mautic.audit.md.

---

## Checks de Verificação

### 1. Variáveis de Ambiente Obrigatórias

Verifique se todas as variáveis abaixo estão definidas no anchor `x-mautic-db-config`:

**Banco de dados MySQL/Percona (`x-mautic-db-config`)**

- `MAUTIC_DB_HOST` — deve ser definido (padrão: `mysql`)
- `MAUTIC_DB_USER` — deve ser definido (não deve ser `root`)
- `MAUTIC_DB_PASSWORD` — deve existir e **não deve ser o placeholder `SENHA_MAUTIC`**, compare com a senha definida em `mysql.yaml`
- `MAUTIC_DB_NAME` — deve ser definido (padrão: `mautic`)

---

### 2. Serviços Obrigatórios

Verifique se todos estes serviços estão presentes:

| Serviço | Obrigatório |
|---|---|
| `mautic_web` | Sim |
| `mautic_cron` | Sim |
| `mautic_worker` | Sim |

---

### 3. Variáveis por Serviço

Verifique as variáveis específicas de cada serviço:

| Serviço | Variável | Valor Esperado |
|---|---|---|
| `mautic_web` | `DOCKER_MAUTIC_LOAD_TEST_DATA` | `"false"` (não carregar dados de teste em produção) |
| `mautic_cron` | `DOCKER_MAUTIC_ROLE` | `mautic_cron` |
| `mautic_worker` | `DOCKER_MAUTIC_ROLE` | `mautic_worker` |

Alertar se `DOCKER_MAUTIC_LOAD_TEST_DATA` não for `"false"` em produção.

---

### 4. Replicas dos Serviços

Verifique a quantidade de réplicas de cada serviço:

| Serviço | Réplicas Mínimas | Observação |
|---|---|---|
| `mautic_web` | 1 | Interface web principal |
| `mautic_cron` | 1 | Não deve ter mais de 1 (evita execuções duplicadas) |
| `mautic_worker` | 1 | Pode escalar para mais workers |

Alertar se `mautic_cron` tiver mais de 1 réplica (pode causar execuções duplicadas de cron jobs).

---

### 5. Rotas Traefik

Para o serviço `mautic_web`, verifique:

**Âncora de endereço (`x-mautic-app-url`):**

- A âncora `x-mautic-app-url` deve existir e conter um domínio válido (não placeholder como `mautic.agenciasynca.com.br`)
- O domínio na âncora **deve ser idêntico** ao domínio dentro de `Host(...)` na label `traefik.http.routers.mautic.rule`
- Se não forem iguais, reportar como ❌ Erro: inconsistência entre `x-mautic-app-url` e a regra Traefik

**Labels obrigatórias:**

- `traefik.enable=true`
- `traefik.swarm.network=network_swarm_public`
- `traefik.http.routers.mautic.rule` — deve conter `Host(...)` com domínio válido e coincidir com `x-mautic-app-url`
- `traefik.http.routers.mautic.entrypoints=websecure`
- `traefik.http.routers.mautic.tls.certresolver=letsencryptresolver`
- `traefik.http.routers.mautic.service=mautic`
- `traefik.http.services.mautic.loadbalancer.server.port=80`

**Regras:**

- `mautic_cron` e `mautic_worker` **não devem** ter labels Traefik (serviços de background)

---

### 6. Volumes Compartilhados

Verifique o anchor `x-mautic-volumes` e se todos os volumes são compartilhados entre todos os serviços:

| Volume | Caminho | Deve Ser Compartilhado |
|---|---|---|
| `mautic_config` | `/var/www/html/config` | Entre todos os serviços |
| `mautic_logs` | `/var/www/html/var/logs` | Entre todos os serviços |
| `mautic_media_files` | `/var/www/html/docroot/media/files` | Entre todos os serviços |
| `mautic_media_images` | `/var/www/html/docroot/media/images` | Entre todos os serviços |

Alertar se algum serviço não estiver usando o anchor `*mautic-volumes`.

---

### 7. Recursos dos Containers

Para cada serviço, verifique os limites de recursos:

| Serviço | CPU Mínimo | Memória Máxima |
|---|---|---|
| `mautic_web` | "1" | 1024M |
| `mautic_cron` | — | verificar se tem limits definidos |
| `mautic_worker` | — | verificar se tem limits definidos |

Alertar se `mautic_cron` ou `mautic_worker` não tiverem `resources.limits` definidos.

---

### 8. Configuração de Deploy

Para cada serviço, verifique:

- `mode: replicated` — todos devem ser `replicated`
- `placement.constraints` — deve incluir `node.role == manager`
- Verificar se há `update_config` com `order: start-first` e `failure_action: rollback` (recomendado)

---

### 9. Redes e Imagens

**Redes:**

- Todos os serviços devem estar na rede `network_swarm_public`
- A rede deve ser declarada como `external: true` na seção `networks:`

**Imagens:**

- Todos os serviços devem usar `*mautic-image` (anchor)
- Verificar se a imagem usa tag específica de versão em vez de `latest` (recomendado em produção)

---

### 10. Segurança

- `MAUTIC_DB_PASSWORD` não deve ser `SENHA_MAUTIC` (placeholder)
- `MAUTIC_DB_USER` não deve ser `root` (privilégio excessivo)
- `DOCKER_MAUTIC_LOAD_TEST_DATA` deve ser `"false"` em produção
- Verificar se o banco `mautic` existe no MySQL (usuário `mautic` com acesso apenas ao banco `mautic`)

---

## Formato do Relatório de Saída

Ao final, produza um relatório estruturado:

```
# Relatório de Auditoria — mautic.yaml
Data: <data atual>

## Resumo
- Total de checks: X
- ✅ OK: X
- ⚠️ Atenções: X
- ❌ Erros: X

## Resultados por Categoria

### 1. Variáveis de Ambiente
✅ MAUTIC_DB_HOST: definido como `mysql`
❌ MAUTIC_DB_PASSWORD: usando placeholder SENHA_MAUTIC — troque antes do deploy
...

### 2. Serviços
✅ mautic_web: presente
✅ mautic_cron: presente
✅ mautic_worker: presente

### 3. Variáveis por Serviço
✅ mautic_web: DOCKER_MAUTIC_LOAD_TEST_DATA=false
✅ mautic_cron: DOCKER_MAUTIC_ROLE=mautic_cron
...

### 4. Replicas
✅ mautic_cron: 1 réplica (sem risco de duplicação)
⚠️ mautic_worker: sem resource limits definidos
...

### 5. Rotas Traefik
✅ mautic_web: rota Host correta, TLS ok
✅ mautic_cron: sem Traefik (correto)
...

### 6. Volumes
✅ mautic_config: compartilhado entre todos os serviços
✅ mautic_media_files: compartilhado entre todos os serviços
...

### 7. Recursos
⚠️ mautic_cron: sem resource limits — recomendado definir
...

### 8. Deploy
⚠️ update_config não definido — recomendado configurar start-first e rollback
...

### 9. Redes e Imagens
⚠️ Imagem usando `latest` — considere fixar uma versão em produção
...

### 10. Segurança
❌ MAUTIC_DB_PASSWORD: placeholder SENHA_MAUTIC detectado
...

## Ações Recomendadas (por prioridade)

### Crítico (fazer antes do deploy)
1. ...

### Recomendado
1. ...

### Opcional
1. ...
```
