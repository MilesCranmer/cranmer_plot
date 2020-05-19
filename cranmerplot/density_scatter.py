import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
plt.rc('font', family='serif')

def density_scatter(x, y, xlabel='', ylabel='', clabel='Sample Density', log=False,
    width_mult=1, bins=30, p_cut=0, update_rc=True, weights=None, cmap='viridis'):
    np = onp
    if update_rc:
        plt.rc('font', family='serif')

    fig, ax = plt.subplots(1, 1, figsize=(4*width_mult, 3))
    xy = np.array([x, y]).T
    px = xy[:, 0]
    py = xy[:, 1]
    p = p_cut
    range_x = [np.percentile(xy[:, 0], i) for i in [p, 100-p]]
    range_y = [np.percentile(xy[:, 1], i) for i in [p, 100-p]]
    mask = (xy[:, 0] > range_x[0]) & (xy[:, 0] < range_x[1]) & (xy[:, 1] > range_y[0]) & (xy[:, 1] < range_y[1])

    pxy = xy[mask]
    if weights is not None:
        weights = np.array(weights)
        weights = weights[mask]
    px = pxy[:, 0]
    py = pxy[:, 1]
    norm = None
    if log:
        norm = LogNorm()
    if not isinstance(bins, list):
        bins = [int(width_mult*bins), bins]

    h, xedge, yedge, im = ax.hist2d(
        px, py, density=True,
        norm=norm, bins=bins,
        weights=weights, cmap=cmap
        )
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    fig.colorbar(im).set_label(clabel)
    fig.tight_layout()

    return fig, ax
