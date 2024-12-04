## Problema: Clasificación de Clientes según su Perfil Financiero

### Descripción del Problema

Una institución financiera desea clasificar a sus clientes en tres categorías basándose en su perfil financiero y de comportamiento:

1.  ****Riesgo Bajo****: Clientes que cumplen con todos los pagos a tiempo y tienen ingresos estables.
2.  ****Riesgo Medio****: Clientes con retrasos esporádicos en los pagos o ingresos variables.
3.  ****Riesgo Alto****: Clientes con historial de impagos o ingresos inestables.

****Características de Entrada****:

1.  ****Historial de pagos****: Porcentaje de pagos realizados a tiempo (normalizado entre 0 y 1).
2.  ****Ingresos mensuales****: Ingresos promedio del cliente (normalizado entre 0 y 1).
3.  ****Relación deuda-ingreso****: Proporción entre la deuda total y los ingresos totales (normalizado entre 0 y 1).

****Categorías de Salida****:

-   `Riesgo Bajo`: [1, 0, 0]
-   `Riesgo Medio`: [0, 1, 0]
-   `Riesgo Alto`: [0, 0, 1]

### Conjunto de Datos de Entrenamiento
| Historial de pagos |  Ingresos mensuales| Relación deuda-ingreso | Resultado | 
|  |
|--|--|
|  |  |

|--|--|
|  |  |


### Actividades

***1.  Implementar una red neuronal multicapa para clasificar los clientes según su riesgo.***
***2.  Encontrar los valores óptimos para los pesos `w1`, `w2` 'wn' y el sesgo `b` mediante entrenamiento.***


***3.  Graficar la frontera de decisión que separa los clientes .***
import  numpy  as  np

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import Dense

import  matplotlib.pyplot  as  plt

from  sklearn.model_selection  import  train_test_split

from  matplotlib.colors  import  ListedColormap


X  =  np.array([

[0.9, 0.8, 0.2],

[0.7, 0.6, 0.5],

[0.4, 0.4, 0.8],

[0.8, 0.9, 0.3],

[0.5, 0.7, 0.6],

[0.3, 0.5, 0.9]

])

y  =  np.array([

[1, 0, 0],

[0, 1, 0],

[0, 0, 1],

[1, 0, 0],

[0, 1, 0],

[0, 0, 1]

])

  

X_train, X_test, y_train, y_test  =  train_test_split(X, y, test_size=0.2, random_state=42)

  

model  = Sequential([

Dense(8, input_dim=3, activation='relu'),

Dense(6, activation='relu'),

Dense(3, activation='softmax')

])

  

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

  

history  =  model.fit(X_train, y_train, epochs=50, batch_size=4, verbose=1)

  

loss, accuracy  =  model.evaluate(X_test, y_test, verbose=0)

print(f"\nPrecisión en el conjunto de prueba: {accuracy:.2f}")

  

nuevo_dato  =  np.array([[0.6, 0.6, 0.4]])

prediccion  =  model.predict(nuevo_dato)

categorias  = ["Riesgo Bajo", "Riesgo Medio", "Riesgo Alto"]

print(f"Predicción para {nuevo_dato}: {categorias[np.argmax(prediccion)]}")

  

print("\nPesos y sesgos del modelo:")

pesos_y_sesgos  =  model.get_weights()

for  i, peso  in  enumerate(pesos_y_sesgos):

print(f"Pesos/sesgos de la capa {i//2  +  1}  {'(pesos)'  if  i  %  2  ==  0  else  '(sesgo)'}: \n{peso}\n")

  

def  graficar_frontera_decision(model, X, y):

h  =  0.01

x_min, x_max  =  X[:, 0].min() -  0.1, X[:, 0].max() +  0.1

y_min, y_max  =  X[:, 1].min() -  0.1, X[:, 1].max() +  0.1

xx, yy  =  np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

Z  =  model.predict(np.c_[xx.ravel(), yy.ravel(), np.zeros(xx.ravel().shape)])

Z  =  np.argmax(Z, axis=1)

Z  =  Z.reshape(xx.shape)

plt.figure(figsize=(10, 6))

plt.contourf(xx, yy, Z, alpha=0.8, cmap=ListedColormap(["#FFAAAA", "#AAFFAA", "#AAAAFF"]))

scatter  =  plt.scatter(X[:, 0], X[:, 1], c=np.argmax(y, axis=1), edgecolor='k', cmap=ListedColormap(["#FF0000", "#00FF00", "#0000FF"]))

plt.xlabel("Historial de pagos")

plt.ylabel("Ingresos mensuales")

plt.title("Frontera de decisión")

plt.legend(*scatter.legend_elements(), title="Categorías")

plt.show()

  

graficar_frontera_decision(model, X, y)



***4.  ¿Son los datos linealmente separables?***
		Parece ser que si son linealmente separables debido a que se muestran dos líneas rectas en la gráfica.


***6.  ¿Qué ajustes podrían hacer al modelo para mejorar la clasificación?***
	Tal vez, recopilar una mayor cantidad de datos para entrenar el modelo, también comprobar que la normalización esté bien hecha y que todas las carecteríticas que necesitamos cumplan con ella y ajustar la tasa de aprendizaje.
		

***7.  Describir cada una de las partes del modelo implementando***
	     **Capa de entrada**: Tiene 3 características.
 **Capas ocultas**: Dos capas densas con 8 y 6 neuronas respectivamente, además de activación relu.
 **Capa de salida**: Tiene 3 neuronas, una para cada categoría, también tiene activación softmax para clasificar las categorías de manera probabilística.
**Optimización y pérdida**: El optimizador ajusta los pesos para minimizar la pérdida.

