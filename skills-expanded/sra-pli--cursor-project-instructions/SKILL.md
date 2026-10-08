# Instruções Do Projeto (SRA)

## Como Usar Este Documento

Fonte canônica de domínio, stack, permissões, fluxos, PDF e ciclo de notificações. Atualize na mesma entrega quando mudar comportamento persistente, modelo de dados, rotas, templates principais, importação, PDF, deploy ou tarefas do Cursor. Não atualize por correções triviais.

Estrutura de `.cursor/`: `rules/*.mdc` (regras editor), `skills/*/SKILL.md` (workflows `/nome-do-skill`), `agents/*.md` (subagentes `/nome`). Encerramento de tarefa: `.cursor/rules/task-completion.mdc`. Índice resumido para agentes: `AGENTS.md`. **Boas-vindas genéricas para agentes IA** (segredos, serviços externos, leituras iniciais, fora de pastas de IDE): `docs/AI_AGENT_WELCOME_PROMPT.md`.

## O Que É Esta Aplicação

SRA (Sistema de Relatórios de Atividades) do contrato PLI/SP-2050. Plataforma web interna para produção semi-automática dos Relatórios Mensais D20 do consórcio Concremat-Transplan, no contexto SEMIL/DER-SP. Autores preenchem suas seções com blocos estruturados; coordenadores e admins controlam relatórios, seções, responsáveis, revisão, pré-visualização HTML A4 e exportação DOCX.

Modo de produção real: sem mocks, dados fictícios ou atalhos.

## Stack E Arquitetura

- Backend: FastAPI; ORM: SQLAlchemy 2; Banco: PostgreSQL real (geralmente remoto no Render).
- Templates: Jinja2 com HTML tradicional. Frontend: HTML/CSS/JS simples — **não migrar para React**.
- PDF: desativado em produção; pré-visualização usa HTML A4 a partir de `app/templates/pdf/relatorio.html`, e a exportação disponível é DOCX.
- Sessão assinada via `SessionMiddleware`; senha com `bcrypt`. Uploads de figura ficam no banco em `Figura.dados` (binário).
- Deploy: Docker e Render. Evite acionar WeasyPrint em produção; a pré-visualização HTML A4 substitui a geração de PDF para não consumir recursos do serviço.

### Arquivos Centrais

- `app/main.py`: cria FastAPI, registra middleware, estáticos e routers. `SraAutorRouteGuardMiddleware` + `SessionMiddleware` (ordem em `add_middleware`); middlewares `@app.middleware("http")` ficam por fora da sessão. `sra_http_audit_log` registra `metodo/path/status/duracao(ms)` para `/relatorios`, `/usuarios`, URLs com sufixo `upload-conteudo` e rotas com `/importar/` (logger `app.http`).
- `app/access_control.py`: URLs permitidas a `autor` e `SraAutorRouteGuardMiddleware`.
- `app/db.py`: engine SQLAlchemy, normaliza `DATABASE_URL` para `postgresql+psycopg2`, configura pool/latência para Postgres remoto.
- `app/models.py`: `User`, `Relatorio`, `Secao`, `Bloco`, `Figura`, `EntregaRelatorio`, `NotificacaoEnvio`, `SECOES_PADRAO`.
- `app/bootstrap.py`: inicialização leve do banco, seed do admin, ajustes de esquema simples.
- `app/auth.py`: usuário atual, validação de roles, regras de nome/senha.
- `app/routes/`: rotas de páginas, relatórios, blocos, figuras, importação e PDF.
- `app/pdf_render.py`: monta contexto e converte blocos para HTML/PDF.
- `app/list_lines.py`: detecção/renderização de listas em texto bruto (parágrafos + listas; HTML para PDF e ramo de bloco `lista`).
- `app/templates/complementos/*.html`: páginas Jinja servidas pelas rotas. `base.html` permanece em `app/templates/`. PDF (`pdf/`) e e-mail (`notificacoes/templates/`) mantêm caminhos próprios.
- `app/templates/complementos/secao_edit_conteudo_upload.html`: única UI de edição/gestão por seção — coordenação (responsável/status), importação assistida com revisão, tabela de blocos com aprovação em lote, **editor WYSIWYG Quill 2** (CDN jsDelivr, BSD — sem conta nem chave), barra com cabeçalhos H2–H6, ênfase, citação, listas, sobrescrito/subscrito, indentação, alinhamento, link e imagem; sincronização para `<textarea>` oculto com prefixo `<!--SRA_RICH-->`; sem CDN cai em `<textarea>` visível. Pré-visualização HTML A4. Ao escolher uma seção como alvo, **blocos, contagens de figura/tabela, iframe de pré-visualização e caixas da exportação** incluem **toda a subárvore PLI** (âncora + descendentes `N.*`, ver `secao_ids_na_subarvore` em `app/numeracao.py`).
- `app/routes/mapa_aplicacao.py` + `app/templates/mapa_aplicacao.html`: `GET /mapa-aplicacao` (sessão obrigatória) lista cartões de ficheiros em `complementos/` com rota de exemplo, restrição e "em uso". Metadados em `app/mapa_aplicacao_catalog.py`; `mapa_da_aplicacao.html` na raiz é cópia estática para consulta offline.

### Mapa De Rotas

