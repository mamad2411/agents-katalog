# React面试题集

‌&emsp;&emsp;React 是一个用于构建用户界面的 JavaScript 库，由 Facebook 开发并开源。它采用组件化开发模式，通过虚拟 DOM 和高效的 Diff 算法实现高性能的页面渲染。

---

## 📚 React学习路线大纲

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          🚀 React学习路线总览                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  【第一阶段：基础入门】                                                          │
│  ├── 1. React基础概念（什么是React、JSX、组件化）                               │
│  ├── 2. State与Props（状态管理基础）                                             │
│  ├── 3. 事件处理与条件渲染                                                       │
│  ├── 4. 列表渲染与Key                                                           │
│  └── 5. 组件通讯（父子、兄弟、跨级）                                             │
│                                                                                 │
│  【第二阶段：核心进阶】                                                          │
│  ├── 6. Hooks完全指南（useState、useEffect、useContext）                         │
│  ├── 7. useRef详细用法                                                          │
│  ├── 8. useMemo与useCallback（性能优化）                                         │
│  ├── 9. useReducer（复杂状态管理）                                               │
│  ├── 10. 组件生命周期（类组件）                                                  │
│  └── 11. PureComponent与React.memo                                              │
│                                                                                 │
│  【第三阶段：高级特性】                                                          │
│  ├── 12. 高阶组件（HOC）                                                        │
│  ├── 13. Render Props                                                           │
│  ├── 14. 错误边界                                                               │
│  ├── 15. React中的表单处理                                                       │
│  └── 16. React中的DOM操作                                                       │
│                                                                                 │
│  【第四阶段：生态工具】                                                          │
│  ├── 17. Redux状态管理                                                          │
│  ├── 18. Redux Toolkit（RTK）                                                  │
│  ├── 19. React Router路由                                                       │
│  ├── 20. TypeScript与React                                                      │
│  └── 21. CSS解决方案（CSS Modules、Styled Components、Tailwind）                 │
│                                                                                 │
│  【第五阶段：原理深度】                                                          │
│  ├── 22. 虚拟DOM工作原理                                                        │
│  ├── 23. Diff算法详解                                                           │
│  ├── 24. Fiber架构                                                              │
│  ├── 25. React调度系统                                                          │
│  └── 26. 更新机制与批处理                                                       │
│                                                                                 │
│  【第六阶段：自定义Hooks】                                                       │
│  ├── 27. 自定义Hooks基础                                                        │
│  ├── 28. 常用自定义Hooks（useLocalStorage、useDebounce、useFetch等）            │
│  └── 29. 进阶自定义Hooks（useAsync、usePrevious）                                │
│                                                                                 │
│  【第七阶段：React 18新特性】                                                    │
│  ├── 30. 并发渲染                                                               │
│  ├── 31. startTransition与useDeferredValue                                      │
│  ├── 32. React Server Components                                               │
│  └── 33. Suspense增强                                                          │
│                                                                                 │
│  【第八阶段：实战与优化】                                                        │
│  ├── 34. 性能优化深入策略                                                        │
│  ├── 35. 列表虚拟化                                                             │
│  ├── 36. 状态管理优化                                                           │
│  └── 37. 代码分割与懒加载                                                        │
│                                                                                 │
│  【第九阶段：面试冲刺】                                                          │
│  └── 38. 高频面试题深度解答                                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 基础概念篇

## 1、React是什么？有什么特点？

&emsp;&emsp;**定义**
&emsp;&emsp;React 是一个用于构建用户界面的 JavaScript 库，主要用于构建单页面应用（SPA）。它专注于视图层的开发，通过组件化的方式构建复杂的 UI 界面。

&emsp;&emsp;**核心特点**

&emsp;&emsp;**（1）组件化**
```jsx
// 函数组件
function Welcome(props) {
    return <h1>你好，{props.name}</h1>;
}

// 类组件
class Welcome extends React.Component {
    render() {
        return <h1>你好，{this.props.name}</h1>;
    }
}

// 使用组件
const element = <Welcome name="张三" />;
```

&emsp;&emsp;**（2）虚拟DOM**
&emsp;&emsp;React 在内存中维护一个虚拟 DOM 树，当状态变化时，先更新虚拟 DOM，再通过 Diff 算法计算出最小更新方案，最后批量更新真实 DOM。这种机制大大减少了直接操作 DOM 带来的性能开销。

&emsp;&emsp;**（3）单向数据流**
&emsp;&emsp;React 遵循单向数据流原则，数据从父组件流向子组件，通过 props 传递，子组件不能直接修改父组件传来的 props。

```jsx
// 单向数据流示例
function Parent() {
    const [count, setCount] = useState(0);
    
    return (
        <div>
            <p>计数器：{count}</p>
            <Child count={count} onIncrement={() => setCount(count + 1)} />
        </div>
    );
}

function Child({ count, onIncrement }) {
    return (
        <div>
            <p>子组件接收到的值：{count}</p>
            <button onClick={onIncrement}>增加</button>
        </div>
    );
}
```

&emsp;&emsp;**（4）JSX语法**
&emsp;&emsp;JSX 是 JavaScript 的语法扩展，允许在 JavaScript 中编写类似 HTML 的代码。

```jsx
// JSX 示例
const element = (
    <div className="container">
        <h1>欢迎来到React世界</h1>
        <p>学习 React 真有趣！</p>
    </div>
);

// 表达式嵌入
const name = '小明';
const greeting = <p>你好，{name}！今天是{new Date().toLocaleDateString()}</p>;

// 条件渲染
const isLoggedIn = true;
const welcome = (
    <div>
        {isLoggedIn ? <h1>欢迎回来</h1> : <h1>请登录</h1>}
    </div>
);
```

---

## 2、React元素与JSX

&emsp;&emsp;**（1）JSX语法规则**
```jsx
// 1. 标签必须闭合
const element1 = <input type="text" />;
const element2 = <div>内容</div>;

// 2. className 替代 class
const element = <div className="box">盒子</div>;

// 3. style 需要是对象
const styleObj = {
    color: 'red',
    fontSize: '16px'
};
const element = <div style={styleObj}>样式</div>;

// 4. 组件首字母大写
function MyComponent() {
    return <div>我的组件</div>;
}
const element = <MyComponent />;

// 5. 注释需要用花括号包裹
const element = (
    <div>
        {/* 这是一个注释 */}
        <h1>标题</h1>
    </div>
);
```

&emsp;&emsp;**（2）React.createElement**
&emsp;&emsp;JSX 会被 Babel 编译成 React.createElement 调用：

```jsx
// JSX写法
const element = <h1 className="greeting">Hello, world!</h1>;

// 编译后
const element = React.createElement(
    'h1',
    { className: 'greeting' },
    'Hello, world!'
);

// createElement返回的对象结构
{
    type: 'h1',
    props: {
        className: 'greeting',
        children: 'Hello, world!'
    }
}
```

---

## 3、State与Props的区别

&emsp;&emsp;**（1）Props（属性）**
&emsp;&emsp;Props 是组件对外的接口，用于父组件向子组件传递数据。

```jsx
// Props只读，不能在子组件中修改
function Student(props) {
    return (
        <div>
            <p>姓名：{props.name}</p>
            <p>年龄：{props.age}</p>
            <p>学校：{props.school}</p>
        </div>
    );
}

// 使用时传入props
<Student name="张三" age={20} school="清华大学" />
```

&emsp;&emsp;**（2）State（状态）**
&emsp;&emsp;State 是组件内部的状态，用于组件内部数据的管理和更新。

```jsx
// State可以在组件内部修改，修改后会触发重新渲染
class Counter extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            count: 0
        };
    }

    increment = () => {
        this.setState({ count: this.state.count + 1 });
    }

    render() {
        return (
            <div>
                <p>计数：{this.state.count}</p>
                <button onClick={this.increment}>增加</button>
            </div>
        );
    }
}
```

&emsp;&emsp;**（3）Props与State对比**
```
+----------+----------------------------------+------------------------------+
|  特性    |            Props                |          State              |
+----------+----------------------------------+------------------------------+
|  用途    |  父组件向子组件传递数据          |  组件内部管理数据           |
|  可变性  |  只读，不能在子组件中修改         |  可通过setState修改         |
|  触发    |  父组件重新渲染时变化            |  setState调用时变化         |
|  初始化  |  组件调用时传入                  |  constructor中初始化        |
+----------+----------------------------------+------------------------------+
```

---

## 4、函数组件与类组件的区别

&emsp;&emsp;**（1）基本写法对比**
```jsx
// 函数组件（无状态组件）
function Button(props) {
    return <button>{props.text}</button>;
}

// 类组件（有状态组件）
class Button extends React.Component {
    render() {
        return <button>{this.props.text}</button>;
    }
}
```

&emsp;&emsp;**（2）核心区别**

| 特性 | 函数组件 | 类组件 |
|------|----------|--------|
| 是否有this | 没有 | 有（指向组件实例） |
| 是否有state | Hook之前没有，现在可以通过useState | 有 |
| 是否有生命周期 | Hook之前没有，现在可以通过useEffect | 有 |
| 是否有生命周期方法 | 无 | 有（componentDidMount等） |
| 性能 | 相对更轻量 | 需要实例化，稍微重一些 |

&emsp;&emsp;**（3）生命周期差异**
```jsx
// 函数组件使用Hooks
function UserComponent() {
    const [user, setUser] = useState(null);

    // 相当于 componentDidMount + componentDidUpdate
    useEffect(() => {
        fetchUser().then(setUser);
    }, []); // 空数组表示只执行一次

    return <div>{user?.name}</div>;
}

// 类组件使用生命周期方法
class UserComponent extends React.Component {
    state = { user: null };

    componentDidMount() {
        fetchUser().then(user => this.setState({ user }));
    }

    render() {
        return <div>{this.state.user?.name}</div>;
    }
}
```

---

## 5、事件处理

&emsp;&emsp;**（1）基本事件绑定**
```jsx
// 函数组件
function EventButton() {
    function handleClick() {
        console.log('按钮被点击');
    }

    return <button onClick={handleClick}>点击我</button>;
}

// 类组件
class EventButton extends React.Component {
    handleClick() {
        console.log('按钮被点击');
    }

    render() {
        return <button onClick={this.handleClick.bind(this)}>点击我</button>;
    }
}
```

&emsp;&emsp;**（2）事件对象与参数传递**
```jsx
function EventDemo() {
    // 方式1：箭头函数包裹
    const handleClick = (event) => {
        console.log('事件对象:', event);
        console.log('目标元素:', event.target);
    };

    // 方式2：闭包传递参数
    const handleDelete = (id) => {
        console.log('删除ID:', id);
    };

    return (
        <div>
            <button onClick={handleClick}>查看事件对象</button>
            <button onClick={() => handleDelete(1)}>删除</button>
            <button onClick={(e) => handleDelete(2, e)}>删除2</button>
        </div>
    );
}
```

&emsp;&emsp;**（3）常见事件类型**
```jsx
function EventsDemo() {
    const handleChange = (e) => {
        console.log('输入值:', e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault(); // 阻止默认行为
        console.log('表单提交');
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            console.log('按下了回车键');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                onChange={handleChange}
                onKeyDown={handleKeyDown}
            />
            <button type="submit">提交</button>
        </form>
    );
}
```

---

## 6、条件渲染

&emsp;&emsp;**（1）if语句方式**
```jsx
function UserGreeting(props) {
    return <h1>欢迎回来！</h1>;
}

function GuestGreeting(props) {
    return <h1>请先登录。</h1>;
}

function Greeting(props) {
    if (props.isLoggedIn) {
        return <UserGreeting />;
    }
    return <GuestGreeting />;
}
```

&emsp;&emsp;**（2）三元运算符**
```jsx
function LoginControl() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    return (
        <div>
            {isLoggedIn ? (
                <button onClick={() => setIsLoggedIn(false)}>登出</button>
            ) : (
                <button onClick={() => setIsLoggedIn(true)}>登录</button>
            )}
        </div>
    );
}
```

&emsp;&emsp;**（3）逻辑与运算符 &&**
```jsx
function Mailbox(props) {
    const unreadMessages = props.messages;

    return (
        <div>
            <h1>收件箱</h1>
            {unreadMessages.length > 0 && (
                <h2>您有 {unreadMessages.length} 条未读消息。</h2>
            )}
        </div>
    );
}
```

&emsp;&emsp;**（4）阻止组件渲染**
```jsx
function WarningBanner(props) {
    // 如果warn为false，组件不渲染任何内容
    if (!props.warn) {
        return null;
    }

    return (
        <div className="warning">
            警告！
        </div>
    );
}
```

---

## 7、列表渲染与Key

&emsp;&emsp;**（1）基本列表渲染**
```jsx
function NumberList(props) {
    const numbers = props.numbers;

    // 必须为每个列表元素添加key
    const listItems = numbers.map((number) => (
        <li key={number.toString()}>{number}</li>
    ));

    return <ul>{listItems}</ul>;
}

// 或者直接在JSX中渲染
function NumberList(props) {
    const numbers = props.numbers;

    return (
        <ul>
            {numbers.map((number) => (
                <li key={number.toString()}>{number}</li>
            ))}
        </ul>
    );
}
```

&emsp;&emsp;**（2）Key的作用与最佳实践**
```jsx
// 好的key使用：使用唯一ID
const todoItems = todos.map((todo) => (
    <li key={todo.id}>
        {todo.text}
    </li>
));

// 避免使用索引作为key（当列表顺序可能变化时）
// 不好：如果列表顺序改变，索引会变化
const todoItems = todos.map((todo, index) => (
    <li key={index}>{todo.text}</li>
));

// 好的：使用稳定的唯一标识
const todoItems = todos.map((todo) => (
    <li key={todo.id}>{todo.text}</li>
));
```

&emsp;&emsp;**（3）渲染复杂列表**
```jsx
function ProductList(props) {
    const { products } = props;

    return (
        <div className="product-list">
            {products.map(product => (
                <div key={product.id} className="product-card">
                    <img src={product.image} alt={product.name} />
                    <h3>{product.name}</h3>
                    <p>价格：¥{product.price}</p>
                    <button>加入购物车</button>
                </div>
            ))}
        </div>
    );
}
```

---

## 8、组件通讯

&emsp;&emsp;**（1）父子组件通讯**
```jsx
// 父组件 -> 子组件：通过props
function Parent() {
    const [message, setMessage] = useState('来自父组件的消息');

    return <Child message={message} onMessageChange={setMessage} />;
}

// 子组件 -> 父组件：通过回调函数props
function Child({ message, onMessageChange }) {
    return (
        <div>
            <p>收到：{message}</p>
            <button onClick={() => onMessageChange('来自子组件的消息')}>
                回复
            </button>
        </div>
    );
}
```

&emsp;&emsp;**（2）跨级组件通讯：Context**
```jsx
// 创建Context
const ThemeContext = React.createContext('light');

// Provider（提供者）
function App() {
    const [theme, setTheme] = useState('dark');

    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            <Toolbar />
        </ThemeContext.Provider>
    );
}

// 消费Context（方式1：Consumer）
function ThemedButton() {
    return (
        <ThemeContext.Consumer>
            {(value) => (
                <button style={{ background: value.theme === 'dark' ? '#333' : '#fff' }}>
                    按钮
                </button>
            )}
        </ThemeContext.Consumer>
    );
}

// 消费Context（方式2：useContext Hook）
function ThemedButton() {
    const { theme } = useContext(ThemeContext);

    return (
        <button style={{ background: theme === 'dark' ? '#333' : '#fff' }}>
            按钮
        </button>
    );
}
```

&emsp;&emsp;**（3）兄弟组件通讯**
```jsx
// 方案1：提升状态到父组件
function Parent() {
    const [sharedData, setSharedData] = useState('初始数据');

    return (
        <>
            <SiblingA data={sharedData} />
            <SiblingB onDataChange={setSharedData} />
        </>
    );
}

// 方案2：使用事件总线/状态管理库
// 使用EventEmitter或第三方库如pubsub-js
```

---

## 中级进阶篇

---

## 中级进阶篇（Hooks深入）

## 9、Hooks完全指南

&emsp;&emsp;**Hooks是React 16.8引入的新特性，允许在函数组件中使用state和其他React特性。**

