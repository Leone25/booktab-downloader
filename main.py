import sys  
import requests
import base64
from xml.dom.minidom import parseString
from io import BytesIO, SEEK_SET, SEEK_END 
import PyPDF2

# Create a class which convert PDF in BytesIO form 
# TBH I stole this one from somewhere and I have no idea how it works
class ResponseStream(object): 
      
    def __init__(self, request_iterator): 
        self._bytes = BytesIO() 
        self._iterator = request_iterator 
   
    def _load_all(self): 
        self._bytes.seek(0, SEEK_END) 
          
        for chunk in self._iterator: 
            self._bytes.write(chunk) 
   
    def _load_until(self, goal_position): 
        current_position = self._bytes.seek(0, SEEK_END) 
          
        while current_position < goal_position: 
            try: 
                current_position = self._bytes.write(next(self._iterator)) 
                  
            except StopIteration: 
                break
   
    def tell(self): 
        return self._bytes.tell() 
   
    def read(self, size = None): 
        left_off_at = self._bytes.tell() 
          
        if size is None: 
            self._load_all() 
        else: 
            goal_position = left_off_at + size 
            self._load_until(goal_position) 
   
        self._bytes.seek(left_off_at) 
          
        return self._bytes.read(size) 
   
    def seek(self, position, whence = SEEK_SET): 
          
        if whence == SEEK_END: 
            self._load_all() 
        else: 
            self._bytes.seek(position, whence) 


cookie = input("Paste the shibsession cookie: ")

isbn = input("Input the ISBN of the book you want to download: ")

print("Gethering information about the volume...")

spine = requests.get('http://web.booktab.it/boooks_web/'+isbn+'/spine.xml', allow_redirects=False, headers={'Cookie':'_shibsession_626f6f6b746162776562687474703a2f2f7765622e626f6f6b7461622e69742f73686962626f6c657468='+cookie})

pdfsToMerge = []

if spine.status_code == 302:
    print("Invalid shibsession cookie, please try again.")
    sys.exit() 
elif spine.status_code != 200:

    spine = requests.get('http://web.booktab.it/boooks_web/'+isbn+'/volume.xml', allow_redirects=False, headers={'Cookie':'_shibsession_626f6f6b746162776562687474703a2f2f7765622e626f6f6b7461622e69742f73686962626f6c657468='+cookie})
    if spine.status_code == 302:
        print("Invalid shibsession cookie, please try again.")
        sys.exit() 
    elif spine.status_code != 200:
        print("Invalid ISBN, please try again.")
        sys.exit()

print("Extracting chapters...")

spine = parseString(spine.text)

parts = spine.getElementsByTagName("unit")

merger = PyPDF2.PdfFileMerger()

print("Downloading all parts...")

for part in parts:

    partInfo = requests.get('http://web.booktab.it/boooks_web/'+isbn+'/'+part.getAttribute("btbid")+'/config.xml', headers={'Cookie':'_shibsession_626f6f6b746162776562687474703a2f2f7765622e626f6f6b7461622e69742f73686962626f6c657468='+cookie})

    if partInfo.status_code != 200:
        continue

    partXML = parseString(partInfo.text)

    key = partXML.getElementsByTagName("content")[0].firstChild.nodeValue

    pdfUrl = ''
    
    for entry in partXML.getElementsByTagName("entry"):
        if entry.getAttribute("key") == key+".pdf":
            pdfUrl = entry.firstChild.nodeValue+".pdf"
            break

    pdf = requests.get('http://web.booktab.it/boooks_web/'+isbn+'/'+part.getAttribute("btbid")+'/'+pdfUrl, headers={'Cookie':'_shibsession_626f6f6b746162776562687474703a2f2f7765622e626f6f6b7461622e69742f73686962626f6c657468='+cookie})
    
    merger.append(PyPDF2.PdfFileReader(ResponseStream(pdf.iter_content(64))))


merger.write(input("Input a title for the file: ") + ".pdf")
