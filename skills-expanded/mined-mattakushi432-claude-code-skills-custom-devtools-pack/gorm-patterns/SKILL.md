---
name: gorm-patterns
description: "When to activate: GORM ORM, models, queries, associations, hooks, migrations, transactions, soft delete in Go"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: go
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# GORM Patterns

## Model Definition

```go
import "gorm.io/gorm"

type User struct {
    gorm.Model           // embeds ID, CreatedAt, UpdatedAt, DeletedAt (soft delete)
    Email     string     `gorm:"uniqueIndex;not null"`
    Name      string     `gorm:"not null"`
    Role      string     `gorm:"default:user"`
    Articles  []Article  `gorm:"foreignKey:AuthorID"`
}

type Article struct {
    gorm.Model
    Title    string `gorm:"not null"`
    Body     string `gorm:"type:text"`
    AuthorID uint
    Author   User
    Tags     []Tag `gorm:"many2many:article_tags"`
}

type Tag struct {
    gorm.Model
    Name     string    `gorm:"uniqueIndex"`
    Articles []Article `gorm:"many2many:article_tags"`
}
```

## Connection and Auto-Migrate

```go
import (
    "gorm.io/driver/postgres"
    "gorm.io/gorm"
    "gorm.io/gorm/logger"
)

func NewDB(dsn string) (*gorm.DB, error) {
    db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Warn),
        NowFunc: time.Now,
    })
    if err != nil { return nil, err }

    sqlDB, _ := db.DB()
    sqlDB.SetMaxOpenConns(25)
    sqlDB.SetMaxIdleConns(10)
    sqlDB.SetConnMaxLifetime(5 * time.Minute)

    return db, nil
}

func Migrate(db *gorm.DB) error {
    return db.AutoMigrate(&User{}, &Article{}, &Tag{})
}
```

## CRUD Operations

```go
// Create
user := User{Email: "alice@example.com", Name: "Alice"}
result := db.Create(&user)
if result.Error != nil { return result.Error }
// user.ID is now populated

// Find
var user User
db.First(&user, "id = ?", id)                  // by primary key
db.First(&user, "email = ?", "alice@example.com")

// Preload associations
db.Preload("Articles.Tags").First(&user, id)

// Update — only changed fields with Save; specific fields with Updates
user.Name = "Alice Smith"
db.Save(&user)                                   // UPDATE all columns
db.Model(&user).Update("name", "Alice Smith")    // UPDATE one column
db.Model(&user).Updates(map[string]any{          // UPDATE multiple
    "name": "Alice Smith",
    "role": "admin",
})

// Delete (soft delete when gorm.Model embedded)
db.Delete(&user, id)

// Hard delete
db.Unscoped().Delete(&user, id)
```

## Queries with Conditions

```go
var articles []Article

db.Where("author_id = ? AND created_at > ?", authorID, since).
    Order("created_at DESC").
    Limit(20).
    Offset((page-1) * 20).
    Find(&articles)

// Count
var total int64
db.Model(&Article{}).Where("author_id = ?", authorID).Count(&total)

// Scopes for reusable query fragments
func published(db *gorm.DB) *gorm.DB {
    return db.Where("published_at IS NOT NULL AND published_at <= ?", time.Now())
}

func byAuthor(authorID uint) func(*gorm.DB) *gorm.DB {
    return func(db *gorm.DB) *gorm.DB {
        return db.Where("author_id = ?", authorID)
    }
}

db.Scopes(published, byAuthor(1)).Find(&articles)
```

## Transactions

```go
func transferCredits(from, to uint, amount int) error {
    return db.Transaction(func(tx *gorm.DB) error {
        if err := tx.Model(&User{}).Where("id = ? AND credits >= ?", from, amount).
            Update("credits", gorm.Expr("credits - ?", amount)).Error; err != nil {
            return err
        }
        if err := tx.Model(&User{}).Where("id = ?", to).
            Update("credits", gorm.Expr("credits + ?", amount)).Error; err != nil {
            return err
        }
        return nil
    })
}
```

## Hooks

```go
func (u *User) BeforeCreate(tx *gorm.DB) error {
    u.Email = strings.ToLower(u.Email)
    hashed, err := bcrypt.GenerateFromPassword([]byte(u.Password), bcrypt.DefaultCost)
    if err != nil { return err }
    u.PasswordHash = string(hashed)
    u.Password = ""  // don't persist plain text
    return nil
}

func (u *User) AfterCreate(tx *gorm.DB) error {
    return tx.Create(&AuditLog{Action: "user_created", UserID: u.ID}).Error
}
```

## Common Anti-Patterns

- **`db.Find` without limit** — always paginate; unbounded queries can OOM the server
- **Ignoring `result.Error`** — GORM doesn't panic; always check the error
- **N+1 queries** — use `Preload` or `Joins` instead of loading associations in a loop
- **AutoMigrate in production** — wrap in a proper migration tool (goose, migrate) for reversible changes
- **Using GORM in repository layer directly** — wrap in a repository interface for testability
