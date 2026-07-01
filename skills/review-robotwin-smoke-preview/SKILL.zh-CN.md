# 审查 RoboTwin Smoke Preview

当需要检查 placement run 产生的 RoboTwin smoke 输出时使用这个 skill。Smoke success 只说明 RoboTwin 能加载并渲染场景，不等于这个场景视觉上正确。

## 检查项

- `smoke_report.json` 存在且结果为 pass。
- `head_camera.png` 和 `observer_camera.png` 存在。
- 可选的 `observer_camera.mp4` 存在。
- preview 需要由人工或 VLM 继续检查 object identity、prompt match、floating、penetration、严重遮挡和错误物体数量。
- 如果物体明显侧躺、倒置、穿桌、悬空、严重遮挡或语义错误，必须标记为 fail。
- 如果还没有人工 / VLM / Codex visual review 真正看过图片，只能标记为 pending，不能标记为 pass。

这个 skill 不替代视觉模型。它定义的是 review 标准和 artifact contract。
