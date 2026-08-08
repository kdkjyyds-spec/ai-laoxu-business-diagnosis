# 实战案例库（Case Library）

> K 盘「案例库 1-8 期」1,182 篇实战案例的解析与提取结果。
> 数据源：`K:\生财有术【第1—9期】(1)\` 下的 1-4 期/5/6/7 期完整版 + 第 8 期普通帖/精华帖/风向标/航海篇，共 1,186 PDF（4 个 < 1KB 跳过，1,182 个成功提取）。

---

## 一、目录结构

```
case-library/
├── raw-text/              # 1,182 个 PDF 的前 30 页文本（按期数分目录）
│   ├── 案例库 1-4 期完整版]/  (253 files, 5.9 MB)
│   ├── 案例库 第8 期普通帖]  /  (643 files, 2.9 MB)
│   ├── 案例库 第8 期精华帖]  /  (107 files, 0.7 MB)
│   └── 案例库 第8 期风向标]  /  (179 files, 1.0 MB)
├── extracted/             # 结构化提取结果
│   ├── all-100-cases.json        # 100 个抽样的合并提取（10 LLM + 90 程序化）
│   ├── auto-classify.json        # 1,182 个全量自动分类
│   ├── group-0-llm-extract.json  # 10 个 LLM 精读（C-1 到 C-10）
│   └── index-by-industry.json    # 按行业/模式/期数 INDEX
├── prompts/               # 10 个子智能体 prompt（group-0 到 group-9）
├── batch_extract.py       # PDF 批量文本提取脚本（多进程）
├── auto_classify.py       # 全量自动分类脚本
├── program_extract_90.py  # 90 个抽样的程序化提取脚本
├── gen_prompts.py         # 子智能体 prompt 生成器
├── sample_100.py          # 100 个抽样脚本
├── merge_and_index.py     # 合并 + INDEX 脚本
└── README.md              # 本文件
```

---

## 二、数据统计

### 1,182 篇全量自动分类（关键词 + 正则）

**Top 10 主题**：
| 主题 | 命中次数 | 代表案例数（按 100 抽样）|
|------|----------|--------------------------|
| IP/内容 | 842 | 2 |
| 抖音/直播 | 372 | 7 |
| AI 工具/提效 | 323 | 36 |
| 培训/课程 | 234 | - |
| 工具/SaaS | 193 | - |
| 小红书 | 170 | 8 |
| 咨询/陪跑 | 162 | 4 |
| 视频号 | 110 | 10 |
| 电商/带货 | 109 | 2 |
| TikTok/海外 | 101 | 6 |

### 100 个抽样的精细提取（10 LLM + 90 程序化）

**行业分布**（100 抽样）：
- AI 工具: 36 cases
- 微信生态: 13 cases
- 视频号: 10 cases
- 小红书: 8 cases
- 抖音: 7 cases
- TikTok/海外: 6 cases
- 咨询/陪跑: 4 cases
- 电商: 2 cases
- Web3/新概念: 2 cases
- IP/内容: 2 cases
- 投资/金融: 2 cases
- 教育: 2 cases
- 情感/社交: 1 case
- 中医/养生: 1 case

**模式分布**（Top 10）：
- 短视频IP: 34 cases
- 课程训练营: 25 cases
- 1v1咨询/陪跑: 18 cases
- 直播带货: 17 cases
- 不明确: 16 cases
- 私域转化: 11 cases
- 直播: 10 cases
- 课程/分销: 7 cases
- 线下服务: 7 cases
- 电商代发: 6 cases

**期数分布**（4 个子目录各 25 个）：
- 案例库 1-4 期完整版]: 25 cases
- 案例库 第8 期普通帖]: 25 cases
- 案例库 第8 期精华帖]: 25 cases
- 案例库 第8 期风向标]: 25 cases

---

## 三、提取方法说明

### LLM 精读（10 cases, group-0）
- 用子智能体 + Read 工具，深度提取每个 case 的：
  - project_name（脱敏）
  - industry（行业）
  - pattern（模式）
  - client_type（客户类型）
  - price_point + price_evidence（客单价 + 原文依据）
  - key_design（3-5 个关键设计点）
  - monetization_chain（变现链路）
  - revenue_signal（收入线索）
  - risk_factors（风险因素）
  - differentiation（差异化）
  - one_line_summary（一句话总结）
- **质量**：高，每个 case ~1.3KB JSON，含具体数字/原文/设计点
- **限制**：Token Plan 用完后无法继续（剩 9 个 group 共 90 cases 跑不了）

### 程序化提取（90 cases, group-1 到 group-9）
- 关键词 + 正则 + 结构化推断
- 字段：同上，但 key_design 可能是"30-50 字 snippet"（不如 LLM 精读）
- **质量**：中，project_name 和 industry 可能误判
- **优势**：不需要 LLM，1 分钟跑完 100 个

### 自动分类（1,182 cases, 全量）
- 关键词频次统计（不提取结构化字段）
- 用于"主题分布速查"
- **质量**：粗，只看关键词命中数

---

## 四、已知限制与解决方向

| 限制 | 当前 | 解决方向 |
|------|------|----------|
| 行业分类误判 | C-1 把"100 赚钱高手合集"分到 Web3（因文中提"区块"）| 加 LLM 精读覆盖 + 行业优先级排序 |
| Key Design 提取杂讯 | 部分 case 抓到了目录页/分隔符 | 增强过滤（已修复 + 重跑）|
| Token Plan 限制 | 9 个 group 没跑 LLM 精读 | 等用户充值 token 后重跑；或接受程序化结果 |
| 模式/行业 标签不统一 | LLM 用 str，程序化用 list | 已加 `split(",")` 兼容 |
| 长文 PDF 全文未提取 | 只取了前 30 页 | 部分精华案例可能藏在 30 页后；可按需补充 |

---

## 五、如何使用

### 查找特定主题/行业的案例
```python
import json
d = json.load(open(r"...\extracted\all-100-cases.json", encoding="utf-8"))
ai_cases = [c for c in d["cases"] if "AI" in c["industry"]]
print(f"AI 类案例: {len(ai_cases)}")
for c in ai_cases[:3]:
    print(f"  {c['case_id']}: {c['project_name']}")
