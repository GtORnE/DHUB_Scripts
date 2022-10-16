'''
Gustavo Rene Teran Mina
Data HUB - USFQ
'''

import random
import unidecode #para quitar tildes (Install)
from time import sleep #time for prevent any situation with IP
from selenium import webdriver #This can control browser (Install)
from selenium.webdriver.common.by import By #for selenium sintaxis
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options #for set download directory
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager #(Install)
import pandas as pd #para almacenaje en csv (Install)
import csv
import os #para almacenaje de csv y carpetas

driver = webdriver.Chrome(ChromeDriverManager().install()) #Download and install chromedriver automatically
url = 'https://datosabiertos.gob.ec/dataset/'
driver.get(url)                                 #for open the page for scrapy
                                                #if the page do not load susesfully
                                                #the scrapy do not continue

#change the pages 
def nextPage(value): 
    nextPage = driver.find_element(By.XPATH, value = '//a[@href="/dataset/?page={0}"]'.format(value)) #find next page icon
    nextPage.click() #click 

#read csv files
def read_csvNames(filename):
    links = []
    metatitles = []
    with open(filename) as f:  # name for read files
        reader = csv.reader(f)
        next(reader)  # ignore first line (title)
        i = 0
        sleep(5)
        for link in reader:
            print("{0}: {1} {2}".format((i + 1), (str(link[0])), str(link[1]).replace(':', '_')))
            links.append(str(link[0]))
            metatitles.append(str(link[1]).replace(' ', '_'))
            i += 1
        print("\n\t*************Second Reading Finished*************\t")

    return links, metatitles

#read csv with hrefs
def read_csv(filename):
    links = []
    with open(filename) as f: #name for read files
        reader = csv.reader(f)
        next(reader) #ignore first line (title)
        i = 0
        sleep(5)
        for link in reader:
            print("{0}: {1}".format((i + 1), (str(link[0]))))
            links.append(str(link[0]))
            i += 1
        print("\n\t*************First Reading Finished*************\t")
    
    return links

#extract the information 
def extractHrefsMeta(): 
    infoToCSV = []
    counter = 0
    meta = driver.find_elements(By.XPATH, value = '//a[@class="pdae-package-item"]') #return a list
    for elem in meta:
        titulo = elem.find_element(By.XPATH, value = './/h2[@class="text-blue-sapphire fs-22 fw-bold m-0 leading-tight"]').text
        tituloFinal = unidecode.unidecode(titulo.lower()).replace(' ', '_') #cambia a minusculas
        tituloFinal = tituloFinal.replace(':', '_')
        hrefs = elem.get_attribute("href") #get metadata hrefs

        #to export .csv
        table_Dict = {'Href': hrefs,
                      'Title': tituloFinal} #for csv row
        infoToCSV.append(table_Dict)
        df = pd.DataFrame(infoToCSV)

        #show in console
        print("\n**************{0}**************".format(counter + 1))
        print("Seccion: {0}".format([tituloFinal]))
        print("Href: {0}".format([hrefs]))
        counter += 1    

    path = 'OpenDataHrefs.csv'
    df.to_csv(path, index = None, mode = 'a', header = not (os.path.isfile(path) and os.stat(path).st_size != 0))        
    return counter

