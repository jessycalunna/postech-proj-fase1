from fastapi import FastAPI
import os
import pandas as pd
from typing import Optional

##############################################################
####### Inicialização da API 
##############################################################

app = FastAPI(
    title="PosTech Projeto Fase 1 API",
    description="API para consulta de livros do Books to Scrape",
    version="1.0.0"
)

##############################################################
####### Configuração do Path do CSV
##############################################################

path_csv = os.path.join(os.getcwd(), "data/livros.csv")

# path_csv = "livros.csv"

##############################################################
####### Carregar Base de Dados em DF Pandas 
##############################################################

def carregar_base_dados():
    """Carrega o arquivo CSV em um DataFrame pandas"""
    try:
        if not os.path.exists(path_csv):
            raise FileNotFoundError(f"Arquivo {path_csv} não encontrado")
        
        df = pd.read_csv(path_csv, encoding='utf-8-sig')
        print(f"Base de dados carregada: {len(df)} livros")
        return df
    except Exception as e:
        print(f"Erro ao carregar base de dados: {e}")
        return pd.DataFrame()

# Carrega os dados na inicialização
df_livros = carregar_base_dados()


##############################################################
####### Teste Inicial da API 
##############################################################

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    """
    Exibe o conteúdo do README.md renderizado em HTML como página inicial da API.
    """
    try:
        readme_path = os.path.join(os.getcwd(), "README.md")
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
        html_content = markdown.markdown(readme_content)
        return f"""
        <html>
            <head>
                <meta charset="utf-8">
                <title>📚 Books API</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Roboto, sans-serif;
                        max-width: 900px;
                        margin: 40px auto;
                        line-height: 1.6;
                        color: #333;
                    }}
                    code {{
                        background-color: #f4f4f4;
                        padding: 2px 4px;
                        border-radius: 4px;
                        font-size: 0.95em;
                    }}
                    pre {{
                        background-color: #f4f4f4;
                        padding: 10px;
                        border-radius: 8px;
                        overflow-x: auto;
                    }}
                    h1, h2, h3 {{
                        color: #d9480f;
                    }}
                    a {{
                        color: #0078d4;
                        text-decoration: none;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
        </html>
        """
    except Exception as e:
        return f"<h2>Erro ao carregar README.md:</h2><pre>{str(e)}</pre>"

##############################################################
####### MÉTODO 1: Verificar Status da API e Dados 
##############################################################

@app.get("/api/v1/health")
def verificar_saude():
    """
    Verifica o status da API e conectividade com os dados
    """
    dados_ok = not df_livros.empty
    arquivo_existe = os.path.exists(path_csv)
    
    if dados_ok and arquivo_existe:
        status = "healthy"
    else:
        status = "unhealthy"
    
    return {
        "status": status,
        "api": "online",
        "base_dados": {
            "arquivo_csv": path_csv,
            "arquivo_existe": arquivo_existe,
            "dados_carregados": dados_ok,
            "total_livros": len(df_livros) if dados_ok else 0,
            "colunas": list(df_livros.columns) if dados_ok else []
        }
    }

##############################################################
####### MÉTODO 2: Listar ID e Título dos Livros
##############################################################

@app.get("/api/v1/books")
def listar_livros():
    """
    Lista todos os livros mostrando apenas ID e título
    """
    if df_livros.empty:
        raise HTTPException(status_code=500, detail="Base de dados vazia")
    
    livros = df_livros[['id', 'titulo']].to_dict(orient='records')
    
    return {
        "total": len(livros),
        "livros": livros
    }

##############################################################
####### MÉTODO 3: Buscar Livros por Título e/ou Categoria
##############################################################

@app.get("/api/v1/books/search")
def buscar_livros(title: Optional[str] = None, category: Optional[str] = None):
    """
    Busca livros por título e/ou categoria
    """
    resultado = df_livros.copy()
    
    if title:
        resultado = resultado[resultado['titulo'].str.contains(title, case=False, na=False)]
    
    if category:
        resultado = resultado[resultado['categoria'].str.contains(category, case=False, na=False)]
    
    livros = resultado[['id', 'titulo', 'categoria', 'preco', 'rating']].to_dict(orient='records')
    
    return {
        "parametros_busca": {
            "title": title,
            "category": category
        },
        "total": len(livros),
        "livros": livros
    }


##############################################################
####### MÉTODO 4: Buscar Livro por ID
##############################################################

@app.get("/api/v1/books/{id}")
def obter_livro_por_id(id_livro: str):
    """
    Obtém informações completas de um livro específico pelo ID
    """
    df_temp = df_livros.copy()
    df_temp['id'] = df_temp['id'].astype(str)
    
    livro = df_temp[df_temp['id'] == str(id_livro)]
    
    if livro.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Livro com ID '{id_livro}' não encontrado"
        )
    
    dados_livro = livro.iloc[0].to_dict()
    return dados_livro

##############################################################
####### MÉTODO 5: Listar Categorias
##############################################################

@app.get("/api/v1/categories")
def listar_categorias():
    """
    Lista todas as categorias disponíveis
    """
    categorias = df_livros['categoria'].unique().tolist()
    
    return {
        "total": len(categorias),
        "categorias": sorted(categorias)
    }
