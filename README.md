# 🎬 MoodMatch - Movie Recommender Based on Your Feelings
# 🎬 MoodMatch - 気分で選ぶ映画レコメンダー

> Let your emotions choose what to watch tonight.
> 今夜観る映画は、あなたの「気分」に任せてみませんか？

---

## 🌟 Overview / 概要

**MoodMatch** is a movie recommendation app that suggests films based on your **feelings**.
Instead of endlessly scrolling through titles, just let your mood decide.

**MoodMatch** は、あなたの「気分」に合った映画をおすすめするレコメンダーアプリです。
何を見るか迷ってスクロールする時間を、もう減らしましょう。

---

## 🛠 Tech Stack / 使用技術

## 🛠 Tech Stack / 使用技術

| Area / 領域            | Tech Used / 使用技術                       |
|------------------------|--------------------------------------------|
| 💻 Frontend UI         | Streamlit                                  |
| 🧠 NLP (Embedding)     | Transformers / Sentence-BERT (HuggingFace) |
| 🗃 Vector Storage       | PyTorch (`.pt` ファイル)                   |
| 📊 Visualization       | matplotlib / seaborn                       |
| 🐍 Language            | Python 3.10

---

## 📂 Project Structure / プロジェクト構成

movie-recommender-clean/
│
├── app/                       # Streamlit frontend (UI)
│   └── streamlit_app.py
├── data/
│   └── processed/             # 処理済みレビューCSV
├── embeddings/                # 埋め込みベクトル保存
├── notebooks/                 # 分析用ノートブック
├── save_embeddings.py         # 埋め込み生成スクリプト
├── requirements.txt           # 依存パッケージ一覧
├── .gitignore
└── README.md

## 🚀 Demo / デモ画面

![App Screenshot](screenshots/demo.gif)
※ GIF または PNG 画像を `screenshots/` フォルダに保存してください。

---

## ⚙️ How to Run / アプリの起動方法

1. Clone the repository and move into it / リポジトリをクローンし、移動：

    ```bash
    git clone https://github.com/kazu6383/movie-recommender.git movie-recommender-clean
    cd movie-recommender-clean
    ```

2. Install dependencies / 依存パッケージのインストール：

    ```bash
    pip install -r requirements.txt
    ```

3. Run the app / アプリを起動：

    ```bash
    streamlit run app/streamlit_app.py
    ```

## 🎯 Purpose & Background / 目的と背景

We often find ourselves spending more time **choosing** a movie than actually **watching** it.
MoodMatch solves this problem by helping you pick a movie based on your current **mood**.

私たちは時に、映画を「観る」よりも「選ぶ」ことに時間を使ってしまいます。
MoodMatch は、そんな悩みを「気分」からのアプローチで解決します。

Also, by trusting this app,
you might discover new movies you wouldn't normally choose on your own.

このアプリに任せれば、
**今まで自分では選ばなかった新しい映画との出会い**があるかもしれません。

---

## 💡 Inspiration / 着想のきっかけ

Recommendation systems typically rely on user history and preferences.
But sometimes, that's not enough—because our **emotions change daily**.

多くのレコメンドシステムは視聴履歴や好みに依存します。
でも、私たちの「気分」は日々変わるもの。
だからこそ、MoodMatch は**今の気持ち**を重視しています。

---

## 📩 Feedback / フィードバック歓迎！

If you have any feedback or suggestions, feel free to open an issue or pull request.
ご意見・ご提案がありましたら、Issue や PR にてお気軽にどうぞ！

---

Thank you for using **MoodMatch**! 😊
MoodMatch を使っていただき、ありがとうございます！
