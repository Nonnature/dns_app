from flask import Flask, request, jsonify
import socket, requests, re

app = Flask(__name__)

def dns_query(as_ip: str, name: str) -> str:
    msg = f"TYPE=A\nNAME={name}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    sock.sendto(msg.encode(), (as_ip, 53533))
    data, _ = sock.recvfrom(2048)
    sock.close()
    text = data.decode()
    m = re.search(r"VALUE=([0-9.]+)", text)
    if not m:
        raise RuntimeError("No A record found")
    return m.group(1)

@app.get("/fibonacci")
def call_fibonacci():
    params = ("hostname","fs_port","number","as_ip","as_port")
    if any(k not in request.args for k in params):
        return jsonify(error="bad request"), 400
    hostname = request.args["hostname"]
    fs_port  = int(request.args["fs_port"])
    number   = request.args["number"]
    as_ip    = request.args["as_ip"]
    ip = dns_query(as_ip, hostname)
    url = f"http://{ip}:{fs_port}/fibonacci"
    r = requests.get(url, params={"number": number}, timeout=3)
    return (r.content, r.status_code, r.headers.items())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
