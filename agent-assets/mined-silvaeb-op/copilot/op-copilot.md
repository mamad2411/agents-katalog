# Copilot instructions for OP

## Project context
- Flask 2.3 monolith using SQLite (`database.db`) and pandas/openpyxl for Excel imports. Core logic lives in [app.py](../app.py); schemas and helpers are in [database.py](../database.py).
- UI is Jinja templates under [templates/](../templates) with dynamic behavior in [static/js/cadastro_completo.js](../static/js/cadastro_completo.js) and [static/js/script.js](../static/js/script.js). Keep labels and messages in Portuguese.
- Excel inputs: `CODOM.xlsx` (UG/CODOM/subordination) and `Dados.xlsx` (Vinculo_OM, Efetivo). They feed globals `DADOS_OMS`, `DADOS_UG_CODOM`, `DADOS_SUBORDINACAO`, `DADOS_VINCULO_OP`, `DADOS_EFETIVO_OM`, `DADOS_RM_OP`. Preserve structure if extending.

## Setup and running
- Python 3.x. Install deps: `pip install -r requirements.txt` (Flask 2.3.3, Werkzeug 2.3.7, pandas 2.0.3, openpyxl 3.1.2, gunicorn 21.2.0).
- Env defaults are documented in [start.ps1](../start.ps1): `SECRET_KEY`, `FLASK_DEBUG`, `FLASK_HOST`, `FLASK_PORT`, `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_SAMESITE`, `MAX_CONTENT_MB`. Upload limit is `MAX_CONTENT_MB` in MB.
- Initialize/reset DB with `python atualizar_bd.py` (backs up `database.db`, seeds admin `admin/admin123`). Run app locally with `python app.py` (or gunicorn via [wsgi.py](../wsgi.py)).

## Auth and roles
- Session fields: `user_id`, `username`, `nome_completo`/`nome_guerra`, `nivel_acesso` (`admin`, `cadastrador`, `visualizador`), optional `orgao_provedor` binding. Decorators `login_required` and `admin_required` enforce access.
- Non-admin users are generally restricted to their own OP records; mirror existing checks when adding routes/actions.
- Passwords are stored with `generate_password_hash`; validate with `check_password_hash`.

## Data model (SQLite)
- Main tables: `orgao_provedor` (one per OP), `usuarios`, `energia_eletrica`, `geradores`, `pessoal`, `viaturas`, `instalacoes`, `empilhadeiras`, `sistemas_seguranca`, `equipamentos_unitizacao`, `fotos`. See [database.py](../database.py) for columns and `atualizar_tabelas()` migrations.
- Always use `database.get_db()` (row_factory rows), `commit()` on success and `rollback()` on exceptions; close happens via `teardown_appcontext`.

## Uploads and files
- Upload root is `app.config['UPLOAD_FOLDER']` defaulting to `static/uploads`; subfolders already created (instalacoes, equipamentos, areas_edificaveis, sistemas_seguranca, equipamentos_unitizacao, viaturas, geradores, empilhadeiras, pessoal).
- Allowed extensions: png, jpg, jpeg, gif, pdf. Use `secure_filename`/`allowed_file()` and respect `MAX_CONTENT_LENGTH`.
- Persist file metadata in `fotos` (fields `tabela_origem`, `registro_id`, `caminho_arquivo`, `tipo_foto`, `descricao`). Access files with `url_for('uploaded_file', filename=...)`.

## Forms and frontend
- `cadastro_op.html` is a tabbed multi-section form for OP creation/edition. Hidden counters (`*_count` inputs) must stay in sync with dynamic lists (instalacoes, viaturas, pessoal, geradores, subitems). JS templates live in the same file; cloning logic is in [static/js/cadastro_completo.js](../static/js/cadastro_completo.js).
- `static/js/script.js` initializes the personnel matrix and seeds initial installation when not editing. Keep JS and template field names aligned (`tipo_instalacao_*`, `viatura_*`, `pessoal_*`).
- OM selection uses `DADOS_OMS` injected via context; functions `preencherOMsSelecionadas`, `adicionarOMsSelecionadas` etc. rely on table structures in the template.
- Dashboard/admin charts and tables (index/admin views) depend on existing fields; when adding/removing columns update the corresponding summaries/exports.

## Behavior and exports
- Auto-fill helpers: `get_dados_automaticos_op`, `get_ug_codom`, `get_subordinacao_by_codom` supply UG/CODOM/subordination and supported OMs; keep new features compatible with these lookups.
- Reports: CSV/Excel exports (`admin_relatorios*` routes) expect current schema; extend them when adding new columns/entities.
- Backups: admin route `admin_backup` streams `database.db` download; do not break path/config assumptions.

## Coding guidelines
- Keep messages and labels in Portuguese; avoid changing existing field names or request keys unless you update all call sites (backend, templates, JS, exports).
- Prefer small helpers over duplicating logic; reuse existing validators (`allowed_file`, role decorators) and data loaders (Excel-driven globals).
- Honor per-role restrictions in new endpoints and templates; block state-changing actions for non-admins unless explicitly allowed.
- When altering data models, update: schema in [database.py](../database.py), seed/update in [atualizar_bd.py](../atualizar_bd.py), form fields/templates, JS serializers, exports, and view serializers that render `visualizar_op`.
- Keep uploads organized under existing subfolders; ensure deletions clean DB rows and disk when relevant (see `delete_foto`).

## Quick QA checklist
- After schema changes: run `python atualizar_bd.py`, verify admin login, create/edit OP with full form (instalacoes, viaturas, pessoal, geradores), upload/remove photos, and export CSV/Excel.
- Confirm CODOM/Dados Excel lookups still populate UG/CODOM/subordination and OM lists.
- Validate role rules: non-admin should be blocked from admin tools and limited to their OP; admin can manage users/backups/exports.
