---
name: computer-use
description: "电脑操控技能。让AI像人一样操控电脑：看屏幕、点鼠标、打字、操作软件。适用于：操作桌面软件（没有API的系统）、自动填写表单、点击按钮、多窗口操作、截屏查看界面。"
dependencies: "pip install pyautogui mss pillow pygetwindow pyperclip"
---

# Computer Use - 电脑操控技能

让小咪像人一样操控电脑：看屏幕、点鼠标、打字、操作软件。

---

## 依赖安装

使用前需安装 Python 依赖：
```bash
pip install pyautogui mss pillow pygetwindow pyperclip
```

---

## When to Use

**当以下情况时使用此 Skill：**

- 需要操作桌面软件（没有 API 的系统）
- 需要自动填写表单、点击按钮
- 需要在多个窗口/应用间操作
- 用户提到"操作电脑"、"帮我点"、"帮我操作"、"自动化"、"Computer Use"
- 需要截屏查看当前界面

---

## 三层架构（优先级从高到低）

| 层级 | 方式 | 速度 | 成本 | 适用场景 |
|------|------|------|------|---------|
| **L1** | UI Automation | ⚡极快 | 免费 | Windows 原生应用、标准控件 |
| **L2** | 截图 + AI 视觉 | 🐢较慢 | 消耗token | 复杂界面、非标准控件 |
| **L3** | OCR + 文本分析 | ⚡快 | 低 | 纯文字识别场景 |

**原则：能用 L1 就不用 L2，90% 的操作 L1 就够了。**

---

## 工作流程

### 标准操作循环

```
1. 获取界面信息（UI Tree 或 截图）
2. 分析界面，理解当前状态
3. 决定下一步操作
4. 执行操作（点击/输入/快捷键）
5. 等待响应
6. 再次获取界面信息，确认结果
7. 循环直到任务完成
```

### 步骤详解

#### Step 1: 获取界面信息

**方式 A: UI Automation（首选）**
```bash
python ~/.openclaw/skills/computer-use/scripts/ui_tree.py
```
输出：当前窗口所有可交互元素的列表（名称、类型、坐标）

**方式 B: 截图 + AI 分析（备选）**
```bash
python ~/.openclaw/skills/computer-use/scripts/screenshot.py 0.5
```
然后用 `image` 工具分析截图：
```
image(image="~/tmp/screenshot.png", prompt="描述这个界面上有哪些可交互元素")
```

#### Step 2: 执行操作

```bash
# 点击
python ~/.openclaw/skills/computer-use/scripts/action.py "{\"type\":\"click\",\"x\":500,\"y\":300}"

# 双击
python ~/.openclaw/skills/computer-use/scripts/action.py "{\"type\":\"double_click\",\"x\":500,\"y\":300}"

# 输入文字
python ~/.openclaw/skills/computer-use/scripts/action.py "{\"type\":\"type\",\"text\":\"Hello World\"}"

# 快捷键
python ~/.openclaw/skills/computer-use/scripts/action.py "{\"type\":\"hotkey\",\"keys\":[\"ctrl\",\"c\"]}"

# 按键
python ~/.openclaw/skills/computer-use/scripts/action.py "{\"type\":\"press\",\"key\":\"enter\"}"

# 滚动
python ~/.openclaw/skills/computer-use/scripts/action.py "{\"type\":\"scroll\",\"amount\":-3}"

# 拖拽
python ~/.openclaw/skills/computer-use/scripts/action.py "{\"type\":\"drag\",\"start_x\":100,\"start_y\":200,\"end_x\":300,\"end_y\":400}"

# 等待
python ~/.openclaw/skills/computer-use/scripts/action.py "{\"type\":\"wait\",\"seconds\":2}"
```

#### Step 3: 确认结果

再次运行 ui_tree.py 或 screenshot.py 确认操作是否成功。

---

## 支持的操作类型

| 操作 | type | 必需参数 | 可选参数 |
|------|------|---------|---------|
| 点击 | `click` | x, y | button(left/right), clicks |
| 双击 | `double_click` | x, y | - |
| 右键 | `right_click` | x, y | - |
| 移动鼠标 | `move` | x, y | - |
| 输入文字 | `type` | text | interval |
| 快捷键 | `hotkey` | keys[] | - |
| 按键 | `press` | key | - |
| 滚动 | `scroll` | amount | x, y |
| 拖拽 | `drag` | start_x, start_y, end_x, end_y | duration |
| 等待 | `wait` | seconds | - |

---

## 安全规则（必须遵守）

1. **确认再操作** — 执行前先描述将要做什么，等用户确认
2. **避免破坏性操作** — 删除文件、格式化、关闭未保存文档前必须确认
3. **不操作敏感页面** — 支付、银行、密码管理器等页面不自动操作
4. **紧急停止** — 鼠标移到屏幕左上角可紧急停止所有操作
5. **操作间隔** — 每次操作间隔 0.3 秒，防止过快
6. **失败重试上限** — 同一操作最多重试 3 次

---

## 脚本位置

```
~/.openclaw/skills/computer-use/
├── SKILL.md              # 本文件
└── scripts/
    ├── screenshot.py     # 屏幕截图
    ├── action.py         # 操作执行
    └── ui_tree.py        # UI 元素树获取
```

## 依赖

```bash
# Linux/Mac
pip install pyautogui mss pillow

# Windows（需要 pyperclip 支持中文输入）
pip install pyautogui mss pillow pygetwindow pyperclip
```

---

## 示例场景

### 场景 1: "帮我打开记事本写点东西"

```
1. exec: 启动记事本 → start notepad
2. wait: 等待窗口出现
3. ui_tree: 获取记事本窗口元素
4. action: 点击编辑区域
5. action: 输入文字
6. action: Ctrl+S 保存
```

### 场景 2: "帮我在浏览器里搜索xxx"

```
1. ui_tree: 获取浏览器窗口
2. action: 点击地址栏
3. action: 输入搜索内容
4. action: 按回车
5. screenshot: 截图确认结果
```

### 场景 3: "帮我操作这个软件"

```
1. screenshot: 先截图看看当前界面
2. image: 分析界面布局
3. 根据分析结果决定操作
4. action: 执行操作
5. screenshot: 确认结果
```

---

## Source

自研技能，灵感来自 Anthropic Claude Computer Use
