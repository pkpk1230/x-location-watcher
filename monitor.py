def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    res = requests.get(url, headers=headers)
    print("ユーザーID取得レスポンス:", res.status_code)
    print("レスポンス内容:", res.text)
    data = res.json()
    if "data" in data:
        return data["data"]["id"]
    else:
        send_to_discord("❌ ユーザーIDの取得に失敗しました。APIレスポンスを確認してください。")
        return None

def get_location(user_id):
    if user_id is None:
        return ""
    url = f"https://api.twitter.com/2/users/{user_id}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    res = requests.get(url, headers=headers)
    print("プロフィール取得レスポンス:", res.status_code)
    print("レスポンス内容:", res.text)
    data = res.json()
    if "data" in data:
        return data["data"].get("location", "")
    else:
        send_to_discord("❌ プロフィール情報の取得に失敗しました。APIレスポンスを確認してください。")
        return ""
