---
name: create-k8s
description: Gera manifestos Kubernetes para aplicações web seguindo boas práticas e convenções do projeto. Use esta skill sempre que o usuário pedir para criar, gerar, corrigir ou revisar manifestos Kubernetes — mesmo que não use esses termos exatos. Também use quando o usuário mencionar "subir no Kubernetes", "criar yamls do k8s", "configurar k8s", "deploiar no cluster", "criar deployment", "criar service", "preparar para o Kubernetes", ou qualquer variação que indique configuração de recursos Kubernetes para o projeto.
---

## O que esta skill faz

Gera um único arquivo YAML com todos os manifestos Kubernetes necessários para rodar a aplicação no cluster, usando o `docker-compose.yml` como fonte da verdade para identificar a aplicação e suas dependências externas. Ao final, exibe um resumo das decisões tomadas.

---

## Pré-condição obrigatória

**O projeto deve ter um `docker-compose.yml`.** Se não existir, pare imediatamente e oriente o usuário a criá-lo primeiro — ele é a fonte da verdade para mapear dependências externas da aplicação.

---

## Escopo

Esta skill cobre o padrão mais comum:

- **App web stateless** — qualquer linguagem, exposta via HTTP
- **Banco de dados relacional** — Postgres ou MySQL como dependência externa

Dependências não cobertas (Redis, RabbitMQ, etc.) devem ser mencionadas no resumo final como "fora do escopo".

---

## Regras obrigatórias

### 1. Arquivo único com separadores

Todos os manifestos ficam em um único arquivo `k8s/<nome-da-app>.yml`, separados por `---`. O nome do arquivo deve ser o nome da aplicação extraído do docker-compose.

### 2. Namespace com nome da aplicação

O namespace deve ser o **primeiro recurso** do arquivo. Para definir o nome:

1. Use o nome do serviço da app no docker-compose.
2. **Exceção:** se esse nome for genérico (`app`, `web`, `api`, `backend`, `server`, `frontend`), use o nome do diretório raiz do projeto — ele costuma ser mais descritivo e evita namespaces sem significado em clusters com múltiplas aplicações.

### 3. Ordem hierárquica obrigatória

A ordem dos recursos no YAML deve respeitar as dependências:

1. `Namespace`
2. `Secret` — credenciais do banco
3. `PersistentVolumeClaim` — volume do banco
4. `Deployment` do banco
5. `Service` do banco (ClusterIP interno)
6. `Deployment` da aplicação
7. `Service` da aplicação (LoadBalancer)

### 4. Namespace em todos os recursos

Todo recurso deve ter o namespace escolhido na regra 2 no campo `metadata.namespace`.

### 5. Credenciais sempre em Secret

Nunca coloque senhas ou usuários hardcoded em `env` de Deployment. Sempre referencie via `secretKeyRef` apontando para o Secret criado.

### 6. Imagens com tag explícita

Proibido usar `latest`. Use sempre a tag exata (ex: `postgres:15-alpine`, `mysql:8-debian`). Prefira imagens Alpine quando disponíveis.

### 7. PersistentVolumeClaim com subPath

O `volumeMount` do banco deve sempre usar `subPath: <nome-do-banco>-data` para evitar conflito com `lost+found` em sistemas de arquivos ext4. Defina `PGDATA` (Postgres) ou `MYSQL_DATADIR` (MySQL) apontando para o subdiretório.

**Postgres:**
```yaml
env:
  - name: PGDATA
    value: /var/lib/postgresql/data/pgdata
volumeMounts:
  - name: postgres-data
    mountPath: /var/lib/postgresql/data
    subPath: pgdata
```

**MySQL:**
```yaml
volumeMounts:
  - name: mysql-data
    mountPath: /var/lib/mysql
    subPath: mysql-data
```

### 8. Probes no banco de dados

Use `readinessProbe` para garantir que o banco está pronto antes da app conectar.

**Postgres:**
```yaml
readinessProbe:
  exec:
    command: ["pg_isready", "-U", "<usuario>", "-d", "<banco>"]
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 5
  failureThreshold: 5
```

**MySQL:**
```yaml
readinessProbe:
  exec:
    command: ["mysqladmin", "ping", "-h", "localhost", "-u", "<usuario>", "-p<senha>"]
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 5
  failureThreshold: 5
```

### 9. Probes na aplicação

A app deve ter `readinessProbe` e `livenessProbe`. Verifique se a aplicação expõe endpoints de health (ex: `/health`, `/ready`, `/healthz`, `/livez`). Se existirem, use-os. Se não existirem, use TCP socket na porta da aplicação como fallback.

**Com endpoints HTTP:**
```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: <porta>
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 3
livenessProbe:
  httpGet:
    path: /health
    port: <porta>
  initialDelaySeconds: 15
  periodSeconds: 10
  failureThreshold: 3
```

**Fallback TCP:**
```yaml
readinessProbe:
  tcpSocket:
    port: <porta>
  initialDelaySeconds: 10
  periodSeconds: 5
livenessProbe:
  tcpSocket:
    port: <porta>
  initialDelaySeconds: 15
  periodSeconds: 10
```

### 10. Service da aplicação como LoadBalancer

O Service da aplicação é sempre `type: LoadBalancer` na porta `80`, apontando para a porta interna da app. Nunca use `NodePort`.

---

## Processo de execução

1. **Verifique a pré-condição:** o docker-compose.yml existe? Se não, pare e oriente.
2. **Leia o docker-compose.yml:** identifique o serviço da aplicação, suas variáveis de ambiente, porta exposta e dependências externas (bancos, etc.).
3. **Leia o código da aplicação:** verifique se existem endpoints de health/readiness para configurar as probes.
4. **Verifique se já existe `k8s/`:** se existir arquivo de manifesto, leia e identifique violações às regras acima.
5. **Gere ou corrija:** crie o arquivo `k8s/<nome-da-app>.yml` do zero ou aplique as correções, sem pedir confirmação.
6. **Exiba o resumo.**

---

## Resumo final (sempre exibir)

```
## Decisões aplicadas

| Regra | Situação | Ação |
|---|---|---|
| Namespace | [nome utilizado] | [criado / já existia] |
| Arquivo único | k8s/<nome>.yml | [gerado / corrigido] |
| Credenciais | Secret: <nome> | [criado / já existia] |
| PVC + subPath | [banco detectado] | [ok / corrigido] |
| Imagens | [tags utilizadas] | [ok / corrigido] |
| Probes do banco | [tipo de probe] | [ok / criado] |
| Probes da app | [endpoints ou TCP] | [ok / criado] |
| Service da app | LoadBalancer porta 80 | [ok / corrigido] |
| Dependências fora do escopo | [lista ou "nenhuma"] | — |
```
