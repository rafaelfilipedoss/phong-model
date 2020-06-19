# Rafael Filipe (16415) - 5o ano - COMP 2020
from PIL import Image
import numpy as np
import math

def min_sol_quad_eq(a,b,c):
    if b*b - 4*a*c >= 0:
        if c < 0:
            return (-b + math.sqrt(b*b-4*a*c))/(2*a)
        else:
            if (-b - math.sqrt(b*b-4*a*c))/(2*a) >= 0:
                return (-b - math.sqrt(b*b-4*a*c))/(2*a)
            else:
                return "no solution"
    else:
        return "no solution"

def inner_prod(u,v):
    return np.inner(u,v)/(np.linalg.norm(u)*np.linalg.norm(v))

# im ---> imagem base
# camera ---> localizacao do observador
# light ---> localizacao da fonte de luz
# rad ---> raio da esfera
# scr_dist ---> distancia da tela ao centro da esfera
# lamb ---> 0 se for lambertiano e 1 caso contrario
# Kd, Ks, Ii, Iamb, n ---> variaveis do Modelo de Phong

def phong(name, lamb, Kd, Ks, Ii, Iamb, n, rad, scr_dist, camera, light):
    # gerando a imagem base
    d = rad*math.sqrt(pow(scr_dist,2)-pow(rad,2))/scr_dist # semelhança para definir um tamanho bom para a img base    
    im = Image.new('RGB', (int(d),int(d)), color = (0,0,0))

    # gerando a tela
    screen = []
    for i in range (-rad, rad + 1):
        for j in range (-rad, rad + 1):
            screen.append((i,j,scr_dist))

    for P in screen:
        A = [P[0] - camera[0], P[1] - camera[1], P[2] - camera[2]]

        # Descobrindo os pontos da esfera mais próximos ao observador
        # x=t*A[0], y=t*A[1], z=camera[2]+t*A[2], resolver x^2 + y^2 + z^2 = rad^2 e pegar a menor raiz
        a = pow(A[0],2) + pow(A[1],2) + pow(A[2],2)
        b = 2*A[2]*camera[2]
        c = pow(camera[2],2) - pow(rad,2)
        t = min_sol_quad_eq(a,b,c)

        if t != "no solution":
            N = [t*A[0], t*A[1], camera[2] + t*A[2]]
            V = [0-N[0], 0-N[1], camera[2]-N[2]]
            L = [light[0] - N[0], light[1] - N[1], light[2] - N[2]]

            # Calculo da reflexão da luz (soma de vetores e Lei dos Cossenos para achar R)
            k = 2*np.linalg.norm(L)*inner_prod(L,N)/np.linalg.norm(N)
            R = [k*N[0] - L[0], k*N[1] - L[1], k*N[2] - L[2]]
            
            # Determinando as coordenadas RGB com a influencia das intensidades
            # os maximos e minimos sao para manter os valores nos intervalos corretos -> <0 vira 0 e >255 vira 255
            # semelhante para os produtos internos -> <0 vira 0
            r = max(0, min(255, int((Kd[0]*max(inner_prod(N,L),0) + lamb*Ks*pow(max(inner_prod(R,V),0),n))*Ii[0] + Iamb[0])))
            g = max(0, min(255, int((Kd[1]*max(inner_prod(N,L),0) + lamb*Ks*pow(max(inner_prod(R,V),0),n))*Ii[1] + Iamb[1])))
            b = max(0, min(255, int((Kd[2]*max(inner_prod(N,L),0) + lamb*Ks*pow(max(inner_prod(R,V),0),n))*Ii[2] + Iamb[2])))

            im.putpixel((P[1]+int(d/2),P[0]+int(d/2)), (r,g,b))
    
    im.save(name)

# Gerando as imagens
Kd = [0.103849765,0.708920188,0.627230047]
Ks = 0.8
Ii = [255,255,255]
Iamb = [40,0,40]
n = 50
rad = 700
scr_dist = 800
camera = [0,0,900]

phong("image1.png", 0, Kd, Ks, Ii, Iamb, n, rad, scr_dist, camera, [0,1000,1100])
phong("image2.png", 1, Kd, Ks, Ii, Iamb, n, rad, scr_dist, camera, [500,500,900])
phong("image3.png", 1, Kd, Ks, Ii, Iamb, n, rad, scr_dist, camera, [1100,-1200,1000])
phong("image4.png", 1, Kd, Ks, Ii, Iamb, n, rad, scr_dist, camera, [-1100,0,1100])

