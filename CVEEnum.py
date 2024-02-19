from  urllib.request import urlopen, Request
import sys
import json

def downloadCVE (bin, version):
    print(bin +  " " + version)
    req = Request("https://services.nvd.nist.gov/rest/json/cpes/2.0?keywordSearch=" + bin + "%20" + version)
    req.add_header('apiKey','5dad0289-d91d-4ef9-8df0-bd2330031115')
    response = urlopen(req).read()

    data_json = json.loads(response)

    if data_json['resultsPerPage'] > 0:
        
        for i in range(data_json['resultsPerPage']):
            
            cpeName = data_json['products'][i]['cpe']['cpeName']
            
            if bin == cpeName.split(":")[4] and version in cpeName.split(":")[5] :
                print("-> cpeName found: " + cpeName)

                req = Request("https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=" + cpeName)
                req.add_header('apiKey','5dad0289-d91d-4ef9-8df0-bd2330031115')
                response = urlopen(req).read()
                
                cveList = json.loads(response)
                print(cveList)
    else:
        print(f"No results found for " +  bin + ":" + version)


downloadCVE(sys.argv[1],sys.argv[2])