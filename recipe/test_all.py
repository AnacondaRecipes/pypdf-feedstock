import subprocess
import sys
from pathlib import Path

COV_FAIL_UNDER = 80
UTF8 = dict(encoding="utf-8")

HERE = Path(__file__).parent
PYPROJECT_TOML = HERE / "pyproject.toml"

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

# Why: these tests need encrypted PDF fixtures that are removed from the
# packaged tarball (security scanner flags password-protected PDFs).
# --deselect needs each nodeid as its own argv entry -- a single combined
# string with spaces would be passed to pytest as one broken argument.
DESELECT_TESTS = [
    "tests/test_encryption.py::test_encryption",
    "tests/test_encryption.py::test_make_crypt_filter_large_object_number",
    "tests/test_encryption.py::test_pdf_encrypt",
    "tests/test_encryption.py::test_pdf_encrypt_multiple",
    "tests/test_encryption.py::test_are_permissions_valid_none_for_unencrypted",
    "tests/test_encryption.py::test_are_permissions_valid_none_before_decrypt",
    "tests/test_encryption.py::test_are_permissions_valid_true_for_valid_r6",
    "tests/test_encryption.py::test_are_permissions_valid_true_for_v4",
    "tests/test_encryption.py::test_are_permissions_valid_false_when_tampered",
    "tests/test_encryption.py::test_aes256_decrypt_does_not_call_md5",
    "tests/test_encryption.py::test_read_page_from_encrypted_file_aes_256",
    "tests/test_encryption.py::test_merge_encrypted_pdfs",
    "tests/test_encryption.py::test_aesv2_without_length_in_encrypt_dict",
    "tests/test_encryption.py::test_pdf_with_both_passwords",
    "tests/test_merger.py::test_merger_operations_by_traditional_usage_with_writer",
    "tests/test_merger.py::test_merger_operations_by_semi_traditional_usage_with_writer",
    "tests/test_merger.py::test_merger_operation_by_new_usage_with_writer",
    "tests/test_page.py::test_compress_content_streams",
    "tests/test_page.py::test_get_fonts",
    "tests/test_reader.py::test_get_page_of_encrypted_file",
    "tests/test_reader.py::test_read_encrypted_without_decryption",
    "tests/test_reader.py::test_user_access_permissions",
    "tests/test_reader.py::test_wrong_password_error",
    "tests/test_workflows.py::test_decrypt",
    "tests/test_workflows.py::test_text_extraction_encrypted",
]

# appearance_stream_rtl needs arabic_reshaper (conda underscore name) + python-bidi
try:
    import arabic_reshaper  # noqa: F401
    import bidi  # noqa: F401
except ImportError:
    K_SKIPS.append("appearance_stream_rtl")

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
    *[f"--deselect={nodeid}" for nodeid in DESELECT_TESTS],
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
    [(HERE / clobber).unlink() for clobber in CLOBBER]
    print(">>> ", "\t".join(PYTEST_ARGS), flush=True)
    rc = subprocess.call(PYTEST_ARGS, cwd=str(HERE))
    sys.exit(rc)
