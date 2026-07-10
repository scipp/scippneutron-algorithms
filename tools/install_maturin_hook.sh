# Custom import hook installation.

# Do not install the hook in CI. We never modify the code in CI
# and the hook requires additional, non-trivial configuration.
if [[ ! -n "$CI" ]]; then
    # Change to this if/when
    # https://github.com/PyO3/maturin-import-hook/issues/29
    # gets fixed:
    #
    #   python -m maturin_import_hook site install

    # This relies on `.python-version` to locate the environment.
    # But that file is unused otherwise. So remove it if we change this
    # to the default hook installation.
    PYTHON_SITE_CUSTOMIZE="$CONDA_PREFIX"/lib/python$(cat "$PIXI_PROJECT_ROOT"/.python-version)/site-packages/sitecustomize.py
    if [ ! -f "$PYTHON_SITE_CUSTOMIZE" ]; then
        cp tools/sitecustomize.py "$PYTHON_SITE_CUSTOMIZE"
    fi
fi
