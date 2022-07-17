# -*- coding: UTF-8 -*-

# standard
import configparser
from distutils.command.config import config

# module
import gdrivepdfdl


def main():
    
    # 初期設定
    settings_file_path = 'settings.ini'
    config = configparser.ConfigParser()
    
    if (not config.read(settings_file_path)):
        print(f'{settings_file_path} is not found.')
        return
    
    # [bin]
    proxy_bat_path        = config['bin']['proxy_bat_path']
    edge_driver_path      = config['bin']['edge_driver_path']
    # [userdata]
    edge_profile_path     = config['userdata']['edge_profile_path']
    gdrive_url            = config['userdata']['gdrive_url']
    # [settings]
    mime_type             = config['settings']['mime_type']
    mode                  = config['settings']['mode']
    width                 = int(config['settings']['width'])
    rendering_waiting_sec = int(config['settings']['rendering_waiting_sec'])
    access_waiting_sec    = int(config['settings']['access_waiting_sec'])
    output_dir            = config['settings']['output_dir']

    print(f"Proxy bat path          : {proxy_bat_path}")
    print(f"Edge driver path        : {edge_driver_path}")
    print(f"Edge profile path       : {edge_profile_path}")
    print(f"Google drive folder url : {gdrive_url}")
    print(f"mime_type               : {mime_type}")
    print(f"q(quality) or s(speed)  : {mode}")
    print(f"width                   : {width}")
    print(f"rendering wait sec      : {rendering_waiting_sec}")
    print(f"access wait sec         : {access_waiting_sec}")
    print(f"output dir              : {output_dir}")

    gdh = gdrivepdfdl.GDriveHar(proxy_bat_path, edge_driver_path, edge_profile_path, gdrive_url)
    
    pdf_data = gdh.get(mode, mime_type, width, rendering_waiting_sec, access_waiting_sec)
    urls = gdrivepdfdl.Utility.to_base64_list(pdf_data['har'], mime_type)
    gdrivepdfdl.Utility.save_image(output_dir, urls,  pdf_data['pdf_infos'], mime_type, True)


if __name__ == '__main__':
    main()

