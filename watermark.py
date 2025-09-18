import argparse
import os
from PIL import Image, ImageDraw, ImageFont, ExifTags

def get_exif_date(img):
    """Extracts the photo's shooting date from its EXIF data."""
    try:
        exif_data = img._getexif()
        if not exif_data:
            return None

        for tag, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            if tag_name == 'DateTimeOriginal':
                return value.split(' ')[0].replace(':', '-')
    except (AttributeError, KeyError, IndexError):
        return None
    return None

def add_watermark(image_path, output_path, font_size_arg, color, position):
    """Adds a date watermark to an image."""
    try:
        with Image.open(image_path) as img:
            date_str = get_exif_date(img)
            if not date_str:
                print(f"Skipping {os.path.basename(image_path)}: No EXIF date found.")
                return

            # If font_size is not provided, calculate it based on image width
            if font_size_arg == 0:
                font_size = int(img.width / 40)
            else:
                font_size = font_size_arg

            draw = ImageDraw.Draw(img)
            
            try:
                # Try to use a common system font, fallback to a basic one
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                print("Arial font not found. Using default font.")
                # For default font, we can't set size, so we use a new approach for it
                # This is a limitation of the default font in Pillow
                if font_size_arg != 0:
                    print("Warning: Cannot set font size with default font. The size will be small.")
                font = ImageFont.load_default()

            text_bbox = draw.textbbox((0, 0), date_str, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            img_width, img_height = img.size
            margin = 10
            
            positions = {
                "top-left": (margin, margin),
                "top-right": (img_width - text_width - margin, margin),
                "bottom-left": (margin, img_height - text_height - margin),
                "bottom-right": (img_width - text_width - margin, img_height - text_height - margin),
                "center": ((img_width - text_width) / 2, (img_height - text_height) / 2)
            }
            
            text_position = positions.get(position.lower())
            if not text_position:
                print(f"Invalid position: {position}. Using bottom-right.")
                text_position = positions["bottom-right"]

            draw.text(text_position, date_str, font=font, fill=color)
            
            img.save(output_path)
            print(f"Watermarked image saved to: {output_path}")

    except IOError:
        print(f"Error processing {os.path.basename(image_path)}. It might be a non-image file or corrupted.")
    except Exception as e:
        print(f"An unexpected error occurred with {os.path.basename(image_path)}: {e}")


def main():
    """Main function to parse arguments and process images."""
    parser = argparse.ArgumentParser(description="Add date watermarks to photos based on EXIF data.")
    parser.add_argument("directory", help="Path to the directory containing images.")
    parser.add_argument("--font-size", type=int, default=0, help="Font size for the watermark text. Default is dynamic based on image width.")
    parser.add_argument("--color", default="white", help="Color of the watermark text (e.g., 'white', '#FFFFFF').")
    parser.add_argument("--position", default="bottom-right", choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"], help="Position of the watermark on the image.")
    
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory not found at '{args.directory}'")
        return

    output_dir_name = os.path.basename(os.path.abspath(args.directory)) + "_watermark"
    output_dir = os.path.join(args.directory, output_dir_name)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    for filename in os.listdir(args.directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            image_path = os.path.join(args.directory, filename)
            output_path = os.path.join(output_dir, filename)
            add_watermark(image_path, output_path, args.font_size, args.color, args.position)

if __name__ == "__main__":
    main()
