import os
import streamlit as st
from PIL import Image

class ImageCropper:
    def __init__(self):
        self.image_folder = '/home/imran/Downloads/Output/chandana_'  
        self.save_folder = '/home/imran/Downloads/Output/chandana/'  
        self.image_paths = []
        self.skipped_images = []  
        self.current_image = None
        self.image_index = 0
        self.crop_rectangle = None
        self.total_cropped = 0
        self.total_skipped = 0  

    def load_images(self):
        all_images = [
            os.path.join(self.image_folder, f) 
            for f in os.listdir(self.image_folder) 
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
        ]

        cropped_images = [
            os.path.splitext(f)[0] for f in os.listdir(self.save_folder) 
            if f.lower().endswith('.webp')
        ]

        self.image_paths = [img for img in all_images if os.path.basename(img).split('.')[0] not in cropped_images]

    def show_image(self):
        if self.image_index < len(self.image_paths):
            original_filename = os.path.basename(self.image_paths[self.image_index])
            self.current_image = Image.open(self.image_paths[self.image_index])
            st.image(self.current_image, caption=original_filename)

    def crop_image(self):
        x1, y1, x2, y2 = self.crop_rectangle
        self.cropped_image = self.current_image.crop((x1, y1, x2, y2))
        original_filename = os.path.basename(self.image_paths[self.image_index])
        save_path = os.path.join(self.save_folder, f"{os.path.splitext(original_filename)[0]}.webp")
        self.cropped_image.save(save_path, format='WEBP', quality=90)
        self.total_cropped += 1

    def next_image(self):
        if self.image_index < len(self.image_paths) - 1:
            self.image_index += 1
        else:
            st.info("You are at the last image.")

    def run(self):
        st.title("Image Cropper")
        self.load_images()

        if st.button("Load Images"):
            self.show_image()

        if st.button("Next Image"):
            self.next_image()
            self.show_image()

        # Add your cropping rectangle logic here. Streamlit does not directly support
        # mouse event binding like Tkinter, so you might need to adjust this part.

if __name__ == "__main__":
    app = ImageCropper()
    app.run()
