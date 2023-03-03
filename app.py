# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 20:20:30 2023

@author: Samue
"""
import requests
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import math 
import numpy
import matplotlib.pyplot as plt


def load_lottieurl(url):
    r= requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
tabla_disolventes = pd.read_excel("C:/Users/HP/Desktop/Libro1.xlsx", skiprows=[0], usecols="B,D:F") 
lottie_coding= load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_hgjskqs0.json")
st.set_page_config(page_title="Disolventes", page_icon=":tada:", layout="wide")

st.title("Cálculo de solubilidad a partir de parámetros de Hansen.")
st.subheader("Elección de disolventes")

with st.container():
    st.write("---")
    left_column, right_column=st.columns(2)
    with left_column:
        st.dataframe(tabla_disolventes)
with right_column:
    st_lottie(lottie_coding, height=300, key="coding" )
with st.container():
    left_column1, right_column2=st.columns(2)
    st.write("---") 
    with left_column1:
        Primer_Disolvente = st.number_input('Primer disolvente', min_value=0, max_value = 87, step=1)
    with right_column2:
        Segundo_Disolvente= st.number_input('Segundo disolvente', min_value=0, max_value = 87, step=1)

#print (tabla_disolventes)
z=tabla_disolventes.iloc[Primer_Disolvente]
print (z)   

disolvente1_dd=(tabla_disolventes.iat[Primer_Disolvente,1])
disolvente1_dp=(tabla_disolventes.iat[Primer_Disolvente,2])
disolvente1_dh=(tabla_disolventes.iat[Primer_Disolvente,3])

print(disolvente1_dd)
print(disolvente1_dp)
print(disolvente1_dh)



    
#print("has introducido el disolvente:", Se)
#print(type(segundo))

z=tabla_disolventes.iloc[Segundo_Disolvente]
print (z)

disolvente2_dd=(tabla_disolventes.iat[Segundo_Disolvente,1])
disolvente2_dp=(tabla_disolventes.iat[Segundo_Disolvente,2])
disolvente2_dh=(tabla_disolventes.iat[Segundo_Disolvente,3])

print(disolvente2_dd)
print(disolvente2_dp)
print(disolvente2_dh)

with st.container():
    if disolvente1_dd != "":
        st.markdown(
            f"""
            Disolvente 1: 
                    dd: {disolvente1_dd}
                    dp: {disolvente1_dp}
                   dh: {disolvente1_dh}
                   """
                   )
    if disolvente2_dd != "":
        st.markdown(
            f"""
            Disolvente 2: 
                    dd: {disolvente2_dd}
                    dp: {disolvente2_dp}
                    dh: {disolvente2_dh}
                   """
                   )
            
st.subheader("Elección de soluto")

with st.container():
    soluto= st.number_input('Introduzca el soluto', min_value=0, max_value = 87, step=1)  
    
z=tabla_disolventes.iloc[soluto]
print (z)
soluto_dd=(tabla_disolventes.iat[soluto,1])
soluto_dp=(tabla_disolventes.iat[soluto,2])
soluto_dh=(tabla_disolventes.iat[soluto,3])

lista_devaloresdd=[]
lista_devaloresdp=[]
lista_devaloresdh=[]
lista_devaloresRa=[]

for ConcentracionPrimero in numpy.arange(1,-0.25,0.25):
   
    ConcentracionSegundo=float(1-ConcentracionPrimero)
   
    mezcla_dd=math.sqrt((ConcentracionPrimero*(disolvente1_dd)*(disolvente1_dd))+(ConcentracionSegundo*(disolvente2_dd)*(disolvente2_dd)))
    mezcla_dp=math.sqrt((ConcentracionPrimero*(disolvente1_dp)*(disolvente1_dp))+(ConcentracionSegundo*(disolvente2_dp)*(disolvente2_dp)))
    mezcla_dh=math.sqrt((ConcentracionPrimero*(disolvente1_dh)*(disolvente1_dh))+(ConcentracionSegundo*(disolvente2_dh)*(disolvente2_dh)))
    
    lista_devaloresdd.append(mezcla_dd)
    lista_devaloresdp.append(mezcla_dp)
    lista_devaloresdh.append(mezcla_dh)
    
    Ra=math.sqrt(4*(mezcla_dd-soluto_dd)*(mezcla_dd-soluto_dd)+(mezcla_dp-soluto_dp)*(mezcla_dp-soluto_dp)+(mezcla_dh-soluto_dh)*(mezcla_dh-soluto_dh))
    Ra_redondeado=round(Ra, 2)
    lista_devaloresRa.append(Ra_redondeado)
    
mejor_opcion= min(lista_devaloresRa)

st.markdown(
     f"""
     Valores de Ra obtenidos para los compuestos seleccionados: 
             Ra = {lista_devaloresRa}
             
             El valor mínimo será: {mejor_opcion}

            """
            )

y=numpy.array(lista_devaloresRa)

x=numpy.array([100,75,50,25,0])
fig = plt.figure(figsize = (10, 5))

plt.title("Solubilidad de soluto en mezcla")
plt.ylabel("Valores de Ra obtenidos")
plt.xlabel("Concentración de disolvente 1 en tanto por ciento")
plt.plot(x, y, color = "red", marker = "o", label = "Array elements")
st.pyplot(fig)

st.write("El valor más bajo de Ra indicará que concentración del disolvente 1 es la óptima para lograr la disolución del soluto empleando esa mezcla.")


st.write("Si el valor es superior a 8 no serán disolventes útiles para ese soluto")










