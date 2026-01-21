# AI Quiz Assessment System

This project is an AI-based quiz assessment system built using Flask and Streamlit.

Flask is used for handling authentication (login, signup, logout) and Streamlit is
used for rendering the quiz interface. The quiz adapts its difficulty dynamically
and predicts the user's skill level using machine learning.

The project focuses on integrating multiple Python frameworks in a clean and
maintainable way.

---

## Features

- User login and signup using Flask
- Token-based access to Streamlit application
- Adaptive quiz based on difficulty progression
- Skill level prediction using ML
- Logout handled via Flask
- Modular project structure

---

## Tech Stack

- Python
- Flask
- Streamlit
- SQLite
- Machine Learning
- Git / GitHub

---

## Project Structure

AI_QUIZ_ASSESSMENT_SYSTEM/
├── app.py
├── core/
├── ml/
├── utils/
├── ui/
├── data/
├── experiments/
│ └── flask_authentication/
│ ├── auth.py
│ ├── users.db
│ ├── templates/
│ │ ├── login.html
│ │ └── signup.html
│ └── static/
│ └── styles.css
├── requirements.txt
└── README.md

---

## Application Flow

- User opens the Flask login page
- After successful login, a token is generated
- Streamlit quiz opens with token validation
- User attempts the quiz
- Skill level is calculated after quiz completion
- Logout redirects back to login page

---

## How to Run

Install dependencies: pip install -r requirements.txt

Run the application using the following command:

python experiments/flask_authentication/auth.py

Then open the application in your browser at:

http://127.0.0.1:5000

## Notes

- The Streamlit app can also be run independently using `streamlit run app.py`.
- Authentication flow is controlled by Flask.
- Token handling is intentionally kept simple for now.
- This project is primarily intended for local development and experimentation.

---

## Known Issues

- The Streamlit application can be accessed directly when run independently.
- Token validation is basic and does not include expiry handling.
- Logout currently depends on Flask terminating the Streamlit process.

---

## Limitations

- Session persistence is not implemented.
- Security mechanisms are intentionally minimal at this stage.
- The application is designed for local usage and experimentation.

---

## Future Work

- Add token expiry and session management.
- Restrict direct access to the Streamlit application.
- Improve authentication and authorization flow.
- Prepare the application for deployment.

---

## Author

Isha Rajput  
Python and AI Developer  

This project was developed as part of hands-on learning and experimentation
with Flask, Streamlit, and machine learning–based assessment systems.
