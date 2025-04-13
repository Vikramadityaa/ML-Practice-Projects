from fastapi import FastAPI, Depends, HTTPException
from db_helper import get_db_session, fetch_questions, save_answer, fetch_scoreboard, register_user, authenticate_user, save_question, Question
from ai_backend import generate_question, evaluate_answer
from sqlalchemy.orm import Session
import logging
from datetime import date
from pydantic import BaseModel

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db_session)):
    return register_user(db, username, password)


@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db_session)):
    return authenticate_user(db, username, password)


@app.get("/questions")
def get_questions(topic):
    """Fetch or generate exactly 5 questions for a given topic and date."""
    today = date.today()

    with get_db_session() as db:  # Use context manager
        try:
            questions = fetch_questions(db, topic, today)
            num_questions_needed = 5 - len(questions)

            if num_questions_needed > 0:
                logger.info(f"Generating {num_questions_needed} new questions for topic {topic}")

                new_questions = [generate_question(topic) for _ in range(num_questions_needed)]

                for question_text in new_questions:
                    save_question(db, topic, question_text, today)

                questions = fetch_questions(db, topic, today)

            if questions:
                logger.info(f"Returning {len(questions)} questions for topic {topic}")
            else:
                logger.warning(f"No questions available after generation attempt.")

            # Convert SQLAlchemy objects to JSON-serializable format
            return [{"id": q.id, "topic": q.topic, "question_text": q.question_text, "date_added": str(q.date_added)}
                    for q in questions]

        except Exception as e:
            logger.error(f"Error in get_questions: {e}")
            db.rollback()  # Rollback transaction on error
            raise  # Re-raise the error after logging

class AnswerSubmission(BaseModel):
    user_id: int
    question_id: int
    answer_text: str


@app.post("/submit_answer")
def submit_answer(data: AnswerSubmission):
    with get_db_session() as db:
        question = db.query(Question).filter(Question.id == data.question_id).first()

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        evaluation =    evaluate_answer(question.question_text, data.answer_text)
        save_answer(db, data.user_id, data.question_id, data.answer_text, evaluation["score"])

        return evaluation

@app.get("/scoreboard")
def scoreboard(db: Session = Depends(get_db_session)):
    return fetch_scoreboard(db)
