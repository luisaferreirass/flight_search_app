import psycopg2
import os
from dotenv import load_dotenv
from data_models import Flight, Connection, ConnectionFlight, Itinerarie
from typing import List

load_dotenv()

class DBHandler:
    def __init__(self):
        self.connection = self.get_connection()
        self.cursor = self.connection.cursor()

    def get_connection(self):
        return psycopg2.connect(
            dbname=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USERNAME"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
        )

    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS locations (
            id SERIAL PRIMARY KEY,
            city TEXT NOT NULL,
            airport TEXT NOT NULL)
            """
        )
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS itineraries (
                id SERIAL PRIMARY KEY,
                search_execution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                price NUMERIC(10,2) NOT NULL,

                origin_id INT REFERENCES locations(id),
                destination_id INT REFERENCES locations(id)
            )
            """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                id SERIAL PRIMARY KEY,

                itinerary_id INT REFERENCES itineraries(id) ON DELETE CASCADE,
                flight_type VARCHAR(10) CHECK (flight_type IN ('outbound', 'return')),

                origin_id INT REFERENCES locations(id),
                destination_id INT REFERENCES locations(id),

                date DATE NOT NULL,
                duration INTERVAL NOT NULL
            )
            """
            )

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS flight_conexions (
                id SERIAL PRIMARY KEY,

                flight_id INT REFERENCES flights(id) ON DELETE CASCADE,

                origin_id INT REFERENCES locations(id),
                destination_id INT REFERENCES locations(id),

                departure TIMESTAMP NOT NULL,
                arrival TIMESTAMP NOT NULL,

                flight_number TEXT NOT NULL,
                segment_order INT NOT NULL
            )
            """)

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS conexions(
            id SERIAL PRIMARY KEY,

            flight_id INT REFERENCES flights(id) ON DELETE CASCADE,

            waiting_time INTERVAL NOT NULL,
            change_airport BOOLEAN DEFAULT FALSE,
            connection_order INT NOT NULL)
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS location_conexion (
            id SERIAL PRIMARY KEY,

            conexion_id INT REFERENCES conexions(id) ON DELETE CASCADE,
            location_id INT REFERENCES locations(id),

            role VARCHAR(10) CHECK (role IN ('arrival', 'departure')))
            """
        )

        self.connection.commit()

    def get_location(self, location: dict) -> int:
        self.cursor.execute(
            """
            SELECT id 
            FROM locations
            WHERE city = %s AND airport = %s
            """, (location["city"], location["airport"])
        )

        resultado = self.cursor.fetchone()
        if resultado:
            return resultado[0]
        return None
    
    def insert_location(self, location: dict) -> int:
        location_id = self.get_location(location)
        if location_id:
            return location_id

        self.cursor.execute(
            """
            INSERT INTO locations (city, airport) 
            VALUES (%s, %s)
            RETURNING id
            """, (location["city"], location["airport"])
        )

        location_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return location_id
    
    def insert_conexion_flight(self, conexion_flight: ConnectionFlight, flight_id: int, segment_order: int):
        origin_id = self.insert_location(conexion_flight.origin)
        destination_id = self.insert_location(conexion_flight.destination)

        self.cursor.execute(
            """
            INSERT INTO flight_conexions (flight_id, origin_id, destination_id, departure, arrival, flight_number, segment_order) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (flight_id, origin_id, destination_id, conexion_flight.departure, conexion_flight.arrival, conexion_flight.flight_number, segment_order)
        )

        self.connection.commit()
        
    def insert_conexion(self, conexion: Connection, flight_id: int, conexion_order: int):
        self.cursor.execute(
            """
            INSERT INTO conexions (flight_id, waiting_time, change_airport, connection_order) 
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """, (flight_id, conexion.waiting_time, conexion.change_airport, conexion_order)
        )

        conexion_id = self.cursor.fetchone()[0]
        self.connection.commit()

        for idx, location in enumerate(conexion.locations):
            location_id = self.insert_location(location)
            
            role = 'arrival' if idx == 0 else 'departure'
                
            self.cursor.execute(
                """
                INSERT INTO location_conexion (conexion_id, location_id, role)
                VALUES (%s, %s, %s)
                """, (conexion_id, location_id, role)
            )
        
        self.connection.commit()
        return conexion_id

    def insert_flight(self, flight: Flight, itinerary_id: int, flight_type: str) -> int:
        origin_id = self.insert_location(flight.origin)
        destination_id = self.insert_location(flight.destination)
        
        self.cursor.execute(
            """
            INSERT INTO flights (itinerary_id, flight_type, origin_id, destination_id, date, duration) 
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """, (itinerary_id, flight_type, origin_id, destination_id, flight.date, flight.duration)
        )

        flight_id = self.cursor.fetchone()[0]
        self.connection.commit()

        for idx, conexion_flight in enumerate(flight.segments):
            self.insert_conexion_flight(conexion_flight, flight_id, idx)

        for idx, conexion in enumerate(flight.connections):
            self.insert_conexion(conexion, flight_id, idx)

        return flight_id

    def insert_itinerarie(self, itinerary: Itinerarie) -> int:
        origin_id = self.insert_location(itinerary.flight_departure.origin)
        destination_id = self.insert_location(itinerary.flight_departure.destination)

        self.cursor.execute(
            """
            INSERT INTO itineraries (price, origin_id, destination_id) 
            VALUES (%s, %s, %s)
            RETURNING id
            """, (itinerary.price, origin_id, destination_id)
        )

        itinerary_id = self.cursor.fetchone()[0]
        self.connection.commit()
        
        # Insere voo de ida
        self.insert_flight(itinerary.flight_departure, itinerary_id, 'outbound')

        if itinerary.flight_return:
            self.insert_flight(itinerary.flight_return, itinerary_id, 'return')

        return itinerary_id

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()