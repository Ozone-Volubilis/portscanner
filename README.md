# portscanner

A small TCP connect port scanner written in Python, using only the standard library.

I'm building it step by step as part of my cybersecurity learning path, to understand what tools like nmap do underneath. It isn't meant to replace them.

## Features

- Scans a range of TCP ports on a host and lists the open ones
- Accepts a hostname or an IP address
- Validates its input and fails with a clear message instead of a traceback:
  - ports outside 1–65535
  - hostnames that can't be resolved, including names too long to be valid
  - a reversed range (`30010 30000`) is swapped instead of rejected
- Stops cleanly on Ctrl+C, with exit code 130 (the Unix convention for an interrupted program)
- Filters out TCP self-connects, a source of false positives when scanning localhost (see below)

## Requirements

Python 3. No third-party packages.

## Usage

```
usage: portscanner.py [-h] hostname firstport lastport

This tool scans a range of ports on a targeted host

positional arguments:
  hostname    enter host address
  firstport   the first port of the investigated range
  lastport    the last port of the investigated range
```

Example:

```
$ python3 portscanner.py localhost 1 65535
Port 34567 is open
```

## How it works

For each port in the range, the scanner opens a TCP socket and attempts a full connection with `connect_ex`, which returns 0 when the connection succeeds. A successful connection means something is listening on that port. Each attempt has a 1-second timeout, and each socket is closed automatically by a `with` block, even if the scan is interrupted.

The hostname is resolved to an IPv4 address once, before the scan starts.

## A false positive I found: TCP self-connect

While scanning localhost over a large range, the scanner reported ports as open (for example 45168, later 35830 and 37070) that `ss -tlnp` showed nothing listening on, and that disappeared when I scanned again.

The cause is a TCP quirk. Every outgoing connection gets a random source port from Linux's ephemeral range (32768–60999). When a scan of localhost covers that range, the kernel will sooner or later give a socket the same source port as the destination port it's trying to reach. TCP then lets the socket connect to itself ("simultaneous open"), and `connect_ex` reports success even though no service exists.

The fix: after a successful connection, compare the socket's local end (`getsockname()`) with its remote end (`getpeername()`). If they're identical, the socket connected to itself, and the port isn't reported. After the fix, several full scans of 1–65535 on localhost reported only the port I had a listener on.

## Limitations

- **Slow**: ports are scanned one at a time. A port that doesn't answer costs the full 1-second timeout, so large ranges against a remote host can take hours.
- **TCP connect only**: completes the full handshake, so it's easy to spot in the target's logs. No SYN or UDP scanning.
- **IPv4 only** (`gethostbyname`).
- **No service detection**: it says a port is open, not what's running on it.

## Roadmap

- [ ] Scan ports concurrently with `concurrent.futures`
- [ ] `--timeout` option
- [ ] Banner grabbing, to show what answers on each open port
- [ ] IPv6 support with `getaddrinfo`
- [ ] Tests

## Legal

Only scan systems you own or have written permission to test. For practice, use your own lab, or `scanme.nmap.org`, which the nmap project provides for exactly this purpose.
