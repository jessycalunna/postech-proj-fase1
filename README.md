<!-- TITULO DO PROJETO -->
<br />
  <h3 align="center">Fase 1: Tech Challenge Machine Learning Engineering</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- SOBRE O PROJETO -->
## Objetivo

Este projeto foi desenvolvido com o objetivo de **construir uma infraestrutura de extração, transformação e disponibilização de dados via API pública**, permitindo que **cientistas de dados e sistemas de recomendação** possam consumir dados estruturados de forma simples e eficiente.

O sistema coleta dados do site [Books to Scrape](https://books.toscrape.com/), processa as informações e as disponibiliza por meio de uma API.

As tecnologias utilizadas para a realização do projeto foram:

* [![FastAPI][FastAPI]][FastAPI-url]
* [![pandas][Pandas]][Pandas-url]
* [![BeautifulSoup][BeautifulSoup]][BeautifulSoup-url]
* [![Requests][Requests]][Requests-url]
* [![os][OS]][OS-url]
* [![typing][Typing]][Typing-url]
* [![Vercel][Vercel]][Vercel-url]
* [![Uvicorn][Uvicorn]][Uvicorn-url]

Todos os testes foram realizados em ambiente virtual local com uso do Python 3.11.

<!-- API PUBLICA -->
## API Pública (Deploy Vercel)

Para acessar a API pública, hospedada no Vercel, acesse [https://postech-proj-fase1-ixihc9ir3-jessycas-projects-cf4a9dab.vercel.app](https://postech-proj-fase1-ixihc9ir3-jessycas-projects-cf4a9dab.vercel.app)

### Documentação dos Endpoints da API

Para consultar o SWAGGER da API acesse [https://postech-proj-fase1-ixihc9ir3-jessycas-projects-cf4a9dab.vercel.app/docs](https://postech-proj-fase1-ixihc9ir3-jessycas-projects-cf4a9dab.vercel.app/docs)

| Método | Endpoint | Descrição |
|--------|-----------|------------|
| `GET` | `/api/v1/health` | Verifica o status da API e a conectividade com os dados |
| `GET` | `/api/v1/books` | Lista ID e título dos livros disponíveis |
| `GET` | `/api/v1/books/search` | Busca livros por título e/ou categoria |
| `GET` | `/api/v1/books/{id}` | Obtém informações completas de um livro específico |
| `GET` | `/api/v1/categories` | Lista todas as categorias disponíveis |

<!-- REPRODUZIR O PROJETO -->
## Como reproduzir o projeto localmente

1. Clone o Repositório
   ```sh
   git clone https://github.com/jessycalunna/postech-proj-fase1.git
   cd postech-proj-fase1
   ```
2. Crie um Ambiente Virtual
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```
3. Instale as Dependências
   ```sh
   pip install -r requirements.txt
   ```
4. Execute o Script de Extração
     ```sh
   python scripts/scrape_livros_csv.py
   ```
5. Inicie a API Localmente
     ```sh
   uvicorn api.index:app --reload
   ```
   > Acesse em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- CONTATO -->
## Contato

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
[FastAPI]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[Pandas]: https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
[BeautifulSoup]: https://img.shields.io/badge/BeautifulSoup-4B8BBE?style=for-the-badge&logo=python&logoColor=white
[BeautifulSoup-url]: https://beautiful-soup-4.readthedocs.io/
[Requests]: https://img.shields.io/badge/Requests-007ec6?style=for-the-badge&logo=python&logoColor=white
[Requests-url]: https://requests.readthedocs.io/
[OS]: https://img.shields.io/badge/os-FFD43B?style=for-the-badge&logo=python&logoColor=306998
[OS-url]: https://docs.python.org/3/library/os.html
[Typing]: https://img.shields.io/badge/typing-3776AB?style=for-the-badge&logo=python&logoColor=white
[Typing-url]: https://docs.python.org/3/library/typing.html
[Vercel]: https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white
[Vercel-url]: https://vercel.com/
[Uvicorn]: https://img.shields.io/badge/Uvicorn-0C3C26?style=for-the-badge&logo=fastapi&logoColor=white
[Uvicorn-url]: https://www.uvicorn.org/
