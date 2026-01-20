import streamlit as st

def render_title():
    st.markdown(
        "<div class='app-title'>🧠 AI Quiz Assessment System</div>",
        unsafe_allow_html=True
    )

def render_question(text):
    st.markdown(
        f"<div class='question-box'>{text}</div>",
        unsafe_allow_html=True
    )

def render_result(correct, correct_answer, time_taken):
    if correct:
        st.success("✅ Correct Answer")
    else:
        st.error(f"❌ Wrong Answer | Correct: {correct_answer}")

    st.caption(f"⏱ Time taken: {time_taken} seconds")
