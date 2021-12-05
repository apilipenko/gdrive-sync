#!/usr/bin/python
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

import os
import yaml
import logging
import json

GDRIVE_SETTINGS = 'gdrive-settings.yaml'
logging.root.setLevel("INFO")


def get_settings():
    folder_id = None
    setting_file = os.path.join(os.path.curdir, GDRIVE_SETTINGS)
    if os.path.exists(setting_file):
        with open(setting_file) as f:
            config_map = yaml.safe_load(f)
            folder_id = config_map["parent_id"]
            logging.info(f'File [{GDRIVE_SETTINGS} found. Using folder [{folder_id}]]')
    else:
        logging.info(f'File [{GDRIVE_SETTINGS} not found]')
    return folder_id


def file_meta(file_name: str, parent_folder_id: str = None):
    if not file_name:
        raise RuntimeError('file_name is empty')
    meta = {'title': file_name}
    if parent_folder_id:
        meta['parents'] = [{'id': parent_folder_id}]
    return json.dumps(meta)


def upload_file(file_path: str):
    get_settings()

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file_name = os.path.basename(file_path)
    parent_folder = get_settings()
    meta = file_meta(file_name, parent_folder)
    f = drive.CreateFile(meta)
    f.SetContentFile(file_path)
    f.Upload()

    # Due to a known bug in pydrive if we
    # don't empty the variable used to
    # upload the files to Google Drive the
    # file stays open in memory and causes a
    # memory leak, therefore preventing its
    # deletion
    f = None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    files = set(os.listdir(os.path.curdir))
    if files.__contains__(GDRIVE_SETTINGS):
        files.remove(GDRIVE_SETTINGS)

    for f in files:
        logging.info(f'File [{f}] will be uploaded')

    # print(get_settings())
    # upload_file('/home/apilipenko/bigdata.png')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
