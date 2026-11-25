---
name: tools-unity-state-machine
description: State machine patterns for Unity including hierarchical states, async transitions, and cleanup safety.
---

# Unity State Machine Patterns

## Overview

State machines manage game flow, UI navigation, and entity behavior. This skill covers safe implementation patterns for async state transitions and proper cleanup.

## When to Use

- Game state management (menu, loading, gameplay)
- UI navigation flows
- AI behavior states
- Animation state control
- Feature/activity controllers

## Basic State Machine

### State Interface

```csharp
public interface IState
{
    UniTask Enter(IStateTransitionData data);
    UniTask Exit(bool applicationExiting);
    UniTask Suspend(IStateTransitionData nextStateData);
    UniTask Resume();
    IStateTransitionData GetTransitionData();
}

public interface IStateTransitionData
{
    Type Installer { get; }
}
```

### Simple State Implementation

```csharp
public abstract class BaseState : IState
{
    protected bool IsActive { get; private set; }
    protected bool IsSuspended { get; private set; }
    
    public virtual async UniTask Enter(IStateTransitionData data)
    {
        IsActive = true;
        IsSuspended = false;
        await OnEnter(data);
    }
    
    public virtual async UniTask Exit(bool applicationExiting)
    {
        if (!IsActive) return;
        
        IsActive = false;
        await OnExit(applicationExiting);
    }
    
    public virtual async UniTask Suspend(IStateTransitionData nextStateData)
    {
        IsSuspended = true;
        await OnSuspend();
    }
    
    public virtual async UniTask Resume()
    {
        IsSuspended = false;
        await OnResume();
    }
    
    protected abstract UniTask OnEnter(IStateTransitionData data);
    protected abstract UniTask OnExit(bool applicationExiting);
    protected virtual UniTask OnSuspend() => UniTask.CompletedTask;
    protected virtual UniTask OnResume() => UniTask.CompletedTask;
    
    public abstract IStateTransitionData GetTransitionData();
}
```

## State Navigation Controller

### Core Navigation Controller

```csharp
public class StateNavigationController : IStateNavigator
{
    private readonly LifetimeScope _rootScope;
    private readonly List<LifetimeScope> _stateStack = new();
    private bool _navigationInProgress;
    
    public StateNavigationController(LifetimeScope rootScope)
    {
        _rootScope = rootScope;
    }
    
    public async UniTask NavigateTo(IStateTransitionData transitionData)
    {
        // Wait for any ongoing navigation
        if (_navigationInProgress)
        {
            var waited = await UniTask.WaitUntil(() => !_navigationInProgress)
                .TimeoutWithoutException(TimeSpan.FromSeconds(5));
            
            if (!waited)
            {
                Debug.LogError("Navigation timeout - forcing through");
                _navigationInProgress = false;
            }
        }
        
        _navigationInProgress = true;
        
        try
        {
            // Exit all current states
            await ExitAllStates();
            
            // Enter new state
            await EnterState(transitionData);
        }
        finally
        {
            _navigationInProgress = false;
        }
    }
    
    public async UniTask NavigateToAdditive(IStateTransitionData transitionData)
    {
        if (_navigationInProgress)
        {
            await UniTask.WaitUntil(() => !_navigationInProgress);
        }
        
        _navigationInProgress = true;
        
        try
        {
            // Suspend current state
            if (_stateStack.Count > 0)
            {
                var currentScope = _stateStack[^1];
                if (TryResolveState(currentScope, out var currentState))
                {
                    await currentState.Suspend(transitionData);
                }
            }
            
            // Enter new state additively
            await EnterState(transitionData);
        }
        finally
        {
            _navigationInProgress = false;
        }
    }
    
    public async UniTask ExitActiveState()
    {
        if (_navigationInProgress || _stateStack.Count == 0)
            return;
        
        _navigationInProgress = true;
        
        try
        {
            // Pop and exit top state
            var exitScope = PopState();
            
            if (TryResolveState(exitScope, out var exitState))
            {
                await exitState.Exit(false);
            }
            
            // CRITICAL: Wait before disposal
            await UniTask.Yield();
            
            exitScope.Dispose();
            
            // Resume underlying state
            if (_stateStack.Count > 0)
            {
                var revealedScope = _stateStack[^1];
                if (TryResolveState(revealedScope, out var revealedState))
                {
                    await revealedState.Resume();
                }
            }
        }
        finally
        {
            _navigationInProgress = false;
        }
    }
    
    private async UniTask EnterState(IStateTransitionData transitionData)
    {
        var installer = (IInstaller)Activator.CreateInstance(transitionData.Installer);
        var stateScope = _rootScope.CreateChild(installer);
        
        _stateStack.Add(stateScope);
        
        if (TryResolveState(stateScope, out var state))
        {
            await state.Enter(transitionData);
        }
    }
    
    private async UniTask ExitAllStates()
    {
        while (_stateStack.Count > 0)
        {
            var scope = PopState();
            
            if (TryResolveState(scope, out var state))
            {
                await state.Exit(false);
            }
            
            await UniTask.Yield();
            scope.Dispose();
        }
    }
    
    private LifetimeScope PopState()
    {
        var index = _stateStack.Count - 1;
        var scope = _stateStack[index];
        _stateStack.RemoveAt(index);
        return scope;
    }
    
    private bool TryResolveState(LifetimeScope scope, out IState state)
    {
        state = null;
        try
        {
            if (scope?.Container == null) return false;
            state = scope.Container.Resolve<IState>();
            return state != null;
        }
        catch
        {
            return false;
        }
    }
    
    public async UniTask Shutdown()
    {
        for (int i = _stateStack.Count - 1; i >= 0; i--)
        {
            var scope = _stateStack[i];
            
            if (TryResolveState(scope, out var state))
            {
                await state.Exit(true);
            }
            
            scope.Dispose();
        }
        
        _stateStack.Clear();
    }
}
```

