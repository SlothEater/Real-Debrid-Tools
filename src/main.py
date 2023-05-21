import argparse
import os
import time
import requests
import shutil
from flask import Flask, request
from constants import HEADERS, TIMEOUT, AVAILABLE_HOSTS_URL, ADD_MAGNET_URL, \
    TORRENT_INFO_URL, SELECT_FILES_URL, UNRESTRICT_LINK_URL, VLC_PATH

app = Flask(__name__)


def get_available_hosts():
    hosts_response = requests.get(AVAILABLE_HOSTS_URL, headers=HEADERS)
    hosts = hosts_response.json()
    return hosts


def convert_magnet_to_rd_link(magnet_link, host):
    add_magnet_data = {'magnet': magnet_link, 'host': host}
    add_magnet_response = requests.post(ADD_MAGNET_URL,
                                        data=add_magnet_data,
                                        headers=HEADERS)
    add_magnet_data = add_magnet_response.json()
    torrent_id = add_magnet_data['id']
    return torrent_id


def select_files_to_download(torrent_id):
    torrent_info_response = requests.get(f'{TORRENT_INFO_URL}{torrent_id}',
                                         headers=HEADERS)
    torrent_info_data = torrent_info_response.json()
    file_ids = [str(file['id']) for file in torrent_info_data['files']]
    requests.post(f'{SELECT_FILES_URL}{torrent_id}',
                  data={'files': ','.join(file_ids)},
                  headers=HEADERS)


def check_download_status(torrent_info_url):
    while True:
        torrent_info_response = requests.get(torrent_info_url, headers=HEADERS)
        torrent_info_data = torrent_info_response.json()
        if torrent_info_data['status'] == 'downloaded':
            break
        time.sleep(TIMEOUT)


def get_download_link(torrent_info_data):
    download_link = torrent_info_data['links'][0]
    return download_link


def unrestrict_link(download_link):
    unrestrict_link_data = {'link': download_link}
    unrestrict_link_response = requests.post(UNRESTRICT_LINK_URL,
                                             data=unrestrict_link_data,
                                             headers=HEADERS)
    unrestricted_link = unrestrict_link_response.json()['download']
    return unrestricted_link


def open_in_vlc(unrestricted_link):
    os.system(r'"{}" {}'.format(VLC_PATH, unrestricted_link))


def main(magnet_link, destination):
    hosts = get_available_hosts()
    host = hosts[0]

    torrent_id = convert_magnet_to_rd_link(magnet_link, host)

    select_files_to_download(torrent_id)

    torrent_info_url = f'{TORRENT_INFO_URL}{torrent_id}'
    check_download_status(torrent_info_url)

    torrent_info_response = requests.get(torrent_info_url, headers=HEADERS)
    torrent_info_data = torrent_info_response.json()

    download_link = get_download_link(torrent_info_data)

    unrestricted_link = unrestrict_link(download_link)

    if destination == 'v':
        open_in_vlc(unrestricted_link)
    elif destination == 'f':
        return unrestricted_link


@app.route('/trigger-vlc', methods=['POST'])
def trigger_vlc():
    magnet_link = request.form.get('magnet_link')
    main(magnet_link, 'v')
    return {'ok': True}


@app.route('/trigger-save', methods=['POST'])
def trigger_save():
    magnet_link = request.form.get('magnet_link')
    download_links = main(magnet_link, 'f')
    return {'download_links': download_links}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
