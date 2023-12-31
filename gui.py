from typing import Literal, Optional, Tuple, Union
import threading 
import customtkinter as ctk
from PIL import Image
from customtkinter.windows.widgets.font import CTkFont
import webcolors
from PIL import ImageTk, Image
import json
import sys

OSX = sys.platform



class CoordinateFrame(ctk.CTkFrame):
    
    def __init__(self, master, x , y, w, h, image_path):
        super().__init__(master, width=600, border_width=1)
        self.master = master
        self.image_path = image_path
        self.x = x 
        self.y = y
        self.w = w 
        self.h = h
        self.x2 = self.x+self.w
        self.y2 = self.y+self.h
        self.xlabel  = ctk.CTkLabel(self, text="x: "+str(self.x))
        self.xlabel.grid(column=0, row=0, padx=(5,2), pady=(2,0), ipadx=0, ipady=0)
        self.ylabel  = ctk.CTkLabel(self, text="y: "+str(self.y))
        self.ylabel.grid(column=1, row=0, padx=(20,2), pady=(2,0), ipadx=0, ipady=0)
        self.wlabel  = ctk.CTkLabel(self, text="width: "+str(self.w))
        self.wlabel.grid(column=2, row=0, padx=(20,2), pady=(2,0))
        self.hlabel  = ctk.CTkLabel(self, text="height: "+str(self.h))
        self.hlabel.grid(column=0, row=1, padx=(5,2), pady=(0,0))
        self.x2label = ctk.CTkLabel(self, text="x2: "+str(self.x2))
        self.x2label.grid(column=1, row=1, padx=(20,2), pady=(0,0))
        self.y2label = ctk.CTkLabel(self, text="y2: "+ str(self.y2))
        self.y2label.grid(column=2, row=1, padx=(20,2), pady=(0,0))
        self.subimage = Image.open(self.image_path)
        self.cropped_image = self.subimage.crop((self.x, self.y, self.x + self.w, self.y + self.h))
        self.cropped_image = self.cropped_image.convert("RGB")
        self.cropped_image= self.cropped_image.resize((self.w, self.h))
        self.sub_photoimage = ImageTk.PhotoImage(self.cropped_image, size=(self.w, self.h))
        self.photoimage = ctk.CTkCanvas(self, width=w, height=h)
        self.photoimage.grid(column=3, row=0, pady=2, padx=2)
        self.photoimage.create_image(w//2, h//2, image=self.sub_photoimage)
        self.remove_button = ctk.CTkButton(self, image=make_photo("minus.png")[0], text="", width=30, height=30)
        self.remove_button.grid(column=4, row=0, rowspan=3, pady=(2,2), padx=(40,2))
        self.remove_button.bind("Button-1", self.remove_me)
    
    def remove_me(self, *args):
        self.destroy()
        self.master.yindex -1
    
    def get_coordinates(self) -> None:
        return {"x":self.x, "y":self.y, "w":self.w, "h":self.h, "x2":self.x2, "y2":self.y2} 



class CoordinatesFrame(ctk.CTkFrame):
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, scrollbar_fg_color: str | Tuple[str, str] | None = None, scrollbar_button_color: str | Tuple[str, str] | None = None, scrollbar_button_hover_color: str | Tuple[str, str] | None = None, label_fg_color: str | Tuple[str, str] | None = None, label_text_color: str | Tuple[str, str] | None = None, label_text: str = "", label_font: tuple | CTkFont | None = None, label_anchor: str = "center", orientation: Literal['vertical', 'horizontal'] = "vertical"):
        super().__init__(master, border_width=4, height=600, width=700)
        self.coordinate_frame = ctk.CTkScrollableFrame(self, border_width=2, width=400)
        self.coordinate_frame.grid(column=0, row=0, columnspan=3, padx=(5,5), pady=(5,5), sticky='nsew')
        self.button_frame = ctk.CTkFrame(self, width=700, height=200)
        self.button_frame.grid(column=0, row=1, sticky='nsew')
        self.save_button = ctk.CTkButton(self.button_frame, text="save to json", command=self.save_coords, width=400, state="disabled")
        self.save_button.grid(column=0, row=0, columnspan=3, sticky='nsew')
        self.yindex = 0
        self.xindex = 0
        self.coords = []
        self.save_disabled = True
        
    def add_coordinate(self, x, y ,w, h, image_path):
        if self.save_disabled == True:
            self.save_button.configure(state="normal")
            self.save_disabled = False
        self.new_frame: CoordinateFrame = CoordinateFrame(self.coordinate_frame, x, y, w, h, image_path)
        self.new_frame.grid(column=self.xindex, row=self.yindex, sticky='wens', padx=(3,3), pady=(2,2), columnspan=3)
        self.yindex+=1
        self.coords.append(self.new_frame)
    
    def get_coordinates(self) -> None:
        retv = []
        for coord in self.coords:
            retv.append(coord.get_coordinates())
        return retv
    
    def save_coords(self) -> None:
        coords = self.get_coordinates()
        with open("coordinates.json", "w") as jfile:
            json.dump(coords, jfile)
    
    
