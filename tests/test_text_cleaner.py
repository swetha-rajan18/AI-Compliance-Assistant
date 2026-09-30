from src.ingestion.text_cleaner import clean_text


def test_clean_text_fixes_hyphenated_line_breaks():
    text = "recommenda-\ntion"
    cleaned = clean_text(text)

    assert cleaned == "recommendation"


def test_clean_text_normalizes_line_breaks():
    text = "Artificial Intelligence\nRisk Management\nFramework"
    cleaned = clean_text(text)

    assert cleaned == "Artificial Intelligence Risk Management Framework"


def test_clean_text_collapses_whitespace():
    text = "Artificial    Intelligence   Framework"
    cleaned = clean_text(text)

    assert cleaned == "Artificial Intelligence Framework"


def test_clean_text_strips_outer_whitespace():
    text = "   Artificial Intelligence   "
    cleaned = clean_text(text)

    assert cleaned == "Artificial Intelligence"


def test_clean_text_rejects_non_string():
    try:
        clean_text(None)
        assert False
    except TypeError:
        assert True