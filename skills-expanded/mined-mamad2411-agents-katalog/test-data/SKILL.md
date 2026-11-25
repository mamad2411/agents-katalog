---
name: test-data
description: "Generate realistic test data with Faker, create database seeds, manage fixtures, and build factory patterns."
metadata: {"thinkfleetbot":{"emoji":"🎲","requires":{"anyBins":["python3","node","npx"]}}}
---

# Test Data Generation

Generate realistic test data for development, testing, and demos.

## Faker (Python)

```bash
# Quick generation
python3 -c "
from faker import Faker
import json
fake = Faker()
users = [{'name': fake.name(), 'email': fake.email(), 'phone': fake.phone_number(), 'address': fake.address(), 'company': fake.company()} for _ in range(10)]
print(json.dumps(users, indent=2))
"

# Generate CSV
python3 -c "
from faker import Faker
import csv, sys
fake = Faker()
w = csv.writer(sys.stdout)
w.writerow(['name','email','phone','joined'])
for _ in range(100):
    w.writerow([fake.name(), fake.email(), fake.phone_number(), fake.date_between('-2y','today')])
" > test_users.csv

# Locale-specific data
python3 -c "
from faker import Faker
fake = Faker('en_US')
print(fake.name(), fake.zipcode(), fake.state())
fake_jp = Faker('ja_JP')
print(fake_jp.name(), fake_jp.address())
"

# Seeded (reproducible)
python3 -c "
from faker import Faker
fake = Faker()
Faker.seed(42)
print(fake.name())  # Always same result
"
```

## Faker (JavaScript)

```bash
# Generate JSON test data
node -e "
const { faker } = require('@faker-js/faker');
const users = Array.from({length: 10}, () => ({
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  avatar: faker.image.avatar(),
  createdAt: faker.date.past().toISOString(),
}));
console.log(JSON.stringify(users, null, 2));
"
```

## Database Seeding

### PostgreSQL

```bash
# Generate and insert directly
python3 -c "
from faker import Faker
fake = Faker()
Faker.seed(42)
for i in range(100):
    name = fake.name().replace(\"'\", \"''\")
    email = fake.email()
    print(f\"INSERT INTO users (name, email, created_at) VALUES ('{name}', '{email}', '{fake.date_between('-1y', 'today')}');\")
" | psql $DATABASE_URL
```

### JSON fixtures

```bash
# Generate fixture file
python3 -c "
from faker import Faker
import json
fake = Faker()
Faker.seed(42)
data = {
    'users': [{'id': i, 'name': fake.name(), 'email': fake.email()} for i in range(1, 21)],
    'posts': [{'id': i, 'user_id': fake.random_int(1, 20), 'title': fake.sentence(), 'body': fake.paragraph()} for i in range(1, 51)],
    'comments': [{'id': i, 'post_id': fake.random_int(1, 50), 'user_id': fake.random_int(1, 20), 'text': fake.sentence()} for i in range(1, 101)]
}
print(json.dumps(data, indent=2))
" > fixtures/test_data.json
```

## Specific Data Types

```bash
python3 -c "
from faker import Faker
fake = Faker()

# Financial
print('CC:', fake.credit_card_number())
print('IBAN:', fake.iban())
print('Price:', fake.pricetag())

# Technical
print('IP:', fake.ipv4())
print('MAC:', fake.mac_address())
print('UA:', fake.user_agent())
print('URL:', fake.url())

# Content
print('Paragraph:', fake.paragraph())
print('BS:', fake.bs())
print('Job:', fake.job())

# Dates
print('Past:', fake.date_between('-1y', 'today'))
print('Future:', fake.date_between('today', '+1y'))
"
```

## Notes

- Always use `Faker.seed()` for reproducible test data in CI.
- Install: `pip install faker` or `npm install @faker-js/faker`.
- Never use Faker-generated data that looks like real PII in production databases.
- For load testing, generate data in bulk and import via COPY/bulk insert, not row-by-row INSERT.
- JSON fixtures are portable across test frameworks. Store them in `fixtures/` or `test/data/`.
