
# Space Invaders - IA con Algoritmo Genético

Este proyecto es una simulación del clásico juego "Space Invaders" desarrollada con Pygame, donde la nave defensora es controlada por una inteligencia artificial basada en un Algoritmo Genético (AG).

El objetivo del proyecto es demostrar cómo un AG puede evolucionar una estrategia reactiva para resolver un problema simple en un entorno de juego.

## Características

-   **Inteligencia Artificial Reactiva:** La IA no sigue una secuencia de movimientos fija, sino que reacciona a la posición del enemigo en tiempo real.
-   **Algoritmo Genético:** El "cerebro" de la IA (sus parámetros de decisión) evoluciona a lo largo de las generaciones para optimizar su comportamiento.
-   **Simulación con Pygame:** El entorno del juego está construido con la popular librería Pygame.
-   **Controles Interactivos:** Permite modificar la visualización y la velocidad del juego durante la ejecución.
-   **Registro de Experimentos:** Guarda automáticamente un log de cada ejecución para su posterior análisis.

## Requisitos

-   Python 3.x
-   Pygame

## Instalación y Setup

1.  **Clonar o descargar el proyecto.**

2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    ```

3.  **Activar el entorno virtual:**
    -   En Windows:
        ```powershell
        .\venv\Scripts\activate
        ```
    -   En macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Instalar las dependencias:**
    ```bash
    pip install pygame
    ```

## Cómo Ejecutar

Para ejecutar el programa, es **obligatorio** proporcionar una **semilla numérica** como argumento en la línea de comandos. Esto asegura que los resultados de cada ejecución sean replicables.

**Ejemplo de ejecución:**
```bash
python main.py 123
```
(Puedes usar cualquier número entero como semilla).

## Interacción durante el Juego

Mientras se está visualizando la partida de un individuo, puedes usar las siguientes teclas:

-   `V`: **Alternar Visualización:** Activa o desactiva la visualización para las generaciones futuras. Es útil para acelerar el entrenamiento.
-   `Flecha Derecha`: **Acelerar:** Aumenta la velocidad de la simulación visual.
-   `Flecha Izquierda`: **Velocidad Normal:** Devuelve la simulación a su velocidad normal.

## Estructura del Proyecto

-   `main.py`: El punto de entrada del programa. Gestiona el bucle de generaciones, la visualización y la interacción del usuario.
-   `ga.py`: Contiene toda la lógica del Algoritmo Genético. Define las clases `Individual` (el "cerebro" reactivo) y `Population` (el motor de la evolución).
-   `game.py`: Define la lógica y las reglas del juego con Pygame. Contiene las clases `Game`, `Defender`, `Invader`, `Missile` y `Bomb`.
-   `*.png`: Archivos de imagen para los sprites y el fondo.

> **Nota:** Todo el código fuente (`.py`) ha sido documentado con docstrings para facilitar su comprensión y mantenimiento.

## Registro de Resultados

Al finalizar las N generaciones, el programa creará automáticamente un archivo de texto llamado `log_semilla_XXX.txt`, donde `XXX` es la semilla utilizada. Este archivo contiene un resumen del `fitness` y el `umbral de disparo` del mejor individuo de cada generación, permitiendo un análisis detallado del proceso de aprendizaje.
