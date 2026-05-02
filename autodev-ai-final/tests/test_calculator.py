import pytest
from sample_repo.main import add_numbers

def test_add_two_integers():
    assert add_numbers(2, 3) == 5

def test_add_numeric_string():
    assert add_numbers(2, "3") == 5

def test_invalid_input_raises_value_error():
    with pytest.raises(ValueError):
        add_numbers(2, "abc")
