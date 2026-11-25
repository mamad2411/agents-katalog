---
name: "Threading & Multi-Threading"
description: "Padrões de threading em FreePascal/Lazarus — TThread, Synchronize, Queue, TCriticalSection, TEvent, thread-safety, Producer-Consumer e cancelamento"
---

# Threading & Multi-Threading — Skill

Use esta skill ao trabalhar com threads e tarefas assíncronas em projetos FreePascal/Lazarus.

## Quando Usar

- Ao executar operações demoradas sem bloquear a UI (LCL)
- Ao criar servidores/workers que processam requisições concorrentes
- Ao sincronizar acesso a recursos compartilhados
- Ao implementar cancelamento gracioso de threads

## Regra de Ouro do Threading no Lazarus

> **NUNCA acesse componentes visuais (LCL) diretamente de uma thread secundária.**
> Use `TThread.Synchronize` ou `TThread.Queue` para atualizar a UI.

## Incompatibilidades FPC vs Delphi

> **IMPORTANTE:** As seguintes primitivas do Delphi **NÃO existem** no FreePascal:
> - `TTask`, `TTask.Run` (PPL)
> - `TParallel.For` (PPL)
> - `IFuture<T>`, `TFuture<T>` (PPL)
> - `TInterlocked` (classe estática)
> - `TMonitor` (lock nativo de objeto)
> - `TThreadedQueue<T>` (fila genérica thread-safe)
> - `TThread.CreateAnonymousThread` (anonymous methods em threads)
> - `TThread.Current.CheckTerminated`
> - `TThread.NameThreadForDebugging`
>
> Use exclusivamente `TThread`, `TCriticalSection`, `TEvent`, `TThreadList`,
> `TMultiReadExclusiveWriteSynchronizer` e funções atômicas nativas
> (`InterlockedIncrement`, `InterlockedDecrement`, `InterlockedExchange`).

## Abordagens Disponíveis no FPC

| Abordagem | Quando Usar | Complexidade |
|-----------|-------------|--------------|
| `TThread` (herança) | Controle total, workers permanentes | Média |
| `TThread.Synchronize` | Atualizar UI (bloqueante) | Baixa |
| `TThread.Queue` | Atualizar UI (não-bloqueante, PREFERIR) | Baixa |
| `TCriticalSection` | Seção de exclusão mútua (Enter/Leave) | Baixa |
| `TThreadList` | Lista thread-safe com LockList/UnlockList | Baixa |
| `TEvent` | Sinalização entre threads (WaitFor/SetEvent) | Média |
| `TMultiReadExclusiveWriteSynchronizer` | Cache: muitas leituras, poucas escritas | Média |

## TThread — Padrão Principal no FPC

### Thread com Herança (Recomendado para Workers)

```pascal
uses
  Classes, SysUtils;

type
  /// <summary>
  ///   Worker thread para processamento em background.
  ///   Demonstra herança de TThread com cancelamento via Terminated.
  /// </summary>
  TDataProcessorThread = class(TThread)
  private
    FProgressCurrent: Integer;
    FProgressTotal: Integer;
    FErrorMsg: string;
    procedure DoUpdateProgress;
    procedure DoShowError;
  protected
    procedure Execute; override;
  public
    constructor Create;
  end;

constructor TDataProcessorThread.Create;
begin
  inherited Create(True);   // Criar suspensa
  FreeOnTerminate := True;  // Auto-libera ao terminar
end;

procedure TDataProcessorThread.Execute;
var
  I: Integer;
begin
  FProgressTotal := 100;
  try
    for I := 0 to FProgressTotal - 1 do
    begin
      { Verificar cancelamento em cada iteração }
      if Terminated then
        Exit;

      { Processar item }
      ProcessItem(I);
      FProgressCurrent := I + 1;

      { Atualizar UI via Queue (não-bloqueante) }
      Queue(@DoUpdateProgress);
    end;
  except
    on E: Exception do
    begin
      FErrorMsg := E.Message;
      Queue(@DoShowError);
    end;
  end;
end;

procedure TDataProcessorThread.DoUpdateProgress;
begin
  // Acessa LCL de forma segura aqui (roda na main thread)
  frmMain.pbrProgress.Max := FProgressTotal;
  frmMain.pbrProgress.Position := FProgressCurrent;
end;

procedure TDataProcessorThread.DoShowError;
begin
  ShowMessage('Erro: ' + FErrorMsg);
end;
```

