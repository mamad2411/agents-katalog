---
name: shopify-development
description: |
  Construa apps Shopify, extensões e temas usando GraphQL Admin API, Shopify CLI, Polaris UI e Liquid.
  TRIGGER: "shopify", "app shopify", "extensão checkout", "extensão admin", "extensão POS",
  "tema shopify", "template liquid", "polaris", "shopify graphql", "webhook shopify",
  "cobrança shopify", "assinatura app", "metafields", "shopify functions"
---

# Habilidade de Desenvolvimento Shopify

Use essa habilidade quando o usuário perguntar sobre:

- Construir apps ou extensões Shopify
- Criar customizações de UI checkout/admin/POS
- Desenvolver temas com templating Liquid
- Integrar com GraphQL ou APIs REST Shopify
- Implementar webhooks ou cobrança
- Trabalhar com metafields ou Shopify Functions

---

## ROTEAMENTO: O que Construir

**SE o usuário quer integrar serviços externos OU construir ferramentas merchant OU cobrar por funcionalidades:**
→ Construa um **App** (veja `references/app-development.md`)

**SE o usuário quer customizar checkout OU adicionar UI admin OU criar ações POS OU implementar regras de desconto:**
→ Construa uma **Extensão** (veja `references/extensions.md`)

**SE o usuário quer customizar design da loja OU modificar páginas de produto/coleção:**
→ Construa um **Tema** (veja `references/themes.md`)

**SE o usuário precisa de lógica backend E UI da vitrine:**
→ Construa combinação **App + Theme Extension**

---

## Comandos Shopify CLI

Instalar CLI:

```bash
npm install -g @shopify/cli@latest
```

Criar e executar app:

```bash
shopify app init          # Criar novo app
shopify app dev           # Iniciar servidor dev com tunnel
shopify app deploy        # Build e upload para Shopify
```

Gerar extensão:

```bash
shopify app generate extension --type checkout_ui_extension
shopify app generate extension --type admin_action
shopify app generate extension --type admin_block
shopify app generate extension --type pos_ui_extension
shopify app generate extension --type function
```

Desenvolvimento de tema:

```bash
shopify theme init        # Criar novo tema
shopify theme dev         # Iniciar preview local em localhost:9292
shopify theme pull --live # Puxar tema em produção
shopify theme push --development  # Fazer push para tema de desenvolvimento
```

---

## Escopos de Acesso

Configure em `shopify.app.toml`:

```toml
[access_scopes]
scopes = "read_products,write_products,read_orders,write_orders,read_customers"
```

Escopos comuns:

- `read_products`, `write_products` - Acesso ao catálogo de produtos
- `read_orders`, `write_orders` - Gerenciamento de pedidos
- `read_customers`, `write_customers` - Dados de clientes
- `read_inventory`, `write_inventory` - Níveis de estoque
- `read_fulfillments`, `write_fulfillments` - Fulfillment de pedidos

---

## Padrões GraphQL (Validados contra API 2026-01)

### Consultar Produtos

```graphql
query GetProducts($first: Int!, $query: String) {
  products(first: $first, query: $query) {
    edges {
      node {
        id
        title
        handle
        status
        variants(first: 5) {
          edges {
            node {
              id
              price
              inventoryQuantity
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Consultar Pedidos

```graphql
query GetOrders($first: Int!) {
  orders(first: $first) {
    edges {
      node {
        id
        name
        createdAt
        displayFinancialStatus
        totalPriceSet {
          shopMoney {
            amount
            currencyCode
          }
        }
      }
    }
  }
}
```

### Definir Metafields

```graphql
mutation SetMetafields($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id
      namespace
      key
      value
    }
    userErrors {
      field
      message
    }
  }
}
```

Exemplo de variáveis:

```json
{
  "metafields": [
    {
      "ownerId": "gid://shopify/Product/123",
      "namespace": "custom",
      "key": "care_instructions",
      "value": "Manipule com cuidado",
      "type": "single_line_text_field"
    }
  ]
}
```

---

## Exemplo de Extensão de Checkout

```tsx
import {
  reactExtension,
  BlockStack,
  TextField,
  Checkbox,
  useApplyAttributeChange,
} from "@shopify/ui-extensions-react/checkout";

export default reactExtension("purchase.checkout.block.render", () => (
  <GiftMessage />
));

