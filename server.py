import logging
import logging.config
import os
import socketserver

from lib.parser import parse_string, MalformedExpression, InvalidToken


logging_conf = os.environ.get("SERVER_LOGGING_CONF")
if logging_conf:
    logging.config.fileConfig(logging_conf)

log = logging.getLogger("arithmeticServer")

if not logging_conf:
    ch = logging.StreamHandler()
    log.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(fmt)
    log.addHandler(ch)


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for the arithmetic server.

    The handler receives an arithmetic operation encoded in asccii and returns its
    evaluation to the client.
    """

    def close_session(self):
        log.info(
            "{}:{} end session".format(
                self.client_address[0],
                self.client_address[1],
            )
        )

    def handle(self):
        while True:
            try:
                data = self.request.recv(1024)
            except BrokenPipeError:
                self.close_session()
                break
            if not data:
                self.close_session()
                break
            self.data = data.strip()
            log.info(
                "Received from {}:{}".format(
                    self.client_address[0], self.client_address[1]
                )
            )
            try:
                msg = self.data.decode("ascii")
            except UnicodeDecodeError:
                log.debug("{} got decoding error".format(self.client_address[0]))
                self.request.sendall("error: decoding error".encode("ascii"))
                continue
            try:
                expr = parse_string(msg)
            except MalformedExpression:
                log.debug("{} sent malformed expression".format(self.client_address[0]))
                self.request.sendall("error: malformed expression".encode("ascii"))
            except InvalidToken as err:
                log.debug(
                    "{} sent expression with invalid token".format(
                        self.client_address[0]
                    )
                )
                self.request.sendall(f"error: {str(err)}".encode("ascii"))
            else:
                result = expr.result
                log.debug("{}: {} = {}".format(self.client_address[0], msg, result))
                self.request.sendall(str(result).encode("ascii"))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    with socketserver.ForkingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
