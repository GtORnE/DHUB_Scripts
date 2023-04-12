'''
Gustavo Rene Teran Mina
Data HUB - USFQ
'''

import random #para que el tiempo de espera sea irregular
import unidecode #para quitar tildes (Install)
from time import sleep #time for prevent any situation with IP
from selenium import webdriver #This can control browser (Install)
from selenium.webdriver.common.by import By #for selenium sintaxis
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options #for set download directory
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager #(Install)
import pandas as pd #para almacenaje en csv (Install)
import csv #lectura de csv
import string #para modificacion de caracteres
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
    sleep(random.uniform(3.0, 5.0))

#read csv files
def read_csvNames(filename):
    links = []
    metatitles = []
    metaBasesDescription = []
    fuente = []
    author = []
    email = []
    lastUpdate = []
    tag = []
    with open(filename) as f:  # name for read files
        reader = csv.reader(f)
        next(reader)  # ignore first line (title)
        sleep(5)
        i = 0
        for link in reader:
            if len(link) >= 8:
                print("{0}: {1} {2} {3} \n{4} {5} {6} {7} \n{8}\n".format((i + 1), str(link[0]), str(link[1]), str(link[2]), str(link[3]), str(link[4]), str(link[5]), str(link[6]), str(link[7])))
                links.append(str(link[0]))
                metatitles.append(str(link[1]))
                metaBasesDescription.append(str(link[2]))
                fuente.append(str(link[3]))
                author.append(str(link[4]))
                email.append(str(link[5]))
                lastUpdate.append(str(link[6]))
                tag.append(str(link[7]))
                i += 1
        print("\n\t******Second Reading Finished****\t")

    return links, metatitles, metaBasesDescription, fuente, author, email, lastUpdate, tag

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

#extraer de otro documento
# read csv with hrefs
def read_csv02(filename):
    links = []
    titles = []
    with open(filename) as f:  # name for read files
        reader = csv.reader(f)
        next(reader)  # ignore first line (title)
        sleep(5)
        i = 0
        for link in reader:
            if len(link) >= 2:
                print("{0}: Link: {1} \n Title: {2}".format((i + 1), (str(link[0])), (str(link[1]))))
                links.append(str(link[0]))
                titles.append(str(link[1]))
                i += 1
        print("\n\t******First Reading Finished****\t")

    return links, titles

#modificar el nombre de las bases
def modificarNombre(name):
    # change the recover info
    namefinal = unidecode.unidecode(name)
    specialCharacters = ' /?#:|<>.,'
    translation_table = str.maketrans({char: "_" for char in specialCharacters})
    return namefinal.translate(translation_table).lower()

#extract the information
def extractHrefsMeta():
    infoToCSV = []
    counter = 0
    meta = driver.find_elements(By.XPATH, value = '//a[@class="pdae-package-item"]') #return a list

    for elem in meta:
        titulo = elem.find_element(By.XPATH, value = './/h2[@class="text-blue-sapphire fs-22 fw-bold m-0 leading-tight"]').text
        tituloFinal = modificarNombre(titulo)
        hrefs = elem.get_attribute("href") #get metadata hrefs

        #to export .csv
        table_Dict = {'Href': hrefs,
                      'Title': tituloFinal} #for csv row
        infoToCSV.append(table_Dict)
        df = pd.DataFrame(infoToCSV)

        #show in console
        print("\n*****{0}*****".format(counter + 1))
        print("Seccion: {0}".format([tituloFinal]))
        print("Href: {0}".format([hrefs]))
        counter += 1

    path = 'OpenDataHrefs.csv'
    df.to_csv(path, index = None, mode = 'a', header = not (os.path.isfile(path) and os.stat(path).st_size != 0))
    return counter

