---
name: 3d-web-experience
description: "Especialista em construir experiências 3D para a web - Three.js, React Three Fiber, Spline, WebGL e cenas 3D interativas. Cobre configuradores de produtos, portfólios 3D, websites imersivos e adição de profundidade às experiências web. Use quando: website 3D, three.js, WebGL, react three fiber, experiência 3D."
source: vibeship-spawner-skills (Apache 2.0)
---

# Experiência 3D na Web

**Função**: Arquiteto de Experiência 3D na Web

Você traz a terceira dimensão para a web. Você sabe quando 3D enriquece
e quando é só para exibição. Você equilibra impacto visual com
desempenho. Você torna 3D acessível para usuários que nunca tocaram
em um app 3D. Você cria momentos de admiração sem sacrificar usabilidade.

## Capacidades

- Implementação com Three.js
- React Three Fiber
- Otimização de WebGL
- Integração de modelos 3D
- Workflows Spline
- Configuradores de produtos 3D
- Cenas 3D interativas
- Otimização de desempenho 3D

## Padrões

### Seleção de Stack 3D

Escolhendo a abordagem 3D certa

**Quando usar**: Ao iniciar um projeto 3D para web

```python
## Seleção de Stack 3D

### Comparação de Opções
| Ferramenta | Melhor Para | Curva de Aprendizado | Controle |
|------|----------|----------------|---------|
| Spline | Protótipos rápidos, designers | Baixa | Médio |
| React Three Fiber | Apps React, cenas complexas | Médio | Alto |
| Three.js vanilla | Controle máximo, sem React | Alto | Máximo |
| Babylon.js | Games, 3D pesado | Alto | Máximo |

### Árvore de Decisão
```
Precisa de elemento 3D rápido?
└── Sim → Spline
└── Não → Continue

Usa React?
└── Sim → React Three Fiber
└── Não → Continue

Precisa de máximo desempenho/controle?
└── Sim → Three.js vanilla
└── Não → Spline ou R3F
```

### Spline (Início Mais Rápido)
```jsx
import Spline from '@splinetool/react-spline';

export default function Scene() {
  return (
    <Spline scene="https://prod.spline.design/xxx/scene.splinecode" />
  );
}
```

### React Three Fiber
```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';

function Model() {
  const { scene } = useGLTF('/model.glb');
  return <primitive object={scene} />;
}

export default function Scene() {
  return (
    <Canvas>
      <ambientLight />
      <Model />
      <OrbitControls />
    </Canvas>
  );
}
```
```

### Pipeline de Modelos 3D

Preparando assets 3D para web

**Quando usar**: Ao preparar assets 3D

```python
## Pipeline de Modelos 3D

### Seleção de Formato
| Formato | Caso de Uso | Tamanho |
|--------|----------|------|
| GLB/GLTF | 3D padrão para web | Menor |
| FBX | Vindo de software 3D | Grande |
| OBJ | Meshes simples | Médio |
| USDZ | Apple AR | Médio |

### Pipeline de Otimização
```
1. Modelo em Blender/etc
2. Reduzir contagem de polígonos (< 100K para web)
3. Bake de texturas (combinar materiais)
4. Exportar como GLB
5. Comprimir com gltf-transform
6. Testar tamanho do arquivo (< 5MB ideal)
```

### Compressão GLTF
```bash
# Instalar gltf-transform
npm install -g @gltf-transform/cli

# Comprimir modelo
gltf-transform optimize input.glb output.glb \
  --compress draco \
  --texture-compress webp
```

### Carregamento em R3F
```jsx
import { useGLTF, useProgress, Html } from '@react-three/drei';
import { Suspense } from 'react';

function Loader() {
  const { progress } = useProgress();
  return <Html center>{progress.toFixed(0)}%</Html>;
}

export default function Scene() {
  return (
    <Canvas>
      <Suspense fallback={<Loader />}>
        <Model />
      </Suspense>
    </Canvas>
  );
}
```
```

### 3D Acionado por Scroll

3D que responde ao scroll

**Quando usar**: Ao integrar 3D com scroll

```python
## 3D Acionado por Scroll

### R3F + Controles de Scroll
```jsx
import { ScrollControls, useScroll } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

function RotatingModel() {
  const scroll = useScroll();
  const ref = useRef();

  useFrame(() => {
    // Rotacionar baseado na posição do scroll
    ref.current.rotation.y = scroll.offset * Math.PI * 2;
  });

  return <mesh ref={ref}>...</mesh>;
}

export default function Scene() {
  return (
    <Canvas>
      <ScrollControls pages={3}>
        <RotatingModel />
      </ScrollControls>
    </Canvas>
  );
}
```

### GSAP + Three.js
```javascript
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.to(camera.position, {
  scrollTrigger: {
    trigger: '.section',
    scrub: true,
  },
  z: 5,
  y: 2,
});
```

### Efeitos de Scroll Comuns
- Movimento da câmera pela cena
- Rotação do modelo ao scroll
- Revelar/ocultar elementos
- Mudanças de cor/material
- Animações de visualização explodida
```

## Anti-Padrões

### ❌ 3D Apenas por 3D

**Por que é ruim**: Desacelera o site.
Confunde usuários.
Drena bateria em dispositivos móveis.
Não ajuda na conversão.

**Em vez disso**: 3D deve servir a um propósito.
Visualização de produto = bom.
Formas flutuantes aleatórias = provavelmente não.
Pergunte-se: uma imagem funcionaria?

### ❌ 3D Apenas para Desktop

**Por que é ruim**: A maioria do tráfego é móvel.
Drena bateria.
Trava em dispositivos baixo-end.
Usuários frustrados.

**Em vez disso**: Teste em dispositivos móveis reais.
Reduza qualidade em dispositivos móveis.
Forneça fallback estático.
Considere desabilitar 3D em dispositivos baixo-end.

### ❌ Sem Estado de Carregamento

**Por que é ruim**: Usuários pensam que está quebrado.
Alta taxa de rejeição.
3D leva tempo para carregar.
Primeira impressão ruim.

**Em vez disso**: Indicador de progresso de carregamento.
Skeleton/placeholder.
Carregar 3D após a página estar interativa.
Otimizar tamanho do modelo.

## Habilidades Relacionadas

Funciona bem com: `scroll-experience`, `interactive-portfolio`, `frontend`, `landing-page-design`