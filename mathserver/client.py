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


def main():
    args = parser.parse_args()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((args.host, args.port))
        with open(args.input_file) as inputs:
            with open(args.output_file, "w") as out:
                for line in inputs:
                    expr = line.strip()
                    log.debug("send: %s", expr)
                    sock.sendall(expr.encode("ascii"))
                    result = sock.recv(1024)
                    data = result.decode("ascii")
                    log.debug("receive: %s", data)
                    out.write(data)
                    out.write("\n")


if __name__ == "__main__":
    main()