## Activity State Pattern

### Activity State Base

```csharp
public abstract class ActivityState<TController> : IState 
    where TController : IActivityController
{
    private readonly TController _controller;
    private bool _disposed;
    
    protected ActivityState(TController controller)
    {
        _controller = controller;
    }
    
    public async UniTask Enter(IStateTransitionData data)
    {
        if (_disposed) return;
        await _controller.Initialize(data);
    }
    
    public async UniTask Exit(bool applicationExiting)
    {
        if (_disposed) return;
        _disposed = true;
        
        await _controller.Shutdown(applicationExiting);
    }
    
    public async UniTask Suspend(IStateTransitionData nextStateData)
    {
        if (_disposed) return;
        await _controller.Suspend(nextStateData);
    }
    
    public async UniTask Resume()
    {
        if (_disposed) return;
        await _controller.Resume();
    }
    
    public IStateTransitionData GetTransitionData()
    {
        return _controller.GetTransitionData();
    }
}
```

### Activity Controller Base

```csharp
public abstract class ActivityController<TData, TView> : IActivityController
    where TData : IStateTransitionData
    where TView : ActivityView
{
    protected TData TransitionData { get; private set; }
    protected TView View { get; private set; }
    protected CancellationTokenSource LifecycleCts { get; private set; }
    
    private bool _isShuttingDown;
    
    public async UniTask Initialize(IStateTransitionData data)
    {
        TransitionData = (TData)data;
        LifecycleCts = new CancellationTokenSource();
        
        await LoadView();
        await SetupView();
        await OnInitialized();
        
        View.SetActive(true);
    }
    
    public async UniTask Shutdown(bool applicationExiting)
    {
        if (_isShuttingDown) return;
        _isShuttingDown = true;
        
        // Cancel pending operations
        LifecycleCts?.Cancel();
        
        if (!applicationExiting)
        {
            await View.PlayExitAnimation();
        }
        
        await OnShutdown(applicationExiting);
        
        ReleaseView();
        
        LifecycleCts?.Dispose();
        LifecycleCts = null;
    }
    
    public virtual async UniTask Suspend(IStateTransitionData nextStateData)
    {
        View.SetInteractable(false);
        await OnSuspended();
    }
    
    public virtual async UniTask Resume()
    {
        View.SetInteractable(true);
        await OnResumed();
    }
    
    protected abstract UniTask OnInitialized();
    protected abstract UniTask OnShutdown(bool applicationExiting);
    protected virtual UniTask OnSuspended() => UniTask.CompletedTask;
    protected virtual UniTask OnResumed() => UniTask.CompletedTask;
    
    public abstract IStateTransitionData GetTransitionData();
}
```

## Hierarchical State Machine

### HSM Implementation

```csharp
public class HierarchicalStateMachine
{
    private readonly Dictionary<string, IState> _states = new();
    private readonly Dictionary<string, string> _parentStates = new();
    private readonly Stack<string> _activeStateStack = new();
    
    public string CurrentState => _activeStateStack.Count > 0 ? _activeStateStack.Peek() : null;
    
    public void AddState(string id, IState state, string parentId = null)
    {
        _states[id] = state;
        if (parentId != null)
            _parentStates[id] = parentId;
    }
    
    public async UniTask TransitionTo(string targetState)
    {
        // Find common ancestor
        var currentPath = GetStatePath(CurrentState);
        var targetPath = GetStatePath(targetState);
        
        var commonAncestor = FindCommonAncestor(currentPath, targetPath);
        
        // Exit states up to common ancestor
        while (_activeStateStack.Count > 0 && _activeStateStack.Peek() != commonAncestor)
        {
            var stateId = _activeStateStack.Pop();
            if (_states.TryGetValue(stateId, out var state))
            {
                await state.Exit(false);
            }
        }
        
        // Enter states from common ancestor to target
        var enterStates = new List<string>();
        var current = targetState;
        
        while (current != null && current != commonAncestor)
        {
            enterStates.Insert(0, current);
            _parentStates.TryGetValue(current, out current);
        }
        
        foreach (var stateId in enterStates)
        {
            _activeStateStack.Push(stateId);
            if (_states.TryGetValue(stateId, out var state))
            {
                await state.Enter(null);
            }
        }
    }
    
    private List<string> GetStatePath(string stateId)
    {
        var path = new List<string>();
        var current = stateId;
        
        while (current != null)
        {
            path.Insert(0, current);
            _parentStates.TryGetValue(current, out current);
        }
        
        return path;
    }
    
    private string FindCommonAncestor(List<string> path1, List<string> path2)
    {
        string common = null;
        var minLength = Math.Min(path1.Count, path2.Count);
        
        for (int i = 0; i < minLength; i++)
        {
            if (path1[i] == path2[i])
                common = path1[i];
            else
                break;
        }
        
        return common;
    }
}
```

