import requests

def get_poster_url(title):
    """
    映画タイトルを入力すると、OMDb APIを使ってポスター画像のURLを返す関数。
    エラーが発生した場合や画像が見つからない場合は None を返す。
    """
    api_key = "447fcc04"
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"

    try:
        response = requests.get(url, timeout=5)  # タイムアウトを明示的に設定
        response.raise_for_status()  # HTTPステータスコード 4xx/5xx のとき例外を出す
        data = response.json()

        if data.get("Response") == "True" and data.get("Poster") != "N/A":
            return data.get("Poster")
        else:
            return None

    except requests.RequestException as e:
        print(f"⚠️ APIリクエストでエラー: {e}")
        return None
