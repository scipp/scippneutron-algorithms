// SPDX-License-Identifier: BSD-3-Clause
// Copyright (c) 2026 Scipp contributors (https://github.com/scipp)

use pyo3::prelude::*;

#[pymodule]
mod _scippneutron_algorithms_lib {
    use numpy::{IntoPyArray, PyArray4, PyReadonlyArray1, PyReadonlyArray2};
    use pyo3::prelude::*;

    #[pyfunction]
    #[pyo3(signature = (*, start, stop, solid_angle, grid, n_threads=None, block_size=None))]
    fn compute_single_crystal_norm<'py>(
        py: Python<'py>,
        start: PyReadonlyArray2<'py, f64>,
        stop: PyReadonlyArray2<'py, f64>,
        solid_angle: PyReadonlyArray1<'py, f64>,
        grid: (
            PyReadonlyArray1<'py, f64>,
            PyReadonlyArray1<'py, f64>,
            PyReadonlyArray1<'py, f64>,
            PyReadonlyArray1<'py, f64>,
        ),
        n_threads: Option<usize>,
        block_size: Option<usize>,
    ) -> Bound<'py, PyArray4<f64>> {
        use algo_impl::normalization::single_crystal_norm::{
            Grid, ThreadConfig, compute_single_crystal_norm,
        };

        let grid = Grid::new(
            grid.0.as_array(),
            grid.1.as_array(),
            grid.2.as_array(),
            grid.3.as_array(),
        );

        compute_single_crystal_norm(
            start.as_array(),
            stop.as_array(),
            solid_angle.as_array(),
            grid,
            ThreadConfig::new(n_threads, block_size),
        )
        .into_pyarray(py)
    }
}
