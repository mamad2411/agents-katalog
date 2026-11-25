---
name: twilio-communications
description: "Construa recursos de comunicação com Twilio: mensagens SMS, chamadas de voz, WhatsApp Business API e verificação de usuários (2FA). Abrange todo o espectro, desde notificações simples até sistemas IVR complexos e autenticação multicanal. Foco crítico em conformidade, limites de taxa e tratamento de erros. Use quando: twilio, enviar SMS, mensagem de texto, chamada de voz, verificação de telefone."
source: vibeship-spawner-skills (Apache 2.0)
---

# Comunicações Twilio

## Padrões

### Padrão de Envio de SMS

Padrão básico para enviar mensagens SMS com Twilio.
Trata dos fundamentos: formatação de números de telefone, entrega de mensagens
e callbacks de status de entrega.

Considerações principais:
- Números de telefone devem estar no formato E.164 (+1234567890)
- Limite de taxa padrão: 80 mensagens por segundo (MPS)
- Mensagens com mais de 160 caracteres são divididas (e custam mais)
- Filtragem de operadora pode bloquear mensagens (especialmente para números dos EUA)


**Quando usar**: ['Enviar notificações para usuários', 'Mensagens transacionais (confirmações de pedidos, envios)', 'Alertas e lembretes']

```python
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
import re

class TwilioSMS:
    """
    SMS sending with proper error handling and validation.
    """

    def __init__(self):
        self.client = Client(
            os.environ["TWILIO_ACCOUNT_SID"],
            os.environ["TWILIO_AUTH_TOKEN"]
        )
        self.from_number = os.environ["TWILIO_PHONE_NUMBER"]

    def validate_e164(self, phone: str) -> bool:
        """Validate phone number is in E.164 format."""
        pattern = r'^\+[1-9]\d{1,14}$'
        return bool(re.match(pattern, phone))

    def send_sms(
        self,
        to: str,
        body: str,
        status_callback: str = None
    ) -> dict:
        """
        Send an SMS message.

        Args:
            to: Recipient phone number in E.164 format
            body: Message text (160 chars = 1 segment)
            status_callback: URL for delivery status webhooks

        Returns:
            Message SID and status
        """
        # Validate phone number format
        if not self.validate_e164(to):
            return {
                "success": False,
                "error": "Phone number must be in E.164 format (+1234567890)"
            }

        # Check message length (warn about segmentation)
        segment_count = (len(body) + 159) // 160
        if segment_count > 1:
            print(f"Warning: Message will be sent as {segment_count} segments")

        try:
            message = self.client.messages.create(
                to=to,
                from_=self.from_number,
                body=body,
                status_callback=status_callback
            )

            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status,
                "segments": segment_count
            }

        except TwilioRestException as e:
            return self._handle_error(e)

    def _handle_error(self, error: Twilio
```

### Padrão Twilio Verify (2FA/OTP)

Use Twilio Verify para verificação de número de telefone e 2FA.
Trata geração de código, entrega, limitação de taxa e prevenção de fraude.

Benefícios principais comparado a OTP caseiro:
- Twilio gerencia geração e expiração de código
- Prevenção de fraude integrada (economizou clientes US$ 82M+ bloqueando 747M tentativas)
- Gerencia limitação de taxa automaticamente
- Multicanal: SMS, Voz, Email, Push, WhatsApp

Google descobriu que 2FA por SMS bloqueia "100% de bots automatizados, 96% de ataques de phishing em massa e 76% de ataques direcionados."


**Quando usar**: ['Verificação de número de telefone do usuário no cadastro', 'Autenticação de dois fatores (2FA)', 'Verificação de redefinição de senha', 'Confirmação de transações de alto valor']

