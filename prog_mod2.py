import streamlit as st
import random
import re


# Diccionario de las ponderaciones de las transiciones de acordes
tabla_transiciones = {
    
    'Jonico': {
        'Imaj7/sus4': {'IIm7': 0.4, 'IVmaj7': 0.4, 'VIm7': 0.2},
        'IIm7': {'Imaj7/sus4': 0.4, 'IIIm7': 0.4, 'VIm7': 0.2},
        'IIIm7': {'IIm7': 0.4, 'IVmaj7': 0.4, 'VIm7': 0.2},
        'IVmaj7': {'Imaj7/sus4': 0.6, 'IIIm7': 0.4},
        'VIm7': {'IIm7': 0.4, 'IIIm7': 0.6},
    },
    'Dorico': {
        'Im7': {'IIm7': 0.35, 'Vm7': 0.15, 'IV6': 0.15, 'VIIb': 0.35},
        'IIm7': {'Im7': 0.4, 'IIIbmaj7': 0.4, 'Vm7': 0.2},
        'IIIbmaj7': {'IIm7': 0.35, 'IV6': 0.35, 'VIIb': 0.3},
        'IV6': {'Im7': 0.2, 'IIIbmaj7': 0.4, 'Vm7': 0.4},
        'Vm7': {'IIm7': 0.4, 'IV6': 0.6},
        'VIIb': {'Im7': 0.6, 'IIIbmaj7': 0.2, 'IV6': 0.2}
    },
    'Frigio': {
        'Im7': {'IIbmaj7': 0.4, 'IVm7': 0.2, 'VIIbm7': 0.4},
        'IIbmaj7': {'Im7': 0.4, 'IIIb6': 0.4, 'IVm7': 0.1, 'VIbmaj7': 0.1},
        'IIIb6': {'IIbmaj7': 0.4, 'IVm7': 0.4, 'VIIbm7': 0.2 },
        'IVm7': {'Im7':0.4, 'IIIb6': 0.4, 'VIIbm7': 0.2},
        'VIbmaj7': {'IIIb6': 0.3, 'IVm7': 0.1, 'VIIbm7': 0.6},
        'VIIbm7': {'Im7': 0.4, 'IVm7': 0.2, 'VIbmaj7': 0.4}
    },
    'Lidio': {
        'Imaj7': {'II6': 0.4, 'VIIm7': 0.4, 'Vmaj7': 0.2},
        'II6': {'Imaj7': 0.4, 'IIIm7': 0.4, 'VIm7': 0.2},
        'IIIm7': {'II6': 0.4, 'VIIm7': 0.4, 'VIm7': 0.2},
        'Vmaj7': {'VIm7': 0.4, 'II6': 0.4, 'IIIm7': 0.2},
        'VIm7': {'VIIm7': 0.4,  'Vmaj7': 0.4, 'IIIm7': 0.2},
        'VIIm7': {'VIm7': 0.4, 'Imaj7': 0.4,'IIIm7': 0.2}
    },
    'Mixolidio': {
        'I6/sus4': {'IIm7': 0.4, 'VIIbmaj7': 0.4, 'IVmaj7': 0.2},
        'IIm7': {'I6/sus4': 0.5, 'VIm7': 0.5},
        'IVmaj7': {'I6/sus4': 0.5, 'Vm7': 0.5},
        'Vm7': {'IVmaj7': 0.4, 'VIm7': 0.4, 'IIm7': 0.2},
        'VIm7': {'VIIbmaj7': 0.5,  'Vm7': 0.5},
        'VIIbmaj7': {'VIm7': 0.4, 'I6/sus4': 0.4,'IVmaj7': 0.2}
    },
    'Eolico': {
        'Im7': {'VIIb6': 0.5, 'Vm7': 0.5 },
        'IIIbmaj7': {'IVm7': 0.6, 'VIIb6': 0.2, 'VIbmaj7': 0.2},
        'IVm7': {'IIIbmaj7': 0.4, 'Vm7': 0.4, 'Im7': 0.2},
        'Vm7': {'VIbmaj7': 0.5, 'IVm7': 0.5, },
        'VIbmaj7': {'VIIb6': 0.4, 'Vm7': 0.4, 'IIIbmaj7': 0.2},
        'VIIb6': {'Im7': 0.4, 'VIbmaj7': 0.4, 'IVm7': 0.2}
    },
}

