---
name: cpp-concurrency
description: "When to activate: C++ concurrency, std::thread, mutex, atomic, future, promise, coroutines, thread pool, parallel algorithms"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: cpp
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# C++ Concurrency Patterns

## std::thread & RAII Guard

```cpp
#include <thread>
#include <mutex>

// jthread (C++20) — auto-joins on destruction, supports stop_token
std::jthread worker([](std::stop_token st) {
    while (!st.stop_requested()) {
        doWork();
    }
});
// worker.request_stop() + auto-join on scope exit

// RAII lock guard
std::mutex mtx;
{
    std::scoped_lock lock{mtx};  // C++17, handles multiple mutexes
    sharedData.push_back(42);
}  // unlocks here

// Shared read / exclusive write
std::shared_mutex rwmtx;
{
    std::shared_lock  read_lk{rwmtx};   // multiple readers OK
    auto val = cache[key];
}
{
    std::unique_lock write_lk{rwmtx};   // exclusive
    cache[key] = newVal;
}
```

## Atomic Operations

```cpp
#include <atomic>

std::atomic<int>  counter{0};
std::atomic<bool> ready{false};

// Fetch-and-add (lock-free on most platforms)
counter.fetch_add(1, std::memory_order_relaxed);

// Compare-and-swap
int expected = 0;
bool swapped = counter.compare_exchange_strong(expected, 1);

// Sequentially consistent (default, safest)
counter.store(42);
int val = counter.load();

// Flag for once-initialization
std::atomic_flag flag = ATOMIC_FLAG_INIT;
if (!flag.test_and_set()) { /* first caller */ }
```

## std::future / std::promise

```cpp
#include <future>

// async task
auto future = std::async(std::launch::async, []() -> int {
    return heavyComputation();
});
// ... do other work ...
int result = future.get(); // blocks until ready

// Promise for manual signaling
std::promise<std::string> prom;
auto fut = prom.get_future();

std::jthread producer([&prom] {
    try {
        prom.set_value(fetchData());
    } catch (...) {
        prom.set_exception(std::current_exception());
    }
});

std::string data = fut.get(); // or throws
```

## Parallel Algorithms (C++17)

```cpp
#include <execution>
#include <algorithm>

std::vector<double> data(1'000'000);

// Parallel sort
std::sort(std::execution::par_unseq, data.begin(), data.end());

// Parallel reduce (sum)
double sum = std::reduce(std::execution::par_unseq, data.begin(), data.end(), 0.0);

// Parallel transform
std::transform(std::execution::par_unseq,
    data.begin(), data.end(), data.begin(),
    [](double x) { return std::sqrt(x); });
```

## Thread Pool (Simple)

```cpp
#include <functional>
#include <queue>
#include <condition_variable>

class ThreadPool {
    std::vector<std::jthread> threads_;
    std::queue<std::function<void()>> tasks_;
    std::mutex mtx_;
    std::condition_variable_any cv_;
    bool stop_ = false;

public:
    explicit ThreadPool(std::size_t n) {
        for (std::size_t i = 0; i < n; ++i) {
            threads_.emplace_back([this](std::stop_token st) {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock lk{mtx_};
                        cv_.wait(lk, st, [&]{ return !tasks_.empty() || stop_; });
                        if (stop_ && tasks_.empty()) return;
                        task = std::move(tasks_.front());
                        tasks_.pop();
                    }
                    task();
                }
            });
        }
    }

    template<typename F>
    auto submit(F&& f) -> std::future<std::invoke_result_t<F>> {
        using R = std::invoke_result_t<F>;
        auto task = std::make_shared<std::packaged_task<R()>>(std::forward<F>(f));
        auto fut = task->get_future();
        { std::scoped_lock lk{mtx_}; tasks_.emplace([task]{ (*task)(); }); }
        cv_.notify_one();
        return fut;
    }

    ~ThreadPool() {
        { std::scoped_lock lk{mtx_}; stop_ = true; }
        cv_.notify_all();
    }
};
```

## C++20 Coroutines (with cppcoro)

```cpp
#include <cppcoro/task.hpp>
#include <cppcoro/sync_wait.hpp>

cppcoro::task<int> fetchAsync(std::string url) {
    auto response = co_await httpGet(url);
    co_return response.statusCode;
}

int main() {
    auto code = cppcoro::sync_wait(fetchAsync("http://example.com"));
    std::cout << code << '\n';
}
```
