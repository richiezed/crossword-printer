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
import webbrowser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv

#Environment variables in use
load_dotenv()

CHROMIUM_PATH = os.getenv("CHROMIUM_PATH")
CHROMIUM_PROFILE = os.getenv("CHROMIUM_PROFILE")
WEBDRIVER_PATH = os.getenv("WEBDRIVER_PATH")
PAGE_URL = os.getenv("PAGE_URL")

print("CHROMIUM_PATH " + str(CHROMIUM_PATH))
print("CHROMIUM_PROFILE " + str(CHROMIUM_PROFILE))
print("WEBDRIVER_PATH " + str(WEBDRIVER_PATH))
print("PAGE_URL " + str(PAGE_URL))

class PdfGenerator:
    driver = None
    # https://chromedevtools.github.io/devtools-protocol/tot/Page#method-printToPDF
    print_options = {
        'landscape': True,
        'displayHeaderFooter': False,
        'printBackground': False,
        'preferCSSPageSize': False,
        'pageRanges': "1",
        'marginTop': .1,
        'marginBottom': .1,


      #  'paperWidth': 8.3,
      #  'paperHeight': 11.7,
  
    }

    def __init__(self, urls: List[str]):
        self.urls = urls

    def _get_pdf_from_url(self, url, *args, **kwargs):
        self.driver.get(url)
        time.sleep(0.3)  # allow the page to load, increase if needed
#TODO: Check if logged in


        #webbrowser.get("/snap/bin/chromium").open("https://www.theage.com.au")
        #exit()

        try: 
            button=self.driver.find_element(By.ID, "myAccountMenuButton") 
            print("Logged in, proceding to print stage") 
        except NoSuchElementException as e: 
            self.driver.close()
            print("Not logged in, please log in")
            webbrowser.get(CHROMIUM_PATH).open(PAGE_URL) #THis may not be needed, this is on an exception path!
            
            #print("/snap/chromium/current/usr/lib/chromium-browser/chrome --user-data-dir=" + os.path.expanduser("~") + "/snap/chromium/common/chromium")
            #os.system("/snap/chromium/current/usr/lib/chromium-browser/chrome --user-data-dir=" + os.path.expanduser("~") + "/snap/chromium/common/chromium")
            #os.system("/snap/chromium/current/usr/lib/chromium-browser/chrome --user-data-dir=" + os.path.expanduser("~") + "/snap/chromium/common/chromium" + " https://www.theage.com.au")


            #exit()
        #print(self.driver.find_element(By.ID, "myAccountMenuButton"))
        #print(self.driver.find_element(By.CSS_SELECTOR, "button._2CAtX").tag_name)

        
        elem = self.driver.find_element(By.CLASS_NAME, "_5bcpS")
        #print (elem)

        # This prints the header on the left
        self.driver.execute_script("arguments[0].removeAttribute('class')", elem) 

        # This prints the header in the middle
        #self.driver.execute_script("arguments[0].setAttribute('class', 'p3h3q EdtFg')", elem) 


        #const element = document.getElementById('yourElementId');

       # myElement.removeClass('_5bcpS')

#        <header class="k4t-m"><div class="_5bcpS p3h3q EdtFg">
#document.querySelector("#content > div > header")

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
        webdriver_options.add_argument('--disable-dev-shm-usage')
        webdriver_options.add_argument('--disable-gpu')
        #webdriver_options.add_argument('--no-sandbox')
        webdriver_options.add_argument('--disable-software-rasterizer')
        home_dir = os.path.expanduser("~") + "/"
        chrome_profile= home_dir + CHROMIUM_PROFILE
        #webdriver_options.add_argument("--user-data-dir=/cw/config") 
        #webdriver_options.add_argument("--profile-directory=chrome-profile")
        print(chrome_profile)
        webdriver_options.add_argument('--user-data-dir=' + chrome_profile)
       # webdriver_options.add_argument('--user-data-dir=/cw/config/chrome-profile')
        chromium_path = CHROMIUM_PATH
        webdriver_options.binary_location = chromium_path
        
        try:
            chromedriver_path = ChromeService(executable_path=WEBDRIVER_PATH)
            #self.driver = webdriver.Chrome(service=chromedriver_path, options=webdriver_options)
            self.driver = webdriver.Chrome(service=chromedriver_path, options=webdriver_options)
            result = self._generate_pdfs()

        finally:
            self.driver.close()

        return result


       # <button aria-controls="myAccountMenu" aria-expanded="false" class="_3s-xg _2CAtX" id="myAccountMenuButton" data-testid="my-account-menu"><span class="_22xoE">Richie Z</span><span class="_2Rpde"><svg aria-hidden="true" class="QMY9O" focusable="false" height="24px" width="24px"><use xlink:href="#icon-account"></use></svg></span></button>
      #  <span class="_22xoE">Richie Z</span>
