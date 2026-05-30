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

## Packaging, Deployment & Distribution Learnings

After the posture detection system was completed, the next challenge was turning the project into a standalone desktop application.

This phase introduced an entirely different set of engineering problems unrelated to posture detection itself.

### PyInstaller Fundamentals

Learned how PyInstaller packages:

* Python interpreter
* Source code
* Dependencies

into a standalone executable.

Key concepts explored:

* Build process
* One-file executables
* Build artifacts
* Dependency collection
* Application distribution

### Dependency Packaging Issues

The first executable build failed with:

```text
ModuleNotFoundError: No module named 'mediapipe.tasks.c'
```

This revealed that some MediaPipe components were not automatically discovered by PyInstaller.

The issue was resolved by using:

```bash
pyinstaller --collect-all mediapipe
```

which forced PyInstaller to include all MediaPipe resources.

### Asset Packaging Problems

After fixing MediaPipe packaging, the executable failed again because:

```text
pose_landmarker_full.task
```

could not be found.

This highlighted an important distinction:

* Python code is packaged automatically.
* External assets are not.

The solution was to explicitly include project assets using:

```bash
--add-data
```

during the build process.

### Runtime Path Handling

A major lesson was learning that:

```python
Path(__file__).parent
```

works during development but behaves differently inside packaged executables.

This led to learning how PyInstaller extracts files into temporary runtime directories and how to access bundled resources correctly using:

```python
sys._MEIPASS
```

A reusable `resource_path()` helper function was implemented to support both development and packaged environments.

### Pathlib Compatibility

During refactoring, MediaPipe produced an error because it expected string paths while `pathlib` returned `Path` objects.

This reinforced the importance of understanding:

* Path objects
* String conversion
* Third-party library expectations

The issue was resolved using:

```python
str(path)
```

when required.

### Git & Deployment Mistakes

While preparing deployment commits, large build artifacts were accidentally committed:

```text
dist/
build/
main.exe
```

This caused GitHub to reject pushes because packaged executables exceeded the 100 MB repository file limit.

Lessons learned:

* Build artifacts should never be committed.
* `.gitignore` is essential.
* Generated files and source code should remain separate.
* Always review `git status` before committing.

### Final Result

Successfully created a standalone executable that:

* Launches without Python installed
* Loads MediaPipe correctly
* Loads project assets correctly
* Performs calibration
* Detects posture
* Plays audio alerts

The executable was tested outside the project directory and functioned correctly, confirming that dependency and asset packaging were successful.

### Key Takeaway

Building the application was only half the challenge.

Making the application portable, distributable, and executable on another system required learning:

* Packaging
* Dependency management
* Resource handling
* Deployment workflows
* Git best practices

This deployment phase provided as many engineering lessons as the original computer vision implementation itself.

