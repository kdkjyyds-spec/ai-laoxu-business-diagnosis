# 案例与效果验证（Examples）

> 这个目录放了 3 份"中医出海"项目的诊断报告，对比**有/无 business-diagnosis skill** 的输出差异。
> 目的：让用户/审阅者直观看到 skill 带来的增量价值。

---

## 文件清单

| 文件 | 角色 | 大小 | 行数 | 说明 |
|------|------|------|------|------|
| `01-baseline-no-skill.md` | 无 skill 对照组 | 10.2 KB | 100 | 通用大模型能力，无任何方法论指引 |
| `02-with-skill-v1-attempt.md` | with-skill 第一次 | 13.1 KB | 159 | 子智能体未能加载 skill（路径问题）|
| `03-with-skill-v2-true.md` | **with-skill 真正版** | 28.8 KB | 282 | 真正加载并应用 6 个 reference 文件 |
| `eval-comparison.md` | 对比总结 | - | - | 核心差异 + 量化指标 |

---

## 怎么读这套例子

1. **先看 `eval-comparison.md`** → 理解对比维度和结论
2. **再看 `01-baseline-no-skill.md`** → 知道"没 skill 时输出长什么样"
3. **最后看 `03-with-skill-v2-true.md`** → 知道"有 skill 时输出长什么样"
4. （可选）`02-with-skill-v1-attempt.md` → 看 v1 失败原因，调试多 agent 加载 skill 的注意事项

---

## 复现方式

### 准备
- 一份完整项目资料（项目名 + 客户 + 客单价 + 模式 + 团队 + 投入 + 目标）
- 建议 200-500 字

### 跑 baseline
让任意 LLM 子智能体直接做诊断，**不加载任何 skill**，prompt 模板：
```
请对以下项目做商业模式诊断：[项目资料]
要求：完整结构化评估 + 评分 + 优势风险 + 行动建议
```

### 跑 with-skill
让子智能体**先 Read** 以下文件再开始诊断：
1. `business-diagnosis/SKILL.md`
2. `business-diagnosis/references/6-layer-methodology.md`
3. `business-diagnosis/references/13-dimensions-rubric.md`
4. `business-diagnosis/references/sample-library.md`
5. `business-diagnosis/references/industry-patterns.md`
6. `business-diagnosis/references/output-templates.md`

然后按 6 层方法论做完整诊断，**必须引用 sample-library.md 里的同主题 TOP 标杆做横向对比**。

### 注意事项
- ⚠️ 多 agent 环境下，**子智能体可能看不到主 agent 的 skill 目录**，必须用 Read 工具显式加载
- 子智能体 agent_name 不要用 `general`（看不到 mavis 的 skill），建议用 `mavis` 或 inline 内容
- prompt 里**强制要求"必须引用知识库"**，否则子智能体可能"读而不引"

---

## 关键结论

**skill 真的有效。** 同一份项目资料，with-skill 输出在：
- 结构化程度（6 层 vs 自创 8 维度）
- 知识库引用（15 个 vs 0 个）
- 横向对比（4 个详细对比标杆 vs 无）
- 行业洞察（24 主题陷阱表 vs 自说自话）
- 可执行性（每条建议带具体标杆 vs 通用建议）

这 5 个维度上都明显强于 baseline。
