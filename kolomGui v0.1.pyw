# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 19:16:24 2018

@author: decro
"""
import tkinter as tk

def ingave(b,h,fc,n,m,di,dj,L):
    global B 
    global H 
    global fck 
    global Nd 
    global Md 
    global d1 
    global d2
    global d
    global x
    global Eps_yd
    global Es
    global fyd
    global fcd
    global As
    global Lengte
    global Lambda
    global Lambda_lim
    
   
    
    B = float(b)
    H = float(h)
    fck = float(fc)
    Nd = float(n)
    Md = float(m)
    d1 = float(di)
    d2 = float(dj)
    Lengte = float(L)
    Eps_yd = 0.002174
    Es = 200000.0
    fyd = 500/1.15
    fcd = 0.85*fck/1.5
    As = 0


    d = H - d2
    x = 2.33 * d



def bereken():
    
    # Berekenen symetrisch gewapende doorsnede
    
    global Md,Mrd
    global x
    global sigm_s1,sigm_s2
    global Nd,Nrd
    
    # Controleren van de minimale excentricteit
    #if Md <= Nd*0.02 :
    #       Md = Nd * 0.02

    #controleer slankheid
    e_2 = 0
    if is_slank(Lengte,H):
        print("kolom is slank")
        #schatting wapening
        As_est = max([(Nd*1000*1.1-(B*H*fcd))/(435-fcd),0.1*Nd*1000/435])
        print(As_est)
        #bepaal Kr
        omega = As_est*500/(B*H*fcd)
        print(omega)
        n_u=1+omega
        n_bal=0.4
        n = Nd*1000/(B*H*fcd)
        Kr=(n_u-n)/(n_u-n_bal)
        print(Kr)
        #bepaal K_cr
        Lambda = 3.46*Lengte/H
        phi_eff = 2
        Beta = 0.35+fck/200-Lambda/150
        K_cr = 1+Beta*phi_eff
        print(K_cr)
        #bepaal e_2

        e_2 = 0.1*(Kr*K_cr*435/(0.45*d*200000))*Lengte**2
        print(e_2)

    #bepaal Md
    e_i = max([Lengte/400,H/30,20])
    print("e_i")
    print(e_i)
    M01 = 0
    M02 = Md + Nd * e_i/1000
    M2 = e_2*Nd/1000
    M0e=0.6*M02+0.4*M01
    Md = max([M02,M0e+M2,M01+0.5*M2])
    print("Md")
    print(Md)
        
    while x>H:
            #bereken doorsnede in zone 3
            sigm_s1,sigm_s2 = bep_staalspanning_z3(x)
            As = bereken_As_from_N(x,Nd)
            Mrd = bereken_Mrd_from_As(x,As)
            if Mrd > 0.98 * Md and Mrd < 1.02*Md:
                x = 0
            else:
                x = x-1
        
    while x>d2:
            #bereken doorsnede in zone 2
            sigm_s1,sigm_s2 = bep_staalspanning_z2(x)
            As = bereken_As_from_M(x,Md)
            Nrd = bereken_Nrd_from_As(x,As)
            if Nrd > 0.98 * Nd and Nrd < 1.02*Nd:
                k = x
                x = 0
            else:
                x = x-1

    
    #controleer minimum wapening
    if is_slank(Lengte,H):
        As_comm = "De kolom is slank! As Berekend"
    else:
        As_comm = "As Berekend"
            
    if As < 0.0010*B*H:
        As = 0.0010*B*H
        As_comm = "As 0.001 x Ac (formule 9.12N)"  
    if As < 0.05*Nd*1000/fyd:
        As = 0.05*Nd*1000/fyd
        As_comm = "As 0.05 x Nd (formule 9.12N)"
    #controleer max wapening
    if As > 0.02*B*H:
        As_comm = "FOUT - As.max = {:01.0f} mm²".format(0.02*B*H)
    # print(k)
    return '{:01.0f} mm² => {}'.format(As,As_comm)

def bep_staalspanning_z3(x):
    #bepaal staalrek_z3
    Eps_2 = 0.002*(x-d2)/(x-3*H/7)
    Eps_1 = 0.002*(x-d)/(x-3*H/7)
    #bepaal staalspanning_z3
    if Eps_2 >= Eps_yd:
        sigm_s2 = fyd
    else:
        sigm_s2 = Es * Eps_2
    
    if Eps_1 >= Eps_yd:
        sigm_s1 = fyd
    else:
        sigm_s1 = Es * Eps_1
    return sigm_s1,sigm_s2

def bep_staalspanning_z2(x2):
    #bepaal staalrek_z3
    Eps_2 = 0.0035*(x2-d2)/x2
    Eps_1 = 0.0035*(x2-d)/x2
    #print(Eps_1)
    #bepaal staalspanning_z3
    if Eps_2 >= Eps_yd:
        sigm_s2 = fyd
    else:
        sigm_s2 = Es * Eps_2
    
    if Eps_1 <= -Eps_yd:
        sigm_s1 = -fyd
    else:
        sigm_s1 = Es * Eps_1
    return sigm_s1,sigm_s2

def bereken_As_from_N(x3,N):
    As = (N*1000-(B*H*fcd*(1.0-0.1905*(4*H/7)**2/(x3-3*H/7)**2)))/(sigm_s1+sigm_s2)
    return As

def bereken_Mrd_from_As (x3,As):
    M = ((B*H*fcd*(0.1905*(4*H/7)**2)/(x3-3*H/7)**2)*(6*H/7-H/2)-As * sigm_s1*(d-H/2)+As * sigm_s2*(H/2-d2))/1000000
    return M
    
def bereken_As_from_M(x2,M):
    As = (M * 1000000-B*x2*fcd*0.81*(H/2-0.416*x2))/((-sigm_s1+sigm_s2)*(H/2-d2))
    return As

def bereken_Nrd_from_As(x2,As):
    N = ( B*x2*fcd*0.81 + As*(sigm_s1+sigm_s2))/1000
    return N

def Max(a,b):
    if a>=b:
        return a
    else:
        return b
def Min(a,b):
    if a<=b:
        return a
    else:
        return b

#2de orde berekening

def is_slank(l_0,h):
    C = 1.7
    n = Nd*1000/(B*H*fcd)
    Lambda = 3.46*l_0/h
    Lambda_lim = 15.4*C/(n**0.5)
    print(Lambda)
    print(Lambda_lim)
    return Lambda >= Lambda_lim
    

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
                
        self.lbl_B = tk.Label(self,text = "Breedte")
        self.txt_B = tk.Entry(self)
        self.lbl_H = tk.Label(self,text = "Hoogte")
        self.txt_H = tk.Entry(self)
        self.lbl_L = tk.Label(self,text = "Lengte")
        self.txt_L = tk.Entry(self)
        self.lbl_d1 = tk.Label(self,text = "d1")
        self.txt_d1 = tk.Entry(self)
        self.lbl_Nd = tk.Label(self,text = "Nd")
        self.txt_Nd = tk.Entry(self)
        self.lbl_Md = tk.Label(self,text = "Md")
        self.txt_Md = tk.Entry(self)
        self.lbl_fck = tk.Label(self,text = "fck")
        self.txt_fck = tk.Entry(self)
        self.btn = tk.Button(self,text = "Bereken As",command = self.Solve)
        self.lbl_resultaat = tk.Label(self,text = "                        ")
        
        self.lbl_B.pack()
        self.txt_B.pack()
        self.lbl_H.pack()
        self.txt_H.pack()
        self.lbl_L.pack()
        self.txt_L.pack()
        self.lbl_d1.pack()
        self.txt_d1.pack()
        self.lbl_Nd.pack()
        self.txt_Nd.pack()
        self.lbl_Md.pack()
        self.txt_Md.pack()
        self.lbl_fck.pack()
        self.txt_fck.pack()
        self.btn.pack(padx=120, pady=30)
        self.lbl_resultaat.pack(padx=120, pady=30)

    def Solve(self):
        ingave(self.txt_B.get(),self.txt_H.get(),self.txt_fck.get(),self.txt_Nd.get(),self.txt_Md.get(),self.txt_d1.get(),self.txt_d1.get(),self.txt_L.get())
        As = bereken()
        self.lbl_resultaat.config(text=As)
        
        
if __name__=="__main__":
    App=App()
    App.title("Symmetrisch gewapende kolom v0.1")
    App.geometry("500x500+10+10")
    #App.iconbitmap('kolom.ico')
    App.mainloop()
    
#ingave(300,500,30,1215,313,45,45)
#bereken()
