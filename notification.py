from bluepy import btle
from bluepy.btle import BTLEDisconnectError
import time
import requests

# defining the api-endpoint 
API_ENDPOINT = "http://pc.lightsoftsolutions.com/api/records"
API_KEY = "XXXXXXXXXXXXXXXXX"

# defining weight scale info
FUEL_TYPE = 1
MAC_ADDR = "5c:ca:d3:0d:c6:77"
BODY_INFO_UUID = "00002a9c-0000-1000-8000-00805f9b34fb"

def sendToDB(weight):
    data = {'api_dev_key':API_KEY,
            'fuel_type': FUEL_TYPE,
            'measurement': weight
            }
    
    r = requests.post(url = API_ENDPOINT, data = data)
    response = r.text
    print(response)

def waitForConnection():
    
    while True:
        
        try:
            print("Attesa connessione...")
            p = btle.Peripheral(MAC_ADDR)
            getWeight(p)
            break
        
        except BTLEDisconnectError:
            print("Bilancia non trovata. Ritento connessione...")
    
def getWeight(p):
    finalWeight = None
    
    while True:
        
        try:
                
            bodyChar = p.getCharacteristics(1, 0xFFFF, BODY_INFO_UUID)[0]
            
            value = bodyChar.read()
            splitted = str(value).split("\\x")
            weight = splitted[13] + splitted[12]
            finalWeight = 0.01 * int(weight, 16)
            print("Hex: " + weight)
            print("Peso rilevato: " + str(finalWeight))

            time.sleep(0.5)
            
        except BTLEDisconnectError:
            print("Bilancia disconnessa.")
            break
        
    sendToDB(finalWeight)   
    waitForConnection()


#start application
waitForConnection()




