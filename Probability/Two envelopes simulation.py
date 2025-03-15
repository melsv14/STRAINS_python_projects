import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Function to simulate the Two Envelopes Problem
def two_envelopes_simulation(switch=True):
    envelope_A = np.random.randint(1, 1000)
    envelope_B = 2 * envelope_A if np.random.rand() > 0.5 else envelope_A // 2
    chosen_envelope = envelope_A if np.random.rand() > 0.5 else envelope_B
    if switch:
        other_envelope = envelope_B if chosen_envelope == envelope_A else envelope_A
        return other_envelope
    else:
        return chosen_envelope

# Number of simulations
num_simulations = 1000

# Run simulations
results_no_switch = [two_envelopes_simulation(switch=False) for _ in range(num_simulations)]
results_switch = [two_envelopes_simulation(switch=True) for _ in range(num_simulations)]

# Calculate mean and standard deviation
mean_no_switch = np.mean(results_no_switch)
std_no_switch = np.std(results_no_switch)
mean_switch = np.mean(results_switch)
std_switch = np.std(results_switch)

# Print mean and standard deviation
print(f"No Switching - Mean: {mean_no_switch}, Standard Deviation: {std_no_switch}")
print(f"Switching - Mean: {mean_switch}, Standard Deviation: {std_switch}")

# Fit normal distributions to the data
mu_no_switch, std_no_switch_fit = norm.fit(results_no_switch)
mu_switch, std_switch_fit = norm.fit(results_switch)

# Plot histograms and fitted distributions
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.hist(results_no_switch, bins=30, color='blue', edgecolor='black', alpha=0.7, density=True)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p_no_switch = norm.pdf(x, mu_no_switch, std_no_switch_fit)
plt.plot(x, p_no_switch, 'k', linewidth=2)
plt.title('Distribution of Gains (No Switching)')
plt.xlabel('Amount in Chosen Envelope')
plt.ylabel('Density')

plt.subplot(1, 2, 2)
plt.hist(results_switch, bins=30, color='green', edgecolor='black', alpha=0.7, density=True)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p_switch = norm.pdf(x, mu_switch, std_switch_fit)
plt.plot(x, p_switch, 'k', linewidth=2)
plt.title('Distribution of Gains (Switching)')
plt.xlabel('Amount in Chosen Envelope')
plt.ylabel('Density')

plt.tight_layout()
plt.show()
