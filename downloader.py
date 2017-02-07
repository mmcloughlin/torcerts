import requests
import subprocess
import os
import os.path
import uuid
import logging
import random


DEVNULL = open(os.devnull, 'w')


def fetch_relays(limit=100):
    url = 'https://onionoo.torproject.org/details'
    params = dict(
            limit=limit,
            )
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json()


def download_certificate(addr, output):
    logging.info('downloading certificate for addr=%s', addr)
    args = ['openssl', 's_client', '-connect', addr]
    subprocess.check_call(args, stdin=DEVNULL, stdout=output, stderr=DEVNULL)


def download_certificate_to_directory(addr, output_dir='./certs'):
    filename = str(uuid.uuid4())
    path = os.path.join(output_dir, filename)

    with open(path, 'w') as f:
        try:
            download_certificate(addr, f)
        except Exception as e:
            logging.error(e)


def download_relay_certificates(num, output_dir='./certs'):
    data = fetch_relays(limit=num)
    relays = data['relays']
    random.shuffle(relays)

    for relay in relays:
        if not relay['running']:
            continue

        addr = relay['or_addresses'][0]
        download_certificate_to_directory(addr, output_dir)


def main():
    logging.basicConfig(level=logging.DEBUG)
    download_relay_certificates(100)


if __name__ == '__main__':
    main()
