import os
import re
from pypdf import PdfReader

# Mapeamento estrito de Metadados por Documento
DOC_METADATA = {
    "manual_conduta_convivencia.pdf": {"category": "RH & Treinamento", "ownership": "Recursos Humanos"},
    "politica_recarga_manutencao_baterias.pdf": {"category": "RH & Treinamento", "ownership": "Gestão de Operações"},
    "guia_manutencao_preventiva_cyber_x.pdf": {"category": "Suporte / Técnico", "ownership": "Engenharia Robótica"},
    "manual_atualizacao_firmware_nucleo.pdf": {"category": "Suporte / Técnico", "ownership": "Desenvolvimento de Core"},
    "catalogo_modelos_domestica_industrial.pdf": {"category": "Vendas & Produtos", "ownership": "Comercial"},
    "tabela_garantia_cobertura_danos.pdf": {"category": "Vendas & Produtos", "ownership": "Atendimento & Garantia"},
    "diretrizes_leis_robotica_aplicadas.pdf": {"category": "Jurídico / Compliance", "ownership": "Comitê de Ética"},
    "termos_privacidade_protecao_dados.pdf": {"category": "Jurídico / Compliance", "ownership": "DPO / Privacidade"}
}

def clean_text(text: str) -> str:
    """Aplica regras de limpeza para eliminar ruídos de leitura do PDF."""
    text = re.sub(r'Página \d+ de \d+', '', text)
    text = re.sub(r'CONFIDENCIAL — .*?\n', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def create_chunks(text: str, chunk_size: int = 800, overlap: int = 120) -> list:
    """Realiza o chunking do texto garantindo sobreposição entre janelas."""
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)

    return chunks

def extract_and_chunk_all(directory="base_conhecimento_androids"):
    """Lê todos os PDFs do diretório, extrai, limpa e retorna chunks com metadados."""
    all_chunks = []
    
    if not os.path.exists(directory):
        print(f"Erro: Diretório '{directory}' não encontrado. Crie a pasta e coloque os PDFs dentro.")
        return []

    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

    for filename in pdf_files:
        filepath = os.path.join(directory, filename)
        meta_info = DOC_METADATA.get(filename, {"category": "Geral", "ownership": "Geral"})
        
        reader = PdfReader(filepath)
        full_raw_text = ""
        
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                full_raw_text += f" {extracted}"

        cleaned = clean_text(full_raw_text)
        chunks = create_chunks(cleaned, chunk_size=800, overlap=120)

        for idx, chunk_str in enumerate(chunks):
            all_chunks.append({
                "id": f"{filename}_chunk_{idx+1}",
                "text": chunk_str,
                "metadata": {
                    "source": filename,
                    "category": meta_info["category"],
                    "ownership": meta_info["ownership"],
                    "chunk_index": idx + 1,
                    "total_chunks": len(chunks)
                }
            })

    return all_chunks

if __name__ == "__main__":
    results = extract_and_chunk_all()
    if results:
        print(f"✅ Processamento concluído! Total de {len(results)} chunks preparados.")