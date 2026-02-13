# ============================
# ReviewSense – Milestone 1
# Feedback Data Collection & Preprocessing
# ============================

import pandas as pd
import re
import string
import os

# Expanded Stopwords for better cleaning
STOPWORDS = {
    "is", "the", "and", "a", "an", "to", "of", "in", "on", "for", "with", "this",
    "that", "it", "was", "are", "as", "at", "be", "by", "from", "or", "but", "so",
    "if", "then", "there", "about", "more", "all", "any"
}

def clean_text(text):
    """
    Cleans raw text by removing URLs, numbers, punctuation, and stopwords.
    """
    # 1. Convert to lowercase and string conversion
    text = str(text).lower()
    
    # 2. Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    
    # 3. Remove numbers
    text = re.sub(r"\d+", "", text)
    
    # 4. Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # 5. Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    
    # 6. Remove Stopwords
    words = [w for w in text.split() if w not in STOPWORDS]
    
    return " ".join(words)

def main():
    # Define paths (Using the directory you specified)
    base_dir = r"C:\extracting_insights_from_customers"
    file_path_excel = os.path.join(base_dir, "ReviewSense_Customer_Feedback_5000.xlsx")
    file_path_csv = os.path.join(base_dir, "Milestone1_Cleaned_Feedback.csv")
    
    df = None

    # --- PHASE 1: Data Ingestion ---
    try:
        if os.path.exists(file_path_excel):
            print(f"📂 Reading from Excel: {file_path_excel}")
            df = pd.read_excel(file_path_excel)
        elif os.path.exists(file_path_csv):
            print(f"📂 Excel not found. Reading from existing CSV: {file_path_csv}")
            df = pd.read_csv(file_path_csv)
            
            # Check if already cleaned
            if "clean_feedback" in df.columns:
                print("✨ Data already contains cleaned feedback. Skipping processing.")
                print(df[["feedback", "clean_feedback"]].head())
                return
        else:
            raise FileNotFoundError("Neither Excel nor CSV input files were found.")

    except Exception as e:
        print(f"❌ Error during loading: {e}")
        return

    # --- PHASE 2: Data Cleaning ---
    if "feedback" not in df.columns:
        print("❌ Error: The column 'feedback' was not found in the dataset.")
        return

    print("🛠️  Preprocessing and cleaning text data...")
    df["clean_feedback"] = df["feedback"].apply(clean_text)

    # --- PHASE 3: Saving Output ---
    try:
        df.to_csv(file_path_csv, index=False)
        print("✅ Milestone 1 completed successfully!")
        print("-" * 30)
        print("PREVIEW OF CLEANED DATA:")
        print(df[["feedback", "clean_feedback"]].head())
        print("-" * 30)
        print(f"Output saved to: {file_path_csv}")
    except Exception as e:
        print(f"❌ Error saving the file: {e}")

if __name__ == "__main__":
    main()