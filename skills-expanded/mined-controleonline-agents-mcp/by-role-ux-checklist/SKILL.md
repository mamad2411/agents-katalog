# UX Checklist

Base: heuristica de Nielsen (NN/g) + auditoria de jornada **ao vivo no browser**.
Heuristica nao substitui teste com usuario; e o gate interno antes do staging.

Percorra o fluxo na tela real (abrir browser → autenticar se preciso → navegar).

## 1. Visibilidade do status do sistema (H1)

- [ ] Loading / progresso / feedback imediato apos acao
- [ ] Estados de resultado (sucesso, erro) visiveis na tela
- [ ] Nao parece "travado" sem estado

## 2. Linguagem do mundo do cliente (H2)

- [ ] Textos da UI sao do cliente, nao jargao interno de engenharia
- [ ] Ordem da jornada coincide com a tarefa real (ex.: pedido → pagamento → pronto)

## 3. Controle e liberdade (H3)

- [ ] Da para voltar / cancelar no fluxo
- [ ] Acao destrutiva tem confirmacao e nao fica colada na acao primaria

## 4. Consistencia e padroes (H4)

- [ ] Mesma acao = mesmo nome de botao nas telas
- [ ] Padroes do produto (salvar, filtrar, cobrar) nao foram reinventados sem motivo

## 5. Prevencao de erro (H5)

- [ ] Campos obrigatorios evidentes antes do submit
- [ ] Valores perigosos nao sao o default

## 6. Reconhecer, nao lembrar (H6)

- [ ] Opcoes visiveis; usuario nao precisa lembrar codigo/ID da tela anterior
- [ ] Contexto da decisao esta na propria tela

## 7. Eficiencia (H7) + Hick / Fitts

- [ ] Acao primaria e o alvo mais obvio (tamanho/posicao)
- [ ] Tela nao despeja 10 decisoes do mesmo peso ao mesmo tempo

## 8. Design minimo (H8) + ajuda no ponto certo (H10)

- [ ] Informacao secundaria fora do caminho critico
- [ ] Explicacao extensa **nao** ocupa o layout; vive no **"?"** / help contextual
- [ ] Empty state diz o que fazer agora (com CTA), nao so ilustracao

## 9. Erro recuperavel (H9)

- [ ] Mensagem de erro esta perto do problema e fala o proximo passo
- [ ] Falha nao apaga o trabalho ja preenchido (quando a tela permitir julgar)

## 10. Jornada completa

- [ ] Fluxo percorrido cobre inicio → acao da issue → resultado na tela real

## Decisao

Qualquer `fail` em jornada de produto → `agent:ux:rejected`.
Todos `ok` ou `n/a` justificados → `agent:ux:accepted`.
