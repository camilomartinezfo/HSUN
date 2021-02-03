#!/usr/bin/env python3

from PIL import Image

def tramosImg(x):
    im_logo = Image.open("1-256x256.png") 
    im_fin = Image.open("2-256x256.png")
    imgorro = Image.open("gorroesc.png")
    img = Image.open("New.png")
    if x < 20:
        img.paste(im_logo,(20, 335))
    elif x < 100:
        img.paste(im_logo,(x,round(385 - (0.4375*x + 41.25))))
    elif x < 185:
        img.paste(im_logo,(x,round(385 - (1.058823*x - 20.88))))        
    elif x < 255:
        img.paste(im_logo,(x,round(385 - (0.7857*x + 29.6429))))        
    elif x < 405:
        img.paste(im_logo,(x,round(385 - (0.3667*x + 136.5))))        
    elif x < 445:
        img.paste(im_logo,(x,round(385 - (1.55*x - 342.75))))        
    elif x < 480:      
        img.paste(im_fin,(470, 25))
        img.paste(imgorro,(470,12))
    img.save('image.png')                           


def Rescala(x):
    return round(4.5*x + 20)


def logoGrafico(x):
    xvalue = Rescala(x)
    tramosImg(xvalue)
    Img = Image.open("image.png")
    ImgMod = Img.resize((190,140))
    ImgMod.save("image.png","png")


PAPA = float(input("Ingrese el PAPA en porcentaje: "))
logoGrafico(PAPA)