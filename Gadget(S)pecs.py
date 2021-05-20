import requests
from bs4 import BeautifulSoup as bs
from progress.bar import PixelBar
import os
import time
from texttable import Texttable
from prettytable import PrettyTable
from colorama import Fore,Back,Style
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

rangeOpts = [
    'list-of-laptops/laptops-in-range-of-20000',
    'list-of-laptops/laptops-in-range-of-20000-to-30000',
    'list-of-laptops/laptops-in-range-of-30000-to-40000',
    'list-of-laptops/laptops-in-range-of-40000-to-50000',
    'list-of-laptops/laptops-in-range-of-50000-to-60000',
    'lss-4187',
    'top-10-laptops-in-india'
]

laptops = []
lapSpecScore = []
lapUrls = []
lapPrice = []
specifications = []
propertys = []
values = []

def properties(soup):
    for props in soup.findAll('td',{'class':'spec_ttle'}):
        propertys.append(bcolors.WARNING+props.get_text()+bcolors.ENDC)

def valus(soup):
    for props in soup.findAll('td',{'class':'spec_des'}):
        some = props.get_text()
        vals = some.replace(' ','')
        final = vals.replace('\n','')
        if(len(final) == 0):
            for i in props.findAll('img'):
                values.append(f'{bcolors.BOLD}'+i['alt']+f'{bcolors.ENDC}')
        else:
            values.append(f'{bcolors.BOLD}'+final+f'{bcolors.ENDC}')
            
    print(values)

def scrapeRanges(rangeUrl):
    Headers = { "User-Agent": 'Mozila/5.0 (Windows NT 10.0; Win64; X64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.100 Safari/537.36' }
    page = requests.get(rangeUrl, headers = Headers)
    soup = bs(page.content,'html.parser')

    for i in soup.findAll('div',{'class','finder_snipet_wrap'}):
        for x in i.findAll('div',{'class','filter filer_finder'}):
            for y in x.findAll('div',{'class','filter-grey-bar'}):
                for rating in y.findAll('div',{'class','rating_box_new_list'}):
                    lapSpecScore.append(rating.getText())
                for nt in y.findAll('h3'):
                    for name in nt.findAll('a'):
                        lapUrls.append('https://91mobiles.com'+name['href'])
                        laptops.append(name.getText())
                for a in y.findAll('div',{'class':'filter-right'}):
                    for amt in a.findAll('span',{'class':'price price_padding'}):
                        lapPrice.append(amt.getText())

    t = Texttable()
    ro = []
    ro.append(['S.no','Name', 'Age'])
    for ins in range(0,len(lapPrice)):
        ro.append([str(ins+1),laptops[ins],lapPrice[ins]])

    t.add_rows(ro)
    os.system('cls')
    print(f'{bcolors.WARNING}'+t.draw())

    theOne = int(input('Which Laptop?'))
    theOnePage = requests.get(lapUrls[theOne-1])
    theOneSoup = bs(theOnePage.content, 'html.parser')

    try:
        price = theOneSoup.find('span',{'itemprop':'price'}).getText()
        name = theOneSoup.find('span',{'itemprop':'name'}).getText()
    except AttributeError:
        print('wait')

    properties(theOneSoup)
    valus(theOneSoup)

    print(len(propertys))
    print(len(values))

    if len(propertys) == len(values):
        arrow = "----->"
        det = f"{bcolors.HEADER}Laptop Details{bcolors.ENDC}"
        spec = f"{bcolors.WARNING}Specifications{bcolors.ENDC}"
        print('\n')
        print(f"{det:^100}")
        print('\nName: \t\t\t'+f'{bcolors.BOLD}'+name+f'{bcolors.ENDC}'+'\nPrice(Today):\t\t'+f'{bcolors.BOLD}'+price+f'{bcolors.ENDC}'+'\n\n')
        spcaer = int(os.get_terminal_size().columns/2)
        print('\n')
        
        specTable = PrettyTable()
        specTable.field_names = [Back.WHITE+'Property'+Style.RESET_ALL,Back.WHITE+'Value'+Style.RESET_ALL] 
        specRow = []
        for ins in range(0,len(propertys)):
            specRow.append([propertys[ins],values[ins]])

        specTable.align[Back.WHITE+'Property'+Style.RESET_ALL] = 'l'
        specTable.align[Back.WHITE+'Value'+Style.RESET_ALL] = 'l'
        specTable.align['value'] = 'l'
        specTable.add_rows(specRow)
        print(specTable)
        input("Press Enter to continue...")

    else:
        print("There is an un-known error occurred")

