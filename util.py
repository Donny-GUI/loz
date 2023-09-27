import customtkinter
from PIL import Image
import webcolors
import os
import tkinter as tk
from PIL import ImageTk, Image

rgb_values = [(r, g, b) for r in range(256) for g in range(256) for b in range(256)]


class RGBPixel:
    def __init__(self, tuple_pixels) -> None:
        self._red = tuple_pixels[0]
        self._green = tuple_pixels[1]
        self._blue = tuple_pixels[2]
        self._value = (self._red, self._green, self._blue)
        self._name = None 
        self._update_name()

    def _update_name(self):
        try:
            self._name = webcolors.rgb_to_name(self.pixel)
        except ValueError:
            self._name = "Unknown"

    def _update_value(self):
        self._value = (self._red, self._green, self._blue)
    
    @property 
    def name(self):
        return self._name
    
    @property
    def value(self):
        return self._value
    
    @property 
    def pixel(self):
        return (self._red, self._green, self._blue)

    @property 
    def blue(self):
        return self._blue 

    @property 
    def red(self):
        return self._red 

    @property 
    def green(self):
        return self._green 

    def set(self, __value):
        if isinstance(__value, tuple):
            self._red   = __value[0]
            self._green = __value[1]
            self._blue  = __value[2]
        elif isinstance(__value, RGBPixel):
            self._red   = __value.red
            self._green = __value.green
            self._blue  = __value.blue

    def set_red(self, __value: int) -> None:
        self._red = __value
        if self._red > 255:
            self._red = 255
        elif self._red < 0:
            self._red = 0
        self._update_value()
        self._update_name()
    
    def set_green(self, __value: int) -> None:
        self._green = __value
        if self._green > 255:
            self._green = 255
        elif self._green < 0:
            self._green = 0
        self._update_value()
        self._update_name()
        
    def set_blue(self, __value: int) -> None:
        self._blue = __value
        if self._blue > 255:
            self._blue = 255
        elif self._blue < 0:
            self._blue = 0
        self._update_value()
        self._update_name()
    
    def increase_red(self):
        self._red+=1
        if self._red > 255:
            self._red = 255
        self._update_value()
        self._update_name()

    def decrease_red(self):
        self._red = self._red - 1
        if self._red < 0:
            self._red = 0
        self._update_value()
        self._update_name()
        
    def increase_blue(self):
        self._blue+=1
        if self._blue > 255:
            self._blue = 255
        self._update_value()
        self._update_name()
        
    def increase_green(self):
        self._green+=1
        if self._green > 255:
            self._green = 255
        self._update_value()
        self._update_name()
        
    def decrease_blue(self):
        self._blue = self._blue - 1
        if self._blue < 0:
            self._blue = 0
        self._update_value()
        self._update_name()
            
    def decrease_green(self):
        self._green = self._green - 1
        if self._green < 0:
            self._green = 0
        self._update_value()
        self._update_name()
        
    def get(self):
        return self.pixel
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, tuple):
            _value = __value
        elif isinstance(__value, RGBPixel):
            _value = __value.pixel
        elif isinstance(__value, list):
            _value = (__value[0], __value[1], __value[2])
        
        return _value == self.pixel
        
    def __ne__(self, __value: object) -> bool:
        if isinstance(__value, tuple):
            _value = __value
        elif isinstance(__value, RGBPixel):
            _value = __value.pixel
        elif isinstance(__value, list):
            _value = (__value[0], __value[1], __value[2])
        
        return _value != self.pixel

    
    
class PixelImage:
    def __init__(self, path: str) -> None:
        self.path = path
        self.xarray = read_image_to_2darray(self.path)
        self.invisible_color = self.xarray[0][0]
        self.max_width = determine_max_width(self.xarray)
        self.max_height = determine_max_height(self.xarray)
        self.startx = determine_startx(self.xarray)

        
    
    def analytics(self):
        print("path: ", self.path)
        print("invisible color: ", self.invisible_color)
        print("sprite-width: ", self.max_width)
        print("sprite-height: ", self.max_height)
        print("sprite-start-pixel-x:", self.startx)

