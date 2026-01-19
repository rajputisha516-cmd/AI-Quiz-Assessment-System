import streamlit as st
import time
from core.quiz_engine import QuizEngine
from utils.helpers import log_attempt
from utils.difficulty_logic import get_next_difficulty
from ml.skill_prediction import predict_skill_level

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="AI Quiz Assessment System", layout="centered")
st.title("🧠 AI Quiz Assessment System")

engine = QuizEngine()

# ---------------- SESSION STATE INIT ----------------
defaults = {
    "quiz_started": False,
    "current_question": None,
    "start_time": None,
    "difficulty": "easy",
    "quiz_type": None,
    "asked_questions": set(),
    "show_result": False,
    "last_result": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- QUIZ TYPE ----------------
quiz_type = st.selectbox(
    "Select Quiz Type",
    ["Single Skill", "Combined (Interview Mode)"]
)

if quiz_type == "Single Skill":
    subject = st.selectbox("Select Skill", ["Python", "ML", "SQL"])
else:
    subject = "Combined"

# ---------------- RESET BUTTON ----------------
if st.button("🔄 Reset Quiz"):
    for k, v in defaults.items():
        st.session_state[k] = v
    st.rerun()

# ---------------- START QUIZ ----------------
if not st.session_state.quiz_started:
    if st.button("▶️ Start Quiz"):
        st.session_state.quiz_started = True
        st.session_state.quiz_type = quiz_type
        st.session_state.difficulty = "easy"
        st.session_state.asked_questions = set()
        st.session_state.show_result = False
        st.session_state.last_result = None

        questions = engine.get_questions(
            subject=subject,
            difficulty=st.session_state.difficulty,
            asked_questions=st.session_state.asked_questions,
            n=1
        )

        if not questions:
            st.error("No questions available.")
            st.stop()

        st.session_state.current_question = questions[0]
        st.session_state.start_time = time.time()
        st.rerun()

# ---------------- SHOW QUESTION ----------------
if st.session_state.quiz_started and st.session_state.current_question:

    q = st.session_state.current_question

    st.markdown(f"### ❓ {q['question']}")

    options = [
        q["option_a"],
        q["option_b"],
        q["option_c"],
        q["option_d"]
    ]
    options = [o for o in options if isinstance(o, str) and o.strip()]

    selected_option = st.radio(
        "Choose one:",
        options,
        index=None,
        key="option_radio"
    )

    # ---------------- SUBMIT ANSWER ----------------
    if not st.session_state.show_result:
        if st.button("✅ Submit Answer"):
            if selected_option is None:
                st.warning("⚠️ Please select an option.")
                st.stop()

            end_time = time.time()
            time_taken = round(end_time - st.session_state.start_time, 2)

            correct_answer = q[f"option_{q['correct_option']}"]
            correct = selected_option == correct_answer

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
                    st.session_state.difficulty,
                    correct,
                    time_taken
                )

            st.session_state.show_result = True
            st.rerun()

    # ---------------- SHOW RESULT ----------------
    else:
        result = st.session_state.last_result

        if result["correct"]:
            st.success("🎉 Correct Answer!")
        else:
            st.error(f"❌ Wrong Answer | Correct: {result['correct_answer']}")

        st.write(f"⏱️ Time taken: {result['time_taken']} seconds")

        if st.button("➡️ Next Question"):
            questions = engine.get_questions(
                subject=subject,
                difficulty=st.session_state.difficulty,
                asked_questions=st.session_state.asked_questions,
                n=1
            )

            # ---------- QUIZ COMPLETED ----------
            if not questions:
                st.success("🎉 Quiz Completed!")

                result = predict_skill_level("data/user_attempts.csv")

                if not result["show_level"]:
                    st.info(result["message"])
                else:
                    st.markdown("## 🧠 Skill Assessment Result")
                    st.success(f"Skill Level: **{result['level']}**")

                    if "note" in result:
                        st.caption(result["note"])

                st.session_state.quiz_started = False
                st.session_state.current_question = None
                st.stop()

            # ---------- LOAD NEXT QUESTION ----------
            st.session_state.current_question = questions[0]
            st.session_state.start_time = time.time()
            st.session_state.show_result = False
            st.session_state.last_result = None
            st.rerun()
