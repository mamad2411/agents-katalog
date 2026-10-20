---
description: 
globs: 
alwaysApply: true
---
# CalorieCam Database Schema
## Rule Type: Always

Use a dedicated Supabase database for calorie tracking with this schema:

```sql
-- Users (auth optional)
create table users (
  id uuid primary key default gen_random_uuid(),
  email text unique,
  created_at timestamptz default now()
);

-- Food Logs
create table food_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  image_url text not null,
  food_name text,
  calories integer,
  proteins numeric(5,2),
  fats numeric(5,2),
  carbs numeric(5,2),
  logged_at timestamptz default now()
);

•	Allow anonymous uploads (user_id nullable), but progress tracked only for logged-in users.