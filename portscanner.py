import argparse  # import the commandline parser
import socket  # import the network module
import sys


def scan_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # create a TCP socket
        s.settimeout(1)  # set a timeout
        if (
            s.connect_ex((ip, port)) != 0
        ):  # 0 means the port is open, so if the port is unavailable, just exit the function with return and the False goes in the loop
            return False
        return (
            s.getsockname() != s.getpeername()
        )  # so only if the port is open, then check for self-connections that often give false positives by comparing the identity of the host and the peer


parser = argparse.ArgumentParser(
    description="This tool scans a range of ports on a targeted host"
)
parser.add_argument("hostname", help="enter host address")
parser.add_argument(
    "firstport", type=int, help="the first port of the investigated range"
)
parser.add_argument(
    "lastport", type=int, help="the last port of the investigated range"
)
args = parser.parse_args()

if not (1 <= args.firstport <= 65535 and 1 <= args.lastport <= 65535):
    parser.error("ports must be between 1 and 65535")
try:
    target_ip = socket.gethostbyname(args.hostname)
except (socket.gaierror, UnicodeEncodeError):
    parser.error("could not resolve host")
if (
    args.firstport > args.lastport
):  # this takes care of the case where user inverts the range
    args.firstport, args.lastport = args.lastport, args.firstportS
try:  # 3 levels of nesting. it is time to create a function at least for the with block
    for port in range(args.firstport, args.lastport + 1):
        if scan_port(
            target_ip, port
        ):  # No need to add the ==True because if is already a check on True/False
            print(f"Port {port} is open")
except KeyboardInterrupt:
    print("\nScan Interrupted")
    sys.exit(130)
