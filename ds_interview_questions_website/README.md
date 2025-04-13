Here's a clean and structured `README.md` draft for your interview questions website project:

---

# 🧠 Daily Interview Questions Platform

An interactive web platform that helps users practice and improve their ML/DL/Python skills through daily interview-style questions. Users choose a topic, receive 5 AI-generated questions each day, submit answers, and get scored automatically. A leaderboard tracks daily performance across users (WIP).

---

## 🚀 Features

- ✅ Topic-wise daily questions (5 per day)
- ✅ AI-generated and AI-evaluated using LangChain
- ✅ User answer submission and scoring
- ⚙️ Daily scores saved and tracked per user
- 📊 Daily leaderboard (Work in Progress)
- 🔐 User registration & login (Work in Progress)

---

## 📂 Project Structure

### **A. Backend**

#### `ai_backend/`
- LangChain-powered logic
- Generates daily question sets
- Evaluates submitted answers
- Returns scores based on quality of answer

#### `backend/`
- FastAPI backend with endpoints:
  - `/register` (WIP)
  - `/login` (WIP)
  - `/get_questions` – Fetch daily questions
  - `/submit_answers` – Submit answers and get score
  - `/get_leaderboard` (WIP)

#### `db_helper/`
- Handles MySQL database logic
- Tables:
  - `users`, `questions`, `answers`, `scores`
- Key Functions:
  - `authenticate_user()` – WIP
  - `fetch_questions()`
  - `save_question()`
  - `save_answer()`
  - `fetch_scoreboard()` – WIP

---

### **B. Frontend**

#### `frontend/`
- Built using Streamlit
- Simple UI with:
  - Topic selector
  - Daily question display
  - Answer input box
  - Submit button to get score

---

## ✅ To-Do

- [ ] Complete **leaderboard** implementation
- [ ] Make **login and registration** functional
- [ ] Add **test cases** for endpoints and evaluation
- [ ] Improve **logging and error handling**

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit  
- **Backend**: FastAPI, LangChain  
- **Database**: MySQL  
- **AI Evaluation**: LangChain-based scoring logic  

---

## 📌 How to Run

> Coming Soon – Will include setup and run instructions here once deployment begins.

---

Let me know if you want a version with badges, a setup guide, or API endpoint documentation!