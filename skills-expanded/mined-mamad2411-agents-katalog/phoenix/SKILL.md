---
name: "phoenix"
description: "Build Elixir Phoenix web applications with LiveView, channels, and Ecto"
---

# Elixir + Phoenix

## When to activate
- Building Phoenix web applications or APIs
- Designing OTP supervision trees with GenServer and Supervisor
- Implementing Phoenix LiveView for server-rendered reactive UIs
- Writing Ecto changesets and database transactions
- Configuring mix releases for production deployment
- Using the pipe operator and pattern matching idioms

## When NOT to use
- Non-Elixir Erlang/OTP work where Elixir syntax is irrelevant
- Simple scripting tasks better handled by a shell script
- When the codebase is Elixir but the question is purely about PostgreSQL query optimization with no Ecto involvement

## Instructions

### GenServer Skeleton

A GenServer is a stateful process. Implement all standard callbacks explicitly:

```elixir
defmodule MyApp.Cache do
  use GenServer
  require Logger

  # --- Client API ---

  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def get(key), do: GenServer.call(__MODULE__, {:get, key})
  def put(key, value), do: GenServer.cast(__MODULE__, {:put, key, value})
  def delete(key), do: GenServer.cast(__MODULE__, {:delete, key})

  # --- Server Callbacks ---

  @impl true
  def init(_opts) do
    {:ok, %{}}   # initial state is an empty map
  end

  @impl true
  def handle_call({:get, key}, _from, state) do
    {:reply, Map.get(state, key), state}
  end

  @impl true
  def handle_cast({:put, key, value}, state) do
    {:noreply, Map.put(state, key, value)}
  end

  @impl true
  def handle_cast({:delete, key}, state) do
    {:noreply, Map.delete(state, key)}
  end

  @impl true
  def handle_info(:cleanup, state) do
    Logger.info("Running cache cleanup")
    {:noreply, %{}}
  end

  @impl true
  def terminate(reason, _state) do
    Logger.warning("Cache terminating: #{inspect(reason)}")
    :ok
  end
end
```

Use `handle_call` for synchronous operations that return a value. Use `handle_cast` for fire-and-forget mutations. Use `handle_info` for messages not sent via `call`/`cast` (timers, process monitor messages).

### Supervision Strategy Selection

