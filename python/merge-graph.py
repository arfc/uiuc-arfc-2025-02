import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib as mpl
mpl.rc_file("./matplotlib.rc")
cycle = mpl.rcParams["axes.prop_cycle"].by_key()["color"]
import networkx as nx

graph = nx.DiGraph()

C2 = ["C2_0"]
C1 = [f"C1_{i}" for i in range(4)]
C0 = [f"C0_{i}" for i in range(16)]
graph.add_nodes_from(C2 + C1 + C0)

for n in C1:
    graph.add_edge("C2_0", n)

# this is pretty messy, but idk how else to do this
for i, p in enumerate(C1):
    for j, c in enumerate(C0):
        if j % 4 == i and j%5 != 0:
            pass
        elif i < 2 and j/4 >= 3:
            pass
        elif i > 2 and j < 4:
            pass
        else:
            graph.add_edge(p, c)

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