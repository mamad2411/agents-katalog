---
name: tpl-backend-elixir-phoenix
description: Template do pack (backend/10-elixir-phoenix.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/10-elixir-phoenix.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Elixir Phoenix API + LiveView App

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/10-elixir-phoenix.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Language:** Elixir 1.16 / OTP 26
- **Framework:** Phoenix 1.7 + Phoenix LiveView 0.20
- **Database:** PostgreSQL via Ecto 3.11
- **Testing:** ExUnit + Mox + Wallaby (E2E)
- **Linting:** Credo + Dialyzer
- **Auth:** phx_gen_auth (sessions) or Guardian (JWT)

---

## PROJECT STRUCTURE
```
lib/
├── my_app/                   # Core business logic (Contexts)
│   ├── accounts/
│   │   ├── accounts.ex       # Public context API
│   │   ├── user.ex           # Ecto schema
│   │   └── user_token.ex
│   ├── blog/
│   │   ├── blog.ex
│   │   └── post.ex
│   └── workers/
│       └── email_worker.ex   # GenServer / Oban job
├── my_app_web/               # Web layer
│   ├── router.ex
│   ├── endpoint.ex
│   ├── controllers/
│   │   ├── user_controller.ex
│   │   └── fallback_controller.ex
│   ├── live/
│   │   ├── post_live/
│   │   │   ├── index.ex
│   │   │   └── index.html.heex
│   │   └── post_live/
│   │       ├── show.ex
│   │       └── show.html.heex
│   ├── channels/
│   │   └── room_channel.ex
│   └── views/
│       └── error_view.ex
priv/
└── repo/
    └── migrations/
test/
├── my_app/
│   └── accounts_test.exs
└── my_app_web/
    ├── controllers/
    └── live/
```

---

## ARCHITECTURE RULES
1. **Contexts are the only public API** — `MyApp.Accounts.get_user/1`, never `Repo.get(User, id)` from controllers.
2. **Schemas are dumb** — schemas hold field definitions and `changeset/2` only; no business logic.
3. **FallbackController handles all errors** — controllers call `with` patterns and fall through to `{:error, ...}`.
4. **LiveView mounts must assign minimal data** — use `handle_params/3` to load page-specific data lazily.
5. **GenServer only for stateful processes** — if you need a cache, counter, or connection manager; not for one-off tasks.
6. **Channels for real-time push** — use Phoenix Channels; do not poll from the frontend.
7. **Credo + Dialyzer must pass** — `mix credo --strict` and `mix dialyzer` are CI blockers.

---

## ECTO CHANGESETS

```elixir
# lib/my_app/accounts/user.ex
defmodule MyApp.Accounts.User do
  use Ecto.Schema
  import Ecto.Changeset

  @derive {Jason.Encoder, only: [:id, :email, :name, :inserted_at]}
  schema "users" do
    field :email,           :string
    field :name,            :string
    field :hashed_password, :string, redact: true
    timestamps()
  end

  @required [:email, :name, :password]
  def registration_changeset(user \\ %__MODULE__{}, attrs) do
    user
    |> cast(attrs, @required)
    |> validate_required(@required)
    |> validate_format(:email, ~r/@/, message: "must have @")
    |> validate_length(:name, min: 2, max: 100)
    |> validate_length(:password, min: 8, max: 72)
    |> unique_constraint(:email)
    |> put_password_hash()
  end

  defp put_password_hash(%Ecto.Changeset{valid?: true, changes: %{password: pw}} = cs),
    do: change(cs, hashed_password: Bcrypt.hash_pwd_salt(pw))
  defp put_password_hash(cs), do: cs
end
```

---

## CONTEXT + CONTROLLER PATTERN

```elixir
# lib/my_app/accounts/accounts.ex
defmodule MyApp.Accounts do
  alias MyApp.Repo
  alias MyApp.Accounts.User

  def get_user(id), do: Repo.get(User, id)
  def get_user!(id), do: Repo.get!(User, id)

  def create_user(attrs) do
    %User{}
    |> User.registration_changeset(attrs)
    |> Repo.insert()
  end

  def list_users(opts \\ []) do
    limit  = Keyword.get(opts, :limit, 20)
    offset = Keyword.get(opts, :offset, 0)
    Repo.all(from u in User, limit: ^limit, offset: ^offset, order_by: [asc: u.inserted_at])
  end
end

# lib/my_app_web/controllers/user_controller.ex
defmodule MyAppWeb.UserController do
  use MyAppWeb, :controller
  alias MyApp.Accounts
  action_fallback MyAppWeb.FallbackController

  def index(conn, _params) do
    users = Accounts.list_users()
    render(conn, :index, users: users)
  end

  def create(conn, %{"user" => user_params}) do
    with {:ok, user} <- Accounts.create_user(user_params) do
      conn |> put_status(:created) |> render(:show, user: user)
    end
  end

  def show(conn, %{"id" => id}) do
    with user when not is_nil(user) <- Accounts.get_user(id) do
      render(conn, :show, user: user)
    else
      nil -> {:error, :not_found}
    end
  end
end

# lib/my_app_web/controllers/fallback_controller.ex
defmodule MyAppWeb.FallbackController do
  use MyAppWeb, :controller

  def call(conn, {:error, %Ecto.Changeset{} = cs}) do
    conn |> put_status(:unprocessable_entity)
         |> render(:error, changeset: cs)
  end

  def call(conn, {:error, :not_found}) do
    conn |> put_status(:not_found) |> render(:error, message: "Not found")
  end

  def call(conn, {:error, :unauthorized}) do
    conn |> put_status(:unauthorized) |> render(:error, message: "Unauthorized")
  end
end
```

---

## PHOENIX CHANNELS

```elixir
# lib/my_app_web/channels/room_channel.ex
defmodule MyAppWeb.RoomChannel do
  use Phoenix.Channel
  alias MyApp.Blog

  def join("room:" <> room_id, _payload, socket) do
    send(self(), {:after_join, room_id})
    {:ok, assign(socket, :room_id, room_id)}
  end

  def handle_info({:after_join, room_id}, socket) do
    messages = Blog.list_messages(room_id, limit: 50)
    push(socket, "history", %{messages: messages})
    {:noreply, socket}
  end

  def handle_in("new_message", %{"body" => body}, socket) do
    case Blog.create_message(socket.assigns.room_id, body, socket.assigns.current_user) do
      {:ok, msg} ->
        broadcast!(socket, "new_message", %{id: msg.id, body: msg.body})
        {:noreply, socket}
      {:error, _cs} ->
        {:reply, {:error, %{reason: "invalid"}}, socket}
    end
  end
end
```

---

## GENSERVER PATTERN (Cache Example)

```elixir
defmodule MyApp.StatCounter do
  use GenServer

  # Client API
  def start_link(opts), do: GenServer.start_link(__MODULE__, %{}, opts)
  def increment(key),   do: GenServer.cast(__MODULE__, {:inc, key})
  def get(key),         do: GenServer.call(__MODULE__, {:get, key})

  # Server callbacks
  @impl true
  def init(state), do: {:ok, state}

  @impl true
  def handle_cast({:inc, key}, state) do
    {:noreply, Map.update(state, key, 1, &(&1 + 1))}
  end

  @impl true
  def handle_call({:get, key}, _from, state) do
    {:reply, Map.get(state, key, 0), state}
  end
end
```

---

## ROUTING TABLE

| Verb | Path | Controller/LiveView | Action |
|------|------|---------------------|--------|
| GET | /api/users | UserController | :index |
| POST | /api/users | UserController | :create |
| GET | /api/users/:id | UserController | :show |
| PUT | /api/users/:id | UserController | :update |
| DELETE | /api/users/:id | UserController | :delete |
| POST | /api/sessions | SessionController | :create (login) |
| DELETE | /api/sessions | SessionController | :delete (logout) |
| GET | /posts | PostLive.Index | (LiveView) |
| GET | /posts/:id | PostLive.Show | (LiveView) |
| WS | /socket | UserSocket + RoomChannel | real-time |

---

## QUALITY GATES
- [ ] `mix compile --warnings-as-errors` — zero warnings
- [ ] `mix credo --strict` — clean
- [ ] `mix dialyzer` — no type errors
- [ ] `mix test` — all pass; no skipped without reason
- [ ] All contexts tested independently (no controller in unit tests)
- [ ] Changesets return descriptive error messages
- [ ] `mix coveralls` ≥ 80% coverage
- [ ] Phoenix.PubSub used for cross-process events (not direct PID messages)

---

## FORBIDDEN
- ❌ `Repo.*` calls inside controllers, views, or LiveViews — use Contexts
- ❌ `GenServer` for things a simple function call handles
- ❌ `send/2` to unknown PIDs — always use Registry or named processes
- ❌ Atoms from user input (`String.to_atom/1`) — use `String.to_existing_atom/1`
- ❌ `IO.inspect/puts` in production code — use `Logger`
- ❌ Mutable global state via `:ets` without supervision
- ❌ Business logic in templates or LiveView `render/1`
