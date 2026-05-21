from http.server import BaseHTTPRequestHandler
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cart import calculate_cart


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length))
        try:
            payment, consumed = calculate_cart(
                int(data["total_amount"]),
                data["membership_rank"],
                data["coupon"],
                int(data["points_to_use"]),
            )
            self._respond(200, {"payment": payment, "consumed_points": consumed})
        except Exception as e:
            self._respond(400, {"error": str(e)})

    def _respond(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body, ensure_ascii=False).encode())
