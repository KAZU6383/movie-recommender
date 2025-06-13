import streamlit as st

# ✅ ページ設定は一番上で
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

# ===== モデルの読み込み（1回だけ）=====
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ===== 埋め込み & データの読み込み =====
@st.cache_data(show_spinner="🔄 映画データを読み込み中…")
def load_processed_data():
    base_path = Path(__file__).resolve().parent.parent / "embeddings"
    df = pd.read_csv(base_path / "processed_reviews.csv")
    embeddings = torch.load(base_path / "review_embeddings.pt")
    return df, embeddings

df, review_embeddings = load_processed_data()

# ===== Streamlit UI =====
st.title("🎬 Movie Recommender App")
st.markdown("映画レビューから、気分やキーワードにぴったりの映画を見つけよう！")


# 👇 このブロックをここに追加！
mood_options = [
    "--- 気分を選んでください ---",
    "元気になりたい 💪",       # energizing
    "恋愛したい気分 💕",       # romantic
    "癒されたい 🫶",           # heartwarming
    "笑いたい 😂",             # funny
    "感動したい 😭",           # emotional
    "ドキドキしたい 🔥",       # suspenseful
    "謎を解きたい 🕵️‍♂️",
    "どんでん返しを楽しみたい 🤯"
]
# キーワード変換
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


if selected_mood != "--- 気分を選んでください ---":
    query_clean = clean_text(mood_keyword_map[selected_mood])

    with st.spinner("🔍 類似映画を検索中..."):
        query_embedding = model.encode([query_clean], convert_to_tensor=True)[0]

        # 類似度計算
        cosine_scores = util.pytorch_cos_sim(query_embedding, review_embeddings)[0].cpu().numpy()
        df["similarity"] = cosine_scores

        # カスタムスコアでランキング
        df["score"] = 0.7 * df["similarity"] + 0.3 * (df["rating"] / 5)
        top_results = df.sort_values("score", ascending=False).head(10)

    # 2. ===== 表示 ===== セクションの中でポスター画像も表示
    for _, row in top_results.iterrows():
        st.subheader(row["title"])

        # 🔽 ポスター画像の表示（if available）
        poster_url = get_poster_url(row["title"])
        if poster_url:
            st.image(poster_url, width=200)

        st.markdown(f"⭐️ 評価: {row['rating']:.1f}（{int(row['rating_number']):,}件）")
        st.markdown(f"🧠 推薦スコア: {row['score']:.4f}")
        st.write(row["description"])
        st.markdown("---")
