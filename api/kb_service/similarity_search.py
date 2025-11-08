from .Embedding import generate_embeddings
from .DBService import create_connection


def similarity_search(user_prompt, top_k=3):
    [embedding_obj] = generate_embeddings(user_prompt)
    user_prompt_embeded = embedding_obj.values
    conn = create_connection()
    cursor = conn.cursor()
    query = f"SELECT chunk from embeddings_store order by embedding <=> %s::vector limit {top_k}"
    cursor.execute(query, (user_prompt_embeded,))
    data = cursor.fetchall()
    return data

if __name__ == "__main__":
    user_prompt = "Where the nifty headed in this week ?"
    
    print(similarity_search(user_prompt))