&emsp;&emsp;**（1）useState - 状态管理**
```jsx
// 基本用法
function Counter() {
    const [count, setCount] = useState(0);

    return (
        <div>
            <p>计数：{count}</p>
            <button onClick={() => setCount(count + 1)}>增加</button>
            <button onClick={() => setCount(count - 1)}>减少</button>
            <button onClick={() => setCount(0)}>重置</button>
        </div>
    );
}

// 函数式更新（当新状态依赖旧状态时）
function Counter() {
    const [count, setCount] = useState(0);

    // 推荐：使用函数式更新，避免依赖外部状态
    const increment = () => {
        setCount(prevCount => prevCount + 1);
    };

    return <button onClick={increment}>计数：{count}</button>;
}

// 多个状态
function UserForm() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [age, setAge] = useState(0);

    return (
        <form>
            <input value={name} onChange={e => setName(e.target.value)} />
            <input value={email} onChange={e => setEmail(e.target.value)} />
            <input value={age} onChange={e => setAge(Number(e.target.value))} />
        </form>
    );
}
```

&emsp;&emsp;**（2）useEffect - 副作用处理**
```jsx
// 基本用法：组件渲染后执行
function UserStatus() {
    const [isOnline, setIsOnline] = useState(null);

    useEffect(() => {
        // 组件挂载后执行
        const timer = setInterval(() => {
            setIsOnline(Math.random() > 0.5);
        }, 1000);

        // 返回清理函数：组件卸载时执行
        return () => {
            clearInterval(timer);
        };
    }, []); // 空依赖数组：只在挂载时执行一次

    return <div>{isOnline ? '在线' : '离线'}</div>;
}

// 依赖项用法
function User({ userId }) {
    const [user, setUser] = useState(null);

    useEffect(() => {
        fetchUser(userId).then(setUser);
    }, [userId]); // userId变化时重新执行

    return <div>{user?.name}</div>;
}

// 条件执行effect
function SearchResults({ query }) {
    const [results, setResults] = useState([]);

    useEffect(() => {
        if (query) {
            searchAPI(query).then(setResults);
        }
    }, [query]);

    return <ul>{results.map(r => <li key={r.id}>{r.text}</li>)}</ul>;
}
```

&emsp;&emsp;**（3）useContext - 上下文访问**
```jsx
// 定义主题Context
const ThemeContext = createContext({
    theme: 'light',
    toggleTheme: () => {}
});

// 在组件中使用
function Header() {
    const { theme, toggleTheme } = useContext(ThemeContext);

    return (
        <header style={{ background: theme === 'dark' ? '#333' : '#fff' }}>
            <button onClick={toggleTheme}>切换主题</button>
        </header>
    );
}
```

---

## 10、useRef详细用法

&emsp;&emsp;**（1）访问DOM元素**
```jsx
function TextInput() {
    const inputRef = useRef(null);

    const focusInput = () => {
        // 聚焦输入框
        inputRef.current.focus();
    };

    return (
        <div>
            <input ref={inputRef} type="text" />
            <button onClick={focusInput}>聚焦</button>
        </div>
    );
}

// 获取DOM属性
function ImageLoader() {
    const imgRef = useRef(null);

    useEffect(() => {
        console.log('图片尺寸:', imgRef.current.width, imgRef.current.height);
    }, []);

    return <img ref={imgRef} src="/image.jpg" alt="测试" />;
}
```

&emsp;&emsp;**（2）保存可变值（不触发重新渲染）**
```jsx
function Timer() {
    const [count, setCount] = useState(0);
    const intervalRef = useRef(null);

    useEffect(() => {
        // 保存定时器ID，不触发重新渲染
        intervalRef.current = setInterval(() => {
            setCount(c => c + 1);
        }, 1000);

        return () => clearInterval(intervalRef.current);
    }, []);

    return <div>计数：{count}</div>;
}
```

&emsp;&emsp;**（3）previous value实现**
```jsx
function Counter() {
    const [count, setCount] = useState(0);
    const prevCountRef = useRef();

    useEffect(() => {
        // 保存上一次的count值
        prevCountRef.current = count;
    });

    return (
        <div>
            <p>当前：{count}，上次：{prevCountRef.current}</p>
            <button onClick={() => setCount(c => c + 1)}>增加</button>
        </div>
    );
}
```

---

## 11、useMemo与useCallback

&emsp;&emsp;**（1）useMemo - 缓存计算结果**
```jsx
// 避免不必要的重复计算
function ExpensiveList({ items, filter }) {
    // 只有items或filter变化时才重新计算
    const filteredItems = useMemo(() => {
        console.log('执行过滤计算...');
        return items.filter(item => item.name.includes(filter));
    }, [items, filter]);

    return <ul>{filteredItems.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}

// 性能优化示例
function DataTable({ data, sortKey }) {
    // 缓存排序后的数据
    const sortedData = useMemo(() => {
        return [...data].sort((a, b) => {
            return a[sortKey] > b[sortKey] ? 1 : -1;
        });
    }, [data, sortKey]);

    return <Table data={sortedData} />;
}
```

&emsp;&emsp;**（2）useCallback - 缓存回调函数**
```jsx
// 避免子组件不必要的重新渲染
function Parent() {
    const [count, setCount] = useState(0);
    const [name, setName] = useState('张三');

    // 每次渲染都创建新函数
    const handleClick = () => {
        console.log('点击');
    };

    // 只有count变化时才创建新函数
    const handleIncrement = useCallback(() => {
        setCount(count + 1);
    }, [count]);

    // 使用函数式更新，无需依赖count
    const handleIncrementFixed = useCallback(() => {
        setCount(c => c + 1);
    }, []); // 空依赖，函数引用保持稳定

    return (
        <div>
            <p>{count}</p>
            <Child onClick={handleClick} />
            <Counter onIncrement={handleIncrement} />
        </div>
    );
}
```

---

## 12、useReducer - 复杂状态管理

&emsp;&emsp;**（1）基本用法**
```jsx
// 定义reducer函数
function reducer(state, action) {
    switch (action.type) {
        case 'INCREMENT':
            return { count: state.count + 1 };
        case 'DECREMENT':
            return { count: state.count - 1 };
        case 'RESET':
            return { count: 0 };
        default:
            return state;
    }
}

function Counter() {
    const [state, dispatch] = useReducer(reducer, { count: 0 });

    return (
        <div>
            <p>计数：{state.count}</p>
            <button onClick={() => dispatch({ type: 'INCREMENT' })}>+1</button>
            <button onClick={() => dispatch({ type: 'DECREMENT' })}>-1</button>
            <button onClick={() => dispatch({ type: 'RESET' })}>重置</button>
        </div>
    );
}
```

&emsp;&emsp;**（2）复杂状态示例：TODO列表**
```jsx
const initialState = { todos: [] };

function todoReducer(state, action) {
    switch (action.type) {
        case 'ADD_TODO':
            return {
                todos: [
                    ...state.todos,
                    { id: Date.now(), text: action.text, completed: false }
                ]
            };
        case 'TOGGLE_TODO':
            return {
                todos: state.todos.map(todo =>
                    todo.id === action.id
                        ? { ...todo, completed: !todo.completed }
                        : todo
                )
            };
        case 'DELETE_TODO':
            return {
                todos: state.todos.filter(todo => todo.id !== action.id)
            };
        default:
            return state;
    }
}

function TodoApp() {
    const [state, dispatch] = useReducer(todoReducer, initialState);
    const [input, setInput] = useState('');

    const addTodo = () => {
        if (input.trim()) {
            dispatch({ type: 'ADD_TODO', text: input });
            setInput('');
        }
    };

    return (
        <div>
            <input value={input} onChange={e => setInput(e.target.value)} />
            <button onClick={addTodo}>添加</button>
            <ul>
                {state.todos.map(todo => (
                    <li key={todo.id}>
                        <span
                            style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}
                            onClick={() => dispatch({ type: 'TOGGLE_TODO', id: todo.id })}
                        >
                            {todo.text}
                        </span>
                        <button onClick={() => dispatch({ type: 'DELETE_TODO', id: todo.id })}>
                            删除
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}
```

---

## 13、React生命周期

&emsp;&emsp;**类组件生命周期**

&emsp;&emsp;**（1）挂载阶段**
```
constructor() -> static getDerivedStateFromProps() -> render() -> componentDidMount()
```
```jsx
class UserComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = { user: null };
        console.log('1. 构造函数');
    }

    static getDerivedStateFromProps(props, state) {
        // 从props派生state时使用
        return null;
    }

    componentDidMount() {
        console.log('3. 组件挂载完成');
        // 适合：请求数据、添加订阅、操作DOM
        fetch('/api/user')
            .then(res => res.json())
            .then(user => this.setState({ user }));
    }

    render() {
        console.log('2. 渲染');
        return <div>用户信息：{this.state.user?.name}</div>;
    }
}
```

&emsp;&emsp;**（2）更新阶段**
```
props变化 -> static getDerivedStateFromProps() -> shouldComponentUpdate() -> render() -> getSnapshotBeforeUpdate() -> componentDidUpdate()
state变化 -> shouldComponentUpdate() -> render() -> getSnapshotBeforeUpdate() -> componentDidUpdate()
```
```jsx
class Counter extends React.Component {
    state = { count: 0 };

    shouldComponentUpdate(nextProps, nextState) {
        // 返回false可以阻止更新，用于性能优化
        return nextState.count !== this.state.count;
    }

    getSnapshotBeforeUpdate(prevProps, prevState) {
        // 返回值会传递给componentDidUpdate
        return { scrollTop: this.listRef?.scrollTop };
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        // 可以访问更新前的DOM状态
        if (snapshot) {
            this.listRef.scrollTop = snapshot.scrollTop;
        }
    }

    render() {
        return <div>计数：{this.state.count}</div>;
    }
}
```

&emsp;&emsp;**（3）卸载阶段**
```
componentWillUnmount()
```
```jsx
class Timer extends React.Component {
    componentDidMount() {
        this.timerID = setInterval(() => {
            console.log('tick');
        }, 1000);
    }

    componentWillUnmount() {
        // 清理定时器、取消订阅等
        clearInterval(this.timerID);
    }

    render() {
        return <div>计时器组件</div>;
    }
}
```

---

## 14、React.Component常用方法

&emsp;&emsp;**（1）setState详解**
```jsx
class MyComponent extends React.Component {
    state = { count: 0 };

    // 方式1：对象形式（可能异步更新）
    handleClick1 = () => {
        this.setState({ count: this.state.count + 1 });
    };

    // 方式2：函数形式（推荐，确保基于最新状态）
    handleClick2 = () => {
        this.setState((state, props) => ({
            count: state.count + 1
        }));
    };

    // 方式3：回调函数（更新完成后执行）
    handleClick3 = () => {
        this.setState(
            { count: this.state.count + 1 },
            () => console.log('状态更新完成')
        );
    };
}
```

&emsp;&emsp;**（2）forceUpdate**
```jsx
class MyComponent extends React.Component {
    handleForceUpdate = () => {
        // 强制组件重新渲染，跳过shouldComponentUpdate
        this.forceUpdate();
    };
}
```

---

---

## 高级应用篇

## 15、高阶组件（HOC）

&emsp;&emsp;**高阶组件是参数为组件，返回值为新组件的函数。**

&emsp;&emsp;**（1）基本结构**
```jsx
// 高阶组件函数
function withAuthentication(WrappedComponent) {
    return function AuthenticatedComponent(props) {
        const [isAuthenticated, setIsAuthenticated] = useState(false);

        if (!isAuthenticated) {
            return <div>请先登录</div>;
        }

        return <WrappedComponent {...props} />;
    };
}

// 使用HOC
const AuthenticatedUserProfile = withAuthentication(UserProfile);

function App() {
    return <AuthenticatedUserProfile />;
}
```

&emsp;&emsp;**（2）HOC高级用法：属性代理**
```jsx
function withStyles(WrappedComponent) {
    return function StyledComponent(props) {
        const style = {
            padding: '20px',
            background: '#f5f5f5',
            borderRadius: '8px'
        };

        // 传递新的props
        const newProps = {
            ...props,
            customProp: '额外添加的属性'
        };

        return (
            <div style={style}>
                <WrappedComponent {...newProps} />
            </div>
        );
    };
}
```

&emsp;&emsp;**（3）HOC高级用法：继承反转**
```jsx
function withLoading(WrappedComponent) {
    return class WithLoading extends WrappedComponent {
        render() {
            if (this.props.isLoading) {
                return <div>加载中...</div>;
            }
            return super.render();
        }
    };
}
```

---

## 16、Render Props

&emsp;&emsp;**Render Props是一种在组件之间共享代码的技术，使用一个值为函数的prop。**

&emsp;&emsp;**（1）基本用法**
```jsx
class MouseTracker extends React.Component {
    state = { x: 0, y: 0 };

    handleMouseMove = (e) => {
        this.setState({
            x: e.clientX,
            y: e.clientY
        });
    };

    render() {
        return (
            <div onMouseMove={this.handleMouseMove}>
                {this.props.render(this.state)}
            </div>
        );
    }
}

// 使用render prop
function App() {
    return (
        <MouseTracker
            render={({ x, y }) => (
                <h1>鼠标位置：({x}, {y})</h1>
            )}
        />
    );
}
```

&emsp;&emsp;**（2）children作为函数**
```jsx
// 将children改为函数形式
function MouseTracker({ children }) {
    const [position, setPosition] = useState({ x: 0, y: 0 });

    const handleMouseMove = (e) => {
        setPosition({ x: e.clientX, y: e.clientY });
    };

    return (
        <div onMouseMove={handleMouseMove}>
            {children(position)}
        </div>
    );
}

// 使用
<MouseTracker>
    {({ x, y }) => (
        <div>
            鼠标位置：{x}, {y}
        </div>
    )}
</MouseTracker>
```

---

## 17、组件优化PureComponent与React.memo

&emsp;&emsp;**（1）PureComponent**
```jsx
// 类组件使用PureComponent自动进行浅比较
class MyComponent extends React.PureComponent {
    render() {
        return <div>{this.props.name}</div>;
    }
}

// 注意：如果是引用类型，需要创建新对象
class Parent extends React.PureComponent {
    state = {
        items: [{ id: 1 }]
    };

    // 错误：直接修改会跳过更新
    handleAdd = () => {
        this.state.items.push({ id: 2 });
        this.forceUpdate(); // 需要强制更新
    };

    // 正确：创建新数组
    handleAdd = () => {
        this.setState({
            items: [...this.state.items, { id: 2 }]
        });
    };
}
```

&emsp;&emsp;**（2）React.memo**
```jsx
// 函数组件使用React.memo
const MyComponent = React.memo(function MyComponent(props) {
    return <div>{props.name}</div>;
});

// 自定义比较函数
const MyComponent = React.memo(
    function MyComponent(props) {
        return <div>{props.name}</div>;
    },
    (prevProps, nextProps) => {
        // 返回true表示不需要重新渲染
        return prevProps.name === nextProps.name;
    }
);
```

&emsp;&emsp;**（3）性能优化对比**
```
+------------------+------------------------+------------------------+
|    特性          |    类组件              |     函数组件           |
+------------------+------------------------+------------------------+
|  组件类型        |  Component             |  React.memo            |
|  浅比较          |  PureComponent自动     |  React.memo自动        |
|  自定义比较      |  shouldComponentUpdate |  React.memo第二个参数  |
|  深比较          |  需手动实现            |  需手动实现            |
+------------------+------------------------+------------------------+
```

---

## 18、React中的DOM操作

&emsp;&emsp;**（1）Refs创建与使用**
```jsx
class AutoFocusInput extends React.Component {
    constructor(props) {
        super(props);
        // 创建ref
        this.textInput = React.createRef();
    }

    componentDidMount() {
        // 访问DOM元素
        this.textInput.current.focus();
    }

    render() {
        return (
            <input
                ref={this.textInput}
                type="text"
            />
        );
    }
}
```

&emsp;&emsp;**（2）回调Refs**
```jsx
class CustomTextInput extends React.Component {
    constructor(props) {
        super(props);
        this.textInput = null;
        // 设置回调ref
        this.setTextInputRef = element => {
            this.textInput = element;
        };
    }

    componentDidMount() {
        // 组件挂载后自动聚焦
        if (this.textInput) {
            this.textInput.focus();
        }
    }

    render() {
        return (
            <input
                ref={this.setTextInputRef}
                type="text"
            />
        );
    }
}
```

&emsp;&emsp;**（3）函数组件使用Refs**
```jsx
function TextInput() {
    const inputRef = useRef(null);

    const focusInput = () => {
        inputRef.current.focus();
    };

    return (
        <div>
            <input ref={inputRef} type="text" />
            <button onClick={focusInput}>聚焦</button>
        </div>
    );
}
```

---

## 19、React中的表单处理

&emsp;&emsp;**（1）受控组件**
```jsx
function LoginForm() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('用户名:', username, '密码:', password);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="用户名"
            />
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="密码"
            />
            <button type="submit">登录</button>
        </form>
    );
}
```

&emsp;&emsp;**（2）非受控组件**
```jsx
class FileInput extends React.Component {
    constructor(props) {
        super(props);
        this.fileInput = React.createRef();
    }

    handleSubmit = (e) => {
        e.preventDefault();
        alert(`选择了文件: ${this.fileInput.current.files[0].name}`);
    };

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <input type="file" ref={this.fileInput} />
                <button type="submit">提交</button>
            </form>
        );
    }
}
```

