# Operational Source of Truth

## Overview

Use esta skill quando o trabalho depender de descobrir ou confirmar:

- servidores e servicos corretos
- hosts, portas e bases
- credenciais indiretas e parametros operacionais
- janelas e frequencia de execucao
- tabelas de controle operacional e historico de execucao

## Workflow

1. trate o banco principal e os arquivos de ambiente anexados ao agent como fontes de verdade primarias para descoberta operacional
2. use essas fontes para identificar o alvo correto antes de agir
3. confirme ambiente, tenant, servico, escopo e parametros relevantes antes de concluir ou executar acoes
4. se houver divergencia entre historico salvo, estado atual do ambiente, banco principal e outras fontes auxiliares, priorize a verificacao do estado real e registre a inconsistencia
5. trate arquivos de ambiente e credenciais como sensiveis em todo o fluxo

## Output Contract

Ao concluir, informe objetivamente:

- qual fonte confirmou o alvo
- qual ambiente, servico ou servidor foi validado
- quais inconsistencias foram encontradas
- quais parametros operacionais relevantes foram confirmados

## Quality Bar

- nao adivinhe alvos operacionais
- nao trate fonte auxiliar como superior a fonte de verdade
- nao exponha credenciais, segredos ou conteudo sensivel
- sempre valide o escopo correto antes de agir
