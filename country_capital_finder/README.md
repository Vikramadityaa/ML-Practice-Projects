# 🌍 Country Capital Finder

A simple yet powerful **Streamlit-based web app** that uses **LangChain** and the `tiiuae/falcon-7b-instruct` model to:

1. Predict the **capital** of a given country
2. Suggest the **top 10 places to visit** in that capital

---

## 🛠 Tech Stack

- **Frontend:** Streamlit (`app_country.py`)
- **LLM Backend:** LangChain + `tiiuae/falcon-7b-instruct`
- **Chain Type:** SequentialChain (multi-step reasoning)

---

## 🔁 How It Works

1. **User Input:** Enter a country's name.
   2. **Step 1 – Capital Prediction:**  
      The model returns the capital using the Falcon-7B-Instruct model.
3. **Step 2 – Places to Visit:**  
   The predicted capital is then passed into the second LLM prompt to generate the top 10 tourist attractions.

This two-step process is implemented using **LangChain's SequentialChain**, enabling the output of one prompt to feed into the next.

---

## 🚀 Run the App Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/Vikramadityaa/ML-Practice-Projects.git
   cd ML-Practice-Projects/Country_Capital_Finder
