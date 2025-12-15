# Flight Search Application

Sistema de busca e análise de voos com integração à API Amadeus, desenvolvido para encontrar as melhores opções de passagens aéreas entre diferentes destinos.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Logs](#logs)
- [Tratamento de Erros](#tratamento-de-erros)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## 🎯 Sobre o Projeto

O Flight Search Application é uma ferramenta que automatiza a busca de voos ida e volta, permitindo encontrar as opções mais econômicas dentro de um período específico. O sistema:

- Busca voos em múltiplas datas dentro de um intervalo
- Identifica automaticamente o menor preço disponível
- Armazena os resultados em banco de dados
- Suporta voos diretos e com conexões
- Valida códigos IATA e intervalos de datas

## ✨ Funcionalidades

- ✈️ **Busca Inteligente**: Pesquisa automática em múltiplas datas com incrementos configuráveis
- 💰 **Melhor Preço**: Identifica e filtra automaticamente os voos com menor custo
- 🔄 **Suporte a Conexões**: Calcula tempos de espera entre voos conectados
- 🗄️ **Persistência**: Armazena itinerários em banco de dados para análise posterior
- ✅ **Validação Robusta**: Valida códigos IATA, datas e parâmetros de busca
- 📊 **Logging Detalhado**: Sistema completo de logs para auditoria e debugging
- 🛡️ **Tratamento de Erros**: Gestão abrangente de exceções e casos extremos

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **airportsdata**: Base de dados de aeroportos IATA
- **requests**: Cliente HTTP para API Amadeus
- **sqlite3/postgresql**: Armazenamento de dados
- **logging**: Sistema de logs integrado

## 📦 Pré-requisitos

- Python 3.8 ou superior
- Conta na [Amadeus for Developers](https://developers.amadeus.com/)
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/luisaferreirass/flight-search-app.git
cd flight-search-app
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

1. **Credenciais da API Amadeus**

Crie um arquivo `.env` na raiz do projeto:

```env
AMADEUS_API_KEY=seu_api_key_aqui
AMADEUS_API_SECRET=seu_api_secret_aqui
```

2. **Configuração do Banco de Dados**

O sistema criará automaticamente as tabelas necessárias na primeira execução. Para usar PostgreSQL em vez de SQLite, configure as variáveis de ambiente:

```env
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5437
DB_NAME=flight_search
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

## 💻 Uso

### Executando o Script Principal

```bash
python main.py
```

### Parâmetros de Busca

Edite os parâmetros no arquivo `main.py`:

```python
search_params = {
    "date_start": "01-02-2026",  # Início do período de busca
    "date_end": "20-06-2026",     # Fim do período de busca
    "origin": "NAT",              # Aeroporto de origem (Natal)
    "destination": "GRU",         # Aeroporto de destino (Guarulhos)
    "days": 7                     # Duração da viagem
}
```

### Códigos IATA Comuns

| Cidade | Código IATA |
|--------|-------------|
| São Paulo (Guarulhos) | GRU |
| Rio de Janeiro (Galeão) | GIG |
| Brasília | BSB |
| Natal | NAT |
| Recife | REC |
| Salvador | SSA |
| Fortaleza | FOR |

## 📁 Estrutura do Projeto

```
flight_search_app/
│
├── app/                   # Diretório principal da aplicação
│   ├── api_client.py      # Cliente da API Amadeus
│   ├── data_models.py     # Modelos de dados (Flight, Itinerary, Connection)
│   ├── db.py              # Handler do banco de dados
│   ├── errors.py          # Exceções customizadas
│   ├── helpers.py         # Funções auxiliares
│   ├── main.py            # Script principal de execução
│   ├── models.py          # FlightSearcher e lógica de negócio
│   └── validator.py       # Validadores de entrada (IATA, datas, etc)
│
├── .gitignore             # Arquivos ignorados pelo Git
├── docker-compose.yml     # Configuração Docker
├── README.md              # Documentação do projeto
└── requirements.txt       # Dependências Python do projeto

```

## ⚠️ Limitações

**IMPORTANTE**: Este projeto foi desenvolvido exclusivamente para fins educacionais e de estudo pessoal. **Não deve ser utilizado para aplicações comerciais ou como ferramenta de decisão para compra de passagens.**

### Limitações da API Amadeus

- **Dados Não Atualizados em Tempo Real**: A API do Amadeus não reflete preços em tempo real. Existe um delay significativo entre as atualizações
- **Ausência de Promoções**: Preços promocionais, ofertas relâmpago e descontos especiais disponíveis nos sites das companhias aéreas não aparecem na API
- **Discrepância de Preços**: Os valores retornados podem ser substancialmente diferentes dos encontrados diretamente nos sites oficiais das companhias

### Limitações do Projeto

- **Cobertura Limitada de Companhias**: Este projeto busca voos **apenas da LATAM e GOL**. Outras companhias aéreas que operam no Brasil (Azul, Avianca, etc.) não são incluídas

- **Comparação Incompleta**: Para uma comparação completa de preços, é sempre recomendado consultar diretamente os sites das companhias aéreas e comparadores de voos comerciais



## 📝 Logs

O sistema gera logs detalhados em dois locais:

1. **Console**: Saída em tempo real
2. **Arquivo**: `flight_search.log`

### Níveis de Log

- **INFO**: Operações normais e marcos importantes
- **DEBUG**: Informações detalhadas para debugging
- **WARNING**: Situações inesperadas mas não críticas
- **ERROR**: Erros que impedem operações específicas

### Exemplo de Log

```
2026-01-15 10:30:45 - __main__ - INFO - Flight Search Application Started
2026-01-15 10:30:46 - __main__ - INFO - Obtaining access token...
2026-01-15 10:30:47 - models - INFO - Search concluded. 45 results collected.
2026-01-15 10:30:47 - models - INFO - Lowest price: 850
2026-01-15 10:30:48 - __main__ - INFO - Successfully saved 12/12 itineraries to database.
```

## ⚠️ Tratamento de Erros

O sistema trata os seguintes tipos de erros:

### Erros de Validação

- **InvalidIATACodeError**: Código de aeroporto inválido
- **InvalidDateRangeError**: Intervalo de datas incorreto
- **ValueError**: Número de dias inválido

### Erros de API

- **ConnectionError**: Falha na conexão com a API
- **Timeout**: Tempo limite excedido

### Erros de Banco de Dados

- Falhas de inserção são logadas mas não interrompem o processo
- Conexão é sempre fechada no bloco `finally`



## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

