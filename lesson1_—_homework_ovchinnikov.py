# -*- coding: utf-8 -*-
"""Lesson1 — homework-Ovchinnikov.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14cijpIeHLMudd6v5LsQTbAp1zxMeJQQF

# Deep Learning

Начнём наш курс с исторической справки, когда и как что появилось:

<img src="https://drive.google.com/uc?export=view&id=1c-NlY2gB_yHj_jOzj0MmqizzFSsjZboI" style="width:1066px;height:501px;">

Предполагается, что модель нейрона, используемая в искусственных нейросетях, называемая [перцептроном](https://ru.wikipedia.org/wiki/%D0%9F%D0%B5%D1%80%D1%86%D0%B5%D0%BF%D1%82%D1%80%D0%BE%D0%BD), соответствует биологическим нейронам головного мозга (предполоджение выдвинуто в 1957 году нейрофизиологом Фрэнком Розенблаттом).

<img src="https://drive.google.com/uc?export=view&id=1wh2tZL8Z5H802sZ6j1rCJvqNI9PZjPwT" style="width:533px;height:250px;">

На рисунке выше изображена одна из первых моделей нейросети (1965 год), однако веса в такой модели не подбирались в процессе обучения, а задавались исходя из каких-то базовых предположений.

Помимо событий, отмеченных в таймлайне, нелишним будет упомянуть теорему об универсальной аппроксимации (1989 by George Cybenko), являющейся математическим доказательством того, что искусственная нейросеть способна аппроксимировать любую "достаточно хорошую" функцию:

[Универсальная теорема об аппроксимации (википедии);](https://en.wikipedia.org/wiki/Universal_approximation_theorem)

[Универсальная теорема об аппроксимации (оригинальная статья);](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.441.7873&rep=rep1&type=pdf)

Начало 2000-ых называется также периодом AI Winter (вторая зима ИИ), поскольку все идеи уже были изложены, но по причине отсутствия больших наборов данных и производительных процессоров обучать сложные и глубокие нейросети не представлялось возможным...

2012 год считается прорывным, поскольку тогда нейросеть [AlexNet](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf), обученная на GPU, сумела выиграть соревнование по распознаванию изображений с большим отрывом (порядка 12%). Именно тогда поднялся хайп вокруг DL :)

Еще одним прорывом было поражение [Ли Седоля в игру Go](https://en.wikipedia.org/wiki/AlphaGo_versus_Lee_Sedol) весной 2016 года. AlphaGo был разработан лабораторией Google DeepMind во главе с Демисом Хасабисом. Игра Go считалась прежде непостижимой для AI по причине того, что количество возможных комбинаций ходов не позволяло аналитически строить дерево решений.

## Логистическая регрессия

В данном упражнении мы построим простейший классификатор изображений, основанный на логистической регрессии. 

<img src="https://drive.google.com/uc?export=view&id=14TpTs8-VqVOFR9qMUW4mjMdC6sOpd5Bl" style="width:618px;height:306px;">

Данные в модель мы будем подавать хитрым образом: изображение, то есть матрицу размером $(n,n)$ мы преобразуем в вектор столбец размерности $(n^2,1)$. После этого полученный многомерный вектор будем подавать на вход в модель. Такая модель предполагает, что $n$ необходимо определить заранее, перед обучением, и в дальнейшем его нельзя будет изменить (потребуется обучать модель заново). 

Таким образом, надо проверять, являются ли размеры изображения допустимыми перед тем, как подавать его в модель. Если нет, то можно воспользоваться функцией resize из библиотеки openCV, которая изменяет размеры изображения.

### Шаг 1. Инициализация модели

Данная функция возвращает маccив $w$ и число $b$, которые на каждой итерации обучения будут обновляться.
"""

def init_model(input_size=256):
    
    ###ЗАДАЧА: проинициализируйте веса модели так, чтобы массив w имел размер (input_size^2,1), а b был числом
    w = np.ones((input_size ** 2, 1))
    b = 1
    return w, b

