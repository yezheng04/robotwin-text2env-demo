# 编排摆放生成流程

当需要把 Designer 输出、Critic review 和 validation result 合并成下一步 pipeline artifact 时使用这个 skill。在 agent 流程中，它对应 Orchestrator 能力。

## 规则

- 如果 Critic reject，停止并输出 blocked decision。
- 如果需要 repair，输出具体修复指令。
- 如果通过，写出 stage 为 `final_static_for_smoke` 的最终 `robotwin.tabletop_placement.v0` artifact。
- 保留有效的 object id、asset id、model id 和 pose。
- 把 simulator 和 render 检查项带入 validation plan。
- 没有实际看过 RoboTwin preview evidence 前，不要声称已经完成 visual verification。

## 输出

返回 final placement JSON 和 validation plan。