- `app/routes/auth.py`: login, logout, gestão de usuários.
- `app/routes/pages.py`: dashboard, detalhe do relatório, páginas de seção (`upload-conteudo`; `GET /relatorios/{id}/secoes/{sid}` redireciona `303` para `upload-conteudo`).
- `app/routes/relatorios.py`: criação, edição, status, versão, duplicação, reversão e gestão de seções; `GET /relatorios/{id}/secoes/{sid}/status` redireciona `303` para `upload-conteudo`. `GET /relatorios/{id}/blocos-confirmados.json` (admin/coord) e `POST /relatorios/{id}/blocos/excluir-todos-confirmados` (helpers `_exigir_relatorio_editavel` + `_pode_editar_status` importados de `blocos.py`).
- `app/routes/relatorio_exclusao.py`: `POST /relatorios/{id}/excluir` e `POST /relatorios/{id}/secoes/{sid}/excluir` (mesmo prefixo no `main`); resposta HTML após transação.
- `app/routes/blocos.py`: criação, edição, confirmação/bloqueio, exclusão, movimentação e ações em lote; leitura JSON e mutações aceitam blocos de qualquer seção na **subárvore** da seção da URL (âncora).
- `app/routes/figuras.py`: upload de figuras e entrega dos binários.
- `app/routes/importacao.py`: análise e confirmação da importação assistida de TXT/DOCX (limite por pedido na análise: `IMPORTACAO_ANALISAR_MAX_BYTES` em `app/config.py`, padrão 20 MiB).
- `app/routes/pdf.py`: preview HTML A4 (`/relatorios/{id}/preview`) e exportação por escopo apenas em DOCX (`/relatorios/{id}/exportar?formato=docx&escopo=...`). Rotas legadas de PDF respondem 410 para evitar renderização WeasyPrint em produção.
- `app/routes/notificacoes.py`: toggle do opt-out (`notificacoes_ativas`), painel de entregas (`/relatorios/{id}/entregas`), ações do coord (status / reenvio manual / **reprovação com motivo**) e download autenticado dos modelos `.dotx`. As rotas POST de status/reenviar/reprovar aceitam `redirect_to` opcional para Post-Redirect-Get vindo da governança ou da página de Validação e Revisão (alinhado ao padrão de fato da governança; ver nota em **Convenções De Código**).
- `app/routes/validacao_revisao.py`: `GET /relatorios/{id}/validacao-revisao` (admin/coord) — seletor de relatório; **Seção 1**: sumário **recolhível**; árvore com responsáveis e cores (checagens de parciais); iframe pré-visualização inteira; dock aprovar/reprovar; notas internas. **Seção 2**: **mesmo workspace** (árvore à esquerda com cores por blocos/checagens globais); painel direito com fita **Pré-visualização | Editor de blocos** (iframe para `/preview` ou `…/upload-conteudo`), dock com **revisão linguística** + notas; abaixo: mapa seção ↔ responsável, resumo, categorias **2.1**, fechamento **2.2**; `POST /relatorios/{id}/revisao-linguistica`. Funções auxiliares: `_arvore_revisao_navegacao`, `_dict_navegacao_revisao_secao`. Serviços: `relatorio_secoes_load.py`, `autor_rotulo_secao`, `checagens_globais`. **Revisão editorial**: `GET /relatorios/{id}/revisao-edicao` (admin/coord) serve `complementos/revisao_edicao.html` — workspace dedicado de edição inline em folhas A4 simuladas (reusa `secoes_preview_grupos` de `pdf_render._montar_contexto`, com `bloco_id` e `bloqueado` expostos por bloco). Layout 3 colunas: árvore de seções, documento paginado editável e dock de revisão linguística PT-BR. Editor **Quill 2** (CDN jsDelivr) é instanciado **lazy por bloco** ao receber foco; serializa em HTML rich com prefixo `<!--SRA_RICH-->`. Auto-save por bloco em `POST /relatorios/{id}/blocos/{bid}/revisao-salvar` (JSON, debounce ~900 ms): aceita `conteudo`/`legenda`/`fonte` (parcial), preserva `bloqueado` (admin/coord pode editar bloco confirmado sem desbloquear), recusa em relatório `finalizado` (409). Não cria/move/exclui blocos nem seções. Botão **Revisar** dispara o mesmo `/revisao-linguistica`, sublinha trechos por categoria (ortografia/gramática/estilo) via overlay, dock permite **Aceitar sugestão** / **Ignorar (sessão)** / **Ver no documento**. Frontend: `app/static/css/revisao_edicao.css` + `app/static/js/revisao_edicao.js`. Sidebar: link "Revisão editorial" sob _Relatórios_ (active também quando path termina em `/revisao-edicao`).
- `app/routes/cron_admin.py`: endpoints `POST /admin/cron/...` token-protegidos (`X-Cron-Token`); equivalentes HTTP dos jobs CLI.
- `app/notificacoes/`: orquestração do ciclo mensal — `service.py` (`abrir_periodo`, `notificar_autores_abertura`, `enviar_lembretes`, `retry_falhas`, `recompute_status_enviado`, `alterar_status_entrega`, `reenviar_manual`, `reprovar_entrega`), `email_sender.py`, `modelos.py`, `templates/email_notificacao.{html,txt}`.
- `app/services/validacao/`: checagens estruturais por entrega (`checagens_entrega.py:montar_checagens_validacao`), checagens estruturais agregadas globais (`checagens_globais.py:montar_checagens_globais`) e revisão linguística sob demanda (`revisao_linguistica.py:analisar_relatorio`). **Revisão linguística:** `language_tool_python` está em `requirements.txt`; com **Java 8+** no PATH o serviço usa LanguageTool (gramática, estilo e ortografia). Sem Java (ou se o LT falhar ao subir), permanece **só ortografia** (`pyspellchecker`). A resposta JSON e a página 2.2 indicam o modo. Modo "desligado" só se nenhum pacote estiver importável. **Vocabulário do projeto** combina constantes em `_VOCAB_PROJETO` (siglas universais: PLI, SEMIL, DAEE, SRA…) com termos persistidos em `vocabulario_revisao` (modelo `VocabularioRevisao`, escopo global ao contrato, único por `termo` lowercased). `carregar_vocabulario_db(db)` lê os termos no início de cada análise; `adicionar_termo_vocabulario(db, termo, user_id)` é idempotente e invalida o singleton `_SP_INSTANCE` para refletir o novo termo na próxima análise sem reiniciar o processo. Endpoint `POST /relatorios/{id}/revisao-linguistica/vocabulario` (admin/coord) recebe `{"termo": "..."}`; o botão **+ Dicionário** no dock da Revisão editorial (achados de ortografia) consome esse endpoint.
- `app/services/entregas/lista_painel.py`: fonte única da «Lista de entregas» renderizada por `_lista_entregas_partial.html` em `/relatorios/{id}/entregas`, na governança (Tabela 1) e no rodapé da Validação. Mudança de regra/coluna reflete nos três lugares.
- `app/cron/`: pontos de entrada CLI dos jobs (`abrir_periodo`, `enviar_lembretes`, `retry_falhas`) — `python -m app.cron.NOME_DO_JOB` no Render Cron ou cron externo.
- `app/sumario_extractor.py`: extração de sumário a partir de PDFs entregues/disponíveis.
- `app/numeracao.py`: renumeração hierárquica (`renumerar_relatorio`), consolidação de referências para marcadores estáveis (`consolidar_referencias`) e `secao_ids_na_subarvore` (âncora + descendentes pelo número).
- `app/templates/`: telas Jinja; `app/templates/pdf/relatorio.html` é o template visual reaproveitado pelo preview HTML A4.
- `app/static/`: CSS e assets.

Layout autenticado: em `base.html`, o documento autenticado aplica a classe `sra-app` no elemento raiz (`padding-left: var(--sw)` em `app/static/css/app.css` reserva a largura da sidebar fixa). Classes por página usam o bloco Jinja `body_class` (substitui o antigo `body_attrs`). A sidebar lista apenas páginas completas, agrupadas por semelhança em menus suspensos; não adicione links para âncoras internas (`#...`) nem árvore de seções no menu lateral.

