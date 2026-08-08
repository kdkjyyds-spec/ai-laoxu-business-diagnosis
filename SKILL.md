---
name: business-diagnosis
display_name: 自媒体AI老徐的商业模式诊断
description: |
  【自媒体AI老徐的商业模式诊断】6 层商业模式诊断：把一个项目（资料/方案/PPT/口头描述）按"本体画布 + 可行性 + 健康度 + 对比 + 创新 + 长期价值"做完整结构化诊断，输出 Markdown 报告 + Excel 评分表 + 立即可做建议。
  数据源：1000多分份商业报告 + 14 份专项 +  2000+ 实战手册。
  适用模式：A+B（一次性诊断 + 迭代追问）；输出格式：A+B（Markdown + Excel）。
  Trigger on phrases like: "诊断我的项目", "商业模式分析", "项目评估", "这个商业能不能做", "中医出海怎么做", "新项目可行性", "6 层诊断", "BMC 画布", "13 维度评分", "24 维度梳理".
  Do NOT use for: 写代码、数据清洗、纯 PPT 设计、项目执行（不是分析）、已成熟的运营复盘。
---

# 业务诊断助手（Business Diagnosis）

## Inputs to collect

诊断开始前，先判断输入充分性：

**充分输入**（直接做诊断）：
- 项目资料（docx/pdf/PPT 链接/对话描述）
- 至少有：项目名 + 客户 + 客单价 + 模式 + 团队 + 投入

**不充分输入**（先问 1-2 个澄清问题）：
- 只说"我想做 X"（没说客单价/团队/市场）→ 用 `references/15q-self-check.md` 让用户回答
- 资料只是想法没成型 → 先做"行业典型模式"对比（`references/industry-patterns.md`），再决定要不要深挖

**硬约束（始终执行）**：
- 不出现人名、花名、公司名、品牌名、城市/具体地址、手机/微信号
- 项目类型/行业可保留（如"中医出海""AI 咨询""SpaS 工具"）
- 引用案例全部脱敏（用"项目 A/B/C"或主题+序号代替）

## Procedure

### Step 1 信息收集与脱敏
1. 读用户提供的项目资料（如有文件）
2. 提取 6 个基础事实：项目名 / 客户 / 客单价 / 团队 / 投入 / 目标
3. 脱敏：所有人名/公司/城市/花名 → 替换为"项目 A"或行业+序号
4. 整理成"诊断输入卡"（结构化字段）

### Step 2 选择诊断模式
- 资料丰富（>500 字 + 6 字段齐全）→ **完整 6 层诊断**
- 资料中等（200-500 字）→ **精简 3 层诊断**（本体 + 可行性 + 创新）
- 资料少（<200 字或只有想法）→ **先做自检清单**（用 `references/15q-self-check.md`）

### Step 3 6 层诊断（按 `references/6-layer-methodology.md`）
1. **层 1：商业模式本体** — BMC 9 要素画布（客户细分/价值主张/渠道/客户关系/收入来源/关键资源/关键活动/重要伙伴/成本结构）
2. **层 2：可行性** — 市场/财务/法律/技术/团队/资本 6 维
3. **层 3：健康度** — 增长/复购/复制/抗风险/客户/效率/财务 7 维
4. **层 4：对比** — 直接竞品/替代品/跨界/标杆/护城河
5. **层 5：创新** — 价值/收入/成本/渠道/关系/复制/杠杆 7 个创新方向
6. **层 6：长期价值** — 市场/窗口/周期/沉淀/复制/退出/匹配 7 维

每层评分 1-5 星（看 `references/13-dimensions-rubric.md`），每格附"评分+一句话证据"。

### Step 4 横向对比（可选）
- 询问用户：要不要跟样本库（同主题 TOP 10）对比？
- 是 → 调 `references/sample-library.md` 找同主题案例对比
- 否 → 跳过

### Step 5 输出诊断报告
按 `references/output-templates.md` 输出：
- **Markdown 报告**：6 层结构化诊断 + 立即可做 + 中期可做 + 长期重塑
- **Excel 评分表**（如用户需要）：13 维度 × 项目，4 个 Sheet

### Step 6 持续追问
- 输出诊断后，主动问："要不要我针对某个具体短板深挖？"
- 问 1-2 个 follow-up：
  - "你的最大短板是 X，要不要我帮你拆解怎么补？"
  - "你说的 Y 还能再具体点吗？比如数据/案例/时间节点"

## Output contract

每次诊断输出**至少包含**：

1. **项目速览卡**（6 字段结构化）
2. **6 层诊断表**（每层评分 + 1-2 句话关键证据）
3. **3 大优势 + 3 大风险**
4. **立即可做 3 件事 + 中期 2 件事 + 长期 1 件事**
5. **一句话总结**

可选输出：
- Excel 评分表（4 Sheet：评分总表 / 项目详情 / 排名 / 洞察）
- 同主题横向对比（vs TOP 10 标杆）

## Failure handling

- **资料不足**：先问 1-2 个澄清问题，不要硬猜
- **资料里有敏感信息**：自动脱敏（人名/公司/城市），不报错
- **模式判断困难**：用 `references/industry-patterns.md` 找相似案例，让用户选
- **数据计算错误**：用 `references/13-dimensions-rubric.md` 的自动规则计算
- **用户反复改需求**：保持诊断报告版本号，每次更新标 v1/v2/v3

## Examples

### Example 1：完整诊断
**Input**：用户给"中医出海"项目立项书（>500 字）
**Process**：完整 6 层诊断 + 13 维度评分
**Output**：Markdown 报告 + Excel 评分表
**Time**：约 5-10 分钟

### Example 2：想法阶段
**Input**：用户说"我想做中医出海"
**Process**：先调 `references/15q-self-check.md`，让用户答 5-6 个关键问题；再调 `references/industry-patterns.md` 给 4 种模式对比；再做精简 3 层诊断
**Output**：精简版诊断 + 模式选择建议
**Time**：约 3-5 分钟

## Reference files

诊断过程中需要时再读：
- `references/6-layer-methodology.md` — 6 层方法论详解
- `references/13-dimensions-rubric.md` — 13 维度评分规则（自动 + 关键证据）
- `references/24-dimensions-rubric.md` — 24 维度评估框架
- `references/15q-self-check.md` — 15 题自检清单（用户输入不充分时用）
- `references/industry-patterns.md` — 行业典型模式库（中医出海 4 种、新消费 3 种等）
- `references/sample-library.md` — 脱敏样本库（24 大主题 TOP 案例，整合 1718 立项 + 1-9 期实战）
- `references/desensitization-rules.md` — 脱敏规则清单
- `references/output-templates.md` — 输出模板（Markdown + Excel）
