from langchain_huggingface import HuggingFaceEndpoint
import os
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableParallel

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Load the model from Hugging Face Hub
llm = HuggingFaceEndpoint(repo_id="tiiuae/falcon-7b-instruct",temperature= 0.7,return_full_text=False)


def generate_places_visit(country):
    country_template = PromptTemplate(input_variables=["Country"],
                                      template="What is the capital of {Country}? Provide only one word output, nothing else.")

    place_template = PromptTemplate(input_variables=["Capital"],
                                    template="What are some good places to visit in {Capital}?. Only give a list of comma separated places as output.")
    country_chain = country_template | llm | StrOutputParser()
    place_chain = place_template | llm | StrOutputParser()

    def sequential_chain(input_dict):
        # Get the capital
        capital = country_chain.invoke(input_dict)

        # Pass the capital to the places chain
        places = place_chain.invoke({"Capital": capital})

        return {"Capital": capital, "Places": places}

    # ✅ Using RunnableLambda to execute sequentially
    combined_chain = RunnableLambda(sequential_chain)
    return combined_chain.invoke({"Country": country})

if __name__ == "__main__":
    print(generate_places_visit(["India"]))