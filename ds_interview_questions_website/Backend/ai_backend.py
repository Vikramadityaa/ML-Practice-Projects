import logging
import random
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline
import json

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Hugging Face pipeline
hf_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    do_sample=True,  # Enable sampling
    temperature=0.8,  # Increase randomness
    top_p=0.9,  # Nucleus sampling
    max_new_tokens=50  # Increase variation
)
llm = HuggingFacePipeline(pipeline=hf_pipeline)


# Topics for questions
topics = ["Machine Learning", "Deep Learning", "Python"]


def generate_question(topic):
    """Generate a new question for a given topic using LangChain."""
    variations = [
        f"Create a unique and challenging {topic} question for an advanced learner.",
        f"Generate a fresh {topic} question that has not been used before.",
        f"Give me a difficult {topic} question with detailed concepts.",
        f"Formulate an innovative {topic} question to test deep understanding.",
        f"Create a tricky {topic} question that requires critical thinking."
    ]

    prompt = random.choice(variations)  # Randomize the prompt variation

    try:
        question_text = llm.invoke(
            prompt,
            do_sample=True,  # Enable sampling
            temperature=0.7,  # Increase randomness
            top_p=0.9  # Adjust nucleus sampling
        )

        if not question_text:
            raise ValueError("Generated question is empty!")

        logger.info(f"Generated question for {topic}: {question_text}")
        return question_text.strip()

    except Exception as e:
        logger.error(f"Error generating question: {e}")
        return "Could not generate a question."

evaluation_prompt = PromptTemplate(
    input_variables=["question", "answer"],
    template=(
        "You are an AI evaluator. Given the question: '{question}' and the answer: '{answer}', "
        "provide a JSON response with two keys: 'score' (integer from 0 to 10) and 'correct_answer' (string). "
        "DO NOT include any extra words or explanations. Only return JSON.\n\n"
        "Example response:\n"
        '{ "score": 8, "correct_answer": "The correct answer is 2025." }'
    )
)

def evaluate_answer(question_text, answer_text):
    """Evaluate an answer using LangChain and return a score along with a correct answer."""
    response = llm.invoke(evaluation_prompt.format(question=question_text, answer=answer_text))
    print(response)  # Debugging: Check what LLM is returning
    print(llm.invoke("Say Hello"))

    try:
        # Ensure the response is in JSON format
        response_data = json.loads(response)
        score = response_data.get("score", 0)
        correct_answer = response_data.get("correct_answer", "Not Available")
    except json.JSONDecodeError:
        # Fallback if response is not in JSON format
        score = 0
        correct_answer = "Not Available"

    logger.info(f"Evaluation: Score: {score}, Correct Answer: {correct_answer}")
    return {"score": score, "correct_answer": correct_answer}


if __name__ == "__main__":
    evaluate_answer("Which year is this?", "2025")