```python
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from enum import Enum
from typing import Optional

class VerifyChannel(Enum):
    SMS = "sms"
    CALL = "call"
    EMAIL = "email"
    WHATSAPP = "whatsapp"

class TwilioVerify:
    """
    Phone verification with Twilio Verify.
    Never store OTP codes - Twilio handles it.
    """

    def __init__(self, verify_service_sid: str = None):
        self.client = Client(
            os.environ["TWILIO_ACCOUNT_SID"],
            os.environ["TWILIO_AUTH_TOKEN"]
        )
        # Create a Verify Service in Twilio Console first
        self.service_sid = verify_service_sid or os.environ["TWILIO_VERIFY_SID"]

    def send_verification(
        self,
        to: str,
        channel: VerifyChannel = VerifyChannel.SMS,
        locale: str = "en"
    ) -> dict:
        """
        Send verification code to phone/email.

        Args:
            to: Phone number (E.164) or email
            channel: SMS, call, email, or whatsapp
            locale: Language code for message

        Returns:
            Verification status
        """
        try:
            verification = self.client.verify \
                .v2 \
                .services(self.service_sid) \
                .verifications \
                .create(
                    to=to,
                    channel=channel.value,
                    locale=locale
                )

            return {
                "success": True,
                "status": verification.status,  # "pending"
                "channel": channel.value,
                "valid": verification.valid
            }

        except TwilioRestException as e:
            return self._handle_verify_error(e)

    def check_verification(self, to: str, code: str) -> dict:
        """
        Check if verification code is correct.

        Args:
            to: Phone number or email that received code
            code: The code entered by user

        R
```

### Padrão IVR TwiML

Construa sistemas de Resposta de Voz Interativa (IVR) usando TwiML.
TwiML (Linguagem de Marcação Twilio) é XML que diz ao Twilio o que fazer
quando recebe chamadas.

Verbos TwiML principais:
- <Say>: Síntese de texto em fala
- <Play>: Reproduzir arquivo de áudio
- <Gather>: Coletar entrada de teclado/fala
- <Dial>: Conectar a outro número
- <Record>: Gravar voz do chamador
- <Redirect>: Mover para outro endpoint TwiML

Insight-chave: Twilio faz requisição HTTP para seu webhook, você retorna
TwiML, Twilio executa. Sem estado, então use parâmetros de URL ou sessões.


**Quando usar**: ['Sistemas de menu de telefone (pressione 1 para vendas...)', 'Atendimento ao cliente automatizado', 'Lembretes de compromisso com confirmação', 'Sistemas de caixa postal']

```python
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.request_validator import RequestValidator
import os

app = Flask(__name__)

def validate_twilio_request(f):
    """Decorator to validate requests are from Twilio."""
    def wrapper(*args, **kwargs):
        validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])

        # Get request details
        url = request.url
        params = request.form.to_dict()
        signature = request.headers.get("X-Twilio-Signature", "")

        if not validator.validate(url, params, signature):
            return "Invalid request", 403

        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/voice/incoming", methods=["POST"])
@validate_twilio_request
def incoming_call():
    """Handle incoming call with IVR menu."""
    response = VoiceResponse()

    # Gather digits with timeout
    gather = Gather(
        num_digits=1,
        action="/voice/menu-selection",
        method="POST",
        timeout=5
    )
    gather.say(
        "Welcome to Acme Corp. "
        "Press 1 for sales. "
        "Press 2 for support. "
        "Press 3 to leave a message."
    )
    response.append(gather)

    # If no input, repeat
    response.redirect("/voice/incoming")

    return Response(str(response), mimetype="text/xml")

@app.route("/voice/menu-selection", methods=["POST"])
@validate_twilio_request
def menu_selection():
    """Route based on menu selection."""
    response = VoiceResponse()
    digit = request.form.get("Digits", "")

    if digit == "1":
        # Transfer to sales
        response.say("Connecting you to sales.")
        response.dial(os.environ["SALES_PHONE"])

    elif digit == "2":
        # Transfer to support
        response.say("Connecting you to support.")
        response.dial(os.environ["SUPPORT_PHONE"])

    elif digit == "3":
        # Voicemail
        response.say("Please leave a message after 
```

## ⚠️ Pontos Críticos

| Problema | Severidade | Solução |
|----------|-----------|---------|
| Problema | alta | ## Acompanhe status de opt-out em seu banco de dados |
| Problema | média | ## Implemente lógica de retry para falhas transitórias |
| Problema | alta | ## Registre para A2P 10DLC (requisito nos EUA) |
| Problema | crítica | ## SEMPRE valide a assinatura |
| Problema | alta | ## Acompanhe janelas de sessão por usuário |
| Problema | crítica | ## Nunca codifique credenciais |
| Problema | média | ## Implemente limitação de taxa no nível da aplicação também |