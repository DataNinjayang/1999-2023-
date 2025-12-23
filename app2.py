import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO, StringIO
import base64
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'Source Han Sans CN']
plt.rcParams['axes.unicode_minus'] = False
sns.set(style='whitegrid', font='WenQuanYi Zen Hei', rc={'axes.unicode_minus': False})

# 页面配置
st.set_page_config(
    page_title="企业数字化转型数据查询分析系统",
    page_icon="📊📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS（新增跳转按钮样式）
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 1rem;
        color: #6C757D;
    }
    .chart-container {
        background-color: #FFFFFF;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .sidebar-title {
        font-size: 1.5rem;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .data-table {
        background-color: #FFFFFF;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #6C757D;
        font-size: 0.9rem;
    }
    .company-info-card {
        background-color: #F8F9FA;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .company-info-title {
        font-size: 1.5rem;
        color: #1E88E5;
        margin-bottom: 1rem;
        border-bottom: 1px solid #e9ecef;
        padding-bottom: 0.5rem;
    }
    .info-item {
        display: flex;
        margin-bottom: 0.8rem;
    }
    .info-label {
        font-weight: bold;
        width: 120px;
        color: #495057;
    }
    .info-value {
        flex: 1;
    }
    .tech-card {
        background-color: #FFFFFF;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        height: 100%;
    }
    .tech-title {
        font-size: 1.2rem;
        color: #1E88E5;
        margin-bottom: 0.8rem;
    }
    .tech-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .tech-label {
        font-size: 0.9rem;
        color: #6C757D;
    }
    .welcome-container {
        background-color: #F8F9FA;
        border-radius: 0.5rem;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .welcome-title {
        font-size: 2rem;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .welcome-text {
        font-size: 1.1rem;
        color: #495057;
        line-height: 1.6;
    }
    .sidebar-stats {
        background-color: #F8F9FA;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .sidebar-stat-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    .sidebar-stat-label {
        color: #495057;
    }
    .sidebar-stat-value {
        font-weight: bold;
        color: #1E88E5;
    }
    .export-container {
        background-color: #F0F8FF;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #1E88E5;
    }
    .export-title {
        font-size: 1.2rem;
        color: #1E88E5;
        margin-bottom: 0.8rem;
        font-weight: bold;
    }
    .external-link-button {
        display: inline-block;
        background-color: #1E88E5;
        color: white !important;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        text-decoration: none !important;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s;
    }
    .external-link-button:hover {
        background-color: #1565C0 !important;
        color: white !important;
    }
    /* 新增跳转按钮样式 */
    .navigate-button {
        display: inline-block;
        background-color: #28a745;
        color: white !important;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        text-decoration: none !important;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s;
        margin-top: 1rem;
    }
    .navigate-button:hover {
        background-color: #218838 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 辅助函数：将Plotly图表转换为PIL Image
def fig_to_image(fig, width=800, height=600):
    """将Plotly图表转换为PIL Image对象"""
    try:
        # 将图表保存为PNG字节流
        img_bytes = fig.to_image(format="png", width=width, height=height, scale=2)
        from PIL import Image
        img = Image.open(BytesIO(img_bytes))
        return img
    except Exception as e:
        st.warning(f"图表转换失败: {e}")
        # 创建空白图片作为备用
        from PIL import Image
        img = Image.new('RGB', (width, height), color='white')
        return img

# 辅助函数：将PIL Image转换为ReportLab可用格式
def image_to_reportlab(img, max_width=18, max_height=12):
    """将PIL Image转换为ReportLab的Image对象"""
    try:
        from reportlab.platypus import Image as RLImage
        from reportlab.lib.units import inch
        
        # 保存图片到字节流
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG', dpi=(300, 300))
        img_buffer.seek(0)
        
        # 计算缩放比例
        img_width, img_height = img.size
        width_inch = img_width / 300.0
        height_inch = img_height / 300.0
        
        # 调整大小以适应页面
        if width_inch > max_width:
            scale = max_width / width_inch
            width_inch = max_width
            height_inch = height_inch * scale
        
        if height_inch > max_height:
            scale = max_height / height_inch
            height_inch = max_height
            width_inch = width_inch * scale
        
        # 创建ReportLab Image对象
        rl_img = RLImage(img_buffer)
        rl_img.drawWidth = width_inch * inch
        rl_img.drawHeight = height_inch * inch
        
        return rl_img
    except Exception as e:
        st.warning(f"图片处理失败: {e}")
        return None

# PDF导出功能函数（彻底修复乱码问题）
def generate_pdf(df, selected_company, year_range, selected_industries):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from reportlab.pdfbase.pdfdoc import PDFDocument
        import tempfile
        import requests
        import os
        import sys
        import io

        # 检查数据是否为空
        if df.empty:
            st.error("筛选后的数据为空，无法生成PDF报告")
            return None

        # ===== 彻底修复中文字体问题 =====
        # 1. 定义更全面的中文字体路径
        font_paths = [
            # Linux
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            # Windows
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/microsoftyahei.ttf",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/simsun.ttc",
            # MacOS
            "/System/Library/Fonts/PingFang.ttc",
            "/Library/Fonts/Microsoft/SimHei.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/SourceHanSansCN-Regular.otf"
        ]
        
        # 2. 注册中文字体（增加容错）
        font_name = "ChineseFont"
        font_registered = False
        
        try:
            # 尝试注册系统中文字体
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        if font_path.endswith('.ttc'):
                            pdfmetrics.registerFont(TTFont(font_name, font_path, subfontIndex=0))
                        else:
                            pdfmetrics.registerFont(TTFont(font_name, font_path))
                        font_registered = True
                        st.success(f"成功加载系统字体: {os.path.basename(font_path)}")
                        break
                    except Exception as e:
                        continue
            
            # 3. 如果系统无中文字体，使用内置备用方案（思源黑体）
            if not font_registered:
                try:
                    # 下载思源黑体（备用方案）
                    font_url = "https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/SimplifiedChinese/SourceHanSansSC-Regular.otf"
                    response = requests.get(font_url, timeout=10)
                    if response.status_code == 200:
                        font_data = BytesIO(response.content)
                        pdfmetrics.registerFont(TTFont(font_name, font_data))
                        font_registered = True
                        st.success("成功加载备用中文字体（思源黑体）")
                except:
                    # 最终备用：使用ReportLab内置字体
                    font_name = "Helvetica"
                    st.info("未找到中文字体，将使用默认字体（部分中文可能显示为方框）")
                    
        except Exception as e:
            st.warning(f"字体注册失败: {e}")
            font_name = "Helvetica"

        # 4. 创建样式（强制指定中文字体）
        styles = getSampleStyleSheet()
        
        # 标题样式（优化中文渲染）
        title_style = ParagraphStyle(
            name='MyTitle',
            fontName=font_name,
            fontSize=22,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1E88E5'),
            spaceAfter=20,
            leading=26,
            encoding='utf-8'
        )
        
        # 副标题样式
        subtitle_style = ParagraphStyle(
            name='MySubTitle',
            fontName=font_name,
            fontSize=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#D32F2F'),
            spaceAfter=10,
            leading=22,
            encoding='utf-8'
        )
        
        # 页眉样式
        header_style = ParagraphStyle(
            name='MyHeader',
            fontName=font_name,
            fontSize=15,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#1976D2'),
            spaceAfter=8,
            leading=18,
            encoding='utf-8'
        )
        
        # 普通文本样式（中文优化）
        normal_style = ParagraphStyle(
            name='NormalCN',
            fontName=font_name,
            fontSize=12,
            alignment=TA_LEFT,
            leading=20,  # 增加行高，优化中文显示
            spaceAfter=6,
            encoding='utf-8'
        )
        
        styles.add(title_style)
        styles.add(subtitle_style)
        styles.add(header_style)
        styles.add(normal_style)

        # 创建PDF文档（指定编码）
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4, 
            rightMargin=2*cm, 
            leftMargin=2*cm, 
            topMargin=2*cm, 
            bottomMargin=2*cm,
            title=f"企业数字化转型分析报告_{selected_company if selected_company else '行业整体'}",
            author="企业数字化转型数据查询分析系统",
            encoding='utf-8'
        )
        elements = []

        # 封面（确保中文编码）
        elements.append(Paragraph("企业数字化转型数据分析报告".encode('utf-8').decode('utf-8'), title_style))
        if selected_company:
            elements.append(Paragraph(f"{selected_company} 专项分析".encode('utf-8').decode('utf-8'), subtitle_style))
        else:
            elements.append(Paragraph("行业整体分析报告".encode('utf-8').decode('utf-8'), subtitle_style))
        elements.append(Spacer(1, 20))

        # 基本信息
        elements.append(Paragraph("一、企业基本信息".encode('utf-8').decode('utf-8'), header_style))
        
        # 安全地获取数据信息
        try:
            record_count = len(df)
            company_count = df['企业名称'].nunique() if '企业名称' in df.columns else 0
            industry_count = df['行业名称'].nunique() if '行业名称' in df.columns else 0
            
            info_data = [
                ["企业名称".encode('utf-8').decode('utf-8'), selected_company or "全部企业".encode('utf-8').decode('utf-8')],
                ["年份范围".encode('utf-8').decode('utf-8'), f"{year_range[0]} - {year_range[1]}"],
                ["行业".encode('utf-8').decode('utf-8'), ", ".join(selected_industries) if selected_industries else "全部行业".encode('utf-8').decode('utf-8')],
                ["数据记录数".encode('utf-8').decode('utf-8'), f"{record_count:,} 条".encode('utf-8').decode('utf-8')],
                ["涉及企业数".encode('utf-8').decode('utf-8'), f"{company_count} 家".encode('utf-8').decode('utf-8')],
                ["涉及行业数".encode('utf-8').decode('utf-8'), f"{industry_count} 个".encode('utf-8').decode('utf-8')],
                ["报告生成时间".encode('utf-8').decode('utf-8'), datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            ]
        except Exception as e:
            info_data = [
                ["错误".encode('utf-8').decode('utf-8'), f"数据信息获取失败: {str(e)}"],
                ["报告生成时间".encode('utf-8').decode('utf-8'), datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            ]

        info_table = Table(info_data, colWidths=[3*cm, 10*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0F8FF')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
            ('TEXTENCODING', (0, 0), (-1, -1), 'utf-8')  # 指定文本编码
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 12))

        # 关键指标
        elements.append(Paragraph("二、关键指标概览".encode('utf-8').decode('utf-8'), header_style))
        
        try:
            if selected_company and '企业名称' in df.columns:
                company_data = df[df['企业名称'] == selected_company]
                if not company_data.empty and '年份' in company_data.columns:
                    latest_year = company_data['年份'].max()
                    latest_data_df = company_data[company_data['年份'] == latest_year]
                    if not latest_data_df.empty:
                        latest_data = latest_data_df.iloc[0]
                        overview_data = [
                            ["最新年份".encode('utf-8').decode('utf-8'), str(latest_year)],
                            ["最新数字化程度".encode('utf-8').decode('utf-8'), f"{latest_data.get('数字化程度', 0):.2f}"],
                            ["平均数字化程度".encode('utf-8').decode('utf-8'), f"{company_data.get('数字化程度', pd.Series([0])).mean():.2f}"],
                            ["技术种类数".encode('utf-8').decode('utf-8'), f"{latest_data.get('技术种类数', 0):.0f}"],
                            ["技术多样性".encode('utf-8').decode('utf-8'), f"{latest_data.get('技术多样性', 0):.2f}"],
                            ["累计总词频".encode('utf-8').decode('utf-8'), f"{company_data.get('总词频', pd.Series([0])).sum():.0f}"]
                        ]
                    else:
                        overview_data = [["数据".encode('utf-8').decode('utf-8'), "暂无最新年份数据".encode('utf-8').decode('utf-8')]]
                else:
                    overview_data = [["数据".encode('utf-8').decode('utf-8'), "企业数据为空".encode('utf-8').decode('utf-8')]]
            else:
                overview_data = [
                    ["企业数量".encode('utf-8').decode('utf-8'), f"{df['企业名称'].nunique() if '企业名称' in df.columns else 0} 家".encode('utf-8').decode('utf-8')],
                    ["行业数量".encode('utf-8').decode('utf-8'), f"{df['行业名称'].nunique() if '行业名称' in df.columns else 0} 个".encode('utf-8').decode('utf-8')],
                    ["平均数字化程度".encode('utf-8').decode('utf-8'), f"{df.get('数字化程度', pd.Series([0])).mean():.2f}"],
                    ["最高数字化程度".encode('utf-8').decode('utf-8'), f"{df.get('数字化程度', pd.Series([0])).max():.2f}"],
                    ["最低数字化程度".encode('utf-8').decode('utf-8'), f"{df.get('数字化程度', pd.Series([0])).min():.2f}"],
                    ["平均总词频".encode('utf-8').decode('utf-8'), f"{df.get('总词频', pd.Series([0])).mean():.0f}"]
                ]
        except Exception as e:
            overview_data = [["指标".encode('utf-8').decode('utf-8'), f"指标计算错误: {str(e)}"]]

        overview_table = Table(overview_data, colWidths=[4*cm, 6*cm])
        overview_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
            ('TEXTENCODING', (0, 0), (-1, -1), 'utf-8')
        ]))
        elements.append(overview_table)
        elements.append(Spacer(1, 12))

        # 可视化图表
        elements.append(Paragraph("三、数字化可视化数据图表".encode('utf-8').decode('utf-8'), header_style))
        
        try:
            tech_metrics = ['人工智能', '区块链', '大数据', '云计算', '物联网', '5G通信', '数字平台', '数字安全', '智慧行业应用']
            
            # 检查数据是否包含必要的列
            if selected_company and '企业名称' in df.columns and '年份' in df.columns:
                company_data = df[df['企业名称'] == selected_company]
                if not company_data.empty:
                    # 创建简单的趋势图
                    fig = go.Figure()
                    
                    # 添加总词频趋势
                    if '总词频' in company_data.columns:
                        fig.add_trace(go.Scatter(
                            x=company_data['年份'],
                            y=company_data['总词频'],
                            mode='lines+markers',
                            name='总词频',
                            line=dict(width=2)
                        ))
                    
                    # 添加数字化程度趋势
                    if '数字化程度' in company_data.columns:
                        fig.add_trace(go.Scatter(
                            x=company_data['年份'],
                            y=company_data['数字化程度'],
                            mode='lines+markers',
                            name='数字化程度',
                            line=dict(width=2)
                        ))
                    
                    fig.update_layout(
                        height=400,
                        title=f"{selected_company} 数字化趋势",
                        xaxis_title="年份",
                        yaxis_title="数值",
                        showlegend=True
                    )
                else:
                    # 创建空图表
                    fig = go.Figure()
                    fig.add_annotation(text="无企业数据", x=0.5, y=0.5, showarrow=False)
                    fig.update_layout(height=400, title="无数据")
            else:
                # 行业整体趋势
                if '年份' in df.columns and '总词频' in df.columns:
                    trend_data = df.groupby('年份')['总词频'].mean().reset_index()
                    fig = px.line(trend_data, x='年份', y='总词频', title='总词频年度趋势', markers=True)
                    fig.update_layout(height=400)
                else:
                    fig = go.Figure()
                    fig.add_annotation(text="无趋势数据", x=0.5, y=0.5, showarrow=False)
                    fig.update_layout(height=400, title="无数据")
            
            # 转换为图片
            img = fig_to_image(fig, width=800, height=400)
            rl_img = image_to_reportlab(img, max_width=16, max_height=8)
            if rl_img:
                elements.append(rl_img)
                elements.append(Spacer(1, 10))
            else:
                elements.append(Paragraph("图表生成失败".encode('utf-8').decode('utf-8'), normal_style))
                
        except Exception as e:
            elements.append(Paragraph(f"图表生成失败: {str(e)}".encode('utf-8').decode('utf-8'), normal_style))

        # 详细数据表（前20条）
        elements.append(Paragraph("四、详细数据（前20条）".encode('utf-8').decode('utf-8'), header_style))
        
        try:
            # 安全地选择显示的列
            available_cols = df.columns.tolist()
            preferred_cols = ['年份', '企业名称', '股票代码', '行业名称', '总词频', '数字化程度', '技术种类数', '技术多样性', '年度增长率']
            display_cols = [col for col in preferred_cols if col in available_cols]
            
            if not display_cols:
                display_cols = available_cols[:6]  # 取前6列作为备用
                
            if selected_company and '企业名称' in df.columns:
                detail_df = df[df['企业名称'] == selected_company][display_cols]
                if '年份' in detail_df.columns:
                    detail_df = detail_df.sort_values('年份', ascending=False)
            else:
                detail_df = df[display_cols]
                sort_cols = []
                if '行业名称' in detail_df.columns:
                    sort_cols.append('行业名称')
                if '企业名称' in detail_df.columns:
                    sort_cols.append('企业名称')
                if '年份' in detail_df.columns:
                    sort_cols.append('年份')
                if sort_cols:
                    detail_df = detail_df.sort_values(sort_cols, ascending=[True]*len(sort_cols))
            
            # 限制行数并转换为字符串（处理中文编码）
            detail_df = detail_df.head(20).astype(str)
            
            if not detail_df.empty:
                # 处理中文列名和数据的编码
                table_header = [col.encode('utf-8').decode('utf-8') for col in display_cols]
                table_data = [table_header] + [[str(cell).encode('utf-8').decode('utf-8') for cell in row] for row in detail_df.values.tolist()]
                
                # 智能自适应列宽
                col_widths = []
                for col in display_cols:
                    max_len = max([len(str(x)) for x in [col] + detail_df[col].tolist()])
                    col_widths.append(max(2*cm, min(4*cm, max_len * 0.5 * cm)))
                
                detail_table = Table(table_data, colWidths=col_widths, repeatRows=1)
                detail_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), font_name),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
                    ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#1976D2')),
                    ('TEXTENCODING', (0, 0), (-1, -1), 'utf-8')
                ]))
                elements.append(detail_table)
            else:
                elements.append(Paragraph("无详细数据可显示".encode('utf-8').decode('utf-8'), normal_style))
                
        except Exception as e:
            elements.append(Paragraph(f"详细数据表格生成失败: {str(e)}".encode('utf-8').decode('utf-8'), normal_style))
        
        elements.append(Spacer(1, 10))

        # 生成PDF（强制UTF-8编码）
        doc.build(elements)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # 验证PDF数据
        if len(pdf_data) < 100:
            st.error("生成的PDF文件无效（文件过小）")
            return None
            
        return pdf_data
        
    except Exception as e:
        st.error(f"PDF生成过程中发生错误: {str(e)}")
        import traceback
        st.error(f"详细错误信息: {traceback.format_exc()}")
        return None

