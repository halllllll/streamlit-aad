import streamlit as st
from streamlit_server_state import server_state, server_state_lock
import webbrowser
import os
import auth

if server_state_lock.user is not None:
    # たぶんログイン済みなのでリダイレクトしたい
    st.write("ログイン済のようです")
    # クエリ邪魔なので消したい
    st.experimental_set_query_params()
    # リダイレクトできないので別タブで開くけどしゃーない
    webbrowser.open(auth.INDEX_URL, new=0)
else:
    try:
        cache=auth.Load_Cache()
        # st.write("server_state_lockをみてみようね")
        # st.write(f"state: {server_state_lock.state}")
        # st.write(f"redirect_uri: {server_state_lock.redirect_uri}")
        # st.write(f"scope: {server_state_lock.scope}")
        # st.write(f"auth_uri: {server_state_lock.auth_uri}")
        # st.write(f"code_verifier: {server_state_lock.code_verifier}")
        # st.write(f"nonce: {server_state_lock.nonce}")
        # st.write(f"claims_challene: {server_state_lock.claims_challenge}")

        flow = {
            "state": [server_state_lock.state],
            "redirect_uri": server_state_lock.redirect_uri,
            "scope": server_state_lock.scope, 
            "auth_uri": server_state_lock.auth_uri,
            "code_verifier": server_state_lock.code_verifier,
            "nonce": server_state_lock.nonce,
            "claims_challenge": server_state_lock.claims_challenge
        }
        result = auth.Build_Msal_App(cache=cache).acquire_token_by_auth_code_flow(auth_code_flow=flow, auth_response=st.experimental_get_query_params(), scopes=auth.SCOPE)
        if "error" in result:
            st.header("エラーが起きたよ")
            st.error(result["error"])
        else:
            server_state_lock.user = result["id_token_claims"]
            auth.Save_Cache(cache)
            st.write("ログイン成功〜")
            # ここでどうにかこうにかリダイレクトしたい
            st.experimental_set_query_params()
            st.experimental_rerun()
    except ValueError as e:
        st.error(f"Value Error: {e}")
    except Exception as e:
        st.error(f"error: {e}")







