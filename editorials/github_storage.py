"""
GitHub-backed media storage.

Uploads user-submitted images to a single GitHub repo and returns the
raw.githubusercontent.com URL, which is stored in the DB. Replaces S3.

Uses only the standard library (no requests/Pillow) to keep the project
dependency-light and cheap to run.
"""

import base64
import json
import mimetypes
import uuid
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError

from django.conf import settings


class GitHubStorageError(Exception):
    pass


# ponytail: allow-list; add formats here if needed
ALLOWED_IMAGE_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    "image/webp": "webp",
}


def raw_url_for(path: str) -> str:
    repo = settings.GITHUB_REPO
    branch = settings.GITHUB_BRANCH
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"


def upload_image(uploaded_file) -> str:
    """Upload an in-memory/uploaded file to the configured GitHub repo.

    Returns the raw.githubusercontent.com URL for the stored image.
    """
    token = settings.GITHUB_TOKEN
    repo = settings.GITHUB_REPO
    if not token or not repo:
        raise GitHubStorageError(
            "GitHub storage is not configured (set GITHUB_TOKEN and GITHUB_REPO)."
        )

    content_type = (
        getattr(uploaded_file, "content_type", "")
        or mimetypes.guess_type(uploaded_file.name)[0]
        or ""
    )
    ext = ALLOWED_IMAGE_TYPES.get(content_type)
    if not ext:
        raise GitHubStorageError(
            "Unsupported image type. Allowed: JPEG, PNG, GIF, WebP."
        )

    data = uploaded_file.read()
    if not data:
        raise GitHubStorageError("Empty file.")
    if len(data) > settings.GITHUB_MAX_UPLOAD_BYTES:
        raise GitHubStorageError("Image too large (max 5 MB).")

    filename = f"{uuid.uuid4().hex}.{ext}"
    path = f"{settings.GITHUB_MEDIA_PATH.strip('/')}/{filename}"

    api_url = f"https://api.github.com/repos/{repo}/contents/{path}"
    body = json.dumps(
        {
            "message": f"Add {filename}",
            "content": base64.b64encode(data).decode(),
            "branch": settings.GITHUB_BRANCH,
        }
    ).encode()

    req = urllib_request.Request(
        api_url,
        data=body,
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "dnt-app",
        },
    )
    try:
        with urllib_request.urlopen(req, timeout=30) as resp:
            if resp.status not in (200, 201):
                raise GitHubStorageError(f"GitHub API error: {resp.status}")
    except HTTPError as exc:
        detail = exc.read().decode()[:300]
        raise GitHubStorageError(f"GitHub API error {exc.code}: {detail}")
    except URLError as exc:
        raise GitHubStorageError(f"Could not reach GitHub: {exc.reason}")

    return raw_url_for(path)
