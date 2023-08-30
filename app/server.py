import datetime
import json

from azure.data.tables import TableClient
from flask import Flask, Response, request, send_from_directory, jsonify
from waitress import serve

def flask_app():
    app = Flask(__name__)

    @app.route('/api/water-level/get')
    def get_level():
        record = get_last_waterlevel_record()
        return jsonify(record), 200

    @app.route('/api/water-level/set', methods=["POST"])
    def set_level():
        level = float(request.headers.get("Level"))
        auth = request.headers.get("Auth")
        if auth != "bumbac" or level < 1:
            return Response(status=400)
        insert_new_waterlevel_record(level)
        return Response(status=200)

    @app.route('/')
    def client():
        return send_from_directory('client/public', 'index.html')

    @app.route('/<path:path>')
    def base(path):
        return send_from_directory('client/public', path)

    return app


def get_last_waterlevel_record():
    try:
        table_client = TableClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=jhpsstorage;AccountKey=awHDPAd0xv3lF3NaCBumSBYrgj0DLruk/DODXK4dLRzeSqne0YV+HPCSsqj0dqEXa976SP9tVqIyI69wUjF6gQ==;EndpointSuffix=core.windows.net", "waterlevels")
        f = ""
        query = table_client.query_entities(query_filter=f)
        newest_record = {}
        newest_record_time = 0
        for entity in query:
            date = entity.metadata["timestamp"]
            timestamp = int(round(date.timestamp()))
            if timestamp > newest_record_time:
                newest_record_time = timestamp
                newest_record = entity

        return newest_record
    except Exception as e:
        print(f"Could not finish task run_count_images_task: Reason: {e}")


def insert_new_waterlevel_record(level):
    try:
        rowkey = int(datetime.datetime.now().timestamp())
        table_client = TableClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=jhpsstorage;AccountKey=awHDPAd0xv3lF3NaCBumSBYrgj0DLruk/DODXK4dLRzeSqne0YV+HPCSsqj0dqEXa976SP9tVqIyI69wUjF6gQ==;EndpointSuffix=core.windows.net", "waterlevels")
        task = {'PartitionKey': '1', 'RowKey': str(rowkey), 'Level': level}
        table_client.create_entity(task)
    except Exception as e:
        print(f"Could not finish task run_count_images_task: Reason: {e}")

def server():
    manager_app = flask_app()
    print("Serving on http://localhost:80/")
    serve(manager_app, port=80)