tonalidades_notas = {
    'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    'D': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
    'E': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
    'F': ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],
    'G': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
    'A': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
    'B': ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']
}




def romano_a_entero(numero_romano):
    dict_romano = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7}

    # Utilizamos una expresión regular para buscar el primer match de un número romano
    match = re.match(r'([IV]+)', numero_romano)
    if match:
        return dict_romano[match.group(1)]
    else:
        return None

def generar_progresion(modo, num_acordes, tonalidad):
    # Aseguramos que el primer acorde sea el acorde de tónica.
    acorde_actual = list(tabla_transiciones[modo].keys())[0]
    progresion = [acorde_actual]

    while len(progresion) < num_acordes:
        acordes_posibles = list(tabla_transiciones[modo][acorde_actual].keys())
        pesos = list(tabla_transiciones[modo][acorde_actual].values())

        # Generamos el próximo acorde y nos aseguramos de que no sea igual al acorde actual
        nuevo_acorde = random.choices(acordes_posibles, weights=pesos, k=1)[0]
        while nuevo_acorde == acorde_actual:
            nuevo_acorde = random.choices(acordes_posibles, weights=pesos, k=1)[0]

        acorde_actual = nuevo_acorde
        progresion.append(acorde_actual)

    progresion = [tonalidades_notas[tonalidad][romano_a_entero(acorde.split('/')[0]) - 1] + acorde[len(re.match(r'([IV]+)', acorde.split('/')[0]).group(0)):] if '/' in acorde else tonalidades_notas[tonalidad][romano_a_entero(acorde) - 1] + acorde[len(re.match(r'([IV]+)', acorde).group(0)):] for acorde in progresion]

    # Verificar y corregir accidentes contradictorios
    progresion_corregida = []
    for acorde in progresion:
        # Extraer la raíz y los caracteres después de la raíz
        raiz, resto = acorde[0], acorde[1:]

        # Verificar y corregir accidentes contradictorios
        if "b" in resto and "#" in resto:
            # Si hay un accidente contradictorio, eliminamos ambos caracteres
            resto = resto.replace("b", "").replace("#", "")

        # Combinamos la raíz corregida con el resto del acorde
        acorde_corregido = raiz + resto
        progresion_corregida.append(acorde_corregido)

    return progresion_corregida




# Código de Streamlit
st.sidebar.title('Generador de Progresiones modales por grados contiguos')

def main():
    tonalidad = st.sidebar.selectbox('Selecciona una tonalidad:', list(tonalidades_notas.keys()))
    modo = st.sidebar.selectbox('Selecciona un modo:', list(tabla_transiciones.keys()))
    num_acordes = st.sidebar.slider('Número de acordes:', min_value=1, max_value=64, value=16)
    
    # Agregamos los controles de tamaño de fuente y negritas
    tamano_fuente = st.sidebar.slider('Tamaño de fuente', 10, 50, 20)
    negritas = st.sidebar.checkbox('Negritas')

    # Genera la progresión automáticamente en cada renderizado de la aplicación
    progresion = generar_progresion(modo, num_acordes, tonalidad)

    # Aplicamos el estilo seleccionado a la progresión de acordes
    st.markdown(f"<div style='font-size: {tamano_fuente}px; {'font-weight: bold;' if negritas else ''}'>||: {' | '.join(progresion)} :||</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

if st.checkbox('Mostrar información acerca de esta app'):
    st.markdown("""
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

    

    """)

