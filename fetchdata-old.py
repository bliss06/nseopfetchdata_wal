import pycurl
from io import BytesIO
import json
import time
import os
import gzip
import shutil
import zlib

# while True:
buffer = BytesIO()
c = pycurl.Curl()

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

    # Break the header line into header name and value.
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



#Header Options
header = ['Host: www.nseindia.com',
'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# 'Accept: text/html,application/xhtml+xml,application/xml',
'Accept-Language: en-US,en;q=0.5',
'Accept-Encoding: gzip, deflate, br',
'Connection: keep-alive',
'Referer: https://www.nseindia.com/option-chain',
'Cookie: _ga=GA1.2.460585163.1622459671; RT="z=1&dm=nseindia.com&si=2bed572d-957c-44e6-9be8-9a4a5d16ed0c&ss=kqtadgct&sl=0&tt=0&bcn=%2F%2F684fc53f.akstat.io%2F&nu=ed8553192c8d124be55949cc1b2e99dc&cl=5rx2z"; _gid=GA1.2.1244730889.1625467278; ak_bmsc=27A67EF3D20B88A432B5594F87CEC249~000000000000000000000000000000~YAAQN0YDF5eX0et5AQAAjNrbhAx5rVf4G3faG+kg43L23z/P6jxSGKpNxy7HUh93G5kaAKAMUVbIdfRIKHUwtkzp9Ol5hsw5gjTnk+imKJADYhD+sqYf7s5kij7KMlIQF6FiDsi1RxYp2P6Elbx/AndndOy4sEhb8BLNmkvwwEPL5dppwVhk4VBn9dVD5MsjgSFa5KhZAMOxvQFYiN+DjYp7AzGqAapbx7JqJHheeTrX7luuvrj1YY3OfZCX5Ro9er7BD6lCj13jkfaxk6A7fxw+Aq2xvAKh6TwU/SApwLiSFXLtvqKJSdqdn8fU1v+PSKwJrrik8oEU4CmRXnprC8UgKaxsRby9gmmsq9c1Ug5eGHPR3fKsfWojAn7zSYDf6wl2mL0Qx4CU586jpAk=',
'TE: Trailers']


c.setopt(c.URL, 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY')
# c.setopt(c.URL, 'https://www.nseindia.com/option-chain')
# c.setopt(c.REFERER, 'https://www.nseindia.com/option-chain')
# c.setopt(c.USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0')
# c.setopt(c.ACCEPT_ENCODING, 'gzip, deflate, br')
# # c.setopt(c.ACCEPT, '*/*')
# c.setopt(c.ACCEPT_LANGUAGE, 'en-US,en;q=0.5')
# c.setopt(c.COOKIE, '_ga=GA1.2.460585163.1622459671; RT="z=1&dm=nseindia.com&si=2bed572d-957c-44e6-9be8-9a4a5d16ed0c&ss=kqqdsn2i&sl=0&tt=0&bcn=%2F%2F684fc53e.akstat.io%2F&nu=ed8553192c8d124be55949cc1b2e99dc&cl=agine"; _gid=GA1.2.1244730889.1625467278; ak_bmsc=C6AA1CB4BB9627E234A917738C7FC075~000000000000000000000000000000~YAAQN0YDF26lx+t5AQAAEunmdgzdPS1XAYNQI+Ve1pHLsZ1YcTKlSgFWNuhLpoHjZF/hXtxoQrvAX//e4cK2bDBF0i+UcbTvWi+om8w/HdAhjQt7vZuXmOxKa6LZOQHQLe1t8nZ8PsWo+X8SKGtTNHsTqZX/dBbCRBvXZYnnxuQjKMGVTGeiVY7uyx52N1YnVWT8p1vHQeVXr5poEmP0U6yNAXOMex+BKm4neML8j4jVm3JDrb7hDd/wQlx28aprfzz9qLhnKNjJVZLJwIM5aWogiJ4fTOHXTNOzPEBsJrUw5RvWNCD4/8gVRVH/joterO6NJnGjXjsBVZbPGNHKcZpllJ/A60vqDEDPWlpQQTNsVVMUfFayMm+ppQwpIhfVWzr0tSXpGgS1F5YPT4M=')
#c.setopt(c.VERBOSE, True)
#c.setopt(c.HOST, '*/*')
c.setopt(c.HTTPHEADER, header)
c.setopt(c.WRITEDATA, buffer)

# Set our header function.
c.setopt(c.HEADERFUNCTION, header_function)

c.perform()
c.close()

print(headers)
# print(buffer.getvalue())
# body = gzip.decompress(buffer.read())
print(buffer.getvalue())



# body_text = body.decode('iso-8859-1')
# print(body_text)


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
    
option_chain_file = open(filename, "bw")
# option_chain_file.write(body.decode('iso-8859-1'))
option_chain_file.write(body)
option_chain_file.close()

print('File created')
# time.sleep(200)
