import os
import pathlib
import re

import pytest
import sqlite_utils
from click.testing import CliRunner
from warcdb import warcdb_cli

test_files = pathlib.Path(__file__).parent / "files"

# all these WARC files were created with wget except for apod.warc.gz which was
# created with browsertrix-crawler


@pytest.mark.parametrize(
    "warc_path",
    [
        str(test_files / "google.warc"),
        str(test_files / "google.warc.gz"),
        str(test_files / "no-warc-info.warc"),
        str(test_files / "scoop.wacz"),
        "https://tselai.com/data/google.warc",
        "https://tselai.com/data/google.warc.gz",
    ],
)
def test_import(db_path, warc_path):
    runner = CliRunner()
    args = ["import", db_path, warc_path]
    result = runner.invoke(warcdb_cli, args)
    assert result.exit_code == 0
    db = sqlite_utils.Database(db_path)
    assert set(db.table_names()) == {
        "metadata",
        "request",
        "resource",
        "response",
        "warcinfo",
        "_sqlite_migrations",
    }

    if warc_path == str(test_files / "google.warc"):
        assert db.table("warcinfo").get(
            "<urn:uuid:7ABED2CA-7CBD-48A0-92E5-0059EBFC111A>"
        )
        assert db.table("request").get(
            "<urn:uuid:524F62DD-D788-4085-B14D-22B0CDC0AC53>"
        )

    # os.remove(db_path)


def test_column_names(db_path):
    print(db_path)
    runner = CliRunner()
    runner.invoke(
        warcdb_cli, ["import", db_path, str(pathlib.Path("tests/google.warc"))]
    )

    # make sure that the columns are named correctly (lowercase with underscores)
    db = sqlite_utils.Database(db_path)
    for table in db.tables:
        for col in table.columns:
            assert re.match(r"^[a-z_]+", col.name), f"column {col.name} named correctly"


# def test_http_header():
#     runner = CliRunner()
#     runner.invoke(
#         warcdb_cli, ["import", db_file, str(pathlib.Path("tests/google.warc"))]
#     )
#
#     db = sqlite_utils.Database(db_file)
#
#     resp_headers = list(db["v_response_http_header"].rows)
#     assert len(resp_headers) == 43
#     assert {
#         "name": "content-type",
#         "value": "text/html; charset=UTF-8",
#         "warc_record_id": "<urn:uuid:2008CBED-030B-435B-A4DF-09A842DDB764>",
#     } in resp_headers
#
#     req_headers = list(db["v_request_http_header"].rows)
#     assert len(req_headers) == 17
#     assert {
#         "name": "user-agent",
#         "value": "Wget/1.21.3",
#         "warc_record_id": "<urn:uuid:6E9096E2-5D54-4CD6-A157-1DE4A7040DEB>",
#     } in req_headers


def test_http_header(db_path):
    print(db_path)
    runner = CliRunner()
    runner.invoke(
        warcdb_cli, ["import", db_path, str(pathlib.Path("tests/google.warc"))]
    )
    db = sqlite_utils.Database(db_path)
    # responses = db["response"].rows
    # assert next(responses)["http_status"] == 301
    # assert next(responses)["http_status"] == 302
    # assert next(responses)["http_status"] == 200
