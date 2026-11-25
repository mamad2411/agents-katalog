# Log Investigation Evidence

## Overview

Use esta skill para padronizar investigacao operacional baseada em evidencias de log.

## Fontes oficiais

### Aplicacao (estruturado)

1. **Tabela `logs` no banco de dados** — historico estruturado de erros e eventos de produto. Respeite multi-tenancy (tenant, ambiente, servico, escopo).
2. **API `GET` (ou equivalente) `/logs`** — mesma familia de eventos, com filtros/paginacao da API. Use quando for mais pratico que SQL direto ou para validar o que a tabela mostra.

### Infraestrutura (host / webserver)

3. **SSH no servidor** — estado real, `journalctl`, syslog, auth, processos e paths de log do webserver no filesystem.
4. **FTP/SFTP** — quando houver credencial na fonte operacional, leia/baixe arquivos de log do webserver (access/error) sem precisar so do shell.
5. **Logs do webserver** (nginx, Apache, Caddy, etc.) — 5xx, upstream timeout, vhost; obtidos via SSH e/ou FTP.

## Workflow

1. Para erro de **aplicacao**, consulte primeiro a tabela `logs` e/ou o endpoint **`/logs`**; correlacione periodo, severidade e servico.
2. Para erro de **infra ou web**, use **SSH** (prioritario para estado real) e **FTP/SFTP** quando os arquivos de log estiverem no path de arquivo.
3. Ao consultar o banco, filtre tenant/ambiente corretos.
4. Se houver divergencia entre tabela `logs`, API `/logs` e logs de webserver no host, registre a diferenca e priorize o estado real no servidor quando for falha de infra.
5. Nunca exponha trechos sensiveis de logs em respostas, issues ou registros visiveis.

## Output Contract

Ao concluir, informe objetivamente:

- qual fonte trouxe a evidencia principal (`logs` DB, `/logs`, SSH, FTP/webserver)
- qual erro, padrao ou recorrencia foi encontrado
- qual contexto temporal ou operacional foi confirmado
- quais divergencias entre fontes foram observadas

## Quality Bar

- nao trate evidencia indireta como substituto automatico do estado real do host
- nao ignore multi-tenancy ao investigar no banco ou na API `/logs`
- nao exponha logs sensiveis
- sempre deixe claro de onde veio a evidencia principal
