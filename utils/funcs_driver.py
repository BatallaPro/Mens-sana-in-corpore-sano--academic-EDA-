import time

import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


# Building the driver
def launch_driver():
    srv = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=srv)
    driver.maximize_window()
    
    return driver

# Access to the database
def goto(driver, url):
    # Access website
    driver.get(url)

    # Access database
    driver.find_element(By.ID, 'navigation').find_element(By.LINK_TEXT, 'Consulta').click()
    time.sleep(5)

    # Show items alphabetically ordered
    driver.find_element(By.ID, 'Alfabetica').click()
    time.sleep(5)

    # Access all items
    driver.find_element(By.LINK_TEXT, 'Todos').click()
    
    return None

# Generating an iterator with every food found
def foodindex(driver):
    # The table is made of row-a and row-b classes
    # Create a list for each class elements
    get_row_a = driver.find_elements(By.CLASS_NAME, 'row-a')
    get_row_b = driver.find_elements(By.CLASS_NAME, 'row-b')

    # Let's merge both lists into foodindex
    # The for looping form will be:
    #
    # foodindex = []
    # for tupl in zip(get_row_a, get_row_b):
    #     for i in tupl:
    #         foodindex.append(i)
    #
    # But this can be done with a little tricky list comprehension
    foodindex = [i for tupl in zip(get_row_a, get_row_b) for i in tupl]

    return foodindex

# To access a single element page
def get_in(food):
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
    
    food.find_element(By.ID, 'foodname').find_element(By.TAG_NAME, 'a').click()
    time.sleep(5)
    
    return None

# To get back to the all-food list
def get_back(driver):
    driver = driver.find_element(By.ID, 'content2')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Todos')))

    back = driver.find_element(By.CSS_SELECTOR, 'p').find_element(By.ID, 'Todos')
    back.click()
        
    return None