### Uso da Thread Dedicada

```pascal
procedure TfrmMain.btnProcessClick(Sender: TObject);
var
  LThread: TDataProcessorThread;
begin
  LThread := TDataProcessorThread.Create;
  LThread.Start;
end;

procedure TfrmMain.btnCancelClick(Sender: TObject);
begin
  { Solicitar cancelamento gracioso }
  if Assigned(FCurrentThread) then
    FCurrentThread.Terminate;
end;
```

## Synchronize vs Queue

| Método | Comportamento | Quando Usar |
|--------|--------------|-------------|
| `TThread.Synchronize` | **Bloqueante** — espera a main thread processar | Quando precisa do resultado da UI |
| `TThread.Queue` | **Não-bloqueante** — enfileira e continua | Progresso, logs, atualizações visuais |

```pascal
{ Synchronize: BLOQUEIA a thread até a main thread processar }
Synchronize(@DoUpdateUI);
// A thread só continua AQUI depois que a main thread executou

{ Queue: NÃO BLOQUEIA — enfileira e continua imediatamente }
Queue(@DoUpdateUI);
// A thread continua IMEDIATAMENTE sem esperar
```

> **Recomendação:** Prefira `Queue` sempre que possível. Use `Synchronize` apenas quando precisar de um resultado da UI de volta na thread.

## Thread-Safety — Proteção de Recursos

### TCriticalSection (unit `syncobjs`)

```pascal
uses
  syncobjs;

type
  TThreadSafeCounter = class
  private
    FCount: Integer;
    FLock: TCriticalSection;
  public
    constructor Create;
    destructor Destroy; override;
    procedure Increment;
    function GetValue: Integer;
  end;

constructor TThreadSafeCounter.Create;
begin
  inherited;
  FLock := TCriticalSection.Create;
  FCount := 0;
end;

destructor TThreadSafeCounter.Destroy;
begin
  FLock.Free;
  inherited;
end;

procedure TThreadSafeCounter.Increment;
begin
  FLock.Enter;
  try
    Inc(FCount);
  finally
    FLock.Leave;  // SEMPRE no finally!
  end;
end;

function TThreadSafeCounter.GetValue: Integer;
begin
  FLock.Enter;
  try
    Result := FCount;
  finally
    FLock.Leave;
  end;
end;
```

### Operações Atômicas Nativas do FPC

```pascal
{ InterlockedIncrement — operação atômica nativa }
InterlockedIncrement(FProcessedCount);
InterlockedDecrement(FPendingCount);

{ InterlockedExchange — troca atômica }
InterlockedExchange(FOldValue, LNewValue);

{ InterlockedCompareExchange — compare-and-swap }
InterlockedCompareExchange(FTarget, LNewVal, LExpectedVal);
```

> **Nota:** No FPC são funções livres (`InterlockedIncrement`), não métodos de classe (`TInterlocked.Increment`) como no Delphi.

### TThreadList (Lista Thread-Safe)

```pascal
var
  FSharedList: TThreadList;

{ Thread A: adicionar }
LList := FSharedList.LockList;
try
  LList.Add(LItem);
finally
  FSharedList.UnlockList;
end;

{ Thread B: ler }
LList := FSharedList.LockList;
try
  for I := 0 to LList.Count - 1 do
    ProcessItem(LList[I]);
finally
  FSharedList.UnlockList;
end;
```

### TMultiReadExclusiveWriteSynchronizer (MREWS)

