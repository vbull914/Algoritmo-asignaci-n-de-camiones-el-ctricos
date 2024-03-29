# -*- coding: utf-8 -*-
"""Calculadora IC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1viM_-Tny_Q5OsVtMraW7DeCjWWGms6Jl
"""

#SOLO DEBES CORRER ESTA CELDA PARA USAR LA HERRAMIENTA

#RESTRICIONES A CONSIDERAR:
#-->1. No pueden haber más cargadores que camiones.
#-->2. Un cargador ultrarapido puede tener 2 salidas.
#-->3. Se utiliza potencia constante durante la mayor cantidad de los periodos de carga.
#-->4. No se excede el máximo consumo en kWh al mes definido por la distribuidora.
#-->5. Asumo que la máxima potencia entregada es soportada por el vehículo.
#Primero se ingresa la base de información de costos eléctricos
import pandas as pd

data=[['Cerrillos','AT4.3',796,0.701,10.343,77.3,2080,6744],['La Florida','AT4.3',796,0.701,10.343,77.27,2074,6744],['Cerrillos','BT4.3',796,0.701,10.343,81.57,11340,4210],['La Florida','BT4.3',796,0.701,10.343,81.57,11340,4210]]
costos=pd.DataFrame(data, columns=['Comuna','Tipo','Cargo fijo', 'Cargo servicio publico', 'Cargo transporte','Costo energía','Costo potencia medida en hora punta','Costo potencia consumida'])
#Costo potencia medida en hora punta[AA,SA,AS,SS]
#Costo potencia consumida[AA,SA,AS,SS]

#Ahora lo hacemos interactivo
#Se piden los input
ncamiones = int(input("¿Cuál es el número de vehículos eléctricos que tiene? "))
hora_inicio = int(input("¿A qué hora puede empezar a cargar las baterías? (Ingrese valores desde 0 a 23) "))
hora_termino = int(input("¿Hasta qué hora puede cargar las baterías?(Ingrese valores desde 0 a 23)"))
comuna = int(input("¿En qué comuna vive? Ingrese 1 si es Cerrillos o 2 si es La Florida"))
tipocontrato = int(input("¿Qué tipo de contrato tiene con el proveedor de energía? Ingrese 1 si es AT4.3 o 2 si es BT4.3"))
bat_cam=int(input("¿Cuál es la capacidad de la batería del vehículo en kWh?"))
mes_evaluacion=int(input("¿Para qué mes quiere evaluar el gasto en energía eléctrica?(Ingrese un número un número de 1 a 12)"))
pot_instala=int(input("¿Cuál es la potencia máxima que soporta su empalme eléctrico en kW?"))
diasmes=int(input("¿Cuántos días del mes espera recargar los camiones en el horario declarado?"))


if comuna==2:
  comun='La Florida'
elif comuna==1:
  comun='Cerrillos'
else:
  print('ERROR, debe ingresar un número de comuna válido')
if tipocontrato==1:
  contrelec='AT4.3'
elif tipocontrato==2:
  contrelec='BT4.3'
else:
  print('ERROR, debe ingresar un número de contrato eléctrico válido')
fila_buscada = costos.loc[(costos['Comuna'] == comun) & (costos['Tipo'] == contrelec)]
fila_buscada.iloc[0][2]

if comuna==2:
  comun='La Florida'
elif comuna==1:
  comun='Cerrillos'
else:
  print('ERROR, debe ingresar un número de comuna válido')
if tipocontrato==1:
  contrelec='AT4.3'
elif tipocontrato==2:
  contrelec='BT4.3'
else:
  print('ERROR, debe ingresar un número de contrato eléctrico válido')
fila_buscada = costos.loc[(costos['Comuna'] == comun) & (costos['Tipo'] == contrelec)]

