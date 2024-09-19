r"""Dynamical Movement Primitive (DMP)
==================================

This module provides implementations of various DMP types. DMPs consist of
a goal-directed movement generated by the transformation system and a forcing
term that defines the shape of the trajectory. They are time-dependent and
usually converge to the goal after a constant execution time.

Every implementation is slightly different, but we use a similar notation for
all of them:

* :math:`y,\dot{y},\ddot{y}` - position, velocity, and acceleration; these
  might be translation components only, orientation, or both
* :math:`y_0` - start position
* :math:`g` - goal of the movement (attractor of the DMP)
* :math:`\tau` - execution time
* :math:`z` - phase variable, starts at 1 and converges to 0
* :math:`f(z)` - forcing term, learned component that defines the shape of the
  movement
* :math:`C_t` - coupling term that is added to the acceleration of the DMP
"""
from ._base import DMPBase, WeightParametersMixin
from ._dmp import DMP, dmp_transformation_system
from ._dmp_with_final_velocity import DMPWithFinalVelocity
from ._cartesian_dmp import CartesianDMP
from ._dual_cartesian_dmp import DualCartesianDMP
from ._coupling_terms import (
    CouplingTermObstacleAvoidance2D, CouplingTermObstacleAvoidance3D,
    CouplingTermPos1DToPos1D, CouplingTermPos3DToPos3D,
    CouplingTermDualCartesianPose, CouplingTermDualCartesianDistance,
    CouplingTermDualCartesianTrajectory, obstacle_avoidance_acceleration_2d,
    obstacle_avoidance_acceleration_3d)
from ._state_following_dmp import StateFollowingDMP
from ._canonical_system import canonical_system_alpha, phase


__all__ = [
    "DMPBase", "WeightParametersMixin",
    "DMP", "dmp_transformation_system", "DMPWithFinalVelocity", "CartesianDMP",
    "DualCartesianDMP", "CouplingTermPos1DToPos1D",
    "CouplingTermObstacleAvoidance2D", "CouplingTermObstacleAvoidance3D",
    "CouplingTermPos3DToPos3D", "CouplingTermDualCartesianPose",
    "CouplingTermDualCartesianDistance", "CouplingTermDualCartesianTrajectory",
    "canonical_system_alpha", "phase", "obstacle_avoidance_acceleration_2d",
    "obstacle_avoidance_acceleration_3d"]