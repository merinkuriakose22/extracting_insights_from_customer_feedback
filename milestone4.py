import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from wordcloud import WordCloud
import numpy as np

# ── Page Configuration ──────────────────────────────────────
st.set_page_config(
    page_title="ReviewSense Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────
st.markdown("""
<style>
.main-header { font-size: 3rem; color: #1f77b4; text-align: center; margin-bottom: 2rem; }
.metric-card { background-color: #f0f2f6; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# ── Data Loading ─────────────────────────────────────────────
@st.cache_data
def load_data():
    # Primary dataset with sentiment results
    df = pd.read_csv("Milestone2_Sentiment_Results_new.csv")
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['sentiment'] = df['sentiment'].str.capitalize()
    return df

@st.cache_data
def load_keywords():
    # Keyword insights dataset
    try:
        return pd.read_csv("Milestone3_Keyword_Insights.csv")
    except:
        return pd.DataFrame()

df = load_data()
keywords_df = load_keywords()

# ── Sidebar Filters ──────────────────────────────────────────
st.sidebar.header("🔍 Filters")
sentiment_filter = st.sidebar.multiselect("Select Sentiment", options=["Positive", "Negative", "Neutral"], default=["Positive", "Negative", "Neutral"])
product_filter = st.sidebar.multiselect("Select Product", options=sorted(df["product"].unique()), default=sorted(df["product"].unique()))

# ── Filter Application ───────────────────────────────────────
filtered_df = df[
    (df["sentiment"].isin(sentiment_filter)) &
    (df["product"].isin(product_filter))
].copy()

# ── Main Dashboard ───────────────────────────────────────────
st.markdown('<h1 class="main-header">📊 ReviewSense Customer Feedback Dashboard</h1>', unsafe_allow_html=True)

# Metrics Summary
col1, col2, col3, col4 = st.columns(4)
total_reviews = len(filtered_df)
pos_count = len(filtered_df[filtered_df['sentiment'] == 'Positive'])
neg_count = len(filtered_df[filtered_df['sentiment'] == 'Negative'])
neu_count = len(filtered_df[filtered_df['sentiment'] == 'Neutral'])

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total Reviews", total_reviews)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Positive", f"{(pos_count/total_reviews*100 if total_reviews > 0 else 0):.1f}%", delta=f"{pos_count}")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Negative", f"{(neg_count/total_reviews*100 if total_reviews > 0 else 0):.1f}%", delta=f"{neg_count}", delta_color="inverse")
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Neutral", f"{(neu_count/total_reviews*100 if total_reviews > 0 else 0):.1f}%", delta=f"{neu_count}", delta_color="off")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Visualizations ──
st.write("---")
c_left, c_right = st.columns(2)

with c_left:
    st.subheader("😊 Sentiment Distribution")
    if not filtered_df.empty:
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        counts = filtered_df["sentiment"].value_counts().reindex(["Positive", "Negative", "Neutral"]).fillna(0)
        ax1.bar(counts.index, counts.values, color=['#4CAF50', '#F44336', '#9E9E9E'])
        st.pyplot(fig1)

with c_right:
    # UPDATED: Matches your Confidence Score Distribution screenshot
    st.subheader("🎯 Confidence Score Distribution")
    if not filtered_df.empty:
        fig_hist, ax_hist = plt.subplots(figsize=(8, 5))
        ax_hist.hist(filtered_df["confidence_score"], bins=20, color='cornflowerblue', edgecolor='black', alpha=0.7)
        ax_hist.set_xlabel("Confidence Score (-1.0 to 1.0)")
        ax_hist.set_ylabel("Count")
        st.pyplot(fig_hist)

# ── Trends Over Time ──
st.write("---")
st.subheader("📈 Sentiment Trends Over Time")
if not filtered_df.empty:
    filtered_df['month_str'] = filtered_df['date'].dt.to_period('M').astype(str)
    trend = filtered_df.groupby(['month_str', 'sentiment']).size().unstack(fill_value=0)
    fig_trend, ax_trend = plt.subplots(figsize=(12, 5))
    trend.plot(kind='line', marker='o', ax=ax_trend, color=['#F44336', '#9E9E9E', '#4CAF50'])
    plt.xticks(rotation=45)
    st.pyplot(fig_trend)

# ── Product Heatmap ──
st.write("---")
st.subheader("📱 Product Sentiment Heatmap")
if not filtered_df.empty:
    product_sent = filtered_df.groupby('product')['sentiment'].value_counts().unstack(fill_value=0)
    for col in ['Positive', 'Neutral', 'Negative']:
        if col not in product_sent.columns: product_sent[col] = 0
    
    # Large figure height to handle many products
    fig_hm, ax_hm = plt.subplots(figsize=(10, 16)) 
    sns.heatmap(product_sent[['Positive', 'Neutral', 'Negative']], annot=True, fmt="d", cmap="RdYlGn", ax=ax_hm)
    st.pyplot(fig_hm)

# ── Keywords Section ──
st.write("---")
st.subheader("🔑 Keyword Insights")
if not keywords_df.empty:
    col_bar, col_wc = st.columns([2, 1])
    with col_bar:
        fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
        ax_bar.barh(keywords_df['keyword'].head(15), keywords_df['frequency'].head(15), color='skyblue')
        ax_bar.invert_yaxis()
        st.pyplot(fig_bar)
    with col_wc:
        word_freq = dict(zip(keywords_df['keyword'], keywords_df['frequency']))
        wc = WordCloud(width=600, height=400, background_color='white').generate_from_frequencies(word_freq)
        fig_wc, ax_wc = plt.subplots()
        ax_wc.imshow(wc)
        ax_wc.axis('off')
        st.pyplot(fig_wc)

# ── Export Options ──
st.write("---")
with st.expander("📋 View Raw Data"):
    st.dataframe(filtered_df.head(50), use_container_width=True)

st.subheader("📥 Export Options")
c_dl1, c_dl2 = st.columns(2)
with c_dl1:
    st.download_button("Download Filtered Reviews", filtered_df.to_csv(index=False).encode('utf-8'), "ReviewSense_Filtered.csv", "text/csv")
with c_dl2:
    if not keywords_df.empty:
        st.download_button("Download Keyword List", keywords_df.to_csv(index=False).encode('utf-8'), "ReviewSense_Keywords.csv", "text/csv")

st.success("✅ Dashboard ready! Use the sidebar to explore different views.")