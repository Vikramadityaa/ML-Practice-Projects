import logging
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import date
from passlib.context import CryptContext
from contextlib import contextmanager

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database Setup
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/workout_base"
engine = create_engine(DATABASE_URL)
SessionLocal =   sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database transaction failed: {e}")
        raise
    finally:
        db.close()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(50))
    question_text = Column(Text)
    date_added = Column(Date, default=date.today)

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_text = Column(Text)
    score = Column(Integer)
    user = relationship("User")
    question = relationship("Question")

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_score = Column(Integer, default=0)
    user = relationship("User")

# Create tables
Base.metadata.create_all(bind=engine)

# Utility functions
def register_user(db, username, password):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"User registered: {username}")
    return {"message": "User registered successfully"}


def authenticate_user(db, username, password):
    user = db.query(User).filter(User.username == username).first()
    if user and pwd_context.verify(password, user.hashed_password):
        logger.info(f"User authenticated: {username}")
        return {"message": "Login successful", "user_id": user.id}
    logger.warning(f"Failed login attempt for username: {username}")
    return {"message": "Invalid credentials"}


def fetch_questions(db, topic=None, today=None):
    """Fetch questions from the database based on optional topic and date filters."""
    try:
        query = db.query(Question)
        if topic:
            query = query.filter(Question.topic == topic)
        if today:
            query = query.filter(Question.date_added == today)

        questions = query.all()
        logger.info(f"Fetched {len(questions)} questions for topic '{topic}' on {today}: {questions}")
        return questions
    except Exception as e:
        logger.error(f"Error fetching questions: {e}")
        return []  # Return an empty list if an error occurs


def save_question(db, topic, question_text, today):
    try:
        question = Question(topic=topic, question_text=question_text, date_added=today)
        db.add(question)
        db.commit()  # Ensure the transaction is committed
        db.refresh(question)
        logger.info(f"Saved question: {question_text} for topic: {topic} on {today}")
    except Exception as e:
        db.rollback()  # Rollback if there's an error
        logger.error(f"Error saving question: {e}")

def save_answer(db, user_id, question_id, answer_text, score):
    answer = Answer(user_id=user_id, question_id=question_id, answer_text=answer_text, score=score)
    db.add(answer)
    db.commit()
    db.refresh(answer)

    user_score = db.query(Score).filter(Score.user_id == user_id).first()
    if not user_score:
        user_score = Score(user_id=user_id, total_score=0)
        db.add(user_score)

    user_score.total_score += score
    db.commit()
    logger.info(f"Answer saved for user {user_id} with score {score}")
    return {"message": "Answer submitted and scored"}


def fetch_scoreboard(db):
    scoreboard = db.query(User.username, Score.total_score).join(Score).order_by(Score.total_score.desc()).all()
    logger.info(f"Fetched scoreboard: {scoreboard}")
    return scoreboard
