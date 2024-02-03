import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
import os, sys
from pathlib import Path

poppler_path=os.environ.get('POPPER_PATH')
class PDF2JPEG:
    def __init__(self):
        self.root = tk.Tk()
        exe_path = os.path.abspath(sys.argv[0])
        exe_dir = os.path.dirname(exe_path)
        icon_path = os.path.join (exe_dir,'icon.ico')  
        self.root.iconbitmap(icon_path)
        self.root.title("PDF to JPEG Converter")
        self.root.geometry("600x400")
        self.root.config(bg="#F5F5F5")    
        # Styles
        self.button_style = {"font": ("Arial", 12), "bg": "#3498DB", "fg": "white", "padx": 10, "pady": 5}
        self.label_style = {"font": ("Arial", 11), "pady": 5}
    
        # Upload file button
        self.upload_button = tk.Button(self.root, text="Upload PDF", command=self.browse_file, **self.button_style)
        self.upload_button.pack(pady=10)

        # Output path button
        self.output_button = tk.Button(self.root, text="Select Output Path", command=self.browse_directory, **self.button_style)
        self.output_button.pack(pady=5)

        # Submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit, **self.button_style)
        self.submit_button.pack(pady=10)

        # Display filename label
        self.filename_label = tk.Label(self.root, text="")
        self.filename_label.pack(pady=5)

        # Display directory label
        self.directory_label = tk.Label(self.root, text="")
        self.directory_label.pack(pady=5)

        self.submit_label = tk.Label(self.root, text="")
        self.submit_label.pack(pady=5)

        self.root.mainloop()
    
    def pdf_to_images(self, pdf_path, output_path):
        images = convert_from_path(pdf_path, 500, poppler_path=poppler_path)
        filename = os.path.splitext(os.path.basename(pdf_path))[0]
        try:
            for i, image in enumerate(images):
                image.save(f"{output_path}/{filename} page_{i+1}.jpg", "JPEG")
            msg = f'PDF file {filename} is successfully converted to JPEG file!'    
        except Exception as e:
            msg = e
        return msg

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
        if filename:
            if Path(filename).suffix != ".pdf":
                msg = "File selected is not a PDF file. Please upload a PDF file."
            else:
                msg = "Valid file format."
            
            self.filename_label.config(text=f"File uploaded: {filename} \n {msg}")   

    def browse_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.directory_label.config(text="Output Path: " + dir_path)

    def submit(self):
        if self.filename_label.cget("text") and self.directory_label.cget('text'):
            filename = self.filename_label.cget("text").split("\n")[0].split(": ")[1]
            directory = self.directory_label.cget('text').split(": ")[1]
            msg = self.pdf_to_images(filename, directory)
            if filename != '' and directory != '':
                self.submit_label.config(text=msg)
            else:
                self.submit_label.config(text='Please enter a filename and/or output path')
        else:
           self.submit_label.config(text='Please enter filename and directory.')

if __name__ == '__main__':
    pdf2jpeg = PDF2JPEG()
