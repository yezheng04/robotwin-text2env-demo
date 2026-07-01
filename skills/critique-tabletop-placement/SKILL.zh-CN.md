# 评估桌面级物体摆放

当需要评估 Designer 生成的 `TabletopPlacementSpec` 时使用这个 skill。在 agent 流程中，它对应 Critic 能力。

## 范围

只检查场景构建质量：

- prompt 和物体语义是否匹配。
- asset 和 model 是否存在。
- pose 是否在 workspace bounds 内。
- 是否有近似碰撞风险。
- 稳定性 metadata 是否合理。
- 机器人可达性和相机可见性风险。
- 这个场景是否能支持后续机器人任务。

不要评价 policy training、数据采集质量或任务 success predicate。

## 输出

返回严格 JSON，使用 `robotwin.tabletop_placement_critic.v0`，verdict 为 `accept_for_next_stage`、`repair_required` 或 `reject`。
