import sys
from PIL import Image

def generate_image(msd_file, stamps_folder, output_image="output_image.png", transparent_bg=False):
    # Constants
    STAMP_SIZE = 44  # Size for stamps
    IMAGE_SIZE = (480, 360)

    # Create a new image with white background or transparent based on the flag
    if transparent_bg:
        img = Image.new("RGBA", IMAGE_SIZE, (0, 0, 0, 0))  # Transparent background
    else:
        img = Image.new("RGBA", IMAGE_SIZE, (255, 255, 255, 255))  # White background

    with open(msd_file, "r") as file:
        stamp_data = file.readlines()

    # Prepare to read stamp data
    for i in range(1, len(stamp_data), 3):  # Read in groups of 3
        if i + 2 >= len(stamp_data):  # Prevent index error
            break
        
        try:
            stamp_id = int(stamp_data[i + 2].strip())  # Stamp ID
            x = int(stamp_data[i].strip())  # X Coordinate
            y = int(stamp_data[i + 1].strip())  # Y Coordinate
        except ValueError as e:
            print(f"Invalid or insufficient values encountered: {stamp_data[i:i+3]} - {e}")
            continue

        # Load the stamp image
        stamp_image_path = f"{stamps_folder}/stamp{stamp_id}.png"
        try:
            stamp_image = Image.open(stamp_image_path)
            # Resize the stamp
            new_size = (STAMP_SIZE, STAMP_SIZE)
            stamp_image = stamp_image.resize(new_size, Image.LANCZOS)

            # Calculate the position on the image (centered)
            x_centered = (x + IMAGE_SIZE[0] // 2) - (STAMP_SIZE // 2)
            # Invert Y-coordinate
            y_centered = (IMAGE_SIZE[1] // 2) - (y + (STAMP_SIZE // 2))

            # Paste the stamp image onto the main image
            img.paste(stamp_image, (x_centered, y_centered), stamp_image)

        except FileNotFoundError:
            print(f"Stamp ID {stamp_id} image not found.")

    # Save the resulting image
    img.save(output_image)
    print(f"Image generated and saved as {output_image}.")

if __name__ == "__main__":
    # Check if the right number of arguments is provided
    if len(sys.argv) < 4:
        print("Usage: python convert.py [FileName].msd [OutputImageName].png [TransparentBackgroundFlag]")
        sys.exit(1)

    # Read command-line arguments
    msd_file = sys.argv[1]
    output_image = sys.argv[2]
    transparent_bg_flag = sys.argv[3].lower() in ['true', '1', 'yes']

    # Call the function with provided arguments
    generate_image(msd_file, "stamps", output_image, transparent_bg_flag)
