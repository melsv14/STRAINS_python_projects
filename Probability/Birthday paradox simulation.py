import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, norm


def birthday_simulation(num_people, num_simulations):
    success_count = 0
    results = []

    for _ in range(num_simulations):
        birthdays = np.random.randint(0, 365, num_people)
        if len(set(birthdays)) < num_people:
            success_count += 1
        results.append(success_count / (len(results) + 1))

    return results


# Parameters
num_people = 23
num_simulations = 1000

# Run the simulation
simulation_results = birthday_simulation(num_people, num_simulations)

# Visualize the results
plt.hist(simulation_results, bins=30, color='blue', edgecolor='black', alpha=0.7, density=True)

# Fit a normal distribution to the data
(mu, sigma) = norm.fit(simulation_results)

# Plot the fitted distribution
x = np.linspace(min(simulation_results), max(simulation_results), 100)
p = norm.pdf(x, mu, sigma)
plt.plot(x, p, 'k', linewidth=2, label=f'Fit results: mu = {mu:.2f},  sigma = {sigma:.2f}')

plt.title('Histogram of Birthday Paradox Simulations')
plt.xlabel('Probability of at least one shared birthday')
plt.ylabel('Density')
plt.legend()
plt.show()

# Print mean and standard deviation
print(f"Mean: {mu:.4f}")
print(f"Standard Deviation: {sigma:.4f}")
