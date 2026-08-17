import streamlit as st
from src.step4_agent import generate_agent_response

# 1. Configuração da Página
st.set_page_config(
    page_title="CyberCore Robotics | Next-Gen Android Fleet",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicialização do Tema no Session State
if "is_dark" not in st.session_state:
    st.session_state["is_dark"] = True

# Barra Lateral (Menu & Configuração de Tema)
with st.sidebar:
    st.image("./assets/cyber_core.jpeg", use_column_width=True)
    st.markdown("<h2 style='text-align: center; color: #58A6FF; margin-top: 10px;'>CYBERCORE</h2>", unsafe_allow_html=True)
    st.caption("<p style='text-align: center; margin-top: -10px;'>Advanced Positronic Systems & Robotics</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    # Alternador de Tema via Botão Único
    theme_label = "☀️ Modo Claro" if st.session_state["is_dark"] else "🌙 Modo Escuro"
    if st.button(f"🎨 Aparência: {theme_label}", use_container_width=True):
        st.session_state["is_dark"] = not st.session_state["is_dark"]
        st.rerun()

    st.markdown("---")
    page = st.radio(
        "Navegação Corporativa:",
        ["Catálogo de Modelos", "Assistente Virtual"]
    )
    st.markdown("---")
    
    st.markdown("#### ⚡ Telemetria da Rede")
    st.markdown("• **Núcleo Positrônico:** 🟢 Online (99.98%)")
    st.markdown("• **Segurança Dogmática:** Três Leis (Nível 0)")
    st.markdown("• **Base de Conhecimento:** 150 Chunks Vetoriais")
    st.markdown("• **Firmware Homologado:** Core 4.2 LTS")

# 3. Definição Dinâmica de Cores CSS de Acordo com o Tema Escolhido
is_dark = st.session_state["is_dark"]

if is_dark:
    bg_gradient = "radial-gradient(circle at 10% 20%, #0d131f 0%, #07090e 90%)"
    text_color = "#E6EDF3"
    sidebar_bg = "#0b0f19"
    hero_bg = "linear-gradient(135deg, rgba(22, 31, 48, 0.85) 0%, rgba(13, 19, 31, 0.95) 100%)"
    hero_border = "rgba(88, 166, 255, 0.3)"
    card_bg = "rgba(22, 27, 34, 0.75)"
    card_border = "rgba(255, 255, 255, 0.08)"
    card_hover_border = "rgba(88, 166, 255, 0.6)"
    subtitle_color = "#8B949E"
    desc_color = "#C9D1D9"
    active_menu_bg = "rgba(56, 139, 253, 0.15)"
else:
    bg_gradient = "radial-gradient(circle at 10% 20%, #F8FAFC 0%, #E2E8F0 90%)"
    text_color = "#0F172A"  # Dark Slate Blue para máxima leitura
    sidebar_bg = "#FFFFFF"
    hero_bg = "linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%)"
    hero_border = "rgba(37, 99, 235, 0.25)"
    card_bg = "#FFFFFF"
    card_border = "rgba(0, 0, 0, 0.08)"
    card_hover_border = "#2563EB"
    subtitle_color = "#475569"
    desc_color = "#1E293B"
    active_menu_bg = "rgba(37, 99, 235, 0.08)"

st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@600;800;900&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">

<style>
    /* Reset & Tipografia Base */
    html, body, [class*="css"], [class*="st-"] {{
        font-family: 'Inter', sans-serif;
        color: {text_color} !important;
    }}
    
    /* Fundo da Aplicação */
    .stApp {{
        background: {bg_gradient};
    }}

    /* Barra Lateral */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid rgba(0, 0, 0, 0.1);
    }}
    
    /* Forçar cores de textos e títulos */
    h1, h2, h3, h4, h5, h6, p, li, span, label, div.stMarkdown, [data-testid="stMarkdownContainer"] {{
        color: {text_color} !important;
    }}

    /* Títulos Principais Futuristas */
    h1, h2, h3 {{
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 0.8px;
    }}
    
    h4, h5, h6 {{
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: 0.3px;
    }}

    /* Hero Banner Principal */
    .hero-container {{
        background: {hero_bg};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid {hero_border};
        border-radius: 16px;
        padding: 30px 36px;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    }}
    
    .hero-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 2.1rem;
        font-weight: 900;
        background: linear-gradient(90deg, #2563EB 0%, #38BDF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }}
    
    .hero-subtitle {{
        font-family: 'Space Grotesk', sans-serif;
        color: {subtitle_color} !important;
        font-size: 1.05rem;
        margin-bottom: 12px;
    }}

    /* Cards de Produtos / Modelos */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {{
        background: {card_bg} !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid {card_border} !important;
        border-radius: 14px !important;
        padding: 18px !important;
        transition: all 0.25s ease;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    }}
    
    div[data-testid="stVerticalBlock"] > div[style*="border"]:hover {{
        border-color: {card_hover_border} !important;
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.12);
    }}

    /* Estilo para as mensagens de chat customizadas */
    div[data-testid="stChatMessage"] {{
        background-color: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
    }}

    /* Estilo para dropdowns, inputs e selectboxes */
    div[data-baseweb="select"] *, input {{
        color: {text_color} !important;
    }}

    /* Estilização Premium do st.radio (Menu de Navegação Lateral) */
    div[data-testid="stRadio"] > label {{
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        color: {subtitle_color} !important;
        margin-bottom: 10px !important;
    }}
    
    div[data-testid="stRadio"] div[role="radiogroup"] {{
        background: transparent !important;
        border: none !important;
        gap: 6px !important;
    }}
    
    div[data-testid="stRadio"] div[role="radiogroup"] label {{
        background-color: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin-bottom: 0px !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04) !important;
        width: 100% !important;
    }}

    /* Efeito Hover na Navegação */
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {{
        border-color: {card_hover_border} !important;
        background-color: rgba(88, 166, 255, 0.06) !important;
        transform: translateX(3px) !important;
    }}

    /* Estilo Ativo (Marcado) via selector de input checked */
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {{
        border-color: {card_hover_border} !important;
        background-color: {active_menu_bg} !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1) !important;
    }}

    /* Esconder completamente a bolinha (círculo) padrão do radio button */
    div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child {{
        display: none !important;
    }}
    div[data-testid="stRadio"] div[role="radiogroup"] label [data-testid="stControlIndicator"] {{
        display: none !important;
    }}
    div[data-testid="stRadio"] div[role="radiogroup"] label input[type="radio"] {{
        display: none !important;
    }}
    
    /* Formatar o texto interno para ficar compacto e sem margem de parágrafo */
    div[data-testid="stRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {{
        padding-left: 0px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }}
    div[data-testid="stRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {{
        margin: 0 !important;
        line-height: 1.2 !important;
        padding: 0 !important;
    }}

    /* Badges de Especificações Técnicas */
    .badge {{
        display: inline-block;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 3px 10px;
        border-radius: 20px;
        margin-right: 6px;
        margin-bottom: 10px;
    }}
    .badge-blue {{ background: rgba(37, 99, 235, 0.15); color: #2563EB; border: 1px solid rgba(37, 99, 235, 0.35); }}
    .badge-gold {{ background: rgba(217, 119, 6, 0.15); color: #D97706; border: 1px solid rgba(217, 119, 6, 0.35); }}
    .badge-red {{ background: rgba(225, 29, 72, 0.15); color: #E11D48; border: 1px solid rgba(225, 29, 72, 0.35); }}
    .badge-teal {{ background: rgba(13, 148, 136, 0.15); color: #0D9488; border: 1px solid rgba(13, 148, 136, 0.35); }}

    /* Imagens arredondadas */
    img {{
        border-radius: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# PÁGINA 1: CATÁLOGO DE MODELOS
# -------------------------------------------------------------
if page == "Catálogo de Modelos":
    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-title">CYBERCORE ROBOTICS</div>
        <div class="hero-subtitle">Engenharia Robótica Humanoide & Inteligência Positrônica Corporativa</div>
        <p style='color: {desc_color}; font-size: 0.95rem; line-height: 1.5; margin: 0;'>
            Projetamos androides autônomos de alta precisão para ambientes industriais complexos e assistência especializada. 
            Todas as nossas unidades operam estritamente sob as <b>Três Leis da Robótica</b> com hardware certificado.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Linha Residencial
    st.markdown("### 🏠 Linha Residencial & Cuidados")
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.image("./assets/cyber_y.jpeg", caption="Unidade Homologada Série Cyber-Y", use_column_width=True)
            st.markdown("#### **Série Cyber-Y (Assistência e Cuidado)**")
            st.markdown("""
            <span class="badge badge-blue">Residencial</span>
            <span class="badge badge-teal">Bateria Li-S 18h</span>
            <span class="badge badge-blue">Anti-Queda 360°</span>
            """, unsafe_allow_html=True)
            st.markdown("""
            * **Propósito:** Apoio diário a idosos, monitorização contínua de sinais vitais e auxílio de mobilidade.
            * **Revestimento:** Bio-silicone macio com sensores táteis hápticos de alta sensibilidade.
            * **Norma:** Atendimento assistido com comunicação de emergência direta.
            """)
            st.caption("📄 *Documento Oficial:* `catalogo_modelos_domestica_industrial.pdf`")

    with col2:
        with st.container(border=True):
            st.image("./assets/cyber_z.jpeg", caption="Unidade Homologada Série Cyber-Z", use_column_width=True)
            st.markdown("#### **Série Cyber-Z (Doméstico Executivo Pro)**")
            st.markdown("""
            <span class="badge badge-blue">Executivo</span>
            <span class="badge badge-teal">Autonomia 24h</span>
            <span class="badge badge-blue">IoT & SLAM 3D</span>
            """, unsafe_allow_html=True)
            st.markdown("""
            * **Propósito:** Governança residencial completa, culinária avançada, integração predial e suporte bilíngue.
            * **Segurança:** Reconhecimento facial local criptografado em chip Edge Neural (AES-256).
            * **Recarga:** Células solares fotovoltaicas dorsais para recarga passiva.
            """)
            st.caption("📄 *Documento Oficial:* `catalogo_modelos_domestica_industrial.pdf`")

    st.markdown("<br>", unsafe_allow_html=True)

    # Linha Industrial & Segurança
    st.markdown("### 🏭 Linha Industrial & Operações Táticas")
    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            st.image("./assets/cyber_x.jpeg", caption="Unidade Industrial Série Cyber-X", use_column_width=True)
            st.markdown("#### **Série Cyber-X (Industrial Pesado)**")
            st.markdown("""
            <span class="badge badge-gold">Carga 450kg</span>
            <span class="badge badge-gold">Blindagem IP68</span>
            <span class="badge badge-gold">Carga Rápida 480V</span>
            """, unsafe_allow_html=True)
            st.markdown("""
            * **Propósito:** Logística de alta tonelagem, soldagem robotizada e operação em atmosferas perigosas.
            * **Mecânica:** Atuadores hidráulicos de titânio com fluído sintético de alta pressão.
            * **Ciclo:** Suporte a recarga ultrarrápida de até 45 minutos contínuos.
            """)
            st.caption("📄 *Documento Oficial:* `guia_manutencao_preventiva_cyber_x.pdf`")

    with col4:
        with st.container(border=True):
            st.image("./assets/cyber_a.jpeg", caption="Unidade Tática Série Cyber-A", use_column_width=True)
            st.markdown("#### **Série Cyber-A (Patrulha & Segurança)**")
            st.markdown("""
            <span class="badge badge-red">Tático / Policial</span>
            <span class="badge badge-red">LiDAR 360°</span>
            <span class="badge badge-red">SLA 2h On-Site</span>
            """, unsafe_allow_html=True)
            st.markdown("""
            * **Propósito:** Patrulha patrimonial armada/desarmada, controle de acesso e monitoramento tático.
            * **Compliance:** Bloqueio rígido de nível 0 da Primeira Lei da Robótica (Inviolabilidade Humana).
            * **Telemetria:** Caixa-preta criptografada inviolável com auditoria contínua de decisões.
            """)
            st.caption("📄 *Documento Oficial:* `tabela_garantia_cobertura_danos.pdf`")

    st.markdown("---")
    st.info("💡 **Precisa consultar procedimentos de garantia, calibração ou diretrizes legais?** Acesse o **Assistente Virtual** no menu lateral.")

# -------------------------------------------------------------
# PÁGINA 2: CHATBOT CORPORATIVO RAG
# -------------------------------------------------------------
elif page == "Assistente Virtual":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title" style="font-size: 1.7rem;">ASSISTENTE DE CONHECIMENTO</div>
        <div class="hero-subtitle">Mecanismo RAG com Base de Conhecimento Vetorial Indexada (ChromaDB + Gemini)</div>
    </div>
    """, unsafe_allow_html=True)

    # Filtros de Busca
    with st.expander("⚙️ Opções de Busca & Filtros por Categoria", expanded=False):
        category_option = st.selectbox(
            "Filtrar busca nos documentos por categoria temática:",
            ["Todas", "RH & Treinamento", "Suporte / Técnico", "Vendas & Produtos", "Jurídico / Compliance"]
        )
    
    selected_category = None if category_option == "Todas" else category_option

    # Inicializa Histórico
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Olá! Sou o Assistente Corporativo da CyberCore Robotics. Como posso ajudar com dúvidas técnicas, manuais, garantias ou políticas internas?"}
        ]

    # Exibe Histórico
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    # Entrada do Usuário
    if user_input := st.chat_input("Digite sua dúvida (ex: Como funciona a garantia da Série Cyber-X?)..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("🔍 Consultando vetores e formulando resposta fundamentada..."):
                result = generate_agent_response(user_input, category_filter=selected_category)
                answer = result["answer"]
                st.write(answer)
                st.session_state["messages"].append({"role": "assistant", "content": answer})
