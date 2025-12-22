import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Circle
from matplotlib.lines import Line2D
import matplotlib as mpl
mpl.rc_file("./matplotlib.rc")
cycle = mpl.rcParams["axes.prop_cycle"].by_key()["color"]
import networkx as nx
import numpy as np

graph = nx.DiGraph()

C2 = ["C2_0"]
C1 = [f"C1_{i}" for i in range(4)]
C0 = [f"C0_{i}" for i in range(16)]
graph.add_nodes_from(C2 + C1 + C0)

for n in C1:
    graph.add_edge("C2_0", n)

for i in [1, 2, 3, #4
          5, 6, 7, #8
          9, 10, 11, #12
          #13, #14, #15, #16
          ]:
    graph.add_edge("C1_0", f"C0_{i-1}")

for i in [2, 3, 4,
          6, 7, 8,
          10, 11, 12]:
    graph.add_edge("C1_1", f"C0_{i-1}")

for i in [# 1, 2, 3, 4,
          5, 6, 7, #8
          9, 10, 11, #12
          13, 14, 15, #16
          ]:
    graph.add_edge("C1_2", f"C0_{i-1}")

for i in [6, 7, 8,
          10, 11, 12,
          14, 15, 16]:
    graph.add_edge("C1_3", f"C0_{i-1}")

# setting the xy locs of eah probe 
pos = {}
pos["C2_0"] = (1.0, 2.0)
for i, n in enumerate(C1):
    pos[n] = (i/2 + 0.25, 1.5)
for i, n in enumerate(C0):
    pos[n] = (0.5 * (i / 4 ) + 0.125/2, 1)

# pretty colors and labels
node_colors = []
labels = {}
for node in graph.nodes:
    c = int(node[1])
    node_colors.append(cycle[c])
    c, j = node[1], int(node[3:])+1
    labels[node] = rf"$P^{c}_{{{j}}}$"
    
plt.figure(figsize=(10, 6))
nx.draw(graph, pos, with_labels=True, labels=labels,
        node_size=700, font_size=8,
        arrowsize=12, node_color=node_colors)
# legend!
legend_handles = [Patch(facecolor=cycle[c], edgecolor="None",
                        label=rf"Cascade $C_{c}$") for c in [2, 1, 0]]
legend_handles += [Line2D([0], [0], color="black", marker=">",
                          markersize=10, label="Communication")]
plt.legend(handles=legend_handles, handlelength=4, frameon=False)

plt.axis("off")
plt.savefig("../figs/rc-merge-graph")
plt.close()

fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.set_axis_off()
ax.set_prop_cycle(None)
c0 = np.meshgrid([1, 3, 5, 7], [7, 5, 3, 1])
c1 = np.meshgrid([2, 6], [6, 2]) 
c2 = np.meshgrid([4], [4])
c_xy = [c0, c1, c2]
for j, c in enumerate(c_xy):
    for i, (x, y) in enumerate(zip(c[0].ravel(), c[1].ravel())):
        x /= 8
        y /= 8
        circ = Circle((x, y), 0.05, facecolor=cycle[j],
                    edgecolor="white")
        ax.add_patch(circ)
        ax.text(x, y, rf"$P_{{{i}}}^{{{j}}}$", ha="center",
                va="center", transform=plt.gca().transAxes)
legend_handles = [Patch(facecolor=cycle[c], edgecolor="None",
                        label=rf"Cascade $C_{c}$") for c in [2, 1, 0]]
plt.legend(loc=(1,0.8), handles=legend_handles, handlelength=4, frameon=False)
fig.savefig("../figs/rc-merge-graph-problem")