```

### 找客单价最高的 case
```python
cases = sorted(d["cases"], key=lambda c: len(c.get("price_point", "")), reverse=True)
for c in cases[:5]:
    print(f"{c['case_id']}: {c['price_point']} | {c['project_name']}")
```

### 按期数分桶
```python
by_period = {}
for c in d["cases"]:
    by_period.setdefault(c["period"], []).append(c)
```

### 读全文（用于深度分析）
```python
from pathlib import Path
text = Path(r"...\raw-text\案例库 1-4 期完整版]\[某txt文件]").read_text(encoding="utf-8")
```

---

## 六、复现/扩展

```bash
# 1. 批量提取 PDF 文本
python batch_extract.py

# 2. 全量自动分类
python auto_classify.py

# 3. 抽样 100 个
python sample_100.py

# 4. 程序化深度提取 90 个（除 group-0）
python program_extract_90.py

# 5. 合并 + INDEX
python merge_and_index.py

# 6. LLM 精读（需要 Token Plan）
# 启动子智能体，用 prompts/group-X-prompt.md
```

---

## 七、归档信息

- **生成日期**：2026-08-07 ~ 2026-08-08
- **总大小**：~12 MB 文本 + ~1.5 MB JSON
- **数据源**：K 盘「生财有术【第1—9期】(1)」
- **脱敏状态**：已脱敏（人名/花名/品牌/公司/城市 → "项目 A/B/C"）
- **Token 状态**：Plan 用完，9 个 group 跑 LLM 失败，已用程序化提取覆盖
