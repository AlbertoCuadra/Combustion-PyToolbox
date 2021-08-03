import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import (PchipInterpolator as pchip)
from palettable.colorbrewer.qualitative import Set3_12
from Solver.Functions.struct2vector import struct2vector

def plotMoles(self, x_vec, display_species, mintol, xlabel, ax=None, plt_args=[], plt_kwargs={}, **kwargs):
    plt.ion()
    if not ax:
        ax = plt.subplot()
    # Data
    struct = self.PS.strP
    Nx = len(x_vec)
    NS = len(struct[0].Xi)
    y_matrix = np.zeros((NS, Nx))
    Ndisplay = set()
    # Display tolerance requirements
    for i in range(Nx):
        y_matrix[:, i] = struct[i].Xi
        for species in display_species:
            ind = self.S.LS.index(species)
            if struct[i].Xi[ind] > mintol:
                Ndisplay.add(ind)
    # Plot configuration
    cmap = matplotlib.colors.ListedColormap(Set3_12.mpl_colors)
    plt.set_cmap(cmap)
    ax.set_xlim(x_vec.min(), x_vec.max())
    ax.set_ylim(mintol, 1.0)
    ax.set_yscale('log')
    labels = np.array(display_species)
    labels = [labels[ndisplay] for ndisplay in Ndisplay]
    # Plot
    for j in Ndisplay:
        ax.plot(x_vec, y_matrix[j, :], *plt_args, **plt_kwargs, **kwargs)
    # Legend    
    ax.legend(labels=labels, loc='upper left', bbox_to_anchor=(1.05, 1))
    plt.subplots_adjust(right=0.8)
    plt.show()
    return self

def plotFigure(self, x_vec, y_vec, ax=None, plt_args=[], plt_kwargs={}, **kwargs):
    plt.ion()
    if not ax:
        ax = plt.subplot()
    # Plot configuration
    ax.set_xlim(x_vec.min(), x_vec.max())
    ax.set_ylim(y_vec.min(), 1.05*y_vec.max())
    # Plot
    ax.plot(x_vec, y_vec, *plt_args, **plt_kwargs, **kwargs)
    plt.subplots_adjust(right=0.8)
    plt.show()
    return self

def plotResults(self, display_species=None, mintol=1e-16):
    phi = self.PD.phi.Value
    ProblemType = self.PD.ProblemType
    # Figure configuration
    plot_params = {'linewidth': 2}
    plot_args = ['-']
    if len(phi) > 1 and all(phi[1::] != phi[0]) and ProblemType != 'DET_OVERDRIVEN':
        plotMoles(self, phi, display_species, mintol, xlabel='Equivalence ratio', plt_args = plot_args, plt_kwargs = plot_params)
        if self.PD.ProblemType.upper() != ('TP' or 'TV'):
            plotFigure(self, phi, struct2vector(self.PS.strP, 'T'), plt_args = plot_args, plt_kwargs = plot_params)
    