function GiftMessage() {
  const [isGift, setIsGift] = useState(false);
  const [message, setMessage] = useState("");
  const applyAttributeChange = useApplyAttributeChange();

  useEffect(() => {
    if (isGift && message) {
      applyAttributeChange({
        type: "updateAttribute",
        key: "gift_message",
        value: message,
      });
    }
  }, [isGift, message]);

  return (
    <BlockStack spacing="loose">
      <Checkbox checked={isGift} onChange={setIsGift}>
        Este é um presente
      </Checkbox>
      {isGift && (
        <TextField
          label="Mensagem de Presente"
          value={message}
          onChange={setMessage}
          multiline={3}
        />
      )}
    </BlockStack>
  );
}
```

---

## Exemplo de Template Liquid

```liquid
{% comment %} Snippet de Cartão de Produto {% endcomment %}
<div class="product-card">
  <a href="{{ product.url }}">
    {% if product.featured_image %}
      <img
        src="{{ product.featured_image | img_url: 'medium' }}"
        alt="{{ product.title | escape }}"
        loading="lazy"
      >
    {% endif %}
    <h3>{{ product.title }}</h3>
    <p class="price">{{ product.price | money }}</p>
    {% if product.compare_at_price > product.price %}
      <p class="sale-badge">Promoção</p>
    {% endif %}
  </a>
</div>
```

---

## Configuração de Webhook

Em `shopify.app.toml`:

```toml
[webhooks]
api_version = "2026-01"

[[webhooks.subscriptions]]
topics = ["orders/create", "orders/updated"]
uri = "/webhooks/orders"

[[webhooks.subscriptions]]
topics = ["products/update"]
uri = "/webhooks/products"

# Webhooks obrigatórios GDPR (requeridos para aprovação de app)
[webhooks.privacy_compliance]
customer_data_request_url = "/webhooks/gdpr/data-request"
customer_deletion_url = "/webhooks/gdpr/customer-deletion"
shop_deletion_url = "/webhooks/gdpr/shop-deletion"
```

---

## Boas Práticas

### Uso da API

- Use GraphQL em vez de REST para novo desenvolvimento
- Solicite apenas campos que você precisa (reduz custo de query)
- Implemente paginação baseada em cursor com `pageInfo.endCursor`
- Use operações em bulk para processar mais de 250 itens
- Trate limites de taxa com backoff exponencial

### Segurança

- Armazene credenciais da API em variáveis de ambiente
- Sempre valide assinaturas HMAC de webhook antes de processar
- Valide parâmetro de estado OAuth para prevenir CSRF
- Solicite escopos de acesso mínimos
- Use session tokens para apps incorporados

### Performance

- Cache respostas da API quando os dados não mudam frequentemente
- Use lazy loading em extensões
- Otimize imagens em temas usando filtro `img_url`
- Monitore custos de query GraphQL através de headers de resposta

---

## Solução de Problemas

**SE você vir erros de limite de taxa:**
→ Implemente lógica de retry com backoff exponencial
→ Mude para operações em bulk para grandes volumes de dados
→ Monitore o header `X-Shopify-Shop-Api-Call-Limit`

**SE a autenticação falhar:**
→ Verifique se o token de acesso ainda é válido
→ Confirme que todos os escopos requeridos foram concedidos
→ Garanta que o fluxo OAuth foi completado com sucesso

**SE a extensão não está aparecendo:**
→ Verifique se o alvo da extensão está correto
→ Confirme que a extensão foi publicada via `shopify app deploy`
→ Valide que o app está instalado na loja de teste

**SE o webhook não está recebendo eventos:**
→ Verifique se a URL do webhook é acessível publicamente
→ Confira lógica de validação de assinatura HMAC
→ Revise logs de webhook no Partner Dashboard

**SE query GraphQL falhar:**
→ Valide a query contra o schema (use explorador GraphiQL)
→ Verifique se há campos descontinuados na mensagem de erro
→ Confirme que você possui os escopos de acesso requeridos

---

## Arquivos de Referência

Para guias detalhados de implementação, leia esses arquivos:

- `references/app-development.md` - Fluxo de autenticação OAuth, mutações GraphQL para produtos/pedidos/cobrança, handlers de webhook, integração com API de billing
- `references/extensions.md` - Componentes de UI de checkout, extensões admin UI, extensões POS, Shopify Functions para descontos/pagamento/entrega
- `references/themes.md` - Referência de sintaxe Liquid, estrutura de diretório de tema, seções e snippets, padrões comuns

---

## Scripts

- `scripts/shopify_init.py` - Scaffolding interativo de projeto. Execute: `python scripts/shopify_init.py`
- `scripts/shopify_graphql.py` - Utilitários GraphQL com templates de query, paginação, rate limiting. Importe: `from shopify_graphql import ShopifyGraphQL`

---

## Links da Documentação Oficial

- Shopify Developer Docs: https://shopify.dev/docs
- Referência GraphQL Admin API: https://shopify.dev/docs/api/admin-graphql
- Referência Shopify CLI: https://shopify.dev/docs/api/shopify-cli
- Polaris Design System: https://polaris.shopify.com

Versão da API: 2026-01 (lançamentos trimestrais, janela de descontinuação de 12 meses)