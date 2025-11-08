from google import genai
from google.genai import types
from dotenv import load_dotenv
# from rich import print
from .DBService import create_connection
import os
import psycopg2

load_dotenv()


def generate_embeddings(user_prompt):
    client = genai.Client(
        api_key=os.getenv('GOOGLE_API_KEY'),
    )

    model = os.getenv('EMBEDDING_MODEL')

    response =  client.models.embed_content(
        model = model,
        contents = user_prompt
    )

    return response.embeddings

# embeddings = generate_embeddings("Hello, How are you ?")
def chunk_text(text, max_length=2000, overlap=400):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_length, len(text))
        chunks.append(text[start:end])
        start += max_length - overlap
    return chunks



def create_kb(data):
    chunks = chunk_text(data)
    conn = create_connection()
    cursor = conn.cursor()
    print(len(chunks))
    i=1
    for chunk in chunks:
        print(i)
        emb = generate_embeddings(chunk)
        [embedding_obj] = emb
        embedding_values = embedding_obj.values
        cursor.execute(
            "INSERT INTO embeddings_store (chunk, embedding) VALUES (%s, %s::vector)",
            (chunk, embedding_values)
        )
        i += 1
    conn.commit()
    cursor.close()
    conn.close()
    print(len(chunks))
    return len(chunks)

if __name__ == "__main__":
    with open(r"D:\GenAI_PJ\api\kb_service\assets\The Economic Times Bangalore 27 10 2025.txt", "r", encoding="utf-8") as f:
        data = f.read()
        
    