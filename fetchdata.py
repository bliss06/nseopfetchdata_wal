import pycurl
from io import BytesIO
import json
import time
import os
import gzip
import shutil

# while True:


headers = {}
def header_function(header_line):
    # HTTP standard specifies that headers are encoded in iso-8859-1.
    # On Python 2, decoding step can be skipped.
    # On Python 3, decoding step is required.
    header_line = header_line.decode('iso-8859-1')

    # Header lines include the first status line (HTTP/1.x ...).
    # We are going to ignore all lines that don't have a colon in them.
    # This will botch headers that are split on multiple lines...
    if ':' not in header_line:
        return

    # Break the header line into header name and va6666666666666666666666666lue.
    name, value = header_line.split(':', 1)

    # Remove whitespace that may be present.
    # Header lines include the trailing newline, and there may be whitespace
    # around the colon.
    name = name.strip()
    value = value.strip()

    # Header names are case insensitive.
    # Lowercase name here.
    name = name.lower()

    # Now we can actually record the header name and value.
    # Note: this only works when headers are not duplicated, see below.
    headers[name] = value


while True:
    #Header Options

    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY')
    c.setopt(c.REFERER, 'https://www.nseindia.com/option-chain')
    c.setopt(c.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/82.0')
    c.setopt(c.ACCEPT_ENCODING, 'gzip, deflate, br')

    c.setopt(c.WRITEDATA, buffer)

    # Set our header function.
    c.setopt(c.HEADERFUNCTION, header_function)


    c.perform()
    c.close()

    print(headers)

    body = buffer.getvalue()
    body_text = body.decode('iso-8859-1')

    #print(body_text)
    # if  body_text.find("expiryDates") == -1:
    #     continue
    # Body is a byte string.
    # We have to know the encoding in order to print it to a text file
    # such as standard output.
    filename = "BNF_OC_MAIN.txt"
    filename1 = "BNF_OC_" + time.strftime("%d%m%Y%H%M%S")+".txt"

    #if the file exists then rename it
    try:
        os.rename(filename,filename1)
    except OSError as error:
        print(error)
        
    option_chain_file = open(filename, "w")
    option_chain_file.write(body_text)
    option_chain_file.close()

    print('File created')
    time.sleep(300)