`app/routes/dev_ui.py`: `GET /dev/modais` (preview local de `window.confirm` via `SRAComplementos`); `GET /dev/preview-emails-notificacao` (página com as 3 mensagens — abertura/lembrete/última chamada); `GET /dev/preview-email-notificacao` (uma mensagem só, iframe `data:text/html;base64,...`); `?raw=1` devolve só o HTML; query opcional `tipo=...`, `relatorio_id=N`. Requer login; ativo com `APP_ENV=development` ou `SRA_MODAL_PREVIEW=1`; `SRA_MODAL_PREVIEW=0` força desligado.

### Confirmação No Browser

- `sra_process_ui.js`: formulários com `data-sra-confirm` (+ `data-sra-title/lead/detail/ask`) disparam `window.confirm` no `submit` via `SRAComplementos`. Em `relatorio_criar`, a fonte do sumário entra no texto da confirmação.
- Operações longas não publicam eventos no servidor.
- `data-sra-iniciar-acompanhamento="1"`: após `window.confirm`, registra em `SRA_LOG`, mostra faixa inferior fixa e desativa botões até receber resposta. `data-sra-busy-msg` para o texto.
- Chaves de fluxo: `importacao_assistida_analise/confirmar`, `relatorio_criar/excluir`, `exportar_relatorio`, `secao_excluir`, `bloco_confirmar/excluir`, `blocos_lote_excluir/aprovar`, `notificar_autores_abertura`, `notificar_ciclo_lembrete`, `notificar_ciclo_ultima_chamada` (no cartão «Notificar usuário» da governança o `data-sra-confirm` muda com o &lt;select&gt; do tipo).
- `window.SRAComplementos`: `init`, `carregarChave`, `confirmarComChave`, `abrirDireto`, `fecharConfirm`.
- Scripts em `base.html`: `sra_log.js` (`SRA_LOG` no console; verbose com `APP_ENV=development` ou hostname loopback), `sra_auth_fetch.js` (em verbose loga cada `fetch`), `sra_process_ui.js`.

## Funcionalidades Atuais

- Sessão e roles `admin`, `coordenador`, `autor`. No `User`, mesmo e-mail pode existir mais de uma vez se o **perfil** for diferente: unicidade `(email, role)`. Login (`POST /login`) exige e-mail + senha + perfil. Recuperação de senha: `GET/POST /recuperar-senha` e `GET/POST /recuperar-senha/definir`; passo válido fica em sessão (`sra_pwd_reset_*`) por até 1h; rotas públicas no guard de autor.
- Cadastro/edição de relatórios D20 com período, mês de referência, número de medição, versão e status.
- Criação a partir de sumário de PDF (entregue/disponível ou upload).
- Criação a partir de DOCX entregue atualiza automaticamente a seção 1
  (Apresentação) com dados do novo relatório: contrato/projeto padrão PLI,
  código D20, número da medição, período, medições realizadas, prazo corrido
  e status de acompanhamento, preservando o callout visual da apresentação.
- Criação automática e gestão de seções padrão (subseções, responsáveis e status por seção).
- Edição por blocos estruturados (`texto`, `lista`, `figura`, `tabela`) com ordem, autor, bloqueio e ações em lote.
- Inserção manual de figuras/tabelas por marcadores no conteúdo, com contagem coerente por seção e global.
- Numeração hierárquica consolidada: ao mutar estrutura, o sistema reescreve `Secao.numero/ordem` em DFS e troca "Figura X.Y" / "Tabela X.Y" / "Secao X.Y" por marcadores `[[REF:tipo|id]]`, resolvidos no render.
- Subseções podem ser movidas cima/baixo na tela de detalhe; relatórios `finalizado` bloqueiam mutações estruturais.
- Upload e reuso de figuras armazenadas no banco.
- Importação assistida de TXT/DOCX com revisão humana antes da persistência.
- Geração, preview e exportação de PDF no padrão visual do contrato.
- Ciclo mensal de notificações (detalhes em **Ciclo De Notificações** abaixo).
- Tarefas de dev no Cursor (`.vscode/tasks.json`): **SRA: backend (8001) + abrir / e /mapa-aplicacao** (`scripts/sra_backend_dev.ps1`, job `sra-open`); **SRA: diagnostico agregado** (`dump_agent_diagnostics.py` via interpretador do workspace ou `npm run dump-diags` → `scripts/npm-dump-diags.mjs`); **SRA: spelling** (`npm run spell`); **SRA: commit + push** (`scripts/sra_commit_deploy.ps1` com **`-SkipDeploy`** na task rapida — evita pager `less`/`(END)` e nao bloqueia 20 min no Render; ha task separada **commit + push + aguardar deploy no Render**). Na barra de estado, a extensao **TaskBari** (`SkySloane.taskbari`, recomendada em `.vscode/extensions.json`) agrupa essas entradas no mesmo `options.statusbar.group` (`SRA`): um unico botao abre o **QuickPick** vertical com a lista; nao usar `tasks.statusbar.limit: 0` com grupos (o overflow mistura comandos de grupo com tarefas soltas).
- Shell Windows neste repo: em `.vscode/settings.json` o perfil por defeito do terminal é **SRA PowerShell 7** (`pwsh` com caminho explícito em `Program Files`), há perfil **SRA Windows PowerShell 5.1** como alternativa, `automationProfile` e `PATH` do terminal pré-fixam PS7 e a pasta do 5.1 no `System32` (para `Get-Command` e ferramentas que dependem do PATH). Tasks `process`/`shell` e Code Runner alinham com esses caminhos. Se o teu PS7 não estiver em `%ProgramFiles%\PowerShell\7` (ex.: só via Scoop noutro sítio), altera o `path` nesses perfis ou define **SRA Windows PowerShell 5.1** como `defaultProfile`.

## Modelo De Domínio

`Relatorio`: D20 mensal, código tipo `D20-15`, período, mês de referência, medição, versão `R00/R01/...`, status.

`Secao`: `numero` (`String(16)`, `UniqueConstraint(relatorio_id, numero)`) e `ordem` (DFS) definem hierarquia. Campo opcional `observacao_validacao` (texto) guarda nota interna do coordenador na página Validação e Revisão (não entra no PDF). Numeração é semântica (não decoração): direciona ordenação, importação, sumário, contadores e referências. Mutação estrutural exige `consolidar_referencias` ANTES e `renumerar_relatorio` DEPOIS, em transação explícita (`tx_session`). Top-level (`4`, `5`, ...) é preservado; só subníveis reescritos em sequência 1..N por DFS.

