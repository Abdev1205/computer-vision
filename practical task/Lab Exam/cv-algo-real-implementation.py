import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageThresholdingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Thresholding")

        self.img_path = None
        self.uploaded_img_label = tk.Label(root)
        self.uploaded_img_label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image, bg="black", fg="white",
                                       activebackground="black", activeforeground="white", relief=tk.FLAT,
                                       font=("Helvetica", 12), padx=10, pady=8, borderwidth=0, highlightthickness=0,
                                       cursor="hand2", width=20)
        self.upload_button.pack()
        self.add_button_hover_effect(self.upload_button)

        self.output_frame = tk.Frame(root)
        self.output_frame.pack(pady=10)

        self.thresholded_label = tk.Label(self.output_frame)
        self.thresholded_label.pack()

        self.method_buttons = [
            ("BINARY", cv2.THRESH_BINARY),
            ("BINARY_INV", cv2.THRESH_BINARY_INV),
            ("TOZERO", cv2.THRESH_TOZERO),
            ("TOZERO_INV", cv2.THRESH_TOZERO_INV),
            ("TRUNC", cv2.THRESH_TRUNC),
            ("MEAN_C", cv2.ADAPTIVE_THRESH_MEAN_C),
            ("GAUSSIAN_C", cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
        ]

        button_frame = tk.Frame(root)
        button_frame.pack()

        for method_name, method_code in self.method_buttons:
            button = tk.Button(button_frame, text=method_name, command=lambda m=method_code: self.apply_thresholding(m),
                                bg="black", fg="white", font=("Helvetica", 12), relief=tk.FLAT, padx=10, pady=8,
                                borderwidth=0, highlightthickness=0, cursor="hand2", width=15)
            button.pack(side=tk.LEFT, padx=5)
            self.rounded_button(button)
            self.add_button_hover_effect(button)

    def upload_image(self):
        self.img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if self.img_path:
            image = Image.open(self.img_path)
            image.thumbnail((300, 300))
            self.uploaded_img_label.img = ImageTk.PhotoImage(image)
            self.uploaded_img_label.config(image=self.uploaded_img_label.img)

    def apply_thresholding(self, method):
        if self.img_path:
            image = cv2.imread(self.img_path, cv2.IMREAD_GRAYSCALE)
            if method in [cv2.ADAPTIVE_THRESH_MEAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C]:
                thresholded = cv2.adaptiveThreshold(image, 255, method, cv2.THRESH_BINARY, 11, 2)
            else:
                _, thresholded = cv2.threshold(image, 128, 255, method)
            
            thresholded_pil = Image.fromarray(thresholded)
            thresholded_resized = thresholded_pil.resize((int(self.uploaded_img_label.winfo_width() * 0.8), int(self.uploaded_img_label.winfo_height() * 0.8)), Image.ANTIALIAS)
            thresholded_tk = ImageTk.PhotoImage(thresholded_resized)
            
            self.thresholded_label.config(image=thresholded_tk)
            self.thresholded_label.image = thresholded_tk

    def rounded_button(self, button):
        button.config(borderwidth=0, highlightthickness=0)
        button.bind("<Enter>", lambda e: button.config(bg="#444"))
        button.bind("<Leave>", lambda e: button.config(bg="black"))

    def add_button_hover_effect(self, button):
        button.bind("<Enter>", lambda e: button.config(bg="#444"))
        button.bind("<Leave>", lambda e: button.config(bg="black"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageThresholdingApp(root)
    root.mainloop()
