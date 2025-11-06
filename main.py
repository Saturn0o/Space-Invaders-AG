import pygame
import sys
import random
from game import Game
from ga import Population, Individual

# --- Modo de Visualización (se puede cambiar durante la ejecución) ---
visualize_each_generation = True

# --- Constantes del Algoritmo Genético ---
NUM_GENERATIONS = 50
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
MUTATION_STRENGTH = 5.0

def run_best_individual_visual(game: Game, individual: Individual):
    """
    Ejecuta una simulación visual para un individuo específico, mostrando cómo juega.

    Esta función permite la interacción del usuario para acelerar, ralentizar o
    alternar el modo de visualización de las generaciones futuras.

    Args:
        game (Game): La instancia del juego en la que se ejecutará la simulación.
        individual (Individual): El individuo del algoritmo genético que controlará al defensor.

    Globales:
        visualize_each_generation (bool): Modifica esta variable global para controlar
                                         si las generaciones futuras se visualizan o no.
    """
    global visualize_each_generation # Necesitamos modificar la variable global

    print("\n--- Mostrando al mejor individuo de la generación ---")
    print("Controles: [V] = Alternar Visualización | [->] = Acelerar | [<-] = Normal")
    game.reset_game()
    max_steps = 1000

    for step in range(max_steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    print(">> Velocidad acelerada")
                    game.speed_up()
                elif event.key == pygame.K_LEFT:
                    print(">> Velocidad normal")
                    game.normal_speed()
                elif event.key == pygame.K_v: # Botón para alternar visualización
                    visualize_each_generation = not visualize_each_generation
                    mode_text = "Activada" if visualize_each_generation else "Desactivada"
                    print(f"\n>> Visualización por generación: {mode_text} <<\n")

        game_state = game.get_state()
        if not game_state['invader_alive']:
            break

        action = individual.decide_action(game_state['defender_x'], game_state['invader_x'])
        game_over, _ = game.game_step(action)
        
        game.render()
        
        if game_over:
            print(f"Simulación terminada en {step} pasos.")
            break
    
    pygame.time.wait(200) # Pausa más corta

def main():
    """
    Punto de entrada principal para entrenar y ejecutar la IA de Space Invaders
    utilizando un algoritmo genético.

    El programa requiere una semilla numérica como argumento de línea de comandos para
    inicializar el generador de números aleatorios, asegurando la reproducibilidad.

    El proceso de entrenamiento evoluciona una población de individuos a lo largo de
    varias generaciones. Al final del entrenamiento, guarda un registro de los
    resultados y muestra al mejor individuo (campeón) en un bucle infinito.
    """
    seed = 0 # Valor por defecto
    if len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
            random.seed(seed)
            print(f"--- Usando semilla aleatoria: {seed} ---")
        except ValueError:
            print("--- Error: La semilla debe ser un número entero. ---")
            sys.exit()
    else:
        print("--- Error: Debes proporcionar una semilla para iniciar. ---")
        print("Uso: python main.py <numero_de_semilla>")
        sys.exit()

    game = Game()
    
    population = Population(POPULATION_SIZE, MUTATION_RATE, MUTATION_STRENGTH)
    
    log_data = [] # Lista para guardar el registro

    for gen in range(NUM_GENERATIONS):
        print(f"========== GENERACIÓN {gen + 1}/{NUM_GENERATIONS} ==========")
        
        population.evolve(game)
        
        best_individual = population.individuals[0] # La población ya está ordenada
        print(f"Mejor Adaptación de la generación: {best_individual.adaptacion}")
        print(f"Mejor Umbral de Disparo: {best_individual.chromosome[0]}")
        
        # Guardar en la lista de registro
        log_line = f"Generación {gen + 1:02d}: Adaptación={best_individual.adaptacion:<22}, Umbral={best_individual.chromosome[0]}"
        log_data.append(log_line)

        if visualize_each_generation:
            run_best_individual_visual(game, best_individual)

    print("\n--- Entrenamiento completado ---")

    # --- GUARDAR REGISTRO EN ARCHIVO ---
    log_filename = f"log_semilla_{seed}.txt"
    log_content = "\n".join(log_data)
    try:
        with open(log_filename, "w") as f:
            f.write(f"Resultados para la semilla: {seed}\n")
            f.write("="*50 + "\n")
            f.write(log_content)
        print(f"\nRegistro de la ejecución guardado en: {log_filename}")
    except IOError as e:
        print(f"\nError al guardar el registro: {e}")
    
    final_best = population.individuals[0]
    print(f"\nMejor adaptación final encontrada: {final_best.adaptacion}")
    print(f"Mejor umbral de disparo final: {final_best.chromosome[0]}")
    print("Mostrando al campeón final...")

    while True:
        run_best_individual_visual(game, final_best)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()