`Bloco` (em ordem dentro da seção):

- `texto`: suporte leve a `#`, `##`, listas e marcadores de figura/tabela.
- `lista`: linhas iniciadas por `-`.
- `figura`: referência opcional a `Figura`, com legenda e fonte.
- `tabela`: tabular em texto, separado por `|`, com legenda e fonte.
- `origem`: `manual` por padrão; importação assistida grava `upload`, usado pelo escopo de exportação "Somente seções importadas".

`Figura`: nome, MIME, binário, legenda, fonte. Pode vir de upload manual ou DOCX.

`Bloco.bloqueado`: bloco confirmado. Não editar/excluir/mover (exceto `POST /relatorios/{id}/blocos/excluir-todos-confirmados` para admin/coord). Bloquear bloco dispara `recompute_status_enviado` (hook `_hook_recompute_entrega` em `app/routes/blocos.py`): se todas as seções do responsável têm todos os blocos bloqueados, `EntregaRelatorio` avança para `enviado` com `data_envio`.

Notificações:

- `User.email` + `User.email2` (ambos obrigatórios): principal (login, unicidade `(email, role)` em `uq_users_email_role`) e **secundário**. Ciclo envia para ambos quando distintos; `EntregaRelatorio.status` evolui só com sucesso para o **principal**.
- `User.notificacoes_ativas` (bool, default true): só `role=autor` com true entram no ciclo. Opt-out em `/usuarios`.
- `EntregaRelatorio` (1 por par `relatorio` × `user`): `status` (`notificado`/`aguardando_envio`/`enviado`/`validado`), `data_envio`, `data_validacao`, `validado_por_id`, **`motivo_reprovacao`/`data_reprovacao`/`reprovado_por_id`** (última devolução pelo coord — sobrescritos a cada reprovação; não há histórico), auditoria. Estado "finalizado" é do `Relatorio` inteiro.
- `NotificacaoEnvio` (1:N por `EntregaRelatorio`): `tipo` (`abertura`/`lembrete`/`ultima_chamada`/`manual`), `enviada_em`, `sucesso`, `erro`, `destinatario_email` (snapshot), `sendgrid_message_id`, `provedor_status`, `provedor_status_em`, `provedor_motivo`, `aberto_em`. `sucesso=true` significa aceite/tentativa bem-sucedida; entrega real só é exibida quando o Event Webhook do SendGrid registra `delivered`. Evento `open` aparece na UI como "Visualização detectada", sem afirmar leitura humana.

## Regras De Permissão

- `admin`: acesso amplo.
- `coordenador`: gestão/revisão.
- `autor`: edita só seções sem responsável ou em que seja responsável (regra por rota); **ao nível de URL**, restrito a fluxo de gestão de seção e upload — ver `app/access_control.py` (`SraAutorRouteGuardMiddleware`, `_AUTOR_PATH_RES`): `GET /`, `GET /painel-upload` (redireciona ao sumário do mais recente), `GET /relatorios/{id}` (sumário), `GET /modelos-word-importacao` (+ `baixar`), `GET /relatorios/{id}/secoes/{sid}/upload-conteudo`, `POST` `responsavel` (só si próprio) e `status`, APIs usadas pela página (blocos.json, importar, figuras, PDF) e login/logout. Após login bem-sucedido, destino do autor é `/relatorios/{id}` (`url_hub_autor` em `app/routes/pages.py`). **Autor não acede `/relatorios/{id}/entregas`** (painel agregado de entregas — admin/coord); o status da própria entrega aparece no sumário e na página de upload da sua seção. `response_entregas_painel` em `app/routes/notificacoes.py` aplica `_coord_or_403` como defesa em profundidade ao bloqueio do middleware.

Sessão guarda `user_role` no login (`app/routes/auth.py`) para o guard não consultar banco em todo pedido; ao editar próprio perfil, `user_role` na sessão é atualizado se mudar.

Em `secao_edit_conteudo_upload.html`: cartão «Coordenação da seção» reúne seção alvo, responsável e status; mudar **Seção alvo** navega para o `upload-conteudo` dessa seção; **Confirmar** envia em sequência `POST .../responsavel` e `POST .../status` com `retorno=upload`. Indicadores verde/vermelho marcam alinhamento. Responsáveis que não sejam ele aparecem desabilitados; com seção `pendente`, sugere `em_andamento`. Em «Editar bloco existente», o seletor «Seção atual» do autor limita-se às seções em que pode atuar; «Todas (blocos confirmados)» e «Excluir todos os blocos» só para admin/coord.

Sempre reutilize `current_user`, `require_user`, `require_admin` e os checks locais. Novas rotas do fluxo de gestão de seção/upload precisam entrar em `path_allowed_for_autor` (ou middleware bloqueia autores).

Mutações estruturais em `relatorios.py`/`blocos.py` passam por guard de status: relatório `finalizado` rejeita. Use `_exigir_relatorio_editavel(rel)` em `relatorios.py` e `_check(..., exigir_editavel=True)` em `blocos.py`.

### Matriz De `Relatorio.status` × Edição De Bloco

`Bloco.bloqueado` é uma trava **cooperativa entre autores durante a coleta**, não um cadeado permanente. A matriz oficial (implementada em `app/routes/blocos.py:_pode_editar_status` + `app/modo_edicao_blocos.py:pode_mutar_apesar_de_bloqueado`):

| Status                          | Autor                                          | Coordenador                                                                      | Admin                             | `bloqueado`                                                                 |
| ------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------- | --------------------------------------------------------------------------- |
| **`aberto`** (coleta)           | edita só blocos não bloqueados das suas seções | edita tudo (precisa **modo edição** ligado para mutar bloco bloqueado por outro) | edita tudo                        | **ativo** — protege blocos confirmados contra outros autores                |
| **`em_revisao`** (coord assume) | apenas leitura                                 | **edita tudo livremente, sem modo edição**                                       | edita tudo livremente             | **inerte** — UI esconde cadeado/desconfirmar; campo permanece intacto no DB |
| **`finalizado`**                | leitura                                        | leitura (precisa reverter status)                                                | leitura (precisa reverter status) | preservado, sem efeito                                                      |

A função `pode_mutar_apesar_de_bloqueado(request, user, rel_id, rel_status)` recebe o status para liberar coord em `em_revisao` sem modo edição. Toda call site em `routes/blocos.py` passa `rel.status` (ou `anc_sec.relatorio.status`). Página de Revisão editorial expõe `bloqueio_visivel = (rel.status == 'aberto')` ao template — o cadeado e o botão "Desconfirmar" só aparecem em `aberto`.

