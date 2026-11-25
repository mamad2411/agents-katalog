---
name: arabic-graphql
name_ar: غرافكيو إل
description: Build GraphQL APIs in Arabic
description_ar: بناء واجهات غرافكيو إل بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

بناء GraphQL APIs باللغة العربية.

## المفاهيم الأساسية

| المصطلح | العربية |
|---------|---------|
| Schema | المخطط |
| Query | استعلام |
| Mutation | تعديل |
| Subscription | اشتراك |
| Resolver | المحلل |
| Type | النوع |

## Schema مثال

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

type Query {
  user(id: ID!): User
  users: [User!]!
  post(id: ID!): Post
}

type Mutation {
  createUser(name: String!, email: String!): User
  updateUser(id: ID!, name: String, email: String): User
  deleteUser(id: ID!): Boolean
}
```

## استعلامات

```graphql
# جلب مستخدم
query {
  user(id: "123") {
    name
    email
    posts {
      title
    }
  }
}

# تعديل
mutation {
  createUser(name: "أحمد", email: "ahmed@example.com") {
    id
    name
  }
}
```

## Resolver مثال (Node.js)

```javascript
const resolvers = {
  Query: {
    user: (_, { id }) => getUserById(id),
    users: () => getAllUsers()
  },
  Mutation: {
    createUser: (_, args) => createUser(args)
  }
};
```

## أفضل الممارسات

✅ Types واضحة
✅ Nullability صحيحة
✅ Error handling
✅ Pagination
✅ Authorization

---

## الكلمات المفتاحية

عربي: "غرافكيو إل", "graphql", "API"
English: "graphql arabic", "api design", "backend"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
