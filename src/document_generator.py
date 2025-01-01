from PIL import Image
import os

def generate_document(images_path, deck_name):
    # Image and padding dimensions in pixels (6.3 cm by 8.8 cm at 300 DPI)
    img_width, img_height = int(6.3 / 2.54 * 300), int(8.8 / 2.54 * 300)
    padding = 10  # Padding between images in pixels

    # A4 dimensions in pixels at 300 DPI
    a4_width, a4_height = 2480, 3508

    # Load all image filenames
    images = sorted(os.listdir(images_path))  # Sort to maintain order

    # List to hold all composite images
    composite_images = []

    # Process each set of 9 images
    for i in range(0, len(images), 9):
        # Create a new image for the composite, sized to A4
        composite_image = Image.new('RGB', (a4_width, a4_height), 'white')

        # Starting coordinates to center the grid on the A4 page
        start_x = (a4_width - (img_width * 3 + padding * 2)) // 2
        start_y = (a4_height - (img_height * 3 + padding * 2)) // 2

        # Loop through up to 9 images for this page
        for j in range(9):
            if i + j < len(images):
                img_path = os.path.join(images_path, images[i + j])
                img = Image.open(img_path)
                img = img.resize((img_width, img_height))

                # Calculate position on the page
                pos_x = start_x + ((img_width + padding) * (j % 3))
                pos_y = start_y + ((img_height + padding) * (j // 3))

                # Paste the image in the correct position
                composite_image.paste(img, (pos_x, pos_y))

        # Append this composite image to the list
        composite_images.append(composite_image)

    # Save all composite images into a PDF file, handling multiple pages
    output_pdf_path = 'documents' + '/' + 'pdfs' + '/' + 'deck-' + deck_name + '.pdf'
    if composite_images:
        composite_images[0].save(output_pdf_path, save_all=True, append_images=composite_images[1:], resolution=100.0)
        print(f"PDF saved as {output_pdf_path}")
    else:
        print("No images to process.")