## Fluxos Principais

### Dashboard E Relatórios

Dashboard lista relatórios e sugere próximo D20 com base na última medição. Tela de detalhe mostra seções, responsáveis, status e acesso para edição.

### Edição De Seção

- `/relatorios/{id}` (`relatorio_detail.html`, `page-rel-com-preview`): layout 2 colunas igual ao `upload-conteudo` — sumário/ações à esquerda (botão `+` por linha cria subseção inline como última filha via `POST /relatorios/{rel_id}/secoes/{sec_id}/subsecao`; servidor decide o número via `_proximo_numero_filho` e roda `consolidar_referencias`+`renumerar_relatorio`); preview HTML A4 à direita. Classe combinada: `page-conteudo-upload page-rel-com-preview`.
- `GET /painel-upload`: redireciona `303` ao sumário `/relatorios/{id}` do mais recente.
- `GET /relatorios/{id}/secoes/{sec_id}` redireciona `303` para `…/upload-conteudo`.
- `GET /relatorios/{id}/secoes/{sec_id}/upload-conteudo`: serve `secao_edit_conteudo_upload.html` — gestão da seção (coordenação, importação assistida, tabela de blocos, editor) + preview HTML A4.

A tela permite: visualizar blocos em tabela; criar bloco manual; editar pelo container inferior; confirmar/bloquear; excluir; importar TXT/DOCX; anexar/usar figuras; manter contagem coerente.

Importação **sempre** permite revisão assistida antes de criar blocos definitivos.

### Importação Assistida

`app/routes/importacao.py` analisa `.txt`/`.docx` e retorna blocos JSON para revisão.

Cuidados:

- `4.4.7Atividades...` ou `4.4.7 - Atividades...` representam destino de seção, não bloco repetido.
- Títulos `4.4.7.1 ...` podem virar subtítulos no conteúdo.
- Legendas `Figura 4-1: ... Fonte: ...` separam legenda e fonte.
- DOCX pode ter imagem em um parágrafo e legenda no seguinte: manter associação.
- Imagem embutida vira `Figura` real ao confirmar.
- Não repita o título da seção como `Bloco.titulo` em todos os blocos.
- Listas no conteúdo são **formatação local** (independente da numeração de seções): `app/list_lines.py` define o texto bruto com recuo em múltiplos de 2 espaços e marcadores (`-`, `1.`, `a)`, romano). DOCX com `w:numPr` + `word/numbering.xml` é normalizado para esse texto bruto. Barra de ferramentas em `secao_edit_conteudo_upload.html` atua só no textarea (com `import_texto_tools.js`).

### Modelo Canônico Word/TXT Para Preenchimento

Não restringe o importador, oferece ficheiro alinhado ao que a análise reconhece (regras seguem `importacao.py` e `list_lines.py`).

**`.txt`**: marcador exato `[SECAO:4.4.1]`; tabelas `[TABELA]` ... `[/TABELA]` com `Fonte:` dentro; linha vazia faz flush; `#`/`##` e subtítulo numerado via `_normalize_heading_line` (`_HEADING_RE` exige número com **2+ segmentos**).

**`.docx`** (foco do modelo recomendado):

- Ordem do corpo Word; evite caixas de texto.
- Seção/títulos: estilos reais (`Heading 1..N` / `Título 1..N`); passam por `_section_from_heading` ou viram blocos com `#`/`##`. Linhas "normais" também batem em `_match_secao_linha` se forem como `4.4.7  Título`.
- Listas: use **listas reais** Word — `w:numPr` + `word/numbering.xml` mapeia `bullet`/`decimal`/`lowerLetter`/`roman` etc. Estilos só de parágrafo "Lista" (sem `numPr`) são aproximados com hífen + espaço.
- Tabelas: nativas viram `| a | b |`; legenda na linha anterior com padrão `Tabela X.Y: ...` (`_TABELA_RE`); `Fonte:` na legenda ou parágrafo seguinte.
- Figuras: imagem **no próprio parágrafo** (incorporar imagem) — `_paragraph_images`. Legenda na linha que bate com `Figura`/`Fig.` + número + `:`/`-`/`.`/`…`; `Fonte:` na linha ou no parágrafo seguinte.

**Catálogo na aplicação**: `GET /modelos-word-importacao` (`app/routes/modelos_word.py`, template `complementos/modelos_word_importacao.html`) lista `SRA_todas_secoes.dotx` e `secao_*.dotx` permitidos. `GET /modelos-word-importacao/baixar/{arquivo}` serve apenas se o nome estiver na lista branca. Pasta `modelos_upload_doc_canonicos/` contém os ficheiros; regenerar com `scripts/build_canonical_upload_dotx.py` quando `SECOES_PADRAO` mudar.

### Ciclo De Notificações Mensais

Persistência editável (coord/admin): tabela singleton `parametros_ciclo_notificacao` (`app/models.ParametrosCicloNotificacao`); carga/definição em `app/notificacoes/ciclo_params.py`. UI `GET /governanca-relatorio` (`app/routes/governanca_relatorio.py`, template `complementos/governanca_relatorio.html`): o router deve ficar fino, só registrando rotas e delegando regras para `app/services/governanca/`. A tela cobre edição das tabelas `parametros_ciclo_notificacao`, `entrega_relatorio`, `notificacao_envio` e `users` (coordenador só vê autores e próprio perfil), acompanhamento do ciclo em linguagem operacional (relatório aberto, envio solicitado, entrega confirmada, visualização técnica detectada, próximos disparos e modal com situação por autor), console de execução manual real com escolha de relatório base para abertura e filtro server-side por relatório em entregas/notificações (padrão: relatório mais recente). Chave SendGrid, kill-switch, token do webhook SendGrid e chave opcional `CRONJOB_ORG_API_KEY` ficam em ambiente. Sidebar: «Governança» > «Governança do relatório».

Pontos de entrada (idempotentes) em `app/notificacoes/service.py`:

