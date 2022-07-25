import auth
import streamlit as st
from auth import aad_login_required
from streamlit_server_state import server_state, server_state_lock
import requests


@aad_login_required
def graphcall():
    token = auth.Get_Token_From_Cache(auth.SCOPE)
    if not token:
        # ログイン情報削除
        del server_state_lock.state 
        del server_state_lock.redirect_uri
        del server_state_lock.scope
        del server_state_lock.auth_uri
        del server_state_lock.code_verifier
        del server_state_lock.nonce
        del server_state_lock.claims_challenge
        del server_state_lock.user
        st.write({"error": "ログインし直してください"})
    else:
        graph_data = requests.get(  # Use token to call downstream service
        auth.GET_ALLUSERS_ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
        st.write(graph_data)

#
# "7650345d-a939-4b3d-8b08-5285524150bd"

@aad_login_required
def teams_call():
    token = auth.Get_Token_From_Cache(auth.SCOPE)
    if not token:
        # ログイン情報削除
        del server_state_lock.state 
        del server_state_lock.redirect_uri
        del server_state_lock.scope
        del server_state_lock.auth_uri
        del server_state_lock.code_verifier
        del server_state_lock.nonce
        del server_state_lock.claims_challenge
        del server_state_lock.user
        st.write({"error": "ログインし直してください"})
    else:
        graph_data = requests.get(  # Use token to call downstream service
        auth.GET_ALLUSERS_ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
        st.write(graph_data)
    
