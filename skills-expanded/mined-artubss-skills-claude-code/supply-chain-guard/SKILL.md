---
name: supply-chain-guard
description: "Detecte e remedeie ataques na cadeia de suprimentos de software em npm, PyPI, crates.io, GitHub Actions e pipelines de CI/CD, verificando pacotes comprometidos conhecidos, versões maliciosas, IOCs de sistema de arquivos, indicadores de C2 e configurações incorretas de CI/CD."
metadata:
  author: dan-avila
  version: '1.0'
  ioc-db-date: '2026-03-31'
---

# Supply Chain Guard

Detecção e remediação automatizadas de ataques na cadeia de suprimentos de software em npm, PyPI, crates.io, GitHub Actions e pipelines de CI/CD. Criado a partir de inteligência de ataques coletada do mundo real até 31 de março de 2026.

## Quando Usar Esta Skill

Use esta skill quando:

- O usuário solicita auditoria de dependências de um projeto quanto a problemas de segurança
- Antes de fazer deploy de código para produção
- Ao investigar um possível comprometimento da cadeia de suprimentos
- Quando o usuário menciona um ataque recente na cadeia de suprimentos e quer verificar seus projetos
- Como verificação de segurança regular em fluxos de desenvolvimento
- Ao configurar pipelines de CI/CD e querer endurecê-los
- Quando um novo ataque na cadeia de suprimentos é reportado e o usuário quer verificar exposição

## Instruções

### Etapa 1: Entenda o Projeto

Identifique o que o projeto do usuário utiliza:
- **Node.js/npm**: Procure por `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- **Python/PyPI**: Procure por `requirements.txt`, `Pipfile`, `pyproject.toml`, `poetry.lock`
- **Rust/crates.io**: Procure por `Cargo.toml`, `Cargo.lock`
- **CI/CD**: Procure por `.github/workflows/`, `Dockerfile`, `docker-compose.yml`

### Etapa 2: Execute os Scanners Apropriados

A skill inclui três scanners especializados mais um executor unificado. Todos os scripts estão no diretório `scripts/`.

**Auditoria completa (recomendado):**
```bash
bash /path/to/supply-chain-guard/scripts/scan-all.sh /path/to/project
```

**Scanners individuais:**
```bash
# Projetos npm/Node.js
bash /path/to/supply-chain-guard/scripts/scan-npm.sh /path/to/project

# Projetos Python/PyPI
bash /path/to/supply-chain-guard/scripts/scan-python.sh /path/to/project

