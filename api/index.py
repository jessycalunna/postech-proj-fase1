from fastapi import FastAPI
from mangum import Mangum
import os
import pandas as pd
from typing import Optional
import os

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

@app.get("/")
def read_root():
    path_csv = os.path.join(os.getcwd(), "data/livros.csv")
    # seu código aqui
    return {"message": "API funcionando"}

##############################################################
####### MÉTODO 1: Verificar Status da API e Dados 
##############################################################

@app.get("/api/v1/health")
def verificar_saude():
    """
    Verifica o status da API e conectividade com os dados
    """
    dados_ok = not df_livros.empty
    arquivo_existe = os.path.exists(CAMINHO_CSV)
    
    if dados_ok and arquivo_existe:
        status = "healthy"
    else:
        status = "unhealthy"
    
    return {
        "status": status,
        "api": "online",
        "base_dados": {
            "arquivo_csv": CAMINHO_CSV,
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

# handler = Mangum(app)
