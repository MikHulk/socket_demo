import logging
import logging.config
import argparse
import os
import socket


logging_conf = os.environ.get("CLIENT_LOGGING_CONF")
if logging_conf:
    logging.config.fileConfig(logging_conf)

log = logging.getLogger("arithmeticClient")

if not logging_conf:
    ch = logging.StreamHandler()
    log.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(fmt)
    log.addHandler(ch)

parser = argparse.ArgumentParser(
    prog="Arithmetic client",
    description="A client for the arithmetic server",
)
parser.add_argument("host")
parser.add_argument("port", type=int)
parser.add_argument("input_file")
parser.add_argument("output_file")
parser.add_argument(
    "--burst", default=1, type=int, help="how many concurrent query you want"
)


def main():
    args = parser.parse_args()
    burst = args.burst
    sockets = [
        socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(burst + 1)
    ]
    for sock in sockets:
        sock.connect((args.host, args.port))
    with open(args.input_file) as inputs:
        with open(args.output_file, "w") as out:
            sock_id = 0
            for line in inputs:
                sock = sockets[sock_id]
                expr = line.strip()
                log.debug("send: %s", expr)
                sock.sendall(expr.encode("ascii"))
                sock_id += 1
                sock_id %= burst + 1
                if sock_id == 0:
                    for sock in sockets:
                        result = sock.recv(1024)
                        data = result.decode("ascii")
                        log.debug("receive: %s", data)
                        out.write(data)
                        out.write("\n")
            for i in range(sock_id):
                sock = sockets[i]
                result = sock.recv(1024)
                data = result.decode("ascii")
                log.debug("receive: %s", data)
                out.write(data)
                out.write("\n")
                sock.close()


if __name__ == "__main__":
    main()
