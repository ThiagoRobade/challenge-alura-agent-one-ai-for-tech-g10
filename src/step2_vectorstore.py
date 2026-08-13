import os
import time
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from step1_ingestion import extract_and_chunk_all

# Carrega as variáveis de ambiente (.env)
load_dotenv()

DB_DIR = "./database"

def create_vector_store():
    print("📥 Extraindo os chunks dos documentos...")
    raw_chunks = extract_and_chunk_all()
    
    if not raw_chunks:
        print("⚠️ Nenhum chunk encontrado. Verifique a etapa 1.")
        return None

    print(f"🔄 Convertendo {len(raw_chunks)} chunks para o formato LangChain...")
    documents = [
        Document(page_content=chunk["text"], metadata=chunk["metadata"])
        for chunk in raw_chunks
    ]

    print("🧠 Inicializando o modelo de Embeddings (Google Gemini)...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    print("💾 Criando e preenchendo o banco vetorial (ChromaDB) com tratamento de cota...")
    
    # Reduzimos o tamanho do lote para 10 para evitar estourar o limite de tokens/requisições
    batch_size = 10
    vectorstore = None
    
    total_batches = (len(documents) + batch_size - 1) // batch_size

    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        print(f"\n📦 Processando lote {batch_num}/{total_batches} ({len(batch)} chunks)...")
        
        # Loop de retentativas para contornar o erro 429
        success = False
        attempts = 0
        max_attempts = 5
        
        while not success and attempts < max_attempts:
            try:
                if vectorstore is None:
                    vectorstore = Chroma.from_documents(
                        documents=batch,
                        embedding=embeddings,
                        persist_directory=DB_DIR
                    )
                else:
                    vectorstore.add_documents(documents=batch)
                
                success = True
                print(f"✅ Lote {batch_num} indexado com sucesso!")
                
            except Exception as e:
                attempts += 1
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    wait_time = 65
                    print(f"⚠️ Limite de cota atingo (429). Aguardando {wait_time}s antes da tentativa {attempts}/{max_attempts}...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ Erro inesperado ao processar lote: {e}")
                    raise e

        # Pausa preventiva entre lotes bem-sucedidos
        if i + batch_size < len(documents):
            time.sleep(15)

    print(f"\n🎉 Banco vetorial criado com sucesso na pasta '{DB_DIR}'!")
    return vectorstore

if __name__ == "__main__":
    create_vector_store()