def get_color_name(rgb):
    try:
        color_name = webcolors.rgb_to_name(rgb)
    except ValueError:
        color_name = "Unknown"
    return color_name
      

def read_image_to_2darray(path):
    
    # Open the image file
    image = Image.open(path)  # Replace "image.jpg" with the path to your image file

    # Convert the image to RGB mode (if needed)
    image = image.convert("RGB")

    # Get the size of the image
    width, height = image.size

    # Read the pixel data
    pixels = list(image.getdata())

    # Optionally, you can reshape the pixel data into a 2D array (width x height)
    pixels = [pixels[i:i+width] for i in range(0, len(pixels), width)]

    return pixels

def determine_startx(pixels) -> int:
    """
    scans each row of the image to find the leftmost non-transparent pixel in each row. 
    It keeps track of the starting x-coordinate of that pixel, 
    updating it if a pixel is found that is further left. 
    The function returns the final startx value, 
    representing the leftmost non-transparent column index encountered in the image.
    """
    startx = len(pixels[0])
    invisible_pixel = pixels[0][0]
    counter = 0
    for row in pixels:
        is_pixelated = False
        for px in row:
            
            if px != invisible_pixel:
               
                if counter < startx:
                   startx = counter
                
                counter = 0
                break
            elif px == invisible_pixel:
                counter+=1
    return startx
 
def width_between_sprites(pixels):
    invisible_pixel             = pixels[0][0]
    has_found_first_pixel       = False
    has_found_second_invisible  = False
    is_pixelated                = False
    counter                     = 0
    width_between               = 0
    
    for row in pixels:
        is_pixelated = False
        # determine if the row is pixelated
        for px in row:
            if px != invisible_pixel:
                is_pixelated = True
                break
        #if it is
        if is_pixelated == True:
            # for each px in the row
            for px in row:
                #increase the counter
                counter+=1
                #if the pixel is NOT invisible
                if px != invisible_pixel:
                    # set the has found the first pixel to true
                    has_found_first_pixel = True
                    # if it has found the second patch of empty pixels
                    if has_found_second_invisible == True:
                        # check the counter to see if its bigger than the width between
                        if counter > width_between:
                            width_between = counter
                            counter = 0
                            break
                # if the pixel is invisible
                elif px == invisible_pixel:
                    # if it has found the first patch of pixels that are not invisible
                    if has_found_first_pixel == True:
                        # then it has found the second patch of invisible pixels
                        has_found_second_invisible = True
                    # if it has not found the first patch of pixels reset the counter and continue
                    elif has_found_first_pixel != True:
                        counter = 0
                        continue
    return width_between

                     
def width_between_sprites_simplified(pixels: list[list[tuple]]):
    """ 
    scans the pixels row by row and counts the width between patches of non-transparent pixels. 
    It tracks whether it is currently inside a patch using the is_inside_patch flag. 
    The counter keeps track of the width between patches, 
    and the width_between variable stores the maximum width encountered. 
    The function returns the final width_between value.
    """
    invisible_pixel = pixels[0][0]
    width_between   = 0
    is_inside_patch = False
    counter         = 0

    for row in pixels:
        for px in row:
            if px == invisible_pixel:
                if is_inside_patch:
                    counter += 1
            else:
                if is_inside_patch:
                    if counter > width_between:
                        width_between = counter
                    counter = 0
                else:
                    is_inside_patch = True

    return width_between            
           

def determine_max_height(pixels):
    """
    Calculates the maximum height of a sequence of consecutive rows of non-transparent pixels in an image.

    Args:
        pixels (list): A 2D list representing an image, where each element represents a pixel.

    Returns:
        int: The maximum height of a sequence of consecutive non-transparent rows.

    The function iterates over the rows of the image and tracks consecutive rows without any non-transparent pixels.
    It keeps a count of the height of such sequences and updates the maximum height found.
    The function returns the maximum height encountered during the iteration.

    Note:
        - The `pixels` list should have at least one row and one column.
        - The transparency of pixels is determined by comparing them to the color of the pixel at (0, 0) in the `pixels` list.
    """
    invisible = pixels[0][0]
    counter = 0
    max_height = 0
    is_pixelated = False
    for row in pixels:
        is_pixelated = is_row_non_uniform(row)
            
        if is_pixelated == False:
            if counter > max_height:
                max_height = counter
            counter = 0
        elif is_pixelated == True:
            counter+=1
            
    return max_height

