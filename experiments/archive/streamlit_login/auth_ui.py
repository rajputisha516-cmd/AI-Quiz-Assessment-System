import streamlit as st
from auth.auth_db import register_user, authenticate_user, create_user_table
from ui.styles import load_login_styles

def show_auth():
    create_user_table()

    load_login_styles()

    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<div class='auth-title'>LOGIN</div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
    login = st.button("Login")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
    signup = st.button("Sign Up")
    st.markdown("</div>", unsafe_allow_html=True)

    if login:
        user = authenticate_user(username, password)
        if user:
            st.session_state.user_id = user[0]
            st.success("Login successful 🎉")
            st.rerun()
        else:
            st.error("Invalid username or password")

    if signup:
        if not username or not email or not password:
            st.warning("Fill all fields")
        else:
            success = register_user(username, email, password)
            if success:
                st.success("Account created! You can now login.")
            else:
                st.error("Username or Email already exists")

    st.markdown("</div>", unsafe_allow_html=True)
