# .clinerules — Planet9 Screening Lab

Este projeto é uma pipeline científica auditável (triagem dinâmica de
candidatos ao Planeta Nove). Precisão, rastreabilidade e honestidade
epistêmica pesam mais que velocidade. Estas regras valem para QUALQUER
agente executor (Cline, Hermes, Antigravity, ou outro), em qualquer
perfil (Auditor ou Executor), rodando neste repositório.

## Ambiente
- Pasta do projeto: confirme o caminho real do projeto no início de cada
  sessão (pwd/Get-Location) — o repositório já foi usado em pelo menos
  3 máquinas/caminhos diferentes (H:\planet9-screening-lab,
  D:\planet9-screening-lab, D:\ATLETA DO ANO\planet9-screening-lab).
  Nunca assuma uma letra de unidade ou caminho fixo; use sempre o
  caminho detectado nesta sessão.
- venv já ativo antes de qualquer sessão. Se `python main.py doctor` falhar
  ou o venv parecer quebrado (Python não encontrado, base ausente), pare e
  reporte antes de tentar reconstruir sozinho às cegas.
- O clone de referência OSSOS (código-fonte Fortran do SurveySimulator,
  usado como base para portes fiéis como
  planet9lab/geometry/poly_footprint.py), se presente nesta máquina
  (verifique com Test-Path antes de assumir o caminho), é READ-ONLY.
  Nunca editar ou deletar nada ali.

## Gate obrigatório (início e fim de toda tarefa)
1. `python -m pytest -q` → deve bater o número de testes já esperado
   (confirme o baseline atual — ver TASK.md ou o último commit — antes de
   mudar algo). Se não bater, PARE.
2. `python -m ruff check .` → deve passar limpo ("All checks passed!").
Nunca declare uma tarefa concluída sem rodar os dois comandos ao final
e reportar a saída literal.

## Canal de comunicação entre Auditor e Executor
- Arquivo único: `TASK.md` na raiz do projeto.
- O Auditor escreve/sobrescreve o plano. O Executor só edita as seções
  "Bloqueios" e "Log de execução" desse mesmo arquivo.
- Nunca acumular versões antigas de plano — sempre a versão vigente.
- **Ao iniciar qualquer sessão (mesmo que pareça continuação de uma
  conversa anterior), releia TASK.md e rode `git log -5 --oneline` +
  `git status` antes de agir.** O repositório circula entre várias
  máquinas: a sessão anterior pode ter rodado em outra máquina, então a
  memória de conversa do agente não é garantia de estado atualizado —
  só o disco é.

## Disciplina científica (herdada do artigo/política de conclusão do repo)
- Nenhuma alteração de código pode, por si, mudar a interpretação dos
  resultados sem dizer isso explicitamente no TASK.md e no PR/commit.
- Vocabulário permitido para conclusões: "triagem exploratória",
  "candidato de interesse dentro do protocolo", "nenhum candidato
  encontrado", "inconclusivo". PROIBIDO usar "confirmado", "descoberta"
  ou "órbita determinada" em qualquer texto gerado (código, docstring,
  commit message, relatório).
- Toda constante física/orbital nova (massas, elementos, épocas, filling
  factors, parâmetros de eficiência etc.) precisa vir com atribuição de
  fonte (arquivo original + linha, ou referência bibliográfica). Nunca
  inventar ou "arredondar de memória" um valor científico.
- Nunca copiar um arquivo de dados de terceiros (.eff, .list, README)
  na íntegra — extrair só os valores necessários, com atribuição.
- Resultado desfavorável ou pendência real (ex. execução ainda não feita,
  significância estatística não atingida) é reportado com o mesmo peso que
  um resultado favorável — nunca suavizado, nunca escondido.

## Disciplina de código
- Nunca editar arquivos fora do escopo declarado na tarefa.
- Nunca remover ou enfraquecer um teste para fazê-lo passar — se um
  teste falha, o problema é no código ou na tarefa, não no teste.
- Mudanças em unidades (graus vs horas, radianos vs graus, UA, JD etc.)
  exigem verificação explícita contra o código-fonte original antes de
  serem assumidas — erros de unidade já ocorreram neste projeto.

## Relatório final (toda tarefa)
Todo encerramento de tarefa (por qualquer perfil) deve reportar:
- Resultado do gate (antes e depois).
- Lista exata de arquivos criados/alterados.
- Qualquer ambiguidade encontrada e como foi resolvida (ou por que foi
  escalada em vez de assumida).
- Commit git correspondente (hash), feito ao final de cada tarefa
  concluída — não só ao fim da sessão inteira.

## Continuidade (execução autônoma de longa duração)
Este projeto nunca está "concluído". Ao esgotar o plano vigente em
TASK.md, o perfil Executor não deve parar e esperar instrução — deve:
1. Reler as seções de limitações conhecidas do projeto (docs/LIMITACOES.md)
   e propor ao Auditor (ou, na ausência de um Auditor ativo na sessão,
   registrar em TASK.md como proposta) o próximo item de valor a atacar.
2. Nunca iniciar uma execução cara/longa (ex. integração secular de várias
   horas) sem essa estar explicitamente registrada como autorizada em
   TASK.md.
3. Se genuinamente não houver próximo passo óbvio, documentar isso em
   TASK.md com a justificativa, em vez de simplesmente parar sem explicação.

## Rotação de modelo (quando os tokens/rate limit de um provedor acabarem)
A lista de modelos disponíveis varia por ferramenta/conta — o que importa
é o princípio, não a lista específica. A troca pode ser manual ou
automática, conforme a ferramenta, mas o agente deve executá-la
sozinho, sem esperar o usuário clicar. Antes de trocar: escrever o
estado atual em TASK.md (seção "Log de execução"), commitar todo
trabalho em andamento (mesmo parcial, com mensagem indicando
checkpoint), depois trocar de modelo. Ao assumir como novo modelo:
reler TASK.md e `git log -5 --oneline` antes de continuar — nunca
reiniciar do zero nem repetir trabalho já commitado.

(Nota histórica, não normativa — exemplo válido em uma sessão
específica: em 2026-09, na conta Cline, os modelos free em ordem de
prioridade eram 1. DeepSeek V4 Flash (`deepseek/deepseek-v4-flash`,
1M contexto); 2. GLM-5.3-Flash; 3. LongCat 2.0; 4. Laguna S 2.1.)