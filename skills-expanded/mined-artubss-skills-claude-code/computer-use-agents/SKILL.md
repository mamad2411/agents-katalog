---
name: computer-use-agents
description: "Construa agentes de IA que interagem com computadores como humanos fazem - visualizando telas, movimentando cursores, clicando botões e digitando texto. Cobre Computer Use da Anthropic, Operator/CUA da OpenAI e alternativas de código aberto. Foco crítico em sandboxing, segurança e tratamento dos desafios únicos do controle baseado em visão. Use quando: computer use, automação de desktop agent, controle de tela IA, agente baseado em visão, automação de GUI."
source: vibeship-spawner-skills (Apache 2.0)
---

# Computer Use Agents

## Padrões

### Loop de Percepção-Raciocínio-Ação

A arquitetura fundamental de agentes de computer use: observar tela,
raciocinar sobre a próxima ação, executar ação, repetir. Este loop integra
modelos de visão com execução de ações através de um pipeline iterativo.

Componentes-chave:
1. PERCEPÇÃO: Captura de screenshot do estado atual da tela
2. RACIOCÍNIO: Modelo de visão-linguagem analisa e planeja
3. AÇÃO: Executa operações de mouse/teclado
4. FEEDBACK: Observa resultado, continua ou corrige

Insight crítico: Agentes de visão ficam completamente parados durante a fase de "pensamento"
(1-5 segundos), criando um padrão de pausa detectável.

**Quando usar**: ['Construindo qualquer agente de computer use do zero', 'Integrando modelos de visão com controle de desktop', 'Entendendo padrões de comportamento de agentes']

```python
from anthropic import Anthropic
from PIL import Image
import base64
import pyautogui
import time

class ComputerUseAgent:
    """
    Implementação do loop de Percepção-Raciocínio-Ação.
    Baseado em padrões Computer Use da Anthropic.
    """

    def __init__(self, client: Anthropic, model: str = "claude-sonnet-4-20250514"):
        self.client = client
        self.model = model
        self.max_steps = 50  # Prevenir loops descontrolados
        self.action_delay = 0.5  # Segundos entre ações

    def capture_screenshot(self) -> str:
        """Captura tela e retorna imagem codificada em base64."""
        screenshot = pyautogui.screenshot()
        # Redimensiona para eficiência de tokens (1280x800 é bom balanço)
        screenshot = screenshot.resize((1280, 800), Image.LANCZOS)

        import io
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    def execute_action(self, action: dict) -> dict:
        """Executa ação de mouse/teclado no computador."""
        action_type = action.get("type")

        if action_type == "click":
            x, y = action["x"], action["y"]
            button = action.get("button", "left")
            pyautogui.click(x, y, button=button)
            return {"success": True, "action": f"clicou em ({x}, {y})"}

        elif action_type == "type":
            text = action["text"]
            pyautogui.typewrite(text, interval=0.02)
            return {"success": True, "action": f"digitou {len(text)} caracteres"}

        elif action_type == "key":
            key = action["key"]
            pyautogui.press(key)
            return {"success": True, "action": f"pressionou {key}"}

        elif action_type == "scroll":
            direction = action.get("direction", "down")
            amount = action.get("amount", 3)
            scroll = -amount if direction == "down" else amount
            pyautogui.scroll(scroll)
            return {"success": True, "action": f"rolou {direction}"}
```

### Padrão de Ambiente Sandboxed

Agentes de computer use DEVEM rodar em ambientes isolados, sandboxed.
Nunca dê aos agentes acesso direto ao seu sistema principal - os riscos
de segurança são muito altos. Use containers Docker com desktops virtuais.

Requisitos-chave de isolamento:
1. REDE: Restringir a endpoints necessários apenas
2. FILESYSTEM: Somente leitura ou escopo para diretórios temporários
3. CREDENCIAIS: Sem acesso a credenciais do host
4. SYSCALLS: Filtrar system calls perigosas
5. RECURSOS: Limitar CPU, memória, tempo

O objetivo é "minimização de raio de explosão" - se o agente falhar,
danos ficam contidos no sandbox.

**Quando usar**: ['Deployando qualquer agente de computer use', 'Testando comportamento do agente com segurança', 'Executando tarefas de automação não confiáveis']

