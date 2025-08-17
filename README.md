# Sistema de Aplicação de Provas

Sistema web completo para aplicação de provas com frontend Vue.js e backend Flask.

## Funcionalidades

- **Login de Instrutor**: Cadastro e autenticação de instrutores por QRA
- **Definir Provas**: Criação de provas com nome e data de aplicação
- **Aplicar Provas**: Registro de pontuações por QRA de aluno (com adição dinâmica de linhas)
- **Resultados**: Visualização de resultados totais por aluno

## Tecnologias

- **Frontend**: Vue.js 3 com Vue Router
- **Backend**: Flask com SQLAlchemy
- **Banco de Dados**: SQLite
- **Deploy**: Vercel

## Estrutura do Projeto

```
sistema-provas-backend/
├── src/
│   ├── models/          # Modelos do banco de dados
│   ├── routes/          # Rotas da API
│   ├── static/          # Frontend Vue.js (build)
│   └── main.py          # Aplicação principal
├── vercel.json          # Configuração da Vercel
├── requirements.txt     # Dependências Python
└── README.md
```

## Deploy na Vercel

1. Faça upload do projeto para um repositório Git
2. Conecte o repositório na Vercel
3. A Vercel detectará automaticamente o projeto Flask
4. O deploy será feito automaticamente

## Desenvolvimento Local

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o servidor:
   ```bash
   python src/main.py
   ```
4. Acesse http://localhost:5000

## API Endpoints

- `GET /api/instrutores` - Lista instrutores
- `POST /api/instrutores` - Cria instrutor
- `GET /api/provas/instrutor/{id}` - Lista provas do instrutor
- `POST /api/provas` - Cria prova
- `GET /api/pontuacoes/prova/{id}` - Lista pontuações da prova
- `POST /api/pontuacoes` - Cria pontuação
- `GET /api/resultados/instrutor/{id}` - Resultados por instrutor

## Uso do Sistema

1. **Cadastro de Instrutor**: Acesse "Login Instrutor" > "Cadastrar" e informe QRA e nome
2. **Login**: Selecione o instrutor cadastrado e clique em "Entrar"
3. **Criar Prova**: Em "Definir Provas", informe nome e data da prova
4. **Aplicar Prova**: Em "Aplicar Provas", selecione a prova e registre as pontuações
5. **Ver Resultados**: Em "Resultados", visualize as pontuações totais por aluno

