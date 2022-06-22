# Imports

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from ipyleaflet import Map, Marker, MarkerCluster

from matplotlib import pyplot as plt
import matplotlib

from pymongo import MongoClient
import numpy as np
import pandas as pd
import time as tm
import re
import unittest
from tqdm import tqdm

import sys
import timeit

import csv

##################################################################

PATH = "/Users/suntim/Documents/Programming/Machine Learning/NYC Crime/chromedriver"

#option = webdriver.ChromeOptions()
#option.add_argument('headless')

driver = webdriver.Chrome(PATH)

driver.get("https://compstat.nypdonline.org/")
driver.maximize_window()

wait = WebDriverWait(driver, 20)
def wait_for_element(locator_type:str,locator:str):
    return wait.until(EC.presence_of_element_located((eval(locator_type), locator)))

try:

    search_weekly_total_crime_number = wait_for_element("By.XPATH", '//*[@id="report-win1"]/div[3]/div[2]/div/div/div[3]/div[1]/table/tbody/tr[9]/td[1]/div/div')
    #search_weekly_total_crime_number.click()

    search_anual_total_crime_number = wait_for_element("By.XPATH", '//*[@id="report-win1"]/div[3]/div[2]/div/div/div[3]/div[1]/table/tbody/tr[9]/td[7]/div/div')
    search_anual_total_crime_number.click()

    #wait_for_cicles_to_appear = wait_for_element("By.CSS_SELECTOR", '#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map > div.km-widget.km-scroll-wrapper > div.km-scroll-container > div:nth-child(4) > svg > circle:nth-child(2)')
    #print(wait_for_cicles_to_appear.get_attribute("innerHTML"))
    #wait_for_cicles_to_appear.click()

    wait_for_cicles_to_appear = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map > div.km-widget.km-scroll-wrapper > div.km-scroll-container > div:nth-child(4) > svg > circle:nth-child(2)'))
    )

    first_circle = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map > div.km-widget.km-scroll-wrapper > div.km-scroll-container > div:nth-child(4) > svg'))
    )

    zoom_out = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map > div.k-map-controls.k-pos-top.k-pos-left > div > button.k-button.k-zoom-out'))
    )

    zoom_in = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map > div.k-map-controls.k-pos-top.k-pos-left > div > button.k-button.k-zoom-in'))
    )

    some_logo = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#report-win13 > div.window-header > h4'))
    )

    loading_disapear = wait.until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, '#report-win13 > div.k-loading-mask > div.k-loading-image'))
    )

    map_mover = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map > div.km-widget.km-scroll-wrapper > div.km-scroll-container'))
    )

    toggle_large_map = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="report-win13"]/div[2]/a/span'))
    )

    map_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map'))
    )

    def moveUp(scalar=10):
        webdriver.ActionChains(driver).move_to_element(map_element).click_and_hold().move_by_offset(0,1*scalar).release().perform()

    def moveDown(scalar=10):
        webdriver.ActionChains(driver).move_to_element(map_element).click_and_hold().move_by_offset(0,-1*scalar).release().perform()

    def moveLeft(scalar=10):
        webdriver.ActionChains(driver).move_to_element(map_element).click_and_hold().move_by_offset(1*scalar,0).release().perform()

    def moveRight(scalar=10):
        webdriver.ActionChains(driver).move_to_element(map_element).click_and_hold().move_by_offset(-1*scalar,0).release().perform()



    toggle_large_map.click()

    webdriver.ActionChains(driver).move_to_element(first_circle).click(first_circle).perform()

    for i in range(1):
        zoom_out.click()

    moveRight(70)

    map_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map'))
    )


    #print(driver.page_source.encode('utf-8'))

    circles = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map > div.km-widget.km-scroll-wrapper > div.km-scroll-container > div:nth-child(4) > svg > circle'))
    )

    print("number of circles: ", len(circles))


    data_frame = pd.DataFrame(columns=["x_cord","y_cord","time","crime","crime_category"])
    crime_counter = 0


    def make_all_disapear():
        circles = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map > div.km-widget.km-scroll-wrapper > div.km-scroll-container > div:nth-child(4) > svg > circle'))
        )

        driver.execute_script("var all_circles = document.getElementsByTagName('circle');\
                               for (i = 0; i < all_circles.length; i++){all_circles[i].style.visibility = 'hidden'};")

        some_logo.click()
        #webdriver.ActionChains(driver).move_to_element_with_offset(map_mover,1000,100).click(map_mover).perform()

    #print(coordinate_array)

    make_all_disapear()



    for i, circle in enumerate(circles):

        #webdriver.ActionChains(driver).move_to_element(circle).click(circle).perform()

        print("i: ", i)

        print("in bounds now index first declared: ", circle_order_fast_route[i])

        given_circle = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map > div.km-widget.km-scroll-wrapper > div.km-scroll-container > div:nth-child(4) > svg > circle:nth-child({i+2})'))
        )

        driver.execute_script(f"var all_circles = document.getElementsByTagName('circle');\
                                all_circles[{i}].style.visibility = 'visible';")

        webdriver.ActionChains(driver).move_to_element(given_circle).click(given_circle).perform()


        #if i+1 < len(circle_order_fast_route):
        #    next_given_circle = wait.until(
        #        EC.presence_of_element_located((By.CSS_SELECTOR, f'#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map > div.km-widget.km-scroll-wrapper > div.km-scroll-container > div:nth-child(4) > svg > circle:nth-child({circle_order_fast_route[i+1]})'))
        #    )

        #    next_given_circle_y_coordinate = next_given_circle.get_attribute("cy")
        #    next_given_circle_x_coordinate = next_given_circle.get_attribute("cy")

        print("heeeeere: ", type(given_circle))


        ############### pseudo code - start #################

        # if circle is in the middle of the frame then

        given_circle_y_coordinate = float(given_circle.get_attribute("cy"))
        given_circle_x_coordinate = float(given_circle.get_attribute("cx"))

        #driver.execute_script("document.getElementsByClassName('k-icon k-i-arrow-s')[0].click();")



            #if (given_circle is not overlapped by other circle):

            #elif (given_circle is overlapped by other circle):
            #    figure out where they overlap and where not
            #    click where they don't overlap


        ############### pseudo code - end #################


        print()
        print()
        print("------COORDINATES------")
        print(i, given_circle.get_attribute("outerHTML"))
        print()
        print()

        y_coordinate = given_circle.get_attribute("cy")
        x_coordinate = given_circle.get_attribute("cx")

        print(y_coordinate)
        print(x_coordinate)
        #driver.execute_script("document.getElementsByClassName('k-icon k-i-arrow-s')[0].click();")

        #webdriver.ActionChains(driver).move_to_element(given_circle).click_and_hold().move_by_offset(0,0).release().perform()
        #webdriver.ActionChains(driver).move_to_element(given_circle).click_and_hold(given_circle).release()
        #click(given_circle).perform()
        """webdriver.ActionChains(driver).click(zoom_out).click(zoom_out).click(zoom_out).move_to_element( \
            driver.find_element(By.CSS_SELECTOR, f'#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map > div.km-widget.km-scroll-wrapper > div.km-scroll-container > div:nth-child(4) > svg > circle:nth-child({i+2})')) \
            .click(zoom_in).click(zoom_in).click(zoom_in) \
            .click(driver.find_element(By.CSS_SELECTOR, f'#report-win13 > div.window-content > div.full-height > div > div.full-height.k-map > div.km-widget.km-scroll-wrapper > div.km-scroll-container > div:nth-child(4) > svg > circle:nth-child({i+2})')) \
            .perform()
        """


        information_box = driver.find_element(By.ID,"map-popup-13")

        try:
            #if there is a h6 header in the informationbox then there are multiple crimes at the same location
            h6_header = information_box.find_element(By.TAG_NAME, "h6")
        except:
            h6_header = False

        if h6_header:
            n_of_crimes = int(re.findall(r'-?\d+\.?\d*', h6_header.get_attribute("innerHTML"))[0])
            crime_counter_depricated = n_of_crimes

            multi_crime_element = information_box.find_elements(By.XPATH, '//div[@style="border-bottom: 1px solid gray;"]')

            for j, element in enumerate(multi_crime_element):
                crime_counter += 1
                print(element.get_attribute("innerHTML"))
                t = 0
                tm.sleep(0.1)

                crime_label_HTML = driver.find_element(By.CSS_SELECTOR,f'#map-popup-13 > div > div:nth-child({j+2}) > div:nth-child({t+1}) > span')


                if len(crime_label_HTML.get_attribute("title"))>0:
                    crime_label = crime_label_HTML.get_attribute("title")
                else:
                    crime_label = crime_label_HTML.text

                print(crime_label)

                crime_category_label_HTML = driver.find_element(By.CSS_SELECTOR, '#map-popup-13 > div > div:nth-child(1) > h5')
                crime_category_label = crime_category_label_HTML.text

                date_time_label_HTML = driver.find_element(By.CSS_SELECTOR,f"#map-popup-13 > div > div:nth-child({j+2}) > div:nth-child({t+2}) > span")
                date_time_label = date_time_label_HTML.text

                data_frame.loc[crime_counter] = pd.Series({"x_cord":x_coordinate,"y_cord":y_coordinate,"time":date_time_label,"crime":crime_label, "crime_category":crime_category_label})
                print(crime_counter)

        else:
            print("single crime: ----> ")
            crime_counter += 1

            tm.sleep(0.1)
            crime_label_HTML = driver.find_element(By.CSS_SELECTOR,'#map-popup-13 > div > div:nth-child(2) > div:nth-child(1) > span')

            print("thats what I'm looking for: ", crime_label_HTML.text)


            if len(crime_label_HTML.get_attribute("title"))>0:
                crime_label = crime_label_HTML.get_attribute("title")
            else:
                crime_label = crime_label_HTML.text

            crime_category_label_HTML = driver.find_element(By.CSS_SELECTOR, '#map-popup-13 > div > div:nth-child(1) > h5')
            crime_category_label = crime_category_label_HTML.text

            print(crime_label)

            date_time_label_HTML = driver.find_element(By.CSS_SELECTOR,'#map-popup-13 > div > div:nth-child(2) > div:nth-child(2) > span')
            date_time_label = date_time_label_HTML.text

            data_frame.loc[crime_counter] = pd.Series({"x_cord":x_coordinate,"y_cord":y_coordinate,"time":date_time_label,"crime":crime_label, "crime_category":crime_category_label})
            print(crime_counter)

        print()
        print()
        print("------ATTRIBUTES------")
        print(information_box.get_attribute("innerHTML"))
        print()
        print()
        #n_of_crimes = information_box.find_element(By.TAG_NAME,"h6")
        #print(n_of_crimes.text)
        #print(circle.get_attribute("innerHTML"))

        #if i > 20:
        #    break

        make_all_disapear()


finally:
    print("complete")
