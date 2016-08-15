#!/usr/bin/env python

import sys
import base64
import socket
import select
import os

BUFSIZE = 1024


class CorkscrewError(Exception):
    pass


class Corkscrew():

    def __init__(self, proxyhost, proxyport, desthost, destport,
                 authfile=None):
        if authfile:
            with open(authfile, "rt") as f:
                auth = f.readline()
        else:
            auth = None

        # Connect socket
        self.f = socket.create_connection((proxyhost, proxyport))

        # Server handshake
        # Send request to proxy
        uri = "CONNECT %s:%s HTTP/1.0" % (desthost, destport)
        if auth:
            uri = uri + "\nProxy-Authorization: Basic %s" % \
                base64.b64encode(auth)
        uri = uri + "\r\n\r\n"
        os.write(self.f.fileno(), uri)

        # Wait for proxy respond
        answer = self.f.recv(BUFSIZE)
        (pre, code, description) = answer.split(' ', 2)

        code = int(code)
        if not pre.startswith("HTTP/") or code < 200 or code >= 300:
            raise CorkscrewError("Proxy could not open connection to %s: %s" %
                                 (desthost, description))

    def run(self):
        while True:
            (rlist, _, _) = select.select([self.f, sys.stdin], [], [], 5)
            if sys.stdin in rlist:
                info = os.read(sys.stdin.fileno(), BUFSIZE)
                os.write(self.f.fileno(), info)

            if self.f in rlist:
                info = os.read(self.f.fileno(), BUFSIZE)
                os.write(sys.stdout.fileno(), info)


def main():
    argv = sys.argv
    if len(argv) not in [5, 6]:
        print("corkscrew\nusage: corkscrew <proxyhost> <proxyport> <desthost> "
              "<destport> [authfile]")
        return 1
    Corkscrew(*argv[1:]).run()
