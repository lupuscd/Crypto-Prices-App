from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from io import BytesIO
import requests
import cgapi

def mouse_wheel(event):
    if event.delta > 0 or event.num == 4:
        scroll = -1
    elif event.delta < 0 or event.num == 5:
        scroll = 1

    my_canvas.yview_scroll(scroll, "units")

def pressed_enter(event):
    click()
    window.destroy()
    coin_search()

def click():
    click.searched_coin = search_box.search_b.get()

def update_button():
    up_button = Button(window, text='Update Prices', bg='cyan', fg='black', font='comicsans 10 bold',
                    activebackground='red', command=lambda:[window.destroy(),coin_show()])
    up_button.grid(row=1, column=5, sticky=E)

def search_box():
    search_box.search_b = Entry(window, width=25, bg='cyan', fg='black', font='comicsans 10 bold')
    search_box.search_b.grid(row=1, column=3, sticky=W)
    search_button = Button(window, text='Search', bg='cyan', fg='black', font='comicsans 10 bold',
                    activebackground='red', command=lambda:[click(),window.destroy(),coin_search()])
    search_button.grid(row=1, column=2, sticky=E)

def new_window():

    global window
    #New frame
    window = Frame(my_canvas)
    #Add the frame to a window in the canvas
    my_canvas.create_window((0,0), window=window, anchor='nw')

    window.configure(bg='black')
    window.columnconfigure(1, minsize=150)
    window.columnconfigure(2, minsize=150)
    window.columnconfigure(3, minsize=350)
    window.columnconfigure(5, minsize=250)
    window.columnconfigure(4, minsize=50)

    #header
    header = Label(window, text='Crypto Prices', bg='black', fg='cyan', font='comicsans 18 bold')
    header.grid(row=0, column=0, sticky=W)

    header2 = Label(window, text='Powered by CoinGecko', bg='black', fg='cyan', font='comicsans 10 bold')
    header2.grid(row=0, column=5, sticky=E)

    #header columns
    rankh = Label(window, text='Rank', bg='black', fg='cyan', font='comicsans 16 bold')
    rankh.grid(row=2, column=0, sticky=W+E+N+S)

    coinh = Label(window, text='Coin', bg='black', fg='cyan', font='comicsans 16 bold')
    coinh.grid(row=2, column=1, sticky=W, padx=1)

    symbolh = Label(window, text='Symbol', bg='black', fg='cyan', font='comicsans 16 bold')
    symbolh.grid(row=2, column=2, sticky=W)

    priceh = Label(window, text='Price EUR|USD', bg='black', fg='cyan', font='comicsans 16 bold')
    priceh.grid(row=2, column=3, sticky=W+E+N+S)

    changeh = Label(window, text='24h Change EUR|USD', bg='black', fg='cyan', font='comicsans 16 bold')
    changeh.grid(row=2, column=5, sticky=W)

