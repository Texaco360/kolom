import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt

def solve_beam(l1,l2,q1,q2):

    l = l1 + l2 #total length
    Mx = sp.symbols('Mx') #create symbol Mx

    #calculate Mx
    Mx = sp.solveset(Mx*l1/3+q1*l1**3/24+Mx*l2/3+q2*l2**3/24).args[0]

    #solve equilibruim equations
    Va, Vb1, Vb2, Vc = sp.symbols('Va Vb1 Vb2 Vc')

    Va, Vb1 = sp.linsolve([Va+Vb1-q1*l1, Vb1*l1 + Mx-(q1*l1**2)/2],(Va, Vb1)).args[0]
    Vc, Vb2 = sp.linsolve([Vb2+Vc-q2*l2, Vb2 *l2 + Mx -(q2*l2**2)/2],(Vc,Vb2)).args[0]

    Vb=Vb1+Vb2

    x1 = np.arange(0,l1+0.1,0.1) #create axis x1
    x2 = np.arange(0, l2+0.1,0.1) #create axis x2

    beam1=pd.DataFrame({"x":x1})  #create a dataframe for the first span
    beam2=pd.DataFrame({"x":x2})  #create a dataframe for the second span
    
  # Convert sympy expressions to floats for compatibility with pandas/numpy
    Va = float(Va)
    Vb2 = float(Vb2)
    Mx = float(Mx)

    beam1["M"] = Va*beam1.x-(q1*beam1.x**2)/2 #calculate M and store it
    beam2["M"] = Mx-(q2*beam2.x**2)/2 + Vb2 * beam2.x #calculate M ans store it

    beam1["V"] = Va-q1*beam1.x #calculate V and store it
    beam2["V"] = Vb2-q2*beam2.x #calculate V and store it

    beam2.x= beam2.x + l1 #re-assign for the seconnd span
    beam = pd.concat([beam1,beam2]) #concatenate the two dataframes

    return(beam)

header = pd.MultiIndex.from_tuples([("combo 1", "M"), ("combo 1","V"),("combo 2", "M"),("combo 2","V")])

combos = pd.DataFrame(columns=header)

beam_result1 = solve_beam(6.0, 6.0, -1.140, 0.13)
beam_result2 = solve_beam(6.0, 6.0, -1.140, -1.140)
combos["x"] = beam_result1["x"]
combos[("combo 1", "M")] = beam_result1["M"]
combos[("combo 1", "V")] = beam_result1["V"]
combos[("combo 2", "M")] = beam_result2["M"]
combos[("combo 2", "V")] = beam_result2["V"]

combos.set_index("x", inplace=True)

combos=combos.astype("float")
combos.head()

print(combos)
combos.to_csv("output.csv", sep=';')

fig = plt.figure(figsize=(8,8))
ax=plt.subplot(211)
ax.invert_yaxis()

combos.loc[:,pd.IndexSlice[:,"M"]].plot(ax=ax)

ax=plt.subplot(212)
ax.invert_yaxis()

combos.loc[:,pd.IndexSlice[:,"V"]].plot(ax=ax)

plt.show()
