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
