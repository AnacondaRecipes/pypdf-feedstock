import subprocess
import sys
from pathlib import Path

COV_FAIL_UNDER = 80
UTF8 = dict(encoding="utf-8")

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
    # https://github.com/conda-forge/pypdf-feedstock/pull/44
    "get_images_raw",
    "issue604",
    "read_prev_0_trailer",
    "read_unknown_zero_pages",
    # https://github.com/conda-forge/pypdf-feedstock/pull/46
    "calling_indirect_objects",
    # https://github.com/conda-forge/pypdf-feedstock/pull/50
    "writer_xmp_metadata_samples",
    "increment_writer",
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

CLOBBER = [
    # https://github.com/conda-forge/pypdf-feedstock/pull/46
    "tests/scripts/test_make_release.py",
]

if __name__ == "__main__":
    [(SRC / clobber).unlink() for clobber in CLOBBER]
    print(">>> ", "\t".join(PYTEST_ARGS), flush=True)
    rc = subprocess.call(PYTEST_ARGS, cwd=str(SRC))
    sys.exit(rc)
