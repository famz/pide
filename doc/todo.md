# TODO

## Turtle 显示与体验
- [x] 在 `TurtleCanvas` 绘制海龟方向指示（小三角），基于 `turtle_update`。
- [x] 实现 `stamp` 指令的渲染。
- [x] 支持 `speed(1–10)` 的节奏控制（后端按档位 sleep，动画可见可控）。

## IDE 细节
- [x] 稳健解析 stdout（按行缓冲，仅整行 `__PIDE_TURTLE__:` 作命令，其余给终端）。
- [x] 运行中断时清空画布并重置 stdout 缓冲。

## 工程与文档
- [x] README：最小 turtle 示例 + demo/ 与 learn/ 目录说明。
- [ ] 可选：在 README 里补一张界面截图。
