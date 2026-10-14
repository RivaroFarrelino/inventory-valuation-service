import logging
import sys

import mysql.connector
from flask import Flask, jsonify

from inventory import MYSQL_CONFIG, iv_bp, siapkan_inventory

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger('inventory-valuation')

app = Flask(__name__)
app.register_blueprint(iv_bp)


@app.route('/health', methods=['GET'])
def health_check():
    konfigurasi = dict(MYSQL_CONFIG)
    konfigurasi['connection_timeout'] = 3
    try:
        connection = mysql.connector.connect(**konfigurasi)
        connection.close()
        return jsonify({'status': 'ok', 'database': 'connected'})
    except Exception as error:
        logger.error('health check database gagal: %s', error)
        return jsonify({'status': 'ok', 'database': 'tidak bisa dihubungi'})


siapkan_inventory()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
