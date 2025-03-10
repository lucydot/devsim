# CHANGES

## Introduction

Please see the release notes in doc/devsim.pdf or at https://devsim.net for more detailed information about changes.

## Version 2.0.0

### Versioned MKL DLL in release build

The Intel Math Kernel Library now uses versioned library names.  Binary releases are now updated against the latest versioned dll names from MKL available in the Anaconda Python distribution.

### Fixed issue in ramp function.

The ``rampbias`` function in the ``devsim.python_packages.ramp`` module has been fixed to properly reduce the bias when there is a convergence failure.

### Transient Simulation

Fixed bug with ``transient_tr`` (trapezoidal) time integration method where the wrong sign was used to integrate previous time steps.

Fixed bug in the charge error calculation, which calculates the simulation result with that a forward difference projection.

Added ``testing/transient_rc.py`` test which compares simulation with analytic result for RC circuit.

Added ``set_initial_condition`` command to provide initial transient conditions based on current solution.

### Create interface from node pairs

Added ``create_interface_from_nodes`` to make it possible to add interface from non-coincident pairs of nodes.

### Solver

#### Convergence Tests

The ``maximum_error`` and ``maximum_divergence`` options where added to the ``solve`` command.  If the absolute error of any iteration goes above ``maximum_error``, the simulation stops with a convergence failure.  The ``maximum_divergence`` is the maximum number of iterations that the simulator error may increase before stopping.

#### Verbosity

During the ``solve``, circuit node and circuit solution information is no longer printed to the screen for the default verbosity level.  In addition, the number of equations per device and region is no longer displayed at the start of the first iteration.

#### SuperLU

The code now supports newer versions of ``SuperLU``.  The release version is still using SuperLU 4.3 for the iterative solution method, and the Intel MKL Pardiso for the direct solve method.

#### Simulation Matrix

The ``get_matrix_and_rhs`` command was not properly accepting the ``format`` parameter, and was always returning the same type.

### Build Scripts

The build scripts have been updated on all platforms to be less dependent on specific Python 3 versions.

An updated fedora build script has been added.  It uses the system installed ``SuperLU`` as the direct solver.

### Documentation Files

Some out of date files (e.g. RELEASE, INSTALL, . . .) have been removed.  The [README.md](README.md) has been updated and the [INSTALL.md](INSTALL.md) have been updated.

### Command Options

The ``variable_name`` option is no longer recognized for the ``devsim.contact_equation`` and ``devsim.interface_equation`` as it was not being used.

## Version 1.6.0

### Array Type Input and Output

