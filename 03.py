import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
from pyecharts.charts import WordCloud, Bar, Pie, Line, Funnel, Scatter, Radar
import pyecharts.options as opts
import string


# 定义函数获取网页文本内容
def get_text_from_url(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        # 将&nbsp;替换为普通空格
        text = text.replace("&nbsp;", " ")
        return text
    except requests.RequestException as e:
        st.error(f"获取网页内容出错: {e}")
        return ""


# 定义函数进行分词和词频统计，添加标点符号过滤功能
def word_frequency(text):
    # 定义英文标点符号字符串
    punctuations = string.punctuation
    digits = string.digits
    # 定义中文标点符号字符集
    chinese_punctuations = ["！", "“", "”", "‘", "’", "（", "）", "《", "》", "【", "】", "；", "：", "。", "？", "，", "、", "、",
                            "|", "－", "…", "·"]

    words = jieba.cut(text)

    # 过滤掉英文标点符号、中文标点符号和数字
    filtered_words = [word for word in words if
                      word not in punctuations and word not in chinese_punctuations and word.strip() != "" and word not in digits]

    word_counts = Counter(filtered_words)
    return word_counts


# 定义函数绘制词云图
def draw_wordcloud(word_counts):
    wordcloud = WordCloud()
    data = [(word, count) for word, count in word_counts.most_common(20)]
    wordcloud.add("", data)
    return wordcloud


# 定义函数绘制柱状图
def draw_bar_chart(word_counts):
    bar = Bar()
    bar.add_xaxis([word for word, _ in word_counts.most_common(20)])
    bar.add_yaxis("词频", [count for _, count in word_counts.most_common(20)])
    return bar


# 定义函数绘制饼图
def draw_pie_chart(word_counts):
    pie = Pie()
    data = [(word, count) for word, count in word_counts.most_common(20)]
    pie.add("", data)
    return pie


# 定义函数绘制折线图（示例，可能不太契合词频展示但满足多种图形要求）
def draw_line_chart(word_counts):
    line = Line()
    line.add_xaxis([word for word, _ in word_counts.most_common(20)])
    line.add_yaxis("词频", [count for _, count in word_counts.most_common(20)])
    return line


# 定义函数绘制漏斗图（示例）
def draw_funnel_chart(word_counts):
    funnel = Funnel()
    data = [(word, count) for word, count in word_counts.most_common(20)]
    funnel.add("词频漏斗", data)
    return funnel


# 定义函数绘制散点图（示例）
def draw_scatter_chart(word_counts):
    scatter = Scatter()
    x_data = [i for i in range(1, 21)]
    y_data = [count for _, count in word_counts.most_common(20)]
    scatter.add_xaxis(x_data)
    scatter.add_yaxis("词频", y_data)
    return scatter


# 定义函数绘制雷达图（示例）
def draw_radar_chart(word_counts):
    radar = Radar()
    schema = [{"name": word, "max": max([count for _, count in word_counts.most_common(20)])} for word, _ in
              word_counts.most_common(20)]
    radar.add_schema(schema)
    data = [[count for _, count in word_counts.most_common(20)]]
    radar.add("词频", data)
    return radar


# Streamlit侧边栏进行图形筛选
st.sidebar.title("选择图形")
graph_type = st.sidebar.selectbox("请选择要展示的图形",
                                  ["词云图", "柱状图", "饼图", "折线图", "漏斗图", "散点图", "雷达图"])

# 文本输入框获取文章URL
url = st.text_input("请输入文章URL")
if url:
    text = get_text_from_url(url)
    word_counts = word_frequency(text)

    if graph_type == "词云图":
        wordcloud = draw_wordcloud(word_counts)
        st.components.v1.html(wordcloud.render_embed(), height=600)
    elif graph_type == "柱状图":
        bar = draw_bar_chart(word_counts)
        st.components.v1.html(bar.render_embed(), height=600)
    elif graph_type == "饼图":
        pie = draw_pie_chart(word_counts)
        st.components.v1.html(pie.render_embed(), height=600)
    elif graph_type == "折线图":
        line = draw_line_chart(word_counts)
        st.components.v1.html(line.render_embed(), height=600)
    elif graph_type == "漏斗图":
        funnel = draw_funnel_chart(word_counts)
        st.components.v1.html(funnel.render_embed(), height=600)
    elif graph_type == "散点图":
        scatter = draw_scatter_chart(word_counts)
        st.components.v1.html(scatter.render_embed(), height=600)
    elif graph_type == "雷达图":
        radar = draw_radar_chart(word_counts)
        st.components.v1.html(radar.render_embed(), height=600)
