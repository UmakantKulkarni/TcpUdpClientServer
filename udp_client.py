#!/usr/bin/env python3
"""
A simple client for talking to a UDP echo server and logging the transactions.
"""
import argparse
import itertools
import logging
import socket
import time
import sys
from random import choice
from string import ascii_uppercase

logger = logging.getLogger(__name__)

# the buffer for receiving incoming messages
BUFFER_SIZE = 4096


def send_and_receive_one(sock, message, addr):
    "Sends a single datagram over the socket and waits for the response."
    output_len = sock.sendto(message.encode(), addr)
    logger.info("Sent message to %s: %s (%s bytes).", addr, message, output_len)
    try:
        input_data, addr = sock.recvfrom(BUFFER_SIZE)
        logger.info("Received message back from %s: %s (%s bytes).", addr, input_data.decode(), len(input_data))
    except socket.timeout:
        logger.warning("Message never received back from %s: (%s).", addr, message)


def start(args):
    "Starts sending messages to the server."
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)  # seconds
    sock.bind((args.client_ip, args.client_port))
    addr = (args.server_ip, args.server_port)
    message = ''.join(choice(ascii_uppercase) for i in range(args.size))
    max_msg = args.count
    if args.count == 0:
        max_msg = 2
    i = 1
    try:
        while i <= max_msg:
            send_and_receive_one(sock, message, addr)
            i = i + 1
            if args.count == 0:
                max_msg = max_msg + 1
    finally:
        logger.info("Shutting down.")
        sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__, formatter_class = argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--server_ip', help = 'The host that the client should connect to.', default = "127.0.0.1")
    parser.add_argument('--server_port', help = 'The port that the client should connect to.', type = int, default = 61592)
    parser.add_argument('--client_ip', help = 'Client\'s local IP address.', default = "127.0.0.1")
    parser.add_argument('--client_port', help = 'Client\'s local port.', type = int, default = 61592)
    parser.add_argument('--verbose', '-v', help = "Increases the logging verbosity level.", action = 'count')
    parser.add_argument('--count', '-c', help = 'Number of udp packets to be sent', type = int, default = 1)
    parser.add_argument('--size', '-s', help = 'size of udp data to be sent in payload', type = int, default = 64)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.INFO,
                        format = '%(asctime)s %(levelname)s %(message)s')
    start(args)
