---
name: manuseio-segredos
description: Protocolo para manusear chaves de API, senhas e credenciais reais com agentes de IA — onde vivem, as proibições absolutas, como verificar presença sem imprimir valor, e a varredura antes de encerrar. Carregar SEMPRE que a tarefa envolver chave real, o arquivo .env, cofre de segredos, ou qualquer valor que não possa vazar para repositório, log ou contexto do agente.
---

# Manuseio de segredos

O contexto de um agente é um log: tudo que passa pelo stdout de um comando entra nele, e pode ir parar em transcript, resumo de compactação, mensagem de commit ou relatório. Segredo que toca o stdout já vazou.

## Onde os segredos vivem

- Arquivo `.env` na raiz, **ignorado pelo git** (confira com `git check-ignore -v .env`).
- Cofre/banco cifrado do produto, quando houver.
- Nunca: arquivo versionado, fixture, exemplo de documentação, CHANGELOG, mensagem de commit, PR, spec, log colado — em repositório nenhum.

`.env.example` existe só com NOMES e valores de exemplo inválidos.

## As proibições absolutas

1. Nunca imprimir o valor (`cat .env`, `echo $CHAVE`, `printenv`, `grep CHAVE .env`).
2. Nunca passar o valor em `argv` (aparece em `ps` e no histórico) — use STDIN ou variável de ambiente do processo filho.
3. Nunca gravar em arquivo intermediário fora do lugar previsto.
4. Nunca hardcode, nem "temporário".

## Como verificar sem ver

```bash
grep -c '^NOME_DA_CHAVE=' .env          # presença (1/0), sem valor
awk -F= '/^NOME=/{print length($2)}' .env   # comprimento, para checar formato
```

Diagnóstico de autenticação: use chave inválida de propósito para provar URL/auth/parsing do provedor, sem gastar a real (a resposta 401 prova o caminho).

## Scanner de segredo: exceção item a item

Baseline por fingerprint (`commit:arquivo:regra:linha`), versionado e com valores `REDACTED` — nunca allowlist por caminho, que desliga a regra no arquivo inteiro. Caso de origem: a allowlist por caminho detectava 1 de 2 canários; o baseline, 2 de 2. Um scanner que degrada em silêncio é pior que nenhum, porque passa confiança. Prove o baseline com canários sintéticos nos dois sentidos.

## Checklist antes de encerrar

1. `.env` não rastreado e ignorado (raiz e cada repositório).
2. Nunca esteve no histórico: `git log --all --full-history -- .env` vazio.
3. Varredura por prefixos conhecidos de chave em arquivos versionados de cada repositório.
4. Nada de valor em transcript, commit, PR ou relatório desta sessão.

## Se vazou

Trate como incidente: tire do histórico antes de qualquer push, revogue/rotacione a credencial, avise o dono. Valor que chegou a um remoto deve ser considerado comprometido mesmo depois de apagado.
