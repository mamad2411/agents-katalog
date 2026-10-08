---
name: animation-review
description: Evaluates purpose, timing, easing, hierarchy, continuity, interruption, accessibility, and reduced motion compliance of every animation in the interface.
license: MIT
metadata:
    aes-category: frontend
    aes-priority: medium
---

# Animation Review

## Objective

Ensinar o agente a avaliar animações contra princípios de motion design: propósito,
timing, easing, hierarquia, continuidade, interrupção, acessibilidade, e reduced
motion. Toda animação deve ter uma razão de existir; se não serve à função, é ruído.

## When to Use

* Em qualquer interface com animações, transições, micro-interações, parallax,
  loaders, ou motion.
* Quando o pedido menciona "animation", "motion", "transitions", "easing", "timing",
  "reduced motion", "parallax".
* **Composição:** roda com `interaction-design` (transições e feedback de estado),
  `accessibility-review` (reduced motion, vestibular), e `ux-review` (animação que
  informa vs distrai). Consulta `references/frontend.yaml` (Animate UI, Impeccable,
  Interfaces).

## Mental Model

Animação não é decoração — é **comunicação**. Toda animação deve responder a uma
pergunta do usuário (o que aconteceu? para onde vai? o que mudou?). Se não responde,
é ruído visual.

Os eixos (do `plan.md` §10):

```text
purpose          — a animação comunica algo? (mudança de estado, navegação, feedback)
timing           — duração correta para o que comunica (muito rápida = imperceptível;
                   muito lenta = frustrante)
easing           — a curva de aceleração é natural? (ease-out para entrada, ease-in
                   para saída, spring para interação)
hierarchy        — animações mais importantes são mais rápidas/notáveis que as menos
                   importantes
continuity       — elementos não teleportam; o movimento é contínuo entre estados
interruption    — a animação pode ser interrompida? (se o usuário clica de novo, o
                   que acontece?)
accessibility    — a animação respeita `prefers-reduced-motion`?
reduced motion   — cores e transições não causam desconforto visual (vestibular,
                   epilepsy)
```

## Investigation Procedure

1. **Inventariar animações** — carregamento, transição de página, hover, expansão,
   entrada/saída, loader, parallax, scroll-triggered.
2. **Para cada, avaliar propósito** — comunica uma mudança de estado, direção, hierarquia?
   Ou é decorativa sem função? ("animation for its own sake")
3. **Avaliar timing** — durações consistentes? (50-100ms para feedback, 200-300ms para
   transição de página, > 500ms só para storytelling). Todas as animações similares
   têm a mesma duração?
4. **Avaliar easing** — a curva de aceleração é natural? (ease-out para entrada de
   objetos, ease-in para saída, spring para interação tátil). Ou é linear (robótica)?
5. **Avaliar hierarchy** — a animação principal é mais rápida que as secundárias? Ou
   tudo anima junto no mesmo tempo?
6. **Avaliar continuity** — elementos teleportam entre estados? (não: movimento
   contínuo é esperado). Exemplo: modal abre sem transição, item some sem fade.
7. **Avaliar interruption** — se o usuário clica de novo, a animação reinicia ou
   inverte suavemente? Ou trava/empilha?
8. **Avaliar reduced motion** — `@media (prefers-reduced-motion: reduce)` é respeitado?
   Animações sensíveis (parallax, scroll, flutuação) são desligadas? Há botão de
   desligar motion no app?
9. **Avaliar desconforto** — parallax acentuado, flutuação constante, scroll-triggered
   que compete com scroll, loading animation que vibra. Causa desconforto vestibular?
10. **Sintetizar** — referenciar `references/frontend.yaml` (Animate UI, Impeccable)
    quando apropriado.

## Questions to Ask

* Esta animação tem propósito? (comunica algo, ou só "enfeita"?)
* Duração é apropriada? (feedback rápido, transição suave, storytelling lento?)
* Easing é natural (ease-out/spring) ou linear (robótica)?
* Animações similares têm a mesma duração e easing? (consistência)
* A animação mais importante é mais rápida que as secundárias? (hierarchy)
* Elementos teleportam ou se movem continuamente? (continuity)
* Se o usuário clica de novo, a animação interrompe suavemente? (interruption)
* `prefers-reduced-motion` é respeitado? (accessibility)
* Alguma animação causa desconforto visual? (parallax/scroll não-controlado)

## Attack Patterns

```text
purpose absent
    entrada de sidebar com fade+slide quando o conteúdo não mudou → por quê?
    (animação decorativa sem função comunicativa)

timing wrong
    hover de botão: 300ms (muito longo para feedback que deve ser < 100ms)
    transição de página: 100ms (muito rápido, não comunica navegação)
    loader: 10s (nunca deve; se > 10s, erro)

easing linear
    todas as animações usam `ease` ou `linear`
    → movimento robótico, sem naturalidade; falta spring/ease-out

hierarchy inverted
    micro-interação de ícone (secundária) anima 300ms
    transição de página (principal) anima 100ms
    → hierarquia invertida; o principal parece menos importante

continuity broken
    modal aparece sem transição (teleport)
    item some antes de sair da tela (corte abrupto)
    → desorientação, perda de contexto

interruption broken
    clique em botão → animação de 300ms
    clique de novo no meio → animação reinicia do início (trava) ou empilha (2×)
    → deveria interromper e inverter suavemente

reduced motion ignored
    parallax no hero com `prefers-reduced-motion: reduce`
    → ainda anima, causa desconforto vestibular

vestibular risk
    paralaxe acentuado em background de scroll-triggered
    flutuação constante de CTA (sobe e desce para sempre)
    loading spinner com rotação rápida + contraste alto
```

## Evidence Requirements

* **Nomear a animação e o eixo** (propósito/timing/easing/hierarchy/continuity/
  interruption/accessibility/reduced motion).
* **Mostrar os valores exatos** (timing em ms, easing function, CSS/JS da animação).
* **Escalar confiança (Animation Review):**
  * `CONFIRMED` — animação sem propósito, timing errado, easing linear, hierarchy
    invertida, continuity quebrada, reduced motion não respeitado.
  * `HIGH CONFIDENCE` — violação clara de princípio.
  * `POSSIBLE` — questão de nuance (timing marginalmente longo).
  * `SPECULATIVE` — preferência pessoal.

## False Positives

* **Animação de marca com propósito** — animações de marca (logo, loading) podem ser
  mais longas e expressivas por design. Avaliar se servem à identidade ou são ruído.
* **Timing varia por plataforma** — mobile vs desktop podem ter durações diferentes.
  Não reportar "inconsistência" entre plataformas sem considerar o contexto.
* **Reduced motion parcial** — se o app respeita reduced motion para as animações
  principais, omitir de micro-interações pode ser aceitável. Marcar como melhoria.
* **Parallax com fallback** — se parallax desliga em reduced motion, é aceitável.
  Confirmar o fallback.
* **Easing linear intencional** — progress bar, skeleton, ou loader podem ser lineares
  intencionalmente. Não reportar como erro.

## Output Format

Para cada animação que viola um princípio, um finding via `templates/audit-report.md`.
Em **Affected component**, nomeie a animação. Em **Reproduction**, descreva o que o
usuário vê vs o esperado (timing, easing, continuity, etc.). Em **Root cause**, aponte
o eixo violado. Em **Recommendation**, dê a correção (timing, easing, respectar
reduced motion, adicionar continuity, interrompção suave, remover animação sem
propósito).

Apresente por eixo. Reduced motion e vestibular (acessibilidade/desconforto) primeiro;
purpose e continuity depois; timing/easing/hierarchy em seguida; interruption por
último.
