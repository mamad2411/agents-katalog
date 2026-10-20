# Contexto do Projeto: Disparador de Avisos de Ponto (PontoMais → WhatsApp)

Tu és um assistente especialista em desenvolvimento Full Stack (Python/Flask + JS vanilla) a atuar no projeto **Disparador de Mensagens PontoMais** da TopFama. O teu objetivo é ajudar a manter, refatorizar e expandir esta ferramenta de automação de avisos de ponto via WhatsApp.

## 📋 Sobre o Projeto

O sistema processa relatórios CSV exportados do **PontoMais** (Auditoria, Ocorrências e Assinaturas), identifica irregularidades de ponto (faltas, horas extras, interjornada/intrajornada insuficiente, assinaturas pendentes, etc.) e envia mensagens formatadas via WhatsApp para o gestor de cada equipe/loja, através da Evolution API.

- **Backend:** Python 3.11+ (Flask 3.x), servido em produção via Gunicorn (`gthread`, porta `8000`).
- **Frontend:** HTML/CSS/JavaScript ES6+ vanilla, servido diretamente pelo Flask (`/static` e `/templates`) — **não há Node.js/build step**.
- **Infraestrutura:** Docker, MySQL (histórico de envios), Evolution API (gateway WhatsApp), Google Sheets API (opcional).

## 🛠️ Stack Tecnológica

- **Framework:** Flask (Blueprint único em `app/routes.py`).
- **Processamento de dados:** Pandas (parsing dos CSVs do PontoMais).
- **Persistência:** MySQL via `mysql-connector-python` (histórico de envios e status de relatórios).
- **Integrações externas:** `requests` para a Evolution API; `gspread`/`google-auth` para Google Sheets.
- **Assíncrono:** `ThreadPoolExecutor` (não usa Celery/Redis) para processar CSVs e enviar mensagens em segundo plano.
- **Exportação:** `openpyxl` para gerar planilhas de histórico.

## 🧠 Regras de Negócio Críticas (Memory Bank)

1. **Nunca usar `time.sleep()` no fluxo assíncrono de envio** — o único delay controlado (anti-spam, `random.uniform(0.25, 0.5)`) fica dentro de `enviar_whatsapp()` em `app/routes.py`, após cada envio bem-sucedido.

2. **Sessão do WhatsApp:** toda tarefa de envio (`app/tasks.py`) verifica `verificar_sessao()` antes de processar. Se a instância não estiver `open` na Evolution API, a tarefa falha sem tentar enviar nada. Se a instância ficar em `connecting` por mais de 60s, o sistema força um logout automático para voltar a `close`.

3. **Proteção contra reenvio duplicado:** o nome do relatório (normalizado via `normalizar_nome_relatorio`) é usado como chave única nas tabelas `relatorios`/`relatorio_pendencias`. Um relatório com status `sucesso_total` só é reenviado se o usuário confirmar `forcarReenvio=true`; um relatório `parcial` reenvia apenas para as equipes pendentes.

4. **Mapeamento de equipes:** `app/processamento/mapear_gerencia.py` normaliza nomes de equipe/loja do CSV (ex.: "Loja 75", "CD10", "Tech", "RH") em códigos padronizados usados em todo o sistema — é o ponto central para adicionar/corrigir setores.

5. **Números de WhatsApp por equipe:** resolvidos dinamicamente por `app/whatsapp/numeros_equipes.py`, lendo uma planilha (CSV público via `PLANILHA_EQUIPES_URL`, com fallback para Google Sheets API via `PLANILHA_EQUIPES_SHEET_ID`). Não há números fixos no código.

## 📂 Estrutura de Pastas Relevante

- `app/routes.py` — Blueprint Flask com todos os endpoints da API e a integração com a Evolution API (`enviar_whatsapp`, `verificar_sessao`).
- `app/tasks.py` — Fila assíncrona (`ThreadPoolExecutor`) e persistência do status de cada tarefa em `task_status/<id>.json`.
- `app/controller.py` — Orquestra o fluxo completo: carrega o CSV, gera as mensagens, envia e registra o histórico.
- `app/processamento/` — Parsers de CSV (`csv_reader*.py`), mapeamento de equipes (`mapear_gerencia.py`) e lógica de mensagens de Ocorrências (`ocorrencias_processor.py`, `motivos_ocorrencias.py`).
- `app/whatsapp/` — Templates e geração de mensagens de Auditoria (`mensagem.py`) e Assinaturas (`mensagem_assinaturas.py`), e resolução de números (`numeros_equipes.py`).
- `app/history.py` — Histórico de envios e status de relatórios no MySQL.
- `app/services/` — Integrações opcionais: `google_sheets.py` (gravação do DataFrame processado) e `email_sender.py` (utilitário de notificação de erro por e-mail, **não é chamado automaticamente** pelo fluxo atual).
- `templates/` + `static/` — Frontend (index.html de envio, historico.html de histórico).
- `tests/` — Suíte pytest. `teste/` — CSVs de exemplo para testes manuais (não confundir com `tests/`).

Ver também [AGENTS.md](AGENTS.md) para a árvore completa de arquivos, a tabela de variáveis de ambiente e as convenções de commit/branch do projeto.

## 🚀 Instruções de Execução

### Local
```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows (ou source .venv/bin/activate no Linux/Mac)
pip install -r requirements.txt
cp .env.example .env       # e edite as variáveis
python main.py             # http://localhost:8000
```

### Docker
```bash
docker compose up -d       # usa docker-compose.yml (porta 192.168.99.50:8000)
```

### Testes
```bash
pytest
flake8   # quando disponível
```
