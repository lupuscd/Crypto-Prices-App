from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from io import BytesIO
import requests
from coin_api import *

def scrollframe():

    #Scrollable frame
    global scrollable_frame
    scrollable_frame = Frame(my_canvas)
    scrollable_frame.configure(bg='black')
    scrollable_frame.columnconfigure(2, minsize=150)
    #scrollable_frame.columnconfigure(3, minsize=50)
    #scrollable_frame.columnconfigure(4, minsize=50)
    my_canvas.create_window((0,0), window=scrollable_frame, anchor=N+W)

    #header
    header = Label(scrollable_frame, text='Crypto Prices', bg='black', fg='cyan', font='comicsans 18 bold')
    header.grid(row=0, column=0, sticky=W)

    header2 = Label(scrollable_frame, text='Powered by CoinGecko', bg='black', fg='cyan', font='comicsans 10 bold')
    header2.grid(row=0, column=4, sticky=E)

    #header columns
    rankh = Label(scrollable_frame, text='Rank', bg='black', fg='cyan', font='comicsans 16 bold')
    rankh.grid(row=2, column=0, sticky=W+N+S+E)

    coinh = Label(scrollable_frame, text='Coin', bg='black', fg='cyan', font='comicsans 16 bold')
    coinh.grid(row=2, column=1, sticky=W, padx=1)

    symbolh = Label(scrollable_frame, text='Symbol', bg='black', fg='cyan', font='comicsans 16 bold')
    symbolh.grid(row=2, column=2, sticky=W)

    priceh = Label(scrollable_frame, text='Price', bg='black', fg='cyan', font='comicsans 16 bold')
    priceh.grid(row=2, column=3, sticky=W)

    changeh = Label(scrollable_frame, text='24h Change', bg='black', fg='cyan', font='comicsans 16 bold')
    changeh.grid(row=2, column=4, sticky=W)

    update_button()
    search_box()
    #currency_button()

def update_button():

    up_button = Button(scrollable_frame, text='Update Prices', bg='cyan', fg='black', font='comicsans 10 bold',
                    activebackground='red', command=lambda:[scrollable_frame.destroy(),coin_show_eur()])
    up_button.grid(row=1, column=4, sticky=E)

def search_box():

    search_b = Entry(scrollable_frame, width=25, bg='cyan', fg='black', font='comicsans 10 bold')
    search_b.grid(row=1, column=3, sticky=W)
    search_button_command = lambda:[searched_coin:=search_b.get(),scrollable_frame.destroy(),coin_search(searched_coin)]
    search_button = Button(scrollable_frame, text='Search', bg='cyan', fg='black', font='comicsans 10 bold',
                    activebackground='red', command= search_button_command)#inside lambda use := for equal
    search_button.grid(row=1, column=2, sticky=E)
    my_canvas.bind_all('<Return>', lambda e:[searched_coin:=search_b.get(),scrollable_frame.destroy(),coin_search(searched_coin)])

