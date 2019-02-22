import csv
import urllib3
import nltk
nltk.download('stopwords')
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import requests
import requests as req
import idna
from gzip import zlib
from idna import core

http = urllib3.PoolManager()
urllib3.disable_warnings()

# Open .csv file
with open('C:/Users/HP/Desktop/Mosaic Case Study/05 Python/WebsitesList_In.csv', "r", encoding="utf8") as csvfile:

    # Prepare csv files
    in_file = open('C:/Users/HP/Desktop/WebsitesList_In.csv', "r", encoding="utf8")
    readCSV = csv.reader(csvfile, delimiter=';')
    first_row = next(readCSV)
    out_file = open('C:/Users/HP/Desktop/MosaicWebsitesList_Out.csv', "a", encoding="utf8")

    for line in readCSV:

        writer = csv.writer(out_file, delimiter=';')

        CurrentWebsite = line[1]

        url = str.format(CurrentWebsite)

        headers = {'User-Agent': "Magic Browser"}

        try:
            http_pool = urllib3.connection_from_url(url)

            session = requests.Session()
            session.max_redirects = 3

            resp = req.get(url, timeout=15)

            url = resp

            print(line)

            print(url)

            most_rated_language = ""

            if resp.status_code == 200 or resp.status_code == 403 or resp.status_code == 402 or resp.status_code == 404 or resp.status_code == "" or resp.status_code == "301" or resp.status_code == "302" or resp.status_code == "302"  or resp.status_code == "303"  or resp.status_code == "307"  or resp.status_code == "308" or resp.status_code == "":

                soup = BeautifulSoup(url.content, 'html.parser')


                # 1 # if found then, most_rated_language = "english"  ##################################################
                # Check header and links to English site
                lang = soup.find_all(lang={"/en/", "en-US", "en-GB"})
                links = soup.find_all(hreflang={"en", "en-US", "en-GB"})

                # Funktioniert das so?
                if lang in ["/en/", "en-US", "en-GB"]:
                    
                    most_rated_language = "english"
                
                else:
                    # 2 # else check paragraphs  ###########################################################################
                    # Check Paragraphs:
                    pars = soup.find_all('p')
                    par = []
                    a = []
                    string_pars=''
                    for par in pars:
                        a.append(par)
                        strip = par.get_text().strip()
                    string_pars = str(a)
                    #print(a)
    
                    # 3 # else if paragraphs empty then try something else like 'div' or other tags ########################
                    string_divs=''
                    if string_pars=='':
                        divs = soup.find_all('div')
                        div = []
                        b = []
        
                        for div in divs:
                            b.append(div)
                            strip = div.get_text().strip()
                        string_divs = str(b)
        
                        #print(b)
                        
                    else:
                         print('Par worked')
                    # 4 # else if paragraphs and divs empty then take the whole html text ##################################
    
                    string_html=''
                    if string_divs==[] and string_pars==[]:
                        print('html')


                    # 5 # Check language - if string pars empty, then string_divs, then webtext,... ########################
                    
                    string_all = string_pars+'\n'+string_divs+'\n'+string_html

                    #print(string_all)

                    stopwords.fileids()
                    stopwords.words('english')
                    languages_ratios = {}
                    tokens = wordpunct_tokenize(string_all)
                    words = [word.lower() for word in tokens]
    
                    writer = csv.writer(out_file, delimiter=';')
    
                    for language in stopwords.fileids():
    
                            stopwords_set = set(stopwords.words(language))
                            words_set = set(words)
                            common_elements = words_set.intersection(stopwords_set)
                            languages_ratios[language] = len(common_elements) # language score
    
                            # Detected Language
                            most_rated_language = max(languages_ratios, key=languages_ratios.get)
    
                    # 6 # if  most_rated language ={'arabic': 0, 'azerbaijani': 0, 'danish': 0, ...} all zero, then most_rated_language = "english"

                    print(most_rated_language)
            else:
                print('Connection failed.')

        except urllib3.exceptions.MaxRetryError as e:
                print('Connection failed.')
                most_rated_language = e
        except urllib3.exceptions.NewConnectionError as e:
                print('Connection failed.')
                most_rated_language = e
        except requests.exceptions.ConnectionError as e:
                print('Connection failed.')
                most_rated_language = e
        except urllib3.exceptions.LocationValueError as e:
                print('Host Error')
                most_rated_language = e
        except requests.exceptions.TooManyRedirects as e:
                print('Connection failed.')
        except requests.exceptions.ReadTimeout as e:
                print('Connection failed.')
        except idna.IDNAError as e:
                print('Connection failed')
        except zlib.error as e:
                print('Connection failed')
        except  urllib3.exceptions.DecodeError as e:
                print('Connection failed.')
        except  requests.exceptions.ContentDecodingError as e:
            print('Connection failed.')

        writer.writerow(line + [most_rated_language])

    with out_file:
        writer = csv.writer(out_file, delimiter=';')
        writer.writerow(line + [most_rated_language])
        out_file.flush()
