import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
mpl.rc_file("./matplotlib.rc")

def add_probe(ax, ro, num_rays, color, x0=0.0, y0=0.0, ri=0.0, shade=True):
    if isinstance(color, int):
        # color is an index, gotta grab from the cycler
        color = mpl.rcParams["axes.prop_cycle"].by_key()["color"][color]
    alpha = 0.15 if shade else 0.0
    # wedge for circular shells, if ri=0 it deals with it fine
    probe = ptc.Wedge((x0, y0), ro, 0, 360, facecolor=color,
                          width=ro - ri, alpha=alpha)
    ax.add_patch(probe)

    # slight ang offset so lines dont perfectly extend
    thetas = (np.pi + 2*np.pi*np.arange(num_rays)) / num_rays
    r = np.array([ri, ro])
    for theta in thetas:
        x = r*np.cos(theta) + x0
        y = r*np.sin(theta) + y0
        (line,) = ax.plot(x, y, color=color)
        line.set_clip_path(probe) # dont bleed into adjacnt intervals

def plot_joint_probes(ax, num_intervals, init_radius, x0=0.0, y0=0.0, init_rays=4):
    ax.set_prop_cycle(None) # reset cycler sampling
    radii = np.r_[0.0, init_radius * 3**np.arange(num_intervals)]
    rays = init_rays * 2**np.arange(num_intervals)
    for ri, ro, nr in zip(radii[:-1], radii[1:], rays):
        color = ax._get_lines.get_next_color() # iterate cycler outside of probe
        add_probe(ax, ro, int(nr), color, ri=ri, x0=x0, y0=y0)


if __name__ == "__main__":
    ###
    # Radiation field -> radiance interval plot
    ###
    fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, sharey=True,
                                   subplot_kw=dict(aspect="equal"))

    num_intervals=4
    # left probe of 'full' radiation field
    add_probe(ax1, 1.5*3**(num_intervals-1), 4*2**(num_intervals-1), -1)

    # discretized into radiance intervals
    plot_joint_probes(ax2, num_intervals, 1.5)
    
    for ax in (ax1, ax2):
        ax.set_axis_off()
    fig.savefig("../figs/rad-field-2-ri")
    plt.close(fig)
    
    ###
    # Radiance interval compression plot
    ###
    fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, sharey=True,
                                   subplot_kw=dict(aspect="equal"))

    # plot the fine probe points
    x, y = np.meshgrid([1, 3, 5, 7], [1, 3, 5, 7])
    for xi, yi in zip(x.ravel(), y.ravel()):
        plot_joint_probes(ax1, 2, 1/3, x0=xi, y0=yi)
        plot_joint_probes(ax2, 1, 1/3, x0=xi, y0=yi)

    # plot the coarse probe points (C1 in right plot)
    x, y = np.meshgrid([2, 6], [2, 6])
    for xi, yi in zip(x.ravel(), y.ravel()):
        add_probe(ax2, ro=1.0, ri=1/3, num_rays=8, color=1, x0=xi, y0=yi)

    for ax in (ax1, ax2):
        ax.set_axis_off()
    fig.savefig("../figs/interval-compression")
    plt.close(fig)