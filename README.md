# Flight Search Application

Flight search and analysis system integrated with the Amadeus API, built to find the best airfare options between different destinations.

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Technologies Used](#️-technologies-used)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Limitations](#️-limitations)
- [Logs](#-logs)
- [Error Handling](#️-error-handling)
- [License](#-license)

## 🎯 About the Project

Flight Search Application is a tool that automates round-trip flight searches, making it possible to find the cheapest options within a given period. The system:

- Searches flights on multiple dates within a range
- Automatically identifies the lowest available price
- Stores the results in a database
- Supports direct flights and flights with connections
- Validates IATA codes and date ranges

## ✨ Features

- ✈️ **Smart Search**: Automatic search across multiple dates with configurable increments
- 💰 **Best Price**: Automatically identifies and filters the lowest-cost flights
- 🔄 **Connection Support**: Computes layover times between connecting flights
- 🗄️ **Persistence**: Stores itineraries in a database for later analysis
- ✅ **Robust Validation**: Validates IATA codes, dates and search parameters
- 📊 **Detailed Logging**: Complete logging system for auditing and debugging
- 🛡️ **Error Handling**: Comprehensive handling of exceptions and edge cases

## 🛠️ Technologies Used

- **Python 3.8+**
- **airportsdata**: IATA airport database
- **requests**: HTTP client for the Amadeus API
- **sqlite3/postgresql**: Data storage
- **logging**: Built-in logging system

## 📦 Prerequisites

- Python 3.8 or later
- An [Amadeus for Developers](https://developers.amadeus.com/) account
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/luisaferreirass/flight-search-app.git
cd flight-search-app
```

2. **Create a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install the dependencies**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

1. **Amadeus API credentials**

Create a `.env` file in the project root:

```env
AMADEUS_API_KEY=your_api_key_here
AMADEUS_API_SECRET=your_api_secret_here
```

2. **Database configuration**

The system automatically creates the required tables on the first run. To use PostgreSQL instead of SQLite, set the environment variables:

```env
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5437
DB_NAME=flight_search
DB_USER=your_user
DB_PASSWORD=your_password
```

## 💻 Usage

### Running the Main Script

```bash
python main.py
```

### Search Parameters

Edit the parameters in the `main.py` file:

```python
search_params = {
    "date_start": "01-02-2026",  # Start of the search period
    "date_end": "20-06-2026",     # End of the search period
    "origin": "NAT",              # Origin airport (Natal)
    "destination": "GRU",         # Destination airport (Guarulhos)
    "days": 7                     # Trip length
}
```

### Common IATA Codes

| City | IATA Code |
|--------|-------------|
| São Paulo (Guarulhos) | GRU |
| Rio de Janeiro (Galeão) | GIG |
| Brasília | BSB |
| Natal | NAT |
| Recife | REC |
| Salvador | SSA |
| Fortaleza | FOR |

## 📁 Project Structure

```
flight_search_app/
│
├── app/                   # Main application directory
│   ├── api_client.py      # Amadeus API client
│   ├── data_models.py     # Data models (Flight, Itinerary, Connection)
│   ├── db.py              # Database handler
│   ├── errors.py          # Custom exceptions
│   ├── helpers.py         # Helper functions
│   ├── main.py            # Main execution script
│   ├── models.py          # FlightSearcher and business logic
│   └── validator.py       # Input validators (IATA, dates, etc.)
│
├── .gitignore             # Files ignored by Git
├── docker-compose.yml     # Docker configuration
├── README.md              # Project documentation
└── requirements.txt       # Project Python dependencies

```

## ⚠️ Limitations

**IMPORTANT**: This project was developed exclusively for educational purposes and personal study. **It should not be used for commercial applications or as a decision-making tool for buying tickets.**

### Amadeus API Limitations

- **Data Not Updated in Real Time**: The Amadeus API does not reflect real-time prices. There is a significant delay between updates
- **No Promotions**: Promotional fares, flash sales and special discounts available on airline websites do not appear in the API
- **Price Discrepancies**: The returned values may differ substantially from those found directly on the airlines' official websites

### Project Limitations

- **Limited Airline Coverage**: This project searches flights **only from LATAM and GOL**. Other airlines operating in Brazil (Azul, Avianca, etc.) are not included

- **Incomplete Comparison**: For a complete price comparison, it is always recommended to check the airlines' websites and commercial flight comparison sites directly



## 📝 Logs

The system generates detailed logs in two places:

1. **Console**: Real-time output
2. **File**: `flight_search.log`

### Log Levels

- **INFO**: Normal operations and important milestones
- **DEBUG**: Detailed information for debugging
- **WARNING**: Unexpected but non-critical situations
- **ERROR**: Errors that prevent specific operations

### Sample Log

```
2026-01-15 10:30:45 - __main__ - INFO - Flight Search Application Started
2026-01-15 10:30:46 - __main__ - INFO - Obtaining access token...
2026-01-15 10:30:47 - models - INFO - Search concluded. 45 results collected.
2026-01-15 10:30:47 - models - INFO - Lowest price: 850
2026-01-15 10:30:48 - __main__ - INFO - Successfully saved 12/12 itineraries to database.
```

## ⚠️ Error Handling

The system handles the following types of errors:

### Validation Errors

- **InvalidIATACodeError**: Invalid airport code
- **InvalidDateRangeError**: Invalid date range
- **ValueError**: Invalid number of days

### API Errors

- **ConnectionError**: Failed to connect to the API
- **Timeout**: Request timed out

### Database Errors

- Insert failures are logged but do not interrupt the process
- The connection is always closed in the `finally` block



## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
