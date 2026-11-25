---
name: Rails Model
description: Criar Models ActiveRecord seguindo convenções do projeto
---

# Rails Model

Models representam as **entidades de domínio** e suas regras de dados.

## Estrutura

```
app/models/
├── application_record.rb
├── concerns/
│   ├── syncable.rb
│   └── categorizable.rb
└── [entidade].rb
```

## Template de Model

```ruby
# app/models/[entidade].rb
class Account < ApplicationRecord
  # == Concerns ==
  include Syncable
  include Categorizable

  # == Associations ==
  belongs_to :user
  belongs_to :institution
  has_many :transactions, class_name: 'AccountTransaction', dependent: :destroy

  # == Enums (com valores explícitos) ==
  enum account_type: {
    CONTA_DEPOSITO_A_VISTA: 'CONTA_DEPOSITO_A_VISTA',
    CONTA_POUPANCA: 'CONTA_POUPANCA',
    CONTA_PAGAMENTO_PRE_PAGA: 'CONTA_PAGAMENTO_PRE_PAGA'
  }
  enum account_status: { available: 'AVAILABLE', unavailable: 'UNAVAILABLE', closed: 'CLOSED' }

  # == Validations ==
  validates :external_account_id, presence: true, uniqueness: { scope: [:user_id, :institution_id] }
  validates :account_number, :branch_code, presence: true

  # == Scopes (preferir sobre métodos) ==
  scope :active, -> { where(is_active: true) }
  scope :pending_sync, -> { where(sync_status: 'PENDING') }
  scope :by_institution, ->(inst) { where(institution: inst) }

  # == Instance Methods (apenas lógica simples) ==
  def recent_transactions(days: 30)
    transactions.where('transaction_date >= ?', days.days.ago).order(transaction_date: :desc)
  end

  def update_balance!(balance_data)
    update!(
      current_balance: balance_data[:current_balance],
      available_balance: balance_data[:available_balance],
      last_balance_update: Time.current
    )
  end
end
```

## Concerns Reutilizáveis

```ruby
# app/models/concerns/syncable.rb
module Syncable
  extend ActiveSupport::Concern

  included do
    enum sync_status: { pending: 'PENDING', synced: 'SYNCED', error: 'ERROR' }

    scope :needs_sync, -> { where(sync_status: %w[PENDING ERROR]) }
    scope :recently_synced, -> { where('last_sync_at > ?', 1.hour.ago) }
  end

  def mark_synced!
    update!(sync_status: :synced, last_sync_at: Time.current)
  end

  def mark_sync_error!(message = nil)
    update!(sync_status: :error, sync_error_message: message)
  end
end

# app/models/concerns/categorizable.rb
module Categorizable
  extend ActiveSupport::Concern

  included do
    belongs_to :category, optional: true

    scope :uncategorized, -> { where(category_id: nil) }
    scope :by_category, ->(cat) { where(category: cat) }
  end

  def auto_categorize!
    Categorization::TransactionCategorizer.new(self).call
  end
end
```

## Enums com Valores Explícitos

```ruby
# ✅ CORRETO: valores explícitos (string no banco)
enum loan_status: { ACTIVE: 'ACTIVE', CLOSED: 'CLOSED', PAID: 'PAID', DEFAULT: 'DEFAULT' }

# ❌ EVITAR: valores implícitos (inteiro no banco)
enum loan_status: [:active, :closed, :paid, :default]
```

## Associações Complexas

```ruby
class User < ApplicationRecord
  # Associações diretas
  has_many :accounts, dependent: :destroy
  has_many :credit_cards, dependent: :destroy
  has_many :loans, dependent: :destroy

  # Through associations
  has_many :account_transactions, through: :accounts, source: :transactions
  has_many :credit_card_bills, through: :credit_cards, source: :bills
end
```

## Validações Customizadas

```ruby
class User < ApplicationRecord
  validates :email, presence: true, uniqueness: true
  validates :cpf_cnpj, presence: true, uniqueness: true

  validate :valid_document

  private

  def valid_document
    return if document_type == 'cpf' && CpfCnpj.valid?(cpf_cnpj, type: :cpf)
    return if document_type == 'cnpj' && CpfCnpj.valid?(cpf_cnpj, type: :cnpj)

    errors.add(:cpf_cnpj, 'inválido')
  end
end
```

## Security in Models

```ruby
# ❌ NUNCA confie em dados externos
def update_from_external(data)
  update!(data)  # Mass assignment vulnerability!
end

# ✅ Whitelist explícita
def update_from_external(data)
  update!(
    account_name: data['name'],
    current_balance: data['balance']
  )
end

# ❌ NUNCA exponha dados sensíveis
def as_json
  super  # Inclui tudo!
end

# ✅ Defina explicitamente
def as_json
  super(only: [:id, :account_name, :account_type])
end
```

---

## Sensitive Data

```ruby
class User < ApplicationRecord
  # Criptografar atributos sensíveis
  encrypts :cpf
  encrypts :access_token

  # Nunca serializar em logs/JSON
  def serializable_hash(options = nil)
    super(options).except('cpf', 'access_token', 'password_digest')
  end
end

# config/initializers/filter_parameter_logging.rb
Rails.application.config.filter_parameters += [
  :password, :cpf, :token, :secret, :credit_card
]
```

---

## Regras

1. **Scopes > Métodos de classe:** para queries reutilizáveis
2. **Enums com string:** usar valores explícitos, não inteiros
3. **Concerns para DRY:** extrair comportamento compartilhado
4. **Validações no model:** dados, não regras de negócio
5. **Dependent destroy:** sempre definir para has_many
6. **Naming:** singular, PascalCase (ex: `AccountTransaction`)
7. **Criptografia:** usar `encrypts` para dados sensíveis
8. **Whitelist:** nunca usar mass assignment com dados externos
9. **Minimal changes:** altere o mínimo possível; pesquise padrões antes de implementar

