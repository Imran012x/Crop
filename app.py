import os
from tkinter import Tk, Canvas, Button, Frame, messagebox, Label, Entry, Toplevel
from PIL import Image, ImageTk

class ImageCropper:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Cropper")

        self.frame = Frame(self.master)
        self.frame.pack()

        self.canvas = Canvas(self.frame, width=800, height=600, bg='gray')
        self.canvas.pack(side="left")

        self.menu_frame = Frame(self.frame)
        self.menu_frame.pack(side="right", padx=10)

        self.load_button = Button(self.menu_frame, text="Load Images", command=self.load_images)
        self.load_button.pack(pady=5)

        self.previous_button = Button(self.menu_frame, text="Previous Image", command=self.previous_image)
        self.previous_button.pack(pady=5)

        self.next_button = Button(self.menu_frame, text="Next Image", command=self.next_image)
        self.next_button.pack(pady=5)

        self.load_skipped_button = Button(self.menu_frame, text="Load Skipped Images", command=self.load_skipped_images)
        self.load_skipped_button.pack(pady=5)

        self.image_name_entry = Entry(self.menu_frame)
        self.image_name_entry.pack(pady=5)
        self.load_by_name_button = Button(self.menu_frame, text="Load by Name", command=self.load_by_name)
        self.load_by_name_button.pack(pady=5)

        self.image_info_label = Label(self.menu_frame, text="", justify='left')
        self.image_info_label.pack(pady=5)

        self.cropped_info_label = Label(self.menu_frame, text="", justify='left')
        self.cropped_info_label.pack(pady=5)

        self.remaining_info_label = Label(self.menu_frame, text="", justify='left')
        self.remaining_info_label.pack(pady=5)

        self.image_folder = '/home/imran/Downloads/Output/chandana_'  
        self.save_folder = '/home/imran/Downloads/Output/chandana/'  

        self.image_paths = []
        self.skipped_images = []  # Store skipped images for later loading
        self.current_image = None
        self.tk_image = None
        self.image_index = 0
        self.crop_rectangle = None
        self.original_size = None  
        self.total_cropped = 0
        self.total_skipped = 0  # Counter for skipped images
        self.total_images = 0  # Total images for remaining count

    def load_images(self):
        all_images = [
            os.path.join(self.image_folder, f) 
            for f in os.listdir(self.image_folder) 
            if f.lower().endswith(('.png', '.jpg', '.jpeg','.webp'))
        ]

        cropped_images = [
            os.path.splitext(f)[0] for f in os.listdir(self.save_folder) 
            if f.lower().endswith('.webp')
        ]

        # Load only images that haven't been cropped yet
        self.image_paths = [img for img in all_images if os.path.basename(img).split('.')[0] not in cropped_images]

        self.total_images = len(all_images)  # Count total images in the folder
        if self.image_paths:
            self.image_index = 0
            self.total_cropped = len(cropped_images)  # Total already cropped images
            self.total_skipped = 0  # Reset skipped counter on loading new images
            self.show_image()
            self.update_cropped_info()
        else:
            messagebox.showerror("Error", "All images have already been cropped.")

    def show_image(self):
        if self.image_index < len(self.image_paths):
            original_filename = os.path.basename(self.image_paths[self.image_index])
            self.current_image = Image.open(self.image_paths[self.image_index])
            self.original_size = self.current_image.size

            self.current_image.thumbnail((800, 600))
            self.tk_image = ImageTk.PhotoImage(self.current_image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)
            self.canvas.bind("<ButtonPress-1>", self.start_crop)
            self.canvas.bind("<B1-Motion>", self.update_crop)
            self.canvas.bind("<ButtonRelease-1>", self.end_crop)

            self.image_info_label.config(text=f"{original_filename}")
            self.update_cropped_info()

    def update_cropped_info(self):
        remaining_images = self.total_images - self.total_cropped - self.total_skipped
        self.cropped_info_label.config(text=f"Cropped Images: {self.total_cropped}\nSkipped Images: {self.total_skipped}")
        self.remaining_info_label.config(text=f"Remaining Images: {remaining_images}")

    def previous_image(self):
        if self.image_index > 0:
            self.image_index -= 1
            self.show_image()
        else:
            messagebox.showinfo("Info", "You are at the first image.")

    def next_image(self):
        if self.image_index < len(self.image_paths) - 1:
            self.image_index += 1
            self.show_image()
        else:
            messagebox.showinfo("Info", "You are at the last image.")

    def load_by_name(self):
        image_name = self.image_name_entry.get().strip()
        full_image_path = os.path.join(self.image_folder, image_name)

        # Check if the image exists in the folder
        if os.path.isfile(full_image_path):
            # Reset image index to load the specific image by name
            self.image_paths = [full_image_path]  # Load only the specified image
            self.image_index = 0
            self.show_image()
        else:
            messagebox.showerror("Error", "Image not found. Please check the folder and image name.")

        # Clear the input box regardless of the result
        self.image_name_entry.delete(0, 'end')

    def load_skipped_images(self):
        # If there are skipped images, load the next one
        if self.skipped_images:
            if self.image_index < len(self.skipped_images):
                # Load skipped images one by one
                self.image_paths = self.skipped_images
                self.image_index = 0
                self.show_image()
            else:
                messagebox.showinfo("Info", "No more skipped images to load.")
        else:
            messagebox.showinfo("Info", "No skipped images available.")

    def start_crop(self, event):
        self.crop_rectangle = [event.x, event.y, event.x, event.y]
        self.canvas.bind("<Motion>", self.update_crop)

    def update_crop(self, event):
        if self.crop_rectangle:
            self.crop_rectangle[2] = event.x
            self.crop_rectangle[3] = event.y
            self.canvas.delete("crop")
            self.canvas.create_rectangle(self.crop_rectangle, outline='red', tags="crop")

    def end_crop(self, event):
        self.canvas.unbind("<Motion>")
        self.crop_image()

    def crop_image(self):
        if self.crop_rectangle and self.current_image:
            x1, y1, x2, y2 = self.crop_rectangle
            x1 = max(x1, 0)
            y1 = max(y1, 0)
            x2 = min(x2, self.original_size[0])
            y2 = min(y2, self.original_size[1])

            if x1 < x2 and y1 < y2:
                self.cropped_image = self.current_image.crop((x1, y1, x2, y2))

                try:
                    if self.cropped_image.getbbox() is None:
                        raise ValueError("Cropped image is empty or invalid.")
                except Exception as e:
                    messagebox.showerror("Error", f"Cropping failed: {e}")
                    return

                if self.cropped_image.mode != 'RGB':
                    self.cropped_image = self.cropped_image.convert('RGB')

                # Save the cropped image with the original name but .webp extension
                original_filename = os.path.basename(self.image_paths[self.image_index])
                save_path = os.path.join(self.save_folder, f"{os.path.splitext(original_filename)[0]}.webp")

                if save_path not in self.skipped_images:  # Avoid saving if already skipped
                    self.save_cropped_image(save_path)
                else:
                    messagebox.showinfo("Info", "Image is skipped; please retake or skip it.")

            else:
                messagebox.showerror("Error", "No valid crop area defined.")

    def save_cropped_image(self, save_path):
        self.cropped_image.save(save_path, format='WEBP', quality=90)
        self.total_cropped += 1  # Increment the total cropped counter
        self.show_crop_success_popup()

    def show_crop_success_popup(self):
        # Create a new top-level window for the success message
        self.success_window = Toplevel(self.master)
        self.success_window.title("Success")
        self.success_window.geometry("350x150")
        self.success_window.transient(self.master)  # Make the popup dependent on the main window
        self.success_window.grab_set()  # Prevent interaction with other windows

        # Center the success window
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - 175
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - 75
        self.success_window.geometry(f"350x150+{x}+{y}")

        success_label = Label(self.success_window, text="Image cropped and saved successfully!")
        success_label.pack(pady=20)

        button_frame = Frame(self.success_window)
        button_frame.pack(pady=10)

        retake_button = Button(button_frame, text="Retake", command=self.retake_image)
        retake_button.grid(row=0, column=0, padx=5)

        ok_button = Button(button_frame, text="OK", command=lambda: self.ok_and_next_image(self.success_window))
        ok_button.grid(row=0, column=1, padx=5)

        skip_button = Button(button_frame, text="Skip", command=lambda: self.skip_image_and_close(self.success_window))
        skip_button.grid(row=0, column=2, padx=5)

    def retake_image(self):
        self.canvas.delete("crop")  # Clear the cropping rectangle
        self.crop_rectangle = None  # Reset crop rectangle
        self.show_image()  # Show the current image again
        self.success_window.destroy()  # Close the success window if open

    def skip_image_and_close(self, success_window):
        success_window.destroy()  # Close the success popup
        self.total_skipped += 1  # Increment skipped counter
        self.skipped_images.append(os.path.basename(self.image_paths[self.image_index]))  # Store skipped image name
        self.update_cropped_info()  # Update display info
        self.next_image()  # Go to the next image

    def ok_and_next_image(self, success_window):
        success_window.destroy()  # Close the success popup
        self.update_cropped_info()  # Update display info
        self.next_image()  # Go to the next image after saving

if __name__ == "__main__":
    root = Tk()  
    app = ImageCropper(root)
    root.mainloop()