&emsp;&emsp;**（3）多个输入框的处理**
```jsx
function MultiInputForm() {
    const [form, setForm] = useState({
        username: '',
        email: '',
        password: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm(prev => ({
            ...prev,
            [name]: value
        }));
    };

    return (
        <form>
            <input
                name="username"
                value={form.username}
                onChange={handleChange}
            />
            <input
                name="email"
                value={form.email}
                onChange={handleChange}
            />
            <input
                name="password"
                type="password"
                value={form.password}
                onChange={handleChange}
            />
        </form>
    );
}
```

---

## 高级应用篇

---

## 状态管理篇

## 20、Redux状态管理

&emsp;&emsp;**（1）Redux核心概念**
```
+----------------+     +----------------+     +----------------+
|    State       | --> |    View        | --> |    Actions      |
|  (单一数据源)  |     |  (React组件)   |     |  (描述意图)     |
+----------------+     +----------------+     +----------------+
       ^                                              |
       |                                              v
       +--------------     +----------------+
                             |    Reducer     |
                             |  (纯函数计算)   |
                             +----------------+
```

&emsp;&emsp;**（2）Redux基本使用**
```jsx
// 1. 定义Action Types
const ADD_TODO = 'ADD_TODO';
const TOGGLE_TODO = 'TOGGLE_TODO';

// 2. 创建Action Creators
const addTodo = (text) => ({
    type: ADD_TODO,
    payload: { text, id: Date.now() }
});

const toggleTodo = (id) => ({
    type: TOGGLE_TODO,
    payload: { id }
});

// 3. 创建Reducer
const initialState = { todos: [] };

function todoReducer(state = initialState, action) {
    switch (action.type) {
        case ADD_TODO:
            return {
                ...state,
                todos: [...state.todos, action.payload]
            };
        case TOGGLE_TODO:
            return {
                ...state,
                todos: state.todos.map(todo =>
                    todo.id === action.payload.id
                        ? { ...todo, completed: !todo.completed }
                        : todo
                )
            };
        default:
            return state;
    }
}

// 4. 创建Store
import { createStore } from 'redux';
const store = createStore(todoReducer);

// 5. 使用Store
store.dispatch(addTodo('学习React'));
store.dispatch(toggleTodo(1));

console.log(store.getState());
```

&emsp;&emsp;**（3）React-Redux连接**
```jsx
import { Provider, useSelector, useDispatch } from 'react-redux';

// 连接到React组件
function Counter() {
    const count = useSelector(state => state.counter.count);
    const dispatch = useDispatch();

    return (
        <div>
            <p>计数：{count}</p>
            <button onClick={() => dispatch({ type: 'INCREMENT' })}>+1</button>
        </div>
    );
}

// 使用Provider包裹应用
function App() {
    return (
        <Provider store={store}>
            <Counter />
        </Provider>
    );
}
```

---

## 21、React Router路由

&emsp;&emsp;**（1）基本路由配置**
```jsx
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            <nav>
                <Link to="/">首页</Link>
                <Link to="/about">关于</Link>
                <Link to="/user/123">用户</Link>
            </nav>

            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/user/:id" element={<User />} />
                <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
                <Route path="*" element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    );
}
```

&emsp;&emsp;**（2）路由参数获取**
```jsx
// URL参数
function User() {
    const { id } = useParams();
    return <div>用户ID: {id}</div>;
}

// 查询参数
function Search() {
    const [searchParams, setSearchParams] = useSearchParams();
    const query = searchParams.get('q');
    const page = searchParams.get('page') || 1;

    return (
        <div>
            <p>搜索: {query}</p>
            <p>页码: {page}</p>
            <button onClick={() => setSearchParams({ q: 'new query' })}>
                改变参数
            </button>
        </div>
    );
}

// 程序式导航
function Login() {
    const navigate = useNavigate();

    const handleLogin = () => {
        // 登录逻辑...
        navigate('/dashboard', { replace: true });
    };

    return <button onClick={handleLogin}>登录</button>;
}
```

&emsp;&emsp;**（3）嵌套路由**
```jsx
function App() {
    return (
        <Routes>
            <Route path="/admin" element={<AdminLayout />}>
                <Route index element={<AdminDashboard />} />
                <Route path="users" element={<UserManagement />} />
                <Route path="settings" element={<AdminSettings />} />
            </Route>
        </Routes>
    );
}

function AdminLayout() {
    return (
        <div className="admin-layout">
            <aside>
                <nav>
                    <Link to="/admin">仪表盘</Link>
                    <Link to="/admin/users">用户管理</Link>
                </nav>
            </aside>
            <main>
                {/* 嵌套路由内容在这里渲染 */}
                <Outlet />
            </main>
        </div>
    );
}
```

---

## 22、React性能优化

&emsp;&emsp;**（1）代码分割**
```jsx
// React.lazy 懒加载
const OtherComponent = React.lazy(() => import('./OtherComponent'));

function MyComponent() {
    return (
        <div>
            <Suspense fallback={<div>加载中...</div>}>
                <OtherComponent />
            </Suspense>
        </div>
    );
}

// 路由级别代码分割
const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));

function App() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
        </Routes>
    );
}
```

&emsp;&emsp;**（2）组件卸载优化**
```jsx
// 列表虚拟化（长列表优化）
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }) {
    const Row = ({ index, style }) => (
        <div style={style}>
            {items[index].name}
        </div>
    );

    return (
        <FixedSizeList
            height={400}
            itemCount={items.length}
            itemSize={50}
            width={300}
        >
            {Row}
        </FixedSizeList>
    );
}
```

&emsp;&emsp;**（3）避免不必要的渲染**
```jsx
// 使用React.memo包装组件
const MemoizedComponent = React.memo(Component);

// 使用key帮助Diff算法
function List({ items }) {
    return (
        <ul>
            {items.map(item => (
                // 使用唯一稳定的key
                <li key={item.id}>{item.name}</li>
            ))}
        </ul>
    );
}

// 组件拆分为小颗粒
// 好的：将变化频繁的部分单独提取
function ProductPage({ product, onAddToCart }) {
    const [selectedOption, setSelectedOption] = useState(null);

    return (
        <div>
            <ProductDetails product={product} />
            <OptionSelector
                selected={selectedOption}
                onChange={setSelectedOption}
            />
            <AddToCartButton onClick={() => onAddToCart(product)} />
        </div>
    );
}
```

---

## 23、React中的错误边界

&emsp;&emsp;**（1）定义错误边界**
```jsx
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        // 更新state使下一次渲染能够显示错误UI
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        // 记录错误信息
        console.error('ErrorBoundary caught an error:', error, errorInfo);
        logErrorToService(error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div>
                    <h1>出错了</h1>
                    <p>{this.state.error.toString()}</p>
                    <button onClick={() => window.location.reload()}>
                        刷新页面
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}
```

&emsp;&emsp;**（2）使用错误边界**
```jsx
function App() {
    return (
        <ErrorBoundary>
            <Header />
            <ErrorBoundary>
                <MainContent />
            </ErrorBoundary>
            <Footer />
        </ErrorBoundary>
    );
}
```

---

## 24、React与TypeScript

&emsp;&emsp;**（1）组件类型定义**
```tsx
// 函数组件类型
interface ButtonProps {
    text: string;
    onClick: () => void;
    variant?: 'primary' | 'secondary';
    disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({
    text,
    onClick,
    variant = 'primary',
    disabled = false
}) => {
    return (
        <button
            className={`btn btn-${variant}`}
            onClick={onClick}
            disabled={disabled}
        >
            {text}
        </button>
    );
};
```

&emsp;&emsp;**（2）Props类型定义**
```tsx
// children类型
interface CardProps {
    title: string;
    children: React.ReactNode;
}

// 事件处理类型
interface InputProps {
    value: string;
    onChange: React.ChangeEventHandler<HTMLInputElement>;
    onBlur: React.FocusEventHandler<HTMLInputElement>;
}

// 泛型组件
interface ListProps<T> {
    items: T[];
    renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
    return <ul>{items.map((item, i) => <li key={i}>{renderItem(item)}</li>)}</ul>;
}
```

&emsp;&emsp;**（3）常用Hooks类型**
```tsx
// useState
const [count, setCount] = useState<number>(0);
const [user, setUser] = useState<User | null>(null);

// useRef
const inputRef = useRef<HTMLInputElement>(null);
const timerRef = useRef<number | null>(null);

// useReducer
interface State { count: number; }
type Action = { type: 'increment' } | { type: 'decrement' };

const [state, dispatch] = useReducer((state: State, action: Action) => {
    // ...
}, { count: 0 });

// useContext
const ThemeContext = createContext<{ theme: string; toggle: () => void } | null>(null);
```

---

---

## React 18新特性篇

## 25、React 18新特性

&emsp;&emsp;**（1）自动批处理（Automatic Batching）**
```jsx
// React 18之前：多次setState只在事件处理函数结束时批处理一次
// React 18：所有setState都会自动批处理

function App() {
    const [count, setCount] = useState(0);
    const [flag, setFlag] = useState(false);

    const handleClick = () => {
        fetch('/api').then(() => {
            // React 17中只有一次渲染，React 18中也只有一次
            setCount(c => c + 1);
            setFlag(f => !f);
        });
    };

    return <button onClick={handleClick}>点击</button>;
}
```

&emsp;&emsp;**（2）新的Root API**
```jsx
// React 17
import ReactDOM from 'react-dom';
ReactDOM.render(<App />, document.getElementById('root'));

// React 18
import ReactDOM from 'react-dom';
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

// 支持卸载
root.unmount();
```

&emsp;&emsp;**（3）Suspense改进**
```jsx
// 路由级别的Suspense
<Suspense fallback={<Loading />}>
    <Routes>
        <Route path="/" element={<Home />} />
    </Routes>
</Suspense>

// 结合React.lazy使用
const LazyComponent = lazy(() => new Promise(resolve => {
    setTimeout(() => resolve({ default: Component }), 1000);
}));
```

&emsp;&emsp;**（4）useId**
```jsx
function LoginForm() {
    const id = useId();

    return (
        <div>
            <label htmlFor={id}>用户名</label>
            <input id={id} type="text" />
        </div>
    );
}
```

&emsp;&emsp;**（5）useTransition**
```jsx
function SearchResults() {
    const [isPending, startTransition] = useTransition();
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = (newQuery) => {
        startTransition(() => {
            setQuery(newQuery);
            setResults(searchAPI(newQuery));
        });
    };

    return (
        <div>
            <input onChange={(e) => handleSearch(e.target.value)} />
            {isPending ? <Spinner /> : <ResultsList results={results} />}
        </div>
    );
}
```

---

## 26、React状态管理进阶

&emsp;&emsp;**（1）Zustand使用**
```jsx
import { create } from 'zustand';

const useStore = create((set) => ({
    bears: 0,
    increase: () => set((state) => ({ bears: state.bears + 1 })),
    reset: () => set({ bears: 0 })
}));

function BearCounter() {
    const bears = useStore((state) => state.bears);
    return <h1>{bears} 只熊</h1>;
}
```

&emsp;&emsp;**（2）Jotai使用**
```jsx
import { atom, useAtom } from 'jotai';

const countAtom = atom(0);
const doubledAtom = atom((get) => get(countAtom) * 2);

function Counter() {
    const [count, setCount] = useAtom(countAtom);
    const [doubled] = useAtom(doubledAtom);

    return (
        <div>
            <p>计数: {count}</p>
            <p>双倍: {doubled}</p>
            <button onClick={() => setCount(c => c + 1)}>+</button>
        </div>
    );
}
```

---

## 27、React测试

&emsp;&emsp;**（1）Jest + React Testing Library**
```jsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Counter from './Counter';

// 测试组件渲染
test('renders counter with initial value', () => {
    render(<Counter initialCount={5} />);
    expect(screen.getByText('计数：5')).toBeInTheDocument();
});

// 测试交互
test('increments counter when button is clicked', async () => {
    render(<Counter initialCount={0} />);
    const button = screen.getByRole('button', { name: '增加' });

    fireEvent.click(button);
    expect(screen.getByText('计数：1')).toBeInTheDocument();

    // 使用userEvent更接近真实用户行为
    await userEvent.click(button);
    expect(screen.getByText('计数：2')).toBeInTheDocument();
});

// 测试异步操作
test('fetches and displays user data', async () => {
    render(<UserProfile userId={1} />);

    // 等待数据加载
    expect(await screen.findByText('加载中...')).toBeInTheDocument();
    expect(await screen.findByText('张三')).toBeInTheDocument();
});
```

---

## 28、React最佳实践

&emsp;&emsp;**（1）组件设计原则**
```
1. 单一职责原则（SPR）：每个组件只做一件事
2. 组件纯度：相同props总是渲染相同结果
3. 状态最小化：尽可能使用props和Context
4. 派生状态：尽量减少派生状态的使用
```

&emsp;&emsp;**（2）Hooks使用规范**
```jsx
// 1. 只在顶层调用Hooks
function CorrectComponent() {
    const [count, setCount] = useState(0); // ✅
    const [name, setName] = useState('');  // ✅

    if (condition) {
        // ❌ 不要在条件语句中调用
        const [temp, setTemp] = useState(null);
    }

    // 2. 只在React函数中调用
    // 3. 自定义Hooks以use开头
}

// 自定义Hook示例
function useLocalStorage(key, initialValue) {
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            return initialValue;
        }
    });

    const setValue = (value) => {
        try {
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error(error);
        }
    };

    return [storedValue, setValue];
}
```

&emsp;&emsp;**（3）性能优化清单**
```
□ 使用生产版本进行测试
□ 避免不必要的重渲染
□ 列表渲染时添加唯一key
□ 使用React.memo包装纯组件
□ 使用useMemo缓存计算结果
□ 使用useCallback缓存回调函数
□ 使用代码分割和懒加载
□ 正确设置依赖数组
□ 清理副作用
□ 避免匿名函数和对象
```

---

## 29、React常见面试题

&emsp;&emsp;**（1）虚拟DOM的工作原理**
&emsp;&emsp;虚拟DOM是真实DOM的JavaScript对象表示。当状态变化时，React会：
1. 创建新的虚拟DOM树
2. 与旧的虚拟DOM树进行Diff比较
3. 计算出最小更新集合
4. 批量更新真实DOM

&emsp;&emsp;**（2）React Fiber是什么**
&emsp;&emsp;React Fiber是React 16引入的新协调引擎，将协调工作拆分成小单元，可以中断、恢复和复用，提高了应用的响应性和流畅度。

&emsp;&emsp;**（3）key的作用**
&emsp;&emsp;Key帮助React识别哪些元素改变了，添加、删除或重新排序。应该使用数据中的唯一标识作为key，避免使用索引。

&emsp;&emsp;**（4）React中的diffing算法**
&emsp;&emsp;React的diffing算法遵循三个策略：
1. 不同类型的元素产生不同的树
2. 相同类型的元素对比属性
3. 相同类型的组件元素，递归对比子元素

&emsp;&emsp;**（5）为什么需要useEffect的依赖数组**
&emsp;&emsp;依赖数组告诉React只有在指定值变化时才执行effect。空数组表示只在挂载时执行一次。缺少依赖可能导致使用过期值或无限循环。

---

## 30、综合实战：Todo应用

