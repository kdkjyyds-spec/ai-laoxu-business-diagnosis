"""
build_report.py - 把诊断报告 Markdown 同时转为 HTML + PDF。

用法：
  python build_report.py <input.md> [--out-dir <output_dir>]

输出：
  - 同名 .html
  - 同名 .pdf
  - 都输出到 --out-dir 目录（默认同 input.md 同目录）

依赖：
  pip install markdown beautifulsoup4 reportlab Pillow

设计：
  - HTML 用 markdown 库（GFM 扩展 + toc）
  - PDF 用 reportlab + 微软雅黑（避免 weasyprint 的 GTK3 依赖）
  - 不依赖 Node.js / Chromium / wkhtmltopdf
"""
import argparse
import re
import sys
from pathlib import Path
import markdown
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, HRFlowable, ListFlowable, ListItem
)


def parse_args():
    p = argparse.ArgumentParser(description="把诊断报告 Markdown 转 HTML + PDF")
    p.add_argument("input", type=Path, help="输入的 Markdown 文件")
    p.add_argument("--out-dir", type=Path, default=None, help="输出目录（默认 = 输入文件同目录）")
    p.add_argument("--html-only", action="store_true", help="只生成 HTML")
    p.add_argument("--pdf-only", action="store_true", help="只生成 PDF")
    p.add_argument("--no-pdf", action="store_true", help="跳过 PDF 生成")
    return p.parse_args()