def coin_show_eur():

    crypto_row = 3

    for crypto in coin_price_in_eur:

        rank = Label(scrollable_frame, text=str(crypto['market_cap_rank']), bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
        rank.grid(row=crypto_row, column=0, sticky=W+N+S+E)

        name = Label(scrollable_frame, text=crypto['name'], bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
        name.grid(row=crypto_row, column=1, sticky=W)

        symbol = Label(scrollable_frame, text=crypto['symbol'].upper(), bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
        symbol.grid(row=crypto_row, column=2, sticky=W+E+N+S)
        
        #Image manipulation
        img_url = crypto['image']
        #img_url.replace('large','small')
        get_img = requests.get(img_url)
        img_data = get_img.content
        img_byte = Image.open(BytesIO(img_data))
        img = img_byte.resize((25,25), Image.ANTIALIAS)
        img_final = ImageTk.PhotoImage(img)
        panel = Label(scrollable_frame, image = img_final, bg='black')
        panel.image = img_final #Need to keep separate reference in order to show
        panel.grid(row=crypto_row, column=2, sticky=W)
        
        price_change_number = crypto.get('price_change_percentage_24h', 0)
        if price_change_number == None:
            price_change_number = 0
        elif price_change_number >= 0:
            price_eur = Label(scrollable_frame, text=format(float(crypto['current_price']),'.4f')+' €', bg='black', fg='green2', font='comicsans 12 bold')
            price_change_24h = Label(scrollable_frame, text=str(price_change_number)+' %', bg='black', fg='green2', font='comicsans 12 bold')
        else:
            price_eur = Label(scrollable_frame, text=format(float(crypto['current_price']),'.4f')+' €', bg='black', fg='red', font='comicsans 12 bold')
            price_change_24h = Label(scrollable_frame, text=str(price_change_number)+' %', bg='black', fg='red', font='comicsans 12 bold')
        price_eur.grid(row=crypto_row, column=3, sticky=W)
        price_change_24h.grid(row=crypto_row, column=4, sticky=W)

        crypto_row += 1 

def coin_show_usd():

    coin_price_in_usd = cryptolist_usd()
    scrollable_frame.withdraw()
    scrollframe()
    crypto_row = 3

    for crypto in coin_price_in_usd:

        rank = Label(scrollable_frame, text=str(crypto['market_cap_rank']), bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
        rank.grid(row=crypto_row, column=0, sticky=W+E+N+S)

        name = Label(scrollable_frame, text=crypto['name'], bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
        name.grid(row=crypto_row, column=1, sticky=W+E+N+S)

        symbol = Label(scrollable_frame, text=crypto['symbol'].upper(), bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
        symbol.grid(row=crypto_row, column=2, sticky=W+E+N+S)
        
        #Image manipulation
        img_url = crypto['image']
        #img_url.replace('large','small')
        get_img = requests.get(img_url)
        img_data = get_img.content
        img_byte = Image.open(BytesIO(img_data))
        img = img_byte.resize((25,25), Image.ANTIALIAS)
        img_final = ImageTk.PhotoImage(img)
        panel = Label(scrollable_frame, image = img_final, bg='black')
        panel.image = img_final #Need to keep separate reference in order to show
        panel.grid(row=crypto_row, column=2, sticky=W)

        price_change_number_usd = crypto.get('price_change_percentage_24h', 0)
        if price_change_number_usd == None:
            price_change_number_usd = 0
        elif price_change_number_usd >= 0:
            price_usd = Label(scrollable_frame, text=format(float(crypto['current_price']),'.4f')+' $', bg='black', fg='green2', font='comicsans 12 bold')
            price_change_24h_usd = Label(scrollable_frame, text=str(price_change_number_usd)+' %', bg='black', fg='green2', font='comicsans 12 bold')
        else:
            price_usd = Label(scrollable_frame, text=format(float(crypto['current_price']),'.4f')+' $', bg='black', fg='red', font='comicsans 12 bold')
            price_change_24h_usd = Label(scrollable_frame, text=str(price_change_number_usd)+' %', bg='black', fg='red', font='comicsans 12 bold')
        price_usd.grid(row=crypto_row, column=3, sticky=W)
        price_change_24h_usd.grid(row=crypto_row, column=4, sticky=W)

        crypto_row += 1

def mouse_wheel(event):
    if event.delta > 0:
        scroll = -1
    elif event.delta < 0:
        scroll = 1

    my_canvas.yview_scroll(scroll, "units")    

def coin_search(searched_coin):

    scrollframe()

    move_on_to_usd = 0

    for crypto in coin_price_in_eur:

        if crypto['name'].lower() == searched_coin or crypto['symbol'].lower() == searched_coin:

            crypto_position = coin_price_in_eur.index(crypto)

            rank = Label(scrollable_frame, text=str(crypto['market_cap_rank']), bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
            rank.grid(row=3, column=0, sticky=W+E+N+S)

            name = Label(scrollable_frame, text=crypto['name'], bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
            name.grid(row=3, column=1, sticky=W)

            symbol = Label(scrollable_frame, text=crypto['symbol'].upper(), bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
            symbol.grid(row=3, column=2, sticky=W)

            #Image manipulation
            img_url = crypto['image']
            #img_url.replace('large','small')
            get_img = requests.get(img_url)
            img_data = get_img.content
            img_byte = Image.open(BytesIO(img_data))
            img = img_byte.resize((25,25), Image.ANTIALIAS)
            img_final = ImageTk.PhotoImage(img)
            panel = Label(scrollable_frame, image = img_final, bg='black')
            panel.image = img_final #Need to keep separate reference in order to show
            panel.grid(row=3, column=2, sticky=N)

            price_change_number = crypto.get('price_change_percentage_24h', 0)
            if price_change_number == None:
                price_change_number = 0
            elif price_change_number >= 0:
                price_eur = Label(scrollable_frame, text=format(float(crypto['current_price']),'.4f')+' €', bg='black', fg='green2', font='comicsans 12 bold')
                price_change_24h = Label(scrollable_frame, text=str(price_change_number)+' %', bg='black', fg='green2', font='comicsans 12 bold')
            else:
                price_eur = Label(scrollable_frame, text=format(float(crypto['current_price']),'.4f')+' €', bg='black', fg='red', font='comicsans 12 bold')
                price_change_24h = Label(scrollable_frame, text=str(price_change_number)+' %', bg='black', fg='red', font='comicsans 12 bold')
            price_eur.grid(row=3, column=3, sticky=W)
            price_change_24h.grid(row=3, column=5, sticky=W)
            move_on_to_usd = 1
            break

    else:
        not_found_msg = Label(scrollable_frame, text='Search Item Not Found Please Repeat Your Search', bg='black', fg='red', font='comicsans 12 bold')
        not_found_msg.grid(row=3, column=0, sticky=W+E+N+S)

    if move_on_to_usd == 1:

        crypto_usd = coin_price_in_usd[crypto_position]

        divider = Label(scrollable_frame, text='|', bg='black', fg='green2', font='comicsans 12 bold')
        divider.grid(row=3, column=3, sticky=N)
        divider_2 = Label(scrollable_frame, text='|', bg='black', fg='green2', font='comicsans 12 bold')
        divider_2.grid(row=3, column=5, sticky=N)
        price_change_number_usd = crypto_usd.get('price_change_percentage_24h', 0)
        if price_change_number_usd == None:
            price_change_number_usd = 0
        elif price_change_number_usd >= 0:
            price_usd = Label(scrollable_frame, text=format(float(crypto_usd['current_price']),'.4f')+' $', bg='black', fg='green2', font='comicsans 12 bold')
            price_change_24h_usd = Label(scrollable_frame, text=str(price_change_number_usd)+' %', bg='black', fg='green2', font='comicsans 12 bold')
        else:
            price_usd = Label(scrollable_frame, text=format(float(crypto_usd['current_price']),'.4f')+' $', bg='black', fg='red', font='comicsans 12 bold')
            price_change_24h_usd = Label(scrollable_frame, text=str(price_change_number_usd)+' %', bg='black', fg='red', font='comicsans 12 bold')
        price_usd.grid(row=3, column=3, sticky=E)
        price_change_24h_usd.grid(row=3, column=5, sticky=E)

def currency_button():
    eur_button = Button(scrollable_frame, text='EUR', bg='yellow', fg='black', font='comicsans 10 bold',
                    activebackground='red', command=coin_show_eur())
    eur_button.grid(row=0, column=1, sticky=N)

    usd_button = Button(scrollable_frame, text='USD', bg='yellow', fg='black', font='comicsans 10 bold',
                    activebackground='red', command=coin_show_usd())
    usd_button.grid(row=0, column=1, sticky=N+E)

coin_price_in_eur = cryptolist_eur()

#Main Window
root = Tk()
root.title('Crypto Live Prices')
root.iconbitmap(r'C:\Main\Programing\Projects\Crypto_Prices_App\btc.ico')
root.minsize(1024,800)
root.configure(bg='black')

#Main Frame 
main_frame = Frame(root)
main_frame.pack(fill=BOTH,expand=True)

#Create canvas
my_canvas = Canvas(main_frame, highlightthickness=0) #highlightthickness=0 svinei ta oria gyrw apo to canvas
my_canvas.configure(bg='black')
my_canvas.pack(side=LEFT, fill=BOTH, expand=True)

#Scrollbar
my_scrollbar = Scrollbar(main_frame, orient='vertical', command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)
my_canvas.config(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all'))) #e is there cause we have 1 input (event)
my_canvas.bind_all('<MouseWheel>', mouse_wheel)

scrollframe()
coin_show_eur()
root.mainloop()
