import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengolahan Citra Digital")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        self.image = None
        self.gray_image = None
        self.binary_image = None

        # =========================
        # FRAME BUTTON
        # =========================
        button_frame = Frame(root, bg="#d9d9d9", width=250)
        button_frame.pack(side=LEFT, fill=Y)

        Label(
            button_frame,
            text="MENU PENGOLAHAN CITRA",
            bg="#d9d9d9",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        Button(button_frame, text="Input Gambar", width=25,
               command=self.load_image).pack(pady=5)

        Button(button_frame, text="Grayscale", width=25,
               command=self.convert_grayscale).pack(pady=5)

        Button(button_frame, text="Citra Biner", width=25,
               command=self.convert_binary).pack(pady=5)

        Button(button_frame, text="Histogram", width=25,
               command=self.show_histogram).pack(pady=5)

        Button(button_frame, text="Blur", width=25,
               command=self.blur_image).pack(pady=5)

        Button(button_frame, text="Sharpen", width=25,
               command=self.sharpen_image).pack(pady=5)

        Button(button_frame, text="Edge Detection", width=25,
               command=self.edge_detection).pack(pady=5)

        Button(button_frame, text="Dilasi", width=25,
               command=self.dilation).pack(pady=5)

        Button(button_frame, text="Erosi", width=25,
               command=self.erosion).pack(pady=5)

        Button(button_frame, text="Operasi AND", width=25,
               command=self.logic_and).pack(pady=5)

        Button(button_frame, text="Operasi OR", width=25,
               command=self.logic_or).pack(pady=5)

        Button(button_frame, text="Tambah Brightness", width=25,
               command=self.add_brightness).pack(pady=5)
        Button(button_frame, text="Kurangi Brightness", width=25,
               command=self.subtract_brightness).pack(pady=5)

        Button(button_frame, text="Simpan Hasil", width=25,
               command=self.save_image).pack(pady=5)

        Button(button_frame, text="Keluar", width=25,
               command=root.quit).pack(pady=5)
         # =========================
        # FRAME IMAGE
        # =========================
        image_frame = Frame(root, bg="white")
        image_frame.pack(side=RIGHT, expand=True, fill=BOTH)

        self.image_label = Label(image_frame, bg="white")
        self.image_label.pack(expand=True)

    # ====================================
    # LOAD IMAGE
    # ====================================
    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
            )

        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image(self.image)

    # ====================================
    # DISPLAY IMAGE
    # ====================================
    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((700, 500))

        img_tk = ImageTk.PhotoImage(img_pil)

        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    # ====================================
    # GRAYSCALE
    # ====================================
    def convert_grayscale(self):
        if self.image is None:
            messagebox.showerror("Error", "Input gambar terlebih dahulu")
            return

        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        gray_bgr = cv2.cvtColor(self.gray_image, cv2.COLOR_GRAY2BGR)
        self.display_image(gray_bgr)

    # ====================================
    # BINARY IMAGE
    # ====================================
    def convert_binary(self):
        if self.gray_image is None:
            self.convert_grayscale()

        _, self.binary_image = cv2.threshold(
            self.gray_image,
            127,
            255,
            cv2.THRESH_BINARY
        )

        binary_bgr = cv2.cvtColor(self.binary_image, cv2.COLOR_GRAY2BGR)
        self.display_image(binary_bgr)

    # ====================================
    # HISTOGRAM
    # ====================================
    def show_histogram(self):
        if self.gray_image is None:
            self.convert_grayscale()

        plt.hist(self.gray_image.ravel(), 256, [0, 256])
        plt.title("Histogram Grayscale")
        plt.xlabel("Nilai Piksel")
        plt.ylabel("Jumlah Piksel")
        plt.show()

    # ====================================
    # BLUR IMAGE
    # ====================================
    def blur_image(self):
        if self.image is None:
            return

        blur = cv2.blur(self.image, (7, 7))
        self.display_image(blur)

    # ====================================
    # SHARPEN IMAGE
    # ====================================
    def sharpen_image(self):
        if self.image is None:
            return

        kernel = np.array([
            [0, -1,  0],
            [-1, 5, -1],
            [0, -1,  0]
        ])

        sharp = cv2.filter2D(self.image, -1, kernel)
        self.display_image(sharp)

    # ====================================
    # EDGE DETECTION
    # ====================================
    def edge_detection(self):
        if self.gray_image is None:
            self.convert_grayscale()

        sobel = cv2.Sobel(self.gray_image, cv2.CV_64F, 1, 1, ksize=3)
        sobel = np.uint8(np.absolute(sobel))

        sobel_bgr = cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)
        self.display_image(sobel_bgr)

    # ====================================
    # DILATION
    # ====================================
    def dilation(self):
        if self.binary_image is None:
            self.convert_binary()

        kernel = np.ones((5, 5), np.uint8)
        dilasi = cv2.dilate(self.binary_image, kernel, iterations=1)

        dilasi_bgr = cv2.cvtColor(dilasi, cv2.COLOR_GRAY2BGR)
        self.display_image(dilasi_bgr)

    # ====================================
    # EROSION
    # ====================================
    def erosion(self):
        if self.binary_image is None:
            self.convert_binary()

        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))

        erosi = cv2.erode(self.binary_image, kernel, iterations=1)

        erosi_bgr = cv2.cvtColor(erosi, cv2.COLOR_GRAY2BGR)
        self.display_image(erosi_bgr)

    # ====================================
    # LOGIC AND
    # ====================================
    def logic_and(self):
        if self.image is None:
            return

        result = cv2.bitwise_and(self.image, self.image)
        self.display_image(result)

    # ====================================
    # LOGIC OR
    # ====================================
    def logic_or(self):
        if self.image is None:
            return

        result = cv2.bitwise_or(self.image, self.image)
        self.display_image(result)

    # ====================================
    # ADD BRIGHTNESS
    # ====================================
    def add_brightness(self):
        if self.image is None:
            return

        bright = cv2.convertScaleAbs(self.image, beta=50)
        self.display_image(bright)

    # ====================================
    # SUBTRACT BRIGHTNESS
    # ====================================
    def subtract_brightness(self):
        if self.image is None:
            return

        dark = cv2.convertScaleAbs(self.image, beta=-50)
        self.display_image(dark)

    # ====================================
    # SAVE IMAGE
    # ====================================
    def save_image(self):
        if self.image is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
        )

        if file_path:
            cv2.imwrite(file_path, self.image)
            messagebox.showinfo("Sukses", "Gambar berhasil disimpan")

# ====================================
# MAIN PROGRAM
# ====================================
root = Tk()
app = ImageProcessingApp(root)
root.mainloop()