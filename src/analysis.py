from pathlib import Path
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from sklearn.feature_extraction.text import CountVectorizer
import networkx as nx

from sklearn.feature_extraction.text import TfidfVectorizer

# ==========================================================
# Folder Output
# ==========================================================

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# ==========================================================
# Load Processed Data
# ==========================================================

def load_processed_documents():

    file_path = Path("data/processed/processed_documents.xlsx")

    df = pd.read_excel(file_path)

    # Hapus baris yang tokennya kosong
    df = df.dropna(subset=["Tokens"])

    return df


# ==========================================================
# Word Frequency
# ==========================================================

def word_frequency(df):

    all_tokens = []

    for tokens in df["Tokens"]:

        # Pastikan bertipe string
        if not isinstance(tokens, str):
            continue

        token_list = [
            token.strip()
            for token in tokens.split(",")
            if token.strip() != ""
        ]

        all_tokens.extend(token_list)

    counter = Counter(all_tokens)

    return counter


# ==========================================================
# Save Top Words
# ==========================================================

def save_top_words(counter, top_n=20):

    top_words = counter.most_common(top_n)

    result = pd.DataFrame(
        top_words,
        columns=["Word", "Frequency"]
    )

    output_file = OUTPUT_DIR / "top_words.xlsx"

    result.to_excel(output_file, index=False)

    print(f"Saved : {output_file}")

    return result


# ==========================================================
# Plot Top Words
# ==========================================================

def plot_top_words(df):

    plt.figure(figsize=(12, 6))

    plt.bar(df["Word"], df["Frequency"])

    plt.title("Top 20 Most Frequent Words")

    plt.xlabel("Word")

    plt.ylabel("Frequency")

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    output_file = OUTPUT_DIR / "top_words.png"

    plt.savefig(output_file, dpi=300)

    plt.close()

    print(f"Saved : {output_file}")

# ==========================================================
# Word Cloud
# ==========================================================

def create_wordcloud(counter):

    print("\nCreating Word Cloud...")

    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        max_words=200
    ).generate_from_frequencies(counter)

    plt.figure(figsize=(14,7))

    plt.imshow(wordcloud, interpolation="bilinear")

    plt.axis("off")

    plt.tight_layout()

    output_file = OUTPUT_DIR / "wordcloud.png"

    plt.savefig(output_file, dpi=300)

    plt.close()

    print(f"Saved : {output_file}")

# ==========================================================
# Bigram
# ==========================================================

def create_bigram(df, top_n=20):

    print("\nCreating Bigram...")

    vectorizer = CountVectorizer(
        ngram_range=(2, 2)
    )

    X = vectorizer.fit_transform(df["Processed Text"])

    words = vectorizer.get_feature_names_out()

    frequencies = X.sum(axis=0).A1

    bigram_df = pd.DataFrame({
        "Bigram": words,
        "Frequency": frequencies
    })

    bigram_df = (
        bigram_df
        .sort_values("Frequency", ascending=False)
        .head(top_n)
    )

    output_file = OUTPUT_DIR / "bigram.xlsx"

    bigram_df.to_excel(output_file, index=False)

    print(f"Saved : {output_file}")

    return bigram_df

# ==========================================================
# Plot Bigram
# ==========================================================

def plot_bigram(bigram_df):

    print("\nCreating Bigram Plot...")

    plt.figure(figsize=(12, 8))

    # Urutkan supaya frekuensi terbesar di atas
    plot_df = bigram_df.sort_values("Frequency")

    plt.barh(
        plot_df["Bigram"],
        plot_df["Frequency"]
    )

    plt.xlabel("Frequency", fontsize=12)
    plt.ylabel("Bigram", fontsize=12)
    plt.title("Top 20 Most Frequent Bigrams", fontsize=14)

    plt.grid(axis="x", linestyle="--", alpha=0.3)

    plt.tight_layout()

    output_file = OUTPUT_DIR / "bigram.png"

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved : {output_file}")

# ==========================================================
# TF-IDF
# ==========================================================

def create_tfidf(df, top_n=20):

    print("\nCalculating TF-IDF...")

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(
        df["Processed Text"]
    )

    feature_names = vectorizer.get_feature_names_out()

    tfidf_scores = tfidf_matrix.mean(axis=0).A1

    tfidf_df = pd.DataFrame({
        "Word": feature_names,
        "TF-IDF Score": tfidf_scores
    })

    tfidf_df = (
        tfidf_df
        .sort_values(
            "TF-IDF Score",
            ascending=False
        )
        .head(top_n)
    )

    output_file = OUTPUT_DIR / "tfidf.xlsx"

    tfidf_df.to_excel(
        output_file,
        index=False
    )

    print(f"Saved : {output_file}")

    return tfidf_df

# ==========================================================
# Plot TF-IDF
# ==========================================================

def plot_tfidf(tfidf_df):

    print("\nCreating TF-IDF Plot...")

    plt.figure(figsize=(12,8))

    plot_df = tfidf_df.sort_values(
        "TF-IDF Score"
    )

    plt.barh(
        plot_df["Word"],
        plot_df["TF-IDF Score"]
    )

    plt.xlabel("TF-IDF Score")

    plt.ylabel("Word")

    plt.title("Top 20 TF-IDF Words")

    plt.grid(
        axis="x",
        linestyle="--",
        alpha=0.3
    )

    plt.tight_layout()

    output_file = OUTPUT_DIR / "tfidf.png"

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved : {output_file}")

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Loading Processed Documents...")
    print("=" * 60)

    df = load_processed_documents()

    print(f"Documents : {len(df)}")

    print("\nCalculating Word Frequency...")

    counter = word_frequency(df)

    print("\nSaving Top Words...")

    top_words = save_top_words(counter)

    print("\nCreating Plot...")

    plot_top_words(top_words)
    create_wordcloud(counter)
    bigram = create_bigram(df)
    plot_bigram(bigram)
    tfidf = create_tfidf(df)
    plot_tfidf(tfidf)

    print("\nTop 20 Most Frequent Words")

    print(top_words)

    print("\nFinished!")