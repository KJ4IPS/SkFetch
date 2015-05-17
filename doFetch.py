import os.path
import json
import urllib2


def main():
    #First, we need the definition file
    if not os.path.isfile("fetch.json"):
        print("ERROR: fetch.json not found")
        exit
        
    fetchfile = open("fetch.json","r")
    try:
        fetchjson=json.load(fetchfile)
    except Exception  as e:
        print("Error: Unable to load json:")
        raise e
        exit

    if not "items" in fetchjson:
        print("ERROR: no 'items' in fetch.json")
        exit

    for item in fetchjson["items"]:
        itemKeys = item.keys()
        if not "method" in itemKeys:
            print("ERROR: Item does not have method")
            print(json.dumps(item))
            exit
        if not item["method"] in fetch_methods:
            print("ERROR: No fetch routine for method {}".format(item["method"]))
            exit
        fetch_methods[item["method"]](item)
    

def http_fetcher(obj):
    if "filename" in obj:
        basename = obj["filename"]
    else:
        basename = obj["location"].rsplit('/',1)[1]
    destpath = os.path.join(obj["destination"].replace('/',os.path.sep),basename)
    http_download(obj["location"],destpath)

def http_download(src,dest):
    if os.path.isfile(dest):
        print(dest + " Already here, skipping");
    else:
        try:
            os.makedirs(dest.rsplit(os.path.sep,1)[0])
        except OSError as e:
            pass
        destfile = open(dest,"wb")
        srcfile = urllib2.urlopen(src)
        print("Downloading " + dest)
        while True:
            dlbuffer = srcfile.read(8192)
            if not dlbuffer:
                break
            destfile.write(dlbuffer)

    
    
    
        

fetch_methods = {"http": http_fetcher}

main()
