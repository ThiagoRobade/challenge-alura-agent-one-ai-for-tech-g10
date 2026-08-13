import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from step3_retriever import search_documents

# Carrega a GOOGLE_API_KEY do .env
load_dotenv()

def generate_agent_response(query: str, category_filter: str = None) -> dict:
    """
    Agente RAG que busca documentos relevantes e gera uma resposta contextualizada
    citando as fontes de informação.
    """
    # 1. Recupera os trechos mais relevantes do banco vetorial
    retrieved_docs = search_documents(query, k=3, category_filter=category_filter)
    
    # Fallback se não encontrar nenhum documento relevante
    if not retrieved_docs:
        return {
            "answer": "Desculpe, não encontrei nenhuma informação relevante na base de conhecimento sobre este assunto.",
            "sources": []
        }

    # 2. Constrói o bloco de contexto e extrai os metadados de origem
    context_text = ""
    sources = []
    
    for idx, doc in enumerate(retrieved_docs, 1):
        source = doc.metadata.get("source", "Documento Desconhecido")
        category = doc.metadata.get("category", "Geral")
        
        context_text += f"\n--- DOCUMENTO {idx} (Arquivo: {source} | Categoria: {category}) ---\n"
        context_text += doc.page_content + "\n"
        
        sources.append({"source": source, "category": category})

    # 3. Prompt estrito para evitar alucinações e garantir citações
    prompt = f"""Você é o Assistente Virtual Oficial corporativo de uma empresa de Androids Inteligentes.
Sua missão é responder à pergunta do colaborador estritamente com base nos documentos corporativos fornecidos no CONTEXTO.

REGRAS OBRIGATÓRIAS:
1. Responda apenas usando as informações contidas no CONTEXTO abaixo.
2. Se a informação necessária não estiver presente no CONTEXTO, diga claramente: "Não encontrei essa informação nos documentos disponíveis."
3. Seja claro, profissional, direto e amigável.
4. Sempre mencione no final da sua explicação quais documentos foram consultados.

CONTEXTO:
{context_text}

PERGUNTA DO COLABORADOR:
{query}

RESPOSTA:"""

    # 4. Inicializa o Modelo de Linguagem com alias com suporte garantido
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0.2
    )

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": sources
    }

if __name__ == "__main__":
    print("🤖 Testando o Agente Conversacional RAG...\n")
    pergunta = "Qual é o procedimento de recarga de bateria e o limite de carga rápida?"
    
    resultado = generate_agent_response(pergunta)
    
    print(f"❓ Pergunta: {pergunta}\n")
    print(f"💬 Resposta do Agente:\n{resultado['answer']}\n")
