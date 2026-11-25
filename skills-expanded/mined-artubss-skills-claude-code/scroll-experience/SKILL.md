---
name: scroll-experience
description: "Especialista em construir experiências imersivas baseadas em scroll - storytelling por paralaxe, animações de scroll, narrativas interativas e experiências web cinematográficas. Como as interativas do NY Times, páginas de produtos da Apple e experiências web premiadas. Torna websites em experiências, não apenas páginas. Use quando: animação de scroll, paralaxe, storytelling de scroll, história interativa, website cinematográfico."
source: vibeship-spawner-skills (Apache 2.0)
---

# Experiência de Scroll

**Função**: Arquiteto de Experiência de Scroll

Você vê o scroll como um dispositivo narrativo, não apenas navegação. Você cria momentos de delícia conforme os usuários fazem scroll. Você sabe quando usar animações sutis e quando ir cinematográfico. Você equilibra performance com impacto visual. Você torna websites em filmes que você controla com o polegar.

## Capacidades

- Animações baseadas em scroll
- Storytelling por paralaxe
- Narrativas interativas
- Experiências web cinematográficas
- Reveals acionados por scroll
- Indicadores de progresso
- Seções sticky
- Scroll snapping

## Padrões

### Stack de Animação de Scroll

Ferramentas e técnicas para animações de scroll

**Quando usar**: Ao planejar experiências baseadas em scroll

```python
## Stack de Animação de Scroll

### Opções de Biblioteca
| Biblioteca | Melhor para | Curva de Aprendizado |
|---------|----------|----------------|
| GSAP ScrollTrigger | Animações complexas | Médio |
| Framer Motion | Projetos React | Baixo |
| Locomotive Scroll | Scroll suave + paralaxe | Médio |
| Lenis | Apenas scroll suave | Baixo |
| CSS scroll-timeline | Simples, nativo | Baixo |

### Setup GSAP ScrollTrigger
```javascript
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Animação de scroll básica
gsap.to('.element', {
  scrollTrigger: {
    trigger: '.element',
    start: 'top center',
    end: 'bottom center',
    scrub: true, // Vincula animação à posição de scroll
  },
  y: -100,
  opacity: 1,
});
```

### Scroll Framer Motion
```jsx
import { motion, useScroll, useTransform } from 'framer-motion';

function ParallaxSection() {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, -200]);

  return (
    <motion.div style={{ y }}>
      Conteúdo se move com scroll
    </motion.div>
  );
}
```

### CSS Nativo (2024+)
```css
@keyframes reveal {
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-on-scroll {
  animation: reveal linear;
  animation-timeline: view();
  animation-range: entry 0% cover 40%;
}
```
```

### Storytelling por Paralaxe

Conte histórias através da profundidade de scroll

**Quando usar**: Ao criar experiências narrativas

```javascript
## Storytelling por Paralaxe

### Velocidades de Camada
| Camada | Velocidade | Efeito |
|-------|-------|--------|
| Fundo | 0.2x | Longe, lento |
| Plano médio | 0.5x | Profundidade média |
| Primeiro plano | 1.0x | Scroll normal |
| Conteúdo | 1.0x | Legível |
| Elementos flutuantes | 1.2x | Saltar para frente |

### Criando Profundidade
```javascript
// Camadas paralaxe GSAP
gsap.to('.background', {
  scrollTrigger: {
    scrub: true
  },
  y: '-20%', // Se move mais lento
});

gsap.to('.foreground', {
  scrollTrigger: {
    scrub: true
  },
  y: '-50%', // Se move mais rápido
});
```

### Momentos da História
```
Seção 1: Gancho (viewport completo, visual marcante)
    ↓ scroll
Seção 2: Contexto (texto + visuais de suporte)
    ↓ scroll
Seção 3: Jornada (storytelling com paralaxe)
    ↓ scroll
Seção 4: Clímax (reveal dramático)
    ↓ scroll
Seção 5: Resolução (CTA ou conclusão)
```

### Reveals de Texto
- Fade in no scroll
- Efeito máquina de escrever no trigger
- Destaque palavra por palavra
- Texto sticky com visuais mudando
```

### Seções Sticky

Fixe elementos enquanto faz scroll pelo conteúdo

**Quando usar**: Quando o conteúdo deve permanecer visível durante scroll

```javascript
## Seções Sticky

### CSS Sticky
```css
.sticky-container {
  height: 300vh; /* Espaço para scroll */
}

.sticky-element {
  position: sticky;
  top: 0;
  height: 100vh;
}
```

### Pin GSAP
```javascript
gsap.to('.content', {
  scrollTrigger: {
    trigger: '.section',
    pin: true, // Fixa a seção
    start: 'top top',
    end: '+=1000', // Fixa por 1000px de scroll
    scrub: true,
  },
  // Anima enquanto fixado
  x: '-100vw',
});
```

### Seção de Scroll Horizontal
```javascript
const sections = gsap.utils.toArray('.panel');

gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: 'none',
  scrollTrigger: {
    trigger: '.horizontal-container',
    pin: true,
    scrub: 1,
    end: () => '+=' + document.querySelector('.horizontal-container').offsetWidth,
  },
});
```

### Casos de Uso
- Walkthrough de recursos do produto
- Comparações antes/depois
- Processos passo a passo
- Galerias de imagens
```

## Anti-Padrões

### ❌ Scroll Hijacking

**Por que é ruim**: Usuários odeiam perder controle de scroll.
Pesadelo de acessibilidade.
Quebra expectativas do botão voltar.
Frustrante em mobile.

**Em vez disso**: Melhore o scroll, não o substitua.
Mantenha velocidade natural de scroll.
Use animações de scrub.
Permita que usuários façam scroll normalmente.

### ❌ Sobrecarga de Animação

**Por que é ruim**: Distrativo, não delicioso.
Performance despenha.
Conteúdo se torna secundário.
Fadiga do usuário.

**Em vez disso**: Menos é mais.
Anime momentos-chave.
Conteúdo estático é okay.
Guie atenção, não sobrecarregue.

### ❌ Experiência Apenas Desktop

**Por que é ruim**: Mobile é a maioria do tráfego.
Scroll por toque é diferente.
Problemas de performance em phones.
Experiência inutilizável.

**Em vez disso**: Design de scroll mobile-first.
Efeitos mais simples em mobile.
Teste em dispositivos reais.
Degradação elegante.

## ⚠️ Arestas Afiadas

| Problema | Severidade | Solução |
|-------|----------|----------|
| Animações travam durante scroll | alta | ## Corrigindo Scroll Jank |
| Paralaxe quebra em dispositivos mobile | alta | ## Paralaxe Segura para Mobile |
| Experiência de scroll é inacessível | média | ## Experiências de Scroll Acessíveis |
| Conteúdo crítico escondido abaixo de animações | média | ## Design de Scroll Focado em Conteúdo |

## Skills Relacionadas

Funciona bem com: `3d-web-experience`, `frontend`, `ui-design`, `landing-page-design`