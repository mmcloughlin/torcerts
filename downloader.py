import subprocess
import os
import os.path
import uuid
import logging
import random

import requests


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
            return None

    return path


def write_summary(addr, filename):
    summary_filename = filename + '.summary'
    with open(summary_filename, 'w') as f:
        f.write('addr={}\n'.format(addr))
        f.write('now=')
        f.flush()
        args = ['date', '-u']
        subprocess.check_call(args, stdin=DEVNULL, stdout=f, stderr=DEVNULL)
        args = ['openssl', 'x509', '-startdate', '-in', filename]
        subprocess.check_call(args, stdin=DEVNULL, stdout=f, stderr=DEVNULL)


def download_relay_certificates(num, output_dir='./certs'):
    data = fetch_relays(limit=num)
    relays = data['relays']
    random.shuffle(relays)

    for relay in relays:
        if not relay['running']:
            continue

        addr = relay['or_addresses'][0]
        filepath = download_certificate_to_directory(addr, output_dir)
        if filepath is None:
            continue
        write_summary(addr, filepath)


def main():
    logging.basicConfig(level=logging.DEBUG)
    download_relay_certificates(1000)


if __name__ == '__main__':
    main()
