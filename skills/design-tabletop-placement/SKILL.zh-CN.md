# 设计桌面级物体摆放

当需要把自然语言桌面场景描述转换成初始 `TabletopPlacementSpec` 时使用这个 skill。在 agent 流程中，它对应 Designer 能力。

## 输入

- placement prompt。
- asset catalog JSON。
- 桌面 workspace bounds。
- 可选的下游机器人任务提示。

## 规则

- 只能选择 catalog 中真实存在的资产。
- 不要编造 asset id、model id、路径、affordance 或任务代码。
- 把 left、right、near、on、inside、separated 等空间语义转换成明确桌面 pose 或 region。
- 每个物体都必须在 workspace bounds 内。
- 除非 prompt 明确要求接触、堆叠或放入容器，否则优先使用简单、稳定、分离的桌面摆放。
- simulator、render、visual checks 在 smoke evidence 出现前都标记为 pending。

## 输出

返回严格 JSON，格式遵循 `robotwin.tabletop_placement.v0`。
