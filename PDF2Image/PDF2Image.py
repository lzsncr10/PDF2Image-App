import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
import os
from pathlib import Path

poppler_path=r'C:\Users\lzsnc\poppler-23.11.0\Library\bin'

def pdf_to_images(pdf_path, output_path):
    pdf_path =  Path(pdf_path)
    images = convert_from_path(pdf_path,500,poppler_path=poppler_path)
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    try:
        for i, image in enumerate(images):
            image.save(f"{output_path}/{filename} page_{i+1}.jpg", "JPEG")
        msg = f'PDF file {filename} is successfully converted to JPEG file!'    
    except Exception as e:
        msg = e
    return msg

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
    if Path(filename).suffix != ".pdf":
        msg = "File selected is not a PDF file. Please upload a PDF file."
    else:
        msg = "Valid file format."
        
    filename_label.config(text=f"File uploaded: {filename} \n {msg}")   

def browse_directory():
    dir_path = filedialog.askdirectory()
    directory_label.config(text="Output Path: " + dir_path)

def submit():
    filename = filename_label.cget('text')
    directory = directory_label.cget('text')
    msg = pdf_to_images(filename, directory)
    if filename != '' and directory != '':
        submit_label.config(text=msg)
    else:
        submit_label.config(text='Please enter a filename and/or output path')


root = tk.Tk()
root.title("PDF to JPEG Converter")
root.geometry("600x400")
              
# Upload file button
upload_button = tk.Button(root, text="Upload PDF", command=browse_file)
upload_button.pack(pady=10)

# Output path button
output_button = tk.Button(root, text="Select Output Path", command=browse_directory)
output_button.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=10)

# Display filename label
filename_label = tk.Label(root, text="")
filename_label.pack(pady=5)

# Display directory label
directory_label = tk.Label(root, text="")
directory_label.pack(pady=5)

submit_label = tk.Label(root, text="")
submit_label.pack(pady=5)

root.mainloop()