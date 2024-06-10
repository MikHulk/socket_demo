import logging
import logging.config
import os
import signal
import socketserver

from lib.parser import parse_string, MalformedExpression, InvalidToken


logging_conf = os.environ.get("SERVER_LOGGING_CONF")
if logging_conf:
    logging.config.fileConfig(logging_conf)

log = logging.getLogger("arithmeticServer")

# default logging configuration
if not logging_conf:
    ch = logging.StreamHandler()
    log.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(fmt)
    log.addHandler(ch)


class ArithmeticTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for the arithmetic server.

    The handler receives an arithmetic operation encoded in asccii and returns its
    evaluation to the client.
    """

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def close_session(self, child_pid):
        os.kill(child_pid, signal.SIGTERM)
        os.waitpid(child_pid, os.WNOHANG)
        self.from_worker.close()
        self.to_worker.close()
        self.from_parent.close()
        self.to_parent.close()
        log.info(
            "{}:{} end session".format(
                self.client_address[0],
                self.client_address[1],
            )
        )

    def wait_for_expression(self):
        while True:
            msg = self.from_parent.readline()
            try:
                msg = msg.decode('ascii')
            except UnicodeDecodeError:
                log.debug("{} got decoding error".format(self.client_address[0]))
                self.to_parent.write("error: decoding error\n".encode("ascii"))
                continue
            try:
                expr = parse_string(msg.strip())
            except MalformedExpression:
                log.debug("{} sent malformed expression".format(self.client_address[0]))
                self.to_parent.write("error: malformed expression\n".encode("ascii"))
            except InvalidToken as err:
                log.debug(
                    "{} sent expression with invalid token".format(
                        self.client_address[0]
                    )
                )
                self.to_parent.write(f"error: {str(err)}\n".encode("ascii"))
            else:
                result = expr.result
                log.debug("{}: {} = {}".format(self.client_address[0], msg.strip(), result))
                self.to_parent.write(str(result).encode("ascii"))
                self.to_parent.write(b'\n')
            

    def handle(self):
        r, w = os.pipe()
        self.from_worker = os.fdopen(r, 'rb', 0)
        self.to_parent = os.fdopen(w, 'wb', 0)
        r, w = os.pipe()
        self.from_parent = os.fdopen(r, 'rb', 0)
        self.to_worker = os.fdopen(w, 'wb', 0)
        child_pid = os.fork()
        if not child_pid:
            self.wait_for_expression()
        while True:
            try:
                data = self.request.recv(1024)
            except BrokenPipeError:
                self.close_session(child_pid)
                break
            if not data:
                self.close_session(child_pid)
                break
            data = data.strip()
            log.info(
                "Received from {}:{}".format(
                    self.client_address[0], self.client_address[1]
                )
            )
            self.to_worker.write(data)
            self.to_worker.write(b'\n')
            result = self.from_worker.readline().strip()
            self.request.sendall(result)


if __name__ == "__main__":
    host = os.environ.get("SERVER_LISTEN_ADDRESS", "localhost")
    port = int(os.environ.get("SERVER_PORT", 9999))

    with socketserver.ForkingTCPServer((host, port), ArithmeticTCPHandler) as server:
        server.serve_forever()
