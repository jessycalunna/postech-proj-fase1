import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

##############################################################
########## Configurações iniciais
##############################################################

URL_BASE = "https://books.toscrape.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}



def obter_numero_paginas():
    """Descobre quantas páginas existem no catálogo"""
    resposta = requests.get(URL_BASE, headers=HEADERS)
    soup = BeautifulSoup(resposta.content, 'html.parser')
    
    # Verifica se existe paginação
    paginacao = soup.find('li', class_='current')
    if paginacao:
        # Extrai o número total de páginas do texto "Page 1 of 50"
        texto = paginacao.text.strip()
        total_paginas = int(texto.split()[-1])
        return total_paginas
    return 1

def extrair_id_livro(url_livro):
    """Extrai o ID do livro a partir da URL"""
    try:
        # O ID está na URL no formato: catalogue/nome-do-livro_ID/index.html
        # Exemplo: catalogue/a-light-in-the-attic_1000/index.html
        partes = url_livro.split('_')
        if len(partes) >= 2:
            id_livro = partes[-1].replace('/index.html', '').replace('/', '')
            return id_livro
        return None
    except:
        return None

def extrair_dados_livro(artigo):
    """Extrai as informações de um livro específico"""
    try:
        # URL do livro para extrair o ID
        link_livro = artigo.find('h3').find('a')['href']
        id_livro = extrair_id_livro(link_livro)
        
        # Título do livro
        titulo = artigo.find('h3').find('a')['title']
        
        # Preço (remove o símbolo £)
        preco = artigo.find('p', class_='price_color').text.strip()[1:]
        
        # Rating (mantém o texto original: One, Two, Three, Four, Five)
        rating_tag = artigo.find('p', class_='star-rating')
        rating = rating_tag['class'][1] if rating_tag and len(rating_tag['class']) > 1 else 'N/A'
        
        # Disponibilidade
        disponibilidade = artigo.find('p', class_='instock availability').text.strip()
        
        # URL da imagem
        imagem = artigo.find('img')['src']
        # Corrige o caminho relativo da imagem
        if imagem.startswith('../'):
            imagem = URL_BASE + imagem.replace('../', '')
        
        return {
            'id': id_livro,
            'titulo': titulo,
            'preco': float(preco),
            'rating': rating,
            'disponibilidade': disponibilidade,
            'imagem': imagem
        }
    except Exception as e:
        print(f"Erro ao extrair dados: {e}")
        return None

def obter_categoria_livro(url_livro):
    """Acessa a página individual do livro para obter a categoria"""
    try:
        resposta = requests.get(url_livro, headers=HEADERS)
        soup = BeautifulSoup(resposta.content, 'html.parser')
        
        # A categoria está no breadcrumb
        breadcrumb = soup.find('ul', class_='breadcrumb')
        if breadcrumb:
            categorias = breadcrumb.find_all('a')
            if len(categorias) >= 3:
                return categorias[2].text.strip()
        return "Sem categoria"
    except:
        return "Erro ao obter"

def processar_pagina(numero_pagina):
    """Processa uma página específica do catálogo"""
    if numero_pagina == 1:
        url = URL_BASE
    else:
        url = f"{URL_BASE}catalogue/page-{numero_pagina}.html"
    
    print(f"Processando página {numero_pagina}...")
    
    try:
        resposta = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resposta.content, 'html.parser')
        
        # Encontra todos os artigos (livros) na página
        artigos = soup.find_all('article', class_='product_pod')
        
        livros_pagina = []
        for artigo in artigos:
            dados_livro = extrair_dados_livro(artigo)
            if dados_livro:
                # Obtém a URL do livro para buscar a categoria
                link_livro = artigo.find('h3').find('a')['href']
                url_completa = URL_BASE + 'catalogue/' + link_livro.replace('../', '')
                
                # Busca a categoria (isso pode ser otimizado se não for necessário)
                dados_livro['categoria'] = obter_categoria_livro(url_completa)
                livros_pagina.append(dados_livro)
        
        return livros_pagina
    except Exception as e:
        print(f"Erro na página {numero_pagina}: {e}")
        return []

def main():
    """Função principal que coordena o scraping"""
    print("Iniciando scraping de books.toscrape.com...")
    inicio = time.time()
    
    # Descobre quantas páginas existem
    total_paginas = obter_numero_paginas()
    print(f"Total de páginas encontradas: {total_paginas}")
    
    todos_livros = []
    
    # Usa ThreadPoolExecutor para processar múltiplas páginas simultaneamente
    # Isso acelera significativamente o processo
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Processa todas as páginas em paralelo
        resultados = executor.map(processar_pagina, range(1, total_paginas + 1))
        
        # Combina os resultados de todas as páginas
        for livros_pagina in resultados:
            todos_livros.extend(livros_pagina)
    
    # Cria DataFrame com pandas
    df = pd.DataFrame(todos_livros)
    
    # Reordena as colunas na ordem solicitada (com ID no início)
    df = df[['id', 'titulo', 'preco', 'rating', 'disponibilidade', 'categoria', 'imagem']]
    
    # Exporta para CSV
    nome_arquivo = 'livros.csv'
    df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
    
    fim = time.time()
    tempo_total = fim - inicio
    
    print(f"\n{'='*60}")
    print(f"Scraping concluído com sucesso!")
    print(f"Total de livros coletados: {len(todos_livros)}")
    print(f"Tempo de execução: {tempo_total:.2f} segundos")
    print(f"Arquivo salvo: {nome_arquivo}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
