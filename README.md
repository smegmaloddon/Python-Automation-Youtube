# Python Automation for Video Processing

This project is a Python-based automation tool for video processing tasks, including merging, trimming, normalizing, and more. It leverages FFMPEG for video manipulation and provides a modular structure for various video-related workflows.

## Features

- Video merging and trimming
- Audio peak detection
- Scene detection and ranking
- Video normalization and speed adjustment
- Web content fetching and filtering
- Custom video separators and hooks
- Support for various video formats

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-automation
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main script:
```
python -m src
```

Or use specific workflows from the `workflows/` directory.

## Example

Here's an example of a processed video template:

<video width="640" height="360" controls>
  <source src="docs/videos/template.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Project Structure

- `src/`: Main source code
  - `helpers/`: Helper modules for audio, video, and web
  - `services/`: Service modules for processing tasks
  - `utils/`: Utility functions
  - `workflows/`: Workflow scripts
- `bin/`: Binary dependencies (e.g., FFMPEG)
- `data/`: Configuration files
- `docs/`: Documentation and examples
- `temp/`: Temporary files
- `assets/`: Audio, video, and font assets


