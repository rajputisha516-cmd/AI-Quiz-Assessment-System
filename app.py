import streamlit as st
import time


from core.quiz_engine import QuizEngine
from utils.helpers import log_attempt
from utils.difficulty_logic import get_next_difficulty
from ml.skill_prediction import predict_skill_level

from ui.styles import load_styles
from ui.components import render_title, render_question, render_result


# ================= PAGE SETUP =================
st.set_page_config(
    page_title="AI Quiz Assessment System",
    layout="wide"
)

load_styles()
engine = QuizEngine()


# ================= CONSTANTS =================
SINGLE_QUIZ_QUESTIONS = 30
COMBINED_QUIZ_QUESTIONS = 50


# ================= SESSION STATE =================
SESSION_DEFAULTS = {
    "quiz_started": False,
    "quiz_completed": False,
    "current_question": None,
    "start_time": None,
    "difficulty": "easy",
    "quiz_type": None,
    "required_questions": 0,
    "asked_questions": set(),
    "show_result": False,
    "last_result": None,
    "correct_count": 0
}

for k, v in SESSION_DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ================= LAYOUT =================
left, center, right = st.columns([1, 3, 1])


# ================= LEFT PANEL =================
with left:
    st.markdown("<div class='left-panel'>", unsafe_allow_html=True)

    st.markdown("### ⚙️ Quiz Settings")

    quiz_type = st.radio(
        "Quiz Mode",
        ["Single Skill", "Combined (Interview Mode)"]
    )

    if quiz_type == "Single Skill":
        subject = st.selectbox("Subject", ["Python", "ML", "SQL"])
        required_questions = SINGLE_QUIZ_QUESTIONS
    else:
        subject = "Combined"
        required_questions = COMBINED_QUIZ_QUESTIONS

    if st.button("🔄 Reset Quiz"):
        for k, v in SESSION_DEFAULTS.items():
            st.session_state[k] = v
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ================= CENTER PANEL =================
with center:
    st.markdown("<div class='center-panel'>", unsafe_allow_html=True)

    render_title()

    # ---------- START QUIZ ----------
    if not st.session_state.quiz_started and not st.session_state.quiz_completed:
        if st.button("▶️ Start Quiz"):
            st.session_state.quiz_started = True
            st.session_state.quiz_type = quiz_type
            st.session_state.required_questions = required_questions
            st.session_state.difficulty = "easy"
            st.session_state.asked_questions = set()
            st.session_state.correct_count = 0
            st.session_state.show_result = False
            st.session_state.last_result = None

            qs = engine.get_questions(
                subject=subject,
                difficulty=st.session_state.difficulty,
                asked_questions=st.session_state.asked_questions,
                n=1
            )

            if not qs:
                st.error("No questions available.")
                st.stop()

            st.session_state.current_question = qs[0]
            st.session_state.start_time = time.time()
            st.rerun()

    # ---------- QUESTION FLOW ----------
    if st.session_state.quiz_started and st.session_state.current_question:
        q = st.session_state.current_question

        render_question(q["question"])

        options = [
            q["option_a"],
            q["option_b"],
            q["option_c"],
            q["option_d"]
        ]
        options = [o for o in options if isinstance(o, str) and o.strip()]

        # ensure minimum 4 options for UI consistency
        while len(options) < 4:
            options.append("None of these")

        selected = st.radio(
            "Choose an answer:",
            options,
            index=None
        )

        col_submit, col_next = st.columns(2)

        with col_submit:
            submit = st.button("✅ Submit Answer")

        with col_next:
            next_btn = st.button("➡️ Next Question")

        # ---------- SUBMIT ----------
        if submit and not st.session_state.show_result:
            if selected is None:
                st.warning("Please select an option.")
                st.stop()

            time_taken = round(time.time() - st.session_state.start_time, 2)
            correct_answer = q[f"option_{q['correct_option']}"]
            correct = selected == correct_answer

            if correct:
                st.session_state.correct_count += 1

            st.session_state.last_result = {
                "correct": correct,
                "correct_answer": correct_answer,
                "time_taken": time_taken
            }

            log_attempt(
                subject=q["subject"],
                topic=q["topic"],
                difficulty=q["difficulty"],
                correct=correct,
                time_taken=time_taken
            )

            st.session_state.asked_questions.add(q["question"])

            if st.session_state.quiz_type == "Single Skill":
                st.session_state.difficulty = get_next_difficulty(
                    current_difficulty=st.session_state.difficulty,
                    subject=subject
                )


            st.session_state.show_result = True
            st.rerun()

        # ---------- RESULT ----------
        if st.session_state.show_result:
            r = st.session_state.last_result
            render_result(
                r["correct"],
                r["correct_answer"],
                r["time_taken"]
            )

        # ---------- NEXT ----------
        if next_btn and st.session_state.show_result:

            # 🔒 ONLY VALID QUIZ END CONDITION
            if len(st.session_state.asked_questions) >= st.session_state.required_questions:
                st.session_state.quiz_completed = True
                st.session_state.quiz_started = False
                st.rerun()

            # try with current difficulty
            qs = engine.get_questions(
                subject=subject,
                difficulty=st.session_state.difficulty,
                asked_questions=st.session_state.asked_questions,
                n=1
            )

            # fallback: ignore difficulty (NEVER END QUIZ HERE)
            if not qs:
                qs = engine.get_questions(
                    subject=subject,
                    difficulty=None,
                    asked_questions=st.session_state.asked_questions,
                    n=1
                )

            # absolute safety (data exhausted)
            if not qs:
                st.warning("Question pool exhausted. Please reset quiz.")
                st.session_state.quiz_started = False
                st.stop()

            st.session_state.current_question = qs[0]
            st.session_state.start_time = time.time()
            st.session_state.show_result = False
            st.session_state.last_result = None
            st.rerun()

    # ---------- QUIZ COMPLETED ----------
    if st.session_state.quiz_completed:
        st.balloons()

        st.markdown(
            "<div style='color:#C4B5FD; font-weight:600;'>🎉 Quiz Completed</div>",
            unsafe_allow_html=True
        )

        assessment = predict_skill_level("data/user_attempts.csv")

        if assessment.get("show_level"):
            st.markdown(
                f"<div style='color:#DDD6FE;'>Skill Level: <b>{assessment['level']}</b></div>",
                unsafe_allow_html=True
            )
        else:
            st.info(assessment["message"])

    st.markdown("</div>", unsafe_allow_html=True)


# ================= RIGHT PANEL =================
with right:
    st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

    st.markdown("### 📊 Progress")

    st.write("Attempted:", len(st.session_state.asked_questions))
    st.write("Correct:", st.session_state.correct_count)
    st.write("Total:", st.session_state.required_questions)

    if len(st.session_state.asked_questions) > 0:
        acc = (st.session_state.correct_count / len(st.session_state.asked_questions)) * 100
        st.write(f"Accuracy: {acc:.1f}%")

    if st.session_state.quiz_completed:
        st.markdown(
            "<div style='color:#C4B5FD; font-weight:600;'>✔ Session Summary Ready</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
