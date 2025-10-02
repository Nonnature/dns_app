from flask import Flask, request, jsonify, Response
import socket

app = Flask(__name__)

def send_udp_register(as_ip, as_port, hostname, ip, ttl="10"):
    msg = f"TYPE=A\nNAME={hostname} VALUE={ip} TTL={ttl}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), (as_ip, 53533))
    sock.close()

def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a+b
    return a

@app.put("/register")
def register():
    data = request.get_json(silent=True) or {}
    required = {"hostname","ip","as_ip","as_port"}
    if not required.issubset(data):
        return jsonify(error="bad request"), 400
    try:
        send_udp_register(data["as_ip"], int(data["as_port"]), data["hostname"], data["ip"])
        return Response(status=201)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.get("/fibonacci")
def fibonacci():
    num = request.args.get("number", "")
    if not num.isdigit():
        return jsonify(error="bad format"), 400
    val = fib(int(num))
    return jsonify(result=val), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)