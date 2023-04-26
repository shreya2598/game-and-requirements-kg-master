import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def generate_url():
    start_urls = ['https://www.techpowerup.com/cpu-specs/?mfgr=Intel&released=2010&sort=name']
    for it in range(2010, 1999, -1):
        start_urls.append('https://www.techpowerup.com/cpu-specs/?mfgr=Intel&released={}&sort=name'.format(it))

    return start_urls

def get_data(start_urls):
    name = []
    codename = []
    cores = []
    clock = []
    socket = []
    process = []
    l3_cache = []
    tdp = []
    released = []
    for url in start_urls:

        page = requests.get(url)
        print(page)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content,'html.parser')
            obj = soup.find_all('td')
            for i in range(0,len(obj),9):
                name.append(obj[i].find('a').get_text())
                codename.append(obj[i+1].get_text())
                cores.append(obj[i+2].get_text())
                clock.append(obj[i+3].get_text())
                socket.append(obj[i+4].get_text())
                process.append(obj[i+5].get_text())
                l3_cache.append(obj[i+6].get_text())
                tdp.append(obj[i+7].get_text())
                released.append(obj[i+8].get_text())
            time.sleep(1)

    amd_df = pd.DataFrame({"Name":name,"Codename":codename,"Cores":cores,"Clock":clock,"Socket":socket,
                           "Process":process,"L3 Cache":l3_cache,"TDP":tdp,"Released":released})
    amd_df.to_csv('intel_cpu_specs1.csv',index = False)

if __name__ == "__main__":
    start_url = generate_url()
    get_data(start_url)