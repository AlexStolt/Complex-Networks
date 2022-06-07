from cProfile import label
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import numpy as np

# Coefficients
b = 3.6
m = 0.000385
r = 0.5
s = 0.5
k = 1.3
a = 0.065
g = 1.4

# Initial Values
NB = 0
initial_values = {
  'susceptible': 1000,
  'recovered': 0,
  'exposed': 0,
  'infected': 0,
}




def seir(t, y):
  S = y[0]  # Susceptible
  R = y[1]  # Recovered
  E = y[2]  # Exposed
  I = y[3]  # Infected
  

  # Original Differential Equations that produce invalid results 
  # ds_dt   = r * NB - b * S * I - m * S
  # de_dt   = b * S * I - (m + s + k) * E
  # di_dt   = s * E - (a + g + m) * I
  # dr_dt   = g * I + k * E - m * R

  # Modified Differential Equations that produce invalid results 
  ds_dt   = r * NB - b * S - m * S
  de_dt   = b * S - (m + s + k) * E
  di_dt   = s * E - (a + g + m) * I
  dr_dt   = g * I + k * E - m * R

  return np.array([ds_dt, dr_dt, de_dt, di_dt])



t_span = np.array([1, 20])
t_eval = np.linspace(1, 20, 1000)
y0 = np.array(list(initial_values.values()))

# Solve the system of differential equations
solution = solve_ivp(seir, t_span=t_span, y0=y0, t_eval=t_eval)

plt.plot(solution.t, solution.y[0], label="ds/dt")
plt.plot(solution.t, solution.y[1], label="dr/dt")
plt.plot(solution.t, solution.y[2], label="de/dt")
plt.plot(solution.t, solution.y[3], label="di/dt")
plt.plot([], [], ' ', label=f"S(0): {initial_values['susceptible']}")
plt.plot([], [], ' ', label=f"E(0): {initial_values['exposed']}")
plt.plot([], [], ' ', label=f"I(0): {initial_values['infected']}")
plt.plot([], [], ' ', label=f"R(0): {initial_values['recovered']}")
plt.plot([], [], ' ', label=f"Births: {NB}")
plt.legend(loc="lower right")
plt.show()
