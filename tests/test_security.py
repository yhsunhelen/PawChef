"""Security checks: no leaked secrets, .env protection, .env.example present."""
import os
import re
import glob


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Patterns that look like real API keys
_SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9\-_]{20,}"),   # Anthropic
    re.compile(r"sk-[A-Za-z0-9]{30,}"),            # OpenAI / DeepSeek
]

_EXCLUDED_DIRS = {".venv", "venv", ".git", "__pycache__", "node_modules"}


def _tracked_source_files():
    """Return .py and .env* files that are not excluded dirs and not .env itself."""
    results = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in _EXCLUDED_DIRS]
        for fname in files:
            if fname == ".env":
                continue
            if fname.endswith(".py") or fname.startswith(".env"):
                results.append(os.path.join(root, fname))
    return results


class TestNoLeakedSecrets:
    def test_no_api_keys_in_source_files(self):
        leaked = []
        for fpath in _tracked_source_files():
            try:
                content = open(fpath, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for pattern in _SECRET_PATTERNS:
                if pattern.search(content):
                    leaked.append(fpath)
                    break
        assert leaked == [], f"Potential API keys found in: {leaked}"


class TestEnvProtection:
    def test_env_file_not_in_repo(self):
        env_path = os.path.join(REPO_ROOT, ".env")
        gitignore_path = os.path.join(REPO_ROOT, ".gitignore")
        if not os.path.exists(gitignore_path):
            return
        content = open(gitignore_path).read()
        assert ".env" in content, ".env must be listed in .gitignore"

    def test_env_example_exists(self):
        example = os.path.join(REPO_ROOT, ".env.example")
        assert os.path.exists(example), ".env.example must exist in repo root"

    def test_env_example_has_no_real_keys(self):
        example = os.path.join(REPO_ROOT, ".env.example")
        if not os.path.exists(example):
            return
        content = open(example, encoding="utf-8").read()
        for pattern in _SECRET_PATTERNS:
            assert not pattern.search(content), ".env.example must not contain real API keys"

    def test_env_example_documents_required_keys(self):
        example = os.path.join(REPO_ROOT, ".env.example")
        if not os.path.exists(example):
            return
        content = open(example, encoding="utf-8").read()
        assert "API_KEY" in content, ".env.example should document at least one API_KEY variable"
