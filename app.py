import streamlit as st
from src.step4_agent import generate_agent_response

# Configuração da página
st.set_page_config(
    page_title="Assistente Corporativo - Androids Inc.",
    page_icon="🤖",
    layout="wide"
)

# Título e cabeçalho
st.title("🤖 Assistente Virtual de Conhecimento Corporativo")
st.caption("Consulte manuais técnicos, diretrizes de RH, suporte e conformidade da nossa frota de Androids.")

# Barra lateral com filtros e informações
with st.sidebar:
    st.header("⚙️ Configurações & Filtros")
    category_option = st.selectbox(
        "Filtrar busca por Categoria:",
        ["Todas", "RH & Treinamento", "Suporte / Técnico", "Vendas & Produtos", "Jurídico / Compliance"]
    )
    
    selected_category = None if category_option == "Todas" else category_option

    st.markdown("---")
    st.markdown("### 📚 Base de Conhecimento")
    st.info("Sistema integrado ao RAG com banco vetorial ChromaDB e Google Gemini.")

# Inicializa o histórico de chat na sessão do Streamlit
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Olá! Sou o assistente corporativo. Como posso ajudar com os documentos de Androids hoje?"}
    ]

# Exibe mensagens do histórico
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Input de nova pergunta do usuário
if user_input := st.chat_input("Digite sua dúvida aqui..."):
    # Salva e exibe pergunta do usuário
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Resposta com spinner de carregamento
    with st.chat_message("assistant"):
        with st.spinner("Buscando nos documentos corporativos..."):
            result = generate_agent_response(user_input, category_filter=selected_category)
            answer = result["answer"]
            
            st.write(answer)
            
            # Registra a resposta no histórico da sessão
            st.session_state["messages"].append({"role": "assistant", "content": answer})
