# LOGOS API WebPosto — convenções para o agente

- Prefira **httpx** para chamadas HTTP assíncronas (AsyncClient), reutilizando cliente/pool quando fizer sentido.
- Mantenha a nomenclatura **"pista"** (`caixa_tipo`, domínio de postos) alinhada aos modelos e à API WebPosto.
- Use **logs detalhados** (nível apropriado + contexto: URL, status, corpo resumido, IDs de unidade/caixa) em falhas de integração com o WebPosto; evite apenas `print` em fluxos de produção.