- `abrir_periodo(db, *, force=False, data_referencia=None, base_relatorio_id=None)`: cria relatório do mês corrente (período via `periodo_referente_para_data` + parâmetros persistidos) clonando seções/blocos/figuras do relatório base escolhido; sem `base_relatorio_id`, usa último `finalizado` com fallback para o mais recente. Ajusta texto do período/código e remapeia `[[REF:]]`. Sem `force` e sem relatório existente: só avança se dia BRT == `dia_abertura_novo_ciclo`; senão devolve aviso. `force=true` ignora calendário.
- `notificar_autores_abertura(db, rel_id, *, force=False)`: Mensagem 1 para autores ativos. Padrão idempotente (cron e scripts: pula quem já recebeu, conta em `pulados_ja_enviados`). `force=True` é o caminho **assistido pelo coordenador** — botão _Notificar autores (abertura)_ no sumário do relatório (`POST /relatorios/{id}/notificar-autores-abertura`) e execução manual da governança (`tipo=abertura`) — força reenvio mesmo a quem já recebeu, em principal e secundário; cada chamada cria nova linha em `notificacao_envio` (audit trail) e não regride status da entrega. O cron HTTP `POST /admin/cron/notificar-autores-abertura?relatorio_id=N&force=true` espelha o opt-in.
- `enviar_lembretes(db, *, tipo, relatorio_id=None, ignorar_calendario=False)`: Mensagem 2. `tipo ∈ {lembrete, ultima_chamada}`; padrão respeita calendário (lembrete em dias configurados; última chamada no dia configurado). `ignorar_calendario=true` (CLI `--ignorar-calendario`, query HTTP, chamadas Python E2E) contorna. Filtro: status `notificado`/`aguardando_envio`, último envio bem-sucedido > 22h. Após 2 envios bem-sucedidos status vai para `aguardando_envio`. `relatorio_id` restringe.
- `retry_falhas(db)`: reenvia falhas dos últimos 7 dias, até 3 tentativas por par `(entrega, tipo)`. Cria nova linha em `notificacao_envio` por tentativa (audit trail).
- `recompute_status_enviado(db, user_id, rel_id)`: avalia se entrega vai a `enviado` (todas as seções do user com pelo menos 1 bloco, todos `bloqueado=true`). Não regride a partir de `enviado`/`validado`. Hook chamado por `confirmar_bloco`/`aprovar_blocos_lote` em `blocos.py` via `_hook_recompute_entrega`.

Ações manuais do coord (`app/routes/notificacoes.py`):

- `POST /usuarios/{id}/notificacoes-toggle`: liga/desliga `notificacoes_ativas`.
- `POST /relatorios/{id}/entregas/{eid}/status` (`novo_status`): altera status; `validado` carimba `validado_por_id`/`data_validacao`. Aceita `redirect_to` opcional para Post-Redirect-Get a partir de páginas externas (Validação e Revisão, governança).
- `POST /relatorios/{id}/entregas/{eid}/reenviar`: nova mensagem `manual`, ignora janela 22h. Mesmo `redirect_to`.
- `POST /relatorios/{id}/entregas/{eid}/reprovar` (`motivo`, `redirect_to`): devolve a parcial ao autor com justificativa obrigatória — status volta para `aguardando_envio` e `motivo_reprovacao`/`data_reprovacao`/`reprovado_por_id` são carimbados.

E-mail (`app/notificacoes/email_sender.py`):

- Modos: `real` (`SENDGRID_API_KEY` + `NOTIFICAR_HABILITADO=true` + `NOTIFICAR_SANDBOX=false`), `sandbox` (renderiza/valida sem enviar), `desligado` (`NOTIFICAR_HABILITADO=false`). `modo_atual()` expõe a decisão.

- Template único `app/notificacoes/templates/email_notificacao.{html,txt}` que muda intro/CTA por `tipo`. HTML usa tabelas + estilos inline (sem flexbox, sem &lt;details&gt;/&lt;summary&gt;) para Outlook desktop, que ignora HTML5 nativo e flui inline quando o elemento não tem &lt;div&gt; interno (foi a causa de seções 1-3 ficarem horizontais antes da troca por tabelas). Largura-base **600px** com `max-width:100%`, viewport meta + `@media (max-width:600px)` reduz padding/fonte em iOS Mail/Gmail/Outlook mobile. A árvore de modelos `.dotx` é renderizada por `render_modelos_arvore` (uma &lt;table&gt; por nó de nível 1, sempre expandida) — sem colapso, mas garante stacking vertical em qualquer cliente. `linear-gradient` evitado: usar `background-color` sólido para que Outlook desktop renderize fundo igual ao mobile.

- Envio real marca prioridade (`Importance`, `X-Priority`, `X-MSMail-Priority`) e habilita `open_tracking` do SendGrid para mensagens do ciclo. O endpoint `POST /admin/sendgrid/events?token=...` recebe Event Webhook (`delivered`, `open`, `bounce`, `dropped`, `spamreport`, `blocked`, `deferred`, `processed`) e atualiza `NotificacaoEnvio`; configure o webhook no painel SendGrid apontando para `APP_BASE_URL` e guardando o token em `SENDGRID_EVENT_WEBHOOK_TOKEN`.

- Links: `link_upload`, `link_dotx` (`/relatorios/{rel}/secoes/{sec}/modelo.dotx` autenticado em `notificacoes.py`), `link_relatorio_painel`, `link_modelos_word_ajuda`, `link_login_sra`, `link_painel_upload`. Hosts derivados de `APP_BASE_URL`.

- Prazos no corpo (`prazos_mensagem_relatorio` em `service.py`): mês/ano de `periodo_fim`; dias de autor e coordenação configuráveis (`prazo_autor_dia`, `prazo_coordenacao_dia`); horas exibidas 23:59.

- Árvore: `arvore_secoes_links` (lista aninhada) montada por `arvore_secoes_com_links` em `app/notificacoes/email_context_arvore.py` (ordenação por partes numéricas de `numero` + `ordem`); texto plano via `format_arvore_secoes_email_plaintext(..., apenas_dotx=True)`. No HTML, lista de modelos usa `&lt;details&gt;` recursivo (fechado por padrão; nível 1 visível). Preview sem BD em `tmp/email_preview_*.html` via `arvore_secoes_padrao_para_preview` (IDs sintéticos 10000+); regerar com `scripts/export_tmp_email_previews.py`.

Cron (Track 5):

- CLI em `app/cron/`: `python -m app.cron.abrir_periodo [--force]`, `python -m app.cron.enviar_lembretes --tipo {lembrete|ultima_chamada} [--relatorio-id N]`, `python -m app.cron.retry_falhas`. Cada um abre `SessionLocal()` próprio.
- HTTP em `/admin/cron/{abrir-periodo,abrir-periodo-background,notificar-autores-abertura?relatorio_id=N,lembretes,retry}`: equivalente JSON, exige `X-Cron-Token == settings.CRON_TOKEN`. Token vazio → 503 (fail-closed). Comparação em tempo constante. Cron externo deve preferir `abrir-periodo-background`, pois a abertura mensal pode ultrapassar o timeout de 30s do cron-job.org quando clona conteúdo e envia e-mails.
- Teste prático: `scripts/teste_http_cron_notificacao.py` (`--http`/`--in-process`; `--no-force` imita produção; `--cadeia-atribuir` atribui seção e notifica). E2E completo: `scripts/_e2e_notificacoes.py`.
- Schedules externos espelham dias/horários guardados (`/governanca-relatorio` e `app/cron/*.py`).

