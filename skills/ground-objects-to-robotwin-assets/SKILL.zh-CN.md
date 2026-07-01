# 将自然语言物体映射到 RoboTwin 资产

当需要把自然语言中的 object mentions 映射到 RoboTwin asset catalog entry 时使用这个 skill。

## 规则

- 用 `semantic_name`、`aliases` 和 `tags` 匹配 prompt terms。
- 优先选择精确语义匹配，而不是宽泛类别匹配。
- 如果多个资产都合理，返回不确定性。
- 不要编造缺失资产；缺失时标记为 unavailable，或请求更丰富的资产库。
- 保留后续 validator 需要的 `asset_id`、`model_id` 和 metadata。
