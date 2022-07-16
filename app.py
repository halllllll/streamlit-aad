import streamlit as st
from streamlit_server_state import server_state, server_state_lock
from streamlit.server.server import Server
import msal
import auth
from auth import aad_login_required
import time
import requests
import webbrowser
from graph_apis import graphcall



def main():
    time.sleep(1)
    st.header("ログインしてないみたいだよ")
    flow = auth.Build_Auth_Code_Flow(scopes=auth.SCOPE)
    # st.subheader("flow?")
    # st.write(flow)
    url = flow['auth_uri']
    # 帰ってきたよ
    # 今度こそ倒す
    # 1. まずsessionに必要な情報を保存 なんかまとめて入れたら死ぬのかもしれないのでひとつずつ
    # と思ったが、ブラウザをリロードすると揮発するらしく、リダイレクトで帰ってきたときにsession_stateがなくなっているのはこれが原因だと思われる...
    # ということでserver-state-lockとかいう拡張をいれた
    # あと後ろのほうに処理をつけたのと、time.sleepで少し待つことにした。どうやらリンクを踏んでもrerunが走るらしく、そのときにリンク先へ飛ぶ前にflowが再発行されてしまうので、再発行されたものを取得するため。

    st.write(f'''
        <a target="_self" href="{url}">
            <button>
                login
            </button>
        </a>''', unsafe_allow_html=True
    )
    server_state_lock.state = flow["state"]
    server_state_lock.redirect_uri = flow["redirect_uri"]
    server_state_lock.scope = flow["scope"]
    server_state_lock.auth_uri = flow["auth_uri"]
    server_state_lock.code_verifier = flow["code_verifier"]
    server_state_lock.nonce = flow["nonce"]
    server_state_lock.claims_challenge = flow["claims_challenge"]

@aad_login_required
def logout():
    st.info("ログアウトするよ")
    del server_state_lock.state
    del server_state_lock.redirect_uri
    del server_state_lock.scope
    del server_state_lock.auth_uri
    del server_state_lock.code_verifier
    del server_state_lock.nonce
    del server_state_lock.claims_challenge
    del server_state_lock.user
    webbrowser.open(f"{auth.AUTHORITY}/oauth2/v2.0/logout?post_logout_redirect_uri={auth.REDIRECT_URL}")

@aad_login_required
def logined():
    # ログインしているとき
    # こっちでデータ表示して、
    # 各種APIはsidemenuにつけようかな
    user = server_state_lock.user
    name = user["name"]
    st.header(f"congratulation!!! {name} さん")
    st.button(label="GRAPH", on_click=graphcall)
    st.button(label="LOGOUT", on_click=logout)


# ページ分岐と初期化
server_state_lock.state = server_state_lock.state if isinstance(server_state_lock.state, str) else None 
server_state_lock.redirect_uri = server_state_lock.redirect_uri if isinstance(server_state_lock.redirect_uri, str) else None
server_state_lock.scope = server_state_lock.scope if isinstance(server_state_lock.scope, list) else None
server_state_lock.auth_uri = server_state_lock.auth_uri if isinstance(server_state_lock.auth_uri, str) else None
server_state_lock.code_verifier = server_state_lock.code_verifier if isinstance(server_state_lock.code_verifier, str) else None
server_state_lock.nonce = server_state_lock.nonce if isinstance(server_state_lock.nonce, str) else None
server_state_lock.claims_challenge = server_state_lock.claims_challenge if isinstance(server_state_lock.claims_challenge, str) else None
server_state_lock.user = server_state_lock.user if isinstance(server_state_lock.user, dict) else None
server_state_lock.token_cache = server_state_lock.token_cache if isinstance(server_state_lock.token_cache, str) else None

if server_state_lock.user is None:
    main()
else:
    logined()