Variáveis de ambiente (`.env.example` / `render.yaml`): `SENDGRID_API_KEY`, `SENDGRID_FROM_EMAIL`, `SENDGRID_FROM_NAME`, `APP_BASE_URL`, `NOTIFICAR_HABILITADO`, `NOTIFICAR_SANDBOX`, `SENDGRID_EVENT_WEBHOOK_TOKEN`, `CRON_TOKEN`; `SESSION_COOKIE_SECURE` (produção HTTPS: cookie de sessão com `Secure`; `render.yaml` define `true`). Opcionais para status do cron externo: `CRONJOB_ORG_API_KEY` (`sync: false` no Render, valor só no ambiente) e `CRONJOB_ORG_JOB_*`.

Fonte única do nome `.dotx` em `app/notificacoes/modelos.py` (`slug_titulo`, `filename_para`, `caminho_para`); `scripts/build_canonical_upload_dotx.py` importa daqui.

E2E manual: `scripts/_e2e_notificacoes.py` (usuários `@notif-test.local`, exercita 4 entradas + ações coord, limpa estado). Idempotente. E2E com conteúdo real: `scripts/teste_real_ciclo_notificacao.py` (`--listar-secoes`, `--criar-periodo`/`--relatorio-id`, `--secoes`, preview via `email_sender.py`; envio efetivo exige `--usuario-email`, `--confirmar` e obedece `NOTIFICAR_*`/SendGrid).

### Preview HTML A4 E DOCX

`app/pdf_render.py` transforma blocos em estrutura para `app/templates/pdf/relatorio.html`. O contexto inclui `secoes_preview_grupos` (agrupamento por seção de nível 1) para desenhar, no navegador, folhas A4 separadas com cabeçalho/rodapé e número de página coerentes com a ordem do documento. A rota pública usada pelos pré-visualizadores é HTML, sem WeasyPrint.

`app/docx_render.py` produz a versão DOCX usando `python-docx`; ele acompanha o template visual e tenta manter alinhamento visual (Verdana 10pt no corpo, parágrafos e **itens de lista** justificados, headings azul-marinho, captions 9pt bold com 'Fonte:' 8.5pt, `bloco.titulo` como Heading 2 12pt, listas com indent 1.27cm, tabelas com cabeçalho 8.8pt bold). Se mudar regras de tipografia em `app/templates/pdf/relatorio.html` (`.bloco p`, `.bloco ul`/`ol`, `.figura .cap`, `.tabela th`, etc.), espelhe em `_format_body_paragraph`/`_format_list_paragraph`/`_format_caption`/`_format_caption_fonte`/`_set_runs_font` para que preview HTML e DOCX continuem visualmente equivalentes.

`app/routes/pdf.py`: `GET /relatorios/{id}/preview` (HTML A4; opcional `secao_ids` para pré-visualizar só o ramo), `GET /relatorios/{id}/exportar` (`docx`, escopo `inteiro`, `selecionadas` ou `importadas`). `GET /relatorios/{id}/pdf`, `formato=pdf` e `GET /relatorios/{id}/exportar-assinatura` são legados desativados com 410.

Cuidados:

- Preview HTML A4 preserva sumário, numeração, legendas, fontes, figuras, tabelas, cabeçalho/rodapé e página de assinaturas.
- Marcadores `[[FIGURA:...]]`/`[[TABELA...]]` ainda suportados por compatibilidade.
- Bloco `figura` sem imagem renderiza placeholder; ideal é DOCX importar imagem real.
- Contadores de figuras/tabelas seguem o primeiro nível da seção (`4.1`, `4.2`).
- `idx` em `[[FIGURA:idx|...]]`/`[[TABELA:idx|...]]` é bimodal: com ponto (`4.1`) é "por seção" e usa contador atual; puramente numérico (`5`) é sequencial global e respeitado; vazio cai no contador local.
- 3 marcadores REF resolvidos em `_resolver_referencias` via `_MapasRef` (`_calcular_mapas_referencia`), sempre exibindo número atual. Alvo excluído → marcador permanece para sinalizar inconsistência (não gera "Figura None"):

  ```text
  [[REF:figura|ID_BLOCO]]
  [[REF:tabela|ID_BLOCO]]
  [[REF:secao|ID_SECAO]]
  ```

### Numeração Hierárquica E Referências Estáveis

Exibição de índice em preview HTML/DOCX e texto resolvido a partir de `[[REF:…]]`: **`capítulo.sequência`** com **ponto** (ex.: `4.1`, `3.2`), não traço — função `label_numero_pli` em `app/ref_resolve.py`.

`app/numeracao.py`:

- `renumerar_relatorio(db, rel_id)`: recalcula `Secao.numero/ordem` por DFS sobre a árvore (prefixo + ordem dos irmãos). Aplica em duas fases (prefixo temporário `__t` e UPDATE com `CASE`) para não colidir com `UniqueConstraint(relatorio_id, numero)`. Top-level preservado.
- `consolidar_referencias(db, rel_id)`: varre `Bloco.conteudo`/`Bloco.legenda`, troca "Figura X.Y"/"Tabela X.Y"/"Secao X.Y" (variantes com `-` e acentuação) por `[[REF:tipo|id]]`. Idempotente.
- `consolidar_e_renumerar(db, rel_id)`: atalho que faz na ordem correta.

Ordem obrigatória nas rotas que mutam estrutura: (1) `consolidar_referencias` ANTES (fixa alvo em ID estável); (2) executa mutação; (3) `renumerar_relatorio` DEPOIS. Tudo em `tx_session`. Já integrado em `relatorios.py` (criar/excluir/mover subseção), `blocos.py` (quando `_impacta_numeracao`) e `importacao.py` (após finalizar importação).

## Banco E Performance

Banco geralmente remoto (Render) com latência alta. `app/db.py` usa pool, keepalives e `isolation_level="AUTOCOMMIT"` para reduzir round-trips.

- Evite N+1 (`selectinload`, `load_only`, agregações, lote).
- Operações multi-statement com atomicidade real → `tx_session` ou `with db.begin()`.
- Não reative `pool_pre_ping` nem remova ajustes de pool sem medir impacto.
- Não conte/insira item a item quando lote resolve.

Skill `/performance-agility` (`.cursor/skills/performance-agility/SKILL.md`) para mudanças cirúrgicas com ganho verificável.

## Convenções De Frontend

