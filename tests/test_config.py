from frontier_lab.config import Settings


def test_no_credentials(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    for key in Settings.model_fields:
        monkeypatch.delenv(key.upper(), raising=False)
        monkeypatch.delenv(key.lower(), raising=False)
    assert all(value is None for value in Settings().model_dump().values())


def test_dotenv_and_environment_precedence(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("OPENAI_API_KEY=dummy-file-value\n")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-environment-value")
    settings = Settings()
    assert settings.openai_api_key.get_secret_value() == "dummy-environment-value"
    assert "dummy-environment-value" not in repr(settings)
    assert "dummy-environment-value" not in settings.model_dump_json()
    monkeypatch.setenv("OPENAI_API_KEY", "")
    assert Settings().openai_api_key.get_secret_value() == "dummy-file-value"


def test_empty_example_is_optional(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    for key in Settings.model_fields:
        monkeypatch.delenv(key.upper(), raising=False)
        monkeypatch.delenv(key.lower(), raising=False)
    (tmp_path / ".env").write_text("OPENAI_API_KEY=\n")
    assert Settings().openai_api_key is None
