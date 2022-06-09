# -*- coding: utf-8 -*-
"""Классификация птиц.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DvHWc09JfuMqwBUApukrTOBUIE97sQqK

# Загрузка библиотек и модулей
"""

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt #  вывод графиков
from tensorflow.keras.layers import Flatten, Dense, Conv2D, MaxPool2D # слои для построения модели
from tensorflow.keras.preprocessing.image import ImageDataGenerator # генератор для разделения на выборки
from tensorflow.keras.models import Sequential # полносвязная модель
from tensorflow.keras.optimizers import Adam # оптимизатор
from google.colab import drive # работа с Google Drive
from time import time # импортируем библиотеку time

# %matplotlib inline

"""# Подготовка файлов"""

!rm -R '/content/birds' # проверяем наличие папки birds. Если есть, удаляем ее

# разархивация датасета в директорию 'content/birds'

!unzip -qo "/content/drive/MyDrive/Project/Bird/train.zip" -d /content/birds

"""# Создание обучающей и проверочной выборки через генератор

Без аугминтации
"""

start = time() # замеряем время на выполнение команды

data_generator = ImageDataGenerator(rescale=1/255) # нормализуем данные

# создаем обучающую выборку
x_train = data_generator.flow_from_directory(
    '/content/birds/train',
    target_size=(224, 224),
    batch_size=128,
    class_mode='sparse')

# создаем проверочную выборку
y_train = data_generator.flow_from_directory(
    '/content/birds/train',
    target_size=(224, 224),
    batch_size=32,
    class_mode='sparse')

print(f'Время = {time() - start}')

"""# Модель и обучение"""

# создание модели
model = Sequential([
                    Conv2D(32, 5, padding='same', activation='relu', input_shape=(224, 224, 3)),
                    MaxPool2D((4, 4)),
                    Conv2D(64, 5, padding='same', activation='relu'),
                    MaxPool2D((4, 4)),
                    Flatten(),
                    Dense(512, activation='relu'),
                    Dense(310, activation='softmax')
])
# компиляция модели
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# обучение модели
history = model.fit(x_train, epochs=10, validation_data=y_train)

"""# Графики

## график ошибки
"""

plt.figure(figsize=(12,4)) # размер графика
plt.plot(history.history['loss'], label='Ошибка на обучающей выборке') # ошибка на проверочной выборке
plt.plot(history.history['val_loss'], label='Ошибка на проверочной выборке') # ошибка на тестовой выборке
plt.title('График ошибки') # название графика
plt.xlabel('Кол-во эпох') #  название оси X
plt.ylabel('% ошибки') # название оси Y
plt.legend() # Вызываем отображение легенды на графике
plt.show() # Фиксируем график

"""## график точности"""

plt.figure(figsize=(12,4)) # размер графика
plt.plot(history.history['accuracy'], label='Точность на обучающей выборке') # точность на проверочной выборке
plt.plot(history.history['val_accuracy'], label='Точность на проверочной выборке') # точность на тестовой выборке
plt.title('График точности обучения') # название графика
plt.xlabel('Кол-во эпох') #  название оси X
plt.ylabel('% точности') # название оси Y
plt.legend() # Вызываем отображение легенды на графике
plt.show() # Фиксируем график