def fetchAndPrintData(theUrl):
    devPage = requests.get(theUrl)
    theOneSoup = bs(devPage.content, 'html.parser')
    
    try:
        price = theOneSoup.find('span',{'itemprop':'price'}).getText()
        name = theOneSoup.find('span',{'itemprop':'name'}).getText()
    except AttributeError:
        name = 'None'
        price = 'Discontined Model'

    properties(theOneSoup)
    valus(theOneSoup)

    print(len(propertys))
    print(len(values))

    if len(propertys) == len(values):
        arrow = "----->"
        det = f"{bcolors.HEADER}Laptop Details{bcolors.ENDC}"
        spec = f"{bcolors.WARNING}Specifications{bcolors.ENDC}"
        print('\n')
        print(f"{det:^100}")
        print('\nName: \t\t\t'+f'{bcolors.BOLD}'+name+f'{bcolors.ENDC}'+'\nPrice(Today):\t\t'+f'{bcolors.BOLD}'+price+f'{bcolors.ENDC}'+'\n\n')
        spcaer = int(os.get_terminal_size().columns/2)
        print('\n')
        
        specTable = PrettyTable()
        specTable.field_names = [Back.WHITE+'Property'+Style.RESET_ALL,Back.WHITE+'Value'+Style.RESET_ALL] 
        specRow = []
        for ins in range(0,len(propertys)):
            specRow.append([propertys[ins],values[ins]])

        specTable.align[Back.WHITE+'Property'+Style.RESET_ALL] = 'l'
        specTable.align[Back.WHITE+'Value'+Style.RESET_ALL] = 'l'
        specTable.align['value'] = 'l'
        specTable.add_rows(specRow)
        print(specTable)
        input("Press Enter to continue...")

    else:
        print("There is an un-known error occurred")
    