# 注册中文字体
def register_chinese_font():
    """注册中文字体（Windows: SimHei）"""
    candidates = [
        r'C:\Windows\Fonts\simhei.ttf',  # Windows SimHei
        r'C:\Windows\Fonts\msyh.ttc',     # Windows Microsoft YaHei
        '/System/Library/Fonts/PingFang.ttc',  # macOS PingFang
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # Linux WQY
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                pdfmetrics.registerFont(TTFont('SimHei', path))
                return 'SimHei'
            except Exception:
                continue
    print("[WARN] 未找到中文字体，PDF 中文可能显示异常", file=sys.stderr)
    return 'Helvetica'


FONT_NAME = register_chinese_font()
print(f"[OK] 字体: {FONT_NAME}")


def md_to_html(md_text, title=""):
    """Markdown 转 HTML（带完整 CSS）"""
    md = markdown.Markdown(
        extensions=['extra', 'codehilite', 'toc', 'fenced_code', 'tables'],
        extension_configs={'toc': {'permalink': True, 'toc_depth': 3}}
    )
    body = md.convert(md_text)

    full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>{HTML_CSS}</style>
</head>
<body>
<div class="container">
{body}
</div>
</body>
</html>
"""
    return full, body

# CSS（仅用于 HTML）
HTML_CSS = """
body {
  font-family: "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB", sans-serif;
  max-width: 800px;
  margin: 40px auto;
  padding: 20px 30px;
  line-height: 1.75;
  color: #222;
  background: #fafafa;
}
.container {
  background: white;
  padding: 40px 50px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
h1 { font-size: 28px; color: #1a1a1a; border-bottom: 3px solid #2563eb; padding-bottom: 10px; }
h2 { font-size: 22px; color: #2563eb; border-bottom: 2px solid #93c5fd; padding-bottom: 6px; margin-top: 35px; }
h3 { font-size: 18px; color: #1e40af; margin-top: 25px; }
h4 { font-size: 15px; color: #1e3a8a; margin-top: 20px; }
blockquote {
  border-left: 4px solid #2563eb;
  background: #eff6ff;
  margin: 15px 0;
  padding: 10px 18px;
  color: #1e40af;
  border-radius: 4px;
}
code { background: #f1f5f9; padding: 2px 5px; border-radius: 3px; color: #be185d; font-size: 0.9em; }
pre { background: #f8fafc; border: 1px solid #cbd5e1; padding: 12px; border-radius: 4px; overflow-x: auto; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 15px 0; font-size: 14px; }
th, td { border: 1px solid #cbd5e1; padding: 8px 12px; text-align: left; }
th { background: #2563eb; color: white; }
tr:nth-child(even) { background: #f8fafc; }
.green { color: #16a34a; font-weight: 700; }
.yellow { color: #ca8a04; font-weight: 700; }
.red { color: #dc2626; font-weight: 700; }
.blue { color: #2563eb; font-weight: 700; }
hr { border: none; border-top: 1px dashed #cbd5e1; margin: 25px 0; }
.toc { background: #f8fafc; padding: 15px 20px; border-radius: 4px; margin: 20px 0; }
.toc ul { padding-left: 25px; }
.toc a { color: #2563eb; text-decoration: none; }
"""


def md_to_html(md_text, title=""):
    """Markdown 转 HTML（带完整 CSS）"""
    md = markdown.Markdown(
        extensions=['extra', 'codehilite', 'toc', 'fenced_code', 'tables'],
        extension_configs={'toc': {'permalink': True, 'toc_depth': 3}}
    )
    body = md.convert(md_text)
    if not title:
        title = "诊断报告"

    full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>{HTML_CSS}</style>
</head>
<body>
<div class="container">
{body}
</div>
</body>
</html>
"""
    return full, body


def html_to_pdf_elements(html_body, styles):
    """把 HTML body 解析成 reportlab Platypus 元素列表"""
    soup = BeautifulSoup(html_body, 'html.parser')

    # 找到 body 内的所有顶级子元素
    if soup.body:
        top_tags = list(soup.body.children)
    else:
        top_tags = list(soup.children)

    elements = []

    for tag in top_tags:
        # 跳过字符串空白
        if not hasattr(tag, 'name') or tag.name is None:
            continue
        # 跳过 script/style/head
        if tag.name in ('script', 'style', 'head', 'meta', 'link', 'title'):
            continue

        elements.extend(_process_tag(tag, styles))

    return elements


def _process_tag(tag, styles, depth=0):
    """处理单个 tag，返回元素列表（不递归处理 div，避免 stack overflow）"""
    if depth > 3:
        # 太深就退化为纯文本
        return [Paragraph(self_clean(tag.get_text()), styles['BodyText'])]

    elements = []

    # 标题
    if tag.name == 'h1':
        elements.append(Paragraph(self_clean(tag.get_text()), styles['Heading1']))
        elements.append(Spacer(1, 4*mm))
    elif tag.name == 'h2':
        elements.append(Paragraph(self_clean(tag.get_text()), styles['Heading2']))
        elements.append(Spacer(1, 3*mm))
    elif tag.name == 'h3':
        elements.append(Paragraph(self_clean(tag.get_text()), styles['Heading3']))
        elements.append(Spacer(1, 2*mm))
    elif tag.name == 'h4':
        elements.append(Paragraph(self_clean(tag.get_text()), styles['Heading4']))
        elements.append(Spacer(1, 2*mm))

    # 段落（保留 inline 格式）
    elif tag.name == 'p':
        html_text = render_inline(tag)
        if html_text.strip():
            elements.append(Paragraph(html_text, styles['BodyText']))

    # 列表
    elif tag.name in ('ul', 'ol'):
        items = []
        for li in tag.find_all('li', recursive=False):
            items.append(Paragraph(render_inline(li), styles['ListItem']))
        bullet = 'bullet' if tag.name == 'ul' else '1'
        elements.append(ListFlowable(items, bulletType=bullet, leftIndent=10*mm))
        elements.append(Spacer(1, 2*mm))

    # 表格
    elif tag.name == 'table':
        rows = []
        for tr in tag.find_all('tr'):
            row = []
            for cell in tr.find_all(['th', 'td']):
                html_text = render_inline(cell)
                row.append(Paragraph(html_text, styles['TableCell']))
            rows.append(row)
        if rows:
            t = Table(rows, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 3*mm))

    # 引用
    elif tag.name == 'blockquote':
        for p in tag.find_all('p', recursive=False):
            elements.append(Paragraph(render_inline(p), styles['BlockQuote']))
        if not tag.find_all('p'):
            elements.append(Paragraph(render_inline(tag), styles['BlockQuote']))

    # 代码块
    elif tag.name == 'pre':
        code_text = tag.get_text()
        elements.append(Paragraph(code_text.replace('\n', '<br/>'), styles['CodeBlock']))

    # 水平线
    elif tag.name == 'hr':
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1')))
        elements.append(Spacer(1, 3*mm))

    # 容器（div/section/article）：处理其子元素（深度限制 3）
    elif tag.name in ('div', 'section', 'article', 'main'):
        for child in tag.children:
            if not hasattr(child, 'name') or child.name is None:
                continue
            if child.name in ('script', 'style'):
                continue
            elements.extend(_process_tag(child, styles, depth=depth+1))

    # 其它（span/p 内联）：不处理顶层，跳过
    else:
        pass

    return elements


def self_clean(text):
    """清理纯文本"""
    return re.sub(r'\s+', ' ', text).strip()


def render_inline(tag):
    """把内联 HTML（strong/em/code）渲染成 reportlab 可识别的标签"""
    # 转换 markdown 内联语法
    html = str(tag)
    # 转换 <code> 内容（用 SimHei 字体，小号）
    html = re.sub(r'<code>(.*?)</code>', r'<font size="9">\1</font>', html, flags=re.DOTALL)
    # 转换 <strong> -> <b>
    html = re.sub(r'<strong>(.*?)</strong>', r'<b>\1</b>', html, flags=re.DOTALL)
    # 转换 <em> -> <i>
    html = re.sub(r'<em>(.*?)</em>', r'<i>\1</i>', html, flags=re.DOTALL)
    # 去掉其他标签
    html = re.sub(r'<[^>]+>', '', html)
    # HTML 实体
    html = html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    # 把换行转 <br/>
    html = html.replace('\n', '<br/>')
    return html


def make_styles():
    """建 reportlab 样式"""
    base = getSampleStyleSheet()

    styles = {
        'Heading1': ParagraphStyle(
            'Heading1', parent=base['Heading1'],
            fontName=FONT_NAME, fontSize=20, leading=26,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=6, spaceBefore=12,
            borderWidth=0, borderColor=colors.HexColor('#2563eb'),
            borderPadding=0,
        ),
        'Heading2': ParagraphStyle(
            'Heading2', parent=base['Heading2'],
            fontName=FONT_NAME, fontSize=15, leading=20,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=6, spaceBefore=14,
        ),
        'Heading3': ParagraphStyle(
            'Heading3', parent=base['Heading3'],
            fontName=FONT_NAME, fontSize=12.5, leading=18,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=4, spaceBefore=10,
        ),
        'Heading4': ParagraphStyle(
            'Heading4', parent=base['Heading4'],
            fontName=FONT_NAME, fontSize=11, leading=16,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=3, spaceBefore=8,
        ),
        'BodyText': ParagraphStyle(
            'BodyText', parent=base['BodyText'],
            fontName=FONT_NAME, fontSize=10, leading=15,
            textColor=colors.HexColor('#222222'),
            alignment=TA_JUSTIFY,
            spaceAfter=4,
        ),
        'ListItem': ParagraphStyle(
            'ListItem', parent=base['BodyText'],
            fontName=FONT_NAME, fontSize=10, leading=15,
            leftIndent=5*mm, spaceAfter=2,
        ),
        'TableCell': ParagraphStyle(
            'TableCell', parent=base['BodyText'],
            fontName=FONT_NAME, fontSize=8.5, leading=12,
            spaceAfter=0,
        ),
        'BlockQuote': ParagraphStyle(
            'BlockQuote', parent=base['BodyText'],
            fontName=FONT_NAME, fontSize=10, leading=15,
            leftIndent=6*mm, rightIndent=4*mm,
            textColor=colors.HexColor('#1e40af'),
            backColor=colors.HexColor('#eff6ff'),
            borderColor=colors.HexColor('#2563eb'),
            borderWidth=2, borderPadding=4,
            spaceAfter=6,
        ),
        'CodeBlock': ParagraphStyle(
            'CodeBlock', parent=base['Code'],
            fontName=FONT_NAME, fontSize=9, leading=13,
            backColor=colors.HexColor('#f8fafc'),
            borderColor=colors.HexColor('#cbd5e1'),
            borderWidth=0.5, borderPadding=6,
            leftIndent=4*mm, rightIndent=4*mm,
            spaceAfter=6,
        ),
    }
    return styles


def main():
    args = parse_args()
    src = args.input
    out_dir = args.out_dir or src.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    html_out = out_dir / f"{src.stem}.html"
    pdf_out = out_dir / f"{src.stem}.pdf"

    if not src.exists():
        print(f"[ERROR] 源文件不存在: {src}")
        sys.exit(1)

    print(f"读源: {src}")
    md_text = src.read_text(encoding="utf-8")
    print(f"  源大小: {len(md_text):,} chars")

    # 取标题（第一行 # 开头）
    title = src.stem
    for line in md_text.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            break

    # ===== 1. HTML =====
    if not args.pdf_only:
        print("\n[1/2] 生成 HTML...")
        full_html, body = md_to_html(md_text, title=title)
        html_out.write_text(full_html, encoding="utf-8")
        print(f"[OK] HTML 已写入: {html_out}")
        print(f"  HTML 大小: {len(full_html):,} chars")
    else:
        # 仍然需要 body 给 PDF 用
        full_html, body = md_to_html(md_text, title=title)

    # ===== 2. PDF =====
    if not args.html_only and not args.no_pdf:
        print("\n[2/2] 生成 PDF...")
        try:
            styles = make_styles()
            elements = html_to_pdf_elements(body, styles)

            doc = SimpleDocTemplate(
                str(pdf_out),
                pagesize=A4,
                leftMargin=1.8*cm, rightMargin=1.8*cm,
                topMargin=2.0*cm, bottomMargin=2.2*cm,
                title=title,
                author="自媒体AI老徐的商业模式诊断 skill",
            )
            doc.build(elements)
            size = pdf_out.stat().st_size
            print(f"[OK] PDF 已写入: {pdf_out}")
            print(f"  PDF 大小: {size:,} bytes ({size/1024:.1f} KB)")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[ERROR] PDF 转换失败: {e}")

    print("\n[DONE] 全部完成")


if __name__ == "__main__":
    main()