"""В нашей модели логистической регрессии по большому счету неважно, как были проинициализированы веса (можно проинициализировать все значения нулями, можно - случайными значениями, можно двойками и т.д.:) ). Однако для глубоких нейросетей это имеет очень большое значение, и $\textbf{крайне не рекомендуется инициализировать значения нулями!}$ Об этом мы ещё обязательно поговорим в дальнейшем.

### Шаг 2. Обучение модели

После того как мы задали начальные параметры (он пока был всего один - это размер  $n$) и проинициализировали веса, можно приступать к обучению модели.

Обучение модели осуществляется в цикле и состоит из трех шагов:
    - подсчет текущего значения функции ошибки
    - подсчет градиента функции ошибки
    - обновление весов модели
    
Вспомним теорию...

Для i-ого образца $x^{(i)}$:

$$z^{(i)} = w^T x^{(i)} + b \tag{1}$$

$$\hat{y}^{(i)} = a^{(i)} = sigmoid(z^{(i)})\tag{2}$$ 

$$ \mathcal{L}(a^{(i)}, y^{(i)}) =  - y^{(i)}  \log(a^{(i)}) - (1-y^{(i)} )  \log(1-a^{(i)})\tag{3}$$

Подсчет функции ошибки - это суммирование потерь на всех образцах:

$$ J = \frac{1}{m} \sum_{i=1}^m \mathcal{L}(a^{(i)}, y^{(i)})\tag{4}$$

**Задачи**:

Необходимо будет реализовать следующие шаги: 
    - Инициализировать параметры модели
    - Обучить параметры, минимизируя функцию потерь  
    - Проверить модель на тестовом наборе данных
    - Проанализировать обученную модель
    
Для начала необходимо будет объявить несколько вспомогательных функций, а затем собрать из них модель и начать обучение.
"""

def sigmoid(z):
    ###ВАЖНО: функция принимает на вход массив любых размеров, на выход возвращает массив такого же размера
    s = 1/(1+np.exp(-z))
    return s

"""Еще раз выпишем формулы для вывода текущего предсказания, для текущей ошибки и для текущего градиента функции ошибки:

    - Подсчитываем предсказание (forward propagation):
    
$$A = \sigma(w^T X + b) = (a^{(1)}, a^{(2)}, ..., a^{(m-1)}, a^{(m)})\tag{6}$$
    - Подсчитываем функцию ошибки: 
    
$$J = -\frac{1}{m}\sum_{i=1}^{m}y^{(i)}\log(a^{(i)})+(1-y^{(i)})\log(1-a^{(i)})\tag{7}$$
    - Подсчитываем градиент функции ошибки (backward propagation):
    
$$ \frac{\partial J}{\partial w}=\nabla J_w = \frac{1}{m}X(A-Y)^T\tag{8}$$

$$ \frac{\partial J}{\partial b} =\frac{dJ}{db}= \frac{1}{m} \sum_{i=1}^m (a^{(i)}-y^{(i)})\tag{9}$$
"""

def propagate(w, b, X, Y):
    """
    Подсчет текущего предсказания (оно же forward propagation) и градиента функции ошибки (оно же backward propagation)

    Input:
    w -- веса, numpy_array размера (num_px * num_px * 3, 1)
    b -- смещение, скалярная величина
    X -- данные размера (num_px * num_px * 3, кол-во образцов)
    Y -- вектор истинных ответов размера (1, кол-во образцов)

    Return:
    cost -- текущая функция потерь
    dw -- градиент функции ошибки по w
    db -- градиент функции ошибки по b (по сути производная по b)
    
    """
    
    m = X.shape[1]
    
    A = s * (np.dot(w.T, X) + b)
    cost = - (1 / m) * np.sum(np.multiply(Y, np.log(A)) + np.multiply(1 - y, np.log(1 - A)))
    
    
    dw = 1/m * np.dot(X,(A - Y).T) 
    db = 1/m * np.sum(A - Y)
    
    
    grads = {"dw": dw,
             "db": db}
    
    return grads, cost



"""Мы реализовали блоки для работы модели и для подсчета функции ошибки и необходимых градиентов. Теперь осталось реализовать функцию, осуществляющую обучение. 

**Под обучением мы сейчас и впредь будем иметь в виду обновление весов таким образом, чтобы функция ошибки на  обучающей выборке достигала минимума.**

**Важно!!!** Под записями $dw$ и $db$ мы будем подразумевать соответствующие градиенты функции потерь, то есть $\frac{\partial J}{\partial w}$(вектор) и $\frac{\partial J}{\partial b} (скаляр)$.

 **Задание:** Реализуйте шаг обновления весов модели. Для параметра $w$ обновление выглядит так: 
 
 $ w := w - \alpha \text{ } dw \tag{10},$ а 
 
 $$ b : = b - \alpha \text{ } db \tag{11},$$
 
где $\alpha$ - некий коэффициент (который называется $\textit{learning rate}$ - не будем переводить это на русский язык).
"""

