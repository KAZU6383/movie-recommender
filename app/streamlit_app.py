import streamlit as st

# ✅ ページ設定（必ず最初に書く）
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")

import pandas as pd
import torch
import re
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from test_omdb import get_poster_url

# ===== テキスト前処理関数 =====
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ===== モデルの読み込み（キャッシュ）=====
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ===== データと埋め込みの読み込み =====
@st.cache_data(show_spinner="🔄 映画データを読み込み中…")
def load_processed_data():
    df = pd.read_csv("data/processed/sample_data.csv")
    emb = torch.load("embeddings/sample_embeddings.pt")
    return df, emb

df, review_embeddings = load_processed_data()

# ===== Streamlit UI =====
st.title("🎬 Movie Recommender App")
st.markdown("映画レビューから、気分やキーワードにぴったりの映画を見つけよう！")

# ==== 気分選択 ====
mood_options = [
    "--- 気分を選んでください ---",
    "元気になりたい 💪", "恋愛したい気分 💕", "癒されたい 🫶", "笑いたい 😂",
    "感動したい 😭", "ドキドキしたい 🔥", "謎を解きたい 🕵️‍♂️", "どんでん返しを楽しみたい 🤯"
]
mood_keyword_map = {
    "元気になりたい 💪": "energizing",
    "恋愛したい気分 💕": "romantic",
    "癒されたい 🫶": "heartwarming",
    "笑いたい 😂": "funny",
    "感動したい 😭": "emotional",
    "ドキドキしたい 🔥": "suspenseful",
    "謎を解きたい 🕵️‍♂️": "mysterious",
    "どんでん返しを楽しみたい 🤯": "mind-blowing"
}

selected_mood = st.selectbox("🎭 なりたい気分を選んでください", mood_options)
display_mode = st.radio("📊 表示方法を選んでください", ["スコア順に表示", "ランダムに表示"])
top_k = st.slider("🔢 表示する件数", min_value=1, max_value=20, value=5)

# ===== レコメンド処理 =====
if selected_mood != "--- 気分を選んでください ---":
    query_clean = clean_text(mood_keyword_map[selected_mood])

    with st.spinner("🔍 類似映画を検索中..."):
        query_embedding = model.encode([query_clean], convert_to_tensor=True)
        review_embeddings = review_embeddings.to(query_embedding.device)  # ⭐️ デバイス統一
        cosine_scores = util.pytorch_cos_sim(query_embedding, review_embeddings)  # (1, N)
        scores_array = cosine_scores.squeeze().cpu().numpy()

        if len(scores_array) != len(df):
            st.error("❌ スコアとデータ件数が一致しません")
            st.stop()

        df["similarity"] = scores_array
        df["score"] = 0.7 * df["similarity"] + 0.3 * (df["rating"] / 5)

        if display_mode == "スコア順に表示":
            top_results = df.sort_values("score", ascending=False).head(top_k)
        else:
            top_results = df.sample(top_k)

    # ===== 結果表示 =====
    for _, row in top_results.iterrows():
        st.subheader(row["title"])
        poster_url = get_poster_url(row["title"])
        if poster_url:
            st.image(poster_url, width=200)
        else:
            st.markdown("🖼️ ポスター画像が見つかりませんでした。")
        st.markdown(f"⭐️ 評価: {row['rating']:.1f}（{int(row['rating_number']):,}件）")
        st.markdown(f"🧠 推薦スコア: {row['score']:.4f}")
        st.write(row["description"])
        st.markdown("---")
