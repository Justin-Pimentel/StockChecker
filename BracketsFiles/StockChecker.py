import webbrowser
import threading
import requests
import time
from bs4 import BeautifulSoup
from playsound import playsound
from datetime import datetime


#Function that takes in url and retrieves HTML content from the webpage
def get_html(url):
    #Function header tells the site that I'm a regular user and not a robot (¬_¬)
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"}
    #Use the requests library to grab HTML info from the specified URL
    page = requests.get(url, headers=headers)
    #print(page.status_code)
    return page.content


#Function that searches the content's HTML for inventory status
def check_inv_newegg(ne_url, refresh_time, stop):
    while True:
        
        if(stop()):
            print("Exiting Newegg thread...")
            break
        
        ne_html = get_html(ne_url)
        #Use BeautifulSoup's HTML parser to gather relevant content
        soup = BeautifulSoup(ne_html, 'html.parser')
        #Find the line that contains stock status
        oos_divs = soup.find("div", {"class": "product-inventory"})
        #print(oos_divs)
        #Return comparison to in stock text
        if(oos_divs.text == "In stock."):
            webbrowser.open_new(ne_url)
            print(str(datetime.now()) + "\t| ASUS TUF IN STOCK")
            playsound('Alarm1.wav')
        else:
            print(str(datetime.now()) + "\t| ASUS TUF out of stock")
    
        time.sleep(float(refresh_time))
        

def check_inv_bb(bb_url, refresh_time, stop):
    while True:
        
        if(stop()):
            print("Exiting BB thread...")
            break

        bb_html = get_html(bb_url)
        bb_html = bb_html.decode()
        search_result = bb_html.find('Sold Out</button>')
        #print(search_result)
        if(search_result == -1):
            webbrowser.open_new(bb_url)
            print(str(datetime.now()) + "\t| 3080FE IN STOCK")
            playsound('Alarm1.wav')
        else:
            print(str(datetime.now()) + "\t| 3080FE out of stock")
        
        time.sleep(float(refresh_time))

        
def main():
    #ne_url = input("Enter Newegg URL: ")
    #bb_url = input("Enter BestBuy URL: ")
    ne_url = 'https://www.newegg.com/asus-geforce-rtx-3080-tuf-rtx3080-o10g-gaming/p/N82E16814126452?Description=rtx3080&cm_re=rtx3080-_-14-126-452-_-Product'
    bb_url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440'
    
    ne_refresh_time = input("Newegg refresh time: ")
    bb_refresh_time = input("Best Buy refresh time: ")
    attempts = 0
    stop_threads = False
    
    #Create threads with appropriate functions.
    #Argument list = (website url, desired refresh time, lambda stop function)
    ne_checker = threading.Thread(target=check_inv_newegg, args=(ne_url, ne_refresh_time, lambda : stop_threads))
    bb_checker = threading.Thread(target=check_inv_bb, args=(bb_url, bb_refresh_time, lambda : stop_threads))
    
    #Spin up threads
    ne_checker.start()
    bb_checker.start()
    
    #Constantly poll for user input
    while True:
        stopper = input("Press 'x' to terminate: \n")
        if(stopper == 'x' or stopper == 'X'):
            stop_threads = True
            ne_checker.join()
            bb_checker.join()
            break
    
    print("Exiting main.")
    print("Lol")

#Run the program and get dat GPU baby
main()