## State Machine Patterns

### Transition Guards

```csharp
public class GuardedStateMachine
{
    private readonly Dictionary<(string from, string to), Func<bool>> _guards = new();
    
    public void AddGuard(string fromState, string toState, Func<bool> guard)
    {
        _guards[(fromState, toState)] = guard;
    }
    
    public bool CanTransition(string from, string to)
    {
        if (_guards.TryGetValue((from, to), out var guard))
        {
            return guard();
        }
        return true; // No guard = allowed
    }
    
    public async UniTask<bool> TryTransitionTo(string targetState)
    {
        if (!CanTransition(CurrentState, targetState))
        {
            Debug.Log($"Transition from {CurrentState} to {targetState} blocked by guard");
            return false;
        }
        
        await TransitionTo(targetState);
        return true;
    }
}
```

### Transition Actions

```csharp
public class StateMachineWithActions
{
    public event Action<string, string> OnStateTransition;
    public event Action<string> OnStateEntered;
    public event Action<string> OnStateExited;
    
    public async UniTask TransitionTo(string targetState)
    {
        var previousState = CurrentState;
        
        if (_states.TryGetValue(previousState, out var exitingState))
        {
            await exitingState.Exit(false);
            OnStateExited?.Invoke(previousState);
        }
        
        CurrentState = targetState;
        OnStateTransition?.Invoke(previousState, targetState);
        
        if (_states.TryGetValue(targetState, out var enteringState))
        {
            await enteringState.Enter(null);
            OnStateEntered?.Invoke(targetState);
        }
    }
}
```

### State History

```csharp
public class StateMachineWithHistory
{
    private readonly Stack<string> _history = new();
    private const int MaxHistorySize = 20;
    
    public bool CanGoBack => _history.Count > 0;
    
    public async UniTask TransitionTo(string targetState)
    {
        if (CurrentState != null)
        {
            _history.Push(CurrentState);
            
            // Limit history size
            while (_history.Count > MaxHistorySize)
            {
                // Remove oldest entries (need to convert to list)
            }
        }
        
        await DoTransition(targetState);
    }
    
    public async UniTask GoBack()
    {
        if (!CanGoBack) return;
        
        var previousState = _history.Pop();
        await DoTransition(previousState);
    }
    
    public void ClearHistory()
    {
        _history.Clear();
    }
}
```

## Cleanup Patterns

### Safe Async Disposal

```csharp
public class SafeStateController
{
    private CancellationTokenSource _cts;
    private bool _disposed;
    
    public async UniTask Initialize()
    {
        _cts = new CancellationTokenSource();
        await StartBackgroundTasks(_cts.Token);
    }
    
    public async UniTask Shutdown(bool immediate)
    {
        if (_disposed) return;
        _disposed = true;
        
        // Cancel all pending operations
        _cts?.Cancel();
        
        if (!immediate)
        {
            // Give time for graceful cancellation
            try
            {
                await UniTask.Delay(100, cancellationToken: default);
            }
            catch { }
        }
        
        _cts?.Dispose();
        _cts = null;
    }
    
    private async UniTask StartBackgroundTasks(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            await DoWork(ct);
            await UniTask.Delay(1000, cancellationToken: ct);
        }
    }
}
```

### Force Hidden State Pattern

```csharp
public interface IForceHideable
{
    void ForceHiddenSuspend();
    void ReleaseForceHidden();
}

public class ActivityState : IState, IForceHideable
{
    private bool _isForcedHidden;
    
    public void ForceHiddenSuspend()
    {
        if (_isForcedHidden) return;
        _isForcedHidden = true;
        
        View.SetActive(false, immediate: true);
    }
    
    public void ReleaseForceHidden()
    {
        if (!_isForcedHidden) return;
        _isForcedHidden = false;
        
        View.SetActive(true, immediate: true);
    }
}
```

## Best Practices

1. **Guard against concurrent navigation** - Use flags/locks
2. **Wait before scope disposal** - Allow pending callbacks
3. **Use CancellationToken** - For all async state operations
4. **Track disposed state** - Prevent double-disposal
5. **Separate sync/async exits** - `applicationExiting` parameter
6. **Log state transitions** - For debugging
7. **Use typed transition data** - Type-safe state parameters
8. **Implement proper cleanup** - Release resources in Exit
9. **Handle navigation timeout** - Don't deadlock on navigation
10. **Test state transitions** - Cover edge cases

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Navigation deadlock | Add timeout to WaitUntil |
| Double disposal | Track disposed flag |
| Callbacks after exit | Use CancellationToken |
| Scope disposed early | Wait after Exit before Dispose |
| Lost state on crash | Implement state persistence |
