"""
Authentication helpers for Habit Tracker using Supabase Auth.
"""

import streamlit as st
from supabase import create_client, Client


def get_supabase_client() -> Client:
    if "sb_client" not in st.session_state:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        st.session_state.sb_client = create_client(url, key)
    return st.session_state.sb_client


def sign_up(email: str, password: str):
    sb = get_supabase_client()
    return sb.auth.sign_up({"email": email, "password": password})


def sign_in(email: str, password: str):
    sb = get_supabase_client()
    res = sb.auth.sign_in_with_password({"email": email, "password": password})
    st.session_state.user = res.user
    return res


def sign_out():
    sb = get_supabase_client()
    sb.auth.sign_out()
    for key in ["user", "sb_client", "habits"]:
        st.session_state.pop(key, None)
    for key in list(st.session_state.keys()):
        if key.startswith("checkins_"):
            del st.session_state[key]


def get_current_user():
    return st.session_state.get("user")


def current_user_id():
    user = get_current_user()
    return user.id if user else None


def render_auth_gate():
    if get_current_user():
        return True

    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <h1>🌿 Habit Tracker</h1>
        <p style="color:#8a9a8a; font-style:italic;">Log in to see your own habits</p>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Log In", key="login_btn"):
            try:
                sign_in(email, password)
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")

    with tab_signup:
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password (min 6 characters)", type="password", key="signup_password")
        if st.button("Create Account", key="signup_btn"):
            try:
                sign_up(new_email, new_password)
                st.success("Account created! Check your email to confirm, then log in.")
            except Exception as e:
                st.error(f"Sign up failed: {e}")

    return False
