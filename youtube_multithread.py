import time
import random
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


MAX_THREADS = 2
proxyList = set()
userAgent = set()
sleep_time = 0
PROXY = ""

## To get random proxies from the free proxy websites http://free-proxy-list.net, http://free-proxy-list.net, https://www.sslproxies.org
#req_proxy = RequestProxy()
#proxies = req_proxy.get_proxy_list()
#proxyList = { proxies[p].get_address() for p in range(len(proxies))}

## Country specific proxies collection
# proxyList = { proxies[p].get_address() for p in range(len(proxies)) if proxies[p].country == "India"}

## With static known proxies , if you know the proxies then create this file with name proxy_list.txt
with open('proxy_list.txt', 'r') as file:
    proxyList = { s for s in file.read().split('"\n"') }

with open(r'user_agents.txt', 'r') as file:
    userAgent = { s for s in file.read().split('"\n"') }


videos = [
'https://www.youtube.com/watch?v=m-6V9B3mTKs',
'https://www.youtube.com/watch?v=7UDGuq7pTDU'
] * 4

def firefoxUrl(PROXY):
    webdriver.DesiredCapabilities.FIREFOX['proxy']={
        "httpProxy":PROXY,
     #   "ftpProxy":PROXY,
        "sslProxy":PROXY,
        "proxyType":"MANUAL",
    }
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", random.choice(tuple(userAgent)))
    brdriver = webdriver.Firefox(options = options, executable_path= r"C:\Users\klal\Downloads\Kubernetes_in_action\geckodriver-v0.29.1-win64\geckodriver.exe")
    brdriver.maximize_window()
    return brdriver

def chromeUrl(PROXY):
    webdriver.DesiredCapabilities.CHROME['proxy']={
        "httpProxy":PROXY,
      #  "ftpProxy":PROXY,
        "sslProxy":PROXY,
    
        "proxyType":"MANUAL",
    }
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    brdriver = webdriver.Chrome(options=options, executable_path= r"C:\Users\klal\Downloads\Kubernetes_in_action\chromedriver_win32\chromedriver.exe")
    brdriver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    brdriver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(tuple(userAgent))})
    print(brdriver.execute_script("return navigator.userAgent;"))
    return brdriver

def youtubeThread(videos):

    PROXY = random.choice(tuple(proxyList))

    if random.randint(0,1) == 1:
        driver = chromeUrl(PROXY)
    else:
        driver = firefoxUrl(PROXY)

    #print("Watching for {} time".format(i))
    random_video = random.randint(0,len(videos)-1)
    try: 
        # driver.set_page_load_timeout(random.randint(60,120))
        driver.get(videos[random_video])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Play']"))).click()
        #with open('proxy_list.txt', 'a+') as file:
        #    file.write(PROXY+"\n")
    except:
        driver.quit()
        proxyList.remove(PROXY)
        print("Not working Proxy, DELETED " + PROXY + ", Length of proxyList "+ str(len(proxyList)))

    sleep_time = random.randint(30, 60)
    time.sleep(sleep_time) # Let the user actually see something!
    driver.quit()


def main(videos):
    threads = min(MAX_THREADS, len(videos))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(youtubeThread, videos)


if __name__ == '__main__':
    main(videos)