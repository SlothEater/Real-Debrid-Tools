# Real-Debrid Tools

Real-Debrid Tools is a Chrome extension and Flask application that allows you to trigger actions for magnet links using the Real-Debrid service.

## Chrome Extension

The Chrome extension provides context menu options for magnet links. It communicates with the Flask application to perform API calls and retrieve results.

### Installation

1. Download the extension folder.
2. Open Chrome and go to `chrome://extensions`.
3. Enable the "Developer mode" toggle.
4. Click on "Load Unpacked" and select the extension folder.

### Usage

1. Right-click on a magnet link.
2. Select one of the available options:
   - **Download**: Sends the magnet link to the Flask application to trigger a download.
   - **Open in VLC**: Sends the magnet link to the Flask application to open it in VLC.

## Flask Application

The Flask application handles API calls to the Real-Debrid service and performs various actions based on the requests received from the Chrome extension.

### Prerequisites

- Python 3.x
- VLC media player installed (provide the path in `constants.py`)

### Installation

1. Clone the repository.
2. Install the required dependencies using pip:
    ```
    pip install -r requirements.txt
    ```


### Configuration

In the `constants.py` file, provide the following configurations:

- `VLC_PATH`: Path to the VLC media player executable.
- `API_KEY`: Your Real-Debrid API key.

### Usage

1. Start the Flask application by running `main.py`:
    ```
    python main.py
    ```
2. The application will run on `http://localhost:5000`.

### API Endpoints

- `/trigger-vlc`: Triggers the download of the magnet link and opens it in VLC.
- `/trigger-save`: Triggers the download of the magnet link and returns the download link.

## License

This project is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
