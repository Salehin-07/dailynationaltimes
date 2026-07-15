from io import BytesIO
from unittest import mock

from django.conf import settings
from django.test import TestCase, override_settings

from editorials.github_storage import GitHubStorageError, raw_url_for, upload_image


class FakeResponse:
    def __init__(self, status=201):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return b""


@override_settings(
    GITHUB_REPO="owner/repo",
    GITHUB_BRANCH="main",
    GITHUB_TOKEN="tok",
    GITHUB_MEDIA_PATH="media/posts",
)
class GitHubStorageTests(TestCase):
    def test_raw_url_for(self):
        self.assertEqual(
            raw_url_for("media/posts/a.jpg"),
            "https://raw.githubusercontent.com/owner/repo/main/media/posts/a.jpg",
        )

    @mock.patch("editorials.github_storage.urllib_request.urlopen")
    def test_upload_returns_raw_url(self, urlopen):
        urlopen.return_value = FakeResponse()
        f = BytesIO(b"\xff\xd8\xfffakejpg")
        f.name = "x.jpg"
        f.content_type = "image/jpeg"
        url = upload_image(f)
        self.assertTrue(url.startswith("https://raw.githubusercontent.com/owner/repo/main/media/posts/"))
        self.assertTrue(url.endswith(".jpg"))

    @mock.patch("editorials.github_storage.urllib_request.urlopen")
    def test_upload_rejects_bad_type(self, urlopen):
        f = BytesIO(b"not an image")
        f.name = "x.txt"
        f.content_type = "text/plain"
        with self.assertRaises(GitHubStorageError):
            upload_image(f)

    @mock.patch("editorials.github_storage.urllib_request.urlopen")
    def test_upload_raises_on_api_error(self, urlopen):
        urlopen.side_effect = GitHubStorageError("GitHub API error 401")
        f = BytesIO(b"\xff\xd8\xfffakejpg")
        f.name = "x.jpg"
        f.content_type = "image/jpeg"
        with self.assertRaises(GitHubStorageError):
            upload_image(f)
