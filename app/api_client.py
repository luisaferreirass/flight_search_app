import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

api_key = os.getenv("API_KEY")
secret = os.getenv("SECRET")


def get_access_token() -> str:
    if not api_key or not secret:
        raise ValueError("API_KEY e SECRET devem estar configurados no .env")
    
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials",
              "client_id": api_key,
              "client_secret": secret}
    

    
    response = requests.post(url, headers=headers, data=data, timeout=10)
    response.raise_for_status()

    logging.info("Requesting access token from Amadeus API")
    token = response.json()["access_token"]
    return token



def search_flights(day: int, month: int, year: int, origin: str, destination: str, token: str, day_r: int, month_r: int, year_r: int) -> dict:
    url = "https://test.api.amadeus.com//v2/shopping/flight-offers"

    date = f"{year:04d}-{month:02d}-{day:02d}"
    date_r = f"{year_r:04d}-{month_r:02d}-{day_r:02d}"

    payload = {"originDestinations": [
        {   "id": "1",
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDateTimeRange": {
                "date": date,
                "dateWindow": "P3D"
            }, "carrierRestrictions": {
                "includedCarrierCodes": ["LA", "G3"]
            }
        },  { "id": "2",
            "originLocationCode": destination,
            "destinationLocationCode": origin, 
            "departureDateTimeRange": { 
                "date": date_r,
                "dateWindow": "P3D" 
                }}
    ],
    "travelers": [
        {
            "id": "1",
            "travelerType": "ADULT"
        }
    ],
    "currencyCode": "BRL",
    "sources": ["GDS"]}

    headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "X-HTTP-Method-Override": "GET"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    logging.info("Flight search successful - Status code: %d", response.status_code)
    return response
