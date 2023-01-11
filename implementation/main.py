from Simplex import *
from Problem_set import *

# Test
(LP_1,LP_2) = solve_LP(*dataset(9))
# LP_2.plot_cost_trace()
# LP_1.plot_cost_trace()


# Visualization
fig = plt.figure(figsize=(8,8))

cost_trace_LP1 = list()
for i in LP_1.solution_trace:
    cost_trace_LP1.append(LP_1.c @ i)

cost_trace_LP2 = list()
for i in LP_2.solution_trace:
    cost_trace_LP2.append(LP_2.c @ i)

ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)


ax1.plot(cost_trace_LP1)
ax1.set_title("Phase1 - cost")

ax2.plot(cost_trace_LP2)
ax2.set_title("Phase2 - cost")

plt.show()

