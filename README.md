# Photo Watermark

A command-line tool to add date watermarks to your photos based on their EXIF data.

## Features

-   Automatically extracts the shooting date from EXIF data.
-   Customizable font size, color, and position of the watermark.
-   Processes all images in a specified directory.
-   Saves watermarked images to a new sub-directory (`<original_directory_name>_watermark`).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/photo-watermark.git
    cd photo-watermark
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Usage

Run the script from your terminal, providing the path to your image directory.

### Basic Usage

```bash
python watermark.py /path/to/your/photos
```

This will add a white watermark with a font size of 36 to the bottom-right corner of each image.

### Advanced Usage

You can customize the watermark's appearance and position:

-   **Font Size:**
    ```bash
    python watermark.py /path/to/your/photos --font-size 50
    ```

-   **Color:**
    You can use color names (e.g., `red`, `blue`) or hex codes (e.g., `#FF0000`).
    ```bash
    python watermark.py /path/to/your/photos --color yellow
    ```

-   **Position:**
    Available positions are `top-left`, `top-right`, `bottom-left`, `bottom-right`, and `center`.
    ```bash
    python watermark.py /path/to/your/photos --position top-left
    ```

### Example

```bash
python watermark.py ./my_vacation_pics --font-size 48 --color "#FFFF00" --position bottom-left
```

This command will process all images in the `my_vacation_pics` directory, adding a yellow watermark with a font size of 48 to the bottom-left corner of each photo. The new images will be saved in `./my_vacation_pics/my_vacation_pics_watermark/`.
