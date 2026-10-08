# 🐝 Colony OS Kernel - Setup Instructions

## Step 1: Configure Environment Variables

1. **Open** `colony-os/.env` file
2. **Replace** `SUPABASE_KEY` with your actual service role key:

```bash
SUPABASE_URL="https://vuanulvyqkfefmjcikfk.supabase.co"
SUPABASE_KEY="your-actual-service-role-key-here"
```

### How to Get Your Service Role Key:

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project: **zyeuté**
3. Navigate to: **Project Settings** > **API**
4. Copy the **`service_role`** key (not the `anon` key)
5. Paste it into `.env` file

⚠️ **Important:** The `service_role` key bypasses Row Level Security (RLS). Keep it secret and only use it in backend code.

## Step 2: Install Dependencies

```bash
cd colony-os
pip install -r requirements.txt
```

## Step 3: Verify Connection

Run the example script to test the Supabase connection:

```bash
python example_usage.py
```

You should see:
- ✅ Supabase client initialized
- 📝 Task persisted to DB: [task_id]
- ✅ Task [task_id] status: completed

## Step 4: Check Supabase

1. Go to Supabase Dashboard > **Table Editor**
2. Select the **`tasks`** table
3. You should see your test task with:
   - `type`: "document_summary"
   - `status`: "completed"
   - `result`: JSON with the processing result

## 🎯 Success Criteria

✅ Tasks are persisted to Supabase before execution  
✅ Task status updates through: `pending` → `assigned` → `in_progress` → `completed`  
✅ Results are stored in the `result` JSONB column  
✅ Tasks survive server restarts (they're in the database!)

---

**The Hive now has memory!** 🧠🐝

