import json

import pytest
from pydantic import ValidationError

from eval.golden_set import load_golden_qa_set


def test_loads_valid_items(tmp_path):
    path = tmp_path / "golden_qa.json"
    path.write_text(
        json.dumps(
            [
                {
                    "question": "What does Article 1 of the Constitution declare India to be?",
                    "chunk_text": "India, that is Bharat, shall be a Union of States.",
                }
            ]
        )
    )

    items = load_golden_qa_set(path)

    assert len(items) == 1
    assert items[0].question == "What does Article 1 of the Constitution declare India to be?"
    assert items[0].chunk_text == "India, that is Bharat, shall be a Union of States."


def test_raises_on_item_missing_required_field(tmp_path):
    path = tmp_path / "golden_qa.json"
    path.write_text(json.dumps([{"question": "What does Article 1 declare?"}]))

    with pytest.raises(ValidationError):
        load_golden_qa_set(path)