&emsp;&emsp;**完整的功能性Todo应用示例：**
```jsx
import React, { useState, useEffect, useRef } from 'react';

// Todo项组件
function TodoItem({ todo, onToggle, onDelete }) {
    return (
        <li className={todo.completed ? 'completed' : ''}>
            <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => onToggle(todo.id)}
            />
            <span>{todo.text}</span>
            <button onClick={() => onDelete(todo.id)}>删除</button>
        </li>
    );
}

// Todo列表组件
function TodoList({ todos, onToggle, onDelete, filter }) {
    const filteredTodos = todos.filter(todo => {
        switch (filter) {
            case 'active': return !todo.completed;
            case 'completed': return todo.completed;
            default: return true;
        }
    });

    return (
        <ul>
            {filteredTodos.map(todo => (
                <TodoItem
                    key={todo.id}
                    todo={todo}
                    onToggle={onToggle}
                    onDelete={onDelete}
                />
            ))}
        </ul>
    );
}

// 主应用组件
function TodoApp() {
    const [todos, setTodos] = useState([]);
    const [input, setInput] = useState('');
    const [filter, setFilter] = useState('all');
    const inputRef = useRef(null);

    // 从localStorage加载
    useEffect(() => {
        const saved = localStorage.getItem('todos');
        if (saved) {
            setTodos(JSON.parse(saved));
        }
    }, []);

    // 保存到localStorage
    useEffect(() => {
        localStorage.setItem('todos', JSON.stringify(todos));
    }, [todos]);

    const addTodo = () => {
        if (input.trim()) {
            setTodos([
                ...todos,
                {
                    id: Date.now(),
                    text: input.trim(),
                    completed: false,
                    createdAt: new Date().toISOString()
                }
            ]);
            setInput('');
        }
    };

    const toggleTodo = (id) => {
        setTodos(todos.map(todo =>
            todo.id === id ? { ...todo, completed: !todo.completed } : todo
        ));
    };

    const deleteTodo = (id) => {
        setTodos(todos.filter(todo => todo.id !== id));
    };

    const clearCompleted = () => {
        setTodos(todos.filter(todo => !todo.completed));
    };

    const activeCount = todos.filter(t => !t.completed).length;
    const completedCount = todos.length - activeCount;

    return (
        <div className="todo-app">
            <h1>Todo App</h1>

            <div className="input-section">
                <input
                    ref={inputRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && addTodo()}
                    placeholder="添加新任务..."
                />
                <button onClick={addTodo}>添加</button>
            </div>

            <div className="filters">
                <button
                    className={filter === 'all' ? 'active' : ''}
                    onClick={() => setFilter('all')}
                >
                    全部 ({todos.length})
                </button>
                <button
                    className={filter === 'active' ? 'active' : ''}
                    onClick={() => setFilter('active')}
                >
                    待办 ({activeCount})
                </button>
                <button
                    className={filter === 'completed' ? 'active' : ''}
                    onClick={() => setFilter('completed')}
                >
                    已完成 ({completedCount})
                </button>
            </div>

            <TodoList
                todos={todos}
                filter={filter}
                onToggle={toggleTodo}
                onDelete={deleteTodo}
            />

            {completedCount > 0 && (
                <button onClick={clearCompleted} className="clear-btn">
                    清除已完成
                </button>
            )}
        </div>
    );
}

export default TodoApp;
```

---

---

## 原理深度篇

## 31、React原理深度解析

### 31.1 虚拟DOM工作原理

&emsp;&emsp;**（1）什么是虚拟DOM**
&emsp;&emsp;虚拟DOM是真实DOM的JavaScript对象表示，用轻量级的JS对象描述复杂的DOM结构。

```jsx
// 真实DOM结构
<div className="container">
    <h1>标题</h1>
    <p>内容</p>
</div>

// 对应的虚拟DOM对象
{
    type: 'div',
    props: {
        className: 'container',
        children: [
            { type: 'h1', props: { children: '标题' } },
            { type: 'p', props: { children: '内容' } }
        ]
    }
}
```

&emsp;&emsp;**（2）虚拟DOM的优势**
```
+------------------+------------------------+------------------------+
|    操作          |      真实DOM           |      虚拟DOM           |
+------------------+------------------------+------------------------+
|  创建新元素      |  直接创建，重量级      |  创建JS对象，轻量级     |
|  属性修改        |  直接修改，触发重排    |  修改JS对象，可批量     |
|  批量更新        |  每次修改都触发重排    |  先更新虚拟DOM再批量   |
|  跨平台能力      |  仅限浏览器            |  可支持SSR、移动端等   |
+------------------+------------------------+------------------------+
```

&emsp;&emsp;**（3）虚拟DOM的创建过程**
```jsx
// JSX会被Babel编译成createElement调用
const element = (
    <div className="greeting">
        <h1>Hello!</h1>
        <p>Welcome to React</p>
    </div>
);

// 编译后等价于
const element = React.createElement(
    'div',
    { className: 'greeting' },
    React.createElement('h1', null, 'Hello!'),
    React.createElement('p', null, 'Welcome to React')
);

// createElement返回虚拟DOM对象
{
    type: 'div',
    props: {
        className: 'greeting',
        children: [
            { type: 'h1', props: { children: 'Hello!' } },
            { type: 'p', props: { children: 'Welcome to React' } }
        ]
    }
}
```

---

### 31.2 Diff算法详解

&emsp;&emsp;**（1）Diff算法核心策略**
&emsp;&emsp;React的Diff算法遵循三个核心策略来高效比较虚拟DOM树：

```jsx
// 策略一：不同类型的元素产生不同的树
// 当元素类型不同时，React会直接卸载旧树，构建新树
<div>
    <Counter />  // 类型: div
</div>

// 变为
<span>
    <Counter />  // 类型: span - 完全重建
</span>

// 策略二：相同类型的元素对比属性
<div className="before" title="old">
    <span>内容</span>
</div>

// 变为
<div className="after" title="new">  // 只修改变化的属性
    <span>内容</span>
</div>

// 策略三：相同类型的组件元素，递归对比子元素
```

&emsp;&emsp;**（2）List Diff（列表比对）**
&emsp;&emsp;列表对比是Diff算法中最复杂的部分，涉及key的作用。

```jsx
// 场景：列表元素重新排序
// 原列表
[A, B, C]  // key: 1, 2, 3

// 新列表
[B, A, C]  // key: 2, 1, 3

// 没有key时（错误做法）：
// React会认为ABC都变了，全部重新创建

// 有key时（正确做法）：
// React通过key识别出B和A只是交换了位置
// 只需要移动DOM节点，性能大幅提升
```

&emsp;&emsp;**（3）Tree Diff（树比对）**
```jsx
// React采用分层对比策略
// 1. 根节点对比 - 不同类型则完全重建
// 2. 同级节点逐个对比 - 使用key优化

// 示例：组件类型变化
<Profile person={person} />  // type: Profile

// 变为
<Avatar person={person} />   // type: Avatar - 完全重建子树
```

&emsp;&emsp;**（4）Component Diff（组件比对）**
```jsx
// 1. 相同类型组件：虚拟DOM递归对比
// 2. 不同类型组件：卸载重建

// 判断是否需要更新
shouldComponentUpdate(nextProps, nextState) {
    // 返回false跳过子树的diff
    return nextProps.id !== this.props.id;
}
```

---

### 31.3 React Fiber架构

&emsp;&emsp;**（1）为什么需要Fiber**
&emsp;&emsp;React 16之前的调和(Reconciliation)过程是同步的，当组件树非常庞大时，会阻塞主线程，导致页面卡顿。

```
React 15架构（同步调和）：
┌─────────────────────────────────────┐
│           Stack Reconciler           │
│  ┌────────────────────────────────┐ │
│  │   递归遍历组件树（不可中断）    │ │
│  │   work() -> render() -> commit │ │
│  └────────────────────────────────┘ │
│         阻塞主线程，大树会卡顿        │
└─────────────────────────────────────┘

React 16+ Fiber架构（可中断）：
┌─────────────────────────────────────┐
│            Fiber Reconciler          │
│  ┌────────────────────────────────┐ │
│  │  workLoop (可中断)              │ │
│  │  ┌─────┐ ┌─────┐ ┌─────┐      │ │
│  │  │Fiber│→│Fiber│→│Fiber│→ ... │ │
│  │  └──┬──┘ └──┬──┘ └──┬──┘      │ │
│  │     │       │       │         │ │
│  │  wipRoot  wipRoot  wipRoot     │ │
│  └─────┼───────┼───────┼──────────┘ │
│        │       │       │            │
│        └───────┴───────┘            │
│         时间切片，优先响应交互        │
└─────────────────────────────────────┘
```

&emsp;&emsp;**（2）Fiber数据结构**
```jsx
// Fiber节点的主要属性
const fiber = {
    // 标识组件信息
    type: 'div',                    // 组件类型
    key: null,                      // 唯一标识
    stateNode: null,                // DOM节点或组件实例

    // 连接关系
    return: fiber,                 // 父Fiber
    child: fiber,                   // 第一个子Fiber
    sibling: fiber,                 // 兄弟Fiber

    // 工作类型
    effectTag: 'Update',            // 标记要做的工作类型
    pendingProps: {},               // 新的props
    memoizedProps: {},              // 旧的props

    // 状态相关
    memoizedState: null,            // 组件状态
    alternate: fiber,              // 双缓存，用于切换

    // 更新队列
    updateQueue: [],               // 待执行的任务队列
};
```

&emsp;&emsp;**（3）Fiber的工作阶段**
```jsx
// 阶段一：Render/Reconciliation（可中断）
// 决定需要做什么工作
function renderPhase() {
    // 1. 创建新的Fiber树
    // 2. diff比较找出需要更新的地方
    // 3. 标记effect（副作用）
    // 可被高优先级任务打断
}

// 阶段二：Commit（不可中断）
// 执行实际的DOM操作
function commitPhase() {
    // 1. 执行所有标记的effect
    // 2. 更新DOM
    // 3. 调用生命周期函数
    // 必须一次性完成
}
```

&emsp;&emsp;**（4）Fiber的时间切片**
```jsx
// 使用requestIdleCallback实现时间切片
function workLoop(deadline) {
    while (nextUnitOfWork && deadline.timeRemaining() > 0) {
        // 执行一个小单元的工作
        nextUnitOfWork = performUnitOfWork(nextUnitOfWork);
    }

    // 如果还有工作，预约下一个时间片
    if (nextUnitOfWork) {
        requestIdleCallback(workLoop);
    }
}

// React实际使用scheduler包实现
import { scheduleCallback, shouldYield } from 'scheduler';

function performUnitOfWork(fiber) {
    // ...执行工作...

    // 检查是否需要让出控制权
    if (shouldYield()) {
        // 让出控制权给浏览器或其他高优先级任务
        scheduleCallback(performUnitOfWork);
    }
}
```

&emsp;&emsp;**（5）Fiber对生命周期的影响**
```jsx
// React 16之前（同步，可能阻塞）
componentWillMount
componentWillReceiveProps
componentWillUpdate
// 这些方法可能被多次调用，不适合做副作用操作

// React 16之后（异步可中断）
// 上述方法被标记为UNSAFE_
// 推荐使用getDerivedStateFromProps和getSnapshotBeforeUpdate
// 或使用Hooks方式
```

---

### 31.4 React更新机制

&emsp;&emsp;**（1）更新触发时机**
```jsx
// 触发更新的方式
// 1. setState（类组件）
this.setState({ count: this.state.count + 1 });

// 2. useState的setter（函数组件）
const [count, setCount] = useState(0);
setCount(count + 1);

// 3. forceUpdate
this.forceUpdate();

// 4. 父组件重新渲染
// 当父组件状态变化时，子组件会重新渲染
```

&emsp;&emsp;**（2）setState的同步与异步**
```jsx
// React 18之前
// 在React事件处理中是异步的
class Counter extends React.Component {
    handleClick = () => {
        this.setState({ count: this.state.count + 1 });
        console.log(this.state.count); // 仍然是旧值
    };
}

// 在setTimeout和原生事件中是同步的
componentDidMount() {
    document.addEventListener('click', () => {
        this.setState({ count: this.state.count + 1 });
        console.log(this.state.count); // 新值（React 18之前）
    });
}

// React 18之后
// 自动批处理，所有更新都是异步的
function App() {
    const [count, setCount] = useState(0);
    const [flag, setFlag] = useState(false);

    const handleClick = () => {
        fetch('/api').then(() => {
            setCount(c => c + 1);  // 不触发重渲染
            setFlag(f => !f);      // 不触发重渲染
            // 只触发一次重渲染
        });
    };
}
```

&emsp;&emsp;**（3）批量更新**
```jsx
// 同步批量更新
function Parent() {
    const [parentRender, setParentRender] = useState(0);

    return (
        <Child
            onClick={() => {
                setParentRender(c => c + 1);
                setParentRender(c => c + 1);
                // 只触发一次重渲染
            }}
        />
    );
}

// flushSync强制同步更新
import { flushSync } from 'react-dom';

function App() {
    const [count, setCount] = useState(0);

    const handleClick = () => {
        flushSync(() => {
            setCount(c => c + 1);  // 立即触发重渲染
        });
        flushSync(() => {
            setCount(c => c + 1);  // 再触发一次重渲染
        });
        // 触发两次重渲染
    };
}
```

---

### 31.5 React调度系统

&emsp;&emsp;**（1）调度优先级**
```jsx
// React 18之前的优先级
// ImmediatePriority - 同步优先级
// UserBlockingPriority - 用户阻塞优先级（约250ms）
// NormalPriority - 正常优先级（约5s）
// LowPriority - 低优先级（约10s）
// IdlePriority - 空闲优先级（无期限）

// React 18使用Lane模型
// 将任务分为不同车道
export const SyncLane = 0b0000000000000000000000000000001;
export const InputContinuousLane = 0b0000000000000000000000000000100;
export const DefaultLane = 0b0000000000000000000000000001000;
export const TransitionLane = 0b0000000000000000000000010000000;
export const IdleLane = 0b0000000000000000000100000000000;
```

&emsp;&emsp;**（2）useTransition与调度**
```jsx
function SearchResults() {
    const [isPending, startTransition] = useTransition();
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = (newQuery) => {
        // 将后续更新标记为非紧急任务
        startTransition(() => {
            setQuery(newQuery);
            // 这个更新可能被中断
            setResults(expensiveSearch(newQuery));
        });
    };

    // 搜索输入框是紧急的
    return (
        <div>
            <input
                value={query}
                onChange={(e) => {
                    setQuery(e.target.value);
                    handleSearch(e.target.value);
                }}
            />
            {isPending ? <Spinner /> : <ResultsList results={results} />}
        </div>
    );
}
```

---

---

## 自定义Hooks篇

## 32、自定义Hooks完整指南

### 32.1 自定义Hooks基础

&emsp;&emsp;**（1）自定义Hook规则**
```
1. 自定义Hook必须以"use"开头命名
2. 自定义Hook本质是一个函数，可以使用其他Hooks
3. 自定义Hook用于复用有状态的逻辑
4. 每次使用自定义Hook，都会创建独立的state
```

&emsp;&emsp;**（2）基本结构**
```jsx
// use+驼峰命名.js
import { useState, useEffect } from 'react';

function useCustomHook(initialValue, apiUrl) {
    // 可以在里面使用任何Hooks
    const [data, setData] = useState(initialValue);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(apiUrl)
            .then(res => res.json())
            .then(result => {
                setData(result);
                setLoading(false);
            });
    }, [apiUrl]);

    // 返回需要共享的状态和操作
    return { data, loading, setData };
}

// 使用自定义Hook
function MyComponent() {
    const { data, loading, setData } = useCustomHook([], '/api/items');
    // ...
}
```

---

### 32.2 常用自定义Hooks

&emsp;&emsp;**（1）useLocalStorage**
```jsx
function useLocalStorage(key, initialValue) {
    // 获取初始值
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error('Error reading localStorage:', error);
            return initialValue;
        }
    });

    // 设置值并同步到localStorage
    const setValue = (value) => {
        try {
            const valueToStore = value instanceof Function
                ? value(storedValue)
                : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error('Error setting localStorage:', error);
        }
    };

    // 监听其他标签页的修改
    useEffect(() => {
        const handleStorageChange = (e) => {
            if (e.key === key && e.newValue !== null) {
                setStoredValue(JSON.parse(e.newValue));
            }
        };

        window.addEventListener('storage', handleStorageChange);
        return () => window.removeEventListener('storage', handleStorageChange);
    }, [key]);

    return [storedValue, setValue];
}

// 使用示例
function App() {
    const [name, setName] = useLocalStorage('name', '');

    return (
        <div>
            <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="输入你的名字"
            />
            <p>你好，{name || '陌生人'}!</p>
        </div>
    );
}
```

&emsp;&emsp;**（2）useDebounce**
```jsx
function useDebounce(value, delay = 500) {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => {
            clearTimeout(timer);
        };
    }, [value, delay]);

    return debouncedValue;
}

// 使用示例：搜索防抖
function SearchComponent() {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);
    const [isSearching, setIsSearching] = useState(false);

    // 防抖后的搜索词
    const debouncedSearchTerm = useDebounce(searchTerm, 300);

    useEffect(() => {
        if (debouncedSearchTerm) {
            setIsSearching(true);
            searchAPI(debouncedSearchTerm)
                .then(setResults)
                .finally(() => setIsSearching(false));
        } else {
            setResults([]);
        }
    }, [debouncedSearchTerm]);

    return (
        <div>
            <input
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="搜索..."
            />
            {isSearching && <Spinner />}
            <ResultsList results={results} />
        </div>
    );
}
```

