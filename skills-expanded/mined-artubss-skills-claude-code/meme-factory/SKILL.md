---
name: meme-factory
description: Gerar memes usando a API memegen.link. Use quando usuários solicitarem memes, quiserem adicionar humor ao conteúdo ou precisarem de recursos visuais para redes sociais. Suporta 100+ templates populares com texto e estilo personalizados.
---

# Meme Factory

Crie memes usando a API gratuita memegen.link e formatos de memes textuais.

---

## Triggers

| Trigger | Descrição |
|---------|-----------|
| `/meme-factory` | Invocação manual |
| `/meme-factory {template} {top} {bottom}` | Geração direta de meme |
| `meme-factory: create a meme about X` | Solicitação em linguagem natural |

---

## Referência Rápida

| Ação | Formato |
|------|---------|
| Meme básico | `https://api.memegen.link/images/{template}/{top}/{bottom}.png` |
| Com dimensões | `?width=1200&height=630` |
| Fundo personalizado | `?style=https://example.com/image.jpg` |
| Todos os templates | https://api.memegen.link/templates/ |
| Documentação interativa | https://api.memegen.link/docs/ |

**Recursos Adicionais:**
- [Markdown Memes Guide](references/markdown-memes-guide.md) - 15+ formatos de memes textuais
- [Examples](references/examples.md) - Exemplos de uso prático
- [meme_generator.py](scripts/meme_generator.py) - Script auxiliar em Python

---

## Início Rápido

### Estrutura Básica de Meme

```
https://api.memegen.link/images/{template}/{top_text}/{bottom_text}.{extension}
```

**Exemplo:**
```
https://api.memegen.link/images/buzz/memes/memes_everywhere.png
```

Resultado: Meme do Buzz Lightyear com "memes" no topo e "memes everywhere" na base.

### Formatação de Texto

| Caractere | Codificação |
|-----------|-------------|
| Espaço | `_` ou `-` |
| Quebra de linha | `~n` |
| Ponto de interrogação | `~q` |
| Símbolo de percentual | `~p` |
| Barra | `~s` |
| Hash | `~h` |
| Apóstrofo | `''` |
| Aspas | `""` |

---

## Templates Populares

| Template | Caso de Uso | Exemplo |
|----------|------------|---------|
| `buzz` | X, X em todo lugar | bugs/bugs_everywhere |
| `drake` | Comparações | manual_testing/automated_testing |
| `success` | Vitórias | deployed/no_errors |
| `fine` | Coisas dando errado | server_on_fire/this_is_fine |
| `fry` | Incerteza | not_sure_if_bug/or_feature |
| `changemind` | Opiniões polêmicas | tabs_are_better_than_spaces |
| `distracted` | Prioridades | my_code/new_framework/current_project |
| `mordor` | Não é simplesmente | one_does_not_simply/deploy_on_friday |

---

## Guia de Seleção de Template

| Contexto | Template | Por Quê |
|----------|----------|--------|
| Comparando opções | `drake` | Formato dois painéis rejeitar/aprovar |
| Celebrando vitórias | `success` | Ênfase em resultado positivo |
| Problemas ignorados | `fine` | "Tudo está bem" irônico |
| Incerteza | `fry` | Formato "Não tenho certeza se X ou Y" |
| Opinião controversa | `changemind` | Afirmação + desafio |
| Coisas onipresentes | `buzz` | "X, X em todo lugar" |
| Ideias ruins | `mordor` | "Não é simplesmente..." |

---

## Validação

Após gerar um meme:

- [ ] URL retorna imagem válida (teste no navegador)
- [ ] Texto é legível (não muito longo)
- [ ] Template combina com o contexto da mensagem
- [ ] Caracteres especiais propriamente codificados
- [ ] Dimensões apropriadas para a plataforma

### Dimensões por Plataforma

| Plataforma | Dimensões |
|-----------|-----------|
| Redes sociais (Open Graph) | 1200x630 |
| Slack/Discord | 800x600 |
| GitHub | Padrão |

---

## Anti-Padrões

| Evite | Por Quê | Use Em Seu Lugar |
|------|--------|-----------------|
| Espaços sem codificação | URL quebra | Use `_` ou `-` |
| Muito texto | Ilegível | 2-6 palavras por linha |
| Template errado | Mensagem desconectada | Combine template com contexto |
| Extensão ausente | URL inválida | Sempre inclua `.png`, `.jpg`, etc. |
| Caracteres especiais não codificados | URL quebra | Use `~q`, `~s`, `~p`, etc. |
| Assumir que template existe | Erro 404 | Verifique lista de templates primeiro |

---

## Verificação

A geração de meme é bem-sucedida quando:

