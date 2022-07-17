# -*- coding: UTF-8 -*-

# standard
import os
import time
import base64

# numpy
import numpy as np

# opencv
import cv2

# pdf
import img2pdf

class Utility:
    def __init__(self):
        pass

    @staticmethod
    def to_base64_list(har_data, mime_type):
        base64_list = []
        minsize = 1024

        for e in har_data['log']['entries']:
            element = e.get('response').get('content')
            if element.get('encoding') == 'base64':
                if element.get('text'):
                    # iconのような小さいサイズは除外する
                    if element.get('mimeType') == f'image/{mime_type}' and minsize <= element.get('size'):
                        base64_list.append(element.get('text'))

        return base64_list
    
    @staticmethod
    def to_image(base64_data, path):
        # base64データを画像に変換する
        image = np.frombuffer(base64.b64decode(base64_data), dtype=np.uint8)
        decoded_image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # 日本語だと文字化けするので、ファイル名outで出力してから引数の名前へ変換する
        cv2_path = f'{os.path.dirname(path)}/out{os.path.splitext(path)[-1]}'
        cv2.imwrite(cv2_path, decoded_image)
        os.rename(cv2_path, path)

    @staticmethod
    def save_image(save_path, base64_list, pdf_infos, mime_type, is_pdf):
        index = 0
        page = 0
        filename_list = []
        for e in base64_list:
            max_page = int(pdf_infos[index]['total_page'])
            page += 1

            file_name  = f'{os.path.splitext(os.path.basename(pdf_infos[index]["pdf_name"]))[0]}'
            image_path = f'{os.path.dirname(save_path)}/{file_name}-{page}.{mime_type}'
            pdf_path   = f'{os.path.dirname(save_path)}/{file_name}.pdf'

            print((file_name, image_path, pdf_path))

            Utility.to_image(e, image_path)
            filename_list.append(image_path)

            if max_page // (page+1) == 0:
                with open(pdf_path,'wb') as f:
                    if is_pdf:
                        f.write(img2pdf.convert(filename_list))
                        for e in filename_list:
                            os.remove(e)

                page = 0
                index += 1
                filename_list = []


    # sleeping with reason
    @staticmethod
    def sleep_with_reason(sec, reason=None):
        if reason:
            print(f'sleep {sec} sec because {reason}')
        time.sleep(sec)

