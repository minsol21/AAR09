import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import beta

class TileWorld:
    def __init__(self, length):
        # Initialize the world with random black(0) and white(1) tiles
        self.tiles = [random.choice([0, 1]) for _ in range(length)]
        self.length = length

class Robot:
    def __init__(self, world):
        self.world = world
        self.position = random.randint(0, self.world.length - 1)
        self.world_model = {i: [0, 0] for i in range(self.world.length)}  # Histogram: [black_count, white_count]
        self.history = []

        # Initialize noise level (default 0%)
        self.noise_level = 0.0

    def set_noise_level(self, noise_level):
        if noise_level not in [0.0, 0.1, 0.4]:
            raise ValueError("Noise level must be 0.0 (no noise), 0.1 (10% noise), or 0.4 (40% noise).")
        self.noise_level = noise_level

    def sense(self):
        # Simulate perception with noise based on self.noise_level
        # Noise of perception
        perceived_color = self.world.tiles[self.position]
        
        if self.noise_level == 0.1:
            if random.random() < 0.1:
                perceived_color = 1 - perceived_color  # Flip perception with 10% probability
        elif self.noise_level == 0.4:
            if random.random() < 0.4:
                perceived_color = 1 - perceived_color  # Flip perception with 40% probability
        
        # Update the histogram for the current position
        if perceived_color == 0:
            self.world_model[self.position][0] += 1
        else:
            self.world_model[self.position][1] += 1

        self.history.append(self.position)

    def predict_color(self, position):
        black_count, white_count = self.world_model[position]
        total_count = black_count + white_count
        if total_count == 0:
            return 0.5  # Initial prediction when no data
        else:
            return white_count / total_count

    def choose_action(self, strategy='cautious'):
        if strategy == 'cautious':
            return self.cautious_strategy()
        elif strategy == 'adventurous':
            return self.adventurous_strategy()
        else:
            raise ValueError("Unknown strategy. Choose 'cautious' or 'adventurous'.")

    def cautious_strategy(self):
        if self.position == 0:
            return 1  # Move right if at the left edge
        elif self.position == self.world.length - 1:
            return -1  # Move left if at the right edge

        # Calculate uncertainty for left and right actions
        left_uncertainty = self.calculate_uncertainty(self.position - 1)
        right_uncertainty = self.calculate_uncertainty(self.position + 1)

        # Choose action based on minimum uncertainty
        if left_uncertainty < right_uncertainty:
            return -1  # Move left
        elif right_uncertainty < left_uncertainty:
            return 1  # Move right
        else:
            return random.choice([-1, 1])  # Random choice if uncertainty is equal

    def adventurous_strategy(self):
        if self.position == 0:
            return 1  # Move right if at the left edge
        elif self.position == self.world.length - 1:
            return -1  # Move left if at the right edge

        # Calculate uncertainty for left and right actions
        left_uncertainty = self.calculate_uncertainty(self.position - 1)
        right_uncertainty = self.calculate_uncertainty(self.position + 1)

        # Choose action based on maximum uncertainty
        if left_uncertainty > right_uncertainty:
            return -1  # Move left
        elif right_uncertainty > left_uncertainty:
            return 1  # Move right
        else:
            return random.choice([-1, 1])  # Random choice if uncertainty is equal

    def calculate_uncertainty(self, position):
        # Calculate uncertainty using beta distribution variance
        if position < 0 or position >= self.world.length:
            return float('inf')  # High uncertainty if out of bounds

        black_count, white_count = self.world_model[position]
        total_count = black_count + white_count
        if total_count == 0:
            return 0.25  # Maximum uncertainty when no data
        p = white_count / total_count
        variance = beta.mean(white_count + 1, black_count + 1) * (1 - beta.mean(white_count + 1, black_count + 1)) / (1 + white_count + black_count)
        return variance

    def move(self, action):
        # Simulate action with noise
        if random.random() < self.noise_level:
            action = -action  # Flip action with probability equal to noise level

        self.position += action
        self.position = max(0, min(self.position, self.world.length - 1))

    def run(self, steps, strategy='cautious'):
        for _ in range(steps):
            self.sense()
            action = self.choose_action(strategy)
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
    steps = 40
    noise_levels = [0.0, 0.1, 0.4]  # Noise levels for perception

    # Initialize
    world = TileWorld(world_length)
    robot = Robot(world)

    # Run simulations for each noise level and strategy
    for noise_level in noise_levels:
        robot.set_noise_level(noise_level)

        for strategy in ['cautious', 'adventurous']:
            print(f"\nRunning the simulation with {strategy} strategy and {noise_level * 100}% noise... ")
            robot.run(steps, strategy)

            print("World Tiles:", world.tiles)
            #print("Robot History:", robot.history)

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
                    variance = beta.mean(white_count + 1, black_count + 1) * (1 - beta.mean(white_count + 1, black_count + 1)) / (1 + white_count + black_count)
                means.append(mean)
                variances.append(variance)
                print(f"Position {pos}: Mean = {mean:.3f}, Variance = {variance:.3f}")

            # Create subplots for histograms and KDE plots
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
            ax.set_title(f'Histogram of Black and White Tile Counts (Noise {noise_level * 100}%)', fontsize=16, fontweight='bold', pad=40)
            ax.text(0.5, 1.1, f'{strategy.capitalize()} Robot\nReal World Tiles: ' + str(world.tiles), transform=ax.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='center')
            ax.set_xticks(x)
            ax.set_xticklabels(x)
            ax.legend()

            #====== Plot the distribution of mean predictions across tile indices =====#
            ax = axes[1]

            # Plotting KDE for each tile index
            for index, (mean, variance) in enumerate(zip(means, variances)):
                samples = Robot.generate_samples(mean, variance)
                sns.kdeplot(samples, label=f'Tile {index}', linewidth=2)

            ax.set_xlabel('Mean Prediction')
            ax.set_ylabel('Density')
            ax.set_title(f'Distribution of Mean Predictions for Each Tile Index (Noise {noise_level * 100}%)', fontsize=16, fontweight='bold')
            ax.legend()

            # Set x-axis limits
            ax.set_xlim(-0.5, 1.5)

            plt.tight_layout()
            plt.savefig(f'{strategy}_{int(noise_level * 100)}_noise.png')
            plt.show()

# Run the main function
if __name__ == "__main__":
    main()
