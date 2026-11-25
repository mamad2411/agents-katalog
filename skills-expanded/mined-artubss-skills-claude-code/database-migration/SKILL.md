---
name: database-migration
description: "Domine migrações de schema e dados em ORMs (Sequelize, TypeORM, Prisma), incluindo estratégias de rollback e deployments sem downtime."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Migração de Banco de Dados

Domine migrações de schema e dados em ORMs (Sequelize, TypeORM, Prisma), incluindo estratégias de rollback e deployments sem downtime.

## Não use esta skill quando

- A tarefa não está relacionada a migração de banco de dados
- Você precisa de um domínio ou ferramenta diferente fora deste escopo

## Instruções

- Esclareça objetivos, restrições e entradas necessárias.
- Aplique as melhores práticas relevantes e valide resultados.
- Forneça passos práticos e verificação.
- Se exemplos detalhados forem necessários, abra `resources/implementation-playbook.md`.

## Use esta skill quando

- Migrar entre diferentes ORMs
- Realizar transformações de schema
- Mover dados entre bancos de dados
- Implementar procedimentos de rollback
- Deployments sem downtime
- Atualizações de versão de banco de dados
- Refatoração de modelo de dados

## Migrações em ORMs

### Migrações Sequelize
```javascript
// migrations/20231201-create-users.js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('users', {
      id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true
      },
      email: {
        type: Sequelize.STRING,
        unique: true,
        allowNull: false
      },
      createdAt: Sequelize.DATE,
      updatedAt: Sequelize.DATE
    });
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable('users');
  }
};

// Executar: npx sequelize-cli db:migrate
// Reverter: npx sequelize-cli db:migrate:undo
```

### Migrações TypeORM
```typescript
// migrations/1701234567-CreateUsers.ts
import { MigrationInterface, QueryRunner, Table } from 'typeorm';

export class CreateUsers1701234567 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(
      new Table({
        name: 'users',
        columns: [
          {
            name: 'id',
            type: 'int',
            isPrimary: true,
            isGenerated: true,
            generationStrategy: 'increment'
          },
          {
            name: 'email',
            type: 'varchar',
            isUnique: true
          },
          {
            name: 'created_at',
            type: 'timestamp',
            default: 'CURRENT_TIMESTAMP'
          }
        ]
      })
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable('users');
  }
}

// Executar: npm run typeorm migration:run
// Reverter: npm run typeorm migration:revert
```

### Migrações Prisma
```prisma
// schema.prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  createdAt DateTime @default(now())
}

// Gerar migração: npx prisma migrate dev --name create_users
// Aplicar: npx prisma migrate deploy
```

## Transformações de Schema

### Adicionando Colunas com Padrões
```javascript
// Migração segura: adicionar coluna com padrão
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('users', 'status', {
      type: Sequelize.STRING,
      defaultValue: 'active',
      allowNull: false
    });
  },

  down: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'status');
  }
};
```

### Renomeando Colunas (Zero Downtime)
```javascript
// Passo 1: Adicionar nova coluna
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('users', 'full_name', {
      type: Sequelize.STRING
    });

    // Copiar dados da coluna antiga
    await queryInterface.sequelize.query(
      'UPDATE users SET full_name = name'
    );
  },

  down: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'full_name');
  }
};

// Passo 2: Atualizar aplicação para usar nova coluna

// Passo 3: Remover coluna antiga
module.exports = {
  up: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'name');
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('users', 'name', {
      type: Sequelize.STRING
    });
  }
};
```

### Alterando Tipos de Coluna
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Para tabelas grandes, use abordagem multi-etapa

    // 1. Adicionar nova coluna
    await queryInterface.addColumn('users', 'age_new', {
      type: Sequelize.INTEGER
    });

    // 2. Copiar e transformar dados
    await queryInterface.sequelize.query(`
      UPDATE users
      SET age_new = CAST(age AS INTEGER)
      WHERE age IS NOT NULL
    `);

    // 3. Remover coluna antiga
    await queryInterface.removeColumn('users', 'age');

    // 4. Renomear nova coluna
    await queryInterface.renameColumn('users', 'age_new', 'age');
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.changeColumn('users', 'age', {
      type: Sequelize.STRING
    });
  }
};
```

## Transformações de Dados

### Migração Complexa de Dados
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Obter todos os registros
    const [users] = await queryInterface.sequelize.query(
      'SELECT id, address_string FROM users'
    );

    // Transformar cada registro
    for (const user of users) {
      const addressParts = user.address_string.split(',');

      await queryInterface.sequelize.query(
        `UPDATE users
         SET street = :street,
             city = :city,
             state = :state
         WHERE id = :id`,
        {
          replacements: {
            id: user.id,
            street: addressParts[0]?.trim(),
            city: addressParts[1]?.trim(),
            state: addressParts[2]?.trim()
          }
        }
      );
    }

    // Remover coluna antiga
    await queryInterface.removeColumn('users', 'address_string');
  },

  down: async (queryInterface, Sequelize) => {
    // Reconstruir coluna original
    await queryInterface.addColumn('users', 'address_string', {
      type: Sequelize.STRING
    });

    await queryInterface.sequelize.query(`
      UPDATE users
      SET address_string = CONCAT(street, ', ', city, ', ', state)
    `);

    await queryInterface.removeColumn('users', 'street');
    await queryInterface.removeColumn('users', 'city');
    await queryInterface.removeColumn('users', 'state');
  }
};
```