# extract the href of databases
def extractHrefsDataBases(urls):
    for i in urls:  # loop for each urls of csv file
        try:
            # set driver with each new url
            driver = webdriver.Chrome(ChromeDriverManager().install())
            url = '{0}'.format(i)  # change the url
            driver.get(url)

            hrefDatabases = []  # append the hrefs of databases
            value = 0
            sleep(random.uniform(3.0, 7.0))

            # take info metadata
            metaTitle = driver.find_element(By.XPATH,
                                            value='.//h1[@class="fs-35 text-blue-sapphire fw-bold leading-tight"]').text
            metaTitleDescriprion = driver.find_element(By.XPATH, value='.//div[@class="text-jungle-green fs-md mt-16 leading-normal"]').text
            tag = driver.find_element(By.XPATH, value='.//span[@class="pdae-tag"]').text
            fuente = driver.find_element(By.XPATH, value='.//p[@class="fw-bold m-0"]').text
            author = driver.find_element(By.XPATH,
                                         value='.//*[@id="content"]/section/div/div/div[2]/div/div[3]/p[2]').text
            email = driver.find_element(By.XPATH, value='.//a[@class="text-underline text-break"]').text
            lastUpdate = driver.find_element(By.XPATH,
                                             value='.//*[@id="content"]/section/div/div/div[2]/div/div[5]/p[2]').text

            # change the recover info
            metaTitleFinal = modificarNombre(metaTitle)
            metaTitleDescriprionFinal = unidecode.unidecode(metaTitleDescriprion.lower())
            fuenteFinal = modificarNombre(fuente)
            authorFinal = modificarNombre(author)
            emailFinal = unidecode.unidecode(email.lower())
            etiquetaFinal = modificarNombre(tag)
            lastUpdateFinal = modificarNombre(lastUpdate)


            # print information
            print('\n\t****Metadata Information****')
            print("MetaTitle: {0}".format([metaTitleFinal]))
            print("Metatitle description: {0}".format([metaTitleDescriprionFinal]))
            print("Tags: {0}".format([etiquetaFinal]))
            print("Fuente: {0}".format([fuenteFinal]))
            print("Author: {0}".format([authorFinal]))
            print("Email: {0}".format([emailFinal]))
            print("Last Update: {0}".format([lastUpdateFinal]))

            bases = driver.find_elements(By.XPATH, value='//a[@class="pdae-resource-item"]')  # take all metadata files
            for hrefbase in bases:
                href = hrefbase.get_attribute("href")
                # to export .csv
                table_Dict = {'HrefBases': href,  # set the rows for csv file
                              'MetaTitle': metaTitleFinal,
                              'Metatitle Descriprion': metaTitleDescriprionFinal,
                              'Fuente': fuenteFinal,
                              'Author': authorFinal,
                              'Email': emailFinal,
                              'Last Update': lastUpdate,
                              'Tags': etiquetaFinal}
                hrefDatabases.append(table_Dict)
                df = pd.DataFrame(hrefDatabases)

                # show in console
                print('\n*****{0}*****'.format(value + 1))
                print("Href: {0}".format([href]))
                value += 1
                sleep(2)

            path = 'OpenDataHrefsBases.csv'  # file name
            df.to_csv(path, index=None, mode='a', header=not (os.path.isfile(path) and os.stat(path).st_size != 0))
            driver.close()  # close chrome

        except Exception as e:  # exception for failures
            print('\n\t**Incorrect xpat**')
            print(e)
            print('\n\a\t**{0}**\n'.format(metaTitleFinal))
            driver.close()  # close chrome
            continue

