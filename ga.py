
import random
from game import Game

# Rango para los valores iniciales del gen
SHOOT_THRESHOLD_RANGE = [0, 100]

class Individual:
    """
    Representa un único individuo en la población del algoritmo genético.

    Atributos:
        chromosome (list): La lista de genes del individuo. En este caso, contiene solo un gen: el umbral de disparo.
        adaptacion (float): El valor de fitness del individuo. Se inicializa como infinito.
        puntuacion_acum (float): Un duplicado de `adaptacion` para reflejar el diseño original.
        es_elitista (bool): Una bandera que indica si el individuo es el mejor de su generación.
    """
    def __init__(self):
        """Inicializa un nuevo individuo con un cromosoma aleatorio."""
        self.chromosome = [random.uniform(SHOOT_THRESHOLD_RANGE[0], SHOOT_THRESHOLD_RANGE[1])]
        self.adaptacion = float('inf')
        self.puntuacion_acum = float('inf') # Duplicado de adaptacion para reflejar el diseño
        self.es_elitista = False # Bandera para marcar al mejor individuo

    def decide_action(self, defender_x, invader_x):
        """
        Decide la próxima acción del defensor basándose en las posiciones del defensor y del invasor.

        Args:
            defender_x (int): La posición x del defensor.
            invader_x (int): La posición x del invasor.

        Returns:
            int: La acción a realizar (0: izquierda, 1: derecha, 2: disparar).
        """
        shoot_threshold = self.chromosome[0]
        delta_x = defender_x - invader_x

        if abs(delta_x) < shoot_threshold:
            return 2  # Disparar
        elif delta_x > 0:
            return 0  # Moverse a la izquierda para alinearse
        else:
            return 1  # Moverse a la derecha para alinearse

    def calculate_fitness(self, game_instance: Game):
        """
        Calcula el fitness del individuo simulando una partida del juego.

        Args:
            game_instance (Game): Una instancia del juego para simular.
        """
        game_instance.reset_game()
        total_fitness = 0
        max_steps = 500

        for step in range(max_steps):
            game_state = game_instance.get_state()
            if not game_state['invader_alive']:
                break

            action = self.decide_action(game_state['defender_x'], game_state['invader_x'])
            
            game_over, fitness_delta = game_instance.game_step(action)
            total_fitness += fitness_delta

            if game_over:
                break
        
        self.adaptacion = total_fitness
        self.puntuacion_acum = total_fitness # Mantener el valor sincronizado

class Population:
    """
    Representa una población de individuos en el algoritmo genético.

    Atributos:
        individuals (list): Una lista de objetos `Individual`.
        pop_size (int): El número de individuos en la población.
        mutation_rate (float): La probabilidad de que ocurra una mutación en un individuo.
        mutation_strength (float): La magnitud máxima del cambio durante la mutación.
    """
    def __init__(self, pop_size, mutation_rate=0.1, mutation_strength=5.0):
        """
        Inicializa una nueva población de individuos.

        Args:
            pop_size (int): El tamaño de la población.
            mutation_rate (float): La tasa de mutación.
            mutation_strength (float): La fuerza de la mutación.
        """
        self.individuals = [Individual() for _ in range(pop_size)]
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength

    def evaluate(self, game_instance: Game):
        """
        Evalúa el fitness de cada individuo en la población.

        Args:
            game_instance (Game): La instancia del juego utilizada para la evaluación.
        """
        for individual in self.individuals:
            individual.calculate_fitness(game_instance)

    def select(self):
        """
        Selecciona un individuo de la población mediante selección por torneo.

        Returns:
            Individual: El individuo seleccionado.
        """
        tournament_size = 3
        competitors = random.sample(self.individuals, tournament_size)
        competitors.sort(key=lambda ind: ind.adaptacion) # Usar .adaptacion
        return competitors[0]

    def crossover(self, parent1: Individual, parent2: Individual):
        """
        Realiza un cruce entre dos padres para crear un nuevo individuo (hijo).

        Args:
            parent1 (Individual): El primer padre.
            parent2 (Individual): El segundo padre.

        Returns:
            Individual: El individuo hijo resultante del cruce.
        """
        child = Individual()
        child.chromosome[0] = (parent1.chromosome[0] + parent2.chromosome[0]) / 2.0
        return child

    def mutate(self, individual: Individual):
        """
        Aplica una mutación al cromosoma de un individuo.

        Args:
            individual (Individual): El individuo a mutar.
        """
        if random.random() < self.mutation_rate:
            change = random.uniform(-self.mutation_strength, self.mutation_strength)
            individual.chromosome[0] += change
            individual.chromosome[0] = max(SHOOT_THRESHOLD_RANGE[0], min(individual.chromosome[0], SHOOT_THRESHOLD_RANGE[1]))

    def evolve(self, game_instance: Game):
        """
        Evoluciona la población a la siguiente generación.

        Args:
            game_instance (Game): La instancia del juego utilizada para la evaluación.
        """
        # Resetear la bandera de elitismo de la generación anterior
        for ind in self.individuals:
            ind.es_elitista = False

        self.evaluate(game_instance)
        self.individuals.sort(key=lambda ind: ind.adaptacion) # Usar .adaptacion

        new_population = []
        
        # Marcar y preservar al mejor individuo (elitismo)
        best_individual = self.individuals[0]
        best_individual.es_elitista = True
        new_population.append(best_individual)

        while len(new_population) < self.pop_size:
            parent1 = self.select()
            parent2 = self.select()
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_population.append(child)
            
        self.individuals = new_population
