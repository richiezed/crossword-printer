#!/usr/bin/env python3

# Based on a library found at
# https://medium.com/@nikitatonkoshkur25/create-pdf-from-webpage-in-python-1e9603d6a430
# Updated for snap version of chromium

import base64
import json
import logging
import time
from io import BytesIO
from typing import List
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


class PdfGenerator:
    driver = None
    # https://chromedevtools.github.io/devtools-protocol/tot/Page#method-printToPDF
    print_options = {
        'landscape': True,
        'displayHeaderFooter': False,
        'printBackground': False,
        'preferCSSPageSize': False,
        'pageRanges': "1",
    }

    def __init__(self, urls: List[str]):
        self.urls = urls

    def _get_pdf_from_url(self, url, *args, **kwargs):
        self.driver.get(url)
        time.sleep(0.3)  # allow the page to load, increase if needed
#TODO: Check if logged in
        print_options = self.print_options.copy()
        result = self._send_devtools(self.driver, "Page.printToPDF", print_options)
        return base64.b64decode(result['data'])

    @staticmethod
    def _send_devtools(driver, cmd, params):
        """from selenium.webdriver.chrome.service import Serviceus commands to it.
        """
        resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
        url = driver.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = driver.command_executor._request('POST', url, body)
        return response.get('value')

    def _generate_pdfs(self):
        pdf_files = []

        for url in self.urls:
            print(url)
            result = self._get_pdf_from_url(url)
            file = BytesIO()
            file.write(result)
            pdf_files.append(file)

        return pdf_files

    def main(self) -> List[BytesIO]:
        webdriver_options = ChromeOptions()
        webdriver_options.add_argument('--headless')
        webdriver_options.add_argument('--disable-gpu')
        home_dir = os.path.expanduser("~")
        chrome_profile= home_dir + "/snap/chromium/common/chromium"


        webdriver_options.add_argument('--user-data-dir=' + chrome_profile)
        chromium_path = "/snap/chromium/current/usr/lib/chromium-browser/chrome"
        webdriver_options.binary_location = chromium_path

        try:
            chromedriver_path = ChromeService(executable_path="/snap/chromium/current/usr/lib/chromium-browser/chromedriver")
            self.driver = webdriver.Chrome(service=chromedriver_path, options=webdriver_options)
            result = self._generate_pdfs()

        finally:
            self.driver.close()

        return result
