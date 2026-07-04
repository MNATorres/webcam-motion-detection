"""Tests for capture.py.

These exercise the pure logic extracted from the webcam loop, so they need no
camera: motion detection runs on synthetic numpy frames, and the interval
logic is driven with injected timestamps.
"""
from datetime import datetime

import numpy as np
import pandas as pd
import pytest

import capture


# --- helpers ---------------------------------------------------------------

def blank_frame(h=240, w=320):
    """A black BGR frame (H, W, 3) uint8."""
    return np.zeros((h, w, 3), dtype=np.uint8)


def frame_with_square(size, value=255, top=20, left=20, h=240, w=320):
    """A black frame with a filled ``size``x``size`` bright square drawn on it."""
    frame = blank_frame(h, w)
    frame[top:top + size, left:left + size] = value
    return frame


# --- preprocess_frame ------------------------------------------------------

def test_preprocess_frame_returns_2d_grayscale():
    gray = capture.preprocess_frame(blank_frame(120, 160))
    assert gray.shape == (120, 160)      # color channel collapsed
    assert gray.dtype == np.uint8


# --- detect_motion ---------------------------------------------------------

def test_no_motion_between_identical_frames():
    ref = capture.preprocess_frame(blank_frame())
    status, boxes, _, _ = capture.detect_motion(ref, ref)
    assert status == 0
    assert boxes == []


def test_large_object_is_detected_as_motion():
    ref = capture.preprocess_frame(blank_frame())
    gray = capture.preprocess_frame(frame_with_square(120))
    status, boxes, delta, thresh = capture.detect_motion(ref, gray)

    assert status == 1
    assert len(boxes) == 1
    x, y, w, h = boxes[0]
    assert w * h > capture.MIN_CONTOUR_AREA   # the box covers a large area
    # debug frames come back same size as the input, single channel
    assert delta.shape == ref.shape
    assert thresh.shape == ref.shape


def test_tiny_object_below_area_threshold_is_ignored():
    ref = capture.preprocess_frame(blank_frame())
    gray = capture.preprocess_frame(frame_with_square(6))
    status, boxes, _, _ = capture.detect_motion(ref, gray)
    assert status == 0
    assert boxes == []


def test_min_area_parameter_controls_sensitivity():
    ref = capture.preprocess_frame(blank_frame())
    gray = capture.preprocess_frame(frame_with_square(60))

    # A 60x60 change is well above the default 1000 px^2 threshold -> detected.
    assert capture.detect_motion(ref, gray)[0] == 1
    # Raise the bar past any possible contour -> nothing qualifies.
    assert capture.detect_motion(ref, gray, min_area=10_000_000)[0] == 0


def test_threshold_value_parameter_affects_detection():
    ref = capture.preprocess_frame(blank_frame())
    # A dim square (value 40): a low threshold catches it, a high one doesn't.
    gray = capture.preprocess_frame(frame_with_square(120, value=40))
    assert capture.detect_motion(ref, gray, threshold_value=20)[0] == 1
    assert capture.detect_motion(ref, gray, threshold_value=200)[0] == 0


# --- record_transition -----------------------------------------------------

TS = datetime(2025, 1, 1, 12, 0, 0)


def test_rising_edge_0_to_1_records_start():
    times = []
    capture.record_transition([0, 1], times, now=TS)
    assert times == [TS]


def test_falling_edge_1_to_0_records_end():
    times = []
    capture.record_transition([1, 0], times, now=TS)
    assert times == [TS]


@pytest.mark.parametrize("status_list", [[0, 0], [1, 1]])
def test_no_edge_records_nothing(status_list):
    times = []
    capture.record_transition(status_list, times, now=TS)
    assert times == []


def test_fewer_than_two_statuses_is_a_noop():
    times = []
    capture.record_transition([None], times, now=TS)
    capture.record_transition([], times, now=TS)
    assert times == []


def test_initial_none_pair_records_nothing():
    # status_list starts as [None, None]; the first real append makes [None, s]
    # which must not be treated as an edge.
    times = []
    capture.record_transition([None, 1], times, now=TS)
    assert times == []


# --- pair_times ------------------------------------------------------------

def test_pair_times_even_list():
    t = [datetime(2025, 1, 1, 0, 0, s) for s in range(4)]
    assert capture.pair_times(t) == [[t[0], t[1]], [t[2], t[3]]]


def test_pair_times_odd_list_appends_closing_timestamp():
    t = [datetime(2025, 1, 1, 0, 0, s) for s in range(3)]
    closing = datetime(2025, 1, 1, 0, 0, 9)
    rows = capture.pair_times(t, now=closing)
    assert rows == [[t[0], t[1]], [t[2], closing]]


def test_pair_times_empty_list():
    assert capture.pair_times([]) == []


def test_pair_times_does_not_mutate_input():
    t = [datetime(2025, 1, 1, 0, 0, 0)]   # odd -> triggers the append path
    original = list(t)
    capture.pair_times(t, now=TS)
    assert t == original


# --- build_dataframe -------------------------------------------------------

def test_build_dataframe_shape_and_values():
    t = [datetime(2025, 1, 1, 0, 0, s) for s in range(4)]
    df = capture.build_dataframe(t)
    assert list(df.columns) == ["Start", "End"]
    assert len(df) == 2
    assert df.iloc[0]["Start"] == t[0]
    assert df.iloc[1]["End"] == t[3]


def test_build_dataframe_closes_odd_interval():
    t = [datetime(2025, 1, 1, 0, 0, s) for s in range(3)]
    closing = datetime(2025, 1, 1, 0, 0, 9)
    df = capture.build_dataframe(t, now=closing)
    assert len(df) == 2
    assert df.iloc[1]["End"] == closing


def test_build_dataframe_empty():
    df = capture.build_dataframe([])
    assert list(df.columns) == ["Start", "End"]
    assert len(df) == 0
