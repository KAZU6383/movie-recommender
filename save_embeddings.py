# save_embeddings.py
import pandas as pd
from sentence_transformers import SentenceTransformer
from pathlib import Path
import torch
import re

# === テキスト前処理関数 ===
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# === データ読み込み ===
csv_path = Path("data/processed/movie_reviews.csv")  # CSVの場所に注意
df = pd.read_csv(csv_path, low_memory=False)

# === 映画だけ抽出 ===
df = df[df["main_category"].str.contains("Movie|DVD", case=False, na=False)].copy()

# 必要なカラムだけ抽出・整形
df = df[["title_y", "text", "average_rating", "rating_number", "image_url", "description"]].copy()
df = df.rename(columns={"title_y": "title", "average_rating": "rating"})
df = df.dropna(subset=["title", "text", "rating", "rating_number"])

# === テキスト前処理 ===
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

df["clean_text"] = df["text"].apply(clean_text)

# === Sentence-BERT モデルで埋め込み作成 ===
print("🔍 モデルを読み込み中...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("🔄 埋め込みを計算中...")
embeddings = model.encode(df["clean_text"].tolist(), convert_to_tensor=True)

# === 保存 ===
Path("embeddings").mkdir(exist_ok=True)  # 保存先フォルダを作成

df.to_csv("embeddings/processed_reviews.csv", index=False)
torch.save(embeddings, "embeddings/review_embeddings.pt")

print("✅ 保存完了！")
print(" - reviews: embeddings/processed_reviews.csv")
print(" - vectors: embeddings/review_embeddings.pt")
