from tkinter import mainloop,Tk,Label,Button,filedialog
from pathlib import Path


def selam():
    select = filedialog.askopenfilenames()
    print(select)


win = Tk()
win.title("Scorpion") #pencerenin başlığını belirliyor
win.geometry("500x500") #pencerenin boyunu ayarlyıor
win.resizable(False, False) #pencereyi yeniden boyutlandırmayı iptal ediyor ilk parametre en diğeri boy
win.wm_attributes("-topmost", 1) #ilk iki parametre saydamlık veriyor diğer iki paramtre en önde kalmasını sağlıyor
Label(text="Selam", fg="green",cursor="spider").pack() #label ile bir label oluşturup pack() ile windowa paketliyorz
Button(text="Select Image", command=selam).pack()
mainloop()
