# Space Invaders con Algoritmo Genético

## Descripción

Este proyecto utiliza un algoritmo genético para entrenar a una inteligencia artificial (IA) para jugar al clásico juego de Space Invaders. El objetivo es que la IA aprenda por sí misma la mejor estrategia para esquivar las bombas de los invasores y dispararles para ganar puntos.

## Cómo Jugar

Para ejecutar el proyecto, necesitas tener Python y Pygame instalados.

1.  **Instala Pygame:**
    ```bash
    pip install pygame
    ```

2.  **Ejecuta el programa:**
    Abre una terminal o línea de comandos, navega hasta la carpeta del proyecto y ejecuta el siguiente comando:
    ```bash
    python main.py <numero_de_semilla>
    ```
    Reemplaza `<numero_de_semilla>` con cualquier número entero. Este número se utiliza para inicializar el generador de números aleatorios, lo que permite que los resultados del entrenamiento sean reproducibles. Por ejemplo:
    ```bash
    python main.py 42
    ```

## ¿Qué es un Algoritmo Genético?

Un algoritmo genético es una técnica de IA inspirada en el proceso de selección natural de Charles Darwin. Funciona de la siguiente manera:

1.  **Población Inicial:** Se crea una "población" de "individuos". En nuestro caso, cada individuo es una IA con una estrategia de juego ligeramente diferente (un "cromosoma" que define su comportamiento).

2.  **Evaluación (Fitness):** Cada individuo juega una partida de Space Invaders y se le asigna una puntuación de "adaptación" (fitness) basada en su rendimiento. ¡Cuanto mejor jueguen, mayor será su puntuación!

3.  **Selección:** Los individuos con las mejores puntuaciones son "seleccionados" para reproducirse. Esto es similar a la "supervivencia del más apto".

4.  **Cruce (Crossover):** Los individuos seleccionados se "cruzan" para crear nuevos individuos (descendencia). La descendencia hereda una combinación de las estrategias de sus padres.

5.  **Mutación:** Para introducir nuevas estrategias y evitar que la población se estanque, algunos de los nuevos individuos sufren una "mutación" aleatoria en su estrategia.

Este ciclo de evaluación, selección, cruce y mutación se repite durante muchas "generaciones". Con el tiempo, la población evoluciona y produce individuos cada vez mejores en el juego.

## Controles de Visualización

Durante la ejecución, puedes usar las siguientes teclas para controlar la visualización:

-   `V`: Activa o desactiva la visualización de la partida del mejor individuo de cada generación.
-   `Flecha Derecha`: Acelera la visualización.
-   `Flecha Izquierda`: Vuelve a la velocidad normal.

## Entendiendo los Resultados

Al final de cada ejecución, se genera un archivo `log_semilla_<numero>.txt` que contiene los resultados del entrenamiento. Cada línea del registro muestra:

-   **Generación:** El número de la generación.
-   **Adaptación:** La puntuación de fitness del mejor individuo de esa generación.
-   **Cromosoma:** La "estrategia" del mejor individuo. En este proyecto, el cromosoma tiene dos valores:
    -   **Umbral de Disparo:** Define qué tan cerca debe estar el invasor para que la IA decida disparar.
    -   **Tendencia a Esquivar:** Una probabilidad que determina si la IA hará un movimiento aleatorio para ser menos predecible.

Observando cómo cambian la adaptación y el cromosoma a lo largo de las generaciones, puedes ver cómo la IA "aprende" y mejora su estrategia de juego.