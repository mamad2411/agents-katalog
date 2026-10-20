---
name: dev-env-hardening
version: 1.0.0
description: >
  Isola e endurece o ambiente local de desenvolvimento do setup ao build do artefato.
  Foca em resiliência contra falhas de rede, vazamento de secrets e corrupção de cache.
triggers:
  - "isolar ambiente local"
  - "hardening de dev"
  - "prevenir vazamento de variáveis"
  - "ambiente de dev seguro"
  - "setup resiliente"
  - "/hardening-dev"
---

# DEV ENV HARDENING — Ambientes locais inquebráveis e à prova de vazamento

> **Propósito**: Garantir que o processo de build local seja um sandbox impenetrável, reproduzível e resiliente, eliminando vazamentos de credenciais e "funciona na minha máquina" através de isolamento rigoroso e tratamento de falhas cirúrgico.

---

## Filosofia Central

1. **Zero Trust Local** — O host (sua máquina) é tratado como hostil. Na prática: secrets nunca tocam o disco em texto claro, mesmo localmente.
2. **Fail-Closed por Padrão** — Erros de infraestrutura interrompem o build imediatamente. Na prática: scripts abortam se variáveis obrigatórias ou checksums falharem, sem tentar adivinhar defaults.
3. **Imutabilidade de Dependências** — O estado do ambiente não pode ser alterado durante o build. Na prática: lockfiles (`package-lock.json`, `poetry.lock`) são montados no container como *read-only*.
4. **Reproducibilidade Host-Agnostic** — O build local deve ser bit-a-bit idêntico ao do CI. Na prática: imagens base fixadas por digest SHA256, nunca por tag flutuante.

---

## Quando Ativar

### ✅ Ativar para:
- Criar ou refatorar `Dockerfile`s, `docker-compose.yml` ou configurações de DevContainers.
- Escrever scripts de bootstrap/Makefiles para subir o ambiente de desenvolvimento.
- Auditar risco de vazamento de `.env` ou credenciais em logs de build.
- Implementar mecanismos de retry para installs de dependências com rede instável.

### ❌ NÃO ativar para:
- Configurar pipelines de CI/CD (GitHub Actions, GitLab CI) → use `ci-cd-setup`.
- Integrar com cofres de senhas corporativos (HashiCorp Vault, AWS Secrets) → use `secrets-management`.
- Otimizar performance de runtime da aplicação → responda diretamente com foco no perfilamento.

---

## Protocolo de Execução

1. **Validar Pré-requisitos de Host** — Executar checagens de disco, RAM e disponibilidade do daemon (Docker/Podman). Abortar com mensagem de erro amigável se faltar algo.
2. **Provisionar Secrets com Segurança** — Gerar `.env` local a partir de um `.env.example`. Aplicar permissões restritas (`chmod 600`) e validar que o arquivo está no `.gitignore`.
3. **Construir Imagem Isolada** — Fazer o build da imagem base usando digest SHA256. Rodar estágios de build como usuário não-root. Não permitir cache se arquivos de configuração mudaram.
4. **Executar Build com Resiliência** — Montar volumes de código como *read-only*. Implementar lógica de retry com *backoff exponencial* para downloads de pacotes (npm, pip, apt).
5. **Extrair Artefato Final** — Copiar o artefato compilado (binário, .zip, .jar) para um volume de saída dedicado. Forçar *chown* para o UID/GID do usuário do host. Invalidar caches sensíveis da memória.

---

## Padrões Específicos

### Padrão 1: Pinagem de Imagem Base por SHA256

**Regra**: Nunca use tags flutuantes (`:latest`, `:alpine`) em ambientes de hardening. Use sempre o digest.

```dockerfile
# ✅ PASS — Imutável e rastreável
FROM node:20-slim@sha256:1234abcd...na verdade use o sha real

# ❌ FAIL — Pode quebrar amanhã ou introduzir vulnerabilidade silenciosa
FROM node:20-slim
```

**Por que importa**: Tags são mutáveis apontadores. Um `docker build` hoje pode ter um resultado completamente diferente amanhã, quebrando a reprodução exata.

---

### Padrão 2: Montagem de Código como Read-Only

**Regra**: O container de build nunca deve ter permissão de escrita no código-fonte do host.

```yaml
# ✅ PASS (docker-compose.yml)
volumes:
  - .:/app:ro
  - node_modules:/app/node_modules # Cache isolado

# ❌ FAIL
volumes:
  - .:/app # Permite que o build polua o repositório local
```

**Por que importa**: Impede que ferramentas de build (compiladores, formatters) alterem acidentalmente arquivos no seu sistema de arquivos host, garantindo que o estado permaneça limpo.

---

### Padrão 3: Fail-Fast de Variáveis de Ambiente

**Regra**: O script de entrada deve validar a presença e o formato de secrets antes de iniciar qualquer operação pesada.

```bash
# ✅ PASS — Falha antes de gastar 2 minutos instalando dependências
set -euo pipefail

required_vars=("DATABASE_URL" "JWT_SECRET")
for var in "${required_vars[@]}"; do
  if [ -z "${!var:-}" ]; then
    echo "[ERRO FATAL] Variável obrigatória ausente: $var" >&2
    exit 1
  fi
done
echo "Secrets validados. Iniciando build..."

# ❌ FAIL — O app sobe, tenta conectar ao banco e crashes com stack trace confusa
npm run build
```

