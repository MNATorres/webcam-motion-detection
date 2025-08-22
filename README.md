
# Webcam Motion Detection

![Motion Detection Banner](https://img.shields.io/badge/OpenCV-Motion%20Detection-blue?style=for-the-badge&logo=opencv)

Detect and log motion intervals using your webcam, OpenCV, and pandas. Results are saved in a CSV file.

---

## 🚀 Requirements

- Python 3.8+
- [OpenCV](https://pypi.org/project/opencv-python/)
- [pandas](https://pypi.org/project/pandas/)

Install dependencies with:

```bash
pip install opencv-python pandas
```

---

## 🖥️ Quick Start

1. Clone this repository or download the files.
2. Run the main script:

```bash
python capture.py
```

3. Several windows will open showing the video and processing steps.
4. Press `q` to stop recording.
5. Check the detected motion intervals in the `Times.csv` file.

---

## 📂 What does the script do?

- Starts the webcam and analyzes video in real time.
- Detects significant changes between frames (motion).
- Marks the start and end times of each motion event.
- Saves the intervals in a CSV file for later analysis.

---

## 📝 Example output (`Times.csv`)

| Start                | End                  |
|----------------------|---------------------|
| 2025-08-22 18:02:23  | 2025-08-22 18:03:10 |
| 2025-08-22 18:04:01  | 2025-08-22 18:04:15 |

---

## 🎨 Credits & Resources

- Based on OpenCV and pandas tutorials.
- Author: MNATorres

---

## 💡 Notes

- You can adjust the sensitivity by changing the minimum area value in the script (`cv2.contourArea(contour) < 1000`).
- The script works on Windows, Linux, and MacOS.

---

Contributions and suggestions are welcome!
