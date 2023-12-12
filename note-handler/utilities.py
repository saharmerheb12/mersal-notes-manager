from PIL import Image

def overlay_image_on_background(background_path, image_path, output_path, position=(0.5, 0.5), scale=0):
    """
    Overlay the logo on the background at a relative position.
    
    :param background_path: path to the background image (PNG with transparency).
    :param image_path: path to the logo image (JPG or PNG).
    :param output_path: path to save the resulting image (PNG).
    :param position: a tuple (x, y) where x and y are between 0 and 1, representing 
                     the relative position of the center of the image on the background.
    """
    
    # Open the images
    background = Image.open(background_path).convert("RGBA")  # Ensure the image has an alpha channel
    image = Image.open(image_path).convert("RGBA")  # Ensure the logo has an alpha channel, if it's a JPG this will just add a full alpha channel
    
    if scale > 0:
        target_image_size = int(background.width*scale)
        image = image.resize((target_image_size, target_image_size), Image.Resampling.BOX)
    
    # Calculate the position for the logo
    x = int(position[0] * (background.width - image.width))
    y = int(position[1] * (background.height - image.height))
    
    # Overlay the logo onto the background
    background.paste(image, (x, y), image)  # The last parameter is the alpha mask for transparency
    
    # Save the resulting image
    background.save(output_path, "PNG")


def resize(img_path, thumb_max_size):
    thumb_img = Image.open(img_path)
    # Resize the logo to logo_max_size
    thumb_img.thumbnail((thumb_max_size, thumb_max_size), Image.Resampling.BOX)
    return thumb_img