def optimize(w, b, X, Y, num_iterations, learning_rate, print_cost = False):
    """
    Оптимизация с помощью простого градиентного спуска
    
    Input:
    w -- веса, numpy_array размера (num_px * num_px * 3, 1)
    b -- смещение, скалярная величина
    X -- данные размера (num_px * num_px * 3, кол-во образцов)
    Y -- вектор истинных ответов размера (1, кол-во образцов)
    num_iterations -- кол-во итераций алгоритма оптимизации
    learning_rate -- коэффициент learning rate
    print_cost -- True, если хотите выводить функцию ошибки на каждых 100 итерациях
    
    Returns:
    params -- словарь, содержащий w и b
    grads -- словарь, содержащий градиенты функции ошибки по w и b соответственно
    costs -- массив (list) со значением функции ошибки для каждой итерации (так делают для визуализации)
    
    Подсказка:
    
        1) Используйте ранее написанную функцию propagate().
        2) Обновляйте параметры w и b согласно формуле 10.
    """
    
    costs = []
    
    for i in range(num_iterations):
        
        
        ###Напишите значения для градиентов и функции ошибки
        grads, cost = propagate(w, b, X, Y)
        
        
        # Retrieve derivatives from grads
        dw = grads["dw"]
        db = grads["db"]
        
        # обновление параметров
        
        ### START CODE HERE ###
        w = w - learning_rate * dw
        b = b - learning_rate * db
        ### END CODE HERE ###
        
        # Record the costs
        if i % 100 == 0:
            costs.append(cost)
        
        # Print the cost every 100 training iterations
        if print_cost and i % 100 == 0:
            print ("Cost after iteration %i: %f" %(i, cost))
    
    params = {"w": w,
              "b": b}
    
    grads = {"dw": dw,
             "db": db}
    
    return params, grads, costs

"""Теперь реализуем функцию predict(), которая будет вызываться уже после обучения для предсказания моделью:"""

def predict(w, b, X):
    '''
    
    Inputs:
    w
    b
    X -- данные размера (num_px * num_px * 3, кол-во образцов)
    
    Returns:
    Y_prediction
    '''
    
    m = X.shape[1]
    Y_prediction = np.zeros((1,m))
    w = w.reshape(X.shape[0], 1)
    
    
    ### START CODE HERE ### (≈ 1 line of code)
    A = sigmoid(np.dot(w.T,X)+b)
    ### END CODE HERE ###
    
    for i in range(A.shape[1]):
        
        # Установите порог, выше которого считаем, что модель выдает 1, а ниже - ноль
        ### START CODE HERE ###
        if (A[0,i] <= 0.5):
            Y_prediction[0,i] = 0
        else:
            Y_prediction[0,i] = 1
        ### END CODE HERE ###
    
    
    return Y_prediction



"""### Необходимые библиотеки

Перед запуском программ необходимо импортировать следующие библиотеки:

```python
import cv2
import numpy as np
import os
from google.colab import drive 
```
"""

import cv2
import numpy as np
import os
from google.colab import drive

"""**Важно:**
Как монтировать google drive?
"""

from google.colab import drive 
drive.mount('/content/gdrive')
### path = 'gdrive/My\ Drive/__путь_к_папке__'

"""### Парсер данных

Парсер файлов уже написан и приведен ниже. В качестве аргументов ему передаются X - пустое значение, Y - пустой NumPy массив, path - директория к изображением, ans - ответ (1 - если в этой директории лежат кадры с коробками, 0 - если наоборот).
"""

X = None
Y = np.array([])
def read_files(X, Y, path, ans):
  files = os.listdir(path)
  for name in files:
    img = cv2.imread(path + '/' + name, 0)
    if img.shape != 0:
      img = cv2.resize(img, (256, 256))
      vect = img.reshape(1, 256 ** 2)
      vect = vect / 255.
      X = vect if (X is None) else np.vstack((X, vect)) 
      Y = np.append(Y, ans)
  return X, Y