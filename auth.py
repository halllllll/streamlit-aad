import msal
import streamlit as st
from streamlit_server_state import server_state, server_state_lock
from cred import *

# だいたいmsのやつ https://github.com/Azure-Samples/ms-identity-python-flask-webapp-authentication

def Load_Cache():
    cache = msal.SerializableTokenCache()
    # if st.session_state.get("token_cache"):
    if server_state_lock.token_cache:
        cache.deserialize(server_state_lock.token_cache)
    return cache

def Save_Cache(cache):
    if cache.has_state_changed:
        # st.session_state["token_cache"] = cache.serialize()
        server_state_lock.token_cache = cache.serialize()

def Build_Msal_App(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY,
        client_credential=CLIENT_SECRET, token_cache=cache)

# return flow
def Build_Auth_Code_Flow(authority=None, scopes=None):
    return Build_Msal_App(authority=authority).initiate_auth_code_flow(
        scopes,
        redirect_uri=REDIRECT_URL)

def Get_Token_From_Cache(scope=None):
    cache = Load_Cache()  # This web app maintains one cache per SESSION
    cca = Build_Msal_App(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        Save_Cache(cache)
        return result


# ログインしてるかチェックとexpiredしてないかチェック
def aad_login_required(func):
    def wrapper(*args, **kwargs):
        if server_state_lock.user is not None:
            # logined?
            st.sidebar.info("ログイン済です")
            return func(*args, **kwargs)
        else:
            # expired?
            st.error("ログインしてください")
    return wrapper