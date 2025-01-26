from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv

# Load dotenv
load_dotenv()

# Create an instance of the OpenAI class
client = OpenAI()

# Load the tests_list.csv file
def load_lab_tests(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        # Load the CSV file and ensure required columns exist
        lab_tests_df = pd.read_csv(file_path)
        required_columns = {'Code', 'Name', 'Price'}
        if not required_columns.issubset(lab_tests_df.columns):
            raise ValueError(f"The CSV file must contain the following columns: {required_columns}")
        return lab_tests_df
    except Exception as e:
        print(f"Error loading lab test data: {e}")
        return None

# Analyze symptoms using GPT
def analyze_symptoms(api_key, symptoms_description, lab_tests_df):
    client.api_key = api_key
    generation_language = os.getenv("GENERATION_LANGUAGE")
    gpt_model = os.getenv("GPT_MODEL")


    # Generate the list of tests with code, name, and price
    lab_tests_list = "\n".join(
        f"{i+1}. Code: {row['Code']}, Name: {row['Name']}, Price: {row['Price']} UAH"
        for i, row in lab_tests_df.iterrows()
    )
    

    # Define the prompt for the GPT model
    prompt = f"""
    Based on the user symptoms, recommend according mostly possible diagnoses relevant lab tests from the following list:
    {lab_tests_list}
    
    User's symptoms:
    {symptoms_description}
    
    Provide an analysis based on medical approved research and possible diagnoses name, recommend specific tests from the list to help diagnose the issue.
    Provide reason why you decided to recommend these tests and why this diagnose is possible.
    Mark the tests that are required, important for the diagnose and should be done first and the other ones that are optional if they need.
    Provide described reason for each test.
    Provide doctor title that should user go to with provided tests result list.

    Check provided tests list and be sure that all of them are relevant to the possible diagnoses. 
    Be sure that all of them are required for the detect correct diagnose as this is important for the user health and your reputation as professional.
    Save Name, Code, and Price of the tests in result.
    Calculate price for the tests and provide the total cost.

    Return result in {generation_language}.
    """
    try:
        # Use the correct method for the updated library
        chat_completion = client.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": "You are a professional medical assistant that have great experience and reputation."},
                {"role": "user", "content": prompt}
            ]
        )

         # Extract the generated message content
        finish_reason = chat_completion.choices[0].finish_reason
        if(finish_reason == "stop"):
            data = chat_completion.choices[0].message.content
            return data
        else:
            return {"error": "Generation incomplete. Try increasing tokens or re-check the model prompt."}

    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        return None


def main():
    # Load API key and symptoms description from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    symptoms_description = os.getenv("SYMPTOMS_DESCRIPTION")
    file_path = "/app/output/tests_list.csv"  # Path to the CSV file

    if not api_key or not symptoms_description:
        print("Error: Missing required environment variables 'OPENAI_API_KEY' or 'SYMPTOMS_DESCRIPTION'.")
        return

    # Load lab tests data
    lab_tests_df = load_lab_tests(file_path)
    if lab_tests_df is None:
        print("Failed to load lab test data.")
        return
    
    # Analyze symptoms and get recommendations
    analysis = analyze_symptoms(api_key, symptoms_description, lab_tests_df)
    if analysis:
        print("\nAnalysis and Recommended Tests:\n")
        print(analysis)

if __name__ == "__main__":
    main()
