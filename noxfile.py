"""Config file for Nox sessions
By Edward Jazzhands - 2025

NOTE ABOUT NOX CONFIG:
UV and Nox work amazing together. But in some cases, such as if you are
doing development inside a docker container or in other such niche environments,
UV will not be able to create its normal symlinks when making .venv folders.
(For example you might bind mount a folder into the container which contains
your project, you cannot symlink between the container's filesystem and this folder.
That's a fundamental Linux limitation, not because of UV or Docker.)

This creates a problem where Nox will create a new venv folder with hard
copies of everything for every single test. Nox by default does not reuse
existing virtual environments, but rather it will create a new one for each
session every single time it runs. If you have the aforementioned situation
with UV and the symlinks, this means that Nox will be writing several GB
of data to your drive every single time you run it. The space usage itself is 
not so much an issue as the large amount of writing wear it will cause on your
drive if you are writing anywhere from 2-10gb of data every time you run nox.

Setting `nox.options.reuse_existing_virtualenvs` helps to mitigate this issue.
Nox will reuse environments between runs, preventing however
many GB of data from being written to your drive every time you run nox.

If you do not need to reuse existing virtual environments, you can set
`nox.options.reuse_existing_virtualenvs = False` and `DELETE_VENV_ON_EXIT = True`
to delete the virtual environments after each session. This will ensure that
you do not have any leftover virtual environments taking up space on your drive.
Nox would just delete them when starting a new session anyway.
"""

import nox
import pathlib
import shutil

# PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12"]
PYTHON_VERSIONS = ["3.9"]
MAJOR_TEXTUAL_VERSIONS = [3, 4, 5]

##############
# NOX CONFIG #
##############

nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = True
DELETE_VENV_ON_EXIT = False

if nox.options.reuse_existing_virtualenvs and DELETE_VENV_ON_EXIT:
    raise ValueError(
        "You cannot set both `nox.options.reuse_existing_virtualenvs`"
        "and `DELETE_VENV_ON_EXIT` to True (Technically this would not cause "
        "an error, but it would be pointless)."
    )

################
# NOX SESSIONS #
################

@nox.session(
    venv_backend="uv",
    python=PYTHON_VERSIONS,
)
@nox.parametrize("textual", MAJOR_TEXTUAL_VERSIONS)
def tests(session: nox.Session, textual: int) -> None:

    session.run_install(
        "uv",
        "sync",
        "--quiet",
        "--reinstall",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
        external=True,
    )

    session.run_install(
        "uv", "pip", "install",
        f"textual<{str(textual + 1)}.0.0",
        external=True,
    )
    # EXPLANATION: The `textual + 1` is a trick to make UV
    # only download the last version of each major revision of Textual.
    # If the current version is 3, we're saying `install textual<4.0.0`.
    # This will make UV grab the highest version of Textual 3.x.x, which is 3.7.1.
    
    session.run("uv", "pip", "show", "textual")

    session.run("ruff", "check", "src")
    session.run("mypy", "src")
    session.run("basedpyright", "src")
    session.run("pytest", "tests", "-vvv") 

    session_path = pathlib.Path(session.virtualenv.location)
    if session_path.exists() and session_path.is_dir() and DELETE_VENV_ON_EXIT:
        shutil.rmtree(session_path)
