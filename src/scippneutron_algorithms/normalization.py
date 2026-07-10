import numpy as np

from ._scippneutron_algorithms_lib import foo


def bar() -> int:
    return foo(np.arange(3.0))  # type: ignore[no-any-return]
