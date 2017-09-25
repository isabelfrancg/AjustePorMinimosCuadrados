#-*- coding: cp1252 -*-
import sys
import math
import numpy
import matplotlib
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
from operator import add

print('Programa de ajuste por minimos cuadrados')
print('Realizado por Isabel Franco\nLaboratorio de Fisica aplicada UCLM, Julio 2017')
print('\nInstrucciones de uso:\nDebe crear un archivo .txt \ny guardarlo en la misma carpeta que este ejecutable.')
print('En el documento deberan de encontrarse los datos a estudio\nen dos columnas separadas por un espacio.')
print('La primera columna sera utilizada por el programa como las Abcisas\ny la segunda como las Ordenadas de la grafica\n')
print('Notas:\nSi se quiere introducir exponenciales en su documento:\nDebera de ingresarlos como numeroEexponente.\nEjemplo: 5x10e-2 sera 5E-2\n')

raw_input('Enter para continuar\n')

q0=raw_input('Introduzca nombre del archivo\n')

f=open('%s.txt'%q0,"r")    
lines=f.readlines()                 ##list of elements in the document       
Abcisas=[]
Ordenadas=[]
for n in lines:                     ##For loop due to nºiterations needed=len(list)
   Abcisas.append(n.split()[0])     ##Dividing columns in 2 lists
   Ordenadas.append(n.split()[1])

for i in range(len(Abcisas)):        ##We need range(len()) bc we'll use indices
    Abcisas[i] = float(Abcisas[i])      #We'll use same loop since
    Ordenadas[i]=float(Ordenadas[i])    #Both columns will always have same dimension

   
'''Herramientas para el cáclulo de datos'''

sx=0                         ##If you set absc[0] you'd add an extra first term in the sum of the loop
sx2=0
sy=0
sy2=0
sxy=0
sx2y=0

for i in Abcisas:               #Creating summs of the elements in lists
    sx+=i
    sx2+=(i)**2

for i in Ordenadas:
    sy+=i
    sy2+=(i)**2

AO=numpy.array(Abcisas)*numpy.array(Ordenadas)          #You cant multiply lists
A2O=(numpy.array(Abcisas))**2*numpy.array(Ordenadas)    #You need to make them arrays

for i in AO:
    sxy+=i
for i in A2O:
    sx2y+=i

'''Cálculo de datos'''

print('\n---Datos de la recta ajustada---')
   
N=len(Abcisas)                                      #len(abcisas)=len(ordenadas)

raw_input('Enter para visualizar\n')

if 0 in Ordenadas and 0 in Abcisas:                 #If it goes through the origin
    if Ordenadas.index(0)==Abcisas.index(0):
        b=0
        a=(sxy)/float(sx2)                          #We simplify the operations
        print('La pendiente a = %f' %a)                             
        print('La ordenada b = %f' %b)
    else:
        a=((N*sxy)-(sx*sy))/float((N*sx2)-((sx)**2))      #If not - classical calculations
        #b2=((sy)-(a*sx))/float(N)
        b=((sx*sxy)-(sx2*sy))/float((sx)**2-N*(sx2))
        print('La pendiente a = %f' %a)
        print('La ordenada b = %f' %b)
        #print('La ordenada b2 = %f' %b2)               #b2 is the other method to calculate b
else:
    a=((N*sxy)-(sx*sy))/float((N*sx2)-((sx)**2))      #If not - classical calculations
    #b2=((sy)-(a*sx))/float(N)
    b=((sx*sxy)-(sx2*sy))/float((sx)**2-N*(sx2))
    print('La pendiente a = %f' %a)
    print('La ordenada b = %f' %b)
    #print('La ordenada b2 = %f' %b2)
    


r = ((N*sxy)-(sx*sy))/float(math.sqrt(((N*sx2)-(sx**2))*((N*sy2)-(sy**2))))

print ( 'El coeficiente de correlacion lineal "r" = %f' %r)

if -0.50<r<0.50:            #Show the reader how precise our estimation will be
   print('El grado de correlacion entre las variables es : bajo \nLa recta obtenida será imprecisa')
else:
   print('El grado de correlacion entre las variables es : suficiente \nLa recta obtenida es correcta')

'''Herramientas para el cáclulo de error'''

xbar=sx/float(N)
syaxb2=0
sxxbar2=0

for (i,e) in zip(Abcisas,Ordenadas):            #More sums for the calculation of variables
   syaxb2+= (e-a*i-b)**2

for i in Abcisas:
   sxxbar2+= (i - xbar)**2


'''Cálculo de error'''

print('\n---Calculo de error---')

raw_input('Enter para visualizar\n')

Aa=math.sqrt((syaxb2)/float((N-2)*(sxxbar2)))
Ab=math.sqrt(((1/float(N))+((xbar**2)/float(sxxbar2)))*((syaxb2)/float(N-2)))

print( 'Error de pendiente = %f' %Aa)
print( 'Error de la ordenada = %f' %Ab)


'''Gráfica'''
fig=pyplot.figure()     #To open a figure
pyplot.clf()            #To clear the plot window

'''Datos experimentales'''
xs=numpy.array(Abcisas)         #We need to create arrays for the plotting
ys=numpy.array(Ordenadas)
ax=pyplot.plot(xs,ys,'x',color='black',label='Data')  #To plot abcisas against ordenadas

'''Línea Fit'''
x=numpy.linspace(xs[0],xs[-1],60)         #Length of line: from first point until last one
f=a*x+b
pyplot.plot(x,f,label='Fit',linewidth=0.5,color='red')


'''Ajustes'''
print('\n---Ajustes de la grafica---\n')
fig.patch.set_facecolor('white')       #To change outside background colour
pyplot.gca().spines['right'].set_visible(False)    #gca=get the current axes
pyplot.gca().spines['top'].set_visible(False)      #Remove unecessary axes 
pyplot.tick_params(axis='x', which= 'both', bottom='on', top='off') #Which=major and minor ticks
pyplot.tick_params(axis='y', which='both', right='off', left='on')  #Remove dashes from axes removed

pyplot.legend(loc='lower right', numpoints= 1)                         #Position legend
#matplotlib.rcParams['legend.numpoints'] = 1            #Used:To have one unique cross in the legend

q3=raw_input('Introducir titulo de la grafica (Enter para titulo en blanco) ').decode(sys.stdin.encoding)
pyplot.title('%s'%q3)

q1=raw_input ('Introducir titulo del eje de ordenadas (Enter para titulo en blanco) ').decode(sys.stdin.encoding)
pyplot.ylabel('%s'%q1, color='grey')

q2=raw_input ('Introducir titulo del eje de abcisas (Enter para titulo en blanco) ').decode(sys.stdin.encoding)
pyplot.xlabel('%s'%q2,color='grey')

print('\nGrafica lista para visualizar')

pyplot.show()

pyplot.close()