&emsp;&emsp;**（3）useFetch**
```jsx
function useFetch(url, options = {}) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const controller = new AbortController();

        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);

                const response = await fetch(url, {
                    ...options,
                    signal: controller.signal
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const result = await response.json();
                setData(result);
            } catch (err) {
                if (err.name !== 'AbortError') {
                    setError(err.message);
                }
            } finally {
                setLoading(false);
            }
        };

        fetchData();

        // 清理：组件卸载时取消请求
        return () => controller.abort();
    }, [url]);

    return { data, loading, error };
}

// 使用示例
function UserProfile({ userId }) {
    const { data: user, loading, error } = useFetch(
        `/api/users/${userId}`
    );

    if (loading) return <div>加载中...</div>;
    if (error) return <div>错误: {error}</div>;
    if (!user) return <div>用户不存在</div>;

    return (
        <div>
            <h1>{user.name}</h1>
            <p>{user.email}</p>
        </div>
    );
}
```

&emsp;&emsp;**（4）useToggle**
```jsx
function useToggle(initialValue = false) {
    const [value, setValue] = useState(initialValue);

    const toggle = useCallback(() => {
        setValue(v => !v);
    }, []);

    const setTrue = useCallback(() => {
        setValue(true);
    }, []);

    const setFalse = useCallback(() => {
        setValue(false);
    }, []);

    return { value, toggle, setTrue, setFalse };
}

// 使用示例
function ToggleComponent() {
    const { value: isOn, toggle, setTrue, setFalse } = useToggle(false);

    return (
        <div>
            <p>开关状态: {isOn ? 'ON' : 'OFF'}</p>
            <button onClick={toggle}>切换</button>
            <button onClick={setTrue}>打开</button>
            <button onClick={setFalse}>关闭</button>
        </div>
    );
}
```

&emsp;&emsp;**（5）useClickOutside**
```jsx
function useClickOutside(ref, handler) {
    useEffect(() => {
        const listener = (event) => {
            // 检查点击是否在ref元素内部
            if (!ref.current || ref.current.contains(event.target)) {
                return;
            }
            handler(event);
        };

        document.addEventListener('mousedown', listener);
        document.addEventListener('touchstart', listener);

        return () => {
            document.removeEventListener('mousedown', listener);
            document.removeEventListener('touchstart', listener);
        };
    }, [ref, handler]);
}

// 使用示例：点击外部关闭下拉菜单
function Dropdown() {
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);

    // 点击外部关闭
    useClickOutside(dropdownRef, () => setIsOpen(false));

    return (
        <div ref={dropdownRef}>
            <button onClick={() => setIsOpen(!isOpen)}>
                菜单
            </button>
            {isOpen && (
                <div className="dropdown-menu">
                    <MenuItem>选项1</MenuItem>
                    <MenuItem>选项2</MenuItem>
                </div>
            )}
        </div>
    );
}
```

&emsp;&emsp;**（6）useMediaQuery**
```jsx
function useMediaQuery(query) {
    const [matches, setMatches] = useState(
        () => window.matchMedia(query).matches
    );

    useEffect(() => {
        const mediaQuery = window.matchMedia(query);

        // 处理变化
        const handler = (event) => {
            setMatches(event.matches);
        };

        // 添加监听
        mediaQuery.addEventListener('change', handler);

        // 清理
        return () => mediaQuery.removeEventListener('change', handler);
    }, [query]);

    return matches;
}

// 使用示例
function ResponsiveComponent() {
    const isMobile = useMediaQuery('(max-width: 768px)');
    const isDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
    const isRetina = useMediaQuery('(-webkit-min-device-pixel-ratio: 2)');

    return (
        <div>
            {isMobile ? (
                <MobileLayout />
            ) : (
                <DesktopLayout />
            )}
            <p>深色模式: {isDarkMode ? '是' : '否'}</p>
            <p>视网膜屏幕: {isRetina ? '是' : '否'}</p>
        </div>
    );
}
```

---

### 32.3 进阶自定义Hooks

&emsp;&emsp;**（1）useAsync**
```jsx
function useAsync(asyncFn, immediate = true) {
    const [status, setStatus] = useState('idle');
    const [value, setValue] = useState(null);
    const [error, setError] = useState(null);

    const execute = useCallback(async (...args) => {
        setStatus('pending');
        setValue(null);
        setError(null);

        try {
            const response = await asyncFn(...args);
            setValue(response);
            setStatus('success');
        } catch (err) {
            setError(err);
            setStatus('error');
        }
    }, [asyncFn]);

    useEffect(() => {
        if (immediate) {
            execute();
        }
    }, [execute, immediate]);

    return {
        isIdle: status === 'idle',
        isLoading: status === 'pending',
        isError: status === 'error',
        isSuccess: status === 'success',
        execute,
        data: value,
        error
    };
}

// 使用示例
function UserProfile({ userId }) {
    const fetchUser = async () => {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) throw new Error('获取用户失败');
        return response.json();
    };

    const {
        isLoading,
        isError,
        isSuccess,
        execute: reload,
        data: user,
        error
    } = useAsync(fetchUser, false);

    useEffect(() => {
        reload();
    }, [userId]);

    if (isLoading) return <div>加载中...</div>;
    if (isError) return <div>错误: {error.message}</div>;

    return (
        <div>
            <h1>{user.name}</h1>
            <button onClick={reload}>刷新</button>
        </div>
    );
}
```

&emsp;&emsp;**（2）usePrevious**
```jsx
// 方法一：使用useRef保存上一次的值
function usePrevious(value) {
    const ref = useRef();

    useEffect(() => {
        ref.current = value;
    }, [value]);

    return ref.current;
}

// 方法二：支持多种类型
function usePrevious(value) {
    const { current } = useRef({ value });

    if (!Object.is(value, current.value)) {
        current.value = value;
    }

    return current.value;
}

// 使用示例
function CounterWithPrevious() {
    const [count, setCount] = useState(0);
    const previousCount = usePrevious(count);

    return (
        <div>
            <p>当前: {count}</p>
            <p>上次: {previousCount}</p>
            <button onClick={() => setCount(c => c + 1)}>
                增加
            </button>
        </div>
    );
}
```

---

---

## useEffect深入篇

## 33、useEffect深入理解和常见陷阱

### 33.1 useEffect执行时机

&emsp;&emsp;**（1）effect的执行时机**
```jsx
// useEffect是在渲染结果commit到DOM之后执行
// 注意：它不是渲染之后立即执行，而是"之后"

function App() {
    const [count, setCount] = useState(0);

    useEffect(() => {
        // 1. 组件渲染
        // 2. DOM更新
        // 3. 执行effect
        console.log('Effect执行了');
    });

    return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// 与componentDidMount/componentDidUpdate的区别
// componentDidMount/update: 同步执行，然后浏览器更新屏幕
// useEffect: 异步执行，在浏览器更新屏幕之后
```

&emsp;&emsp;**（2）依赖数组详解**
```jsx
// 1. 无依赖数组：每次渲染后都执行
useEffect(() => {
    console.log('每次渲染都执行');
});

// 2. 空数组：只在挂载时执行一次（类似componentDidMount）
useEffect(() => {
    console.log('只在挂载时执行');
    // 适合：发起网络请求、添加事件监听、操作DOM
}, []);

// 3. 有依赖：依赖变化时执行
useEffect(() => {
    console.log('count变化时执行');
}, [count]);

// 4. 多个依赖
useEffect(() => {
    console.log('count或name变化时执行');
}, [count, name]);
```

---

### 33.2 常见陷阱与解决方案

&emsp;&emsp;**（1）闭包陷阱**
```jsx
// 问题：effect中的变量是捕获的旧值
function Counter() {
    const [count, setCount] = useState(0);

    useEffect(() => {
        const timer = setInterval(() => {
            // 这里的count永远是0（闭包陷阱）
            setCount(count + 1);
        }, 1000);

        return () => clearInterval(timer);
    }, []); // 空依赖，count永远不变

    return <div>{count}</div>;
}

// 解决方案1：使用函数式更新
useEffect(() => {
    const timer = setInterval(() => {
        setCount(prev => prev + 1);  // 使用函数式更新
    }, 1000);

    return () => clearInterval(timer);
}, []);

// 解决方案2：将依赖添加到依赖数组
useEffect(() => {
    const timer = setInterval(() => {
        setCount(count + 1);
    }, 1000);

    return () => clearInterval(timer);
}, [count]);  // 每次count变化都会重新创建定时器

// 解决方案3：使用useRef保存最新值
function Counter() {
    const [count, setCount] = useState(0);
    const countRef = useRef(count);

    useEffect(() => {
        countRef.current = count;  // 更新ref
    });

    useEffect(() => {
        const timer = setInterval(() => {
            setCount(countRef.current + 1);  // 使用ref获取最新值
        }, 1000);

        return () => clearInterval(timer);
    }, []);

    return <div>{count}</div>;
}
```

&emsp;&emsp;**（2）无限循环问题**
```jsx
// 问题：effect中更新状态，导致无限循环
function App() {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch('/api/data')
            .then(res => res.json())
            .then(setData);  // 设置data
    });  // 缺少依赖数组，每次渲染都执行

    return <List data={data} />;
}

// 解决方案：正确设置依赖数组
useEffect(() => {
    fetch('/api/data')
        .then(res => res.json())
        .then(setData);
}, []);  // 空数组，只执行一次
```

&emsp;&emsp;**（3）竞态条件**
```jsx
// 问题：多个请求返回顺序不确定
function UserProfile({ userId }) {
    const [user, setUser] = useState(null);

    useEffect(() => {
        fetch(`/api/users/${userId}`)
            .then(res => res.json())
            .then(setUser);  // 可能有旧请求覆盖新请求
    }, [userId]);

    return <div>{user?.name}</div>;
}

// 解决方案：使用cleanup函数或AbortController
function UserProfile({ userId }) {
    const [user, setUser] = useState(null);

    useEffect(() => {
        let cancelled = false;

        fetch(`/api/users/${userId}`)
            .then(res => res.json())
            .then(data => {
                if (!cancelled) {  // 检查是否已取消
                    setUser(data);
                }
            });

        return () => {
            cancelled = true;  // 组件卸载或userId变化时标记
        };
    }, [userId]);

    // 或者使用AbortController（React 18+）
    useEffect(() => {
        const controller = new AbortController();

        fetch(`/api/users/${userId}`, {
            signal: controller.signal
        })
            .then(res => res.json())
            .then(setUser);

        return () => controller.abort();
    }, [userId]);

    return <div>{user?.name}</div>;
}
```

&emsp;&emsp;**（4）依赖数组依赖不足**
```jsx
// 问题：遗漏依赖导致使用过期值
function SearchResults({ query }) {
    const [results, setResults] = useState([]);
    const [page, setPage] = useState(1);

    useEffect(() => {
        searchAPI(query, page)
            .then(setResults);
    }, [query]);  // 缺少page依赖！

    return (
        <div>
            <Results data={results} />
            <button onClick={() => setPage(p => p + 1)}>
                下一页
            </button>
        </div>
    );
}

// 解决方案：包含所有使用的变量
useEffect(() => {
    searchAPI(query, page)
        .then(setResults);
}, [query, page]);
```

&emsp;&emsp;**（5）Effect中调用函数**
```jsx
// 问题：effect中定义并调用函数
useEffect(() => {
    function fetchData() {
        fetch('/api/data')
            .then(res => res.json())
            .then(setData);
    }

    fetchData();
}, []);

// 更好的做法：使用useCallback或提取到外部
const fetchData = useCallback(() => {
    fetch('/api/data')
        .then(res => res.json())
        .then(setData);
}, []);  // 根据setData的依赖添加依赖

useEffect(() => {
    fetchData();
}, [fetchData]);
```

---

### 33.3 useEffect清理函数

&emsp;&emsp;**（1）清理时机**
```jsx
// 清理函数在以下时机执行：
// 1. 组件卸载时
// 2. effect重新执行前（依赖变化时）

function App() {
    useEffect(() => {
        console.log('Effect执行');
        return () => console.log('Cleanup执行');
    }, [count]);

    return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// 第一次渲染: "Effect执行"
// 点击按钮: "Cleanup执行" -> "Effect执行"
// 卸载: "Cleanup执行"
```

&emsp;&emsp;**（2）常见清理场景**
```jsx
// 1. 清理定时器
useEffect(() => {
    const timer = setInterval(() => {
        setCount(c => c + 1);
    }, 1000);

    return () => clearInterval(timer);
}, []);

// 2. 清理事件监听
useEffect(() => {
    function handleResize() {
        setWindowWidth(window.innerWidth);
    }

    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize);
}, []);

// 3. 清理订阅
useEffect(() => {
    const subscription = dataSource.subscribe(
        data => setData(data)
    );

    return () => subscription.unsubscribe();
}, [dataSource]);

// 4. 清理WebSocket连接
useEffect(() => {
    const ws = new WebSocket('ws://api.example.com');

    ws.onmessage = (event) => {
        setMessages(prev => [...prev, event.data]);
    };

    return () => ws.close();
}, []);
```

---

### 33.4 useEffect与useLayoutEffect

&emsp;&emsp;**（1）执行时机区别**
```jsx
// useEffect
// - 渲染结果commit到DOM后异步执行
// - 不会阻塞浏览器绘制
// - 不会造成视觉闪烁

// useLayoutEffect
// - 渲染结果commit到DOM后同步执行
// - 会阻塞浏览器绘制
// - 用于需要同步读取/修改DOM的场景

function Tooltip() {
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const [show, setShow] = useState(false);
    const targetRef = useRef(null);

    // 使用useLayoutEffect确保位置计算在视觉更新前完成
    useLayoutEffect(() => {
        if (show && targetRef.current) {
            const rect = targetRef.current.getBoundingClientRect();
            setPosition({
                x: rect.left,
                y: rect.top - 10
            });
        }
    }, [show]);

    return (
        <>
            <button ref={targetRef} onClick={() => setShow(!show)}>
                Hover me
            </button>
            {show && (
                <div style={{ position: 'absolute', left: position.x, top: position.y }}>
                    Tooltip content
                </div>
            )}
        </>
    );
}

// 优先使用useEffect，只有在需要同步读取DOM时才用useLayoutEffect
```

---

---

## React 18并发篇

## 34、React 18新特性

### 34.1 并发渲染（Concurrent Rendering）

&emsp;&emsp;**（1）什么是并发渲染**
&emsp;&emsp;并发渲染是React 18引入的新能力，允许React同时准备多个版本的UI，通过时间切片实现可中断的渲染。

```
传统渲染（React 17及之前）：
|████████████|          |████████████|          |████████████|
   更新1                  更新2                  更新3
   (阻塞)                 (阻塞)                 (阻塞)

并发渲染（React 18）：
|████|  |████|  |████|    |██|  |██|          |████████|
  更新1   让出   继续      更新2                更新3
      ↑           ↑           ↑
   高优先级   让出控制    继续执行
   任务插入    给主线程    (低优先级)
```

&emsp;&emsp;**（2）startTransition**
```jsx
import { useTransition } from 'react';

// useTransition：标记非紧急更新
function App() {
    const [isPending, startTransition] = useTransition();
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = (value) => {
        setQuery(value);

        // 标记为可中断的过渡更新
        startTransition(() => {
            setResults(searchAPI(value));
        });
    };

    return (
        <div>
            <input onChange={(e) => handleSearch(e.target.value)} />
            {isPending ? <Spinner /> : <ResultsList results={results} />}
        </div>
    );
}

// useDeferredValue：延迟更新非紧急值
function SearchInput() {
    const [text, setText] = useState('');
    // deferredText会延迟更新，用于展示
    const deferredText = useDeferredValue(text);

    return (
        <div>
            <input value={text} onChange={(e) => setText(e.target.value)} />
            <SlowList text={deferredText} />  {/* 使用延迟值 */}
        </div>
    );
}
```

---

### 34.2 React Server Components (RSC)

&emsp;&emsp;**（1）服务端组件 vs 客户端组件**
```jsx
// 服务端组件 (Server Component)
// 默认，所有组件都是服务端组件
// 特点：
// - 在服务端执行，可以直接访问数据库、文件系统
// - 不能使用useState、useEffect等客户端Hooks
// - 不能添加事件监听

// app/components/ServerComponent.jsx (服务端组件)
async function ServerComponent() {
    // 直接访问数据库，无需API
    const data = await db.query('SELECT * FROM products');

    return (
        <div>
            {data.map(product => (
                <ProductCard key={product.id} {...product} />
            ))}
        </div>
    );
}

// 标记为客户端组件
// app/components/ClientComponent.jsx
'use client';

import { useState } from 'react';

function ClientComponent() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

&emsp;&emsp;**（2）服务端组件使用示例**
```jsx
// app/page.jsx
import { Suspense } from 'react';

// 服务端组件 - 获取数据
async function ProductList() {
    const products = await fetchProducts();
    return (
        <ul>
            {products.map(p => (
                <li key={p.id}>{p.name}</li>
            ))}
        </ul>
    );
}

