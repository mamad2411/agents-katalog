# Checklist — Servidores (Sysadmin)

Checklist **incrementável** para varredura e manutenção de infraestrutura. O `sysadmin` marca cada item na execução e anexa evidência sanitizada na task quando abrir issue.

> Este checklist é do **próprio sysadmin** (SO, runtime, pacotes, SSH/FTP, disco, serviços).  
> Problemas de código de produto → use `checklist-system-dev.md` e tag `agent:developer`.

## 0. Preparação

- [ ] Carregar credenciais **SSH** e, se existirem, **FTP/SFTP** a partir da fonte operacional (banco / secrets) **sem** expô-las em issue, log ou chat
- [ ] Listar **todas** as máquinas/credenciais disponíveis na fonte e marcar quais serão verificadas nesta passagem
- [ ] Confirmar ambiente (prod / staging / lab) e janela segura de inspeção
- [ ] Registrar inventário desta execução: hostname, IP/alias, papel (app, db, proxy, worker…)

## 1. Acesso e inventário remoto

- [ ] Testar conectividade **SSH** em cada host listado na fonte de credenciais
- [ ] Testar **FTP/SFTP** quando a credencial existir (path de logs/arquivos)
- [ ] Anotar hosts inacessíveis (timeout, auth fail, host key) e abrir task `agent:sysadmin` se for falha real
- [ ] Confirmar usuário, porta e jump host corretos por máquina
- [ ] Verificar se há hosts órfãos na fonte (credencial sem máquina) ou máquinas sem credencial

## 2. Saúde básica do host

- [ ] Uptime e carga (`load average`)
- [ ] CPU: processos top consumidores
- [ ] Memória / swap
- [ ] Disco: uso de partições, inodes, volumes críticos (`/`, `/var`, logs, backups)
- [ ] Serviços essenciais no ar (nginx/caddy, php-fpm, node, mysql/postgres, redis, queue workers, docker… conforme o papel do host)
- [ ] Relógio/NTP razoável (skew que quebre TLS/certs)

## 3. Versões e patches (SO e runtime)

- [ ] Versão do SO e status de atualizações de segurança pendentes
- [ ] Kernel e necessidade de reboot pós-patch
- [ ] Runtime da aplicação no host (PHP, Node, Python, Java…) — versão instalada vs esperada
- [ ] Servidor web / reverse proxy — versão e módulos críticos
- [ ] Banco de dados no host (se aplicável) — versão e patch level
- [ ] Docker / container runtime (se aplicável) — versão e imagens base desatualizadas
- [ ] Certificados TLS: validade, cadeia, renovação (Let’s Encrypt / interno)
- [ ] Pacotes com CVE conhecidos ou `apt/yum` security updates pendentes

## 4. Bibliotecas e dependências de sistema

- [ ] Pacotes de sistema desatualizados relevantes ao stack
- [ ] Extensões PHP / módulos nativos críticos
- [ ] Bibliotecas compartilhadas (`ldd` / package manager) com alerta de segurança
- [ ] Ferramentas CLI operacionais (composer, npm, awscli…) — presença e versão mínima

> **Atenção:** desatualização de **dependência de código** no repositório Git (`package.json`, `composer.json`) é task `agent:developer` + `checklist-system-dev.md`. Desatualização **instalada no servidor** (pacote SO / runtime do host) permanece neste checklist + `agent:sysadmin`.

## 5. Logs — aplicação e infraestrutura

### Aplicação (produto)

- [ ] Consultar tabela **`logs`** no banco (filtros de tenant/ambiente/período)
- [ ] Consultar API **`/logs`** quando disponível (mesma família de eventos, filtros da API)
- [ ] Correlacionar erros recorrentes / stacks com possível causa de app → issue `agent:developer` se for bug de produto

### Host e webserver

- [ ] Logs do sistema via SSH (`journalctl`, `/var/log/syslog`, auth)
- [ ] Logs do **webserver** (access/error: nginx, Apache, Caddy…) via **SSH** e/ou **FTP/SFTP**
- [ ] 5xx, upstream timeout, falhas de vhost
- [ ] Logs de banco / redis / fila no host
- [ ] Rotação de logs funcionando (tamanho explosivo = incidente)
- [ ] Tentativas de autenticação anômalas (SSH brute force)

## 6. Rede e exposição

- [ ] Portas abertas vs esperado
- [ ] Firewall / security groups coerentes
- [ ] DNS e healthchecks externos (quando couber)
- [ ] Espaço e retenção de backup (se o host for responsável)

## 7. Encerramento da passagem de servidor

- [ ] Resumo por host: OK / ATTENTION / FAIL
- [ ] Fontes de log usadas registradas (`logs` DB, `/logs`, SSH, FTP/webserver)
- [ ] Para cada FAIL/ATTENTION: issue criada com label adequada, evidência sanitizada e item(ns) deste checklist citados
- [ ] Credenciais e saídas sensíveis **não** foram coladas na issue
- [ ] Inventário de hosts verificados vs hosts na fonte de credenciais (cobertura %)

## Itens futuros (backlog do checklist)

_Adicionar aqui novos itens conforme a operação evoluir:_

- [ ] _(vazio — incrementar)_ 