```python
# Dockerfile para ambiente sandboxed de computer use
# Baseado no padrão de implementação de referência da Anthropic

FROM ubuntu:22.04

# Instala ambiente desktop
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    fluxbox \
    xterm \
    firefox \
    python3 \
    python3-pip \
    supervisor

# Segurança: Criar usuário não-root
RUN useradd -m -s /bin/bash agent && \
    mkdir -p /home/agent/.vnc

# Instala dependências Python
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# Segurança: Remover capabilities
RUN apt-get install -y --no-install-recommends libcap2-bin && \
    setcap -r /usr/bin/python3 || true

# Copia código do agent
COPY --chown=agent:agent . /app
WORKDIR /app

# Configuração Supervisor para display virtual + VNC
COPY supervisord.conf /etc/supervisor/conf.d/

# Expõe porta VNC apenas (não desktop diretamente)
EXPOSE 5900

# Executa como não-root
USER agent

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

---

# docker-compose.yml com restrições de segurança
version: '3.8'

services:
  computer-use-agent:
    build: .
    ports:
      - "5900:5900"  # VNC para observação
      - "8080:8080"  # API para controle

    # Restrições de segurança
    security_opt:
      - no-new-privileges:true
      - seccomp:seccomp-profile.json

    # Limites de recursos
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '0.5'
          memory: 1G

    # Isolamento de rede
    networks:
      - agent-network

    # Sem acesso a filesystem do host
    volumes:
      - agent-tmp:/tmp

    # Filesystem raiz somente leitura
    read_only: true
    tmpfs:
      - /run
      - /var/run

    # Ambiente
    environment:
      - DISPLAY=:99
      - NO_PROXY=localhost

networks:
  agent-network:
    driver: bridge
    internal: true  # Sem internet por padrão

volumes:
  agent-tmp:

---

# Wrapper Python com sandboxing de runtime adicional
import subprocess
import os
```

### Implementação Anthropic Computer Use

Padrão de implementação oficial usando a capacidade computer use do Claude.
Claude 3.5 Sonnet foi o primeiro modelo frontier a oferecer computer use.
Claude Opus 4.5 agora é o "melhor modelo do mundo para computer use".

Capacidades-chave:
- screenshot: Captura estado atual da tela
- mouse: Operações de clique, movimento, drag
- keyboard: Digitar texto, pressionar teclas
- bash: Executar comandos shell
- text_editor: Visualizar e editar arquivos

Versões de ferramenta:
- computer_20251124 (Opus 4.5): Adiciona ação de zoom para inspeção detalhada
- computer_20250124 (Todos outros modelos): Capacidades padrão

Limitação crítica: "Alguns elementos de UI (como dropdowns e scrollbars)
podem ser complicados para Claude manipular" - documentação Anthropic

**Quando usar**: ['Construindo agentes de computer use em produção', 'Precisa de melhor qualidade de entendimento de visão', 'Controle completo de desktop (não apenas browser)']

```python
from anthropic import Anthropic
from anthropic.types.beta import (
    BetaToolComputerUse20241022,
    BetaToolBash20241022,
    BetaToolTextEditor20241022,
)
import subprocess
import base64
from PIL import Image
import io

class AnthropicComputerUse:
    """
    Implementação oficial Anthropic Computer Use.

    Requer:
    - Container Docker com display virtual
    - VNC para visualizar ações do agent
    - Implementações adequadas de ferramentas
    """

    def __init__(self):
        self.client = Anthropic()
        self.model = "claude-sonnet-4-20250514"  # Melhor para computer use
        self.screen_size = (1280, 800)

    def get_tools(self) -> list:
        """Define ferramentas de computer use."""
        return [
            BetaToolComputerUse20241022(
                type="computer_20241022",
                name="computer",
                display_width_px=self.screen_size[0],
                display_height_px=self.screen_size[1],
            ),
            BetaToolBash20241022(
                type="bash_20241022",
                name="bash",
            ),
            BetaToolTextEditor20241022(
                type="text_editor_20241022",
                name="str_replace_editor",
            ),
        ]

    def execute_tool(self, name: str, input: dict) -> dict:
        """Executa uma ferramenta e retorna resultado."""

        if name == "computer":
            return self._handle_computer_action(input)
        elif name == "bash":
            return self._handle_bash(input)
        elif name == "str_replace_editor":
            return self._handle_editor(input)
        else:
            return {"error": f"Ferramenta desconhecida: {name}"}

    def _handle_computer_action(self, input: dict) -> dict:
        """Manipula ações de controle de computador."""
        action = input.get("action")

        if action == "screenshot":
            # Captura via xdotool/scrot
            subprocess.run(["scrot", "/tmp/screenshot.png"])

            with open("/tmp/screenshot.png", "rb") as f:
                pass
```

## ⚠️ Arestas Perigosas

| Problema | Severidade | Solução |
|----------|-----------|---------|
| Problema | crítica | ## Defesa em profundidade - nenhuma solução única funciona |
| Problema | média | ## Adicionar variação similar a humanos nas ações |
| Problema | alta | ## Usar alternativas de teclado quando possível |
| Problema | média | ## Aceitar o tradeoff |
| Problema | alta | ## Implementar gestão de contexto |
| Problema | alta | ## Monitorar e limitar custos |
| Problema | crítica | ## SEMPRE usar sandboxing |