// 客户端组件 - 交互
'use client';
function AddToCartButton({ productId }) {
    const [added, setAdded] = useState(false);
    return (
        <button onClick={() => setAdded(true)}>
            {added ? '已添加' : '加入购物车'}
        </button>
    );
}

// 页面组合
export default function Page() {
    return (
        <div>
            <h1>产品列表</h1>
            <Suspense fallback={<Loading />}>
                <ProductList />
            </Suspense>
        </div>
    );
}
```

---

### 34.3 Suspense增强

&emsp;&emsp;**（1）Suspense for Data Fetching**
```jsx
// 之前Suspense只用于React.lazy
// React 18支持数据获取的Suspense

function ProfilePage() {
    return (
        <Suspense fallback={<ProfileSkeleton />}>
            <ProfileDetails />
            <Suspense fallback={<FeedSkeleton />}>
                <Feed />
            </Suspense>
        </Suspense>
    );
}

// 配合React Query使用
import { Suspense } from 'react';
import { useQuery } from '@tanstack/react-query';

function UserProfile({ userId }) {
    const { data: user } = useQuery({
        queryKey: ['user', userId],
        queryFn: () => fetchUser(userId),
        suspense: true  // 启用suspense
    });

    return <div>{user.name}</div>;
}
```

&emsp;&emsp;**（2）use Suspense + use hook**
```jsx
// 新的API：use hook for Suspense
import { use, Suspense } from 'react';

// Promise作为prop
function User({ userPromise }) {
    const user = use(userPromise);  // 会suspend直到promise resolved
    return <div>{user.name}</div>;
}

function App() {
    return (
        <Suspense fallback={<div>加载中...</div>}>
            <User userPromise={fetchUser()} />
        </Suspense>
    );
}

// Context作为prop
function ThemeProvider({ themePromise }) {
    const theme = use(themePromise);
    return (
        <ThemeContext.Provider value={theme}>
            <App />
        </ThemeContext.Provider>
    );
}
```

---

### 34.4 其他新特性

&emsp;&emsp;**（1）新的Root API**
```jsx
// React 17
import ReactDOM from 'react-dom';
const container = document.getElementById('root');
ReactDOM.render(<App />, container);

// React 18
import ReactDOM from 'react-dom/client';
const root = ReactDOM.createRoot(container);
root.render(<App />);

// 新的卸载API
root.unmount();
```

&emsp;&emsp;**（2）严格模式改进**
```jsx
// React 18 StrictMode会执行两次effect
// 帮助发现副作用问题
function App() {
    useEffect(() => {
        console.log('Effect执行');
        return () => console.log('Cleanup');
    }, []);

    return <div>App</div>;
}

// 开发环境输出：
// Effect执行
// Cleanup
// Effect执行

// 这样可以发现：
// - 缺少cleanup导致的内存泄漏
// - effect不应该在mount时执行多次的问题
```

---

---

## Redux进阶篇

## 35、Redux Toolkit完整指南

### 35.1 Redux Toolkit简介

&emsp;&emsp;**Redux Toolkit（RTK）是Redux官方推荐的编写Redux逻辑的方式，简化了传统Redux的繁琐配置。**

&emsp;&emsp;**（1）核心API**
```
configureStore  - 创建store，整合reducer和middleware
createSlice     - 创建slice，包含reducer和action creators
createAsyncThunk- 创建异步action
createSelector  - 创建记忆化selector
```

&emsp;&emsp;**（2）createSlice基础**
```jsx
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
    name: string;
    age: number;
    status: 'idle' | 'loading' | 'failed';
}

const initialState: UserState = {
    name: '',
    age: 0,
    status: 'idle'
};

const userSlice = createSlice({
    name: 'user',  // 自动生成action type: 'user/setName'
    initialState,
    reducers: {
        // 普通reducer
        setName: (state, action: PayloadAction<string>) => {
            state.name = action.payload;
        },
        setAge: (state, action: PayloadAction<number>) => {
            state.age = action.payload;
        },
        setStatus: (state, action: PayloadAction<string>) => {
            state.status = action.payload;
        }
    }
});

// 导出自动生成的action creators和reducer
export const { setName, setAge, setStatus } = userSlice.actions;
export default userSlice.reducer;
```

---

### 35.2 Store配置与使用

&emsp;&emsp;**（1）创建Store**
```jsx
import { configureStore } from '@reduxjs/toolkit';
import userReducer from './features/userSlice';
import postsReducer from './features/postsSlice';

export const store = configureStore({
    reducer: {
        user: userReducer,
        posts: postsReducer,
        // 多个reducer会自动combine
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                // 忽略这些action类型的序列化检查
                ignoredActions: ['users/fetchUsers/fulfilled'],
            },
        }),
    devTools: process.env.NODE_ENV !== 'production',
});

// 自动类型推导
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

&emsp;&emsp;**（2）在组件中使用**
```jsx
import { useDispatch, useSelector } from 'react-redux';
import type { TypedUseSelectorHook } from 'react-redux';
import type { RootState, AppDispatch } from './store';

// 使用类型化的hooks
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// 组件中使用
function UserProfile() {
    const dispatch = useAppDispatch();
    const { name, age } = useAppSelector(state => state.user);

    return (
        <div>
            <p>姓名: {name}</p>
            <p>年龄: {age}</p>
            <button onClick={() => dispatch(setName('张三'))}>
                修改姓名
            </button>
        </div>
    );
}
```

---

### 35.3 createAsyncThunk异步处理

&emsp;&emsp;**（1）基本用法**
```jsx
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { fetchUserById } from './api';

// 创建异步thunk
export const fetchUser = createAsyncThunk(
    'users/fetchById',
    async (userId: number, { rejectWithValue }) => {
        try {
            const response = await fetchUserById(userId);
            return response;
        } catch (error) {
            // 自定义错误处理
            return rejectWithValue(error.message);
        }
    }
);

interface UserState {
    entities: User[];
    loading: 'idle' | 'pending' | 'succeeded' | 'failed';
    error: string | null;
}

const usersSlice = createSlice({
    name: 'users',
    initialState: { entities: [], loading: 'idle', error: null } as UserState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchUser.pending, (state) => {
                state.loading = 'pending';
            })
            .addCase(fetchUser.fulfilled, (state, action) => {
                state.loading = 'succeeded';
                state.entities.push(action.payload);
            })
            .addCase(fetchUser.rejected, (state, action) => {
                state.loading = 'failed';
                state.error = action.payload as string;
            });
    }
});
```

&emsp;&emsp;**（2）处理多个异步请求**
```jsx
// 并行请求
export const fetchUserAndPosts = createAsyncThunk(
    'users/fetchUserAndPosts',
    async (_, { dispatch }) => {
        const userPromise = dispatch(fetchUser(1)).unwrap();
        const postsPromise = dispatch(fetchPosts({ userId: 1 })).unwrap();

        const [user, posts] = await Promise.all([userPromise, postsPromise]);
        return { user, posts };
    }
);
```

---

### 35.4 createSelector记忆化选择器

&emsp;&emsp;**（1）基础记忆化**
```jsx
import { createSelector } from '@reduxjs/toolkit';

const selectUser = (state) => state.user;
const selectPosts = (state) => state.posts;

// 创建记忆化选择器
export const selectUserWithPosts = createSelector(
    [selectUser, selectPosts],  // 输入选择器
    (user, posts) => {
        // 只有user或posts变化时才会重新计算
        const userPosts = posts.filter(p => p.userId === user.id);
        return {
            ...user,
            postCount: userPosts.length,
            recentPosts: userPosts.slice(0, 5)
        };
    }
);

// 使用
function UserCard() {
    const userData = useAppSelector(selectUserWithPosts);
    // ...
}
```

&emsp;&emsp;**（2）参数化选择器**
```jsx
// 使用createSelectorFactory自定义选择器行为
import { createSelector } from '@reduxjs/toolkit';

const selectTodos = (state) => state.todos;

// 参数化选择器工厂
export const makeSelectTodosByStatus = () => {
    return createSelector(
        [selectTodos, (_, status) => status],
        (todos, status) => {
            if (status === 'all') return todos;
            return todos.filter(todo => todo.status === status);
        }
    );
};

// 在组件中使用
function TodoList() {
    const selectTodosByStatus = useMemo(makeSelectTodosByStatus, []);

    const activeTodos = useAppSelector(state =>
        selectTodosByStatus(state, 'active')
    );
    const completedTodos = useAppSelector(state =>
        selectTodosByStatus(state, 'completed')
    );
    // ...
}
```

---

---

## Router高级篇

## 36、React Router v6高级用法

### 36.1 路由守卫与权限控制

&emsp;&emsp;**（1）Auth Route（认证路由）**
```jsx
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';

function RequireAuth() {
    const { isAuthenticated, isLoading } = useAuth();

    if (isLoading) {
        return <LoadingSpinner />;
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    return <Outlet />;
}

function App() {
    return (
        <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route element={<RequireAuth />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/settings" element={<Settings />} />
            </Route>
        </Routes>
    );
}
```

&emsp;&emsp;**（2）角色权限控制**
```jsx
import { Navigate, Outlet } from 'react-router-dom';
import { useUserRole } from './hooks/useUserRole';

function RoleBasedRoute({ allowedRoles }) {
    const { role, isLoading } = useUserRole();

    if (isLoading) {
        return <LoadingSpinner />;
    }

    if (!allowedRoles.includes(role)) {
        return <Navigate to="/unauthorized" replace />;
    }

    return <Outlet />;
}

function App() {
    return (
        <Routes>
            <Route element={<RoleBasedRoute allowedRoles={['admin']} />}>
                <Route path="/admin" element={<AdminPanel />} />
                <Route path="/admin/users" element={<UserManagement />} />
            </Route>
            <Route element={<RoleBasedRoute allowedRoles={['user', 'admin']} />}>
                <Route path="/profile" element={<Profile />} />
            </Route>
        </Routes>
    );
}
```

---

### 36.2 动态路由与路由加载

&emsp;&emsp;**（1）数据加载模式**
```jsx
// 方式1：使用loader获取数据
import { useLoaderData } from 'react-router-dom';

async function loader({ params }) {
    const user = await fetchUser(params.id);
    return { user };
}

function UserProfile() {
    const { user } = useLoaderData();
    return <div>{user.name}</div>;
}

<Route path="/users/:id" element={<UserProfile />} loader={loader} />

// 方式2：使用Await和Suspense处理异步数据
import { Await, useLoaderData } from 'react-router-dom';
import { Suspense } from 'react';

function loader() {
    return fetchUserData();
}

function UserProfile() {
    const { userPromise } = useLoaderData();

    return (
        <Suspense fallback={<Loading />}>
            <Await
                resolve={userPromise}
                errorElement={<Error />}
                children={(user) => <div>{user.name}</div>}
            />
        </Suspense>
    );
}
```

&emsp;&emsp;**（2）Form与Actions**
```jsx
// 使用action处理表单提交
import { Form, useActionData, useNavigation } from 'react-router-dom';

async function action({ request }) {
    const formData = await request.formData();
    const data = Object.fromEntries(formData);

    await updateUser(data);
    return { success: true };
}

function EditProfile() {
    const actionData = useActionData();
    const navigation = useNavigation();
    const isSubmitting = navigation.state === 'submitting';

    return (
        <Form method="post">
            <input name="name" type="text" />
            <input name="email" type="email" />
            <button type="submit" disabled={isSubmitting}>
                {isSubmitting ? '提交中...' : '提交'}
            </button>
            {actionData?.success && <p>保存成功!</p>}
        </Form>
    );
}
```

---

### 36.3 路由元信息与转换

&emsp;&emsp;**（1）useMatches获取路由信息**
```jsx
import { useMatches } from 'react-router-dom';

function Breadcrumb() {
    const matches = useMatches();

    const crumbs = matches
        .filter(match => match.handle?.crumb)
        .map(match => ({
            label: match.handle.crumb(match.data),
            path: match.pathname
        }));

    return (
        <nav className="breadcrumb">
            {crumbs.map((crumb, index) => (
                <span key={crumb.path}>
                    {index > 0 && ' > '}
                    {index === crumbs.length - 1 ? (
                        crumb.label
                    ) : (
                        <Link to={crumb.path}>{crumb.label}</Link>
                    )}
                </span>
            ))}
        </nav>
    );
}

// 在路由中定义handle
function App() {
    return (
        <Routes>
            <Route path="/" handle={{ crumb: () => '首页' }} element={<Home />} />
            <Route
                path="/users/:id"
                handle={{ crumb: (data) => data.user.name }}
                element={<UserProfile />}
            />
        </Routes>
    );
}
```

---

### 36.4 路由状态管理

&emsp;&emsp;**（1）useSearchParams**
```jsx
function FilterableList() {
    const [searchParams, setSearchParams] = useSearchParams();
    const category = searchParams.get('category') || 'all';
    const sort = searchParams.get('sort') || 'newest';

    const updateFilter = (key, value) => {
        const newParams = new URLSearchParams(searchParams);
        if (value) {
            newParams.set(key, value);
        } else {
            newParams.delete(key);
        }
        setSearchParams(newParams);
    };

    return (
        <div>
            <select
                value={category}
                onChange={(e) => updateFilter('category', e.target.value)}
            >
                <option value="all">全部</option>
                <option value="electronics">电子产品</option>
                <option value="clothing">服装</option>
            </select>

            <select
                value={sort}
                onChange={(e) => updateFilter('sort', e.target.value)}
            >
                <option value="newest">最新</option>
                <option value="price-low">价格从低到高</option>
                <option value="price-high">价格从高到低</option>
            </select>

            <Link to="?" onClick={() => setSearchParams({})}>
                清除筛选
            </Link>
        </div>
    );
}
```

---

---

## CSS解决方案篇

## 37、React CSS解决方案对比

### 37.1 CSS Modules

&emsp;&emsp;**（1）基础使用**
```css
/* Button.module.css */
.button {
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
}

.primary {
    background: blue;
    color: white;
}

.secondary {
    background: gray;
    color: black;
}
```

```jsx
import styles from './Button.module.css';

function Button({ variant = 'primary', children }) {
    return (
        <button className={`${styles.button} ${styles[variant]}`}>
            {children}
        </button>
    );
}
```

&emsp;&emsp;**（2）高级特性**
```css
/* variables.module.css */
:local(.primary) {
    --bg-color: blue;
    --text-color: white;
}

/* 全局样式 */
:global(.app-container) {
    padding: 20px;
}
```

---

### 37.2 Styled Components

&emsp;&emsp;**（1）基础用法**
```jsx
import styled from 'styled-components';

// 创建样式组件
const Button = styled.button`
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    background: ${props => props.$primary ? 'blue' : 'gray'};
    color: ${props => props.$primary ? 'white' : 'black'};

    &:hover {
        opacity: 0.9;
    }

    &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
`;

// 使用
function App() {
    return (
        <div>
            <Button $primary>主要按钮</Button>
            <Button>次要按钮</Button>
        </div>
    );
}
```

&emsp;&emsp;**（2）扩展样式和继承**
```jsx
const BaseButton = styled.button`
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
`;

const PrimaryButton = styled(BaseButton)`
    background: blue;
    color: white;
`;

const LargeButton = styled(BaseButton)`
    font-size: 18px;
    padding: 12px 24px;
`;

// 动态样式
const Input = styled.input`
    border: 1px solid ${props => props.$error ? 'red' : '#ccc'};
    padding: 8px;
    border-radius: ${props => props.$rounded ? '50%' : '4px'};
`;
```

---

### 37.3 Tailwind CSS

&emsp;&emsp;**（1）基础用法**
```jsx
// 安装：npm install -D tailwindcss postcss autoprefixer
// 配置：npx tailwindcss init -p

function Button({ variant = 'primary', children }) {
    const baseClasses = 'px-4 py-2 rounded font-medium transition-colors';

    const variantClasses = {
        primary: 'bg-blue-500 text-white hover:bg-blue-600',
        secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
        danger: 'bg-red-500 text-white hover:bg-red-600'
    };

    return (
        <button className={`${baseClasses} ${variantClasses[variant]}`}>
            {children}
        </button>
    );
}
```

&emsp;&emsp;**（2）响应式和状态**
```jsx
function ResponsiveCard() {
    return (
        <div className="
            w-full md:w-1/2 lg:w-1/3
            p-4 md:p-6 lg:p-8
            bg-white
            rounded-lg
            shadow-md
            hover:shadow-lg
            transition-shadow
        ">
            <h2 className="text-xl font-bold text-gray-900">
                响应式卡片
            </h2>
            <p className="mt-2 text-gray-600">
                在不同屏幕尺寸下表现不同
            </p>
        </div>
    );
}

// 使用clsx或classnames合并动态类名
import { clsx } from 'clsx';

function Input({ error, disabled }) {
    return (
        <input
            className={clsx(
                'px-4 py-2 border rounded',
                error && 'border-red-500',
                disabled && 'bg-gray-100 cursor-not-allowed'
            )}
        />
    );
}
```

