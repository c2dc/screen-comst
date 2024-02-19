from  urllib.request import urlopen
from  urllib.parse import quote
from os.path import exists
import json
import sys


_BD = "/home/rehosting/screen-sbrc-2023/FirmAE/sbrc/bd/"

vulns={
        "VENDOR":"",
        "MODEL":"",
        "VERSION":"",
        "LOW":0,
        "MEDIUM":0,
        "HIGH":0,
        "CRITICAL":0
    }

def readSemgrep(fileName):

    if exists(fileName):
        f = open(fileName)
        data = json.load(f)
       
        for cve in data['results']:
            #print(json.dumps(cve['cve']['id'], indent=1))
            #cwe=cve['extra']['metadata']['cwe'][0]
            #impact=cve['extra']['metadata']['impact']
            #path=cve['path'].split('/')[2]
            if len(cve['extra']['metadata']['cwe']) > 1:
                print(cve['extra']['metadata']['cwe'])
                print(cve['path'].split('/')[2])

            #print(cwe + "\n" + impact + "\n" + path)
    else:
        print("Erro!")
    

readSemgrep(sys.argv[1])