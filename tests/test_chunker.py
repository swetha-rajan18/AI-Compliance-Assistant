import pytest

from src.retrieval.chunker import create_fixed_chunks


def test_fixed_chunks_split_text():
    text = "abcdefghijklmnopqrstuvwxyz"

    chunks = create_fixed_chunks(
        text,
        chunk_size=10,
        overlap=2,
    )

    assert len(chunks) > 1
    assert chunks[0] == "abcdefghij"


def test_fixed_chunks_have_overlap():
    text = "abcdefghijklmnopqrstuvwxyz"

    chunks = create_fixed_chunks(
        text,
        chunk_size=10,
        overlap=2,
    )

    assert chunks[0][-2:] == chunks[1][:2]


def test_empty_text_returns_empty_list():
    assert create_fixed_chunks("") == []


def test_non_string_input_is_rejected():
    with pytest.raises(TypeError):
        create_fixed_chunks(None)


def test_invalid_chunk_size_is_rejected():
    with pytest.raises(ValueError):
        create_fixed_chunks("hello", chunk_size=0)


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValueError):
        create_fixed_chunks(
            "hello",
            chunk_size=10,
            overlap=10,
        )