def askOptions():
    thestr = f'''{Fore.CYAN}    MMMMMMMMMMNXKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKXWMMMMMMMMMMMMMM
    MMMMMMMMMNo'........................................................................,kWMMMMMMMMMMMMM
    MMMMMMMMMX:  ..;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;,,,,,,.  .oWMMMMMMMMMMMMM
    MMMMMMMMMX:  .{Fore.GREEN}oNWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNNXXXXX0{Style.RESET_ALL}:  .{Fore.CYAN}oWMMMMMMMMMMMMM
    MMMMMMMMMX:  .{Fore.GREEN}oWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWNNNNNK{Style.RESET_ALL}:. .{Fore.CYAN}oWMMMMMMMMMMMMM
    MMMMMMMMMX:  .{Fore.GREEN}oWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWNNNNNK{Style.RESET_ALL}:. .{Fore.CYAN}oWMMMMMMMMMMMMM
    MMMMMMMMMX:  .{Fore.GREEN}oWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWKkkkkkkkxxddddo{Style.RESET_ALL}'  .{Fore.CYAN}:xkkkkkkkKWMMMM
    MMMMMMMMMX:  .{Fore.GREEN}oWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMK|{Style.RESET_ALL}{Fore.CYAN};-----------'00'-----------;KMMMM
    MMMMMMMMMX:  .{Fore.GREEN}oWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0|{Style.RESET_ALL}  {Fore.YELLOW}|Oddddddddxxxxxddddddddc|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMMMMMMMX:  .{Fore.GREEN}oWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMMMMMMMMMMMO|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMMMMMMMX:  .{Fore.GREEN}oWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMMMMMMMMMMMO|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMMMMMMMX:  .{Fore.GREEN}oWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMMMMMMMMMMMO|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMMMMMMMX:  .{Fore.GREEN}oWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMMMMMMMMMMMO|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMMMMMMMX:  .{Fore.GREEN}oWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMMMMMMMMMMMO|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMMWXKKKO;  .{Fore.GREEN}c0KKKKNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMMMMMMMMMMMO|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMMK:',;,',;,,,;,',{Fore.GREEN}kMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMMMMMMMMMMMO|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMM0{Fore.YELLOW}|l0XKXXXXKKXKo|{Style.RESET_ALL}{Fore.GREEN}xWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMMMMMMMMMMMO|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMM0{Fore.YELLOW}|lNMMMMMMMMMWx|{Style.RESET_ALL}{Fore.GREEN}xWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMMMMMMMMMWWk|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMM0{Fore.YELLOW}|lNMMMMMMMMMMx|{Style.RESET_ALL}{Fore.GREEN}xWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWO|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMMMMMMMMWWWk|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMM0{Fore.YELLOW}|lNMMMMMMMMMMx|{Style.RESET_ALL}{Fore.GREEN}xWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWNO|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMMMMMMWWNNNk|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMM0{Fore.YELLOW}|lNMMMMMMMMMWx|{Style.RESET_ALL}{Fore.GREEN}xWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWNNNO|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMMMMWWNNNNNk|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMM0{Fore.YELLOW}|lNMMMMMMMMMWd|{Style.RESET_ALL}{Fore.GREEN}ckOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkkxxxxxo|{Style.RESET_ALL}  {Fore.YELLOW}|OMMMMMMMMMMMWWWNNNNNNNk|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMM0{Fore.YELLOW}|lNMMMMMMMMWNd|{Style.RESET_ALL}{Fore.CYAN}..............................................   {Fore.YELLOW}|OMMMMMMWWWWWNNNNNNNNNNk|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMM0{Fore.YELLOW}|lNMMMMMMWWWNd|{Style.RESET_ALL}{Fore.CYAN},clllllllllllllllllllc.         .,cllllllllll:.  {Fore.YELLOW}|kWWWWWWNNNNNNNNNNNNNNNk|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMM0{Fore.YELLOW}|lNMMMWWWNNNNd|{Style.RESET_ALL}{Fore.CYAN}xWMMMMMMMMMMWXKKKKKKKO;         .c0KKKKKKKNWM0,  {Fore.YELLOW}|kNNNNNNNNNNNNNNNNNNNNNk|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMM0{Fore.YELLOW}|lXWWWNNNNNNNd|{Style.RESET_ALL}{Fore.CYAN}xWMMMMMMMMMMKc.........          .........oNM0,  {Fore.YELLOW}|xXXXXXXXXXXXXXXXXXXXXXx|{Style.RESET_ALL} {Fore.CYAN}0MMMM
    MMMM0{Fore.YELLOW}|lKKKKKKKKKKKo|{Style.RESET_ALL}{Fore.CYAN}xWMMMMMMMMMMXl,,,,,,,,,,,,,,,,,,,,,,,,,,,,dNM0,  __________(0)___________ ,0MMMM
    MMMM0,.....''''(0)''''......xMMMMMMMMMMMWNNNNNNNNNNNNNNNNNNNNNNNNNNNNNWMM0;  MMMMMMMMM.:::.MMMMMMMMMM ,0MMMM
    MMMMXxooooodxdooooodKMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNOooooooooooooodoooooooooooookNMMMM'''
    while True:
        os.system('cls')
        print(thestr.center(10))
        device = str(input(f'{Style.RESET_ALL}Select your Option\n1. Search Laptops\n2. Search Mobile\nYour Choice:\t'))
        if(device == '1'):            
            option = str(input(f'{Style.RESET_ALL}Select your Option\n1. Search Laptop Model\n2. Recomend A Laptop\nYour Choice:\t'))
            if(option == '1'):
                mobile = input('What is the Device Brand/Name?')
                url = "https://www.91mobiles.com/search_page.php?q=" + mobile + "&type=all&utm_source=autosuggest"
                url = ' '.join(url.split())
                op = webdriver.ChromeOptions()
                op.add_argument('headless')
                driver = webdriver.Chrome('./chromedriver',options=op) 
                driver.get(url) 
                time.sleep(3)
                html = driver.page_source
                searchSoup =  bs(html, 'html.parser')
                texts = []
                links = []
                for i in searchSoup.findAll('ul',{'class':'product_listing'}):
                    for j in i.findAll('li',{'class':'finder_snipet_wrap'}):
                        for k in j.findAll('div',{'class':'content_info'}):
                            for link in k.findAll('div',{'class':'pro_grid_name'}):
                                temp = link.a['href']
                                temp = temp.replace(' ','')
                                temp = temp.replace('\n','')
                                links.append('https://91mobiles.com'+temp)
                                tname = link.getText()
                                tname = tname.replace('  ','')
                                tname = tname.replace('\n','')
                                texts.append(tname)
                for i in range(0,len(texts)):
                    print(str(i+1)+"\t: \t"+texts[i])
                number = 0
                number = input('Enter the number of the mobile you want to search?')
                searchUrl = links[int(number)-1]
                searchUrl = ' '.join(searchUrl.split())
                with PixelBar('Processing...', max=30) as bar:
                    for xys in range(30):
                        time.sleep(0.1)
                        bar.next()

                fetchAndPrintData(searchUrl)
                
            elif(option == '2'):
                os.system('cls')
                choice = 1
                if(choice == 1):
                    theRange = int(input(f'What\'s Your Range?\n{bcolors.WARNING}1. Below Rs. 20000\n2. Rs. 20000 to Rs. 30000\n3. Rs.30000 to Rs. 40000\n4. Rs.40000 to Rs. 50000\n5. Rs. 50000 to Rs. 60000\n6. Above Rs. 50000\n7. Top 10 Laptops{bcolors.ENDC}\nYour Choice?\t'))
                    rangeUrl = 'https://www.91mobiles.com/'+ rangeOpts[theRange-1]
                    print(rangeUrl)
                    with PixelBar('Processing...', max=30) as bar:
                        for xys in range(30):
                            time.sleep(0.1)
                            bar.next()

                    scrapeRanges(rangeUrl)
                else:
                    print('Invalid Option')
                    input('Retry.......Enter Any Key.......')                    
                    os.system('cls')
            else:
                print('Invalid Option......')
                input('Retry.......Enter Any Key.......')
                os.system('cls')
        elif(device == '2'):
            mobile = input('What is the Device Brand/Name?')
            url = "https://www.91mobiles.com/search_page.php?q=" + mobile + "&type=all&utm_source=autosuggest"
            url = ' '.join(url.split())
            op = webdriver.ChromeOptions()
            op.add_argument('headless')
            driver = webdriver.Chrome('./chromedriver',options=op) 
            driver.get(url) 
            time.sleep(3)
            html = driver.page_source
            searchSoup =  bs(html, 'html.parser')
            texts = []
            links = []
            for i in searchSoup.findAll('ul',{'class':'product_listing'}):
                for j in i.findAll('li',{'class':'finder_snipet_wrap'}):
                    for k in j.findAll('div',{'class':'content_info'}):
                        for link in k.findAll('div',{'class':'pro_grid_name'}):
                            temp = link.a['href']
                            temp = temp.replace(' ','')
                            temp = temp.replace('\n','')
                            links.append('https://91mobiles.com'+temp)
                            tname = link.getText()
                            tname = tname.replace('  ','')
                            tname = tname.replace('\n','')
                            texts.append(tname)
            for i in range(0,len(texts)):
                print(str(i+1)+"\t: \t"+texts[i])
            number = 0
            number = input('Enter the number of the mobile you want to search?')
            searchUrl = links[int(number)-1]
            searchUrl = ' '.join(searchUrl.split())
            with PixelBar('Processing...', max=30) as bar:
                for xys in range(30):
                    time.sleep(0.1)
                    bar.next()

            fetchAndPrintData(searchUrl)
        else:
            input('Invalid Option.......press any key')
            os.system('cls')

if __name__ == '__main__':
    askOptions()