def is_row_uniform(row):
    """
    Determine if a row of pixels consists of the same color.

    Args:
        row (list): A list representing a row of pixels.

    Returns:
        bool: True if all pixels in the row have the same color, False otherwise.
    """
    if not row:
        return False

    first_pixel = row[0]
    for pixel in row[1:]:
        if pixel != first_pixel:
            return False

    return True

def is_row_non_uniform(row: list[tuple[int, int, int]]) -> bool:
    """
    Determine if a row of pixels is not uniform, meaning it contains more than one color.

    Args:
        row (list): A list representing a row of pixels.

    Returns:
        bool: True if the row contains more than one color, False otherwise.
    """
    if not row:
        return False

    first_pixel = row[0]
    for pixel in row[1:]:
        if pixel != first_pixel:
            return True

    return False

def determine_max_width(pixels):
    """ determine the max width of the sprites in a sheet """
    invisible = pixels[0][0]
    maxcount = 0
    for row in pixels:
        count = 0
        for px in row:
            if px == invisible:
                if count != 0:
                    if count > maxcount:
                        maxcount = count
                count = 0
            elif px != invisible:
                count+=1
    return maxcount
            
    
def get_subimage(path: str , x:int, y:int, width: int, height:int):
    box = (x, y, x+width, y+height)
    image = Image.open(path)
    # Convert the image to RGB mode (if needed)
    image = image.convert("RGB")
    # crop it 
    cropped_image = image.crop(box)
    # return it
    return cropped_image

def cut_image_into_subimages(image_path, height, width):
    # Load the image
    image = Image.open(image_path)

    # Get image dimensions
    width, height = image.size

    # Calculate the number of rows and columns
    num_rows = height // height
    num_cols = width // width

    sub_images = []
    
    # Iterate over rows and columns
    for row in range(num_rows):
        for col in range(num_cols):
            # Calculate starting and ending coordinates for the sub-image
            x_start = col * 16
            y_start = row * 16
            x_end = x_start + 16
            y_end = y_start + 16

            # Extract the sub-image
            sub_image = image.crop((x_start, y_start, x_end, y_end))

            # Perform operations on the sub-image if needed

            # Append the sub-image to the list
            sub_images.append(sub_image)

    return sub_images

def test():
    # Usage example
    sub_images = cut_image_into_subimages("loz-link-sprites.png")
    for i, sub_image in enumerate(sub_images):
        sub_image.save(f"sub_image_{i}.jpg")

import requests 
from io import BytesIO

def get_link_bits():
    linkrows = 1, 8

    blue_link = 10, 18
    red_link = 20, 28
    facing = ["right", "forward", "backwards", "forward mouth open", "forward head down", "forward head back", "" ]
    # Download the image
    image_url = "https://www.spriters-resource.com/resources/sheets/56/58952.png?updated=1511155974"
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # Define the size of the small parts
    part_width = 16
    part_height = 16

    # Crop the image into small parts
    num_rows = image.height // part_height
    num_cols = image.width // part_width
    parts = []
    print(num_cols)
    input()
    

    for row in range(num_rows):
        for col in range(num_cols):
            x_start = col * part_width
            y_start = row * part_height
            x_end = x_start + part_width
            y_end = y_start + part_height

            part = image.crop((x_start, y_start, x_end, y_end))
            parts.append(part)

    # Save or process the small parts as needed

    
    
    for i, part in enumerate(parts):
        part.save(f"part_{i}.png")
    
def rename_file(filename, new_name):
    os.rename(filename, new_name)


        