## Estratégias de Rollback

### Migrações Baseadas em Transação
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    const transaction = await queryInterface.sequelize.transaction();

    try {
      await queryInterface.addColumn(
        'users',
        'verified',
        { type: Sequelize.BOOLEAN, defaultValue: false },
        { transaction }
      );

      await queryInterface.sequelize.query(
        'UPDATE users SET verified = true WHERE email_verified_at IS NOT NULL',
        { transaction }
      );

      await transaction.commit();
    } catch (error) {
      await transaction.rollback();
      throw error;
    }
  },

  down: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'verified');
  }
};
```

### Rollback Baseado em Checkpoint
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Criar tabela de backup
    await queryInterface.sequelize.query(
      'CREATE TABLE users_backup AS SELECT * FROM users'
    );

    try {
      // Executar migração
      await queryInterface.addColumn('users', 'new_field', {
        type: Sequelize.STRING
      });

      // Verificar migração
      const [result] = await queryInterface.sequelize.query(
        "SELECT COUNT(*) as count FROM users WHERE new_field IS NULL"
      );

      if (result[0].count > 0) {
        throw new Error('Verificação de migração falhou');
      }

      // Descartar backup
      await queryInterface.dropTable('users_backup');
    } catch (error) {
      // Restaurar do backup
      await queryInterface.sequelize.query('DROP TABLE users');
      await queryInterface.sequelize.query(
        'CREATE TABLE users AS SELECT * FROM users_backup'
      );
      await queryInterface.dropTable('users_backup');
      throw error;
    }
  }
};
```

## Migrações sem Downtime

### Estratégia Blue-Green Deployment
```javascript
// Fase 1: Fazer mudanças compatíveis com versões anteriores
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Adicionar nova coluna (ambos os códigos antigos e novos podem funcionar)
    await queryInterface.addColumn('users', 'email_new', {
      type: Sequelize.STRING
    });
  }
};

// Fase 2: Deploy de código que escreve em ambas as colunas

// Fase 3: Preencher dados
module.exports = {
  up: async (queryInterface) => {
    await queryInterface.sequelize.query(`
      UPDATE users
      SET email_new = email
      WHERE email_new IS NULL
    `);
  }
};

// Fase 4: Deploy de código que lê da nova coluna

// Fase 5: Remover coluna antiga
module.exports = {
  up: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'email');
  }
};
```

## Migrações Entre Bancos de Dados

### PostgreSQL para MySQL
```javascript
// Lidar com diferenças
module.exports = {
  up: async (queryInterface, Sequelize) => {
    const dialectName = queryInterface.sequelize.getDialect();

    if (dialectName === 'mysql') {
      await queryInterface.createTable('users', {
        id: {
          type: Sequelize.INTEGER,
          primaryKey: true,
          autoIncrement: true
        },
        data: {
          type: Sequelize.JSON  // Tipo JSON do MySQL
        }
      });
    } else if (dialectName === 'postgres') {
      await queryInterface.createTable('users', {
        id: {
          type: Sequelize.INTEGER,
          primaryKey: true,
          autoIncrement: true
        },
        data: {
          type: Sequelize.JSONB  // Tipo JSONB do PostgreSQL
        }
      });
    }
  }
};
```

## Recursos

- **references/orm-switching.md**: Guias de migração de ORM
- **references/schema-migration.md**: Padrões de transformação de schema
- **references/data-transformation.md**: Scripts de migração de dados
- **references/rollback-strategies.md**: Procedimentos de rollback
- **assets/schema-migration-template.sql**: Templates de migração SQL
- **assets/data-migration-script.py**: Utilitários de migração de dados
- **scripts/test-migration.sh**: Script de teste de migração

## Melhores Práticas

1. **Sempre Forneça Rollback**: Cada up() precisa de um down()
2. **Teste Migrações**: Teste em staging primeiro
3. **Use Transações**: Migrações atômicas quando possível
4. **Faça Backup Primeiro**: Sempre faça backup antes de migrar
5. **Mudanças Pequenas**: Divida em passos pequenos e incrementais
6. **Monitore**: Observe erros durante o deployment
7. **Documente**: Explique por que e como
8. **Idempotente**: Migrações devem ser rexecutáveis

## Armadilhas Comuns

- Não testar procedimentos de rollback
- Fazer mudanças que quebram compatibilidade sem estratégia de downtime
- Esquecer de lidar com valores NULL
- Não considerar desempenho de índices
- Ignorar restrições de chave estrangeira
- Migrar muitos dados de uma vez