car_fijo=fila_buscada.iloc[0][2] #CLP/mes: cargo fijo mensual neto
car_serpubl=fila_buscada.iloc[0][3] #Cargo por servicio público $/kWh
car_trans=fila_buscada.iloc[0][4] #cargo por transporte neto $/kWh
cost_ener=fila_buscada.iloc[0][5] #costo energia neto $/kwh
cost_potpun=fila_buscada.iloc[0][6] #costo por potencia en horario punta $/kw/mes
cost_potsumi=fila_buscada.iloc[0][7] #costo potencia suministrada neto $/kw/mes

#Datos varios
pcr=50 #kw potencia de carga maxima punto de carga rapida
pcur=120 #kw potencia de carga maxima punto de carga ultra rapida
pcl=22 #kw potencia de carga maxima punto de carga lenta
cost_cr = 19270000 #costo cargador rápido en CLP
cost_cur = 97000000 #costo cargador ultra rápido en CLP
cost_cl = 7200000 #costo cargador lento en CLP
resultados=pd.DataFrame([], columns=['numero c.rapidos','numero c.ultrarapidos','numero c.lentos', 'potencia demandada', 'numero de camiones','inversion inicial','costo mensual','energia demandada en mes','uso en hora punta'])
for i in range(ncamiones+1):
  ncr=i
  for i in range(ncamiones+1):
    ncur=i
    for i in range(ncamiones+1):
      ncl=i
      if ncr+ncur+ncl>ncamiones:
        continue
      if hora_termino>=hora_inicio:
        horas_carga=hora_termino-hora_inicio
      else:
        horas_carga=hora_termino+(24-hora_inicio)
      ener_cr=ncr*pcr*horas_carga #energía provista por cargadores rapidos
      ener_cur=ncur*pcur*horas_carga #energía provista por cargadores ultra rapidos
      ener_cl=ncl*pcl*horas_carga #energia provista por cargadores lentos
      ener_dem=ener_cr+ener_cl+ener_cur
      if ener_dem<ncamiones*bat_cam*0.8:
        continue
      pot_dem=ncr*pcr+ncur*pcur+ncl*pcl
      if pot_dem>pot_instala:
        continue
      inv_ini=ncr*cost_cr+ncur*cost_cur+ncl*cost_cl
      enertotmes=ncamiones*bat_cam*0.8*diasmes
      cartot_serpubl=car_serpubl*enertotmes
      cartot_trans=car_trans*enertotmes
      costot_ener=cost_ener*enertotmes
      if mes_evaluacion==4 or mes_evaluacion==5 or mes_evaluacion==6 or mes_evaluacion==7 or mes_evaluacion==8 or mes_evaluacion==9:
        if hora_inicio==18 or hora_inicio==19 or hora_inicio==20 or hora_inicio==21 or hora_inicio==22 :
          costot_potpun= (ncr*pcr+ncur*pcur+ncl*pcl)*cost_potpun  #Hora punta es de 18:00 a 23:00 horas en los meses de abril y septiembre
          usa_punta='SI'
        elif hora_termino==19 or hora_termino==20 or hora_termino==21 or hora_termino==22 or hora_termino==23:
          costot_potpun=(ncr*pcr+ncur*pcur+ncl*pcl)*cost_potpun#Hora punta es de 18 a 22 horas en los meses de abril y septiembre
          usa_punta='SI'
        else:
          costot_potpun=0
          usa_punta='NO'
      else:
        costot_potpun=0
        usa_punta='NO'
      costot_potsumi= (ncr*pcr+ncur*pcur+ncl*pcl)*cost_potsumi #multiplicacion simple.
      costo_total_mes= car_fijo+cartot_serpubl+cartot_trans+costot_ener+costot_potpun+costot_potsumi
      fila_i=[ncr,ncur,ncl,pot_dem,ncamiones,inv_ini,costo_total_mes,enertotmes,usa_punta]
      nuevo_df = pd.DataFrame([fila_i], columns=resultados.columns)
      resultados = pd.concat([resultados,nuevo_df], ignore_index=True)
