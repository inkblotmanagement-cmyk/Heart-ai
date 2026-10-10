from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def test_app_renders_and_evaluates():
    at = AppTest.from_file(APP, default_timeout=240).run()
    assert not at.exception
    assert "Heart AI" in at.title[0].value
    at.selectbox[0].set_value("Harmful: phishing email").run()
    at.button[0].click().run()
    assert not at.exception
    assert any("Decision: BLOCK" in h.value for h in at.subheader)


def test_app_has_no_fake_claims():
    src = Path(APP).read_text(encoding="utf-8")
    for banned in ("UBI APPROVED", "Poverty = 0%", "PRAY IN CODE", "torch"):
        assert banned not in src
