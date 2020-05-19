import PySimpleGUI as sg
import time
import bs4
import requests

stock_amount = 6    #How many stocks do you want to track? The more stocks you track, the slower individual stocks will update

def parsePrice(sym):
    r = requests.get("https://web.tmxmoney.com/quote.php?qm_symbol=" + sym)     #Canadian stocks source (TSX)
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    try:
        price = soup.find("div", {"class":"labs-symbol"}).find("span", {"class":"price"}).find("span").text
        return price
    except:
        return "Cannot find"
 
sg.theme('DarkAmber')

def StockInfo(line_num):
    return [sg.Input(key=f"i{line_num}", font=('Helvetica', 20), size=(10, 0)), sg.Text("0.00", size=(6, 0), font=('Helvetica', 20), key=f"o{line_num}")]

window = sg.Window("TSX Stocks", [StockInfo(i) for i in range(0, stock_amount)])

while True:                              # Event Loop
    event, values = window.read(timeout=100)
    if event in (None, 'Quit'):          # if user closed the window using X or clicked Quit button
        break
   
    for x in range (stock_amount):
        if values[f'i{x}'] is not "":
            window[f'o{x}'].update(parsePrice(values[f'i{x}']))

window.close()