```pascal
type
  TThreadSafeCache = class
  private
    FData: TStringList;
    FLock: TMultiReadExclusiveWriteSynchronizer;
  public
    constructor Create;
    destructor Destroy; override;
    function TryGet(const AKey: string; out AValue: string): Boolean;
    procedure Put(const AKey, AValue: string);
  end;

function TThreadSafeCache.TryGet(const AKey: string; out AValue: string): Boolean;
var
  LIdx: Integer;
begin
  FLock.BeginRead;  // Múltiplas threads podem ler simultaneamente
  try
    LIdx := FData.IndexOfName(AKey);
    Result := LIdx >= 0;
    if Result then
      AValue := FData.ValueFromIndex[LIdx];
  finally
    FLock.EndRead;
  end;
end;

procedure TThreadSafeCache.Put(const AKey, AValue: string);
begin
  FLock.BeginWrite;  // Apenas uma thread pode escrever por vez
  try
    FData.Values[AKey] := AValue;
  finally
    FLock.EndWrite;
  end;
end;
```

## Eventos e Sinalização

### TEvent

```pascal
uses
  syncobjs;

var
  FStopEvent: TEvent;

{ Criar }
FStopEvent := TEvent.Create(nil, True, False, ''); // Manual reset, initially unsignaled

{ Thread: esperar sinal }
procedure TWorkerThread.Execute;
begin
  while not Terminated do
  begin
    { Esperar até 500ms por sinal de parada }
    if FStopEvent.WaitFor(500) = wrSignaled then
      Break;

    { Fazer trabalho }
    DoWork;
  end;
end;

{ Main thread: sinalizar parada }
FStopEvent.SetEvent;
```

## Padrão Producer-Consumer (sem TThreadedQueue)

No FPC não existe `TThreadedQueue<T>`. Implementamos com `TThreadList` + `TEvent`:

```pascal
type
  TSimpleWorkQueue = class
  private
    FList: TThreadList;
    FNewItemEvent: TEvent;
  public
    constructor Create;
    destructor Destroy; override;
    procedure Push(AItem: Pointer);
    function Pop(ATimeoutMs: Cardinal): Pointer;
  end;

constructor TSimpleWorkQueue.Create;
begin
  inherited;
  FList := TThreadList.Create;
  FNewItemEvent := TEvent.Create(nil, False, False, '');
end;

destructor TSimpleWorkQueue.Destroy;
begin
  FNewItemEvent.Free;
  FList.Free;
  inherited;
end;

procedure TSimpleWorkQueue.Push(AItem: Pointer);
var
  LList: TList;
begin
  LList := FList.LockList;
  try
    LList.Add(AItem);
  finally
    FList.UnlockList;
  end;
  FNewItemEvent.SetEvent; // Sinalizar que há item disponível
end;

function TSimpleWorkQueue.Pop(ATimeoutMs: Cardinal): Pointer;
var
  LList: TList;
begin
  Result := nil;
  if FNewItemEvent.WaitFor(ATimeoutMs) = wrSignaled then
  begin
    LList := FList.LockList;
    try
      if LList.Count > 0 then
      begin
        Result := LList[0];
        LList.Delete(0);
      end;
    finally
      FList.UnlockList;
    end;
  end;
end;
```

## Padrão: Background Worker com Callback

```pascal
type
  /// <summary>
  ///   Background worker genérico que executa trabalho pesado
  ///   e notifica a main thread via métodos sincronizados.
  /// </summary>
  TBackgroundWorkerThread = class(TThread)
  private
    FResult: string;
    FError: string;
    FOnSuccess: TNotifyEvent;
    FOnError: TNotifyEvent;
    procedure DoSuccess;
    procedure DoError;
  protected
    procedure Execute; override;
    function DoWork: string; virtual; abstract;
  public
    property OnSuccess: TNotifyEvent read FOnSuccess write FOnSuccess;
    property OnError: TNotifyEvent read FOnError write FOnError;
    property ResultValue: string read FResult;
    property ErrorMessage: string read FError;
  end;

procedure TBackgroundWorkerThread.Execute;
begin
  try
    FResult := DoWork;
    if Assigned(FOnSuccess) then
      Queue(@DoSuccess);
  except
    on E: Exception do
    begin
      FError := E.Message;
      if Assigned(FOnError) then
        Queue(@DoError);
    end;
  end;
end;

procedure TBackgroundWorkerThread.DoSuccess;
begin
  if Assigned(FOnSuccess) then
    FOnSuccess(Self);
end;

procedure TBackgroundWorkerThread.DoError;
begin
  if Assigned(FOnError) then
    FOnError(Self);
end;
```