indice_fila_min_op = resultados['costo mensual'].idxmin()  # Encuentra el índice del valor mínimo en 'Columna_A'
fila_min = resultados.loc[indice_fila_min_op]  # Accede a toda la fila correspondiente al índice del valor mínimo
print("Los datos de la configuración que produce el menor costo operacional mensual es:")
print(fila_min)
print('Además, le entregamos las 15 mejores opciones basadas en el menor costo operacional mensual')
df_descendente = resultados.sort_values(by='costo mensual', ascending=True)
df_descendente.head(15)



#FUNCIONES AUXILIARES QUE NO ES NECESARIO CORRER

def horascarga(hora_inicio,hora_termino):
  if hora_termino>=hora_inicio:
    horas_carga=hora_termino-hora_inicio
  else:
    horas_carga=hora_termino+(24-hora_inicio)
  return horas_carga
def dalaenergia(ncr,pcr,ncur,pcur,pcl,ncl,ncamiones,bat_cam,hora_inicio,hora_termino):
  ener_cr=ncr*pcr*horascarga(hora_inicio,hora_termino) #energía provista por cargadores rapidos
  ener_cur=ncur*pcur*horascarga(hora_inicio,hora_termino) #energía provista por cargadores ultra rapidos
  ener_cl=ncl*pcl*horascarga(hora_inicio,hora_termino) #energia provista por cargadores lentos
  print('La energía total requerida es:', bat_cam*0.8*ncamiones, 'kWh')
  print('La energía total entregada entre las',hora_inicio,'y',hora_termino,'hrs es:',ener_cr+ener_cl+ener_cur,'kWh')
  if ener_cr+ener_cl+ener_cur<ncamiones*bat_cam*0.8:
    return 0
  else:
    return 1
def sop_maxpot(ncr,pcr,ncur,pcur,pcl,ncl,pot_instala):
  pot_dem=ncr*pcr+ncur*pcur+ncl*pcl
  print('Máxima potencia demandada es:',pot_dem, 'kW')
  if pot_dem<pot_instala:
    return 1
  else:
    return 0
def enertotmes(ncamiones,bat_cam,diasmes):
  return ncamiones*bat_cam*0.8*diasmes
def costo_opmes(car_fijo,car_serpubl,car_trans,cost_ener,cost_potpun,cost_potsumi,mes_evaluacion,hora_inicio,hora_termino):
  cartot_serpubl=car_serpubl*enertotmes(ncamiones,bat_cam,diasmes)
  cartot_trans=car_trans*enertotmes(ncamiones,bat_cam,diasmes)
  costot_ener=cost_ener*enertotmes(ncamiones,bat_cam,diasmes)
  if mes_evaluacion==4 or mes_evaluacion==5 or mes_evaluacion==6 or mes_evaluacion==7 or mes_evaluacion==8 or mes_evaluacion==9:
    if hora_inicio==18 or hora_inicio==19 or hora_inicio==20 or hora_inicio==21 or hora_inicio==22 :
      costot_potpun= (ncr*pcr+ncur*pcur+ncl*pcl)*cost_potpun  #Hora punta es de 18:00 a 23:00 horas en los meses de abril y septiembre
      print("Se registra uso en hora punta")
    elif hora_termino==19 or hora_termino==20 or hora_termino==21 or hora_termino==22 or hora_termino==23:
      costot_potpun=(ncr*pcr+ncur*pcur+ncl*pcl)*cost_potpun#Hora punta es de 18 a 22 horas en los meses de abril y septiembre
      print("Se registra uso en hora punta")
    else:
      costot_potpun=0
  else:
    costot_potpun=0
  costot_potsumi= (ncr*pcr+ncur*pcur+ncl*pcl)*cost_potsumi#multiplicacion simple.
  costo_total_mes= car_fijo+cartot_serpubl+cartot_trans+costot_ener+costot_potpun+costot_potsumi
  print("Costo total mes en CLP es:")
  return costo_total_mes