class ImageViewer(ctk.CTk):
    mac_fonts = [
    "Arial",
    "Helvetica",
    "Verdana",
    "Times New Roman",
    "Courier New",
    "Georgia",
    "Trebuchet MS",
    "Lucida Grande",
    "Palatino",
    "Comic Sans MS",
    ]

    # Common fonts on Windows
    windows_fonts = [
        "Arial",
        "Helvetica",
        "Verdana",
        "Times New Roman",
        "Courier New",
        "Georgia",
        "Trebuchet MS",
        "Lucida Sans",
        "Palatino Linotype",
        "Comic Sans MS",
    ]

    # Common fonts on Linux
    linux_fonts = [
        "Arial",
        "Helvetica",
        "DejaVu Sans",
        "Liberation Sans",
        "Noto Sans",
        "FreeSans",
        "Ubuntu",
        "Roboto",
        "Droid Sans",
        "Cantarell",
    ]
    def __init__(self) -> None:
        super().__init__()
        
        # IMAGES
        self.arrow_up_photo, self.arrow_up_width, self.arrow_up_height = make_photo("arrowup.png")
        self.arrow_left_photo, self.arrow_left_width, self.arrow_left_height = make_photo("arrowleft.png")
        self.arrow_right_photo, self.arrow_right_width, self.arrow_right_height = make_photo("arrowright.png")
        self.arrow_down_photo, self.arrow_down_width, self.arrow_down_height = make_photo("arrowdown.png")
        self.load_image_photo, self.load_image_width, self.load_image_height = make_photo("uploadimage.png") 
        self.plus_photo, self.plus_width, self.plus_height = make_photo("plus.png")
        self.minus_photo, self.minus_width, self.minus_height = make_photo("minus.png") 
        self.save_photo, self.save_width, self.save_height = make_photo("save.png") 
        # VARIABLES
        self.usable_fonts = self._get_usable_fonts()
        self.basic_font = ctk.CTkFont(family=self.usable_fonts[2], size=16)
        self.italic_font = ctk.CTkFont(family=self.usable_fonts[2], size=16, slant="italic")
        self.bold_font = ctk.CTkFont(family=self.usable_fonts[2], size=16, weight="bold")
        self.image_uploaded = False
        self.buttons_enabled = False
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
        self.colors = ["blue", "red", "green", "yellow", "cyan", "white", "magenta"]
        self.color_max = len(self.colors) - 1
        self.color_index = 0
        self.boxes = []
        # VIEW
        self.tab_view = ctk.CTkTabview(master=self)
        self.tab_view.grid(column=0, row=0, sticky="nsew")
        self.tab_view.add("Cropper")
        self.tab_view.add("Settings")
        # CROPPER FRAMES
        self.main_frame = ctk.CTkFrame(self.tab_view.tab("Cropper"), width=1200, height=1000)
        self.main_frame.grid(column=0, row=0, sticky='nsew')
        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.grid(column=0, row=0, sticky='nw')
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.grid(column=1, row=0, sticky='ne')
        self.subframe_bottom = ctk.CTkFrame(self.left_frame, border_width=4)
        self.subframe_bottom.grid(column=0, row=1, sticky='nesw', padx=5, pady=5)
        self.subframe_right = ctk.CTkFrame(self.right_frame)
        self.subframe_right.grid(column=0, row=0, sticky='nwse', padx=5, pady=5)
        self.subframe_right_top = ctk.CTkFrame(self.subframe_right, border_width=4)
        self.subframe_right_top.grid(row=0, column=0, sticky='nwse', padx=2, pady=2)
        self.subframe_right_bottom = ctk.CTkFrame(self.subframe_right, width=700, height=400, border_width=4)
        self.subframe_right_bottom.grid(row=1, column=0, sticky='swne', padx=2, pady=2)
        # CROPPER WIDGETS
        self.image_canvas                   = ctk.CTkCanvas(    self.subframe_bottom,    width=400, height=400, borderwidth=0, background="black")
        self.subimage_canvas                = ctk.CTkCanvas(    self.subframe_right_top, width=60,  height=60,  borderwidth=0,)
        self.load_image_button              = ctk.CTkButton(    self.subframe_right_top,image=self.load_image_photo, text="Load Image", command=self.get_image, border_width=10, font=self.basic_font)
        self.coordinates_frame              = CoordinatesFrame( self.subframe_right_top)
        self.move_left_button               = ctk.CTkButton(    self.subframe_right_bottom, width=self.arrow_left_width, text= "", image=self.arrow_left_photo, command=self.move_box_left, font=self.basic_font)
        self.add_coordinate_button          = ctk.CTkButton(    self.subframe_right_bottom, text="save coordinate", command=self.mark_coordinate, font=self.basic_font)
        self.move_right_button              = ctk.CTkButton(    self.subframe_right_bottom, width=self.arrow_right_width, text= "", image=self.arrow_right_photo, command=self.move_box_right, font=self.basic_font)
        self.move_up_button                 = ctk.CTkButton(    self.subframe_right_bottom, width=self.arrow_up_width, text= "", image=self.arrow_up_photo, command=self.move_box_up, font=self.basic_font)
        self.move_down_button               = ctk.CTkButton(    self.subframe_right_bottom, width=self.arrow_down_width, text= "", image=self.arrow_down_photo, command=self.move_box_down, font=self.basic_font)
        self.increase_box_width_button      = ctk.CTkButton(    self.subframe_right_bottom, image=self.plus_photo,  text="box width", command=self.increase_box_width, font=self.basic_font)
        self.decrease_box_width_button      = ctk.CTkButton(    self.subframe_right_bottom, image=self.minus_photo, text="box width", command=self.increase_box_width, font=self.basic_font)
        self.increase_box_height_button     = ctk.CTkButton(    self.subframe_right_bottom, image=self.plus_photo,  text="box height", command=self.increase_box_height, font=self.basic_font)
        self.decrease_box_height_button     = ctk.CTkButton(    self.subframe_right_bottom, image=self.minus_photo, text="box height", command=self.increase_box_height, font=self.basic_font)
        self.save_crop_button               = ctk.CTkButton(    self.subframe_right_bottom, image=self.save_photo,  text="Save Crop", command=self.save_crop, font=self.basic_font)
        self.save_image_name_label          = ctk.CTkLabel(     self.subframe_right_bottom, text="Image Name: ", font=self.basic_font)
        self.save_image_name                = ctk.CTkEntry(     self.subframe_right_bottom, placeholder_text="cropped_image", font=self.basic_font)
        self.save_image_extension_combo     = ctk.CTkComboBox(  self.subframe_right_bottom, values=["PNG", "GIF", "JPG"],  font=self.basic_font)
        
        self.image_canvas.grid(                 column=0, row=0, padx=(2, 2), pady=(2,2))
        self.subimage_canvas.grid(              row=4, column=2, padx=(20, 2), pady=(10,10), sticky='w')
        self.load_image_button.grid(            column=2, row=0, padx=(20, 20), pady=(5,5))
        self.coordinates_frame.grid(            column=5, row=0, padx=(120, 0), sticky='e')
        self.move_left_button.grid(             column=0, row=1, padx=(2, 2), pady=(2, 2), sticky='e')
        self.add_coordinate_button.grid(        column=1, row=1, pady=(0, 0), padx=(0, 0), sticky='nwse')
        self.move_right_button.grid(            column=2, row=1, padx=(2, 2), pady=(2, 2), sticky='w')
        self.move_up_button.grid(               column=1, row=0, padx=(2, 2), pady=(2, 2), sticky='s')
        self.move_down_button.grid(             column=1, row=2, padx=(2, 2), pady=(2, 2), sticky='n')
        self.increase_box_width_button.grid(    column=3, row=1, padx=(2, 2), pady=(2, 2))
        self.decrease_box_width_button.grid(    column=3, row=2, padx=(2, 2), pady=(2, 2))
        self.increase_box_height_button.grid(   column=4, row=1, padx=(2, 2), pady=(2, 2))
        self.decrease_box_height_button.grid(   column=4, row=2, padx=(2, 2), pady=(2, 2))
        self.save_crop_button.grid(             column=0, row=3, padx=(2, 2), pady=(2, 2))
        self.save_image_name_label.grid(        column=1, row=3, padx=(2, 2), pady=(2, 2))
        self.save_image_name.grid(              column=2, row=3, padx=(2, 2), pady=(2, 2))
        self.save_image_extension_combo.grid(   column=3, row=3)
        
        self.save_image_name.insert(0, "cropped_image")
        
        self.save_image_extension_combo.bind("<Button-1>", lambda cbo: self.set_save_extension())
        self.save_image_extension_combo.set("PNG")
        
        self.disable_until_image_loaded()
        self.mainloop()
    
    def _get_usable_fonts(self) -> None:
        if sys.platform.startswith("w"):
            return self.windows_fonts
        elif sys.platform.startswith('l'):
            return self.linux_fonts
        elif sys.platform.startswith('d'):
            return self.mac_fonts
    
    def disable_until_image_loaded(self) -> None:
        """ Disables the buttons that would cause harm if pressed before image uploaded
        """
        self.move_left_button.configure(state="disabled")
        self.add_coordinate_button.configure(state="disabled")
        self.move_right_button.configure(state="disabled")
        self.move_up_button.configure(state="disabled")
        self.move_down_button.configure(state="disabled")
        self.save_crop_button.configure(state="disabled")
        self.increase_box_width_button.configure(state="disabled")
        self.decrease_box_width_button.configure(state="disabled")
        self.increase_box_height_button.configure(state="disabled")
        self.decrease_box_height_button.configure(state="disabled")
        
    def enabled_after_image_loaded(self) -> None:
        """ Enables the buttons that would cause harm if pressed before an image is uploaded
        """
        self.move_left_button.configure(state="normal")
        self.add_coordinate_button.configure(state="normal")
        self.move_right_button.configure(state="normal")
        self.move_up_button.configure(state="normal")
        self.move_down_button.configure(state="normal")
        self.increase_box_width_button.configure(state="normal")
        self.increase_box_height_button.configure(state="normal")
        self.save_crop_button.configure(state="normal")
        self.increase_box_width_button.configure(state ="normal")
        self.decrease_box_width_button.configure(state ="normal")
        self.increase_box_height_button.configure(state="normal")
        self.decrease_box_height_button.configure(state="normal")
        self.load_image_button.configure(border_width=0)
    
    def mark_coordinate(self) -> None:
        if self.main_image_path != None:
            box = (self.rectx, self.recty, self.rectw, self.recth)
            self.boxes.append(box)
            self.coordinates_frame.add_coordinate(self.rectx, self.recty, self.rectw, self.recth, self.main_image_path)
    
    def set_save_extension(self, *args) -> None:
        self.save_image_extension = self.save_image_extension_combo.get()
        self.save_image_extension_lower = "." + self.save_image_extension.lower()
        
    def save_crop(self) -> None:
        self.subimage = Image.open(self.main_image_path)
        self.cropped_image = self.subimage.crop((self.rectx, self.recty, self.rectx + self.rectw, self.recty + self.recth))
        self.set_save_extension()
        self.save_image_extension_filename = self.save_image_name.get() + self.save_image_extension_lower
        self.cropped_image.save(fp=self.save_image_extension_filename, format=self.save_image_extension)
    
    def increase_box_width(self) -> None:
        self.rectw +=1
        self.refresh_image()
    
    def increase_box_height(self) -> None:
        self.recth +=1
        self.refresh_image()
        
    def move_box_down(self) -> None:
        self.recty+=self.recth 
        if self.recty > self.image_height:
            self.recty = 0
        self.refresh_image()
        
    def move_box_up(self) -> None:
        self.recty = self.recty - self.recth 
        if self.recty < 0:
            self.recty = self.image_height
        self.refresh_image()
    
    def move_box_left(self) -> None:
        self.rectx = self.rectx - self.rectw
        if self.rectx < 0:
            self.rectx = self.image_width - self.rectw
            self.recty+=self.recth
        if self.recty == self.image_height:
            self.recty = self.image_height + self.recth
        self.refresh_image()
    
    def move_box_right(self) -> None:
        self.rectx+=self.rectw
        if self.rectx == self.image_width:
            self.rectx = 0
            self.recty+=self.recth
        if self.recty == self.image_height:
            self.recty = 0
        self.refresh_image()
        
    def get_image(self) -> None:
        image_file = ctk.filedialog.askopenfilename()
        if image_file is not None:
            self.image_uploaded = True
            self.set_image(image_file)
        if self.buttons_enabled == False:
            if self.image_uploaded == True:
                self.enabled_after_image_loaded()
                self.buttons_enabled = True
    
    def set_image(self, image_path):
        self.main_image_path = image_path
        self.image, self.matrix, self.image_width, self.image_height, self.image_center_width, self.image_center_height = image_to_photo(image_path)
        self.reset_box_location()
        self.refresh_image()
    
    def reset_box_location(self) -> None:
        self.rectx = 0
        self.recty = 0
    
    def calculate_subimage_width_height(self) -> None:
        self.subimage_canvas_width = self.rectw/2 if self.rectw%2==0 else self.rectw//2
        self.subimage_canvas_height = self.recth/2 if self.recth%2==0 else self.recth//2
    
    def refresh_image(self) -> None:
        self.image_canvas.create_image(self.image_center_width, self.image_center_height, image=self.image)
        self.image_canvas.configure(height=self.image_height, width=self.image_width)
        self.calculate_subimage_width_height()
        self.draw_subimage()
        self.draw_all_rectangles()
    
    def draw_subimage(self) -> None:
        self.subimage = Image.open(self.main_image_path)
        self.cropped_image = self.subimage.crop((self.rectx, self.recty, self.rectx + self.rectw, self.recty + self.recth))
        self.cropped_image = self.cropped_image.convert("RGB")
        self.cropped_image= self.cropped_image.resize((self.rectw*self.subimage_zoom_factor, self.recth*self.subimage_zoom_factor))
        self.sub_photoimage = ImageTk.PhotoImage(self.cropped_image, size=(self.rectw, self.recth))
        self.subimage_canvas.create_image(self.subimage_canvas_width*self.subimage_zoom_factor, self.subimage_canvas_height*self.subimage_zoom_factor, image=self.sub_photoimage)
        self.subimage_canvas.configure(height=self.recth*self.subimage_zoom_factor, width=self.rectw*self.subimage_zoom_factor)
    
    def draw_all_rectangles(self):
        self.draw_rectangle()
        self.draw_saved_coordinates()
    
    def draw_rectangle(self, *args) -> None:
        self.get_next_color()
        self.image_canvas.create_rectangle(self.rectx,  self.recty, self.rectx+self.rectw, self.recty+self.recth,  outline=self.current_color)
        self.image_canvas.create_rectangle(self.rectx-1,  self.recty+1, self.rectx+self.rectw+1, self.recty+self.recth+1,  outline=self.second_color)
        #self.image_canvas.create_line(self.rectx,  self.recty, 0, 0)
        #self.image_canvas.create_line(self.rectx+self.rectw, self.recty+self.recth, self.image_width, self.image_width)
        self.image_canvas.after(2000, self.draw_rectangle)
        
    
    def draw_saved_coordinates(self):
        for box in self.boxes:
            rect = self.image_canvas.create_rectangle(box[0],  box[1], box[0]+box[2], box[1]+box[3],  outline="blue")
        
    def get_next_color(self):
        self.second_color= self.colors[self.color_index]
        self.color_index+=1
        if self.color_index > self.color_max:
            self.color_index = 0
        self.current_color = self.colors[self.color_index]
        
    
        
def crop_image(image_path, x, y, width, height):
    image = Image.open(image_path)
    cropped_image = image.crop((x, y, x + width, y + height))
    return cropped_image

def create_subimage_from_image(image, x, y, w, h):
    cropped_image = crop_image(image, x, y, w, h)
    cropped_image = cropped_image.convert("RGB")
    photoimage = ImageTk.PhotoImage(cropped_image)
    return photoimage

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

def make_photo(image_path):
    img = Image.open(image_path)
    width, height = img.size
    img.convert("RGB")
    im = ImageTk.PhotoImage(img, size=(width, height))
    img.close()
    return im, width, height



if __name__ == '__main__':
    ImageViewer()
    