# 标题和描述
st.markdown('<h1 class="main-header">企业数字化转型数据查询分析系统</h1>', unsafe_allow_html=True)
st.markdown("本系统提供企业数字化技术应用数据查询与分析功能，支持多维度数据展示和可视化分析。")

# 加载数据
@st.cache_data
def load_data():
    try:
        # 使用相对路径读取Excel文件
        file_path = "1_1999-2023.xlsx"
        # 检查文件是否存在
        if not os.path.exists(file_path):
            st.warning(f"数据文件 {file_path} 不存在，将创建示例数据用于演示")
            # 创建示例数据
            years = list(range(1999, 2024))
            industries = ['制造业', '金融业', '信息技术', '服务业', '零售业']
            companies = [f"企业{i}" for i in range(1, 51)]
            
            data = []
            for year in years:
                for industry in industries:
                    for company in companies[:10]:
                        row = {
                            '年份': year,
                            '企业名称': company,
                            '股票代码': f"{np.random.randint(100000, 999999)}",
                            '行业名称': industry,
                            '行业代码': f"{industry[:2]}{np.random.randint(10, 99)}",
                            '总词频': np.random.randint(100, 10000),
                            '人工智能': np.random.randint(0, 1000),
                            '区块链': np.random.randint(0, 500),
                            '大数据': np.random.randint(0, 1500),
                            '云计算': np.random.randint(0, 1200),
                            '物联网': np.random.randint(0, 800),
                            '5G通信': np.random.randint(0, 600),
                            '数字平台': np.random.randint(0, 900),
                            '数字安全': np.random.randint(0, 700),
                            '智慧行业应用': np.random.randint(0, 1100),
                            '企业数字化': np.random.randint(0, 1300),
                            '数字运营': np.random.randint(0, 800),
                            '数字人才': np.random.randint(0, 600),
                            '技术多样性': np.random.uniform(0, 1),
                            '技术种类数': np.random.randint(0, 10),
                            '数字化程度': np.random.uniform(0, 1),
                            '上年总词频': np.random.randint(80, 9000),
                            '年度增长率': np.random.uniform(-20, 50),
                            '行业公司数': np.random.randint(10, 100)
                        }
                        data.append(row)
            
            df = pd.DataFrame(data)
            return df
        
        df = pd.read_excel(file_path)
        
        # 数据清洗
        # 过滤掉企业名称为"0"、空值、NaN的无效记录
        df = df[~df['企业名称'].isin(['0', '', np.nan, 'nan'])]
        
        # 确保年份是整数类型
        df['年份'] = pd.to_numeric(df['年份'], errors='coerce').fillna(0).astype(int)
        
        # 确保数值列是数值类型
        numeric_cols = ['总词频', '人工智能', '区块链', '大数据', '云计算', '物联网', '5G通信', 
                        '数字平台', '数字安全', '智慧行业应用', '企业数字化', '数字运营', 
                        '数字人才', '技术多样性', '技术种类数', '数字化程度', '上年总词频', 
                        '年度增长率', '行业公司数']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 处理缺失值
        df = df.fillna(0)
        
        # 确保字符串列是字符串类型
        string_cols = ['股票代码', '企业名称', '行业代码', '行业名称']
        for col in string_cols:
            if col in df.columns:
                df[col] = df[col].astype(str)
        
        return df
    except Exception as e:
        st.error(f"加载数据失败: {e}")
        return None

