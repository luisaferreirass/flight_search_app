import logging
import sys
from typing import Optional
from models import FlightSearcher
from api_client import get_access_token
from db import DBHandler
from errors import InvalidIATACodeError, InvalidDateRangeError, APITokenExpiredError

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flight_search.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def initialize_components() -> tuple[Optional[FlightSearcher], Optional[DBHandler]]:
    try:
        logger.info("Obtaining access token...")
        token = get_access_token()
        
        logger.info("Initializing flight searcher...")
        flight_searcher = FlightSearcher(token)
        
        logger.info("Initializing database handler...")
        db_handler = DBHandler()
        db_handler.create_tables()
        
        return flight_searcher, db_handler
    
    except Exception as e:
        logger.error("Unexpected error during initialization: %s", str(e))
        return None, None


def search_and_save_flights(
    flight_searcher: FlightSearcher,
    db_handler: DBHandler,
    date_start: str,
    date_end: str,
    origin: str,
    destination: str,
    days: int
) -> bool:
    """
    Busca voos e salva no banco de dados.
    
    Returns:
        bool: True se a operação foi bem-sucedida, False caso contrário.
    """
    try:
        logger.info(
            "Starting flight search: %s -> %s (%s to %s, %d days)",
            origin, destination, date_start, date_end, days
        )
        
        result_flights = flight_searcher.search(
            date_start=date_start,
            date_end=date_end,
            city_from=origin,
            city_to=destination,
            qtd_days=days
        )
        
        if not result_flights:
            logger.warning("No flights found matching the criteria.")
            return False
        
        logger.info("Found %d itineraries. Saving to database...", len(result_flights))
        
        saved_count = 0
        for itinerary in result_flights:
            try:
                db_handler.insert_itinerarie(itinerary)
                saved_count += 1
            except Exception as e:
                logger.error("Failed to save itinerary: %s", str(e))
                continue
        
        logger.info("Successfully saved %d/%d itineraries to database.", saved_count, len(result_flights))
        return True
    
    except InvalidIATACodeError as e:
        logger.error("Invalid IATA code: %s", str(e))
        return False
    
    except InvalidDateRangeError as e:
        logger.error("Invalid date range: %s", str(e))
        return False
    
    except ValueError as e:
        logger.error("Validation error: %s", str(e))
        return False
    
    except Exception as e:
        logger.error("Unexpected error during flight search: %s", str(e), exc_info=True)
        return False


def main():
    """Função principal do programa."""
    logger.info("=" * 60)
    logger.info("Flight Search Application Started")
    logger.info("=" * 60)
    
    flight_searcher, db_handler = initialize_components()

    if not flight_searcher or not db_handler:
        logger.error("Failed to initialize components. Exiting...")
        sys.exit(1)

    try:
        search_params = {
            "date_start": "01-02-2026",
            "date_end": "20-06-2026",
            "origin": "NAT",
            "destination": "GRU",
            "days": 7
        }

        success = search_and_save_flights(
            flight_searcher=flight_searcher,
            db_handler=db_handler,
            **search_params
        )

        if success:
            logger.info("Flight search completed successfully!")
            sys.exit(0)
        else:
            logger.warning("Flight search completed with warnings or errors.")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user.")
        sys.exit(130)

    finally:
        if db_handler:
            logger.info("Closing database connection...")
            db_handler.close()

        logger.info("=" * 60)
        logger.info("Flight Search Application Finished")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()