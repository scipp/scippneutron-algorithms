# <maturin_import_hook>
# A custom importhook to implement
# https://github.com/PyO3/maturin-import-hook/issues/29
# This can be removed if/when that issue gets fixed.
#
# the following installs the maturin import hook during startup.
# see: `python -m maturin_import_hook site`
try:
    import maturin_import_hook
    from maturin_import_hook.project_importer import DefaultProjectFileSearcher
    from maturin_import_hook.settings import MaturinSettings

    maturin_import_hook.install(
        settings=MaturinSettings(color=True),
        enable_project_importer=True,
        enable_rs_file_importer=False,
        file_searcher=DefaultProjectFileSearcher(
            source_excluded_dir_names={
                *DefaultProjectFileSearcher.DEFAULT_SOURCE_EXCLUDED_DIR_NAMES,
                ".pixi",
            }
        ),
    )
except Exception as e:
    raise RuntimeError(
        f"{e}\n>> ERROR in managed maturin_import_hook installation. "
        "Remove with `python -m maturin_import_hook site uninstall`\n",
    ) from e
# </maturin_import_hook>