1. **URL é válida** - Retorna HTTP 200
2. **Imagem renderiza** - Exibe corretamente em markdown
3. **Texto é visível** - Adequadamente formatado na imagem
4. **Contexto combina** - Template encaixa na mensagem

**Comando de teste:**
```bash
curl -I "https://api.memegen.link/images/buzz/test/test.png"
# Deve retornar: HTTP/2 200
```

---

<details>
<summary><strong>Aprofundamento: Recursos Avançados</strong></summary>

### Formatos de Imagem

| Extensão | Caso de Uso |
|----------|------------|
| `.png` | Melhor qualidade, padrão |
| `.jpg` | Tamanho de arquivo menor |
| `.webp` | Moderno, boa compressão |
| `.gif` | Templates animados |

### Dimensões

```
?width=800
?height=600
?width=800&height=600  (preenchido até exato)
```

### Opções de Layout

```
?layout=top     # Texto apenas no topo
?layout=bottom  # Texto apenas na base
?layout=default # Padrão topo/base
```

### Fontes Personalizadas

Visualize disponíveis: https://api.memegen.link/fonts/

```
?font=impact  (padrão)
```

### Imagens Personalizadas

Use qualquer imagem como fundo:

```
https://api.memegen.link/images/custom/hello/world.png?style=https://example.com/image.jpg
```

</details>

<details>
<summary><strong>Aprofundamento: Memes Contextuais</strong></summary>

### Revisão de Código

```
Template: fry
https://api.memegen.link/images/fry/not_sure_if_feature/or_bug.png
```

### Deployments

```
Template: interesting
https://api.memegen.link/images/interesting/i_dont_always_test/but_when_i_do_i_do_it_in_production.png
```

### Documentação

```
Template: yodawg
https://api.memegen.link/images/yodawg/yo_dawg_i_heard_you_like_docs/so_i_documented_the_documentation.png
```

### Problemas de Performance

```
Template: fine
https://api.memegen.link/images/fine/memory_usage_at_99~/this_is_fine.png
```

### Deploy Bem-Sucedido

```
Template: success
https://api.memegen.link/images/success/deployed_to_production/zero_downtime.png
```

</details>

<details>
<summary><strong>Aprofundamento: Integração de Workflow</strong></summary>

### Gerando Memes em Resposta

```markdown
Aqui está um meme relevante:

![Meme](https://api.memegen.link/images/buzz/bugs/bugs_everywhere.png)
```

### Geração Dinâmica (Python)

```python
def generate_status_meme(status: str, message: str):
    template_map = {
        "success": "success",
        "failure": "fine",
        "review": "fry",
        "deploy": "interesting"
    }

    template = template_map.get(status, "buzz")
    words = message.split()
    top = "_".join(words[0:3])
    bottom = "_".join(words[3:6])

    return f"https://api.memegen.link/images/{template}/{top}/{bottom}.png"
```

### Usando o Script Auxiliar

```python
from meme_generator import MemeGenerator

meme = MemeGenerator()
url = meme.generate("buzz", "features", "features everywhere")
print(url)
```

</details>

<details>
<summary><strong>Aprofundamento: Referência da API</strong></summary>

### Endpoints

| Endpoint | Propósito |
|----------|-----------|
| `/templates/` | Listar todos os templates |
| `/templates/{id}` | Detalhes do template |
| `/fonts/` | Fontes disponíveis |
| `/images/{template}/{top}/{bottom}.{ext}` | Gerar meme |

### Características da API

- Gratuita e open-source
- Sem necessidade de chave de API
- Sem limite de taxa (uso normal)
- Sem estado (todas as informações na URL)
- Imagens geradas sob demanda

### Tratamento de Erros

1. Verifique template em https://api.memegen.link/templates/
2. Verifique formatação de texto (underscores para espaços)
3. Verifique codificação de caracteres especiais
4. Verifique extensão válida
5. Teste URL no navegador

</details>

---

## Referências

| Documento | Conteúdo |
|-----------|----------|
| [markdown-memes-guide.md](references/markdown-memes-guide.md) | 15+ formatos de memes textuais (greentext, copypasta, ASCII, etc.) |
| [examples.md](references/examples.md) | Exemplos de uso prático |

### Scripts

| Script | Propósito |
|--------|-----------|
| [meme_generator.py](scripts/meme_generator.py) | Helper Python para geração de memes |

---

## Resumo

Gere memes contextuais para:
- Adicionar humor às conversas
- Criar recursos visuais para redes sociais
- Tornar revisões de código mais envolventes
- Celebrar sucessos

**Regra de ouro:** Mantenha texto conciso, combine template com contexto.