import pygame
import sys
import random
from game import Game
from ga import Population, Individual

# --- Configuración de la Visualización ---
# Si es True, se mostrará una simulación del mejor individuo de cada generación.
visualize_each_generation = True

# --- Parámetros del Algoritmo Genético ---
NUM_GENERATIONS = 50       # Número de ciclos de evolución.
POPULATION_SIZE = 500      # Número de población en cada generación.
MUTATION_RATE = 0.2         # Probabilidad de que una IA sufra una mutación aleatoria.
MUTATION_STRENGTH = 10.0   # Magnitud del cambio durante una mutación.

def run_best_individual_visual(game: Game, individual: Individual):
    """Ejecuta una simulación visual para ver jugar al mejor individuo de la generación."""
    global visualize_each_generation

    print("\n--- Mostrando al mejor individuo de la generación ---")
    print("Controles: [V] = Alternar Visualización | [->] = Acelerar | [<-] = Normal")
    game.reset_game()
    max_steps = 1000 # Límite de pasos para evitar bucles infinitos

    for step in range(max_steps):
        # Manejo de eventos de Pygame (cerrar ventana, teclas)
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
                elif event.key == pygame.K_v:
                    visualize_each_generation = not visualize_each_generation
                    mode_text = "Activada" if visualize_each_generation else "Desactivada"
                    print(f"\n>> Visualización por generación: {mode_text} <<\n")

        game_state = game.get_state()
        if not game_state['invader_alive']:
            break

        action = individual.decide_action(game_state['defender_x'], game_state['invader_x'])
        game_over, _, _ = game.game_step(action)
        
        game.render()
        
        if game_over:
            break
    
    pygame.time.wait(200)

def main():
    """Función principal que inicializa y ejecuta el algoritmo genético."""
    # Se requiere una semilla (seed) para inicializar el generador de números aleatorios.
    # Esto hace que los resultados del entrenamiento sean consistentes y reproducibles.
    seed = 0
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

    # Inicializar el juego y la población de IAs
    game = Game()
    population = Population(POPULATION_SIZE, MUTATION_RATE, MUTATION_STRENGTH)
    
    log_data = []

    # --- Bucle Principal de Evolución ---
    for gen in range(NUM_GENERATIONS):
        print(f"========== GENERACIÓN {gen + 1}/{NUM_GENERATIONS} ==========")
        
        # El corazón del AG: la población evoluciona para crear una nueva generación.
        outcomes = population.evolve(game)
        
        # Calcular y mostrar estadísticas de la generación
        win_rate = (outcomes.get('WIN', 0) / population.pop_size) * 100
        best_individual = population.individuals[0]
        
        print(f"Mejor Adaptación de la generación: {best_individual.adaptacion}")
        print(f"Tasa de Éxito de la generación: {win_rate:.1f}%")
        print(f"Mejor Cromosoma: {best_individual.chromosome}")
        
        # Guardar datos para el archivo de log
        log_line = f"Generación {gen + 1:02d}: Adaptación={best_individual.adaptacion:<22}, Tasa de Éxito={win_rate:.1f}%, Cromosoma={best_individual.chromosome}"
        log_data.append(log_line)

        # Si la visualización está activada, mostrar cómo juega el mejor individuo
        if visualize_each_generation:
            run_best_individual_visual(game, best_individual)

    print("\n--- Entrenamiento completado ---")

    # --- Guardar el Registro en un Archivo ---
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
    
    # --- Mostrar al Campeón Final en un Bucle Infinito ---
    final_best = population.individuals[0]
    print(f"\nMejor adaptación final encontrada: {final_best.adaptacion}")
    print(f"Mejor cromosoma final: {final_best.chromosome}")
    print("Mostrando al campeón final...")

    while True:
        run_best_individual_visual(game, final_best)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
