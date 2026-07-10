# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Scipp contributors (https://github.com/scipp)
"""Normalization routines for ScippNeutron."""

import scipp as sc
import scipp.constants

from . import _scippneutron_algorithms_lib as lib


def compute_single_crystal_norm(
    *,
    trajectory_start: sc.Variable,  # shape: [*other, pixel, q-e]
    trajectory_stop: sc.Variable,
    solid_angle: sc.Variable,
    grid: tuple[sc.Variable, sc.Variable, sc.Variable, sc.Variable],
    incident_energy: sc.Variable,
    n_threads: int | None = None,
    block_size: int | None = None,
) -> sc.DataArray:
    """Compute a normalization factor for single crystal data.

    The grid is specified in (h, k, l, dE),
    gets converted to (h, k, l, kf)
    The trajectory is specified in (h, k, l, kf)
    """
    orig_grid = tuple(grid)
    grid = (
        *grid[:3],
        _energy_to_final_momentum(
            energy_transfer=grid[3], incident_energy=incident_energy
        ),
    )
    # dE -> kf reverses order, if inputs are ordered, then just flip the array
    grid = (*(x.values for x in grid[:3]), grid[3].values[::-1])

    norm_values = lib.compute_single_crystal_norm(
        start=_reshape_trajectory_point(trajectory_start).values,
        stop=_reshape_trajectory_point(trajectory_stop).values,
        solid_angle=solid_angle.values,
        grid=grid,
        n_threads=n_threads,
        block_size=block_size,
    )[:, :, :, ::-1]  # TODO do this in rust
    return sc.DataArray(
        sc.array(
            dims=["h", "k", "l", "energy_transfer"],
            values=norm_values,
            unit=sc.Unit("1/meV") / solid_angle.unit,
        ),
        coords=dict(zip(("h", "k", "l", "energy_transfer"), orig_grid, strict=True)),
    )


def _reshape_trajectory_point(point: sc.Variable) -> sc.Variable:
    other_dims = tuple(dim for dim in point.dims if dim != "q-e")
    return point.transpose((*other_dims, "q-e")).flatten(dims=other_dims, to="other")


# TODO move to coord transforms (and use in essspectroscopy)
def _energy_to_final_momentum(
    *, incident_energy: sc.Variable, energy_transfer: sc.Variable
) -> sc.Variable:
    final_energy = incident_energy - energy_transfer
    return sc.to_unit(
        sc.sqrt(2 * sc.constants.m_n / sc.constants.hbar**2 * final_energy),
        "1/Å",
        copy=False,
    )