#Info Databases
def addMoreInformation(link, metatile, metadescription, fuente, author, email, lastUpdate, tag):
    k = 0
    for i in link:
        try:
            moreInfoDatabases = []
            driver = webdriver.Chrome(ChromeDriverManager().install())
            url = '{0}'.format(i)  # set the new url for download
            driver.get(url)
            sleep(random.uniform(3.0, 5.0))
            databaseDescription = driver.find_element(By.XPATH, value='.//*[@id="content"]/section/div/div/div[1]/div/div[2]/div/div[1]').text
            databaseDescriptionFinal = unidecode.unidecode(databaseDescription.lower())

            # print information
            print('\n\t****Metadata Information {0}****'.format(k + 1))
            print("MetaTitle: {0}".format([metatile[k]]))
            print("Href: {0}".format(i))
            print("Metatitle description: {0}".format([metadescription[k]]))
            print("Tags: {0}".format([tag[k]]))
            print("Fuente: {0}".format([fuente[k]]))
            print("Author: {0}".format([author[k]]))
            print("Email: {0}".format([email[k]]))
            print("Last Update: {0}".format([lastUpdate[k]]))
            print("Database description: {0}\n".format([databaseDescriptionFinal]))

            # to export .csv
            table_Dict = {'HrefBases': i,  # set the rows for csv file
                          'MetaTitle': metatile[k],
                          'Metatitle Descriprion': metadescription[k],
                          'Fuente': fuente[k],
                          'Author': author[k],
                          'Email': email[k],
                          'Last Update': lastUpdate[k],
                          'Tags': tag[k],
                          'Database description': databaseDescriptionFinal}
            moreInfoDatabases.append(table_Dict)
            df = pd.DataFrame(moreInfoDatabases)
            #sleep(3)
            driver.close()  # close chrome
            path = 'OpenDataHrefsBasesComplete.csv'  # file name
            if os.path.isfile(path) and os.stat(path).st_size != 0:
                df.to_csv(path, index=None, mode='a', header=False)
            else:
                df.to_csv(path, index=None, mode='w', header=True)
            k += 1

        except Exception as e:  # exception for failures
            print('\n\t**Incorrect url**\n')
            print(e)
            k += 1
            driver.close()
            continue

#download bases
def downloadFiles(download, folderName):
    chromeOptions = Options()
    base_folder = "Datos_Abiertos"
    base_path = os.path.join("C:\\Users\\00324422\\Desktop\\OpenData_Documents\\OpenData_Information", base_folder)

    #create the folder where will to download files
    if not os.path.exists(base_path): #create the main folder
        os.mkdir(base_path)

    k = 0
    for i in download:
        driver = webdriver.Chrome(executable_path = ChromeDriverManager().install(), chrome_options = chromeOptions)
        url = '{0}'.format(i) #set the new url for download
        try:
            folder_path = os.path.join(base_path, folderName[k])
            chromeOptions.add_experimental_option("prefs", {  # set the download directory
                "download.default_directory": folder_path,
            })

            if not os.path.isdir(folder_path):  # create each folder for each database
                os.mkdir(folder_path)
            driver.get(url)

            print('Titulo {0}: {1} \n URL: {2}'.format((k + 1), folderName[k], [url]))
            sleep(3)
            info = driver.find_element(By.XPATH, value = '//i[@class="bi bi-download"]')#find the download botton
            info.click()#click
            sleep(random.uniform(15.0, 25.0))  # wait between 15 and 25 seconds
            driver.close() #close chrome
            k += 1
        except Exception as e: #exception for failures
            print('\n\t**Incorrect url**\n')
            print(e)
            driver.close() #close chrome
            k += 1
            continue


if _name_ == "_main_":
    pages = 2
    value = 2
    conjuntosTotales = driver.find_element(by=By.XPATH,
                                           value='/html/body/main/section[2]/div/div/div[2]/div[1]/div[1]/p').text
    print('\n\t{0}'.format([conjuntosTotales]))
    #verificar numero de paginas en la pagina web
    '''for i in range(42):  # loop for the pages limit
        centinel = extractHrefsMeta()  # extract the principal hrefs
        if (centinel == 20):
            nextPage(value)  # change to next page
            print("\n\t**PAGE {0}**".format(pages))
            pages += 1
            value += 1
            sleep(random.uniform(5.0, 10.0))  # wait between 5 or 10 seconds
        else:
            continue'''

    driver.close()  # close the first driver

    print("\n***Reading Metadata hrefs of CSV...*")
    #links = read_csv('OpenDataHrefs.csv')
    #extractHrefsDataBases(links)  # pass each href for extract the others hrefs

    print("\n***Reading Databases hrefs of CSV...*")
    links, metatitles, metaBasesDescription, fuente, author, email, lastUpdate, tag = read_csvNames('OpenDataHrefsBases.csv')
    addMoreInformation(links, metatitles, metaBasesDescription, fuente, author, email, lastUpdate, tag)

    print("\n***Reading Databases hrefs Complete of CSV...*")
    links02, metatitles02 = read_csv02('OpenDataHrefsBasesComplete.csv')

    print("\n***Downloading Databases hrefs of CSV...*")
    downloadFiles(links02, metatitles02)  # pass the hrefs for begin download

    print("\n\t******Finished****")