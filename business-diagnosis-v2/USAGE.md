# 使用指南（USAGE）

> 这份文档讲**别人下载这个 skill 后，怎么用**。
> 3 种使用方式，由易到难。

---

## 方式 1：纯阅读（最简单，不用任何工具）

如果只是想**看诊断报告长什么样**，不打算实际跑：

1. **GitHub 仓库**：[kdkjyyds-spec/ai-laoxu-business-diagnosis](https://github.com/kdkjyyds-spec/ai-laoxu-business-diagnosis)
2. 直接打开 **`examples/05-宝妈诊断-小白版.md`**（GitHub 自动渲染 Markdown）
3. 或者下载 **`examples/05-宝妈诊断-小白版.pdf`** 离线看

✅ 不需要：装 Python、克隆仓库、装依赖
❌ 限制：只能看已有 demo，不能跑新诊断

---

## 方式 2：用 skill 跑自己的项目（推荐）

这是最常见的使用方式——**在你自己的 LLM agent 里加载这个 skill**。

### 步骤 1：克隆仓库

```bash
git clone https://github.com/kdkjyyds-spec/ai-laoxu-business-diagnosis.git
cd business-diagnosis
```

### 步骤 2：装依赖

需要 Python 3.9+：

```bash
pip install markdown beautifulsoup4 reportlab Pillow
```

> 依赖说明：
> - `markdown`：把 .md 转 HTML
> - `beautifulsoup4`：解析 HTML
> - `reportlab`：把 HTML 转 PDF
> - `Pillow`：reportlab 内部需要

### 步骤 3：测试报告生成器

确认 Python 脚本能跑：

```bash
python scripts/build_report.py examples/05-宝妈诊断-小白版.md
```

**预期输出**：
- `examples/05-宝妈诊断-小白版.html`（带样式的网页）
- `examples/05-宝妈诊断-小白版.pdf`（A4 排版的 PDF）

✅ 看到这个就 OK，你的环境配好了。

### 步骤 4：加载到你的 LLM agent

把 `business-diagnosis/SKILL.md` 的内容（或整个 skill 目录）告诉你的 agent。

**Mavis / Claude / GPT 等支持 skill 的 agent**：
- 把整个 `business-diagnosis/` 目录放到你的 agent 找得到的地方
- agent 自动发现并加载 `SKILL.md`

**其他 LLM**：
- 复制 `SKILL.md` 的内容到你的 system prompt
- 把 `references/` 下的 8 个文件作为上下文

### 步骤 5：开始诊断

跟你的 agent 说：

- "诊断我的项目：..."
- "商业模式分析：..."
- "我想做 XX，可行吗？"
- "6 层诊断"

agent 会自动加载 6 层方法论 + 样本库，输出结构化报告。

### 步骤 6：导出报告

拿到 Markdown 报告后，转 HTML + PDF：

```bash
python scripts/build_report.py your-diagnosis-report.md
```

输出 `your-diagnosis-report.html` + `your-diagnosis-report.pdf`。

---

## 方式 3：开发/修改 skill（高级用户）

如果你想**改进这个 skill**（加新主题、新方法论）：

### 装 GitHub Desktop（推荐，图形界面）

1. 下载：**https://desktop.github.com**
2. 登录 GitHub 账号（OAuth，不用 PAT）
3. **File → Add Local Repository** → 选 `business-diagnosis` 文件夹
4. 改代码 → **Commit to main** → **Push origin**（3 步搞定）

### 用命令行（需要学 git）

```bash
# 1. 改完代码
# 2. 提交并推送
cd business-diagnosis
git add .
git commit -m "改了什么"
git push origin main
```

⚠️ 命令行方式需要配代理或 VPN（GitHub 在国内直连可能慢）。

---

## 文件用途速查

| 文件 | 用途 | 何时打开 |
|------|------|----------|
| `SKILL.md` | skill 入口（agent 加载这个）| 让 agent 知道这个 skill 存在 |
| `README.md` | GitHub 展示页 | 别人浏览仓库时看 |
| `references/6-layer-methodology.md` | 6 层诊断方法论 | 想了解诊断怎么做的 |
| `references/13-dimensions-rubric.md` | 13 维度评分规则 | 想给项目打分 |
| `references/sample-library.md` | 24 主题样本库（核心知识库）| 想看同主题标杆 |
| `references/15q-self-check.md` | 15 题自检清单 | 你只想到 idea 没具体方案时 |
| `references/industry-patterns.md` | 行业典型模式 | 想找同行业参考 |
| `references/desensitization-rules.md` | 脱敏规则 | 想看案例怎么脱敏 |
| `references/output-templates.md` | 输出模板 | 想看诊断报告标准结构 |
| `references/24-dimensions-rubric.md` | 24 维度评估 | 想做更细的评估 |
| `scripts/build_report.py` | MD → HTML + PDF 转换器 | 跑 `python scripts/build_report.py xxx.md` |
| `examples/` | 实际诊断案例 | 看别人怎么用的 |
| `examples/case-library/README.md` | K 盘案例库说明 | 想用 1182 个脱敏案例 |

---

## 常见问题

### Q1: 装依赖时报 "Pillow error"
试试：
```bash
pip install --upgrade pip
pip install Pillow
```

### Q2: 生成 PDF 中文是方块
说明系统没装中文字体：
- Windows：自带 SimHei，**不用额外装**
- Mac：装 [PingFang](https://support.apple.com/zh-cn/guide/fontbook/)
- Linux：`apt install fonts-noto-cjk` 或 `apt install fonts-wqy-microhei`

### Q3: git push 时报 "port 443 via 127.0.0.1"
说明你的代理软件没启动，或端口不是 7890/7897。
**推荐方案：装 GitHub Desktop**（图形界面，不用配代理）。

### Q4: SKILL.md 不会用？
打开 `SKILL.md` 看"Procedure"和"Examples"部分——有完整流程和示例。

### Q5: 想看别人用了什么 prompt？
打开 `examples/05-宝妈诊断-小白版.md` 顶部，看 `> 项目名：...` 下面那段——记录了用什么输入得到的这个输出。

---

## 进阶玩法

### 调单个维度评分

在 `references/13-dimensions-rubric.md` 里有每个维度的评分规则和分值区间。你可以在诊断前先看一遍，了解每个维度的标准。

### 加自己的样本库

把你的项目数据加到 `references/sample-library.md`：
1. 按主题分类
2. 写"项目名（脱敏）/ 模式 / 客单价 / 关键设计 / 适用场景"
3. 用 "项目 A/B/C" 编号，不写原项目名

### 自定义诊断输出

修改 `references/output-templates.md` 调整输出结构。

修改后跑：
```bash
python scripts/build_report.py your-report.md
```

会按新模板生成。

---

## 反馈和建议

发现问题或有改进建议？

1. **GitHub Issue**：https://github.com/kdkjyyds-spec/ai-laoxu-business-diagnosis/issues
2. **PR**：直接修改后提交 Pull Request
3. **邮件**：见仓库作者主页

---

*最后更新：2026-08-08*
