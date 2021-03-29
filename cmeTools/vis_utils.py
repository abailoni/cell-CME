import matplotlib
matplotlib.use('Agg')
import os
from matplotlib import pyplot as plt
import numpy as np



# Build random color map:
__MAX_LABEL__ = 100000000
rand_cm = matplotlib.colors.ListedColormap(np.random.rand(__MAX_LABEL__, 3))


matplotlib.rcParams.update({'font.size': 5})
# DEF_INTERP = 'none'
DEF_INTERP = 'nearest'
segm_plot_kwargs = {'vmax': __MAX_LABEL__, 'vmin':0}


def mask_the_mask(mask, value_to_mask=0., interval=None):
    if interval is not None:
        return np.ma.masked_where(np.logical_and(mask < interval[1], mask > interval[0]), mask)
    else:
        return np.ma.masked_where(np.logical_and(mask < value_to_mask+1e-3, mask > value_to_mask-1e-3), mask)

def mask_array(array_to_mask, mask):
    return np.ma.masked_where(mask, array_to_mask)


def plot_segm(target, segm, background=None, mask_value=None, plot_label_colors=True,
              alpha_labels=0.4, cmap=None, alpha_background=1.0):
    if background is not None:
        target.imshow(background, interpolation=DEF_INTERP, alpha=alpha_background)

    if mask_value is not None:
        segm = mask_the_mask(segm, value_to_mask=mask_value)
    if plot_label_colors:
        cmap = rand_cm if cmap is None else cmap
        target.matshow(segm, cmap=cmap, alpha=alpha_labels, interpolation=DEF_INTERP, **segm_plot_kwargs)
