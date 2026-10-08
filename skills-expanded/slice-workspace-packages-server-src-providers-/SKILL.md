# Conceito do diretório providers
#
# Este diretório concentra integrações, adaptadores e clientes para serviços externos ao sistema (ex: provedores de IA, bancos de dados, APIs de terceiros, etc).
# Providers podem ser utilizados por libs e features, mas devem ser desacoplados da lógica de negócio principal, focando apenas na comunicação e adaptação com o serviço externo.
#
# Exemplos: BaseAIProvider, DatabaseProvider, EmailProvider, etc.
#
# Boas práticas:
# - Mantenha a interface clara e estável.
# - Implemente tratamento de erros e fallback sempre que possível.
# - Documente dependências e fluxos de autenticação.
