import logging
import requests
import os
import sys
from pathlib import Path

import subprocess

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class Bulletin():
    TYPE = "image" # Could be changed to pdf,individual
    FILES = [Path("/tmp.im1.jpg"),Path("/tmp.im2.jpg")] #TODO init these files
    ISTRANSLATE = "False"

    def __init__(self,**kwargs):
        try:
            self.state = kwargs['state']
        except KeyError:
            logging.error("State name not passed")
        
        try:
            self.type = kwargs['type']
        except KeyError:
            self.type = self.TYPE
            logging.info("Bulletin type defaulted to image")
        
        try:
            self.files = kwargs['files']
        except KeyError:
            logging.error("Bulletin files not passed. Using sample images")
            self.files = self.FILES

        if not isinstance(self.files, list):
            logger.error('Files should be passed as list')
            raise TypeError

    def get_detailed(self,**kwargs):
        '''
        Call the ocr library to get the corresponding text
        '''
        if (self.state in ["Bihar","Uttar Pradesh"] and self.type != "individual"):
            is_translate = "True"
        else:
            is_translate = "False"
        start_district = ""
        libpath = Path(Path('.').absolute() , "./webScraper/automation/ocr")
        message = ""

        for impath in self.files:
            logging.info(impath)
            # cmd = ['sh', 'ocr.sh', '/tmp/im.jpg', 'Bihar', '', 'False', 'individual']
            command = ["sh",
            "ocr.sh",
            str(impath),
            str(self.state),
            str(start_district),
            str(is_translate),
            str(self.type)
            ]
            logging.info(command)

            # Execute the command
            result = subprocess.run(command,
            cwd=libpath,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
            

            if result.stdout != b'':
                logging.info("Results obtained")
                message = message + result.stdout.decode("utf-8")
            elif result.stderr != b'':
                logging.error("OCR error")
                message = message + result.stderr.decode("utf-8")
            else:
                logger.error("No response from subprocess")
                return -1
        return "```\n" + message.strip() + "\n```"




