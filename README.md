# Posture Correction Utility

**A real-time, personalized posture coach powered by computer vision.**

Posture Correction Utility turns a standard webcam into a lightweight ergonomic feedback system. It uses MediaPipe Pose Landmarker to observe key upper-body landmarks, learns an individual's neutral sitting position during a short calibration, and delivers a timely audio cue when poor posture persists.

Built as a desktop-focused Python application, the project pairs a responsive OpenCV camera experience with an asynchronous pose-detection pipeline—making posture feedback immediate without interrupting the video feed.

## Why it matters

Poor posture is usually gradual and easy to miss during focused work. This utility provides a subtle, real-time reminder before a brief slouch becomes a habit. Rather than relying on a one-size-fits-all threshold, it establishes a personal baseline first, which makes feedback more relevant to the person using it.

## Highlights

- **Personalized 10-second calibration** establishes a forward-lean baseline from live landmark samples.
- **Multi-signal posture analysis** combines forward head position, lateral head offset, and shoulder asymmetry.
- **Real-time asynchronous inference** uses MediaPipe's live-stream callback model to keep webcam processing responsive.
- **Persistent-posture alerting** waits until poor posture lasts beyond the configured delay, avoiding noisy frame-by-frame warnings.
- **Non-blocking audio feedback** runs alert playback on a separate thread so the camera view remains fluid.
- **Portable desktop packaging support** resolves bundled model and audio assets correctly in both source and PyInstaller environments.

## How it works

```text
Webcam frame
    |
    v
MediaPipe Pose Landmarker (live stream)
    |
    v
Landmarks: nose, ears, shoulders
    |
    +--> Calibration: learn forward-lean baseline
    |
    v
Posture evaluation
    |-- Forward lean: right ear depth vs. right shoulder depth
    |-- Head offset: nose position vs. shoulder midpoint
    `-- Shoulder tilt: vertical difference between shoulders
    |
    v
Poor posture persists past alert delay? --> threaded audio reminder
```

### Detection logic

At launch, sit upright and remain in a natural, comfortable position for roughly 10 seconds. The application samples forward lean over that period and calculates an individual baseline. Once calibration is complete, posture is marked as poor when any of the following signals exceeds its threshold:

| Signal | What it identifies |
| --- | --- |
| Forward lean | Head moving noticeably forward or backward relative to the calibrated baseline |
| Head offset | Head drifting sideways from the midpoint of the shoulders |
| Shoulder tilt | Uneven shoulder height that can indicate a side lean |

The alert is intentionally delayed by four seconds by default and plays once per poor-posture episode. Returning to a good posture resets the alert state.

## Tech stack

- Python
- MediaPipe Tasks / Pose Landmarker
- OpenCV
- NumPy
- `threading` for responsive alert playback
- `playsound` for audio feedback
- PyInstaller-compatible resource handling

## Quick start

### Prerequisites

- Python 3.10+ recommended
- A webcam
- Windows is the primary tested environment

### Install and run

```bash
git clone <repository-url>
cd Posture_Correction
python -m venv venv
```

Activate the environment on Windows:

```powershell
venv\Scripts\Activate.ps1
```

Install dependencies and launch the application:

```bash
pip install -r requirements.txt
python main.py
```

When the camera window opens, sit upright for the calibration period. Press `q` while the window is focused to exit.

## Project structure

```text
Posture_Correction/
|-- assets/
|   |-- beep.mp3                     # Posture reminder sound
|   `-- pose_landmarker_full.task    # MediaPipe pose model
|-- docs/
|   |-- Future_improvements.md
|   |-- Project_learning.md
|   `-- landmarks_reference
|-- main.py                          # Application entry point and live pipeline
|-- requirements.txt
`-- README.md
```

## Packaging

The application includes a `resource_path()` helper that loads assets from the source tree during development and from PyInstaller's temporary bundle directory in a packaged build. This allows the pose model and audio reminder to travel with the application instead of depending on machine-specific paths.

For MediaPipe-based builds, ensure the package resources and the `assets` directory are included in the PyInstaller command. Build output is intentionally excluded from version control.

## Current scope and considerations

- Webcam visibility, adequate lighting, and unobstructed landmarks improve detection quality.
- The current version evaluates a single detected person and is designed for seated desktop use.
- Detection thresholds for head offset and shoulder tilt are fixed; forward lean is personalized through calibration.
- The project does not yet include background/system-tray operation, analytics, or automated tests.

## Roadmap

- Configurable sensitivity, alert delay, and sounds
- Landmark confidence filtering and temporal smoothing
- One-click recalibration and user profiles
- System-tray/background mode and desktop notifications
- Session insights and posture analytics
- Modular architecture and automated test coverage

## Documentation

- [Project learnings](docs/Project_learning.md) — engineering notes from developing the computer-vision and packaging pipeline.
- [Future improvements](docs/Future_improvements.md) — planned enhancements for detection, UX, and maintainability.

## License

Provided for educational and personal use.
