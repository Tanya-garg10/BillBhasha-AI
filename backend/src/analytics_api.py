"""
Simple analytics API server for BillBhasha AI call analytics.
This provides an HTTP endpoint to get call analytics data.
"""

import os
from pathlib import Path
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Add src directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.memory import get_call_analytics

load_dotenv(".env.local")

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get call analytics metrics."""
    try:
        analytics = get_call_analytics()
        return jsonify(analytics), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.getenv('ANALYTICS_PORT', 8001))
    print(f"Starting analytics API server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)