```elixir
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = [
      MyApp.Repo,
      MyAppWeb.Endpoint,
      {MyApp.Cache, []},
      {Task.Supervisor, name: MyApp.TaskSupervisor},
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

Strategy guide:
- `:one_for_one` — restart only the crashed child. Use when children are fully independent.
- `:one_for_all` — restart all children when one crashes. Use when all children share state or must start together.
- `:rest_for_one` — restart the crashed child and every child started after it. Use for pipeline-style dependency chains.

Use `DynamicSupervisor` for unbounded, runtime-created processes (e.g., per-user sessions, per-connection workers):

```elixir
{:ok, pid} = DynamicSupervisor.start_child(MyApp.SessionSupervisor, {MyApp.Session, user_id})
```

### Phoenix LiveView — mount/handle_event

```elixir
defmodule MyAppWeb.CounterLive do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, count: 0)}
  end

  @impl true
  def handle_event("increment", _params, socket) do
    {:noreply, update(socket, :count, &(&1 + 1))}
  end

  @impl true
  def handle_event("reset", _params, socket) do
    {:noreply, assign(socket, count: 0)}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div>
      <p>Count: <%= @count %></p>
      <button phx-click="increment">+1</button>
      <button phx-click="reset">Reset</button>
    </div>
    """
  end
end
```

LiveView process lifecycle:
1. `mount/3` — called on static render (no socket) and on live socket connect
2. `handle_params/3` — called after mount when using live navigation
3. `handle_event/3` — handles `phx-click`, `phx-change`, `phx-submit`
4. `handle_info/2` — handles messages from other processes (PubSub broadcasts)

For complex components, extract to `Phoenix.LiveComponent` to scope state and reduce parent re-renders.

### Ecto.Multi for Transactions

Use `Ecto.Multi` to group multiple database operations into an atomic transaction:

```elixir
defmodule MyApp.Accounts do
  alias MyApp.Repo
  alias MyApp.Accounts.{User, Wallet}
  import Ecto.Multi

  def register_user(attrs) do
    Ecto.Multi.new()
    |> Ecto.Multi.insert(:user, User.changeset(%User{}, attrs))
    |> Ecto.Multi.insert(:wallet, fn %{user: user} ->
      Wallet.changeset(%Wallet{}, %{user_id: user.id, balance: 0})
    end)
    |> Ecto.Multi.run(:welcome_email, fn _repo, %{user: user} ->
      case Mailer.send_welcome(user) do
        :ok -> {:ok, user}
        {:error, reason} -> {:error, reason}
      end
    end)
    |> Repo.transaction()
  end
end
```

`Repo.transaction/1` on a Multi returns:
- `{:ok, %{user: user, wallet: wallet, welcome_email: user}}` on success
- `{:error, failed_operation_name, changeset_or_value, changes_so_far}` on failure

Each step receives results from prior steps in the map argument. Rollback is automatic on any `{:error, ...}` return.

### Pipeline Operator Patterns

The pipe operator `|>` passes the result of the left expression as the first argument to the right function:

```elixir
# Data transformation pipeline
def process_orders(user_id) do
  user_id
  |> fetch_orders()
  |> Enum.filter(&(&1.status == :pending))
  |> Enum.map(&calculate_total/1)
  |> Enum.sort_by(& &1.amount, :desc)
  |> Enum.take(10)
end

# String processing
"  Hello, World!  "
|> String.trim()
|> String.downcase()
|> String.split(", ")
# => ["hello", "world!"]

# Pattern matching in pipelines with with
def create_and_notify(attrs) do
  with {:ok, user} <- create_user(attrs),
       {:ok, _token} <- generate_token(user),
       :ok <- send_notification(user) do
    {:ok, user}
  else
    {:error, %Ecto.Changeset{} = cs} -> {:error, format_errors(cs)}
    {:error, reason} -> {:error, reason}
  end
end
```

Use `with` instead of nested `case` expressions for sequences of operations that can each fail independently.

### Environment Config with Config

Phoenix 7 uses the three-file config pattern:

```elixir
# config/config.exs — compile-time, all environments
config :my_app, MyApp.Repo,
  pool_size: 10

config :my_app, MyAppWeb.Endpoint,
  url: [host: "localhost"],
  render_errors: [formats: [html: MyAppWeb.ErrorHTML, json: MyAppWeb.ErrorJSON]]
```

```elixir
# config/runtime.exs — evaluated at runtime, reads System.get_env
import Config

if config_env() == :prod do
  database_url = System.fetch_env!("DATABASE_URL")

  config :my_app, MyApp.Repo,
    url: database_url,
    pool_size: String.to_integer(System.get_env("POOL_SIZE") || "10")

  config :my_app, MyAppWeb.Endpoint,
    secret_key_base: System.fetch_env!("SECRET_KEY_BASE"),
    server: true
end
```

```elixir
# config/dev.exs — development overrides only
config :my_app, MyApp.Repo,
  username: "postgres",
  password: "postgres",
  database: "my_app_dev"
```

Build a mix release:

```bash
MIX_ENV=prod mix release
_build/prod/rel/my_app/bin/my_app start
```

## Example

A PubSub-backed LiveView that shows real-time order updates:

```elixir
defmodule MyAppWeb.OrdersLive do
  use MyAppWeb, :live_view
  alias MyApp.Orders

  @impl true
  def mount(_params, _session, socket) do
    if connected?(socket) do
      Phoenix.PubSub.subscribe(MyApp.PubSub, "orders")
    end

    {:ok, assign(socket, orders: Orders.list_recent())}
  end

  @impl true
  def handle_info({:order_updated, order}, socket) do
    updated = Enum.map(socket.assigns.orders, fn
      %{id: ^(order.id)} -> order
      existing -> existing
    end)
    {:noreply, assign(socket, orders: updated)}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <ul>
      <li :for={order <- @orders}>
        <%= order.id %> — <%= order.status %>
      </li>
    </ul>
    """
  end
end

# Broadcast from the context after an update
def update_order(id, attrs) do
  with {:ok, order} <- do_update(id, attrs) do
    Phoenix.PubSub.broadcast(MyApp.PubSub, "orders", {:order_updated, order})
    {:ok, order}
  end
end
```

---