# Auditoria de pipeline de CI/CD
bash /path/to/supply-chain-guard/scripts/scan-ci.sh /path/to/project
```

Cada scanner verifica:
1. **Pacotes comprometidos conhecidos** — correspondências exatas com o banco de dados de IOC
2. **Versões maliciosas** — números de versão específicos que se sabe conterem malware
3. **IOCs de sistema de arquivos** — mecanismos de persistência deixados por atacantes
4. **IOCs de rede** — domínios C2 e IPs no código-fonte
5. **Configurações incorretas de CI/CD** — ações sem versão fixa, gatilhos perigosos, segredos expostos
6. **Exposição de credenciais** — tokens npm, credenciais PyPI, arquivos .env

### Etapa 3: Interprete Resultados

Os scanners saem com o número de problemas encontrados (0 = limpo). Os problemas são categorizados:

- **[CRITICAL]** — Pacote malicioso conhecido ou IOC ativo detectado. Ação imediata necessária.
- **[WARNING]** — Preocupação de segurança que precisa investigação. Pode não ser um comprometimento ativo.

### Etapa 4: Remedeie

Com base nos achados, guie o usuário pela remediação:

#### Se um pacote comprometido for encontrado:
1. Remova ou faça downgrade para uma versão conhecida como segura imediatamente
2. Limpe os caches de pacotes: `npm cache clean --force` / `pip cache purge`
3. Delete `node_modules` / `.venv` e reinstale a partir do lockfile
4. Rotate TODAS as credenciais que estavam acessíveis a partir do ambiente

#### Se IOCs de sistema de arquivos forem encontrados:
1. O sistema deve ser tratado como **totalmente comprometido**
2. Identifique e remova mecanismos de persistência (serviços systemd, arquivos .pth, jobs cron)
3. Rotate todas as credenciais no sistema
4. Audite logs do provedor de nuvem (AWS CloudTrail, GCP Audit Logs, Azure Activity Log)
5. Verifique movimento lateral em clusters Kubernetes
6. Considere fazer reimage da máquina

#### Se problemas de CI/CD forem encontrados:
1. Fixe todas as GitHub Actions em SHAs de commit completo (nunca tags de versão)
2. Adicione `--ignore-scripts` aos comandos npm install/ci
3. Adicione `--require-hashes` aos comandos pip install
4. Remova ou proteja gatilhos `pull_request_target`
5. Aplique permissões de privilégio mínimo aos tokens de workflow
6. Audite logs de execução de pipeline durante os períodos da janela de ataque

### Etapa 5: Endurecça o Projeto

Após remediação, recomende estas medidas preventivas:

1. **Fixe tudo**: Pins de versão exata + lockfiles commitados no repo
2. **Verifique hash**: Use `npm ci` (não `npm install`), `pip install --require-hashes`
3. **Desabilite scripts**: Use `--ignore-scripts` por padrão, habilite apenas para pacotes confiáveis
4. **Fixe actions**: Todas as GitHub Actions fixadas em SHA completo, nunca tags
5. **Escopo de tokens**: Tokens de CI/CD devem ter permissões mínimas
6. **Monitore**: Configure verificação automatizada de dependências (mas verifique se o próprio scanner não está comprometido — veja incidente Trivy)
7. **Controles de rede**: Bloqueie domínios/IPs C2 conhecidos no firewall
8. **Audite regularmente**: Execute este scanner antes de cada deployment

## Arquivos de Referência

- `references/ioc-database.md` — Banco de dados completo de IOC com todos os pacotes comprometidos, versões maliciosas, infraestrutura C2, indicadores de sistema de arquivos e linhas do tempo de ataque. Leia este arquivo para inteligência detalhada sobre ataques específicos.

## Cenário Atual de Ameaças (a partir de 31 de março de 2026)

### Campanha Ativa: TeamPCP (CRÍTICO)

A ameaça ativa mais significativa. TeamPCP está executando uma campanha em cascata de cadeia de credenciais:
- Trivy (scanner de segurança) comprometido → roubou segredos de CI/CD de milhares de pipelines
- Usou tokens npm roubados para fazer deploy de CanisterWorm em 141+ pacotes npm
- Usou tokens PyPI roubados para fazer backdoor em LiteLLM (95M downloads mensais) e Telnyx
- Usa blockchain (ICP) para C2, tornando desativação impossível
- Faz deploy de esteganografia WAV para entrega de payload
- Tem como alvo Kubernetes para movimento lateral
- Possui variante destrutiva que apaga sistemas iranianos

### Ativo: Sequestro npm axios (31 de março de 2026)

- axios@1.14.1 e axios@0.30.4 contêm RAT dropper via dependência `plain-crypto-js` falsa
- 300M+ downloads semanais torna isto extremamente impactante
- RAT cross-platform para macOS, Windows e Linux
- Conta de mantenedor comprometida (jasonsaayman)

### Recente: Crates Rust Maliciosas (fevereiro/março de 2026)

- 5 crates imitando utilitários de tempo em crates.io
- Roubam arquivos .env, credenciais AWS, chaves SSH
- Primeiro ataque significativo na cadeia de suprimentos focando ecossistema Rust

### Histórico mas Relevante: Shai-Hulud Worm

- Worm npm auto-replicante que comprometeu ~1000 pacotes
- Tem como alvo tokens npm para auto-propagação
- Fallback destrutivo: apaga diretório home se a exfiltração falhar

## Atualizando o Banco de Dados de IOC

Quando novos ataques na cadeia de suprimentos são reportados:

1. Procure pelos avisos mais recentes de Socket, Aikido, Endor Labs, Snyk, JFrog
2. Atualize `references/ioc-database.md` com novos pacotes, versões, domínios, IPs
3. Atualize os scripts do scanner com novas entradas de pacote nos arrays MALICIOUS_*
4. Atualize o `ioc-db-date` no frontmatter SKILL.md