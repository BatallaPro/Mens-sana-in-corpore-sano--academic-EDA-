import time

import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

      
# To get general info from a food page
def get_general_info(driver, item):
    driver = driver.find_element(By.ID, 'content2')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h4')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'span')))
    
    h4 =   driver.find_elements(By.CSS_SELECTOR, 'h4')
    p =    driver.find_elements(By.CSS_SELECTOR, 'p')
    span = driver.find_elements(By.TAG_NAME, 'span')

    item_foodname_ESP = h4[0].text
    item_foodname_ENG = p[2].text[14:]
    item_quantity =     h4[2].text[32:][:-25]

    general_info = [item_foodname_ESP, item_foodname_ENG, item_quantity]

    for i in general_info:
        try:
            item.append(i)
        except:
            item.append(np.nan)
            
    return item

# To get nutritional facts from a food page
def get_nutritional_facts(driver, item):
    driver = driver.find_element(By.ID, 'content2')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
    
    table = driver.find_elements(By.TAG_NAME, 'table')
    nutritional_facts = table[2].text.splitlines()
    
    relevant_facts_index = {'energy': 3, 'fats': 4, 'prot': 5, 'water': 6,
                            'fiber': 8, 'carbs': 9, 'm_unsat_fats': 12,
                            'p_unsat_fats': 13, 'sat_fats': 14, 'palm_acid': 17,
                            'chol': 20, 'A': 26, 'D': 27, 'E': 28, 'B9': 29,
                            'B3': 30, 'B2': 31, 'B1': 32, 'B12': 33, 'B6': 34,
                            'C': 35, 'calcium': 37, 'iron': 38, 'potassium': 39,
                            'magnesium': 40, 'sodium': 41, 'phosphorus': 42,
                            'iodide': 43, 'selenium': 44, 'zinc': 45}
    
    for index in relevant_facts_index.values():
        try:
            item.append(float(nutritional_facts[index].split()[-3]))
        except:
            item.append(np.nan)
    
    return item

# Some values will rise an axception from get_nutritional_facts(driver, item)
# and are added as NaN, but in some cases this is just because they
# need furher transformation. If a error raises then are imported as NaN.
def refine_nutritional_facts(driver,item):
    driver = driver.find_element(By.ID, 'content2')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
    
    table = driver.find_elements(By.TAG_NAME, 'table')
    nutritional_facts = table[2].text.splitlines()
    
    # energy
    # list(relevant_facts_index.keys()).index('energy') + len(general_info) ---> 3
    try:
        item[3] = float(nutritional_facts[3].split(' ')[3][1:-1])
    except:
        pass

    # palm_acid
    # list(relevant_facts_index.keys()).index('palm_acid') + len(general_info) ---> 12
    try:
        palm_acid = nutritional_facts[17].split()[-3]
        if palm_acid == '-':
            item[12] = False
        else:
            item[12] = True
    except:
        pass
        
    return item

# To get all foods that belong to a certain group
def get_group_info(driver, group):
    get_row_a = driver.find_elements(By.CLASS_NAME, 'row-a')
    get_row_b = driver.find_elements(By.CLASS_NAME, 'row-b')

    foods = [i for tupl in zip(get_row_a, get_row_b) for i in tupl]

    for i in range(len(foods)):
        group.append(foods[i].find_element(By.ID, 'foodname').text)
        
    return group