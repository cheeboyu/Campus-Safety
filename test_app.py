"""
Module Name: test_app.py
Purpose: Automated test script to verify core logic functions and AI response parsing with strict type-safety.
"""

import sys
from typing import Any, Callable, cast
from logic_manager import (
    score as _score,  # type: ignore[reportUnknownVariableType]
    route as _route,  # type: ignore[reportUnknownVariableType]
    sort_incidents_by_severity as _sort_incidents_by_severity,  # type: ignore[reportUnknownVariableType]
)
from ai_manager import parse_response as _parse_response  # type: ignore[reportUnknownVariableType]

score: Callable[[dict[str, Any]], float] = cast(
    Callable[[dict[str, Any]], float],
    _score,
)
route: Callable[[dict[str, Any]], str] = cast(
    Callable[[dict[str, Any]], str],
    _route,
)
sort_incidents_by_severity: Callable[[list[dict[str, Any]]], list[dict[str, Any]]] = cast(
    Callable[[list[dict[str, Any]]], list[dict[str, Any]]],
    _sort_incidents_by_severity,
)
parse_response: Callable[[Any], dict[str, Any] | None] = cast(
    Callable[[Any], dict[str, Any] | None],
    _parse_response,
)

def test_scoring() -> None:
    print("Running test_scoring...")
    record_high: dict[str, Any] = {"severity": "High", "impact_headcount": 60}
    s_high = score(record_high)
    assert s_high > 10, f"Expected high score, got {s_high}"

    record_low: dict[str, Any] = {"severity": "Low", "impact_headcount": 5}
    s_low = score(record_low)
    assert s_low == 1.5, f"Expected score 1.5, got {s_low}"
    print("test_scoring passed successfully!")

def test_routing() -> None:
    print("Running test_routing...")
    rec_crit: dict[str, Any] = {"severity": "Critical", "priority_score": 20}
    assert route(rec_crit) == "Urgent Emergency Dispatch"

    rec_std: dict[str, Any] = {"severity": "Low", "priority_score": 1}
    assert route(rec_std) == "Standard Maintenance Queue"
    print("test_routing passed successfully!")

def test_severity_sorting() -> None:
    print("Running test_severity_sorting...")
    unsorted: list[dict[str, Any]] = [
        {"incident_id": "1", "severity": "Low"},
        {"incident_id": "2", "severity": "Critical"},
        {"incident_id": "3", "severity": "High"}
    ]
    sorted_recs = sort_incidents_by_severity(unsorted)
    assert sorted_recs[0]["severity"] == "Critical"
    assert sorted_recs[1]["severity"] == "High"
    assert sorted_recs[2]["severity"] == "Low"
    print("test_severity_sorting passed successfully!")

def test_parse_response() -> None:
    """Tests that parse_response correctly strips markdown code block wrappers from AI raw strings."""
    print("Running test_parse_response...")
    raw_input = "```json\n{\"risk_summary\": \"test\", \"category\": \"Electrical\", \"severity\": \"High\", \"operational_impact\": \"Severe\", \"contextual_insights\": \"test\"}\n```"
    parsed = parse_response(raw_input)
    assert isinstance(parsed, dict), "Expected parsed output to be a dictionary"
    assert parsed.get("category") == "Electrical", f"Expected Electrical category, got {parsed.get('category')}"
    print("test_parse_response passed successfully!")

if __name__ == "__main__":
    print("=== STARTING AUTOMATED TESTS ===")
    try:
        test_scoring()
        test_routing()
        test_severity_sorting()
        test_parse_response()
        print("=== ALL TESTS PASSED CLEANLY ===")
        sys.exit(0)
    except AssertionError as e:
        print(f"Test Failed: {e}")
        sys.exit(1)