- HTML/Jinja2/CSS/JavaScript simples. Sem React.
- Interface densa, utilitária, focada em produção/revisão de relatórios.
- Não fazer mudanças visuais amplas sem pedido direto.
- Em tabelas e controles da seção: preservar legibilidade, alinhamento, bordas e ações por ícones quando o padrão já existir.
- Sem texto explicativo excessivo dentro da interface.

## Convenções De Código

- Mudanças mínimas, focadas e compatíveis com o estilo existente. Não reverta alterações do usuário. Não adicione dependência sem necessidade clara. Não crie abstrações grandes para ajuste pequeno.
- Preserve nomes de domínio em português: relatório, seção, bloco, figura, legenda, fonte, medição.
- Novas rotas: `APIRouter`, `Depends(get_db)`, `current_user`, respostas HTML com `TemplateResponse` (200; reuse `response_dashboard`, `response_relatorio_detail`, `user_or_login_page`, `response_client_goto` em `app/routes/pages.py`) ou `JSONResponse` para API. **Não** use `RedirectResponse` (3xx) para fluxos de formulário; após `POST` devolva a página de destino em 200. **Exceção:** `POST /login` e `GET /logout` usam `response_client_goto` (JS `location.replace`) para alinhar URL e conteúdo.
- **Pendência conhecida:** `app/routes/governanca_relatorio.py` e o caminho `redirect_to` em `notificacoes.py` (rotas de status/reenviar/reprovar de entrega) usam `RedirectResponse 303` em violação à regra acima — ficou consolidado como padrão de fato porque é o único jeito limpo de Post-Redirect-Get entre páginas distintas (governança ↔ entregas, validação ↔ entregas) sem importações cruzadas pesadas. Saneamento futuro: extrair `response_governanca_relatorio` e `response_validacao_revisao` em `pages.py` (ou módulo análogo) e alimentar essas rotas, eliminando o `RedirectResponse`. Tarefa de débito técnico, não bloqueante.
- Templates: Jinja2 simples; prepare dados na rota.

## Linting, Validação E Encerramento

Configuração canônica em `pyproject.toml` e `.vscode/settings.json`. Indentação/charset alinham `.editorconfig` (Python 4 espaços; HTML/CSS/JS/JSON/YAML 2; Markdown sem `trim_trailing_whitespace`).

- **Regras detalhadas**: `.cursor/rules/linting.mdc` (Python/Jinja/cspell) e `.cursor/rules/code-sanitization-efficiency.mdc` (postura).
- **Encerramento de tarefa (obrigatório)**: `.cursor/rules/task-completion.mdc` — execute `scripts/dump_agent_diagnostics.py` (lê `artifacts/agent-diagnostics.txt`, corrige até saída 0), depois lints do agente nos arquivos tocados, releia integralmente.

Setup local mínimo:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Sanity check do app: `.\.venv\Scripts\python.exe -c "import app.main; print('ok')"`.

## Estado Atual SRA 2.0 (2026-05)

A reescrita SRA 2.0 vive em `SRA_2_0/` (FastAPI + SQLAlchemy + Jinja2).

### Schema (alembic 0009-0012)

- `dom_tipos_elemento`: 30 elementos OOXML com `categoria` + `suporte` + `ooxml_tag` (0009)
- `relatorios_finalizados` reescrita: `revisao_id`, `artefato_docx`, `checksum_docx`, `snapshot_conteudo` JSONB, `mes/ano_referencia`, `nome_arquivo` (0009)
- `secoes_canonicas`: `obrigatoria`, `dinamica`, `responsavel_default`, `numero` (0009)
- `templates_dotx`: `dados BYTEA NULL` + `caminho_disco` + `tamanho_bytes` (0010 - Render PG nao comporta 308MB blobs)
- `blocos`: `confirmado_por_autor_em/id` + `aprovado_por_coord_em/id` (0011)
- `templates_mensagem`: assunto + corpo Jinja2, versionado por tipo (0012)

### Rotas novas

- `GET /admin/templates`, `GET /admin/templates/{id}/download` - 28 .dotx canonicos
- `GET /admin/figuras`, `POST /admin/figuras/upload` (dedup SHA-256), `POST /admin/figuras/{id}/excluir`
- `GET /admin/mensagens-templates`, `POST /admin/mensagens-templates/{tipo}` - templates Jinja
- `GET /convite?token=...`, `POST /convite/aceitar` - primeiro acesso por convite
- `POST /usuarios/{id}/convite/reenviar` - admin/coord reenvia convite
- `POST /relatorios/{id}/reabrir` (modo=producao|revisao, motivo obrigatorio)
- `POST /relatorios/{id}/entrega/enviar` - autor envia sua parte
- `POST /relatorios/{r}/secoes/{s}/autores/adicionar` + `.../{u}/remover`

### Servicos

- `services/clonagem.py` - clona D20-N -> D20-N+1 com regex doc 03 sec 3.3
- `services/validacao.py` - 6 criterios bloqueantes da finalizacao
- `services/finalizacao.py` - snapshot + .docx + checksum
- `services/notificacoes.py:renderizar_template` - Jinja2 do templates_mensagem
- `services/importacao_docx.py` - parser OOXML completo (hyperlink/bookmark/field/page_break/section_break/tab/header/footer + word_xml)
- `services/renderer_docx.py` - reaproveita word_xml preservado para fidelidade maxima

### Cron jobs

- `python -m app.cron.abrir_periodo [--mes YYYY-MM] [--force]`
- `python -m app.cron.enviar_lembretes --tipo lembrete|ultima_chamada [--enviar]`
- `python -m app.cron.retry_falhas [--limite 100]`

### Scripts

- `python -m scripts.bootstrap_templates_dotx [--com-blob]` - carga dos 28 .dotx

### Testes (20 passando)

```powershell
.\.venv\Scripts\python.exe -m pytest SRA_2_0/tests/ -v
```

## Regras djlint — Templates Jinja2

**djlint só roda em `.html`** — `*.py` está excluído em `pyproject.toml` (`exclude = ...*.py`). Nunca rode djlint manualmente em arquivos Python.

**Regra de ouro — atributos condicionais Jinja (evita H025):**

```html
<!-- ✅ Correto: tag de abertura e condicionais Jinja na mesma linha -->
<option value="{{ s.id }}" {% if s.id="" ="sec.id" %} selected{% endif %}>
  <!-- ❌ Errado: gera H025 "Tag seems to be an orphan" -->
</option>

<option
  value="{{ s.id }}"
  {%
  if
  s.id=""
  ="sec.id"
  %}selected{%
  endif
  %}
></option>
```

Tags multi-linha sem Jinja nos atributos são permitidas normalmente.
