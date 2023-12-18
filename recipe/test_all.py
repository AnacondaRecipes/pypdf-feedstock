import subprocess
import sys
from pathlib import Path

COV_FAIL_UNDER = 80
UTF8 = dict(encoding="utf-8")
# ignore pycryptodome, only used in py36
MYPY_OVERRIDES = """
[[tool.mypy.overrides]]
ignore_missing_imports = true
module = [
    "Crypto",
    "Crypto.*",
]
"""

HERE = Path(__file__).parent
SRC = HERE / "src"
PYPROJECT_TOML = SRC / "pyproject.toml"

OR_JOIN = " or ".join
# mostly to avoid external assets
M_SKIPS = ["external", "samples", "enable_socket"]
K_SKIPS = [
    # mostly external assets
    "ASurveyofImageClassificationBasedTechniques",
    "encrypt_stream_dictionary",
    "escapedcode_followed_by_int",
    "image_similarity",
    "iss1710",
    "multi_language",
    "old_habibi",
    "pdfa",
    "watermarking_reportlab_rendering",
    # py312:  a bytes-like object is required, not 'str'
    "merging_many_temporary_files",
]

PYTEST_ARGS = [
    sys.executable,
    "-m",
    "pytest",
    "-vv",
    "--color=yes",
    "-m",
    f"not ({OR_JOIN(M_SKIPS)})",
    "-k",
    f"not ({OR_JOIN(K_SKIPS)})",
    "--cov=pypdf",
    "--cov-branch",
    "--cov-report=term-missing:skip-covered",
    "--no-cov-on-fail",
    f"--cov-fail-under={COV_FAIL_UNDER}",
]

MYPY_ARGS = ["mypy", "-p", "pypdf"]


if __name__ == "__main__":
    print(">>> ", "\t".join(PYTEST_ARGS), flush=True)
    rc = subprocess.call(PYTEST_ARGS, cwd=str(SRC))
    if rc == 0:
        new_ppt = "\n\n".join([PYPROJECT_TOML.read_text(**UTF8), MYPY_OVERRIDES])
        print(new_ppt, flush=True)
        PYPROJECT_TOML.write_text(new_ppt, **UTF8)
        print("updated pyproject.toml")
        print(">>> ", "\t".join(MYPY_ARGS), flush=True)
        rc = subprocess.call(MYPY_ARGS, cwd=str(SRC))
    sys.exit(rc)
