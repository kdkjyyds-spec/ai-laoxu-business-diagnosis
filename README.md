# 自媒体AI老徐的商业模式诊断

> 6 层商业模式诊断 skill：把一个项目（资料/方案/PPT/口头描述）按"本体画布 + 可行性 + 健康度 + 对比 + 创新 + 长期价值"做完整结构化诊断，输出 Markdown 报告 + HTML 网页 + PDF 排版 + 立即可做建议。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## 快速上手

### 安装

```bash
git clone https://github.com/your-username/business-diagnosis.git
cd business-diagnosis
pip install markdown beautifulsoup4 reportlab Pillow
```

### 用法

#### 1. 触发 skill（在你的 LLM agent 里）

直接说：
- "诊断我的项目：..."
- "商业模式分析：..."
- "我想做 XX，可行吗？"
- "中医出海怎么做？"
- "6 层诊断"
- "BMC 画布"

skill 会自动加载 6 层方法论 + 样本库（24 大主题 150+ 标杆案例）。

#### 2. 生成报告（Markdown → HTML + PDF）

```bash
python scripts/build_report.py path/to/your-diagnosis.md
```

输出：
- `your-diagnosis.html`（带样式的网页）
- `your-diagnosis.pdf`（A4 排版，可打印分享）

选项：
- `--out-dir <dir>`：自定义输出目录
- `--html-only`：只生成 HTML
- `--pdf-only`：只生成 PDF
- `--no-pdf`：跳过 PDF

---

## 数据源

skill 内置的样本库整合自：
- **1,718 份个人立项报告** + **14 份专项**（脱敏）
- **K 盘 1-9 期 200+ 实战手册**（按 24 大主题分类）

数据全部脱敏（人名/花名/品牌/公司/城市 → 项目 A/B/C），可直接公开。

### 24 大主题分类

| # | 主题 | 占比 | # | 主题 | 占比 |
|---|------|------|---|------|------|
| 1 | 咨询/陪跑类 | 13% | 13 | 生活/消费类 | <1% |
| 2 | 培训/课程类 | 8% | 14-24 | K 盘 1-9 期实战 | 60% |
| 3-13 | ... | ... | | （抖音/视频号/小红书/微信/TikTok/AI/闲鱼/快团团/出海/同城/教育/医疗/金融 等）| |

详见 `references/sample-library.md`。

---

## 目录结构

```
business-diagnosis/
├── SKILL.md                      # 入口（agent 加载的 skill 描述）
├── README.md                     # 本文件（GitHub 展示页）
├── LICENSE                       # MIT
├── .gitignore
├── references/                   # 8 个方法论 + 知识库
│   ├── 6-layer-methodology.md    # 6 层诊断方法论
│   ├── 13-dimensions-rubric.md   # 13 维度评分
│   ├── 24-dimensions-rubric.md   # 24 维度评估
│   ├── 15q-self-check.md         # 15 题自检清单
│   ├── sample-library.md         # 24 主题样本库（核心知识库）
│   ├── industry-patterns.md      # 行业典型模式
│   ├── desensitization-rules.md  # 脱敏规则
│   └── output-templates.md       # 输出模板
├── scripts/
│   └── build_report.py           # Markdown → HTML + PDF 转换器
└── examples/                     # 案例与效果验证
    ├── README.md                 # 怎么用 examples
    ├── 01-baseline-no-skill.md  # 无 skill 对照
    ├── 02-with-skill-v1.md       # with-skill v1 失败
    ├── 03-with-skill-v2.md       # with-skill v2 真正用 skill
    ├── 04-test-宝妈的诊断报告.md # 测试案例（中等详细度）
    ├── 05-宝妈诊断-小白版.md     # 测试案例（小白版，最详细）
    ├── 05-宝妈诊断-小白版.html   # 同上的 HTML 版
    ├── 05-宝妈诊断-小白版.pdf    # 同上的 PDF 版（17 页 A4）
    ├── eval-comparison.md        # baseline vs with-skill 对比
    └── case-library/             # K 盘 1-8 期实战案例（1,182 篇 PDF 解析 + 100 抽样精读）
```

