  # Generador de Progresiones Modales por Grados Contiguos

    Esta aplicación genera progresiones de acordes modales para varios modos musicales. Los acordes se generan de manera semi-aleatoria, pero con ciertas ponderaciones para cada posible transición de acordes, lo que permite crear progresiones que son musicalmente plausibles.

    ## Uso

    La interfaz de la aplicación es simple. En la barra lateral, puedes seleccionar:

    1. **Tonalidad**: Esta es la tonalidad en la que se generará la progresión. Las opciones son 'C', 'D', 'E', 'F', 'G', 'A' y 'B'.
    2. **Modo**: Puedes seleccionar entre varios modos musicales. Cada modo tiene diferentes transiciones de acordes posibles.
    3. **Número de acordes**: Este control deslizante te permite seleccionar el número de acordes que deseas en tu progresión.

    Además, puedes ajustar el tamaño de la fuente y activar o desactivar el texto en negrita para la progresión de acordes generada.

    ## Cómo se generan las progresiones

    Las progresiones de acordes se generan utilizando un mapa de transiciones de acordes. Para cada acorde, hay una lista de acordes a los que puede seguir y una probabilidad asociada a cada posible transición.
    
     Como ejemplo, aquí está la tabla de transiciones para el modo Lidio:

    | Acorde de origen | Acorde destino | Probabilidad |
    | ---------------- | -------------- | ------------ |
    | Imaj7            | II6            | 0.4          |
    | Imaj7            | VIIm7          | 0.4          |
    | Imaj7            | Vmaj7          | 0.2          |
    | II6              | Imaj7          | 0.4          |
    | II6              | IIIm7          | 0.4          |
    | II6              | VIm7           | 0.2          |
    | IIIm7            | II6            | 0.4          |
    | IIIm7            | VIIm7          | 0.4          |
    | IIIm7            | VIm7           | 0.2          |
    | Vmaj7            | VIm7           | 0.4          |
    | Vmaj7            | II6            | 0.4          |
    | Vmaj7            | IIIm7          | 0.2          |
    | VIm7             | VIIm7          | 0.4          |
    | VIm7             | Vmaj7          | 0.4          |
    | VIm7             | IIIm7          | 0.2          |
    | VIIm7            | VIm7           | 0.4          |
    | VIIm7            | Imaj7          | 0.4          |
    | VIIm7            | IIIm7          | 0.2          |

    En la progresión generada, el primer acorde es siempre el acorde tónico. Luego, para cada acorde subsiguiente, se elige al azar de la lista de posibles transiciones del acorde actual, de acuerdo con las ponderaciones especificadas.

    Esto permite generar progresiones que son semi-aleatorias, pero que aún siguen las convenciones de la teoría musical.

    ## Dependencias

    Las bibliotecas necesarias para ejecutar esta aplicación son:

    - streamlit
    - random

    Estas dependencias están incluidas en el archivo `requirements.txt`. 

    Para instalar las dependencias, ejecute el siguiente comando en su terminal:

    ```bash
    pip install -r requirements.txt