### Padrão: Timer Thread (Execução Periódica)

```pascal
type
  TTimerThread = class(TThread)
  private
    FInterval: Cardinal;
    procedure DoTimerTick;
  protected
    procedure Execute; override;
    procedure OnTick; virtual; abstract;
  public
    constructor Create(AIntervalMs: Cardinal);
  end;

constructor TTimerThread.Create(AIntervalMs: Cardinal);
begin
  inherited Create(True);
  FreeOnTerminate := False;
  FInterval := AIntervalMs;
end;

procedure TTimerThread.Execute;
begin
  while not Terminated do
  begin
    Sleep(FInterval);
    if not Terminated then
      Synchronize(@DoTimerTick);
  end;
end;

procedure TTimerThread.DoTimerTick;
begin
  OnTick;
end;
```

## Anti-Patterns a Evitar

```pascal
// ❌ NUNCA acessar UI diretamente de thread secundária
procedure TMyThread.Execute;
begin
  lblStatus.Caption := 'Processando...';  // CRASH ou comportamento imprevisível!
end;

// ✅ SEMPRE usar Synchronize/Queue para UI
procedure TMyThread.Execute;
begin
  Queue(@DoUpdateLabel);  // Seguro!
end;

// ❌ NUNCA criar thread com FreeOnTerminate=True e manter referência
FMyThread := TMyThread.Create(True);
FMyThread.FreeOnTerminate := True;
FMyThread.Start;
FMyThread.WaitFor;  // CRASH! O objeto pode já ter sido liberado!

// ✅ Se precisa de WaitFor, NÃO use FreeOnTerminate
FMyThread := TMyThread.Create(True);
FMyThread.FreeOnTerminate := False;
FMyThread.Start;
FMyThread.WaitFor;
FMyThread.Free;

// ❌ NUNCA acessar variáveis compartilhadas sem proteção
Inc(FSharedCounter);  // Race condition!

// ✅ SEMPRE proteger acesso compartilhado
InterlockedIncrement(FSharedCounter);  // Atômico!
// ou
FLock.Enter;
try
  Inc(FSharedCounter);
finally
  FLock.Leave;
end;

// ❌ NUNCA usar Sleep() na main thread
Sleep(5000);  // Congela a UI por 5 segundos!

// ❌ NUNCA usar TTask.Run, TParallel.For ou IFuture no FPC
// Essas primitivas NÃO EXISTEM no FreePascal!

// ✅ Mover trabalho pesado para TThread
LThread := TMyWorkerThread.Create;
LThread.Start;
```

## Checklist de Threading

- [ ] Operações pesadas estão em threads secundárias (não na main thread)?
- [ ] Toda atualização de UI usa `Synchronize` ou `Queue`?
- [ ] Variáveis compartilhadas protegidas com locks (`TCriticalSection` ou `InterlockedIncrement`)?
- [ ] `FreeOnTerminate` configurado corretamente (True para fire-and-forget, False se precisa WaitFor)?
- [ ] Threads verificam `Terminated` em loops para cancelamento gracioso?
- [ ] Exceções tratadas dentro das threads (não propagam silenciosamente)?
- [ ] `TCriticalSection.Leave` sempre no `finally`?
- [ ] Sem `Sleep()` na main thread?
- [ ] Sem deadlocks (locks aninhados na mesma ordem)?
- [ ] Sem uso de primitivas PPL do Delphi (`TTask`, `TParallel`, `TInterlocked`, `TMonitor`)?
