# -*- coding: UTF-8 -*-

# standard
import os

# psutil
import psutil

# scaring
from selenium import webdriver
from selenium.webdriver.edge.options import Options

# proxy
from browsermobproxy import Server

# module
from gdrivepdfdl.utility import Utility


class HarServer:
    # public

    def __init__(self, proxy_bat_path, edge_driver_path, edge_profile_path):
        self.proxy_bat_path    = proxy_bat_path
        self.edge_driver_path  = edge_driver_path
        self.edge_profile_path = edge_profile_path

        self.server       = None
        self.proxy_server = None
        self.driver       = None
    
    def start(self):
        # proxyを起動する
        self._start_proxy_server()
        print(f'proxy server is started {self.proxy_server.proxy}')

        # Edgeを起動する
        self._start_webdriver()
        Utility.sleep_with_reason(1, 'webdriver is started')

        # harの取得開始
        self.proxy_server.new_har('gdrive', options={'captureContent': True, 'captureBinaryContent': True})

    def stop(self):
        # proxyを停止する
        self._stop_proxy_server()
        print(f'proxy server is stopped')

        # Edgeを停止する
        self._stop_webdriver()
        print(f'webdriver is stopped')
    
    # private

    def _start_proxy_server(self):
        # proxyを起動する
        self.server = Server(self.proxy_bat_path)
        self.server.start()
        self.proxy_server = self.server.create_proxy()

    def _stop_proxy_server(self):
        # proxyを停止する
        self.proxy_server.close()
        self.server.stop()
        # zombie processが残るのでkillする
        for proc in psutil.process_iter():
            try:
                proc_info = proc.as_dict(attrs=['name', 'cmdline'])
                if proc_info.get('name') in ('java', 'java.exe'):
                    for cmd_info in proc_info.get('cmdline'):
                        if cmd_info == '-Dapp.name=browsermob-proxy':
                            proc.kill()
            except psutil.NoSuchProcess:
                pass
    
    def _start_webdriver(self):
        # Edgeを起動する
        edge_options = Options()
        #edge_options.add_argument('--headless')
        edge_options.add_argument(f'--user-data-dir={os.path.split(self.edge_profile_path)[0]}')
        edge_options.add_argument(f'--profile-directory={os.path.split(self.edge_profile_path)[1]}')
        edge_options.add_argument(f'--proxy-server={self.proxy_server.proxy}')
        self.driver = webdriver.Edge(executable_path=self.edge_driver_path, options=edge_options)
    
    def _stop_webdriver(self):
        # Edgeを停止する
        self.driver.quit()

