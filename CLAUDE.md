# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-script webcam motion detector. `capture.py` reads frames from the default camera (`cv2.VideoCapture(0)`), detects motion, and logs the start/end timestamp of each motion interval to `Times.csv`.

## Commands

```bash
pip install opencv-python pandas   # runtime dependencies (no requirements.txt / venv)
python capture.py                  # run; opens 4 preview windows, press 'q' to quit and write Times.csv

pip install pytest                 # test dependency
python -m pytest                   # run the tests (no camera needed)
```

There is no linter or build step.

## How the detection works (capture.py)

The camera loop lives in `main()`; the per-frame logic is factored into pure, testable functions (`preprocess_frame`, `detect_motion`, `record_transition`, `pair_times`, `build_dataframe`) that `test_capture.py` covers without a webcam. Key details worth knowing before editing:

- **Reference frame model**: the *first* captured frame (grayscaled + Gaussian-blurred) is stored as `first_frame` and every later frame is diff'd against it — it is never updated. So detection is relative to the initial scene, not the previous frame; lighting drift or a moved object that stays put will keep reading as motion.
- **Motion pipeline**: grayscale → `GaussianBlur(21,21)` → `absdiff` vs `first_frame` → `threshold(30)` → `dilate(iterations=2)` → `findContours`. A contour with `contourArea >= 1000` counts as motion. Lower the `1000` for more sensitivity, raise it for less (documented in README).
- **Interval logging**: `status_list` tracks per-frame motion (0/1). A 0→1 transition appends a "start" time, a 1→0 transition appends an "end" time. After the loop, if the count is odd, `datetime.now()` is appended to close the open interval, then `times` is paired up into Start/End rows.
- **Output**: `df.to_csv("Times.csv")` overwrites the file each run and includes the default pandas index column (hence the leading unnamed column in `Times.csv`).

## Constraints

- Requires a physical webcam; `video.read()` will fail with no camera attached. There is no headless/file-input mode.
- Runs interactively only (uses `cv2.imshow` windows and keyboard input).
