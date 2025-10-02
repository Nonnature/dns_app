import socket, threading, os

DB_FILE = "records.txt"
HOST, PORT = "0.0.0.0", 53533

def load_records():
    db = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                parts = dict(kv.split("=",1) for kv in line.split())
                name = parts.get("NAME")
                if name:
                    db[name] = (parts.get("VALUE"), parts.get("TTL","10"))
    return db

def save_record(name, value, ttl="10"):
    with open(DB_FILE, "a") as f:
        f.write(f"NAME={name} VALUE={value} TTL={ttl}\n")

def handle_packet(data, addr, sock):
    text = data.decode("utf-8", errors="ignore").strip()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("TYPE=A"):
        return
    if len(lines) >= 2 and "VALUE=" in lines[1]:
        parts = dict(kv.split("=",1) for kv in lines[1].split())
        name, value = parts.get("NAME",""), parts.get("VALUE","")
        ttl = parts.get("TTL","10")
        if name and value:
            save_record(name, value, ttl)
    else:
        parts = dict(kv.split("=",1) for kv in lines[1].split())
        name = parts.get("NAME","")
        db = load_records()
        if name in db:
            ip, ttl = db[name]
            resp = f"TYPE=A\nNAME={name} VALUE={ip} TTL={ttl}\n"
            sock.sendto(resp.encode(), addr)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[AS] UDP on {HOST}:{PORT}")
    while True:
        data, addr = sock.recvfrom(2048)
        threading.Thread(target=handle_packet, args=(data, addr, sock), daemon=True).start()

if __name__ == "__main__":
    main()
