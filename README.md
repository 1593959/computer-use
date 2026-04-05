# Computer Use - 电脑操控技能

让 AI 像人一样操控电脑：看屏幕、点鼠标、打字、操作软件。

## 功能特性

- 🖱️ **鼠标操作** - 点击、双击、右键、拖拽
- ⌨️ **键盘输入** - 输入文字、快捷键
- 🎡 **滚动操作** - 上下滚动页面
- 📸 **截图分析** - 截取当前界面进行分析
- 🌲 **UI 树解析** - 获取窗口和界面元素结构

## 支持平台

- Windows
- macOS（部分功能）

## 安装依赖

```bash
pip install pyautogui mss pillow pygetwindow pyperclip
```

## 目录结构

```
computer-use/
├── SKILL.md              # 技能说明文档
├── scripts/
│   ├── action.py         # 核心操作模块
│   ├── screenshot.py     # 截图模块
│   └── ui_tree.py        # UI 树解析
└── README.md
```

## 使用方式

当需要操作桌面软件、自动填写表单、点击按钮时，激活此技能。

## 相关项目

- [openclawmp](https://openclawmp.stepfun.com) - Agent 技能市场

## License

MIT
