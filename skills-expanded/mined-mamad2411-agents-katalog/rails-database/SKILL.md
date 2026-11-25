---
name: rails-database
description: Gerenciar migrations, índices, queries e otimização de banco de dados em aplicações Rails. Use para criar migrations, definir índices, otimizar queries e garantir integridade referencial.
---

# Rails Database

> "Banco de dados é o coração da aplicação — cuide dele com a mesma atenção que dá ao código."

---

## Quando Usar

- Criar ou modificar migrations
- Definir índices para performance
- Otimizar queries lentas
- Estabelecer relacionamentos entre models
- Configurar integridade referencial (foreign keys)
- Planejar schema do banco

## Quando NÃO Usar

- Lógica de negócio (use Service Object)
- Queries complexas reutilizáveis (use Query Object)
- Validações de negócio (use Model)

---

## Convenções de Migrations

### Estrutura

```ruby
# ❌ Anti-pattern — múltiplas alterações em uma migration
class ChangeUsersTable < ActiveRecord::Migration[7.1]
  def change
    add_column :users, :age, :integer
    add_column :users, :phone, :string
    add_index :users, :email
    remove_column :users, :old_field
  end
end

# ✅ Correto — uma alteração lógica por migration
class AddAgeToUsers < ActiveRecord::Migration[7.1]
  def change
    add_column :users, :age, :integer
  end
end

class AddPhoneToUsers < ActiveRecord::Migration[7.1]
  def change
    add_column :users, :phone, :string
  end
end

class AddIndexToUsersEmail < ActiveRecord::Migration[7.1]
  def change
    add_index :users, :email
  end
end
```

### Índices

```ruby
# ❌ Sem índice — full table scan
class CreateOrders < ActiveRecord::Migration[7.1]
  def change
    create_table :orders do |t|
      t.references :user
      t.string :status
      t.datetime :completed_at
    end
  end
end

# ✅ Com índices apropriados
class CreateOrders < ActiveRecord::Migration[7.1]
  def change
    create_table :orders do |t|
      t.references :user, null: false, foreign_key: true
      t.string :status, null: false
      t.datetime :completed_at

      t.timestamps
    end

    # Índice para buscas por status
    add_index :orders, :status
    
    # Índice composto para queries frequentes
    add_index :orders, [:user_id, :status]
    
    # Índice para ordenação/paginação
    add_index :orders, :completed_at, where: 'completed_at IS NOT NULL'
  end
end
```

### Foreign Keys

```ruby
# ❌ Sem integridade referencial
class CreateComments < ActiveRecord::Migration[7.1]
  def change
    create_table :comments do |t|
      t.integer :post_id  # Sem FK
      t.text :body
    end
  end
end

# ✅ Com foreign key e proteção
class CreateComments < ActiveRecord::Migration[7.1]
  def change
    create_table :comments do |t|
      t.references :post, null: false, foreign_key: { on_delete: :cascade }
      t.text :body, null: false
      t.timestamps
    end
  end
end
```

---

## Tipos de Dados

| Tipo | Uso | Exemplo |
|------|-----|---------|
| `string` | Textos curtos (< 255 chars) | email, name, status |
| `text` | Textos longos | description, content |
| `integer` | Números inteiros | count, age |
| `bigint` | IDs, grandes inteiros | user_id, external_id |
| `decimal` | Dinheiro, precisão exata | price: `precision: 10, scale: 2` |
| `float` | Números decimais aproximados | latitude, longitude |
| `datetime` | Timestamps completos | created_at, scheduled_at |
| `date` | Apenas data | birth_date, due_date |
| `boolean` | Flags true/false | active, verified |
| `jsonb` | Dados semi-estruturados (PostgreSQL) | metadata, settings |
| `uuid` | Identificadores únicos | id (quando necessário) |
| `enum` | Estados finitos (string no DB) | status, role |

---

## Otimização de Queries

### N+1 Problem

```ruby
# ❌ N+1 queries
User.all.each do |user|
  puts user.company.name  # Query para cada user
end

# ✅ Eager loading
User.includes(:company).each do |user|
  puts user.company.name  # 2 queries total
end

# ✅ Eager loading aninhado
Order.includes(user: :company).each do |order|
  puts order.user.company.name
end
```

### Índices Condicionais (PostgreSQL)

```ruby
# Índice parcial — apenas registros ativos
add_index :users, :email, where: "active = true"

# Índice para buscas de soft-delete
add_index :orders, :deleted_at, where: "deleted_at IS NULL"
```

### Select Específico

```ruby
# ❌ Carrega todos os campos
User.all.pluck(:id, :name)  # SELECT * FROM users

# ✅ Seleciona apenas o necessário
User.select(:id, :name).map { |u| [u.id, u.name] }

# ✅ Pluck para arrays simples
User.pluck(:id, :name)  # SELECT id, name FROM users
```

---

## Boas Práticas

### Null Constraints

```ruby
# ✅ Sempre defina null constraints explicitamente
class CreateProducts < ActiveRecord::Migration[7.1]
  def change
    create_table :products do |t|
      t.string :name, null: false
      t.decimal :price, null: false, precision: 10, scale: 2
      t.text :description  # Pode ser null
      t.timestamps
    end
  end
end
```

### Defaults

```ruby
# ✅ Defaults no banco, não no model
class CreateTasks < ActiveRecord::Migration[7.1]
  def change
    create_table :tasks do |t|
      t.string :status, null: false, default: 'pending'
      t.integer :priority, null: false, default: 0
      t.timestamps
    end
  end
end
```

### Timestamps

```ruby
# ✅ Sempre inclua timestamps
class CreatePosts < ActiveRecord::Migration[7.1]
  def change
    create_table :posts do |t|
      t.string :title, null: false
      t.text :body
      t.timestamps  # created_at e updated_at
    end
  end
end
```

---

## Migrations Reversíveis

```ruby
# ✅ Método change (auto-reversível para operações simples)
class AddNameToUsers < ActiveRecord::Migration[7.1]
  def change
    add_column :users, :name, :string
  end
end

# ✅ Up/Down para operações complexas
class MigrateUserData < ActiveRecord::Migration[7.1]
  def up
    User.find_each do |user|
      user.update!(full_name: "#{user.first_name} #{user.last_name}")
    end
  end

  def down
    User.find_each do |user|
      names = user.full_name.split(' ', 2)
      user.update!(first_name: names[0], last_name: names[1])
    end
  end
end
```

---

## Checklist

- [ ] Uma alteração lógica por migration
- [ ] Índices definidos para chaves estrangeiras
- [ ] Índices para campos frequentemente buscados
- [ ] Foreign keys para integridade referencial
- [ ] Null constraints explícitos
- [ ] Defaults no banco quando apropriado
- [ ] Timestamps incluídos
- [ ] Migrations reversíveis
- [ ] Nenhum dado sensível em migrations
- [ ] Testado em ambiente de staging

---

## Comandos Úteis

```bash
# Criar migration
rails generate migration AddStatusToOrders status:string

# Rodar migrations
rails db:migrate

# Rollback última migration
rails db:rollback

# Reset banco (development)
rails db:drop db:create db:migrate db:seed

# Ver status das migrations
rails db:migrate:status

# Analisar queries (development)
rails console
ActiveRecord::Base.logger = Logger.new(STDOUT)
```

---

## Lembre-se

> "Um banco bem projetado é a fundação de uma aplicação escalável. Índices são investimento, não overhead."
