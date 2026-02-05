# Pide — Python 学习环境

现代版 Python 学习环境，替代 Thonny，面向初学者（含儿童）的跨平台单窗口 IDE。

## 目标

- **跨平台**：支持 macOS、Linux（含儿童使用的 Linux 笔记本），后续可考虑 Windows。
- **单窗口**：所有功能集中在一个主窗口，布局清晰。
- **便携**：选用可在各平台一致运行、易于打包/便携分发的 GUI 框架。

## 界面布局（单窗口）

```
┌─────────────────────────────────────────────────────────────────────────┐
│  [ 标题栏 / 菜单 ]                                                        │
├──────────────┬─────────────────────────────┬────────────────────────────┤
│              │                             │                            │
│   Sidebar    │   Editor                    │   Output / 渲染窗          │
│   (左侧)     │   (中间上)                   │   (右侧)                   │
│              ├─────────────────────────────┤                            │
│   代码列表   │   Terminal                  │   PyTurtle / Pygame        │
│   文件树     │   (中间下)                   │   图形输出                  │
│              │                             │                            │
└──────────────┴─────────────────────────────┴────────────────────────────┘
```

- **左侧 (Sidebar)**：代码/文件列表，方便切换多个脚本。
- **中间**：上方为代码编辑区，下方为内置终端，上下堆叠（可调高度）。
- **右侧**：图形输出窗口，支持 **PyTurtle** 或 **Pygame** 的渲染（画布/游戏窗口）。

## 功能需求概要

| 区域       | 功能说明 |
|------------|----------|
| Sidebar    | 文件树或脚本列表；新建/打开/保存/重命名；当前打开文件高亮 |
| Editor     | 语法高亮、行号、基础编辑；运行当前脚本（可配置 Python 解释器） |
| Terminal   | 内置终端，用于 `print`、`input`、错误信息等；与「运行」联动 |
| 右侧渲染窗 | 运行 PyTurtle/Pygame 时在此显示图形窗口，不弹出独立窗口 |

## 技术选型（待定）

- **GUI 框架**：需满足
  - 跨平台（至少 macOS + Linux）
  - 可做成 portable（单目录/单包分发，少依赖系统）
  - 支持：侧边栏、多区域布局、内嵌编辑、内嵌终端、内嵌/对接子进程绘图窗口
- **候选**：如 PyQt/PySide、Tkinter、wxPython、Dear PyGui 等，待评估后选定。
- **编辑组件**：可用现成组件（如 QScintilla、tk 文本框 + 高亮）或轻量嵌入式方案。
- **终端**：框架内终端组件或 `pty` + 自家渲染。
- **PyTurtle/Pygame**：以子进程运行用户脚本，通过管道或 socket 将绘图/窗口嵌入右侧区域，或使用无头/离屏渲染再贴到 GUI（具体方案待定）。

## 安装与运行

### 快速开始（推荐）

**一键运行，自动安装所有依赖：**

```bash
# 克隆仓库
git clone <repository-url>
cd pide

# 直接运行（会自动检测系统并安装依赖）
make run

# 或者使用脚本
./run-pide
```

首次运行时会自动：
- ✅ 检测操作系统（macOS/Linux）
- ✅ 检测 Linux 发行版（Ubuntu/Debian/Fedora/Arch 等）
- ✅ 自动安装系统依赖（需要 sudo 权限）
- ✅ 自动安装 Python 依赖（PySide6 等）

### 手动安装（可选）

如果需要手动控制安装过程：

```bash
# 运行安装脚本
./setup.sh

# 或者使用 Makefile
make setup
```

### Linux 系统依赖

脚本会自动安装，但如果你想手动安装：

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv libxcb-xinerama0 libxcb-cursor0 libxcb-xfixes0
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-pip python3-devel libxcb xcb-util xcb-util-image
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip libxcb
```

### 使用 uv（可选，更快）

如果安装了 `uv`（快速 Python 包管理器），安装会更快：

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 然后正常运行即可
make run
```

## 当前阶段

- [x] 需求与愿景整理（本文档）
- [x] 选定 GUI 框架与技术栈（PySide6）
- [x] 搭建最小单窗口布局（Sidebar + Editor + Terminal + 右侧占位）
- [x] 实现编辑与运行、终端联动
- [x] 语法高亮和智能缩进
- [x] 实现右侧 PyTurtle 渲染窗（海龟方向、速度、stamp、与 print 混用稳健解析；运行中断时清空画布）

## 代码目录（code/）

- **demo/**：内置示例（hello、猜数字、计算器、FizzBuzz），首次运行自动生成。
- **turtle/**：Turtle 示例（星星、螺旋、花、树、同心圆、彩虹等），首次运行自动生成。
- **learn/**：课程或练习脚本，按需放置。

运行带 `import turtle` 的脚本时，图形在右侧窗口内嵌显示，无需弹窗。

最小示例：

```python
import turtle
t = turtle.Turtle()
t.speed(3)
t.forward(100)
t.left(90)
t.forward(50)
turtle.done()
```

## 命名

**Pide**：Python IDE for (learning / education)，简短、好记，便于在 Linux 上敲命令（如 `pide`）。

---

*先从这里开始；下一步建议确定 GUI 框架并搭一个可运行的单窗口骨架。*
