import uuid
from datetime import datetime

from flask import jsonify


def loging(result):
    pass


class Repository:
    def __init__(self, driver):
        self.driver = driver

    def add_events(self, from_devise, to_devise, interaction):
        with self.driver.session() as session:
            query = """
            MERGE (from_device:Device {
            id: $from_device_id,
            name: $from_device_name,
            brand: $from_device_brand,
            model: $from_device_model,
            os: $from_device_os,
            latitude: $from_location_latitude,
            longitude: $from_location_longitude,
            altitude_meters: $from_location_altitude_meters,
            accuracy_meters: $from_location_accuracy_meters
            })

            
            MERGE (to_device:Device {
            id: $to_devise_id,
            name: $to_devise_name,
            brand: $to_devise_brand,
            model: $to_devise_model,
            os: $to_devise_os,
            latitude: $to_location_latitude,
            longitude: $to_location_longitude,
            altitude_meters: $to_location_altitude_meters,
            accuracy_meters: $to_location_accuracy_meters
            })

            
            CREATE (from_device)-[:CONNECTED {
            method: $method,
            bluetooth_version: $bluetooth_version,
            signal_strength_dbm: $signal_strength_dbm,
            distance_meters: $distance_meters,
            duration_seconds: $duration_seconds,
            timestamp: $timestamp
            }]->(to_device)
            """
            result = session.run(query, {
                'from_device_id': from_devise['id'],
                'from_device_name': from_devise['name'],
                'from_device_brand': from_devise['brand'],
                'from_device_model': from_devise['model'],
                'from_device_os': from_devise['os'],
                'from_location_latitude': from_devise['location']['latitude'],
                'from_location_longitude': from_devise['location']['longitude'],
                'from_location_altitude_meters': from_devise['location']['altitude_meters'],
                'from_location_accuracy_meters': from_devise['location']['accuracy_meters'],

                'to_devise_id': to_devise['id'],
                'to_devise_name': to_devise['name'],
                'to_devise_brand': to_devise['brand'],
                'to_devise_model': to_devise['model'],
                'to_devise_os': to_devise['os'],
                'to_location_latitude': to_devise['location']['latitude'],
                'to_location_longitude': to_devise['location']['longitude'],
                'to_location_altitude_meters': to_devise['location']['altitude_meters'],
                'to_location_accuracy_meters': to_devise['location']['accuracy_meters'],

                'method': interaction['method'],
                'bluetooth_version': interaction['bluetooth_version'],
                'signal_strength_dbm': interaction['signal_strength_dbm'],
                'distance_meters': interaction['distance_meters'],
                'duration_seconds': interaction['duration_seconds'],
                'timestamp': datetime.fromisoformat(interaction['timestamp'])

            })
            return result.single()

        # query = """
        #             MERGE (from_device:Device {
        #             id: $from_device_id,
        #             name: $from_device_name,
        #             brand: $from_device_brand,
        #             model: $from_device_model,
        #             os: $from_device_os
        #             })
        #             MERGE (from_location:Location {
        #             id: $from_location_id,
        #             latitude: $from_location_latitude,
        #             longitude: $from_location_longitude,
        #             altitude_meters: $from_location_altitude_meters,
        #             accuracy_meters: $from_location_accuracy_meters
        #             })
        #
        #             MERGE (to_devise:Device {
        #             id: $to_devise_id,
        #             name: $to_devise_name,
        #             brand: $to_devise_brand,
        #             model: $to_devise_model,
        #             os: $to_devise_os
        #             })
        #             MERGE (to_location:Location {
        #             id: $to_location_id,
        #             latitude: $to_location_latitude,
        #             longitude: $to_location_longitude,
        #             altitude_meters: $to_location_altitude_meters,
        #             accuracy_meters: $to_location_accuracy_meters
        #             })
        #
        #             CREATE (from_devise)-[:LOCATED_AT]->(from_location)
        #             CREATE (to_devise)-[:LOCATED_AT]->(to_location)
        #
        #             CREATE (from_devise)-[:CONNECTED {
        #             method: $method,
        #             bluetooth_version: $bluetooth_version,
        #             signal_strength_dbm: $signal_strength_dbm,
        #             distance_meters: $distance_meters,
        #             duration_seconds: $duration_seconds,
        #             timestamp: $timestamp
        #             }]->(to_devise)
        #             """
        # result = session.run(query, {
        #     'from_device_id': from_devise['id'],
        #     'from_device_name': from_devise['name'],
        #     'from_device_brand': from_devise['brand'],
        #     'from_device_model': from_devise['model'],
        #     'from_device_os': from_devise['os'],
        #
        #     'from_location_id': str(uuid.uuid4()),
        #     'from_location_latitude': from_devise['location']['latitude'],
        #     'from_location_longitude': from_devise['location']['longitude'],
        #     'from_location_altitude_meters': from_devise['location']['altitude_meters'],
        #     'from_location_accuracy_meters': from_devise['location']['accuracy_meters'],
        #
        #     'to_devise_id': to_devise['id'],
        #     'to_devise_name': to_devise['name'],
        #     'to_devise_brand': to_devise['brand'],
        #     'to_devise_model': to_devise['model'],
        #     'to_devise_os': to_devise['os'],
        #
        #     'to_location_id': str(uuid.uuid4()),
        #     'to_location_latitude': to_devise['location']['latitude'],
        #     'to_location_longitude': to_devise['location']['longitude'],
        #     'to_location_altitude_meters': to_devise['location']['altitude_meters'],
        #     'to_location_accuracy_meters': to_devise['location']['accuracy_meters'],
        #
        #     'method': interaction['method'],
        #     'bluetooth_version': interaction['bluetooth_version'],
        #     'signal_strength_dbm': interaction['signal_strength_dbm'],
        #     'distance_meters': interaction['distance_meters'],
        #     'duration_seconds': interaction['duration_seconds'],
        #     'timestamp': datetime.fromisoformat(interaction['timestamp'])
        #
        # })

    def find_bluetooth_connected_devices(self):
        with self.driver.session() as session:
            query = """
            MATCH (start:Device)
            MATCH (end:Device)
            WHERE start <> end
            MATCH path = shortestPath((start)-[:CONNECTED*]->(end))
            WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
            WITH path, length(path) as pathLength
            ORDER BY pathLength DESC
            LIMIT 1
            RETURN path, length(path)
            """
            result = session.run(query)

            return result.data()

    def find_strength_connected_devices(self):
        with self.driver.session() as session:
            query = """
            match (d1:Device)-[r:CONNECTED]-(Device)
            where r.signal_strength_dbm>=-60
            return distinct(d1)
            """
            result = session.run(query)

            return result.data()

    def find_count_connected_devices(self, device_id):
        with self.driver.session() as session:
            query = """
            match (d:Device{id: $device_id})-[:CONNECTED]->(:Device)
            return count(distinct(d))
            """
            result = session.run(query, {'device_id': device_id})

            return result.single()

    def find_direct_connected_devices(self, device_id1, device_id2):
        with self.driver.session() as session:
            query = """
            match (d1:Device{id: $device_id1})-[r:CONNECTED]-(d2:Device{id: $device_id2})
            return r
            """
            result = session.run(query, {'device_id1': device_id1, 'device_id2': device_id2}).single()

            return result

    def find_recent_connected_devices(self, device_id):
        with self.driver.session() as session:
            query = """
             match (:Device{id: $device_id1})-[r:CONNECTED]-(d:Device)
             order by r.timestamp
             limit 1
             return d
             """
            result = session.run(query, {'device_id': device_id}).single()

            return result