import cv2, pandas
from datetime import datetime

# Tuning constants (see README "Tuning the sensitivity")
MIN_CONTOUR_AREA = 1000   # contours smaller than this (px^2) are ignored
THRESHOLD_VALUE = 30      # per-pixel diff above this counts as change
BLUR_KERNEL = (21, 21)    # Gaussian blur kernel to suppress noise


def preprocess_frame(frame):
    """Convert a BGR frame into the grayscale + blurred image used for diffing."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, BLUR_KERNEL, 0)
    return gray


def detect_motion(first_frame, gray, min_area=MIN_CONTOUR_AREA,
                  threshold_value=THRESHOLD_VALUE):
    """Compare a preprocessed frame against the reference frame.

    Returns ``(status, boxes, delta_frame, thresh_frame)`` where:
      - ``status`` is 1 if any contour larger than ``min_area`` is found, else 0
      - ``boxes`` is a list of ``(x, y, w, h)`` bounding rectangles for those contours
      - ``delta_frame`` / ``thresh_frame`` are the intermediate images (for the
        debug windows in ``main``)
    """
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, threshold_value, 255,
                                 cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cnts, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)

    status = 0
    boxes = []
    for contour in cnts:
        if cv2.contourArea(contour) < min_area:
            continue
        status = 1
        boxes.append(cv2.boundingRect(contour))
    return status, boxes, delta_frame, thresh_frame


def record_transition(status_list, times, now=None):
    """Append a timestamp to ``times`` on a 0<->1 edge of the last two statuses.

    A 0->1 edge marks the start of a motion interval and a 1->0 edge marks its
    end. ``now`` lets callers/tests inject a deterministic timestamp; it defaults
    to ``datetime.now()``. Does nothing until at least two statuses exist.
    """
    if len(status_list) < 2:
        return
    prev, curr = status_list[-2], status_list[-1]
    if (curr == 1 and prev == 0) or (curr == 0 and prev == 1):
        times.append(now if now is not None else datetime.now())


def pair_times(times, now=None):
    """Pair a flat list of transition timestamps into ``[start, end]`` rows.

    If the number of timestamps is odd, a closing timestamp (``now`` or
    ``datetime.now()``) is appended so the final open interval is closed,
    matching the end-of-run behavior of ``main``.
    """
    times = list(times)
    if len(times) % 2 != 0:
        times.append(now if now is not None else datetime.now())
    return [[times[i], times[i + 1]] for i in range(0, len(times), 2)]


def build_dataframe(times, now=None):
    """Build the Start/End DataFrame written to Times.csv from raw timestamps."""
    df = pandas.DataFrame(columns=["Start", "End"])
    for row in pair_times(times, now=now):
        df.loc[len(df)] = row
    return df


def main():
    first_frame = None
    status_list = [None, None]
    times = []

    video = cv2.VideoCapture(0)

    while True:
        check, frame = video.read()

        gray = preprocess_frame(frame)

        if first_frame is None:
            first_frame = gray
            continue

        status, boxes, delta_frame, thresh_frame = detect_motion(first_frame, gray)
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        status_list.append(status)
        record_transition(status_list, times)

        cv2.imshow("Gray Frame", gray)
        cv2.imshow("Delta Frame", delta_frame)
        cv2.imshow("Threshold Frame", thresh_frame)
        cv2.imshow("Color Frame", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    print(status_list)
    print(times)

    df = build_dataframe(times)
    df.to_csv("Times.csv")

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
