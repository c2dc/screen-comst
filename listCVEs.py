from  urllib.request import urlopen
from  urllib.parse import quote
from os.path import exists
import json
import sys


_BD = "/home/osmany/Dropbox/ITA/SBRC23/bd/"

vulns={
        "VENDOR":"",
        "MODEL":"",
        "LOW":0,
        "MEDIUM":0,
        "HIGH":0,
        "CRITICAL":0
    }

def readCVEList(bin, version):

    fileName = "".join([_BD, bin, "_" , version, ".cve"])
    if exists(fileName):
        f = open(fileName)
        data = json.load(f)
       
        for cve in data['vulnerabilities']:
            #print(json.dumps(cve['cve']['id'], indent=1))
            print(cve['cve']['metrics']['cvssMetricV31'][0]['cvssData'])
            severity=""
            if 'cvssMetricV31' in cve['cve']['metrics']:
                severity=cve['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseSeverity']

            elif 'cvssMetricV3' in cve['cve']['metrics']:
                severity=cve['cve']['metrics']['cvssMetricV3'][0]['cvssData']['baseSeverity']

            else:
                severity=cve['cve']['metrics']['cvssMetricV2'][0]['cvssData']['baseSeverity']

            vulns[severity]+=1
            print(cve['cve']['id'] + " " + severity)
        
        return vulns
    else:
        return False
    
def readServices(vendor, model, fileName):

    vulns["VENDOR"]=vendor
    vulns["MODEL"]=model


    f = open(fileName,"r")
    for binary in f:
        bin=binary.split(": ")[0]
        version=binary.split(": ")[1].strip()
        readCVEList(bin,version)
        
   
    f = open("teste.log", 'w')
    f.write(str(list(vulns.values())))

## vendor, model, versions.txt
readServices(sys.argv[1], sys.argv[2], sys.argv[3])