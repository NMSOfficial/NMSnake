from tkinter import *
import random 

genislik = 500
yukseklik = 500
hiz = 200
alanbuyukluk = 20
baslangıcbuyukluk = 2
fener = "#FFFF00"  # Sarı
bahce = "#000080"  # Lacivert
yem_rengi = "#FFFFFF"
arkaplan = "#000000"

class Yilan: 
    def __init__(self): 
        self.baslangıcbuyukluk = baslangıcbuyukluk 
        self.coordinates = [] 
        self.squares = [] 

        for i in range(0, baslangıcbuyukluk): 
            self.coordinates.append([0, 0]) 

        for x, y in self.coordinates: 
            renk = fener if len(self.squares) % 2 == 0 else bahce
            kare = canvas.create_rectangle(x, y, x + alanbuyukluk, y + alanbuyukluk, fill=renk, tag="yilan") 
            self.squares.append(kare) 

class Yem: 
    def __init__(self): 
        x = random.randint(0, (genislik // alanbuyukluk) - 1) * alanbuyukluk  
        y = random.randint(0, (yukseklik // alanbuyukluk) - 1) * alanbuyukluk  

        self.coordinates = [x, y] 
        canvas.create_oval(x, y, x + alanbuyukluk, y + alanbuyukluk, fill=yem_rengi, tag="yem") 

def sonraki_hamle(yilan, yem): 
    x, y = yilan.coordinates[0] 

    if yon == "yukarı": 
        y -= alanbuyukluk 
    elif yon == "aşağı": 
        y += alanbuyukluk 
    elif yon == "sol": 
        x -= alanbuyukluk 
    elif yon == "sağ": 
        x += alanbuyukluk 

    yilan.coordinates.insert(0, (x, y)) 

    renk = fener if len(yilan.squares) % 2 == 0 else bahce
    kare = canvas.create_rectangle(x, y, x + alanbuyukluk, y + alanbuyukluk, fill=renk) 

    yilan.squares.insert(0, kare) 

    if x == yem.coordinates[0] and y == yem.coordinates[1]: 
        global puan 
        puan += 1
        etiket.config(text="Puan:{}".format(puan)) 
        canvas.delete("yem") 
        yem = Yem() 
    else: 
        del yilan.coordinates[-1] 
        canvas.delete(yilan.squares[-1]) 
        del yilan.squares[-1] 

    if çarpışma_kontrol(yilan): 
        oyun_bitti() 
    else: 
        window.after(hiz, sonraki_hamle, yilan, yem) 

def yön_değiştir(yeni_yön): 
    global yon 

    if yeni_yön == 'sol': 
        if yon != 'sağ': 
            yon = yeni_yön 
    elif yeni_yön == 'sağ': 
        if yon != 'sol': 
            yon = yeni_yön 
    elif yeni_yön == 'yukarı': 
        if yon != 'aşağı': 
            yon = yeni_yön 
    elif yeni_yön == 'aşağı': 
        if yon != 'yukarı': 
            yon = yeni_yön 

def çarpışma_kontrol(yilan): 
    x, y = yilan.coordinates[0] 

    if x < 0 or x >= genislik: 
        return True
    elif y < 0 or y >= yukseklik: 
        return True

    for beden_parçası in yilan.coordinates[1:]: 
        if x == beden_parçası[0] and y == beden_parçası[1]: 
            return True

    return False

def oyun_bitti(): 
    canvas.delete(ALL) 
    canvas.create_text(canvas.winfo_width()/2, 
                       canvas.winfo_height()/2, 
                       font=('SF Pro Display', 70), 
                       text="OYUN BİTTİ", fill="red", 
                       tag="oyunbitti") 

window = Tk() 
window.title("Yılan Oyunu") 

puan = 0
yon = 'aşağı'

etiket = Label(window, text="Puan:{}".format(puan), font=('SF Pro Display', 20)) 
etiket.pack() 

canvas = Canvas(window, bg=arkaplan, height=yukseklik, width=genislik)  # 'height' ve 'width' kullanıldı
canvas.pack() 

window.update() 

window_genislik = window.winfo_width() 
window_yukseklik = window.winfo_height() 
screen_genislik = window.winfo_screenwidth() 
screen_yukseklik = window.winfo_screenheight() 

x = int((screen_genislik/2) - (window_genislik/2)) 
y = int((screen_yukseklik/2) - (window_yukseklik/2)) 

window.geometry(f"{window_genislik}x{window_yukseklik}+{x}+{y}") 

window.bind('<Left>', lambda event: yön_değiştir('sol')) 
window.bind('<Right>', lambda event: yön_değiştir('sağ')) 
window.bind('<Up>', lambda event: yön_değiştir('yukarı')) 
window.bind('<Down>', lambda event: yön_değiştir('aşağı')) 

yilan = Yilan() 
yem = Yem() 

sonraki_hamle(yilan, yem) 

window.mainloop() 
