# Checklist — Sistema / Aplicação (Developer)

Checklist **incrementável** usado quando o `sysadmin` (ou a operação) detecta problema **no software de produto** e abre task com `agent:developer`.

> O sysadmin **não corrige código**. Ele cria a issue, cola este checklist (ou os itens relevantes) e evidencia sanitizada.  
> Infra de servidor (SO, pacotes do host, SSH) → `checklist-server.md` + `agent:sysadmin`.

## 0. Contexto da task (preenchido por quem abre)

- [ ] Título objetivo do sintoma (não o chute da causa)
- [ ] Ambiente (prod / staging / tenant) **sem** dados sensíveis
- [ ] Hostname/serviço apenas se necessário e não secreto
- [ ] Janela temporal do erro (de/até)
- [ ] Frequência (único / intermitente / contínuo)
- [ ] Link ou referência interna sanitizada (issue mãe, deploy, etc.)

## 1. Evidência de aplicação

- [ ] Trecho de log de aplicação relevante (stack trace **sanitizado**: sem tokens, PII, payloads completos)
- [ ] Endpoint / fila / job / comando envolvido
- [ ] Código HTTP ou código de erro de domínio, se houver
- [ ] Correlação com deploy recente ou mudança de config (se souber)
- [ ] Reprodução conhecida ou “não reproduzido, só em log”

## 2. Classificação

- [ ] Bug funcional / regressão
- [ ] Erro de integração com ferramenta externa (API terceira, e-mail, pagamento…)
- [ ] Dependência de código desatualizada ou vulnerável no repositório (`composer` / `npm` / lockfile)
- [ ] Configuração de aplicação (env de app, feature flag) — **não** patch de SO
- [ ] Performance / timeout / memory no processo da app

## 3. Ação esperada do Developer

- [ ] Reproduzir ou confirmar pelo log/teste
- [ ] Corrigir no repositório correto (multi-repo: listar módulos suspeitos)
- [ ] Atualizar versão de biblioteca **no código** (manifest + lock) quando for o caso
- [ ] Branch `task-{id}`, **merge em `dev`** conforme fluxo do `developer` (não em `staging`)
- [ ] Não commitar segredos; não logar PII

## 4. Critério de pronto (para o dev marcar na issue)

- [ ] Causa raiz descrita em comentário (sem dados sensíveis)
- [ ] Correção merged em **`dev`** (ou justificativa)
- [ ] Como validar em um passo
- [ ] Riscos residuais

## 5. Itens típicos de “versão no código”

- [ ] Manifest (`package.json`, `composer.json`, etc.) desatualizado em relação ao desejado/security advisory
- [ ] Lockfile inconsistente
- [ ] Breaking change mapeada e plano de ajuste de código
- [ ] Build/CI passando após o bump

## Itens futuros (backlog do checklist)

_Adicionar aqui novos itens conforme a operação evoluir:_

- [ ] _(vazio — incrementar)_ 
