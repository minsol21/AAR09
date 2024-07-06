import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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

    def sense(self):
        # Simulate perception with 10% noise
        perceived_color = self.world.tiles[self.position]
        if random.random() < 0.1:
            perceived_color = 1 - perceived_color  # Flip perception with 10% probability

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
        left_uncertainty = self.calculate_uncertainty(self.position, 'left')
        right_uncertainty = self.calculate_uncertainty(self.position, 'right')

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
        left_uncertainty = self.calculate_uncertainty(self.position, 'left')
        right_uncertainty = self.calculate_uncertainty(self.position, 'right')

        # Choose action based on maximum uncertainty
        if left_uncertainty > right_uncertainty:
            return -1  # Move left
        elif right_uncertainty > left_uncertainty:
            return 1  # Move right
        else:
            return random.choice([-1, 1])  # Random choice if uncertainty is equal

    def calculate_uncertainty(self, position, direction):
        if position < 0 or position >= self.world.length:
            return float('inf')  # High uncertainty if out of bounds

        if direction == 'left':
            left_position = position - 1
            right_position = position + 1
        else:  # direction == 'right'
            left_position = position - 1
            right_position = position + 1

        left_uncertainty = right_uncertainty = float('inf')

        if 0 <= left_position < self.world.length:
            left_mean = self.predict_color(left_position)
            left_total_count = max(1, sum(self.world_model[left_position]))
            left_variance = left_mean * (1 - left_mean) / left_total_count
            left_perceived_value = self.world.tiles[left_position]
            left_uncertainty = left_variance * abs(left_perceived_value - left_mean)

        if 0 <= right_position < self.world.length:
            right_mean = self.predict_color(right_position)
            right_total_count = max(1, sum(self.world_model[right_position]))
            right_variance = right_mean * (1 - right_mean) / right_total_count
            right_perceived_value = self.world.tiles[right_position]
            right_uncertainty = right_variance * abs(right_perceived_value - right_mean)

        # Assign weights to left and right uncertainties
        if direction == 'left':
            return 0.6 * left_uncertainty + 0.4 * right_uncertainty
        else:
            return 0.4 * left_uncertainty + 0.6 * right_uncertainty

    def move(self, action):
        # Simulate action with 10% noise
        if random.random() < 0.1:
            action = -action  # Flip action with 10% probability

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
    steps = 100

    # Initialize
    world = TileWorld(world_length)
    robot = Robot(world)

    # === Run the simulation === #
    strategy = 'adventurous'
    print("\nRunning the simulation with adventurous strategy... ")
    robot.run(steps, strategy)

    print("World Tiles:", world.tiles)
    print("Robot History:", robot.history)

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
    ax.text(0.5, 1.1, 'Adventurous Robot\nReal World Tiles: ' + str(world.tiles), transform=ax.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='center')
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

    plt.savefig(str(strategy)+'_robot_2')
    plt.tight_layout()
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()