---

### 37.4 CSS解决方案对比

```
+------------------+-------------+-----------------+-------------+---------------+
|    特性          | CSS Modules | Styled Comps    | Tailwind    | CSS-in-JS     |
+------------------+-------------+-----------------+-------------+---------------+
| 写法             | CSS文件     | JS模板字符串    | HTML类名    | JS对象/模板   |
| 样式隔离         | 文件级      | 组件级          | 原子级      | 组件级        |
| 性能             | 好          | 运行时开销      | 最好        | 运行时开销    |
| 学习曲线         | 低          | 中等            | 陡峭        | 中等          |
| 运行时调试       | 好          | 好              | 一般        | 较好          |
| TypeScript支持   | 好          | 好              | 好          | 好            |
| SSR支持          | 好          | 需要配置        | 好          | 需(streaming) |
| CSS变量          | 原生支持    | 需要注入        | 原生支持    | 需要注入      |
+------------------+-------------+-----------------+-------------+---------------+
```

---

---

## 性能优化进阶篇

## 38、React性能优化深入策略

### 38.1 React.memo与性能优化

&emsp;&emsp;**（1）React.memo深入理解**
```jsx
// 基础用法
const MemoizedComponent = React.memo(function MyComponent(props) {
    // 只有props变化时才重新渲染
    return <div>{props.name}</div>;
});

// 自定义比较函数
const MyComponent = React.memo(
    function MyComponent({ name, age, address }) {
        return (
            <div>
                <p>{name}</p>
                <p>{age}</p>
                <p>{address}</p>
            </div>
        );
    },
    (prevProps, nextProps) => {
        // 返回true表示不需要重新渲染
        // 只有name和age变化才重渲染，忽略address
        return prevProps.name === nextProps.name &&
               prevProps.age === nextProps.age;
    }
);
```

&emsp;&emsp;**（2）避免过度优化**
```jsx
// 过度优化示例
const Child = React.memo(function Child({ onClick }) {
    // 即使使用了memo，onClick每次都是新函数引用
    return <button onClick={onClick}>点击</button>;
});

function Parent() {
    const [count, setCount] = useState(0);

    // 每次渲染都创建新函数
    const handleClick = () => console.log('clicked');

    return (
        <div>
            <span>{count}</span>
            <button onClick={() => setCount(c => c + 1)}>
                增加
            </button>
            <Child onClick={handleClick} /> {/* 仍然会重渲染 */}
        </div>
    );
}

// 正确做法：使用useCallback
const Child = React.memo(function Child({ onClick }) {
    return <button onClick={onClick}>点击</button>;
});

function Parent() {
    const [count, setCount] = useState(0);

    // 使用useCallback保持函数引用稳定
    const handleClick = useCallback(() => console.log('clicked'), []);

    return (
        <div>
            <span>{count}</span>
            <button onClick={() => setCount(c => c + 1)}>增加</button>
            <Child onClick={handleClick} />
        </div>
    );
}
```

---

### 38.2 列表性能优化

&emsp;&emsp;**（1）虚拟列表**
```jsx
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }) {
    const Row = ({ index, style }) => (
        <div style={style} className="list-item">
            <img src={items[index].avatar} alt="" />
            <span>{items[index].name}</span>
        </div>
    );

    return (
        <FixedSizeList
            height={400}
            itemCount={items.length}
            itemSize={50}
            width="100%"
        >
            {Row}
        </FixedSizeList>
    );
}

// 可变高度的虚拟列表
import { VariableSizeList } from 'react-window';

function VariableList({ items }) {
    const getItemSize = index => items[index].height || 50;

    const Row = ({ index, style }) => (
        <div style={style}>
            {items[index].content}
        </div>
    );

    return (
        <VariableSizeList
            height={400}
            itemCount={items.length}
            itemSize={getItemSize}
            width="100%"
        >
            {Row}
        </VariableSizeList>
    );
}
```

&emsp;&emsp;**（2）窗口化大列表技巧**
```jsx
// 使用react-window的AutoSizer和List组件
import { AutoSizer, List } from 'react-virtualized';

function AutoSizerList({ items }) {
    return (
        <AutoSizer>
            {({ height, width }) => (
                <List
                    height={height}
                    width={width}
                    itemCount={items.length}
                    itemSize={50}
                >
                    {({ index, style }) => (
                        <div style={style}>
                            {items[index].name}
                        </div>
                    )}
                </List>
            )}
        </AutoSizer>
    );
}
```

---

### 38.3 状态管理优化

&emsp;&emsp;**（1）状态位置优化**
```jsx
// 不好：将不必要的状态提升到父组件
function Parent() {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);

    return (
        <div>
            <Button onClick={() => setIsDropdownOpen(!isDropdownOpen)} />
            <Dropdown isOpen={isDropdownOpen} />
        </div>
    );
}

// 好：将状态保持在需要它的组件内
function Parent() {
    return (
        <div>
            <Button />
            <Dropdown />
        </div>
    );
}

function Dropdown() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
            <Button onClick={() => setIsOpen(!isOpen)} />
            {isOpen && <DropdownMenu />}
        </>
    );
}
```

&emsp;&emsp;**（2）派生状态优化**
```jsx
// 不必要的派生状态
function UserList() {
    const [users, setUsers] = useState([]);
    const [activeUsers, setActiveUsers] = useState([]); // 派生状态

    useEffect(() => {
        setActiveUsers(users.filter(u => u.isActive));
    }, [users]);

    // ...
}

// 好的做法：使用useMemo
function UserList() {
    const [users, setUsers] = useState([]);

    const activeUsers = useMemo(() => {
        return users.filter(u => u.isActive);
    }, [users]);

    // ...
}
```

---

---

## 面试冲刺篇

## 39、React高频面试题深度解答

### 39.1 组件相关面试题

&emsp;&emsp;**（1）React组件如何选择？类组件还是函数组件？**
&emsp;&emsp;**答案：** 现代React开发推荐使用函数组件+Hooks，原因如下：

```
+------------------+------------------------+------------------------+
|    维度          |      函数组件          |       类组件           |
+------------------+------------------------+------------------------+
| 代码量           | 更简洁                 | 需要继承、构造函数     |
| this问题         | 无this问题             | 需要bind处理          |
| 逻辑复用        | 自定义Hooks            | HOC、Render Props     |
| 状态管理        | useState              | setState              |
| 生命周期        | useEffect             | componentDidMount等   |
| 打包体积        | 更小                   | 需要继承React.Component|
| 未来发展        | 官方主推              | 保持兼容但不新增特性   |
+------------------+------------------------+------------------------+

推荐：所有新项目使用函数组件，类组件主要用于维护旧项目。
```

&emsp;&emsp;**（2）受控组件与非受控组件的区别？**
&emsp;&emsp;**答案：** 受控组件的状态由React控制，非受控组件状态由DOM自身控制。

```jsx
// 受控组件 - React完全控制状态
function ControlledInput() {
    const [value, setValue] = useState('');

    return (
        <input
            value={value}
            onChange={(e) => setValue(e.target.value)}
        />
    );
}

// 非受控组件 - 使用ref直接从DOM获取值
function UncontrolledInput() {
    const inputRef = useRef(null);

    const handleSubmit = () => {
        alert(`输入的值: ${inputRef.current.value}`);
    };

    return (
        <div>
            <input ref={inputRef} type="text" />
            <button onClick={handleSubmit}>提交</button>
        </div>
    );
}

// 选择建议：
// - 需要实时验证/格式化 -> 受控组件
// - 只是提交表单数据 -> 非受控组件（文件上传等）
// - 需要与其他库集成 -> 非受控组件
```

---

### 39.2 状态管理面试题

&emsp;&emsp;**（3）Redux的工作流程是什么？**
&emsp;&emsp;**答案：** Redux遵循单向数据流模式。

```
┌─────────────────────────────────────────────────────────────────┐
│                        Redux工作流程                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐    dispatch     ┌───────────┐    subscribe    ┌──────────┐
│   │ Component│ ──────────────→ │   Store   │ ──────────────→│ Component│
│   └──────────┘                 └───────────┘                └──────────┘
│        ↑                              │                           │
│        │                              │                           │
│        │       update          ┌──────┴───────┐                   │
│        └────────────────────── │    Reducer    │ ←───────────────┘
│                               └──────┬───────┘   读取state
│                                      │
│                               ┌──────┴───────┐
│                               │   Action     │
│                               │   (纯对象)   │
│                               └─────────────┘
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

步骤详解：
1. 用户交互触发 dispatch(action)
2. Store 调用 Reducer，传入当前state和action
3. Reducer返回新的state
4. Store通知所有订阅的组件
5. 组件重新渲染（使用新state）
```

&emsp;&emsp;**（4）Redux vs Context API vs Zustand，如何选择？**
&emsp;&emsp;**答案：** 根据应用规模和复杂度选择。

```
选择指南：
├── 小型应用（少量状态共享）
│   └── Context API 或 Zustand
│
├── 中型应用（较多状态，需要中间件）
│   └── Redux Toolkit 或 Zustand
│
└── 大型应用（复杂状态逻辑，多人协作）
    └── Redux Toolkit + RTK Query

Context API特点：
- 内置，无需安装
- 适合主题、国际化等全局配置
- 不适合频繁更新的状态（每次更新都会触发所有消费者）

Zustand特点：
- 轻量级（约1KB）
- 简单直观
- 无Provider包装
- 适合中小型项目

Redux Toolkit特点：
- 完整的开发工具支持
- 强大的中间件生态
- RTK Query处理服务端状态
- 适合大型复杂应用
```

---

### 39.3 性能优化面试题

&emsp;&emsp;**（5）React性能优化的方法有哪些？**
&emsp;&emsp;**答案：** 从多个层面进行优化。

```jsx
// 1. 组件层面优化
// 使用React.memo包装纯组件
const MemoizedComponent = React.memo(Component);

// 使用useMemo缓存计算结果
const expensiveValue = useMemo(() => {
    return computeExpensiveValue(a, b);
}, [a, b]);

// 使用useCallback缓存回调
const handleClick = useCallback(() => {
    doSomething(a, b);
}, [a, b]);

// 2. 列表优化
// 使用虚拟列表处理大数据
import { FixedSizeList } from 'react-window';

// 确保稳定的key
{items.map(item => (
    <ListItem key={item.id} {...item} />  // 用唯一ID，不用索引
))}

// 3. 代码分割
const LazyComponent = React.lazy(() => import('./Component'));
<Suspense fallback={<Loading />}><LazyComponent /></Suspense>

// 4. 状态优化
// 状态位置合理化
// 使用派生状态而非独立状态

// 5. 渲染优化
// 减少不必要的渲染
// 组件拆分
// 避免匿名函数和内联对象
```

&emsp;&emsp;**（6）useMemo和useCallback的区别和使用场景？**
&emsp;&emsp;**答案：** 它们都是为了避免不必要的计算或渲染。

```
+------------------+------------------------+------------------------+
|      Hook        |         作用           |       使用场景         |
+------------------+------------------------+------------------------+
|   useMemo        | 缓存计算结果           |  expensive calculation |
|                  |                        |  derived data          |
+------------------+------------------------+------------------------+
|   useCallback    | 缓存函数引用           |  作为props传递给       |
|                  |                        |  memoized组件          |
+------------------+------------------------+------------------------+

// useMemo示例
function SearchResults({ items, filter }) {
    // 只有items或filter变化时才重新过滤
    const filteredItems = useMemo(() => {
        return items.filter(item => item.name.includes(filter));
    }, [items, filter]);

    return <List items={filteredItems} />;
}

// useCallback示例
function Parent() {
    const [count, setCount] = useState(0);

    // 每次渲染都创建新函数
    const handleClick = () => console.log('click');

    // 只有count变化时才创建新函数
    const increment = useCallback(() => {
        setCount(c => c + 1);
    }, []);

    return (
        <div>
            <MemoizedChild onClick={handleClick} />
            <MemoizedCounter onIncrement={increment} />
        </div>
    );
}

// 使用建议：
// - 不要过早优化，先Profile找到瓶颈
// - useMemo/useCallback本身也有开销
// - 简单值和函数可能不需要缓存
```

---

### 39.4 原理相关面试题

&emsp;&emsp;**（7）setState是同步还是异步的？**
&emsp;&emsp;**答案：** 在React 18中，所有setState都是异步批处理的。

```jsx
// React 18之前
// React事件处理中：异步
// setTimeout/Promise/原生事件：同步

// React 18之后
// 所有更新都自动批处理（异步）

function App() {
    const [count, setCount] = useState(0);
    const [name, setName] = useState('');

    const handleClick = () => {
        setCount(1);
        setName('Alice');
        console.log(count); // 仍然是0，不是1
        // 但会触发一次重渲染，count和name都更新
    };

    // 如果需要立即看到更新后的值
    const handleClickWithCallback = () => {
        setCount(1);
        setName('Alice', () => {
            console.log('更新完成'); // 回调中可获取最新值
        });
    };

    // 或者使用flushSync强制同步
    import { flushSync } from 'react-dom';

    const handleClickSync = () => {
        flushSync(() => setCount(1));
        console.log(count); // 1
        flushSync(() => setName('Alice'));
    };
}
```

&emsp;&emsp;**（8）React的调和（Reconciliation）和渲染（Render）有什么区别？**
&emsp;&emsp;**答案：** 调和是计算差异的过程，渲染是应用差异的过程。

```
┌─────────────────────────────────────────────────────────────────┐
│                        React更新流程                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   State Change ──→ Re-render Component ──→ Render Phase           │
│       │                                         │               │
│       │                                    ┌────┴────┐          │
│       │                                    │         │          │
│       │                              Virtual DOM    Fiber        │
│       │                              Diffing      Tree          │
│       │                                    │         │          │
│       │                              ┌─────┴─────────┘          │
│       │                              │                         │
│       │                         Reconcile                    │
│       │                              │                         │
│       │                              ↓                         │
│       │                         Commit Phase                   │
│       │                              │                         │
│       │                         DOM Updates                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Reconciliation（调和）：
- 虚拟DOM层面的diff算法
- 确定哪些部分需要更新
- 可中断（Fiber架构）

Render（渲染）：
- 实际DOM操作
- 必须同步完成
- 浏览器绘制
```

&emsp;&emsp;**（9）什么是Time Slicing（时间切片）？**
&emsp;&emsp;**答案：** 时间切片是React将渲染工作分解成小单元的机制。

```jsx
// 概念说明
// React将长时间运行的渲染任务分解成小片
// 每个小片执行完后，让出主线程给浏览器
// 这样用户交互可以及时响应

// React 18之前
// 如果有10000个列表项要渲染
// 渲染过程会阻塞主线程，用户无法点击按钮

// React 18+
import { useTransition } from 'react';

function BigList() {
    const [isPending, startTransition] = useTransition();

    const [items, setItems] = useState([]);

    const handleFilter = (filter) => {
        startTransition(() => {
            // 这个更新会被分解成小片执行
            setItems(filterItems(filter));
        });
    };

    return (
        <div>
            <input onChange={(e) => handleFilter(e.target.value)} />
            {isPending ? <Spinner /> : <List items={items} />}
        </div>
    );
}

// 工作原理
function workLoop(deadline) {
    while (nextUnitOfWork && deadline.timeRemaining() > 0) {
        // 执行一个Fiber节点的工作
        nextUnitOfWork = performUnitOfWork(nextUnitOfWork);

        if (shouldYield()) {
            // 时间片用完，让出控制权
            requestIdleCallback(workLoop);
            break;
        }
    }
}
```

---

### 39.5 Hooks相关面试题

&emsp;&emsp;**（10）为什么Hooks不能在条件语句中使用？**
&emsp;&emsp;**答案：** Hooks依赖调用顺序来维护state和dispatch。

```jsx
// 错误的写法
function App() {
    const [name, setName] = useState('Alice');

    if (condition) {
        const [age, setAge] = useState(25); // 错误：条件语句中调用Hooks
    }

    const [color, setColor] = useState('blue');
}

// 第一次渲染（condition=false）：
// useState('Alice') -> state[0]
// useState('blue')  -> state[1]

// 第二次渲染（condition=true）：
// useState('Alice') -> state[0]
// useState(25)      -> state[1]  ← 顺序错乱！
// useState('blue')  -> state[2]  ← 无法执行
```

&emsp;&emsp;**（11）useEffect的依赖数组为空和没有依赖数组有什么区别？**
&emsp;&emsp;**答案：** 空数组只在挂载时执行一次，没有依赖数组则在每次渲染后都执行。

