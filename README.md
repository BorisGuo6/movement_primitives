# Movement Primitives

[API Documentation (only reachable within network of DFKI RIC)](http://bob.dfki.uni-bremen.de/apis/dfki-learning/movement_primitives/movement_primitives/)

## Features

* Dynamical Movement Primitives (DMPs) for
    * positions (with fast Runge-Kutta integration)
    * Cartesian position and orientation (with fast Cython implementation)
    * Dual Cartesian position and orientation (with fast Cython implementation)
* Coupling terms for synchronization of position and/or orientation of dual Cartesian DMPs
* Propagation of DMP weight distribution to state space distribution
* Probabilistic Movement Primitives (ProMPs)

## Install Library

This library requires Python 3.6 or later and pip is recommended for the
installation. In the following instructions, we assume that the command
`python` refers to Python 3. If you use the system's Python version, you
might have to add the flag `--user` to any installation command.

I recommend to install the library via pip in editable mode:

```bash
python -m pip install -e .[all]
```

If you don't want to have all dependencies installed, just omit `[all]`.

Alternatively, you can build the Cython extension with

```bash
python setup.py build_ext --inplace
```

or install the library with

```bash
python setup.py install
```

## Non-public Extensions

Note that scripts from the subfolder `scripts/` require access to git
repositories (URDF files or optional dependencies) that are not publicly
available.

### MoCap Library

```bash
# untested: pip install git+https://git.hb.dfki.de/dfki-interaction/mocap.git
git clone git@git.hb.dfki.de:dfki-interaction/mocap.git
cd mocap
python -m pip install -e .
cd ..
```

### Get URDFs

```bash
# UR5
git clone git@git.hb.dfki.de:models-robots/ur5_fts300_2f-140.git
# RH5
git clone git@git.hb.dfki.de:models-robots/rh5_models/pybullet-only-arms-urdf.git --recursive
# RH5v2
git clone git@git.hb.dfki.de:models-robots/rh5v2_models/pybullet-urdf.git --recursive
# Kuka
git clone git@git.hb.dfki.de:models-robots/kuka_lbr.git
# Solar panel
git clone git@git.hb.dfki.de:models-objects/solar_panels.git
# RH5 Gripper
git clone git@git.hb.dfki.de:motto/abstract-urdf-gripper.git --recursive
```

### Data

I assume that your data is located in the folder `data/` in most scripts.
You should put a symlink there to point to your actual data folder.

## Build API Documentation

You can build an API documentation with [pdoc3](https://pdoc3.github.io/pdoc/).
You can install pdoc3 with

```bash
pip install pdoc3
```

... and build the documentation from the main folder with

```bash
pdoc movement_primitives --html
```

It will be located at `html/movement_primitives/index.html`.

## Test

To run the tests some python libraries are required:

```bash
python -m pip install -e .[test]
```

The tests are located in the folder `test/` and can be executed with:
`python -m nose test`

This command searches for all files with `test` and executes the functions with `test_*`.

## Contributing

To add new features, documentation, or fix bugs you can open a pull request.
Directly pushing to the master branch is not allowed.

## Examples

### Conditional ProMPs

<img src="doc/source/_static/conditional_promps.png" width="800px" />

Probabilistic Movement Primitives (ProMPs) define distributions over
trajectories that can be conditioned on viapoints. In this example, we
plot the resulting posterior distribution after conditioning on varying
start positions.

[Script](examples/plot_conditional_promp.py)

### Potential Field of 2D DMP

<img src="doc/source/_static/dmp_potential_field.png" width="800px" />

A Dynamical Movement Primitive defines a potential field that superimposes
several components: transformation system (goal-directed movement), forcing
term (learned shape), and coupling terms (e.g., obstacle avoidance).

[Script](examples/plot_dmp_potential_field.py)

### Contextual ProMPs

<img src="doc/source/_static/contextual_promps_kuka_panel_width_open3d.png" width="400px" />
<img src="doc/source/_static/contextual_promps_kuka_panel_width_open3d2.png" width="400px" />

We use a dataset of [Mronga and Kirchner (2021)](https://www.sciencedirect.com/science/article/abs/pii/S0921889021000646)
with 10 demonstrations per 3 different panel widths that were obtained through
kinesthetic teaching. The panel width is considered to be the context over
which we generalize with contextual ProMPs. Each color in the above
visualizations corresponds to a ProMP for a different context.

[Script](scripts/vis_contextual_promp_distribution.py)

**Dependencies that are not publicly available:**

* Dataset: panel rotation dataset of
  [Mronga and Kirchner (2021)](https://www.sciencedirect.com/science/article/abs/pii/S0921889021000646)
* MoCap library
* URDF of dual arm Kuka system from
  [DFKI RIC's MRK lab](https://robotik.dfki-bremen.de/en/research/research-facilities-labs/mrk-lab/):
  ```bash
  git clone git@git.hb.dfki.de:models-robots/kuka_lbr.git
  ```

### Dual Cartesian DMP

<img src="doc/source/_static/dual_cart_dmps_rh5_open3d.png" width="300px" />
<img src="doc/source/_static/dual_cart_dmps_rh5_pybullet.png" width="300px" />

We offer specific dual Cartesian DMPs to control dual-arm robotic systems like
humanoid robots.

Scripts: [Open3D](scripts/vis_solar_panel.py), [PyBullet](scripts/sim_solar_panel.py)

**Dependencies that are not publicly available:**

* MoCap library
* URDF of [DFKI RIC's RH5 robot](https://www.youtube.com/watch?v=jjGQNstmLvY):
  ```bash
  git clone git@git.hb.dfki.de:models-robots/rh5_models/pybullet-only-arms-urdf.git --recursive
  ```
* URDF of solar panel:
  ```bash
  git clone git@git.hb.dfki.de:models-objects/solar_panels.git
  ```

### Coupled Dual Cartesian DMP

<img src="doc/source/_static/coupled_dual_cart_dmps_gripper_open3d.png" width="450px" />
<img src="doc/source/_static/coupled_dual_cart_dmps_rh5_pybullet.png" width="250px" />

We can introduce a coupling term in a dual Cartesian DMP to constrain the
relative position, orientation, or pose of two end-effectors of a dual-arm
robot.

Scripts: [Open3D](scripts/vis_cartesian_dual_dmp.py), [PyBullet](scripts/sim_cartesian_dual_dmp.py)

**Dependencies that are not publicly available:**

* URDF of DFKI RIC's gripper:
  ```bash
  git clone git@git.hb.dfki.de:motto/abstract-urdf-gripper.git --recursive
  ```
* URDF of [DFKI RIC's RH5 robot](https://www.youtube.com/watch?v=jjGQNstmLvY):
  ```bash
  git clone git@git.hb.dfki.de:models-robots/rh5_models/pybullet-only-arms-urdf.git --recursive
  ```

### Propagation of DMP Distribution to State Space

<img src="doc/source/_static/dmp_state_space_distribution_kuka_peginhole_matplotlib.png" width="500px" />
<img src="doc/source/_static/dmp_state_space_distribution_kuka_peginhole_open3d.png" width="300px" />

If we have a distribution over DMP parameters, we can propagate them to state
space through an unscented transform.

[Script](scripts/vis_dmp_to_state_variance.py)

**Dependencies that are not publicly available:**

* Dataset: panel rotation dataset of
  [Mronga and Kirchner (2021)](https://www.sciencedirect.com/science/article/abs/pii/S0921889021000646)
* MoCap library
* URDF of dual arm Kuka system from
  [DFKI RIC's MRK lab](https://robotik.dfki-bremen.de/en/research/research-facilities-labs/mrk-lab/):
  ```bash
  git clone git@git.hb.dfki.de:models-robots/kuka_lbr.git
  ```
