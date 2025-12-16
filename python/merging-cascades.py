import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
mpl.rc_file("./matplotlib.rc")

def merge_plot(theta, num_rays, r, bilinear_fix, fname):

    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    
    # c0 probe
    color = ax._get_lines.get_next_color()
    end_pt = partial_colorize_interp(ax, ro=r, num_rays=num_rays, theta=theta,
                                     color=color, exact_ray=True, x0=3, y0=5,
                                     bilinear_fix=bilinear_fix)

    # c1 probes
    x, y = np.meshgrid([2, 6], [2, 6])
    for xi, yi in zip(x.ravel(), y.ravel()):
        color = ax._get_lines.get_next_color()
        partial_colorize_interp(ax, ro=3*r, num_rays=2*num_rays, theta=theta,
                                color=color, x0=xi, y0=yi, ri=r,
                                interp_end=end_pt, bilinear_fix=bilinear_fix)

    ax.set_axis_off() 
    fig.savefig(f"../figs/{fname}")
    plt.close(fig)

def partial_colorize_interp(ax, ro, num_rays, theta, color,
                            exact_ray=False, x0=0.0, y0=0.0,
                            ri=0.0, interp_end=(0.0,0.0),
                            bilinear_fix=False):

    # slight ang offset so lines dont perfectly extend
    thetas = (np.pi + 2*np.pi*np.arange(num_rays)) / num_rays
    # coloring specific rays
    no_color = mpl.rcParams["axes.prop_cycle"].by_key()["color"][-1]
    if exact_ray:
        idx = np.flatnonzero(np.isclose(thetas, theta, atol=1e-12))[0]
        colors = np.where(np.arange(len(thetas)) == idx, color, no_color)
    else:
        color_idx = np.searchsorted(thetas, theta)
        colors = [no_color] * len(thetas)
        colors[color_idx-1:color_idx+1] = [color, color]
    #emphasize colored lines
    widths = np.asarray(colors, dtype=object) != no_color
    widths = widths * 0.6 + 0.8

    # add probe to drawing
    add_probe(ax, x0, y0, ri, ro, thetas, colors, widths)

    if bilinear_fix:
        radius = ri
    elif exact_ray:
        radius = ro
    else:
        radius = ri

    if exact_ray:
        # return end point we want to draw interpolation onto
        x, y = radius * np.cos(theta), radius * np.sin(theta)
        return x+x0, y+y0
    else:
        # draw interpolation
        theta =  (thetas[color_idx] + thetas[color_idx - 1]) / 2
        x, y = radius * np.cos(theta), radius * np.sin(theta)
        ax.plot(x+x0, y+y0, color=color, marker='o', ms=3.0, ls="None")
        interp = [x+x0, interp_end[0]],[y+y0, interp_end[1]]
        ax.plot(*interp, color=color, ls=":")


def add_probe(ax, x0, y0, ri, ro, thetas, colors, widths):

    # need to add the shell so there we can clip the rays to it
    probe = ptc.Wedge((x0, y0), ro, 0, 360,
                      width=ro - ri, alpha=0.0)
    ax.add_patch(probe)

    # add rays
    r = np.array([ri, ro])
    for theta, color, width in zip(thetas, colors, widths):
        x = r*np.cos(theta) + x0
        y = r*np.sin(theta) + y0
        (line,) = ax.plot(x, y, color=color, linewidth=width)
        line.set_clip_path(probe) # dont bleed into adjacnt intervals


if __name__=='__main__':

    merge_plot(np.pi/4, 4, 1/3, False, 'vanilla-merge')
    
    merge_plot(np.pi/4, 4, 1/3, True, 'bilinear-fix-merge')