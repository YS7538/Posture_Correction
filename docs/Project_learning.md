# Project Learnings

This project started as a simple posture detector based only on forward head lean. During development, it evolved into a multi-metric real-time posture monitoring utility and became a valuable learning experience in computer vision, software architecture, debugging, and Python development.

## Computer Vision & MediaPipe

* Learned how MediaPipe Pose Landmarker works and how pose landmarks are represented.
* Understood landmark coordinates (`x`, `y`, `z`) and how they can be used to derive meaningful posture metrics.
* Learned to extract specific landmarks such as ears, shoulders, and nose for posture analysis.
* Discovered the limitations of pose estimation systems, including landmark occlusion, lighting sensitivity, and temporary tracking failures.

## Real-Time Systems

* Learned how webcam frames are continuously processed in a real-time application.
* Understood the difference between synchronous and asynchronous processing.
* Worked with MediaPipe's callback-based architecture using `detect_async()`.
* Learned how application state must persist across frames in a real-time pipeline.

## Posture Analysis

Initially, posture was determined only using forward lean measurements.

The system was later improved by combining multiple posture indicators:

* Forward Lean Detection
* Head Offset Detection
* Shoulder Tilt Detection

This demonstrated an important engineering principle:

> Multiple imperfect signals often produce better results than a single perfect-looking metric.

## Calibration Systems

One of the biggest improvements was implementing personalized calibration.

Key lessons:

* Hardcoded thresholds work poorly across different users.
* Personalized baselines significantly improve accuracy.
* Calibration should collect data over time rather than from a single frame.
* Real-time systems should avoid blocking loops during calibration.

A major bug occurred when calibration was implemented using a `while` loop inside the callback function. This froze the entire application because frame processing could not continue.

The solution was to:

* Collect one sample per frame
* Track elapsed time
* Compute averages after the calibration period ends

This resulted in smoother behavior and a much better user experience.

## Debugging & Problem Solving

Several debugging lessons came from this project:

### Global State Management

Initially, posture values updated inside callbacks were not reflected elsewhere in the application.

This led to learning:

* Variable scope
* Global variables
* State sharing between functions

### Blocking Operations

Audio alerts originally froze the webcam feed.

Investigation revealed that:

* `playsound()` is a blocking function.
* While the sound was playing, frame processing stopped.

This problem introduced the concept of threading.

## Threading

To prevent the webcam feed from freezing, audio playback was moved into a separate thread.

Key concepts learned:

* What threads are
* Why blocking functions cause responsiveness issues
* Function references vs function calls
* Running independent tasks concurrently

Example:

Instead of executing:

`playsound()`

directly inside the detection pipeline, a separate worker thread was launched to handle audio playback.

This was my first practical use of concurrency in Python.

## Project Organization

During development, I also learned several software engineering practices:

* Using virtual environments
* Managing dependencies with `requirements.txt`
* Writing documentation
* Structuring project directories
* Using relative paths with `pathlib`
* Maintaining Git repositories with meaningful commits

## Application Packaging & Deployment

As the project matured, the focus shifted from posture detection to software distribution and usability.

### Packaging Challenges

While preparing the application for deployment, several practical software engineering challenges emerged:

* Managing project assets such as audio files and MediaPipe model files
* Converting absolute paths into portable relative paths
* Organizing project files into a maintainable directory structure
* Preparing dependency management through `requirements.txt`

### PyInstaller

I learned how desktop applications can be distributed without requiring users to install Python or manually configure environments.

Key concepts explored:

* Executable generation using PyInstaller
* One-file vs one-folder builds
* Console vs no-console applications
* Dependency bundling
* Asset packaging considerations

### Resource Management

A notable issue occurred after migrating to `pathlib`.

MediaPipe expected string paths, but `pathlib` returned `WindowsPath` objects, causing runtime errors.

This led to learning:

* Differences between `Path` objects and strings
* Library compatibility issues
* Converting paths using `str(path)` when required

### Future Deployment Goals

Planned deployment improvements include:

* Creating a standalone executable
* Running as a background utility
* System tray integration
* Startup on boot
* Cross-device portability
* Simplified installation process

### Key Lesson

Building a working application is only part of software development.

Making software portable, maintainable, and easy for others to use introduces an entirely new set of engineering challenges involving packaging, dependency management, deployment, and user experience.


## Git & GitHub

This project helped reinforce:

* Repository management
* Incremental commits
* Commit message conventions
* Documentation through README files
* Tracking project progress through version control

## Key Takeaway

The biggest lesson from this project was that building a real application teaches concepts much more effectively than simply reading about them.

Through a single project, I gained practical experience with:

* Computer Vision
* Real-Time Processing
* State Management
* Threading
* Debugging
* Calibration Systems
* Software Packaging Preparation
* Git and GitHub Workflows

This project transformed from a simple posture detector into a complete learning experience in designing and building real-world software systems.