def get_file_paths():
    files = os.listdir()
    part_files = [x for x in files if x.startswith("part")]
    x = [os.path.join(os.getcwd(), x) for x in part_files]
    return x

def delete_blank_images():
    images = get_file_paths()
    for i in range(0,950):
        
        image = images[i]
        pixels = read_image_to_2darray(image)
        invisible = pixels[0][0]
        delete = True
        for row in pixels:
            
            for px in row:
               if px != invisible:
                    delete = False
            if delete == True:
                print("deleting image: ", image)
                try:
                    os.remove(image)
                except:
                    pass


def get_color_palete(file):
    color_palete = []
    pixels = read_image_to_2darray(file)
    invisible = pixels[0][0]
    for row in pixels:
        
        for px in row:
            if px != invisible:
                isin = pixel_in_palete(px, color_palete)
                if isin == False:
                    color_palete.append(px)
    return color_palete

def item_in(item: any, list: list) -> bool:
    for element in list:
        if item == element:
            return True
    return False

def count_item_in(item:any, list:list) -> int:
    count = 0
    for element in list:
        if element == item:
            count+=1
    return count

def uniform_items(list:list) -> bool:
    item = list.pop()
    for element in list:
        if item != element:
            return False
    return True

def index_not_item_in(item, list: list):
    locations = []
    counter = 0
    for element in list:
        if item != element:
            locations.append(counter)
        counter+=1    
    return locations
        

def index_item_in(item: any, list:list) -> list[int]:
    locations = []
    for index, element in enumerate(list):
        if element == item:
            locations.append(index)
    return locations


def index_pixels_that_are_not(row, pixel):
    indices = []
    for index, px in enumerate(row):
        if pixel != px:
            indices.append(index)
    return indices

def pixel_in_palete(pixel, palete):
    for pix in palete:
        if pix == pixel:
            return True
    return False