#extract the href of databases
def extractHrefsDataBases(urls):
    for i in urls: #loop for each urls of csv file
        try:
            #set driver with each new url
            driver = webdriver.Chrome(ChromeDriverManager().install())
            url = '{0}'.format(i) #change the url 
            driver.get(url)

            hrefDatabases = [] #append the hrefs of databases
            value = 0
            sleep(random.uniform(3.0, 7.0))
            bases = driver.find_elements(By.XPATH, value = '//a[@class="pdae-resource-item"]') #take all metadata files

            #take info metadata
            metaTitle = driver.find_element(By.XPATH, value = './/h1[@class="fs-35 text-blue-sapphire fw-bold leading-tight"]').text
            fuente = driver.find_element(By.XPATH, value = './/p[@class="fw-bold m-0"]').text
            author = driver.find_element(By.XPATH, value = './/*[@id="content"]/section/div/div/div[2]/div/div[3]/p[2]').text
            email = driver.find_element(By.XPATH, value = './/a[@class="text-underline text-break"]').text
            lastUpdate = driver.find_element(By.XPATH, value = './/*[@id="content"]/section/div/div/div[2]/div/div[5]/p[2]').text
            
            #change the recover info
            metaTitleFinal = unidecode.unidecode(metaTitle.lower())
            fuenteFinal = unidecode.unidecode(fuente.lower())
            authorFinal = unidecode.unidecode(author)
            emailFinal = unidecode.unidecode(email)

            #print information
            print('\n\t*********Metadata Information*********')
            print("MetaTitle: {0}".format([metaTitleFinal]))
            print("Fuente: {0}".format([fuenteFinal]))
            print("Author: {0}".format([authorFinal]))
            print("Email: {0}".format([emailFinal]))
            print("Last Update: {0}".format([lastUpdate]))

            #Replace special characters for _
            metaTitleFinal = metaTitleFinal.replace(' ', '_')
            metaTitleFinal = metaTitleFinal.replace('/', '_')
            metaTitleFinal = metaTitleFinal.replace('?', '_')
            metaTitleFinal = metaTitleFinal.replace('#', '_ ')
            metaTitleFinal = metaTitleFinal.replace(':', '_')
            metaTitleFinal = metaTitleFinal.replace('|', '_')
            metaTitleFinal = metaTitleFinal.replace('<', '_')
            metaTitleFinal = metaTitleFinal.replace('>', '_')

            for hrefbase in bases:
                href = hrefbase.get_attribute("href")

                #to export .csv
                table_Dict = {'HrefBases': href, #set the rows for csv file
                            'MetaTitle': metaTitleFinal,
                            'Fuente': fuenteFinal,
                            'Author': authorFinal,
                            'Email': emailFinal,
                            'Last Update': lastUpdate}
                hrefDatabases.append(table_Dict)
                df = pd.DataFrame(hrefDatabases)

                #show in console 
                print('\n**************{0}**************'.format(value + 1))
                print("Href: {0}".format([href]))
                value += 1
                sleep(3)

            path = 'OpenDataHrefsBases.csv' #file name
            df.to_csv(path, index = None, mode = 'a', header = not (os.path.isfile(path) and os.stat(path).st_size != 0))
            driver.close() #close chrome

        except:
            print('\n\t*****Incorrect xpat*****\n')  
            print('\n\a\t*****{0}*****\n'.format(metaTitleFinal))
            driver.close() #close chrome
            continue

#download bases
def downloadFiles(download, folderName):
    chromeOptions = Options()
    #create the folder where will to download files
    if not os.path.exists("Datos_Abiertos"): #create the main folder
            os.mkdir("Datos_Abiertos")
    k = 0
    for i in download:

        driver = webdriver.Chrome(executable_path = ChromeDriverManager().install(), chrome_options = chromeOptions)
        url = '{0}'.format(i) #set the new url for download
        try:
            chromeOptions.add_experimental_option("prefs", {  # set the download directory
                "download.default_directory": "D:\\Datos_Abiertos\\{0}".format(
                    folderName[k]),
            })

            if not os.path.isdir(folderName[k]):  # create each folder for each database
                os.mkdir(folderName[k])
            driver.get(url)

            print('Url {0}: {1} Titulo: {2}'.format((k + 1), [url], folderName[k]))
            sleep(3)
            info = driver.find_element(By.XPATH, value = '//i[@class="bi bi-download"]')#find the download botton
            info.click()#click
            sleep(random.uniform(30.0, 40.0))#wait between 30 and 40 seconds
            driver.close() #close chrome
            k += 1
        except: #exception for falls
            print('\n\t*****Incorrect url*****\n')
            driver.close() #close chrome
            k += 1
            continue



if __name__ == "__main__":

    pages = 2
    value = 2
    conjuntosTotales = driver.find_element(by=By.XPATH, value='/html/body/main/section[2]/div/div/div[2]/div[1]/div[1]/p').text
    print('\n\t{0}'.format([conjuntosTotales]))
    for i in range(41):  # loop for the pages limit
        centinel = extractHrefsMeta()  # extract the principal hrefs
        if (centinel == 20):
            nextPage(value)  # change to next page
            print("\n\t*****PAGE {0}*****".format(pages))
            pages += 1
            value += 1
            sleep(random.uniform(5.0, 10.0))  # wait between 5 or 10 seconds
        else:
            continue

    driver.close()  # close the first driver

    print("\n****Reading Metadata hrefs of CSV...****")
    links = read_csv('OpenDataHrefs.csv')
    extractHrefsDataBases(links)#pass each href for extract the others hrefs

    print("\n****Reading Databases hrefs of CSV...****")
    download, metaFolders = read_csvNames('OpenDataHrefsBases.csv')
    downloadFiles(download, metaFolders)#pass the hrefs for begin download

    print("\n\t*************Finished*************")
