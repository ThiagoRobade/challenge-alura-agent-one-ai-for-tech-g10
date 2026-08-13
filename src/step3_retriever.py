import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# Carrega as variáveis de ambiente (.env)
load_dotenv()

DB_DIR = "./database"

def get_retriever(k=4, category_filter=None):
    """
    Carrega o banco vetorial ChromaDB e retorna um objeto retriever do LangChain.
    Permite filtrar por número de trechos (k) e por categoria de documento.
    """
    if not os.path.exists(DB_DIR):
        raise FileNotFoundError(f"O banco vetorial não foi encontrado em '{DB_DIR}'. Execute o step2_vectorstore.py primeiro.")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    vectorstore = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )

    search_kwargs = {"k": k}
    
    # Se for passado um filtro por categoria, aplica aos metadados
    if category_filter:
        search_kwargs["filter"] = {"category": category_filter}

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs=search_kwargs
    )
    
    return retriever

def search_documents(query: str, k=3, category_filter=None):
    """
    Realiza uma busca semântica direta e retorna os documentos encontrados com metadados.
    """
    retriever = get_retriever(k=k, category_filter=category_filter)
    docs = retriever.invoke(query)
    return docs

if __name__ == "__main__":
    print("🔍 Testando a busca semântica na base de conhecimento...")
    test_query = "Qual é o procedimento de recarga de bateria dos androids?"
    
    results = search_documents(test_query, k=2)
    
    print(f"\n❓ Pergunta de teste: '{test_query}'")
    print(f"📄 Trechos encontrados: {len(results)}\n")
    
    for idx, doc in enumerate(results, 1):
        print(f"--- Trecho {idx} ---")
        print(f"Fonte: {doc.metadata.get('source')}")
        print(f"Categoria: {doc.metadata.get('category')}")
        print(f"Conteúdo: {doc.page_content[:200]}...\n")
