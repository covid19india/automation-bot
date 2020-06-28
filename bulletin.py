import logging
import requests
import os
import sys
from pathlib import Path

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class Bulletin():
    BULLETIN_TYPE = "image" # Could be changed to pdf while init
    TMP_DIR = "/tmp"

    def __init__(self,**kwargs):
        try:
            self.state = kwargs['state']
        except KeyError:
            logging.error("State name not passed")
        
        try:
            self.bulletin_type = kwargs['bulletin_type']
        except KeyError:
            self.bulletin_type = self.BULLETIN_TYPE
            logging.info("Bulletin type defaulted to image")
        
        try:
            self.tmp_dir = kwargs['tmp_dir']
        except KeyError:
            self.tmp_dir = self.TMP_DIR
            logging.debug(f"Looking for files in {self.tmp_dir}")



    def self.get_detailed():
        '''
        Call the ocr library to get the corresponding text
        '''
        return detail
    def self.get_full_text():
        '''
        Call the ocr library to get exact text to be added
        to raw data sheet
        '''
        return fulltext

    def self.error_handle():
        '''
        Make sure that the extracted values are correct
        with some error handling code
        '''
        return 0




