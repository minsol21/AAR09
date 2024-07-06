import random

class TileWorld:
    def __init__(self, length):
        self.tiles = [random.choice([0, 1]) for _ in range(length)]
        self.length = length

    def get_tiles(self):
        return self.tiles


class Robot:
    def __init__(self, world):
        self.world = world
        self.position = random.randint(0, self.world.length - 1)
        self.world_model = {i: (1, 1) for i in range(self.world.length)}  # Initial Beta parameters (alpha, beta)
        self.history = []

    def sense(self):
        true_color = self.world.tiles[self.position]
        measured_color = true_color if random.random() > 0.1 else 1 - true_color  # 10% noise
        self.update_belief(measured_color)

    def update_belief(self, color):
        alpha, beta = self.world_model[self.position]
        if color == 0:
            self.world_model[self.position] = (alpha + 1, beta)
        else:
            self.world_model[self.position] = (alpha, beta + 1)

    def predict_color(self, position):
        alpha, beta = self.world_model[position]
        return alpha / (alpha + beta)

    def calculate_uncertainty(self, position):
        alpha, beta = self.world_model[position]
        mean = alpha / (alpha + beta)
        variance = (alpha * beta) / (((alpha + beta) ** 2) * (alpha + beta + 1))
        return variance

    def choose_action(self, strategy='cautious'):
        if self.position == 0:
            return 1
        elif self.position == self.world.length - 1:
            return -1

        left_uncertainty = self.calculate_uncertainty(self.position - 1)
        right_uncertainty = self.calculate_uncertainty(self.position + 1)

        if strategy == 'cautious':
            if left_uncertainty < right_uncertainty:
                return -1
            elif right_uncertainty < left_uncertainty:
                return 1
            else:
                return random.choice([-1, 1])
        elif strategy == 'adventurous':
            if left_uncertainty > right_uncertainty:
                return -1
            elif right_uncertainty > left_uncertainty:
                return 1
            else:
                return random.choice([-1, 1])
        else:
            raise ValueError("Unknown strategy. Choose 'cautious' or 'adventurous'.")

    def move(self, action):
        self.position += action
        self.position = max(0, min(self.position, self.world.length - 1))
        self.history.append(self.position)

    def run(self, steps, strategy='cautious'):
        for _ in range(steps):
            self.sense()
            action = self.choose_action(strategy)
            self.move(action)

def main():
    # Parameters
    world_length = 10
    steps = 100
    noise_levels = [0, 0.1, 0.4]
    strategies = ['cautious', 'adventurous']

    for noise in noise_levels:
        print(f"Running simulations with {noise*100}% noise...\n")
        for strategy in strategies:
            print(f"\n\nStrategy: {strategy}")
            # Initialize
            world = TileWorld(world_length)
            robot = Robot(world)

            # Run simulation
            robot.run(steps, strategy)

            # Print actual world state
            print(f"Actual World State: {world.get_tiles()}")

            # Compute final beliefs
            final_beliefs = {}
            for pos in range(world_length):
                alpha, beta = robot.world_model[pos]
                mean = alpha / (alpha + beta)
                variance = (alpha * beta) / (((alpha + beta) ** 2) * (alpha + beta + 1))
                final_beliefs[pos] = (mean, variance)

            # Print final beliefs
            for pos in range(world_length):
                mean, variance = final_beliefs[pos]
                print(f"Position {pos}: Mean = {mean:.3f}, Variance = {variance:.3f}")
            

            

if __name__ == "__main__":
    main()