def coin_search():
    
    new_window()
    update_button()
    search_box()

    move_on_to_usd = 0

    for crypto in coin_show.js_list_eur:

        if crypto['name'].lower() == click.searched_coin.lower() or crypto['symbol'].lower() == click.searched_coin.lower():

            crypto_position = coin_show.js_list_eur.index(crypto)

            rank = Label(window, text=str(crypto['market_cap_rank']), bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
            rank.grid(row=3, column=0, sticky=W+E+N+S)

            name = Label(window, text=crypto['name'], bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
            name.grid(row=3, column=1, sticky=W)

            symbol = Label(window, text=crypto['symbol'].upper(), bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
            symbol.grid(row=3, column=2, sticky=W)

            #Image manipulation
            img_url = crypto['image']
            #img_url.replace('large','small')
            get_img = requests.get(img_url)
            img_data = get_img.content
            img_byte = Image.open(BytesIO(img_data))
            img = img_byte.resize((25,25), Image.ANTIALIAS)
            img_final = ImageTk.PhotoImage(img)
            panel = Label(window, image = img_final, bg='black')
            panel.image = img_final #Need to keep separate reference in order to show
            panel.grid(row=3, column=2, sticky=N)

            price_change_number = crypto.get('price_change_percentage_24h', 0)
            if price_change_number == None:
                price_change_number = 0
            elif price_change_number >= 0:
                price_eur = Label(window, text=format(float(crypto['current_price']),'.4f')+' €', bg='black', fg='green2', font='comicsans 12 bold')
                price_change_24h = Label(window, text=str(price_change_number)+' %', bg='black', fg='green2', font='comicsans 12 bold')
            else:
                price_eur = Label(window, text=format(float(crypto['current_price']),'.4f')+' €', bg='black', fg='red', font='comicsans 12 bold')
                price_change_24h = Label(window, text=str(price_change_number)+' %', bg='black', fg='red', font='comicsans 12 bold')
            price_eur.grid(row=3, column=3, sticky=W)
            price_change_24h.grid(row=3, column=5, sticky=W)
            move_on_to_usd = 1
            break

    else:
        not_found_msg = Label(window, text='Search Item Not Found Please Repeat Your Search', bg='black', fg='red', font='comicsans 12 bold')
        not_found_msg.grid(row=3, column=0, sticky=W+E+N+S)

    if move_on_to_usd == 1:

        crypto_usd = coin_show.js_list_usd[crypto_position]

        divider = Label(window, text='|', bg='black', fg='green2', font='comicsans 12 bold')
        divider.grid(row=3, column=3, sticky=N)
        divider_2 = Label(window, text='|', bg='black', fg='green2', font='comicsans 12 bold')
        divider_2.grid(row=3, column=5, sticky=N)
        price_change_number_usd = crypto_usd.get('price_change_percentage_24h', 0)
        if price_change_number_usd == None:
            price_change_number_usd = 0
        elif price_change_number_usd >= 0:
            price_usd = Label(window, text=format(float(crypto_usd['current_price']),'.4f')+' $', bg='black', fg='green2', font='comicsans 12 bold')
            price_change_24h_usd = Label(window, text=str(price_change_number_usd)+' %', bg='black', fg='green2', font='comicsans 12 bold')
        else:
            price_usd = Label(window, text=format(float(crypto_usd['current_price']),'.4f')+' $', bg='black', fg='red', font='comicsans 12 bold')
            price_change_24h_usd = Label(window, text=str(price_change_number_usd)+' %', bg='black', fg='red', font='comicsans 12 bold')
        price_usd.grid(row=3, column=3, sticky=E)
        price_change_24h_usd.grid(row=3, column=5, sticky=E)

def coin_show():

    new_window()
    update_button()
    search_box()

    list_eur = ''
    list_usd = ''
    list_eur = cgapi.cryptolist_eur()
    list_usd = cgapi.cryptolist_usd()
    coin_show.js_list_eur = ''
    coin_show.js_list_eur = list_eur
    coin_show.js_list_usd = ''
    coin_show.js_list_usd = list_usd

    crypto_row = 3
    for crypto in list_eur:

        rank = Label(window, text=str(crypto['market_cap_rank']), bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
        rank.grid(row=crypto_row, column=0, sticky=W+E+N+S)

        name = Label(window, text=crypto['name'], bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
        name.grid(row=crypto_row, column=1, sticky=W)

        symbol = Label(window, text=crypto['symbol'].upper(), bg='black', fg='RoyalBlue1', font='comicsans 12 bold')
        symbol.grid(row=crypto_row, column=2, sticky=W)
        
        #Image manipulation
        img_url = crypto['image']
        #img_url.replace('large','small')
        get_img = requests.get(img_url)
        img_data = get_img.content
        img_byte = Image.open(BytesIO(img_data))
        img = img_byte.resize((25,25), Image.ANTIALIAS)
        img_final = ImageTk.PhotoImage(img)
        panel = Label(window, image = img_final, bg='black')
        panel.image = img_final #Need to keep separate reference in order to show
        panel.grid(row=crypto_row, column=2, sticky=N)
        
        price_change_number = crypto.get('price_change_percentage_24h', 0)
        if price_change_number == None:
            price_change_number = 0
        elif price_change_number >= 0:
            price_eur = Label(window, text=format(float(crypto['current_price']),'.4f')+' €', bg='black', fg='green2', font='comicsans 12 bold')
            price_change_24h = Label(window, text=str(price_change_number)+' %', bg='black', fg='green2', font='comicsans 12 bold')
        else:
            price_eur = Label(window, text=format(float(crypto['current_price']),'.4f')+' €', bg='black', fg='red', font='comicsans 12 bold')
            price_change_24h = Label(window, text=str(price_change_number)+' %', bg='black', fg='red', font='comicsans 12 bold')
        price_eur.grid(row=crypto_row, column=3, sticky=W)
        price_change_24h.grid(row=crypto_row, column=5, sticky=W)

        crypto_row += 1

    crypto_row = 3
    for crypto_usd in list_usd:

        divider = Label(window, text='|', bg='black', fg='green2', font='comicsans 12 bold')
        divider.grid(row=crypto_row, column=3, sticky=N)
        divider_2 = Label(window, text='|', bg='black', fg='green2', font='comicsans 12 bold')
        divider_2.grid(row=crypto_row, column=5, sticky=N)
        price_change_number_usd = crypto_usd.get('price_change_percentage_24h', 0)
        if price_change_number_usd == None:
            price_change_number_usd = 0
        elif price_change_number_usd >= 0:
            price_usd = Label(window, text=format(float(crypto_usd['current_price']),'.4f')+' $', bg='black', fg='green2', font='comicsans 12 bold')
            price_change_24h_usd = Label(window, text=str(price_change_number_usd)+' %', bg='black', fg='green2', font='comicsans 12 bold')
        else:
            price_usd = Label(window, text=format(float(crypto_usd['current_price']),'.4f')+' $', bg='black', fg='red', font='comicsans 12 bold')
            price_change_24h_usd = Label(window, text=str(price_change_number_usd)+' %', bg='black', fg='red', font='comicsans 12 bold')
        price_usd.grid(row=crypto_row, column=3, sticky=E)
        price_change_24h_usd.grid(row=crypto_row, column=5, sticky=E)

        crypto_row += 1  

root = Tk()

root.title('Crypto Live Prices')
root.iconbitmap(r'C:\Main\Programing\Projects\Crypto_Prices_App\btc.ico')
root.minsize(1024,800)
root.configure(bg='black')

#Main Frame 
main_frame = Frame(root)
main_frame.pack(fill=BOTH,expand=True)

#####SCROLLBAR######
#Create canvas
my_canvas = Canvas(main_frame, highlightthickness=0) #highlightthickness=0 svinei ta oria gyrw apo to canvas
my_canvas.pack(side=LEFT, fill=BOTH, expand=True)
my_canvas.configure(bg='black')

#Add scrollbar to canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

#Configure canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all'))) #e is there cause we have 1 input (event)

my_canvas.bind_all('<MouseWheel>', mouse_wheel)
#####SCROLLBAR#####

#Enter button searches
my_canvas.bind_all('<Return>', pressed_enter) #can use lambda e:[click(),window.destroy(),coin_search()]

coin_show()

root.mainloop()
