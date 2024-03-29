import webbrowser
import threading
import requests
import time
import sys
import os
from bs4 import BeautifulSoup
from playsound import playsound
from datetime import datetime
from random import randrange

exit_flag = threading.Event()

def get_sleep_time(num):
    #randrange only takes in ints so I typecast it in case it's a float
    n = int(num)
    lower_limit = n
    upper_limit = n + int((num/rand_denominator))
    
    return randrange(lower_limit, upper_limit)

def get_name_bb(url):
    bb_html = get_html(url)
    bb_html = bb_html.decode()
    start_index = bb_html.find('<h1 class="heading-5 v-fw-regular">') + len('<h1 class="heading-5 v-fw-regular">')
    end_index = bb_html.find('</h1>')
    name = bb_html[start_index:end_index]

    return name
    
def handle_exception(e, code):
    retry_time = 30

    print(str(e))
    print("Error code: " + str(code) + ". Retrying...")
    time.sleep(retry_time)

#Function that takes in url and retrieves HTML content from the webpage
def get_html(url):
    #Function header tells the site that I'm a regular user and not a robot (¬_¬)
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"}

    max_retries = 4
    retry = 0
    #Use the requests library to grab HTML info from the specified URL
    while True:
        try:
            page = requests.get(url, headers=headers)
            page.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            handle_exception(e, page.status_code)
        except requests.exceptions.Timeout as e:
            handle_exception(e, page.status_code)
        except requests.exceptions.RequestException as e:
            handle_exception(e, page.status_code)

        if(page.ok or retry == max_retries-1):
            break

        retry += 1

    if(not page.ok):
        return False
 
    return page.content


#Function that searches the content's HTML for inventory status
def check_inv_newegg(ne_url, stop, name):
    while True:
        
        if(stop()):
            print("Exiting Newegg thread")
            break
        
        ne_html = get_html(ne_url)
        if(not ne_html):
            print("Aborting thread")
            break

        #print(ne_html)
        #Use BeautifulSoup's HTML parser to gather relevant content
        soup = BeautifulSoup(ne_html, 'html.parser')
        #Find the line that contains stock status
        oos_divs = soup.find("div", {"class": "product-inventory"})
        #print(oos_divs)
        newegg_name = soup.find("h1", {"class": "product-title"})
        #print(newegg_name.text)
        #print("Name: " + newegg_name.find("a").text)
        #Return comparison to known in stock text
        if(oos_divs.text == "In stock."):
            webbrowser.open_new(ne_url)
            print(name + "\t" + str(datetime.now()) + "\t" + newegg_name.text + "\tIN STOCK!!!")
            playsound(os.path.join(sys.path[0], "Alarm.wav"))
            exit_flag.wait(int(success_wait_time))
        else:
            print(name + "\t" + str(datetime.now()) + "\t" + newegg_name.text + "\tOUT OF STOCK")
    
        rand_time = get_sleep_time(float(ne_refresh_time))
        time.sleep(float(rand_time))
        

def check_inv_bb(bb_url, stop, name):
    #Get product name
    name = get_name_bb(bb_url)

    #Enter main thread execution loop
    while True:
        
        if(stop()):
            print("Exiting BB thread")
            break

        #Search for "Sold Out" button presence. If not there then it's in stock
        bb_html = get_html(bb_url)

        if(not bb_html):
            print("Aborting thread")
            break

        bb_html = bb_html.decode()
        search_result = bb_html.find('Sold Out</button>')

        #Handle result of html scrape
        if(search_result == -1):
            webbrowser.open_new(bb_url)
            print(name + "\t" + str(datetime.now()) + "\t" + name + "\tIN STOCK!!!")
            playsound(os.path.join(sys.path[0], "Alarm.wav"))
            exit_flag.wait(int(success_wait_time))
        else:
            print(name + "\t" + str(datetime.now()) + "\t" + name + "\tOUT OF STOCK")
        
        #Sleep for the allotted amount of time
        time.sleep(float(bb_refresh_time))

        
def main():
    #Get user input data
    global ne_refresh_time
    global bb_refresh_time
    global success_wait_time
    global rand_denominator
    global MAX_THREADS
    stop_threads = False
    NUM_SETTINGS = 5
    settings = [None] * NUM_SETTINGS

    #Gather data from settings.txt
    print("Opening file...")
    with open(os.path.join(sys.path[0], "settings.txt"), "r") as e:
        print("File '" + os.path.basename(e.name) + "' opened successfully...")
   
        for num, line in enumerate(e):
            setting = [x.strip() for x in line.split(":")]
            settings[num] = setting[1]
    
    #Assign global vars
    ne_refresh_time = settings[0]
    bb_refresh_time = settings[1]
    success_wait_time = settings[2]
    rand_denominator = settings[3]
    MAX_THREADS = settings[4]
    threads = [None] * int(MAX_THREADS)

    #Open file and begin reading lines and creating threads
    print("Opening file...")
    with open(os.path.join(sys.path[0], "links.txt"), "r") as f:
        print("File '" + os.path.basename(f.name) + "' opened successfully...")
        ne_th_cnt = 0
        bb_th_cnt = 0
        
        for count, line in enumerate(f):
            if(count == MAX_THREADS):
                break

            #print("Line {}: {}".format(count+1, line.strip()))
            if(line.find('newegg') != -1):
                ne_url = line.strip()
                name = "thread" + str(count)
                threads[count] = threading.Thread(target=check_inv_newegg, args=(ne_url, lambda : stop_threads, name))
                ne_th_cnt += 1
            elif(line.find('bestbuy') != -1):
                bb_url = line.strip()
                name = "thread" + str(count)
                threads[count] = threading.Thread(target=check_inv_bb, args=(bb_url, lambda : stop_threads, name))
                bb_th_cnt += 1
            else:
                print("Invalid link entered")

        print(str(count+1) + " links processed. " + str(ne_th_cnt + bb_th_cnt) + " threads created.")
        print("Newegg threads: " + str(ne_th_cnt) + ". Best Buy threads: " + str(bb_th_cnt))

    #Spin up threads
    print("Spooling up threads...\n")
    for thread in threads:
        if thread is not None:
            thread.start()
    
    #Constantly poll for user input
    #TODO: Finish termination of individual threads
    while True:
        stopper = input("Enter 'x' to terminate: \n")
        term_list = stopper.split()
        if(term_list[0] == 'x' or term_list[0] == 'X'):
            print("Terminating threads...")
            stop_threads = True
            exit_flag.set()
            for thread in threads:
                if thread is not None:
                    thread.join()
            break
    
    print("Exiting main.")

#Run the program and get dat GPU baby
if __name__ == '__main__':
    main()