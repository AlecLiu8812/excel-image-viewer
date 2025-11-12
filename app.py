import streamlit as st
import pandas as pd
import os
import base64

st.set_page_config(page_title="Excel 图片展示工具", page_icon="📊", layout="wide")

st.title("📊 Excel / CSV 图片展示工具")
st.write("上传包含图片链接的 Excel 或 CSV 文件，自动转换为可视化 HTML 页面。")

# 上传文件
uploaded_file = st.file_uploader("请选择文件", type=["xlsx", "xls", "csv"])

if uploaded_file:
    try:
        st.info("⏳ 正在处理文件，请稍候...")

        # 读取文件
        if uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        # 去掉 Unnamed 列
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # 转换图片链接为 HTML
        def link_to_img(val):
            if isinstance(val, str) and val.startswith("http") and \
               any(val.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]):
                return f'<img src="{val}" style="max-width:200px; max-height:200px;">'
            else:
                return val

        html_table = df.applymap(link_to_img).to_html(escape=False, index=False)

        # 拼接 HTML 内容
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>表格图片展示</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
                    padding: 20px;
                    background: #f5f5f5;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    background: white;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: center;
                    vertical-align: middle;
                }}
                th {{
                    background: #4CAF50;
                    color: white;
                    font-weight: 600;
                }}
                tr:hover {{
                    background: #f9f9f9;
                }}
                img {{
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.15);
                    transition: transform 0.2s;
                }}
                img:hover {{
                    transform: scale(1.05);
                }}
            </style>
        </head>
        <body>
            <h1 style="color: #333;">📊 表格数据展示</h1>
            {html_table}
        </body>
        </html>
        """

        # 提供下载按钮
        b64 = base64.b64encode(html_content.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="output.html">📥 下载 HTML 文件</a>'
        st.markdown(href, unsafe_allow_html=True)

        st.success("✅ 文件已成功转换！")

    except Exception as e:
        st.error(f"❌ 处理失败: {e}")
