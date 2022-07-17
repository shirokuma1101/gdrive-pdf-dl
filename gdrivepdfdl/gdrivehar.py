# -*- coding: UTF-8 -*-

# standard
import re
import urllib.parse

# scaring
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# module
from gdrivepdfdl.utility import Utility
from gdrivepdfdl.harserver import HarServer


class GDriveHar:
    # public

    def __init__(self, proxy_bat_path, edge_driver_path, edge_profile_path, gdrive_url):
        self.har_server   = HarServer(proxy_bat_path, edge_driver_path, edge_profile_path)
        self.gdrive_url   = gdrive_url
    
    def get(self, mode, mime_type=None, width=None, rendering_waiting_sec=None, access_waiting_sec=None):

        har, pdf_infos = self._get_preview_har(mode, access_waiting_sec)
        
        if mode == 'q':
            har = self._get_rendered_har(pdf_infos, mime_type, width, rendering_waiting_sec)

        return {'har': har, 'pdf_infos': pdf_infos}

    # private

    def _get_preview_har(self, mode, access_waiting_sec):
        pdf_infos = []
        self.har_server.start()
        #server       = self.har_server.server
        proxy_server = self.har_server.proxy_server
        driver       = self.har_server.driver
        
        driver.get(self.gdrive_url)
        Utility.sleep_with_reason(5, 'waiting for loading the page')

        # PDFファイル名を列挙する
        soup = BeautifulSoup(driver.page_source, 'lxml')
        pdf_names = [e.text for e in soup.find_all('div', {'data-tooltip': re.compile('PDF:')})]

        # 代替にPDFがあるタグを列挙する
        elements = driver.find_elements(By.XPATH, value='//img[@alt=\"PDF"]')
        print(f'find {len(elements)} pdf files')

        # 取得開始
        for i, e in enumerate(elements):
            print(f'{i+1}th file is downloading')

            # ファイルをブラウザ上で開く
            webdriver.ActionChains(driver).double_click(e).perform()
            Utility.sleep_with_reason(5, 'wait for opening the file')

            # スクロールするための前準備
            driver.find_element(by=By.TAG_NAME, value='body').click()
            break_flag = False

            # sモードの場合はスクロールする
            if mode == 's':
                while True:
                    # 現在の画面を取得する
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    
                    # ページ情報を取得する
                    page_info = self._get_page_info(soup)

                    # スクロールする
                    driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)

                    if break_flag:
                        pdf_infos.append({'pdf_name': pdf_names[i], 'total_page': page_info['total_page']})
                        break
                    if page_info['now_page'] == page_info['total_page']:
                        break_flag = True
                
                    Utility.sleep_with_reason(0.5, 'scroolling')
            
            # qモードの場合は表示して終了
            if mode == 'q':
                # 現在の画面を取得する
                soup = BeautifulSoup(driver.page_source, 'lxml')
                pdf_infos.append({'pdf_name': pdf_names[i], 'total_page': self._get_page_info(soup)['total_page']})

            # プレビューを閉じるためにダブルクリックする
            webdriver.ActionChains(driver).double_click(e).perform()
            Utility.sleep_with_reason(access_waiting_sec, 'next pdf file')
        
        # harの取得終了
        print('har is saved')
        har_data = proxy_server.har
        self.har_server.stop()

        unique_urls = self._make_unique_list(har_data)
        for i, e in enumerate(pdf_infos):
            e['url'] = unique_urls[i]

        # {'pdf_name': str, 'total_page': int, 'url': url}

        # 取得した情報を返す
        return har_data, pdf_infos

    def _get_rendered_har(self, pdf_infos, mime_type, width, rendering_waiting_sec):
        self.har_server.start()
        #server       = self.har_server.server
        proxy_server = self.har_server.proxy_server
        driver       = self.har_server.driver
        
        # urlを編集する
        for e in pdf_infos:
            # mimetypeを変更する
            qs_dict = urllib.parse.parse_qs(e['url'].query)
            if mime_type == 'webp':
                pass
            elif mime_type == 'png':
                del qs_dict['webp']
                qs_dict['png'] = ['true']
            elif mime_type == 'jpeg':
                del qs_dict['webp']
                qs_dict['jpeg'] = ['true']
            else:
                print('mime_type is invalid')
                return
            
            # widthを変更する
            qs_dict['w'] = [f'{width}']
            
            # 取得開始
            for page in range(e['total_page']):
                qs_dict['page'] = [f'{page}']
                driver.get(
                    urllib.parse.urlunparse(e['url']._replace(query=urllib.parse.urlencode(qs_dict, doseq=True)))
                    )
                Utility.sleep_with_reason(rendering_waiting_sec, 'waiting for rendering')

        # harの取得終了
        print('har is saved')
        har_data = proxy_server.har
        self.har_server.stop()

        return har_data

    def _get_page_info(self, soup):
        # ページ情報を取得する
        tag = [tag for tag in soup.find_all('div') if tag.text == 'ページ'][0]
        # ページ数を取得する
        pages = [e.text for e in tag.next_siblings]
        # pages['n', '/', 'n']
        return {'now_page': int(pages[0]), 'total_page': int(pages[2])}

    def _make_unique_list(self, har_data):
        urls = []
        index = 0

        for e in har_data['log']['entries']:
            url = urllib.parse.urlparse(e['request']['url'])

            if url.path == '/viewerng/img':
                if len(urls) == 0:
                    urls.append(url)
                else:
                    # 重複を回避する
                    if urllib.parse.parse_qs(urls[index].query)['id'] != urllib.parse.parse_qs(url.query)['id']:
                        urls.append(url)
                        index += 1
        
        return urls