In most circumstances, the software now returns numerical data using the Python ``array`` class.  This is more efficient than using standard lists, as it encapsulates a contiguous block of memory.  More information about this class can be found at [https://docs.python.org/3/library/array.html](https://docs.python.org/3/library/array.html).  The representation can be easily converted to lists and ``numpy`` arrays for efficient manipulation.

When accepting user input involving lists of homogenous data, such as ``set_node_values`` the user may enter data using either a list, string of bytes, or the ``array`` class.  It may also be used to input ``numpy`` arrays or any other class with a ``tobytes`` method.

### Get Matrix and RHS for External Use

The ``get_matrix_and_rhs`` command has been added to assemble the static and dynamic matrices, as well as their right hand sides, based on the current state of the device being simulated.  The ``format`` option is used to specify the sparse matrix format, which may be either in the compressed column or compressed row formats, ``csc`` or ``csr``.

### Maximum Divergence Count

If the Newton iteration errors keep increasing for 20 iterations in a row, then the simulator stops.  This limit was previously 5.

### Mesh Visualization Element Orientation

Elements written to the ``tecplot`` format in 2d and 3d have node orderings compatible with the element connectivity in visualization formats.  Specifying the ``reorder=True`` option in ``get_element_node_list`` will result in node ordering compatible with meshing and visualization software.

## Version 1.5.1

### Math Functions

The following inverse functions and their derivatives are now available in the model interpreter.
- ``erf_inv`` Inverse Error Function
- ``erfc_inv`` Inverse Complimentary Error Function
- ``derf_invdx`` Derivative of Inverse Error Function
- ``derfc_invdx`` Derivative of Complimentary Inverse Error Function

The Gauss-Fermi Integral, using Paasch's equations are now implemented.
- ``gfi`` Gauss-Fermi Integral
- ``dgfidx`` Derivative of Gauss-Fermi Integral
- ``igfi`` Inverse Gauss-Fermi Integral
- ``digfidx`` Derivative of Inverse Gauss-Fermi Integral

Each of these functions take two arguments, ``zeta`` and ``s``.  The derivatives with respect to the first argument are provided.  Please see ``testing/GaussFermi.py`` for an example.

In extended precision mode, the following functions are now evaluated with full extended precision.
- ``Fermi``
- ``dFermidx``
- ``InvFermi``
- ``dInvFermidx``

The following double precision tests:

- ``testing/Fermi1.py`` Fermi Integral Test
- ``testing/GaussFermi.py`` Gauss Fermi Integral Test

Have extended precision variants:

- ``testing/Fermi1_float128.py``
- ``testing/GaussFermi_float128.py``

### Installation Script

A new installation script is in the base directory of the package.
It provides instructions of completing the installation to the ``python`` environment without having to set the ``PYTHONPATH`` environment variable.
It notifies the user of missing components to finish the installation within an ``Anaconda`` or ``Miniconda`` environment.


To use the script, use the following command inside of the ``devsim`` directory.

```
    python install.py
```

The install script will write a file named ``lib/setup.py``, which can be used to complete the installation using ``pip``.  The script provides instructions for the installation and deinstallation of ``devsim``.

```
    INFO: Writing setup.py
    INFO:
    INFO: Please type the following command to install devsim:
    INFO: pip install -e lib
    INFO:
    INFO: To remove the file, type:
    INFO: pip uninstall devsim
```

## Version 1.5.0

The ``custom_equation`` command has been modified to require a third return value.  This boolean value denotes whether the matrix entries should be row permutated or not.  For the bulk equations this value should be ``True``.  For interface and contact boundary conditions, this value should be ``False``.

It is now possible to replace an existing ``custom_equation``.

The file ``examples/diode/diode_1d_custom.py`` demonstrates custom matrix assembly and can be directly compared to ``examples/diode/diode_1d.py``.

The ``EdgeNodeVolume`` model is now available for the volume contained by an edge.

The ``contact_equation`` command now accepts 3 additional arguments.

- ``edge_volume_model``
- ``volume_node0_model``
- ``volume_node1_model``

These options provide the ability to do volume integration on contact nodes.

The ``equation`` command has replaced the ``volume_model`` option with:

- ``volume_node0_model``
- ``volume_node1_model``

so that nodal quantities can be more localized.

More details are in the manual.

## Version 1.4.14
### Platforms

Windows 32 bit is no longer supported.  Binary releases of the ``Visual Studio 2019`` ``MSYS2/Mingw-w64`` 64-bit builds are still available online.

On Linux, the releases are now on Centos 7, as Centos 6 has reached its end of life on November 30, 2020.

### C++ Standard

The C++ standard has been raised to C++17.

## Version 1.4.13

The node indexes with the maximum error for each equation will be printed when ``debug_level`` is ``verbose``.

```
devsim.set_parameter(name="debug_level", value="verbose")
```

These are printed as ``RelErrorNode`` and ``AbsErrorNode``:

```
    Region: "gate"	RelError: 5.21531e-14	AbsError: 4.91520e+04
      Equation: "ElectronContinuityEquation"	RelError: 4.91520e-16	AbsError: 4.91520e+04
	RelErrorNode: 129	AbsErrorNode: 129
```

This information is also returned when using the ``info=True`` option on the ``solve`` command for each equation on each region of a device.

If the ``info`` flag is set to ``True`` on the ``solve`` command, the iteration information will be returned, and an exception for convergence will no longer be thrown.  It is the responsibility of the caller to test the result of the ``solve`` command to see if the simulation converged.  Other types of exceptions, such as floating point errors, will still result in a Python exception that needs to be caught.


## Version 1.4.12

Element assembly for calculation of current and charges from the device into the circuit equation are fixed.  These tests are added:

- ``testing/cap_2d_edge.py``
- ``testing/cap_2d_element.py``
- ``testing/cap_3d_edge.py``
- ``testing/cap_3d_element.py``

The ``edge`` variant is using standard edge based assembly, and the ``element`` variant is using element-based assembly.

## Version 1.4.11

The ``element_pair_from_edge_model`` is available to calculate element edge components averaged onto each node of the element edge.  This makes it possible to create an edge weighting scheme different from those used in ``element_from_edge_model``.

Fixed issue where command option names where not always shown in the documentation.

The platform specific notes now clarify that any version of Python 3 (3.6 or higher) is supported.

- ``linux.txt``
- ``windows.txt``
- ``macos.txt``

## Version 1.4.10

Fixed crash when evaluating element edge model in 3D.

Fixed potential error using ``delete_node_model`` and similar deletion commands.

## Version 1.4.9

Support for loading mesh files containing element edge data.

## Version 1.4.8

In transient mode, the convergence test was flawed so that the ``charge_error`` was the only convergence check required for convergence.  The software now ensures all convergence criteria are met.

## Version 1.4.7

### Models

In the simple physics models, the sign for time-derivative terms was wrong for the electron and hole continuity equations.  This affects small-signal and noise simulations.  The example at ``examples/diode/ssac_diode.py`` was updated to reflect the change.

### Platforms

Fix build script issue for macOS on Travis CI, updated the compiler to ``g++-9``.

Update Centos 6 build from ``devtoolset-6`` to ``devtoolset-8``.

## Version 1.4.6

### Version Information

Parameter ``info`` can be queried for getting version information.  The file ``testing/info.py`` contains an example.

```
  python info.py
  {'copyright': 'Copyright © 2009-2020 DEVSIM LLC', 'direct_solver': 'mkl_pardiso', 'extended_precision': True, 'license': 'Apache License, Version 2.0', 'version': '1.4.6', 'website': 'https://devsim.org'}
```

### Extended Precision

The example ``examples/diode/gmsh_diode3d_float128.py`` provides an example where extended precision is enabled.

### Python Formatting

The Python scripts in the ``examples`` and ``testing`` directories have been reformatted to be more consistent with language standards.

### Platforms

Microsoft Windows 10 is supported and is now compiled using Microsoft Visual Studio 2019.

Microsoft Windows 7 is no longer supported, as Microsoft has dropped support as of January 14, 2020.

### External Meshing

Support for reading meshes from Genius Device Simulator has been completely removed from DEVSIM.


## Version 1.4.5

* Platform Support:
  * An MSYS2/Mingw-w64 build is available for 64-bit Windows.  This build, labeled ``devsim_msys_v1.4.5``, enables the use of the 128-bit floating point precision already available on the macOS and Linux platforms.

## Version 1.4.4

* Bug Fixes:
  * Intermittent crash on Windows 10 at the end of the program
* CHANGES.md containing version changes in markdown format.
* Internal changes:
  * Regression system script refactored to Python.
  * Refactor threading code using C++11 functions
  * Refactor timing functions for verbose mode using C++11 functions.
  * Refactor FPE detection code to C++11 standard.

