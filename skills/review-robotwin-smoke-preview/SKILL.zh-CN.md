# 审查 RoboTwin Smoke Preview

当需要检查 placement run 产生的 RoboTwin smoke 输出时使用这个 skill。

## 检查项

- `smoke_report.json` 存在且结果为 pass。
- `head_camera.png` 和 `observer_camera.png` 存在。
- 可选的 `observer_camera.mp4` 存在。
- preview 需要由人工或 VLM 继续检查 object identity、prompt match、floating、penetration、严重遮挡和错误物体数量。

这个 skill 不替代视觉模型。它定义的是 review 标准和 artifact contract。
