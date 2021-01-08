from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random


DICTIONARY = [x.strip() for x in open("words.txt", "r").readlines()]

PSEUDO_BASE_URL = "https://pseudo.skandbrand.com/"

driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get(PSEUDO_BASE_URL)

IN_GAME = False

prompt = ""
used_letters = [] # can make these sets
used_words = []

def count_new(w):
    rtn = 0
    for c in w:
        if(c not in used_letters):
            rtn += 1
    return rtn

def slow_type(tf, w):
    for c in w:
        tf.send_keys(c)
        time.sleep(random.random()/8)


while True:
    try:
        IN_GAME = ("play" in driver.current_url)

        if(IN_GAME):
            text_input = driver.find_elements_by_xpath("/html/body/div[1]/main/div[1]/div[2]/input")
            if(len(text_input) == 0 or not text_input[0].is_displayed()):
                print("No input field found.")
                continue

            prompt_element = driver.find_elements_by_xpath("/html/body/div[1]/main/div[1]/div[1]/div[4]/span")
            if(len(prompt_element) == 0):
                print("No prompt field found.")
                continue

            prompt = prompt_element[0].get_attribute("innerText")
            valid = []
            for wd in DICTIONARY:
                if(prompt.lower() in wd.lower() and len(wd) < 15 and wd not in used_words):
                    valid.append(wd)

            if(len(valid) == 0):
                print("No valid answers found!!")
                continue


            time.sleep(random.random() * 2)
            while prompt == prompt_element[0].get_attribute("innerText"):
                time.sleep(random.random())
                bc, answer = -1, ""

                for w in valid:
                    cn = count_new(w)
                    if(cn > bc or (cn == bc and len(w) < len(answer))):
                        answer = w
                        bc = count_new(w)

                for c in answer:
                    if(c not in used_letters):
                        used_letters.append(c)

                if(len(used_letters) == 26):
                    used_letters = []

                print("Attempting answer:\t" + answer)
                    
                slow_type(text_input[0], answer)
                time.sleep(0.2)
                text_input[0].send_keys(Keys.ENTER)
                time.sleep(0.2)

                valid.remove(answer)
                used_words.append(answer)
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
        pass

