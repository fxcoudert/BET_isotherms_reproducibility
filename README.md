# Brunauer–Emmett–Teller (BET) fitting of isotherms

This repository contains the code used for [BET adsorption isotherm fitting](https://en.wikipedia.org/wiki/BET_theory) in [our group](https://www.coudert.name). It is part of the crowd-science work performed in the following paper: [“How Reproducible are Surface Areas Calculated from the BET Equation?”](https://doi.org/10.1002/adma.202201502), J. W. M. Osterrieth et al., _Adv. Mater._, **2022**, DOI: [10.1002/adma.202201502](https://doi.org/10.1002/adma.202201502)



## Description

The code requires Python ≥ 3.6 and scientific packages `numpy`, `scipy`, and `matplotlib`. The code is stored in a module named `BET.py` and for each isotherm a Jupyter notebook is available showing the parameters chosen and the fit obtained (from [`A.ipynb`](A.ipynb) to [`R.ipynb`](R.ipynb)).

The typical criteria (from Rouquerol et al., _Is the BET Equation Applicable to Microporous Adsorbents?_) for fitting are automatically checked, and the quality of the least-square linear fit (_R_<sup>2</sup> coefficient) is displayed. Both the BET function and the Rouquerol function are also plotted for visual confirmation of the fit.

![](example.png|width=500px)