---

## 6 层诊断方法论

| 层次 | 关注什么 | 评分维度 |
|------|----------|----------|
| **层 1 本体** | 你的项目画出来是清晰的？| BMC 9 要素（CS/VP/CH/CR/R$/KR/KA/KP/C$）|
| **层 2 可行性** | 能不能跑起来？| 市场/财务/合规/技术/团队/资本 6 维 |
| **层 3 健康度** | 单位经济好不好？| 增长/复购/复制/抗风险/客户/效率/财务 7 维 |
| **层 4 对比** | 你跟同行有什么不一样？| 直接竞品/替代品/跨界/标杆/护城河 |
| **层 5 创新** | 你的差异化点在哪？| 价值/收入/成本/渠道/关系/复制/杠杆 7 方向 |
| **层 6 长期价值** | 5-10 年还能持续吗？| 市场/窗口/周期/沉淀/复制/退出/匹配 7 维 |

**综合评分** = 6 层加权（本体 0.15 + 可行性 0.20 + 健康度 0.15 + 对比 0.10 + 创新 0.15 + 长期价值 0.25）

每层 1-5 星评分 + 1-2 句话关键证据。

---

## 适用场景

✅ **适合用**：
- 复杂项目的系统化诊断（200+ 字资料）
- 需要横向对比同行标杆的场景
- 需要给出"可执行、可信、有依据"建议的场景
- 客户/创始人给完整项目资料做全套报告

❌ **不适合**：
- 简单项目的快速评估（杀鸡用牛刀）
- 客户没准备好资料（先用 15q-self-check.md 问问题）
- 写代码、数据清洗、纯 PPT 设计、项目执行（不是分析）

---

## 示例：完整诊断报告

输入："我想做中医出海"
输出（见 `examples/05-宝妈诊断-小白版.pdf`）：

- 6 层诊断（本体/可行性/健康度/对比/创新/长期价值）
- 横向对比（4 个同主题标杆详细对标）
- 3 大优势 + 3 大风险
- 立即可做 3 件事 + 中期 2 件事 + 长期 1 件事
- 一句话总结
- 知识库引用清单

---

## 测试验证

跑过 2 个真实 case：
- **案例 1**：中医出海项目 → 6 层诊断 + 15 个知识库引用 + 4 个标杆详细对比
- **案例 2**：宝妈自媒体+读书会训练营（v2）→ 综合评分 3.5/5 + "新手背景 = 反模式风险"识别

效果对比（baseline vs with-skill）见 `examples/eval-comparison.md`：
- 输出量提升 2.8 倍
- 知识库引用从 0 → 15
- 方法论从"自创" → "内置 6 层"
- 建议从"通用" → "有标杆依据"

---

## 路线图

- [x] 6 层方法论 + 13/24 维度评分
- [x] 24 大主题样本库（150+ 标杆案例）
- [x] K 盘 1-9 期实战案例库（1,182 篇）
- [x] HTML + PDF 报告自动生成
- [ ] Excel 评分表（4 Sheet）支持
- [ ] 行业模式库扩展（更多行业典型路径）
- [ ] 多语言支持（English / 中文）

---

## 贡献

欢迎贡献！具体方式：
1. **新增主题/行业模式**：在 `references/sample-library.md` 添加新主题和标杆案例
2. **改进方法论**：在 `references/6-layer-methodology.md` 提建议
3. **修 bug / 提 issue**：报告生成器 `scripts/build_report.py` 任何问题

提交 PR 前请：
- 数据脱敏（人名/花名/品牌/公司/城市 → 项目 A/B/C）
- 引用 case 用主题+序号（不要原始项目名）
- 保持样本库格式一致

---

## 许可证

[MIT](LICENSE)

---

## 致谢

skill 内置的样本库来自：

1000 份商业案例
14 份专项
2700+ 实战手册（从0-1拆解如何变现）
数据已全部脱敏，仅用于商业模式诊断方法论研究和教学。
