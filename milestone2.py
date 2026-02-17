# ======================================================
# ReviewSense – Milestone 2 (Integrated Version)
# Data Loading, Sentiment Analysis & Visualization
# ======================================================

import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import os

def get_sentiment(text):
    """
    Analyzes text to return sentiment label and polarity score.
    """
    try:
        # Fixed: Corrected attribute name from 'polarily' to 'polarity'
        analysis = TextBlob(str(text))
        score = analysis.sentiment.polarity
        
        if score > 0:
            return "positive", score
        elif score < 0:
            return "negative", score
        else:
            return "neutral", score
    except Exception:
        # Fallback for empty or unreadable text
        return "neutral", 0.0

def main():
    # 1. Path Setup (Using your established working directory)
    input_file = "Milestone1_cleaned_feedback.csv"
    output_file = "Milestone2_Sentiment_Results_new.csv"
    chart_file = "sentiment_bar_chart.png"

    # 2. Data Ingestion
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found. Ensure Milestone 1 has been run.")
        return

    print("📂 Loading cleaned feedback data...")
    df = pd.read_csv(input_file)

    # 3. Sentiment Processing
    print("🧠 Analyzing sentiment across 5000 records...")
    # Applies sentiment logic and maps results to two new columns
    results = df["clean_feedback"].apply(lambda x: pd.Series(get_sentiment(x)))
    df[["sentiment", "confidence_score"]] = results

    # 4. Save Processed Dataset
    df.to_csv(output_file, index=False)
    print(f"✅ Milestone 2 results saved to: {output_file}")

    # 5. Data Visualization
    print("📊 Generating sentiment distribution chart...")
    sentiment_counts = df['sentiment'].value_counts()
    
    plt.figure(figsize=(8, 5))
    colors = ['#2ca02c', '#d62728', '#7f7f7f']  # Green, Red, Gray
    sentiment_counts.plot(kind='bar', color=colors)
    
    plt.title('ReviewSense: Customer Sentiment Summary', fontsize=14, fontweight='bold')
    plt.xlabel('Sentiment Category', fontsize=12)
    plt.ylabel('Number of Reviews', fontsize=12)
    plt.xticks(rotation=0)

    # Add count labels on top of bars
    for i, count in enumerate(sentiment_counts):
        plt.text(i, count + 20, str(count), ha='center', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig(chart_file, dpi=100)
    print(f"🖼️  Chart saved successfully as: {chart_file}")

    # 6. Final Report for Presentation
    print("\n--- Project Summary for Week 2 ---")
    print(df['sentiment'].value_counts())
    print("\nSample Output:")
    print(df[["clean_feedback", "sentiment", "confidence_score"]].head())

if __name__ == "__main__":
    main()