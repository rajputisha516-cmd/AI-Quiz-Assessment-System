import streamlit as st

def load_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0B1220;
            color: #E5E7EB;
        }

        /* Panels */
        .left-panel, .right-panel {
            background-color: #0F172A;
            padding: 12px;
            border-radius: 10px;
        }

        .center-panel {
            background-color: #101A33;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 0 0 1px rgba(255,255,255,0.05);
        }

        /* Title */
        .app-title {
            text-align: center;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 16px;
        }

        /* Question box */
        .question-box {
            background-color: #141C2F;
            padding: 14px 16px;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 12px;
        }

        /* Buttons */
        .stButton > button {
            background-color: #8B5CF6;
            color: white;
            border-radius: 6px;
            border: none;
            font-weight: 500;
            height: 42px;
        }

        .stButton > button:hover {
            background-color: #7C3AED;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def load_login_styles():
    st.markdown("""
    <style>
    /* ===== ONLY LOGIN PAGE STYLES ===== */

    .login-bg {
        background-color: #213448;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .login-card {
        width: 420px;
        background-color: #2C3E5C;
        padding: 32px;
        border-radius: 16px;
        border: 1px solid #3E4F73;
        box-shadow: 0 14px 35px rgba(0,0,0,0.45);
    }

    .login-title {
        text-align: center;
        font-size: 26px;
        font-weight: 600;
        color: #E5E7EB;
        margin-bottom: 28px;
    }

    label {
        color: #CBD5E1 !important;
        font-size: 14px;
    }

    .stTextInput input {
        background-color: #213448;
        color: #F9FAFB;
        border-radius: 8px;
        border: 1px solid #4B5F8A;
        height: 44px;
    }

    .login-btn button {
        width: 100%;
        height: 44px;
        background-color: #7C3AED !important;
        color: white !important;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        margin-top: 18px;
    }

    .signup-btn button {
        width: 100%;
        height: 44px;
        background-color: #1E3A8A !important;
        color: white !important;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