**Por que importa**: Econimiza tempo de debug e previne logs de erro que podem vazar parcialmente a estrutura do projeto ou conexões falhas para sistemas externos.

---

### Padrão 4: Resiliência de Rede com Backoff Exponencial

**Regra**: Downloads de pacotes em redes locais instáveis (VPN, Wi-Fi fraco) devem ter retry automático, mas com limite.

```bash
# ✅ PASS — Tenta 3 vezes, espera 5s, 10s, 20s
install_deps() {
  local max_attempts=3 delay=5
  for i in $(seq 1 $max_attempts); do
    if npm ci --ignore-scripts; then
      echo "Dependências instaladas com sucesso."
      return 0
    fi
    echo "Tentativa $i falhou. Aguardando ${delay}s..." >&2
    sleep $delay
    delay=$((delay * 2))
  done
  echo "[ERRO FATAL] Falha ao baixar dependências após $max_attempts tentativas." >&2
  return 1
}
install_deps

# ❌ FAIL — Falha na primeira queda de pacote e encerra o processo
npm install
```

**Por que importa**: Reduces false-negative failures no setup local, evitando que o desenvolvedor culpe o código quando o problema foi umaqueda de pacote de 500ms no registry.

---

### Padrão 5: Extração Segura de Artefatos (Chown)

**Regra**: Artefatos gerados dentro do container (que rodam como root por padrão no Docker) devem ser donos do usuário do host na saída.

```dockerfile
# ✅ PASS — Garante que o usuário não precise de 'sudo' para apagar o .zip
USER root
RUN chown -R 1000:1000 /app/dist
USER 1000
CMD ["cp", "-r", "/app/dist", "/output/"]

# ❌ FAIL — Gera arquivos como 'root' no host, forçando uso de 'sudo rm'
CMD ["cp", "-r", "/app/dist", "/output/"]
```

**Por que importa**: Arquivos de propriedade do `root` no host forçam o uso de `sudo` para limpeza, o que é um risco de segurança local e quebra fluxos automatizados de scripts.

---

## Anti-Padrões Críticos

| Anti-padrão | Consequência | Alternativa Correta |
| :--- | :--- | :--- |
| Usar `--env-file .env` no `docker run` de forma irrestrita | Todas as vars do arquivo vão para o container, incluindo vars de debug desnecessárias. | Passar variáveis explicitamente: `-e DATABASE_URL=$DATABASE_URL` |
| Fazer bind mount de `~/.aws` ou `~/.ssh` para o container | O container ganha acesso total às credenciais de infraestrutura do host. | Usar variáveis de ambiente de curta duração (OIDC) ou secrets managers. |
| Adicionar `--no-cache` permanentemente no Makefile | Destrói o cache de camadas, tornando builds diários extremamente lentos. | Invalidar cache seletivamente apenas nas etapas que baixam código (ex: `--build-arg CACHEBUST=$(date +%s)`). |
| Usar o usuário `root` no estágio final da imagem | Se houver RCE na aplicação, o atacante tem acesso total ao sistema de arquivos do container. | Criar usuário dedicado (`USER appuser`) no final do Dockerfile. |

---

## Critérios de Qualidade

Antes de entregar a configuração de ambiente, confirme:

- [ ] Frontmatter completo e triggers válidos aplicados.
- [ ] Imagem base pinada por hash SHA256 (`@sha256:...`).
- [ ] `.env.example` fornecido, validado no entrypoint e `.gitignore` garantido.
- [ ] Código-fonte montado como volume *read-only* (`:ro`).
- [ ] Scripts de shell usam `set -euo pipefail` para falha imediata.
- [ ] Lógica de retry implementada para downloads de pacotes/dependências.
- [ ] Artefato final tem ownership (`chown`) correto para o usuário do host.
- [ ] Nenhum estágio final do Dockerfile roda como `root`.
- [ ] Zero exposição de portas de debug (ex: 9229 do Node) em ambientes de build.

---

## Referências Cruzadas

| Precisa de... | Use a skill... |
| :--- | :--- |
| Subir essa lógica para nuvem (GitHub Actions) | `ci-cd-setup` |
| Integrar com AWS Secrets Manager / Vault | `secrets-management` |
| Escrever o Dockerfile de produção (multi-stage) | `container-build` |
| Lidar com permissões complexas de disco no host | `file-system-permissions` |
```

**Racional das escolhas de design**: Esta skill foi calibrada para atuar no nível de "Engenharia de Plataforma" aplicada ao dia a dia do desenvolvedor. Em vez de focar apenas em conceitos abstratos de segurança, o protocolo e os padrões abordam as falhas que efetivamente causam retrabalho: perda de permissão de arquivo no host (necessitando de `sudo`), falhas de build por quedas microscópicas de rede, e vazamento acidental de secrets por montagem grossa de `.env`. A imposição do uso de `set -euo pipefail` e pinagem por SHA256 garante que o ambiente atua como um verdadeiro sandbox determinístico. Recomenda-se salvar em `docs/ambients/dev-env-hardening.md`.