# 侧边栏
st.sidebar.markdown('<h2 class="sidebar-title">查询条件</h2>', unsafe_allow_html=True)

# 加载数据
df = load_data()

if df is not None:
    # 获取所有不重复的企业名称并排序
    companies = sorted(df['企业名称'].unique())
    
    # 企业选择下拉框
    st.sidebar.subheader("企业查询")
    selected_company = st.sidebar.selectbox(
        "选择企业",
        options=[""] + companies,
        index=0
    )
    
    # 获取年份范围
    min_year = int(df['年份'].min())
    max_year = int(df['年份'].max())
    
    # 侧边栏筛选条件
    st.sidebar.subheader("年份范围")
    year_range = st.sidebar.slider(
        "选择年份范围",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    
    # 行业多选
    st.sidebar.subheader("行业选择")
    industries = sorted(df['行业名称'].unique())
    selected_industries = st.sidebar.multiselect(
        "选择行业（可多选）",
        options=industries,
        default=industries[:5] if len(industries) > 5 else industries
    )
    
    # 侧边栏数据概览
    st.sidebar.markdown('<div class="sidebar-stats">', unsafe_allow_html=True)
    st.sidebar.markdown('<h3 class="sidebar-title">数据概览</h3>', unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="sidebar-stat-item">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-stat-label">企业总数:</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="sidebar-stat-value">{df["企业名称"].nunique()}</div>', unsafe_allow_html=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="sidebar-stat-item">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-stat-label">行业总数:</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="sidebar-stat-value">{df["行业名称"].nunique()}</div>', unsafe_allow_html=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="sidebar-stat-item">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-stat-label">年份范围:</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="sidebar-stat-value">{min_year} - {max_year}</div>', unsafe_allow_html=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # PDF导出功能 - 移到侧边栏
    st.sidebar.markdown('<div class="export-container">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="export-title">📄📄 导出分析报告</div>', unsafe_allow_html=True)
    
    # 生成PDF文件名
    if selected_company:
        filename = f"{selected_company}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    else:
        filename = f"企业数字化转型数据_{year_range[0]}-{year_range[1]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    
    # 生成PDF按钮
    if st.sidebar.button("生成PDF分析报告", type="primary", use_container_width=True):
        with st.spinner("正在生成PDF报告，请稍候..."):
            try:
                # 数据筛选
                filtered_df = df[
                    (df['年份'] >= year_range[0]) & 
                    (df['年份'] <= year_range[1])
                ]
                
                if selected_industries:
                    filtered_df = filtered_df[filtered_df['行业名称'].isin(selected_industries)]
                
                # 检查筛选后的数据是否为空
                if filtered_df.empty:
                    st.sidebar.error("筛选条件无匹配数据，请调整查询条件")
                else:
                    # 生成PDF数据
                    pdf_data = generate_pdf(filtered_df, selected_company, year_range, selected_industries)
                    
                    # 显示下载按钮
                    if pdf_data:
                        st.sidebar.success("PDF报告生成成功！")
                        
                        # 创建下载按钮
                        st.sidebar.download_button(
                            label="📥📥 下载PDF文件",
                            data=pdf_data,
                            file_name=filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                    else:
                        st.sidebar.error("PDF生成失败，请稍后重试。")
                        
            except Exception as e:
                st.sidebar.error(f"生成PDF时发生错误: {str(e)}")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # ===== 添加外部链接按钮（侧边栏最后）=====
    st.sidebar.markdown("---")  # 分隔线
    st.sidebar.markdown('<h3 class="sidebar-title">系统导航</h3>', unsafe_allow_html=True)
    # 创建跳转按钮（绿色样式，与现有按钮区分）
    st.sidebar.markdown(
        '<a href="https://digital-encomy-main.streamlit.app/" target="_blank" class="navigate-button">🌐 访问数字经济主系统</a>',
        unsafe_allow_html=True
    )
    # ==========================================
    
    # 数据筛选
    filtered_df = df[
        (df['年份'] >= year_range[0]) & 
        (df['年份'] <= year_range[1])
    ]
    
    if selected_industries:
        filtered_df = filtered_df[filtered_df['行业名称'].isin(selected_industries)]
    
    # 如果选择了特定企业，则展示该企业的详细信息
    if selected_company:
        # 获取该企业的所有数据
        company_data = df[df['企业名称'] == selected_company]
        
        if not company_data.empty:
            # 获取企业基本信息
            company_info = company_data.iloc[0]
            
            # 企业基础信息卡片
            st.markdown('<div class="company-info-card">', unsafe_allow_html=True)
            st.markdown(f'<h2 class="company-info-title">{selected_company} 企业详情</h2>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="info-item">', unsafe_allow_html=True)
                st.markdown('<div class="info-label">股票代码:</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="info-value">{company_info.get("股票代码", "N/A")}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="info-item">', unsafe_allow_html=True)
                st.markdown('<div class="info-label">所属行业:</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="info-value">{company_info.get("行业名称", "N/A")}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="info-item">', unsafe_allow_html=True)
                st.markdown('<div class="info-label">行业代码:</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="info-value">{company_info.get("行业代码", "N/A")}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="info-item">', unsafe_allow_html=True)
                st.markdown('<div class="info-label">数据年份范围:</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="info-value">{company_data["年份"].min()} - {company_data["年份"].max()}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="info-item">', unsafe_allow_html=True)
                st.markdown('<div class="info-label">记录数:</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="info-value">{len(company_data)}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="info-item">', unsafe_allow_html=True)
                st.markdown('<div class="info-label">最新数字化程度:</div>', unsafe_allow_html=True)
                latest_year = company_data["年份"].max()
                latest_data = company_data[company_data["年份"] == latest_year].iloc[0]
                st.markdown(f'<div class="info-value">{latest_data.get("数字化程度", 0):.2f}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 企业数字化指标概览
            st.header("企业数字化指标概览")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="tech-card">', unsafe_allow_html=True)
                st.markdown('<div class="tech-title">总词频</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="tech-value">{company_data.get("总词频", pd.Series([0])).sum():.0f}</div>', unsafe_allow_html=True)
                st.markdown('<div class="tech-label">累计总词频</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="tech-card">', unsafe_allow_html=True)
                st.markdown('<div class="tech-title">技术种类数</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="tech-value">{latest_data.get("技术种类数", 0):.0f}</div>', unsafe_allow_html=True)
                st.markdown('<div class="tech-label">最新年份数据</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="tech-card">', unsafe_allow_html=True)
                st.markdown('<div class="tech-title">数字化程度</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="tech-value">{latest_data.get("数字化程度", 0):.2f}</div>', unsafe_allow_html=True)
                st.markdown('<div class="tech-label">最新年份数据</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="tech-card">', unsafe_allow_html=True)
                st.markdown('<div class="tech-title">技术多样性</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="tech-value">{latest_data.get("技术多样性", 0):.2f}</div>', unsafe_allow_html=True)
                st.markdown('<div class="tech-label">最新年份数据</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 技术应用趋势图表
            st.header("技术应用趋势")
            
            # 选择要展示的技术指标
            tech_metrics = ['人工智能', '区块链', '大数据', '云计算', '物联网', '5G通信', 
                            '数字平台', '数字安全', '智慧行业应用']
            
            # 创建多子图
            fig = make_subplots(
                rows=3, cols=3,
                subplot_titles=tech_metrics,
                vertical_spacing=0.08,
                horizontal_spacing=0.08
            )
            
            # 添加每个技术的趋势线
            for i, tech in enumerate(tech_metrics):
                if tech in company_data.columns:
                    row = i // 3 + 1
                    col = i % 3 + 1
                    
                    fig.add_trace(
                        go.Scatter(
                            x=company_data['年份'],
                            y=company_data[tech],
                            mode='lines+markers',
                            name=tech,
                            line=dict(width=2),
                            marker=dict(size=6)
                        ),
                        row=row, col=col
                    )
            
            # 更新布局
            fig.update_layout(
                height=800,
                title_text=f"{selected_company} 技术应用趋势",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 年度增长率图表（如果存在该列）
            if '年度增长率' in company_data.columns:
                st.header("年度增长率分析")
                
                # 创建增长率图表
                growth_fig = px.bar(
                    company_data,
                    x='年份',
                    y='年度增长率',
                    title=f"{selected_company} 年度增长率",
                    labels={'年度增长率': '增长率 (%)', '年份': '年份'},
                    color='年度增长率',
                    color_continuous_scale='RdYlGn'
                )
                
                # 添加零线
                growth_fig.add_hline(y=0, line_dash="dash", line_color="red")
                
                growth_fig.update_layout(
                    xaxis_title="年份",
                    yaxis_title="增长率 (%)"
                )
                
                st.plotly_chart(growth_fig, use_container_width=True)
            
            # 行业对比分析
            st.header("行业对比分析")
            
            # 获取同行业其他企业
            industry = company_info.get('行业名称', '')
            if industry:
                industry_companies = df[df['行业名称'] == industry]
                
                # 计算行业平均数字化程度
                industry_avg = industry_companies.groupby('年份')['数字化程度'].mean().reset_index()
                industry_avg.columns = ['年份', '行业平均']
                
                # 获取该企业的数字化程度
                company_digital = company_data[['年份', '数字化程度']]
                company_digital.columns = ['年份', '企业数字化程度']
                
                # 合并数据
                comparison_df = pd.merge(industry_avg, company_digital, on='年份', how='inner')
                
                if not comparison_df.empty:
                    # 创建对比图表
                    comparison_fig = go.Figure()
                    
                    # 添加行业平均线
                    comparison_fig.add_trace(go.Scatter(
                        x=comparison_df['年份'],
                        y=comparison_df['行业平均'],
                        mode='lines+markers',
                        name='行业平均',
                        line=dict(color='blue', width=2),
                        marker=dict(size=8)
                    ))
                    
                    # 添加企业线
                    comparison_fig.add_trace(go.Scatter(
                        x=comparison_df['年份'],
                        y=comparison_df['企业数字化程度'],
                        mode='lines+markers',
                        name=selected_company,
                        line=dict(color='red', width=2),
                        marker=dict(size=8)
                    ))
                    
                    # 更新布局
                    comparison_fig.update_layout(
                        title=f"{selected_company} 与 {industry} 行业数字化程度对比",
                        xaxis_title="年份",
                        yaxis_title="数字化程度",
                        legend_title="数据来源"
                    )
                    
                    st.plotly_chart(comparison_fig, use_container_width=True)
            
            # 企业详细数据表格
            st.header("企业详细数据")
            st.dataframe(
                company_data.sort_values('年份', ascending=False),
                use_container_width=True,
                height=400
            )
        else:
            st.warning(f"未找到企业 '{selected_company}' 的数据")
        
    else:
        # 未选择企业时，显示数据概览和说明
        st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="welcome-title">欢迎使用企业数字化转型数据查询分析系统</h2>', unsafe_allow_html=True)
        st.markdown('<p class="welcome-text">请在左侧侧边栏选择企业，查看企业详细信息和分析报告。</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 数据概览仪表盘
        st.header("数据概览仪表盘")
        
        # 创建指标卡片
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{len(df)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">记录总数</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{df["企业名称"].nunique()}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">企业数量</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{df["行业名称"].nunique()}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">行业数量</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            avg_digital = df["数字化程度"].mean()
            st.markdown(f'<div class="metric-value">{avg_digital:.2f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">平均数字化程度</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 数据表格展示
        st.header("数据详情")
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        
        # 使用Streamlit的数据表格功能
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 多维度可视化图表
        st.header("多维度可视化分析")
        
        # 创建选项卡
        tab1, tab2, tab3, tab4 = st.tabs(["总词频趋势", "技术应用对比", "行业数字化分布", "企业数字化排名"])
        
        with tab1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("总词频年度趋势")
            
            # 按年份分组计算总词频平均值
            trend_data = filtered_df.groupby('年份')['总词频'].mean().reset_index()
            
            # 创建折线图
            fig = px.line(
                trend_data, 
                x='年份', 
                y='总词频',
                title='总词频年度趋势',
                labels={'总词频': '平均总词频', '年份': '年份'},
                markers=True
            )
            
            # 添加趋势线
            fig.update_layout(
                hovermode='x unified',
                xaxis_title="年份",
                yaxis_title="平均总词频"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("各项技术应用对比")
            
            # 选择要对比的技术指标
            tech_metrics = ['人工智能', '区块链', '大数据', '云计算', '物联网', '5G通信', 
                            '数字平台', '数字安全', '智慧行业应用']
            available_tech_metrics = [tech for tech in tech_metrics if tech in filtered_df.columns]
            
            if available_tech_metrics:
                # 计算各技术指标的平均值
                tech_data = filtered_df[available_tech_metrics].mean().reset_index()
                tech_data.columns = ['技术', '平均值']
                
                # 创建柱状图
                fig = px.bar(
                    tech_data,
                    x='技术',
                    y='平均值',
                    title='各项技术应用平均值对比',
                    labels={'平均值': '平均词频', '技术': '技术类型'},
                    color='技术'
                )
                
                fig.update_layout(
                    xaxis_title="技术类型",
                    yaxis_title="平均词频",
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("无技术指标数据可显示")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("行业数字化程度分布")
            
            # 按行业分组计算数字化程度
            industry_data = filtered_df.groupby('行业名称')['数字化程度'].mean().reset_index()
            industry_data = industry_data.sort_values('数字化程度', ascending=False)
            
            # 创建水平柱状图
            fig = px.bar(
                industry_data,
                x='数字化程度',
                y='行业名称',
                title='行业数字化程度分布',
                labels={'数字化程度': '平均数字化程度', '行业名称': '行业名称'},
                orientation='h',
                color='数字化程度',
                color_continuous_scale='Blues'
            )
            
            fig.update_layout(
                xaxis_title="平均数字化程度",
                yaxis_title="行业名称",
                height=max(400, len(industry_data) * 20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab4:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("企业数字化水平排名")
            
            # 按企业分组计算数字化程度
            company_data = filtered_df.groupby('企业名称')['数字化程度'].mean().reset_index()
            company_data = company_data.sort_values('数字化程度', ascending=False).head(20)
            
            # 创建柱状图
            fig = px.bar(
                company_data,
                x='企业名称',
                y='数字化程度',
                title='企业数字化水平TOP20',
                labels={'数字化程度': '平均数字化程度', '企业名称': '企业名称'},
                color='数字化程度',
                color_continuous_scale='Viridis'
            )
            
            fig.update_layout(
                xaxis_title="企业名称",
                yaxis_title="平均数字化程度",
                xaxis={'categoryorder': 'total descending'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 相关性分析
        st.header("指标相关性分析")
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # 选择要分析相关性的指标
        all_metrics = ['人工智能', '区块链', '大数据', '云计算', '物联网', '5G通信', 
                      '数字平台', '数字安全', '智慧行业应用', '总词频', '数字化程度', '技术多样性']
        available_metrics = [metric for metric in all_metrics if metric in filtered_df.columns]
        
        correlation_metrics = st.multiselect(
            "选择要分析相关性的指标",
            options=available_metrics,
            default=available_metrics[:4] if len(available_metrics) >= 4 else available_metrics
        )
        
        if correlation_metrics:
            # 计算相关性矩阵
            correlation_df = filtered_df[correlation_metrics].corr()
            
            # 创建热力图
            fig = px.imshow(
                correlation_df,
                text_auto=True,
                aspect="auto",
                color_continuous_scale='RdBu_r',
                title="指标相关性热力图"
            )
            
            fig.update_layout(
                width=800,
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("请至少选择一个指标进行相关性分析")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 页脚
    st.markdown('<div class="footer">© 2023 企业数字化转型数据查询分析系统 | 数据更新时间: 2023-12-10</div>', unsafe_allow_html=True)
else:
    st.error("无法加载数据，请检查文件路径或文件格式是否正确。")
