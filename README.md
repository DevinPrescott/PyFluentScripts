# PyFluentScripts

Eventually this will be a repository of PyFluent scripts. Currently the only script included is the Coefficient of Variation script.

## COV.PY

#### Description:

The [Coefficient of Variation](https://en.wikipedia.org/wiki/Coefficient_of_variation) is a statistical metric used in many fields of mathematics, science, and engineering which gives a mean normalized view of the standard deviation. In 2022, Katya Menter, Andreas Gantner, and Wolfgang Bauer presented this as a convergence metric for CFD simulations, using the rolling mean of monitored variables with a window of 50 samples wide. The rolling mean window of 50 tends to be a good balance between stability and minimum needed samples (less run time). They suggest a value of 1e-5 as an accepted limit for assessing convergence of a simulation.

#### Dependencies: 

None required, matplotlib for plot generation

#### Usage: 

Running `python cov.py` from a folder with report output (*.out*) files will create a plot of COV_50 and the unit normalized raw variable data as a png image for each output file. Optionally you may add filenames to output files, and the same will be generated. The script also reports the value of COV_50 for the last iteration.

#### A note on this implementation:

This implementation in python has no dependencies and runs approximately and order of magnitude faster than the proposed numpy-looping method in the 2022 presentation. A pandas implementation may be tempting, but it should be noted that the pandas `rolling().std()` method uses Welford's method with Kahan summation [aggregations.pyx](https://github.com/pandas-dev/pandas/blob/main/pandas/_libs/window/aggregations.pyx) which produces unreliable (potentially negative) results for variance at relatively small numbers (1e-4 to 1e-5) and cannot be used here. It's tempting to use the numpy std implemention on a pandas rolling window, `rolling().apply(np.std)` though this is orders of magnitude slower. It is always surprising to this author when native python libraries can outperform the likes of numpy / pandas for speed for numerical operations.