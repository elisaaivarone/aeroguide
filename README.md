# ✈️ AeroGuide Ops API

API desenvolvida como projeto prático para automação e logística de aviação, unindo banco de dados interno, consumo de APIs externas de radar global e Inteligência Artificial.

## 🎯 Objetivo do Projeto

Atuar como um sistema de **Briefing Operacional Inteligente**. A API recebe o número de um voo e:

1. Verifica a malha aérea interna da companhia (Banco de Dados Local).
2. Caso não seja um voo interno, consulta o radar global em tempo real (Integração de API Externa).
3. Utiliza IA (Prompt Engineering) para atuar como um despachante, gerando um briefing técnico e direto para a equipe de solo baseado no status real da aeronave.

## 🛠️ Tecnologias Utilizadas

- **Python** (Lógica de programação e integração de sistemas)
- **FastAPI** (Criação de rotas, Web Basics e documentação Swagger automática)
- **SQLite** (Banco de dados relacional para simulação da malha aérea interna)
- **Google Gemini 2.5 Flash** (IA Generativa para automação do briefing)
- **AviationStack API** (Radar global de voos via requisições HTTP)

## 🚀 Como rodar o projeto localmente

1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv` e ative-o.
3. Instale as dependências:

```bash
  pip install fastapi uvicorn google-genai requests python-dotenv
```

4.Crie um arquivo .env na raiz do projeto com as suas chaves de API:

```bash
GEMINI_API_KEY=sua_chave_do_google
AVIATION_API_KEY=sua_chave_do_aviationstack
```

5.Inicie o servidor:

```bash
uvicorn main:app --reload
```

6.Acesse a documentação interativa em: http://127.0.0.1:8000/docs

## 👩‍💻 Autor

Desenvolvido por Elisa, estudante de Sistemas para Internet no Senac, com foco no desenvolvimento de aplicações web modernas e integração com Inteligência Artificial.