class ImageViewer(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        
        self.arrow_up_photo, self.arrow_up_width, self.arrow_up_height = make_photo("arrowup.png")
        self.arrow_left_photo, self.arrow_left_width, self.arrow_left_height = make_photo("arrowleft.png")
        self.arrow_right_photo, self.arrow_right_width, self.arrow_right_height = make_photo("arrowright.png")
        self.arrow_down_photo, self.arrow_down_width, self.arrow_down_height = make_photo("arrowdown.png")
        self.load_image_photo, self.load_image_width, self.load_image_height = make_photo("uploadimage.png") 
        
        self.subimage_zoom_factor = 4
        self.rectx = 0; self.recty = 0; self.rectw = 16; self.recth = 16
        self.pixel_count = 0
        self.row_count = 0
        self.column_count = 0
        self.image = None
        self.image_path = None 
        self.matrix = None
        self.image_width = None
        self.image_height = None
        self.image_center_width = None
        self.image_center_height = None
        self.subimage_matrixes = []
        self.subimage = None
        self.subimage_path = None 
        self.subimage_matrix = None
        self.subimage_width = None
        self.subimage_height = None
        self.subimage_center_width = None
        self.subimage_center_height = None
        self.current_color = "red"
        

        self.main_frame = customtkinter.CTkFrame(self, width=1200, height=1000)
        self.main_frame.grid(column=0, row=0, sticky='nsew')
        
        self.left_frame = customtkinter.CTkFrame(self.main_frame)
        self.left_frame.grid(column=0, row=0, sticky='nw')
        
        self.right_frame = customtkinter.CTkFrame(self.main_frame)
        self.right_frame.grid(column=1, row=0, sticky='ne')
        
        self.subframe_bottom = customtkinter.CTkFrame(self.left_frame, border_width=4)
        self.subframe_bottom.grid(column=0, row=1, sticky='sw')
        
        self.subframe_right = customtkinter.CTkFrame(self.right_frame)
        self.subframe_right.grid(column=0, row=0, sticky='nw')
        
        self.subframe_right_top = customtkinter.CTkFrame(self.subframe_right)
        self.subframe_right_top.grid(row=0, column=0, sticky='nw')
        
        self.subframe_right_bottom = customtkinter.CTkFrame(self.subframe_right)
        self.subframe_right_bottom.grid(row=1, column=0, sticky='sw')
        
        self.image_canvas = customtkinter.CTkCanvas(self.subframe_bottom, width=400, height=400, borderwidth=0, background="black" )
        self.image_canvas.grid(column=0, row=0, padx=(2, 2), pady=(2,2))
        
        self.subimage_canvas = customtkinter.CTkCanvas(self.subframe_right_top, width=60, height=60)
        self.subimage_canvas.grid(row=6, column=0, padx=(2, 2), pady=(2,2))
        
        
        self.load_image_button = customtkinter.CTkButton(self.subframe_right_top, image=self.load_image_photo, text="Load Image", command=self.get_image).grid(
            column=0, row=5, padx=(2, 2), pady=(2,2))
        
        self.move_left_button = customtkinter.CTkButton( self.subframe_right_bottom, width=self.arrow_left_width, text= "", image=self.arrow_left_photo, command=self.move_box_left).grid(
            column=0, row=1, padx=(2, 2), pady=(2,2))
        self.move_right_button = customtkinter.CTkButton(self.subframe_right_bottom, width=self.arrow_right_width, text= "", image=self.arrow_right_photo, command=self.move_box_right).grid(
            column=2, row=1, padx=(2, 2), pady=(2,2))
        self.move_up_button = customtkinter.CTkButton(   self.subframe_right_bottom, width=self.arrow_up_width, text= "", image=self.arrow_up_photo, command=self.move_box_up).grid(
            column=1, row=0, padx=(2, 2), pady=(2,2))
        self.move_down_button = customtkinter.CTkButton( self.subframe_right_bottom, width=self.arrow_down_width, text= "", image=self.arrow_down_photo, command=self.move_box_down).grid(
            column=1, row=2, padx=(2, 2), pady=(2,2))
        

        self.increase_box_width_button = customtkinter.CTkButton( self.subframe_right_bottom, text= "increase box width", command=self.increase_box_width).grid(
            column=3, row=1, padx=(2, 2), pady=(2,2))
        self.increase_box_height_button = customtkinter.CTkButton( self.subframe_right_bottom, text= "increase box height", command=self.increase_box_height).grid(
            column=4, row=1, padx=(2, 2), pady=(2,2))
        
        self.save_crop_button = customtkinter.CTkButton(self.subframe_right_bottom, text= "Save Crop", command=self.save_crop).grid(
            column=0, row=3, padx=(2, 2), pady=(2,2))
        
        
        self.save_image_name_label = customtkinter.CTkLabel(self.subframe_right_bottom, text="Image Name: ").grid(
            column=1, row=3, padx=(2, 2), pady=(2,2))
        
        self.save_image_name = customtkinter.CTkEntry(self.subframe_right_bottom, placeholder_text="cropped_image").grid(
            column=2, row=3, padx=(2, 2), pady=(2,2))
        
        self.save_image_extension_combo = customtkinter.CTkComboBox(self.subframe_right_bottom, values=["PNG", "GIF", "JPG"], command=self.set_save_extension).grid(
            column = 3, row=3)
        
        
        
        self.mainloop()
    
    def set_save_extension(self, *args):
        self.save_image_extension = self.save_image_extension_combo.get()
        self.save_image_extension_lower = "." + self.save_image_extension.lower()
        
    def save_crop(self):
        self.subimage = Image.open(self.main_image_path)
        self.cropped_image = self.subimage.crop((self.rectx, self.recty, self.rectx + self.rectw, self.recty + self.recth))
        self.set_save_extension()
        self.save_image_extension_filename = self.save_image_name_label.cget() + self.save_image_extension_lower
        self.cropped_image.save(fp=self.save_image_extension_filename, format=self.save_image_extension)
    
    def increase_box_width(self):
        self.rectw +=1
        self.refresh_image()
    
    def increase_box_height(self):
        self.recth +=1
        self.refresh_image()
        
    def move_box_down(self):
        self.recty+=self.recth 
        if self.recty > self.image_height:
            self.recty = 0
        self.refresh_image()
        
    def move_box_up(self):
        self.recty = self.recty - self.recth 
        if self.recty < 0:
            self.recty = self.image_height
        self.refresh_image()
    
    def move_box_left(self):
        self.rectx = self.rectx - self.rectw
        if self.rectx < 0:
            self.rectx = self.image_width - self.rectw
            self.recty+=self.recth
        if self.recty == self.image_height:
            self.recty = self.image_height + self.recth
        self.refresh_image()
    
    def move_box_right(self):
        self.rectx+=self.rectw
        if self.rectx == self.image_width:
            self.rectx = 0
            self.recty+=self.recth
        if self.recty == self.image_height:
            self.recty = 0
        self.refresh_image()
        
    def get_image(self):
        image_file = customtkinter.filedialog.askopenfilename()
        if image_file is not None:
            self.set_image(image_file)
    
    def set_image(self, image_path):
        self.main_image_path = image_path
        self.image, self.matrix, self.image_width, self.image_height, self.image_center_width, self.image_center_height = image_to_photo(image_path)
        
        self.reset_box_location()
        self.refresh_image()
    
    def reset_box_location(self):
        self.rectx = 0
        self.recty = 0
    
    def calculate_subimage_width_height(self):
        self.subimage_canvas_width = self.rectw/2 if self.rectw%2==0 else self.rectw//2
        self.subimage_canvas_height = self.recth/2 if self.recth%2==0 else self.recth//2
    
    def refresh_image(self):
        self.image_canvas.create_image(self.image_center_width, self.image_center_height, image=self.image)
        self.image_canvas.configure(height=self.image_height, width=self.image_width)
        self.calculate_subimage_width_height()
        self.draw_subimage()
        self.draw_rectange()
    
    def draw_subimage(self):
        self.subimage = Image.open(self.main_image_path)
        self.cropped_image = self.subimage.crop((self.rectx, self.recty, self.rectx + self.rectw, self.recty + self.recth))
        self.cropped_image = self.cropped_image.convert("RGB")
        self.cropped_image= self.cropped_image.resize((self.rectw*self.subimage_zoom_factor, self.recth*self.subimage_zoom_factor))
        self.sub_photoimage = ImageTk.PhotoImage(self.cropped_image, size=(self.rectw, self.recth))
        self.subimage_canvas.create_image(self.subimage_canvas_width*self.subimage_zoom_factor, self.subimage_canvas_height*self.subimage_zoom_factor, image=self.sub_photoimage)
        self.subimage_canvas.configure(height=self.recth*self.subimage_zoom_factor, width=self.rectw*self.subimage_zoom_factor)
        
    def draw_rectange(self, *args):
        self.current_color = "red" if self.current_color == 'white' else "white"
        rect = self.image_canvas.create_rectangle(self.rectx,  self.recty, self.rectx+self.rectw, self.recty+self.recth,  outline=self.current_color)
        self.image_canvas.after(1400, self.draw_rectange)
        
        
def crop_image(image_path, x, y, width, height):
    image = Image.open(image_path)
    cropped_image = image.crop((x, y, x + width, y + height))
    return cropped_image

def create_subimage_from_image(image, x, y, w, h):
    cropped_image = crop_image(image, x, y, w, h)
    cropped_image = cropped_image.convert("RGB")
    photoimage = ImageTk.PhotoImage(cropped_image)
    return photoimage

def make_photo(image_path):
    img = Image.open(image_path)
    width, height = img.size
    img.convert("RGB")
    im = ImageTk.PhotoImage(img, size=(width, height))
    img.close()
    return im, width, height
     
def image_to_photo(image_path):
    img = Image.open(image_path)
    width, height = img.size
    print(height)
    print(width)
    img.convert("RGB")
    im = ImageTk.PhotoImage(img, size=(width, height))
    rimgdata = img.getdata()
    img.close()
    return im, rimgdata, width, height, width//2, height//2

if __name__ == '__main__':
    ImageViewer()
    