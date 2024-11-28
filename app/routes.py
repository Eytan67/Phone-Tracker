import logging
from repository import Repository
from init_db import get_driver
from flask import Blueprint, jsonify, request


phone_tracker_rout = Blueprint('phone_tracker', __name__, url_prefix='/api/phone_tracker')


@phone_tracker_rout.route('', methods=['POST'])
def index():
    data = request.get_json()
    required_fields = ['devices', 'interaction']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    print(data)
    try:
        repo = Repository(get_driver())
        repo.add_events(data['devices'][0], data['devices'][1], data['interaction'])

        return jsonify({
            'status': 'success',
        }), 201
    except Exception as e:
        # print(f'Error in POST /api/v1/transaction: {str(e)}')
        logging.error(f'Error in POST /api/phone_tracker: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500

@phone_tracker_rout.route('/bluetooth_connected_devices', methods=['GET'])
def find_bluetooth_connected_devices():
    try:
        repo = Repository(get_driver())
        res = repo.find_bluetooth_connected_devices()
        return jsonify({'res': res}), 200
    except Exception as e:
        logging.error(f'Error in POST /api/phone_tracker/bluetooth_connected_devices: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500

@phone_tracker_rout.route('/strength_connected_devices', methods=['GET'])
def find_strength_connected_devices():
    try:
        repo = Repository(get_driver())
        res = repo.find_strength_connected_devices()
        return jsonify({'res': res}), 200
    except Exception as e:
        logging.error(f'Error in POST /api/phone_tracker/strength_connected_devices: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500


@phone_tracker_rout.route('/count_connected_devices/<device_id>', methods=['GET'])
def find_count_connected_devices(device_id):
    # device_id = request.args.get('device_id')
    if device_id is None:
        return jsonify({'error': 'Missing required parameter'}), 400
    try:
        repo = Repository(get_driver())
        res = repo.find_count_connected_devices(device_id)
        return jsonify({'res': res}), 200
    except Exception as e:
        logging.error(f'Error in POST /api/phone_tracker/count_connected_devices: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500



@phone_tracker_rout.route('/direct_connected_devices', methods=['GET'])
def find_direct_connected_devices():
    device_id1 = request.args.get('device_id1')
    device_id2 = request.args.get('device_id2')

    if device_id1 is None or device_id2 is None:
        return jsonify({'error': 'Missing required parameter'}), 400
    try:
        repo = Repository(get_driver())
        res = repo.find_direct_connected_devices(device_id1, device_id2)
        return jsonify({'res': res}), 200
    except Exception as e:
        logging.error(f'Error in POST /api/phone_tracker/bluetooth_connected_devices: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500

@phone_tracker_rout.route('/recent_connected_devices', methods=['POST'])
def find_recent_connected_devices():
    device_id = request.args.get('device_id')
    if device_id is None:
        return jsonify({'error': 'Missing required parameter'}), 400
    try:
        repo = Repository(get_driver())
        res = repo.find_recent_connected_devices(device_id)
        return jsonify({'res': res}), 200
    except Exception as e:
        logging.error(f'Error in POST /api/phone_tracker/bluetooth_connected_devices: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500




# [
#     {
#         'devices': [
#             {
#                 'id': '80d40b5a-842a-4114-918a-44d4cc5ae156',
#                 'brand': 'Yu LLC',
#                 'model': 'Stock Scientist',
#                 'os': 'MostOS 14.5',
#                 'location': {
#                     'latitude': -55.3992325,
#                     'longitude': -45.687022,
#                     'altitude_meters': 781,
#                     'accuracy_meters': 40
#                 }
#             },
#             {
#                 'id': '80d40b5a-842a-4114-918a-44d4cc5ae156',
#                 'brand': 'Mccarty-Dominguez',
#                 'model': 'Institution Pretty',
#                 'os': 'PersonOS 7.5',
#                 'location': {
#                     'latitude': 88.249525,
#                     'longitude': -121.319607,
#                     'altitude_meters': 717,
#                     'accuracy_meters': 43
#                 }
#             }
#         ],
#         'interaction': {
#             'from_device': '80d40b5a-842a-4114-918a-44d4cc5ae156',
#             'to_device': '80d40b5a-842a-4114-918a-44d4cc5ae156',
#             'method': 'WiFi',
#             'bluetooth_version': '5.3',
#             'signal_strength_dbm': -71,
#             'distance_meters': 2.94,
#             'duration_seconds': 294,
#             'timestamp': '1977-06-23T21:16:17'
#         }
#     },
#     {
#         'devices': [
#         {
#             'id': 'e6e0a8ba-942a-4d34-a98c-cef4ce87f96e',
#             'brand': 'Mcintyre PLC',
#             'model': 'Way President',
#             'os': 'AheadOS 2.2',
#             'location': {
#                 'latitude': -8.1356815,
#                 'longitude': -118.17675,
#                 'altitude_meters': 3562,
#                 'accuracy_meters': 18
#             }
#         },
#         {
#             'id': '469228d5-1ba2-439e-ba5c-b2399af872dc',
#             'brand': 'Harris Ltd',
#             'model': 'Him System',
#             'os': 'AgencyOS 14.0',
#             'location': {
#                 'latitude': 53.5420095,
#                 'longitude': -168.933501,
#                 'altitude_meters': 1084,
#                 'accuracy_meters': 31
#             }
#         }
#         ],
#         'interaction': {
#             'from_device': 'e6e0a8ba-942a-4d34-a98c-cef4ce87f96e',
#             'to_device': '469228d5-1ba2-439e-ba5c-b2399af872dc',
#             'method': 'NFC',
#             'bluetooth_version': '5.2',
#             'signal_strength_dbm': -63,
#             'distance_meters': 4.88,
#             'duration_seconds': 76,
#             'timestamp': '2006-10-19T12:19:40'
#         }
#     },
#     {'devices': [{'id': '2bbe7ec5-c08b-4db8-950f-2f19681e5285', 'brand': 'Collins Ltd', 'model': 'Clear Pm', 'os': 'LineOS 10.4', 'location': {'latitude': 51.44401, 'longitude': -109.503076, 'altitude_meters': 3031, 'accuracy_meters': 44}}, {'id': '9ccee705-858f-4b9b-a5ed-4350213408e0', 'brand': 'Barnett-Alexander', 'model': 'Write Race', 'os': 'CertainlyOS 3.5', 'location': {'latitude': -53.059042, 'longitude': 44.216067, 'altitude_meters': 2640, 'accuracy_meters': 8}}], 'interaction': {'from_device': '2bbe7ec5-c08b-4db8-950f-2f19681e5285', 'to_device': '9ccee705-858f-4b9b-a5ed-4350213408e0', 'method': 'Bluetooth', 'bluetooth_version': '5.3', 'signal_strength_dbm': -88, 'distance_meters': 19.7, 'duration_seconds': 221, 'timestamp': '1986-12-18T17:58:59'}}]
