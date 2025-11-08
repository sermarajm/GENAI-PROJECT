from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from utils import extractJSON

load_dotenv()

def call_llm(user_prompt, system_prompt="You are personalized AI Assitant"):
    client = genai.Client(
        api_key=os.getenv('GOOGLE_API_KEY'),
    )
    model = "gemini-flash-latest"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        system_instruction=[
            types.Part.from_text(text=system_prompt),
        ],
    )
    response =  client.models.generate_content(
        model = model,
        contents = contents,
        config = generate_content_config
    )
    return response.text

"""
News
General
"""





def intent_classifer(user_prompt):
    system_prompt = """
        You are an intent classification assistant. 
        Your task is to analyze the user's prompt and determine whether their intent relates to the topic "News" or "General".
        If the prompt is about current events, headlines, articles, or information from news sources, classify it as "News".
        If the prompt is about general information, everyday topics, or does not fit the "news" category, classify it as "general". 
        Respond with a JSON with key of intent 

        Sample Output : 
        { 
            "intent" : "general"
        }
    """
    response = call_llm(user_prompt, system_prompt)
    return extractJSON(response)


if __name__ == "__main__":
    print(intent_classifer("Any events on todays Nifty and Nifty Bank ?"))