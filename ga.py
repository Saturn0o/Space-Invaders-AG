import random
from game import Game, GRID_WIDTH

# Rango para el gen del umbral de disparo.
SHOOT_THRESHOLD_RANGE = [0, GRID_WIDTH]

class Individual:
    """Representa una única "IA" o "jugador" con su propia estrategia de juego (cromosoma)."""
    def __init__(self):
        # El cromosoma define el comportamiento de la IA.
        # Gen 0: Umbral de Disparo (distancia para decidir disparar).
        # Gen 1: Tendencia a Esquivar (probabilidad de moverse aleatoriamente).
        self.chromosome = [
            random.uniform(SHOOT_THRESHOLD_RANGE[0], SHOOT_THRESHOLD_RANGE[1]),
            random.uniform(0, 1)
        ]
        # La adaptación (fitness) mide qué tan bien jugó el individuo.
        self.adaptacion = -float('inf')
        self.puntuacion_acum = -float('inf')
        self.es_elitista = False

    def decide_action(self, defender_x, invader_x):
        # El "cerebro" de la IA: decide la próxima acción basándose en su estrategia.
        shoot_threshold, dodge_tendency = self.chromosome
        delta_x = defender_x - invader_x

        # Con una cierta probabilidad, la IA se moverá a un lado para ser menos predecible.
        if random.random() < dodge_tendency:
            return random.choice([0, 1])

        # Si el invasor está lo suficientemente cerca, dispara. Si no, se alinea.
        if abs(delta_x) < shoot_threshold:
            return 2  # Disparar
        elif delta_x > 0:
            return 0  # Moverse a la izquierda
        else:
            return 1  # Moverse a la derecha

    def calculate_fitness(self, game_instance: Game):
        """Calcula el fitness del individuo simulando una partida completa."""
        game_instance.reset_game()
        total_fitness = 0
        max_steps = 500 # Límite para evitar partidas infinitas
        outcome = 'TIMEOUT'

        # Simular la partida paso a paso
        for step in range(max_steps):
            game_state = game_instance.get_state()
            if not game_state['invader_alive']:
                outcome = 'WIN' # Si no hay invasores, es una victoria
                break

            action = self.decide_action(game_state['defender_x'], game_state['invader_x'])
            
            game_over, fitness_delta, game_result = game_instance.game_step(action)
            total_fitness += fitness_delta

            if game_over:
                outcome = game_result
                break
        
        self.adaptacion = total_fitness
        self.puntuacion_acum = total_fitness
        return outcome

class Population:
    """Representa un conjunto de individuos (IAs) que evolucionan juntos."""
    def __init__(self, pop_size, mutation_rate=0.1, mutation_strength=5.0):
        self.individuals = [Individual() for _ in range(pop_size)]
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength

    def evaluate(self, game_instance: Game):
        """Evalúa a toda la población y devuelve estadísticas de los resultados."""
        outcomes = {'WIN': 0, 'LOSS_BOMB': 0, 'LOSS_INVADER': 0, 'TIMEOUT': 0}
        for individual in self.individuals:
            result = individual.calculate_fitness(game_instance)
            if result in outcomes:
                outcomes[result] += 1
        return outcomes

    def select(self):
        """Selecciona a un padre para la siguiente generación mediante selección por torneo."""
        tournament_size = 5 # Un torneo más grande aumenta la presión de selección
        competitors = random.sample(self.individuals, tournament_size)
        competitors.sort(key=lambda ind: ind.adaptacion, reverse=True)
        return competitors[0]

    def crossover(self, parent1: Individual, parent2: Individual):
        """Crea un hijo combinando los cromosomas de dos padres (promedio simple)."""
        child = Individual()
        child.chromosome[0] = (parent1.chromosome[0] + parent2.chromosome[0]) / 2.0
        child.chromosome[1] = (parent1.chromosome[1] + parent2.chromosome[1]) / 2.0
        return child

    def mutate(self, individual: Individual):
        """Aplica una pequeña variación aleatoria (mutación) a los genes de un individuo."""
        if random.random() < self.mutation_rate:
            change = random.uniform(-self.mutation_strength, self.mutation_strength)
            individual.chromosome[0] += change
            individual.chromosome[0] = max(SHOOT_THRESHOLD_RANGE[0], min(individual.chromosome[0], SHOOT_THRESHOLD_RANGE[1]))

        if random.random() < self.mutation_rate:
            change = random.uniform(-0.1, 0.1)
            individual.chromosome[1] += change
            individual.chromosome[1] = max(0, min(individual.chromosome[1], 1))

    def evolve(self, game_instance: Game):
        """Realiza un ciclo completo de evolución para crear la siguiente generación."""
        # 1. Evaluar a toda la población actual y obtener los resultados.
        outcomes = self.evaluate(game_instance)
        
        # 2. Ordenar la población por fitness (los mejores primero).
        self.individuals.sort(key=lambda ind: ind.adaptacion, reverse=True)

        new_population = []
        
        # 3. Elitismo: El mejor individuo pasa directamente a la siguiente generación.
        #    Esto asegura que la mejor solución encontrada nunca se pierda.
        best_individual = self.individuals[0]
        best_individual.es_elitista = True
        new_population.append(best_individual)

        # 4. Crear el resto de la nueva población mediante cruce y mutación.
        while len(new_population) < self.pop_size:
            parent1 = self.select()
            parent2 = self.select()
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_population.append(child)
            
        self.individuals = new_population
        
        # 5. Devolver las estadísticas de la generación que acaba de ser evaluada.
        return outcomes