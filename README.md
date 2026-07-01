# 📹 Webcam Motion Detection

![OpenCV](https://img.shields.io/badge/OpenCV-Motion%20Detection-blue?style=for-the-badge&logo=opencv)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow?style=for-the-badge&logo=python)

A small computer-vision program that uses your **webcam** to detect movement in real time. Every time it sees motion it records the **start** and **end** timestamps of the event and saves them to a `Times.csv` file for later analysis.

---

## 📖 What it does

The script continuously reads frames from your webcam and compares each new frame against a reference frame to find what has changed. In plain terms:

1. **Captures** live video from the default webcam.
2. **Detects** significant changes between frames (something moving).
3. **Marks** the exact time each motion event starts and ends.
4. **Draws** a green rectangle around the moving object on screen.
5. **Saves** every motion interval (Start / End) to `Times.csv`.

### How the detection works (step by step)

The program runs a classic OpenCV motion-detection pipeline on every frame:

| Step | What happens | Why |
|------|--------------|-----|
| 1. Grayscale | The color frame is converted to gray | Motion depends on brightness, not color |
| 2. Gaussian blur | The image is smoothed (`21×21` kernel) | Removes noise so tiny pixel changes don't trigger false alarms |
| 3. Reference frame | The first frame is stored as the "empty scene" baseline | Everything is compared against this |
| 4. Absolute difference | Current frame is subtracted from the reference | Highlights pixels that changed |
| 5. Threshold | Differences above `30` become white, the rest black | Turns the change into a clean black-and-white mask |
| 6. Dilate | The white regions are expanded | Fills holes so a moving object is one solid blob |
| 7. Contours | Outlines are found in the mask | Each contour is a candidate moving object |
| 8. Area filter | Contours smaller than `1000` px² are ignored | Filters out small / irrelevant movement |
| 9. Timestamp | When motion starts / stops, `datetime.now()` is recorded | This is what gets saved to the CSV |

---

## 🚀 Requirements

- **Python 3.8 or higher**
- A working **webcam**
- Python packages:
  - [`opencv-python`](https://pypi.org/project/opencv-python/) — video capture and image processing
  - [`pandas`](https://pypi.org/project/pandas/) — building and exporting the CSV

---

## 🔧 Installation

1. **Clone or download** this repository:

   ```bash
   git clone <repository-url>
   cd webcam-motion-detection
   ```

2. *(Recommended)* Create and activate a **virtual environment**:

   ```bash
   # Windows (PowerShell)
   python -m venv venv
   venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies**:

   ```bash
   pip install opencv-python pandas
   ```

---

## ▶️ How to run

From the project folder, run:

```bash
python capture.py
```

When it starts, **four windows** will open so you can watch each stage of the processing:

| Window | Shows |
|--------|-------|
| **Color Frame** | The live webcam image with a green box around any detected motion |
| **Gray Frame** | The blurred grayscale version used for analysis |
| **Delta Frame** | The pixel-by-pixel difference vs. the reference frame |
| **Threshold Frame** | The final black-and-white motion mask |

### Controls

- **Stand still** in front of the camera for the first second — the very first frame becomes the reference "empty scene".
- Move around and you'll see the green rectangle track you.
- Press **`q`** (with a video window focused) to **stop** recording and save the results.

---

## 📄 Output — `Times.csv`

When you quit, all detected motion intervals are written to `Times.csv`. Each row is one motion event with its start and end time:

| Start                | End                  |
|----------------------|----------------------|
| 2025-08-22 18:02:23  | 2025-08-22 18:03:10  |
| 2025-08-22 18:04:01  | 2025-08-22 18:04:15  |

---

## ⚙️ Tuning the sensitivity

You can adjust how the detector behaves by editing a couple of values in `capture.py`:

- **Minimum motion size** — line with `cv2.contourArea(contour) < 1000`.
  Increase `1000` to ignore small movements (e.g. a pet), decrease it to catch tiny ones.

- **Change threshold** — `cv2.threshold(delta_frame, 30, 255, ...)`.
  Lower `30` = more sensitive to subtle changes; raise it = only strong changes count.

- **Blur strength** — `cv2.GaussianBlur(gray, (21, 21), 0)`.
  A larger kernel smooths more (less noise, less detail).

---

## ⚠️ Notes & limitations

- The reference frame is **fixed to the first frame**, so large lighting changes (a light turning on, sunlight moving) can be picked up as motion. Restart the script if the scene's lighting changes a lot.
- Make sure **no other application** is using the webcam, or `cv2.VideoCapture(0)` won't open it.
- If you have more than one camera, change the index in `cv2.VideoCapture(0)` (try `1`, `2`, …).
- Works on **Windows, Linux, and macOS**.

---

## 🎨 Credits

- Built with **OpenCV** and **pandas**, based on classic motion-detection tutorials.
- Author: **MNATorres**

---

Contributions and suggestions are welcome! 🙌