```jsx
function Example() {
    // 1. 空依赖数组 - 只在挂载和卸载时执行
    useEffect(() => {
        console.log('只执行一次（挂载时）');
        return () => console.log('卸载时清理');
    }, []);

    // 2. 没有依赖数组 - 每次渲染都执行
    useEffect(() => {
        console.log('每次渲染都执行');
    });

    // 3. 有依赖数组 - 依赖变化时执行
    useEffect(() => {
        console.log('count变化时执行');
    }, [count]);
}

// 实际场景选择：
// - 发起请求、添加订阅 -> []（挂载时）
// - 每次渲染都要执行 -> 不加数组
// - 特定值变化时执行 -> 添加依赖
```

&emsp;&emsp;**（12）自定义Hooks有哪些实际应用场景？**
&emsp;&emsp;**答案：** 自定义Hooks用于逻辑复用，适合提取可复用的状态逻辑。

```
常见自定义Hooks场景：
├── 数据获取
│   └── useFetch, useAsync, useSWR
│
├── 浏览器API
│   └── useLocalStorage, useMediaQuery, useGeolocation
│
├── 表单处理
│   └── useForm, useInput, useValidation
│
├── 性能优化
│   └── useDebounce, useThrottle, useClickOutside
│
├── 状态管理
│   └── useToggle, useArray, usePrevious
│
└── 动画/交互
    └── useIntersectionObserver, useDrag, useSwipe
```

---

### 39.6 框架相关面试题

&emsp;&emsp;**（13）React与Vue的区别？**
&emsp;&emsp;**答案：** 两者都是优秀的前端框架，有各自的设计理念。

```
+------------------+------------------------+------------------------+
|      维度        |        React          |        Vue            |
+------------------+------------------------+------------------------+
| 模板语法         | JSX（JS扩展）         | 单文件组件（HTML模板）|
| 状态管理         | Context/Redux          | Vuex/Pinia            |
| 数据绑定         | 单向数据流            | 双向绑定可选          |
| 响应式原理       | 手动setState触发更新  | Proxy/Object.define   |
| 生态             | 更灵活，更多选择      | 更统一，官方推荐      |
| 学习曲线         | JSX需要学习           | 模板语法更直观        |
| 社区             | 更大，更活跃          | 增长迅速              |
| 类型支持         | TypeScript原生        | 需配置                |
| 包体积           | 较小                  | 稍大                  |
+------------------+------------------------+------------------------+

共同点：
- 组件化思想
- 虚拟DOM
- 单向数据流
- 路由管理
- 生态丰富
```

&emsp;&emsp;**（14）Next.js相比纯React有哪些优势？**
&emsp;&emsp;**答案：** Next.js提供了服务端渲染、路由系统等企业级功能。

```
Next.js核心优势：
├── 服务端渲染(SSR)
│   └── SEO友好，首屏加载快
│
├── 静态站点生成(SSG)
│   └── 预渲染页面，性能最佳
│
├── API Routes
│   └── 前后端一体化
│
├── 自动代码分割
│   └── 路由级别自动分割
│
├── 图片优化
│   └── <Image>自动优化
│
└── 文件系统路由
    └── pages目录自动生成路由
```

---

### 39.7 实战相关面试题

&emsp;&emsp;**（15）如何实现一个React计数器组件？**
&emsp;&emsp;**答案：** 提供多种实现方式。

```jsx
// 方式1：函数组件 + useState（推荐）
function Counter() {
    const [count, setCount] = useState(0);

    return (
        <div>
            <p>计数: {count}</p>
            <button onClick={() => setCount(c => c + 1)}>+</button>
            <button onClick={() => setCount(c => c - 1)}>-</button>
            <button onClick={() => setCount(0)}>重置</button>
        </div>
    );
}

// 方式2：类组件
class Counter extends React.Component {
    state = { count: 0 };

    increment = () => this.setState({ count: this.state.count + 1 });
    decrement = () => this.setState({ count: this.state.count - 1 });
    reset = () => this.setState({ count: 0 });

    render() {
        return (
            <div>
                <p>计数: {this.state.count}</p>
                <button onClick={this.increment}>+</button>
                <button onClick={this.decrement}>-</button>
                <button onClick={this.reset}>重置</button>
            </div>
        );
    }
}

// 方式3：useReducer（复杂状态）
function counterReducer(state, action) {
    switch (action.type) {
        case 'INCREMENT': return { count: state.count + 1 };
        case 'DECREMENT': return { count: state.count - 1 };
        case 'RESET': return { count: 0 };
        default: return state;
    }
}

function Counter() {
    const [state, dispatch] = useReducer(counterReducer, { count: 0 });

    return (
        <div>
            <p>计数: {state.count}</p>
            <button onClick={() => dispatch({ type: 'INCREMENT' })}>+</button>
            <button onClick={() => dispatch({ type: 'DECREMENT' })}>-</button>
            <button onClick={() => dispatch({ type: 'RESET' })}>重置</button>
        </div>
    );
}
```

&emsp;&emsp;**（16）React如何实现一个Todo List？**
&emsp;&emsp;**答案：** 综合展示React核心概念。

```jsx
// 完整Todo List实现
import React, { useState, useEffect } from 'react';

function TodoApp() {
    const [todos, setTodos] = useState([]);
    const [input, setInput] = useState('');
    const [filter, setFilter] = useState('all');

    // 持久化
    useEffect(() => {
        const saved = localStorage.getItem('todos');
        if (saved) setTodos(JSON.parse(saved));
    }, []);

    useEffect(() => {
        localStorage.setItem('todos', JSON.stringify(todos));
    }, [todos]);

    // 添加
    const addTodo = () => {
        if (!input.trim()) return;
        setTodos([...todos, {
            id: Date.now(),
            text: input.trim(),
            completed: false
        }]);
        setInput('');
    };

    // 切换完成状态
    const toggleTodo = (id) => {
        setTodos(todos.map(t =>
            t.id === id ? { ...t, completed: !t.completed } : t
        ));
    };

    // 删除
    const deleteTodo = (id) => {
        setTodos(todos.filter(t => t.id !== id));
    };

    // 筛选
    const filteredTodos = todos.filter(t => {
        if (filter === 'active') return !t.completed;
        if (filter === 'completed') return t.completed;
        return true;
    });

    const activeCount = todos.filter(t => !t.completed).length;

    return (
        <div className="todo-app">
            <h1>Todo List</h1>

            <div className="input-row">
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && addTodo()}
                    placeholder="添加新任务..."
                />
                <button onClick={addTodo}>添加</button>
            </div>

            <div className="filter-row">
                {['all', 'active', 'completed'].map(f => (
                    <button
                        key={f}
                        className={filter === f ? 'active' : ''}
                        onClick={() => setFilter(f)}
                    >
                        {f}
                    </button>
                ))}
            </div>

            <ul>
                {filteredTodos.map(todo => (
                    <li key={todo.id} className={todo.completed ? 'completed' : ''}>
                        <input
                            type="checkbox"
                            checked={todo.completed}
                            onChange={() => toggleTodo(todo.id)}
                        />
                        <span>{todo.text}</span>
                        <button onClick={() => deleteTodo(todo.id)}>删除</button>
                    </li>
                ))}
            </ul>

            <p>剩余 {activeCount} 项未完成</p>
        </div>
    );
}

export default TodoApp;
```

---

### 39.8 进阶面试题

&emsp;&emsp;**（17）React的设计模式有哪些？**
&emsp;&emsp;**答案：** 了解设计模式有助于构建可维护的React应用。

```
常见React设计模式：
├── Compound Components（复合组件）
│   └── 多个组件协作，共享隐式状态
│   └── 示例：<Select><Option/></Select>
│
├── Render Props
│   └── 将渲染逻辑提取到prop中
│   └── 示例：<MouseTracker render={pos => <Cat pos={pos}/>}/>
│
├── HOC (Higher Order Components)
│   └── 接收组件返回增强后的组件
│   └── 示例：withAuthentication(UserProfile)
│
├── Custom Hooks
│   └── 提取可复用的状态逻辑
│   └── 示例：useDebounce, useFetch
│
├── Container/Presentational（容器/展示组件）
│   └── 分离数据逻辑和UI逻辑
│
└── Provider Pattern
    └── 使用Context共享全局状态
```

&emsp;&emsp;**（18）React的严格模式（StrictMode）有什么作用？**
&emsp;&emsp;**答案：** 帮助发现潜在问题的开发工具。

```jsx
// React StrictMode会：
// 1. 双重调用effect（开发环境）
// 2. 重新调用组件渲染
// 3. 检测不安全的生命周期
// 4. 检测意外副作用

// 示例：发现问题
function EffectExample() {
    useEffect(() => {
        console.log('Effect执行');
        const timer = setInterval(() => {
            console.log('定时器');
        }, 1000);

        return () => clearInterval(timer); // 如果忘记清理，会发现问题
    }, []);

    return <div>检查控制台</div>;
}

// 使用StrictMode
function App() {
    return (
        <React.StrictMode>
            <EffectExample />
        </React.StrictMode>
    );
}

// 开发环境输出：
// Effect执行
// Effect执行    <- 第二次调用帮助发现问题
// 定时器
// 定时器
// ...
// React会帮你检测出没有cleanup的问题
```

---

## 附录：React生态常用工具

&emsp;&emsp;**（1）开发工具**
```
┌─────────────────────────────────────────────────────────────────┐
│                         开发工具                                │
├─────────────────────────────────────────────────────────────────┤
│ Vite        │ 极快的开发服务器和构建工具（推荐）                  │
│ Next.js     │ 服务端渲染（SSR）和静态站点生成（SSG）框架          │
│ Remix       │ 全栈React框架，支持嵌套路由                         │
│ create-react-app │ 官方脚手架（已不推荐新项目使用）              │
│ Tauri       │ 使用Rust构建的轻量级桌面应用                       │
└─────────────────────────────────────────────────────────────────┘
```

&emsp;&emsp;**（2）UI组件库**
```
┌─────────────────────────────────────────────────────────────────┐
│                        UI组件库                                 │
├─────────────────────────────────────────────────────────────────┤
│ Ant Design  │ 蚂蚁金服企业级组件库，中文社区活跃                  │
│ Material UI │ Google Material Design风格                         │
│ Chakra UI   │ 可访问性优先，易于定制                             │
│ Radix UI    │ 无样式、accessible的UI原语                         │
│ Headless UI │ Tailwind CSS团队的无样式组件                       │
│ shadcn/ui   │ 可复制粘贴的组件集合，基于Radix和Tailwind          │
└─────────────────────────────────────────────────────────────────┘
```

&emsp;&emsp;**（3）状态管理**
```
┌─────────────────────────────────────────────────────────────────┐
│                       状态管理库                                 │
├─────────────────────────────────────────────────────────────────┤
│ Redux Toolkit │ Redux官方推荐，现代化Redux开发方式                │
│ Zustand       │ 轻量级（约1KB），简单直观                       │
│ Jotai         │ 原子化状态管理，TypeScript友好                    │
│ Valtio        │ 响应式状态管理，类似MobX                         │
│ React Query   │ 服务端状态管理，数据获取和缓存                   │
│ SWR           │ Vercel出品的远程数据Hook                        │
└─────────────────────────────────────────────────────────────────┘
```

&emsp;&emsp;**（4）样式解决方案**
```
┌─────────────────────────────────────────────────────────────────┐
│                      样式解决方案                               │
├─────────────────────────────────────────────────────────────────┤
│ Tailwind CSS  │ 原子化CSS，实用优先（推荐）                      │
│ CSS Modules   │ CSS文件级作用域，原生支持                        │
│ Styled Comps  │ CSS-in-JS，组件级样式隔离                       │
│ Emotion       │ 性能更好的CSS-in-JS                             │
│ Panda CSS     │ 新型原子化CSS，类型安全                          │
│ UnoCSS       │ 即时原子化CSS引擎                                │
└─────────────────────────────────────────────────────────────────┘
```

&emsp;&emsp;**（5）路由**
```
┌─────────────────────────────────────────────────────────────────┐
│                        路由库                                   │
├─────────────────────────────────────────────────────────────────┤
│ React Router  │ React官方路由库，v6功能强大                       │
│ TanStack Router │ 现代化路由，全类型安全                         │
│ Wouter        │ 轻量级路由（约1.5KB）                           │
└─────────────────────────────────────────────────────────────────┘
```

&emsp;&emsp;**（6）表单处理**
```
┌─────────────────────────────────────────────────────────────────┐
│                        表单库                                   │
├─────────────────────────────────────────────────────────────────┤
│ React Hook Form │ 高性能表单，性能优先（推荐）                    │
│ Formik         │ 传统表单库，社区成熟                            │
│ React Final Form │ 高性能表单，订阅模式                         │
│ Zod            │ 数据验证，通常配合表单库使用                    │
└─────────────────────────────────────────────────────────────────┘
```

&emsp;&emsp;**（7）动画**
```
┌─────────────────────────────────────────────────────────────────┐
│                        动画库                                   │
├─────────────────────────────────────────────────────────────────┤
│ Framer Motion │ 功能强大，声明式动画（推荐）                     │
│ React Spring  │ 物理弹簧动画，自然流畅                          │
│ AutoAnimate   │ 无需代码的动画，auto-animate                    │
│ Motion One    │ 轻量级动画库，Performance优先                   │
└─────────────────────────────────────────────────────────────────┘
```

&emsp;&emsp;**（8）测试**
```
┌─────────────────────────────────────────────────────────────────┐
│                        测试工具                                 │
├─────────────────────────────────────────────────────────────────┤
│ Vitest        │ Vite原生单元测试（推荐）                        │
│ Jest          │ 传统单元测试，广泛使用                          │
│ Testing Library │ 组件行为测试，用户导向                        │
│ Playwright    │ 端到端测试，现代浏览器支持                      │
│ Cypress       │ E2E测试，开发者友好                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 学习资源推荐

```
┌─────────────────────────────────────────────────────────────────┐
│                      官方文档                                   │
├─────────────────────────────────────────────────────────────────┤
│ React官方文档     │ https://react.dev（最新）                   │
│ React旧文档       │ https://reactjs.org                         │
│ React Router文档  │ https://reactrouter.com                     │
│ Redux Toolkit文档 │ https://redux-toolkit.js.org                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      视频课程                                   │
├─────────────────────────────────────────────────────────────────┤
│ React官方教程     │ 交互式学习React基础                         │
│ B站React课程      │ 中文视频教程丰富                            │
│ Frontend Masters  │ 英文高质量课程                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      社区资源                                   │
├─────────────────────────────────────────────────────────────────┤
│ Reactiflux Discord│ 最大的React社区                            │
│ Dev.to React标签   │ 技术文章平台                               │
│ 掘金React标签     │ 中文技术社区                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 面试准备建议

```
┌─────────────────────────────────────────────────────────────────┐
│                     面试准备 Checklist                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ 【基础必备】⭐⭐⭐⭐⭐                                          │
│ □ JSX语法和渲染原理                                             │
│ □ State vs Props的区别和使用场景                                 │
│ □ 事件处理机制                                                  │
│ □ 条件渲染和列表渲染                                             │
│ □ 组件通讯方式（父子、兄弟、Context）                            │
│                                                                  │
│ 【Hooks核心】⭐⭐⭐⭐⭐                                          │
│ □ useState和useEffect的用法和执行时机                           │
│ □ useRef的使用场景                                               │
│ □ useMemo和useCallback的区别                                    │
│ □ useContext的原理                                               │
│ □ useReducer适用场景                                             │
│                                                                  │
│ 【进阶知识】⭐⭐⭐⭐                                            │
│ □ React.memo和PureComponent                                     │
│ □ 高阶组件（HOC）和Render Props                                  │
│ □ 错误边界的使用                                                 │
│ □ 虚拟DOM和Diff算法                                              │
│ □ Fiber架构基本概念                                              │
│                                                                  │
│ 【状态管理】⭐⭐⭐⭐                                            │
│ □ Redux工作流程                                                  │
│ □ Redux Toolkit用法                                              │
│ □ Context API适用场景                                            │
│ □ Zustand/Jotai等轻量方案                                       │
│                                                                  │
│ 【路由与生态】⭐⭐⭐                                            │
│ □ React Router v6核心用法                                        │
│ □ 路由守卫实现                                                   │
│ □ TypeScript配合React                                            │
│                                                                  │
│ 【性能优化】⭐⭐⭐                                              │
│ □ React.memo/useCallback/useMemo                                │
│ □ 代码分割和懒加载                                               │
│ □ 列表虚拟化                                                    │
│ □ 避免不必要的渲染                                              │
│                                                                  │
│ 【React 18】⭐⭐⭐                                              │
│ □ 并发渲染概念                                                   │
│ □ startTransition和useDeferredValue                             │
│ □ Automatic Batching                                            │
│ □ Suspense改进                                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```
