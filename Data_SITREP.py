'''
Gustavo Rene Teran Mina
Data HUB - USFQ BootCamp
'''


import unidecode #para quitar tildes (Install)
from time import sleep #time for prevent any situation with IP
from selenium import webdriver #This can control browser (Install)
from selenium.webdriver.common.by import By #for selenium sintaxis
from selenium.webdriver.chrome.options import Options #for set download directory
from webdriver_manager.chrome import ChromeDriverManager #(Install)
import pandas as pd #para almacenaje en csv (Install)
import csv #lectura de csv
import os #para almacenaje de csv y carpetas
import pyautogui #(Install)

driver = webdriver.Chrome(ChromeDriverManager().install()) #Download and install chromedriver automatically
url = 'https://www.gestionderiesgos.gob.ec/informes-de-situacion-covid-19-desde-el-13-de-marzo-del-2020/'
driver.get(url)

#modificar el nombre de las bases
def modificarNombre(name):
    # change the recover info
    namefinal = unidecode.unidecode(name)
    specialCharacters = ' /?#:|<>.,'
    translation_table = str.maketrans({char: "_" for char in specialCharacters})
    return namefinal.translate(translation_table)


# read csv with hrefs
def read_csv(filename):
    links = []
    with open(filename) as f:  # name for read files
        reader = csv.reader(f)
        next(reader)  # ignore first line (title)
        i = 0
        sleep(5)
        for link in reader:
            print("{0}: {1}".format((i + 1), (str(link[0]))))
            links.append(str(link[0]))
            i += 1
        print("\n\t******First Reading Finished****\t")
    return links


def extractHrefsMeta():
    infoToCSV = []
    counter = 0

    meta = driver.find_elements(By.TAG_NAME, value="p")  # return a list
    for elem in meta:
        try:
            hrefs = []  # create empty list to store hrefs
            links = elem.find_elements(By.TAG_NAME, "a")

            for link in links:
                href = link.get_attribute("href")
                hrefs.append(href)  # add href to list

            # join hrefs list into comma-separated string
            hrefs_str = ', '.join(hrefs)

            # add row to CSV data list
            table_Dict = {'Href': hrefs_str,
                          'Counter': counter}  # for csv row
            infoToCSV.append(table_Dict)

            # create DataFrame and write to CSV
            df = pd.DataFrame(infoToCSV)
            path = 'Situacion_(SITREP).csv'
            df.to_csv(path, index=None, mode='a', header=not (os.path.isfile(path) and os.stat(path).st_size != 0))

            # print output to console
            print("\n*****{0}*****".format(counter + 1))
            print("Href: {0}".format(hrefs_str))
            counter += 1

        except Exception as e:  # exception for failures
            print('\n\t**Incorrect xpath**')
            print(e)
            continue


def downloadFiles(download):
    chromeOptions = Options()
    k = 0
    for i in download:
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chromeOptions)
        url = '{0}'.format(i)  # set the new url for download

        try:
            driver.get(url)
            sleep(10)
            # Obtener la posición del botón de descarga utilizando OCR (reconocimiento óptico de caracteres)
            download_button_position = pyautogui.locateCenterOnScreen('IconoBotonDescarga.png')
            # Hacer clic en el botón de descarga
            pyautogui.click(download_button_position)
            sleep(5)
            save_button_position = pyautogui.locateCenterOnScreen('IconoGuardarDescarga.png')
            # Hacer clic en el botón de guardar
            pyautogui.click(save_button_position)
            sleep(3)
            # print output to console
            print("\n*****{0}*****".format(k + 1))
            print("Href: {0}".format(i))
            driver.close()  # close chrome
            k += 1
        except Exception as e:  # exception for failures
            print('\n\t**Incorrect url**\n')
            print(e)
            driver.close()  # close chrome
            k += 1
            continue


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #extractHrefsMeta()
    driver.close()
    urls = read_csv('Situacion_(SITREP).csv')
    downloadFiles(urls)

