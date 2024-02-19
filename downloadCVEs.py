from  urllib.request import urlopen, Request
from  urllib.parse import quote
from os.path import exists
import json
import sys
import time


_BD = "/home/osmany/Dropbox/ITA/SBRC23/bd/"

def getCVE(bin, version):
    fileName = "".join([_BD, bin, "_" , version, ".cve"])
    if exists(fileName):
        print("Local file found for " + bin + ":" + version)
        return fileName
    else:
        print("Local file not found for " + bin + ":" + version)
        return downloadCVE(bin,version)

def downloadCVE (bin, version):
    req = Request("https://services.nvd.nist.gov/rest/json/cpes/2.0?keywordSearch=" + bin + "%20" + version)
    req.add_header('apiKey','5dad0289-d91d-4ef9-8df0-bd2330031115')
    response = urlopen(req).read()

    data_json = json.loads(response)

    if data_json['resultsPerPage'] > 0:
        
        for i in range(data_json['resultsPerPage']):
            
            cpeName = data_json['products'][i]['cpe']['cpeName']
            #print(cpeName)

            if bin == cpeName.split(":")[4] and version in cpeName.split(":")[5] :
                print("-> cpeName found: " + cpeName)

                req = Request("https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=" + cpeName)
                req.add_header('apiKey','5dad0289-d91d-4ef9-8df0-bd2330031115')
                response = urlopen(req).read()
                
                cveList = json.loads(response)
                fileName = "".join([_BD,bin, "_" , version, ".cve"])
                f = open(fileName, 'w')
                f.write(json.dumps(cveList))
                return fileName
    else:
        print(f"No results found for " +  bin + ":" + version)

def readServices(fileName):
    f = open(fileName,"r")
    for binary in f:
        bin=binary.split(": ")[0]
        version=binary.split(": ")[1].strip()
        #print("Processing " + bin + ":" + version)
        cveFile = downloadCVE(bin, version)
        time.sleep(2)
       
## versions.txt
readServices(sys.argv[1])