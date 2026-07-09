use pyo3::prelude::*;

#[pymodule]
mod _scippneutron_algorithms_lib {
    // use numpy::PyReadonlyArray1;
    use pyo3::prelude::*;

    #[pyfunction]
    fn foo<'py>(py: Python<'py>) -> i64 {
        1234
    }
}
