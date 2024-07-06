import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class TileWorld:
    def __init__(self, length):
        #Initialize the world with random black(0) and white(1) tiles
        self.tiles = [random.choice([0,1]) for _ in range(length)]
        self.length = length


class Robot:
    def __init__(self, world):
        self.world = world
        self.position = random.randint(0, self.world.length - 1)
        self.world_model = {}
        for i in range(self.world.length):
            self.world_model[i] = [0,0] # Histogram: [black_count, white_count]
        self.history = []
        self.exploration_phase = True
        self.exploration_steps = 30

    def sense(self):
        current_tile = self.world.tiles[self.position]
        self.world_model[self.position][current_tile] += 1
        self.history.append(self.position)

    def predict_color(self, position):
        counts = self.world_model[position]
        total_counts = sum(counts)
        if total_counts == 0:
            return 0.5 # Equal probability if no data
        else:
            p = counts[1] / total_counts #probability of the tile being white
            return p
    

    def choose_action(self):
        # Exploration phase to encourage visiting new positions
        if self.exploration_phase:
            if self.exploration_steps > 0:
                self.exploration_steps -= 1
                return random.choice([-1, 1])
            else:
                self.exploration_phase = False

        if self.position == 0:
            return 1 # Move right if at the left edge
        elif self.position == self.world.length - 1:
            return -1 # Move left if at the right edge

        left_counts = self.world_model[self.position -1]
        right_counts = self.world_model[self.position +1]

        # Certainty is the maximum count divided by the total counts at the position
        if sum(left_counts) > 0:
            left_certainty = max(left_counts) / sum(left_counts)
        else:
            left_certainty = 0.5 #Default certainty if no data
        
        if sum(right_counts) > 0:
            right_certainty = max(right_counts) / sum(right_counts)
        else:
            right_certainty = 0.5
        
        # Choose the direction with higher certainty
        if left_certainty > right_certainty:
            return -1 # Move elft
        if right_certainty > left_certainty:
            return 1 # Move right
        else:
            return random.choice([-1,1]) # Random choice if certainty is equal
        
    
    def move(self, action):
        self.position += action
        self.position = max(0, min(self.position, self.world.length - 1))

    def run(self, steps):
        for _ in range(steps):
            self.sense()
            action = self.choose_action()
            self.move(action)

    @staticmethod
    def generate_samples(mean, variance, size=1000):
        if variance == 0:
            variance = 0.0001  # Set a small variance if it is zero
        stddev = np.sqrt(variance)
        return np.random.normal(mean, stddev, size)

def main():
    # Parameters
    world_length = 6
    steps = 100

    # Initialize
    world = TileWorld(world_length)
    robot = Robot(world)

    # Run the simulation
    robot.run(steps)
    print("Running the simulation ... ")

    print("World Tiles:", world.tiles)
    print("Robot History:", robot.history)
    print("World Model:")
    
    for pos, hist in robot.world_model.items():
        print(f"Position {pos}: Black count = {hist[0]}, White count = {hist[1]}")

    # Print final predictions and variances
    print("\nFinal Predictions and Variances:")
    means = []
    variances = []
    for pos in range(world_length):
        black_count, white_count = robot.world_model[pos]
        total_count = black_count + white_count
        if total_count == 0:
            mean = 0.5
            variance = 0.25
        else:
            mean = white_count / total_count
            variance = mean * (1 - mean) / total_count
        means.append(mean)
        variances.append(variance)
        print(f"Position {pos}: Mean = {mean:.3f}, Variance = {variance:.3f}")


    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    #===== Plot the histogram of black and white tile counts for each index ====#
    ax = axes[0]
    width = 0.35  # width of the bars
    x = np.arange(world_length)
    black_counts = [robot.world_model[i][0] for i in range(world_length)]
    white_counts = [robot.world_model[i][1] for i in range(world_length)]
    ax.bar(x - width/2, black_counts, width, color='black', label='Black')
    ax.bar(x + width/2, white_counts, width, color='white', edgecolor='black', label='White')
    ax.set_xlabel('Tile Index')
    ax.set_ylabel('Count')
    ax.set_title('Histogram of Black and White Tile Counts', fontsize=16, fontweight='bold', pad=40)
    ax.text(0.5, 1.1, 'General Robot\nReal World Tiles: ' + str(world.tiles), transform=ax.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='center')
    #ax.set_title('Histogram of Black and White Tile Counts\nnReal World Tiles: ' + str(world.tiles))
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    ax.legend()

    #====== Plot the distribution of mean predictions across tile indices =====#
    # Generate sample data for KDE plots
    samples = [Robot.generate_samples(mean, var) for mean, var in zip(means, variances)]
    ax = axes[1]

    # Plotting KDE for each tile index
    for index, sample in enumerate(samples):
        sns.kdeplot(sample, label=f'Tile {index}', linewidth=2)

    ax.set_xlabel('Mean Prediction')
    ax.set_ylabel('Density')
    ax.set_title('Distribution of Mean Predictions for Each Tile Index', fontsize=16, fontweight='bold')
    ax.legend()

    # Set x-axis limits
    ax.set_xlim(-0.5, 1.5)

    plt.savefig('general_robot')
    plt.tight_layout()
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()






        
