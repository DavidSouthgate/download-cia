import argparse
import requests
import os
import sys
from struct import unpack

base_url = 'http://nus.cdn.c.shop.nintendowifi.net/ccs/download/'


def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    args = parse_args()
    title_base_url = base_url + args.title_id
    output_path = os.path.join(script_directory, 'output', args.title_id)
    output_cia_path = os.path.join(script_directory, 'output', args.title_id + '.cia')

    if os.path.exists(output_path):
        print("Error: {} already exists".format(output_path))
        sys.exit(1)

    os.makedirs(output_path)

    download_cetk(title_base_url, output_path)
    tmd = download_tmd(title_base_url, output_path, args.version)
    download_all_content(title_base_url, output_path, tmd)

    make_cdn_cia = os.path.join(script_directory, 'libs/make_cdn_cia/bin/make_cdn_cia')
    os.system('{} {} {}'.format(make_cdn_cia, output_path, output_cia_path))


def download_all_content(title_base_url, output_path, tmd):
    content_count = unpack('>H', tmd[0x206:0x208])[0]
    for i in range(content_count):
        offset = 0xB04+(0x30*i)
        id = format(unpack('>I', tmd[offset:offset+4])[0], '08x')
        path = os.path.join(output_path, id)
        url = os.path.join(title_base_url, id)
        download_bin(url, path)


def parse_args():
    parser = argparse.ArgumentParser(prog='download-cia',
                                     description='Downloads title from Nintendo servers and converts to CIA')
    parser.add_argument('title_id', help="The title id (E.g. 0004013000002F02)")
    parser.add_argument('version', help="The version of this title (E.g. 9217)")
    return parser.parse_args()


def download_cetk(title_base_url, output_path):
    cetk_url = title_base_url + '/cetk'
    cetk_output_path = os.path.join(output_path, "cetk")
    download_bin(cetk_url, cetk_output_path)


def download_tmd(title_base_url, output_path, version):
    tmd_url = title_base_url + '/tmd.' + version
    cetk_output_path = os.path.join(output_path, "tmd")
    return download_bin(tmd_url, cetk_output_path)


def download_bin(url, output_path):
    response = requests.get(url)
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return response.content


if __name__ == "__main__":
    main()
