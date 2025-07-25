import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from PIL import Image, ImageTk
import io
import math
from pathlib import Path
import json
from datetime import datetime
import sys

class ImageCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Compressor")
        self.root.geometry("1300x600")
        self.root.configure(bg='#f5f5f5')
        
        # Set minimum window size to prevent UI from becoming too cramped
        self.root.minsize(1300, 600)
        
        # Set application icon
        self.set_application_icon()
        
        # Load custom fonts
        try:
            font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts")
            self.regular_font = ("fccTYPO-Regular", 11)
            self.bold_font = ("fccTYPO-Bold", 11)
        except Exception as e:
            print(f"Warning: Could not load custom fonts: {e}")
            self.regular_font = ("Arial", 11)
            self.bold_font = ("Arial", 11)
        
        # Variables
        self.input_files = []
        self.output_dir = ""
        self.compression_settings = {
            'quality': 85,
            'max_width': 1920,
            'max_height': 1080,
            'resample_method': 'LANCZOS',
            'optimize': True,
            'progressive': False,
            'keep_exif': True,
            'format': 'auto'
        }
        
        self.setup_ui()
        self.load_settings()
        
        # Apply some styling
        self.apply_styling()
        
    def set_application_icon(self):
        """Set the application icon based on platform"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_dir, "assets", "icons")
            if sys.platform == "darwin":
                icon_file = os.path.join(icon_path, "icon.png")
                if os.path.exists(icon_file):
                    icon = tk.PhotoImage(file=icon_file)
                    self.root.iconphoto(True, icon)
            elif sys.platform == "win32":
                icon_file = os.path.join(icon_path, "icon.ico")
                if os.path.exists(icon_file):
                    self.root.iconbitmap(icon_file)
            else:
                icon_file = os.path.join(icon_path, "icon.png")
                if os.path.exists(icon_file):
                    icon = tk.PhotoImage(file=icon_file)
                    self.root.iconphoto(True, icon)
        except Exception as e:
            print(f"Error loading application icon: {str(e)}")
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Advanced Image Compressor", 
                               font=self.bold_font)
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Create main content area with two columns
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Left column: File selection and settings
        left_column = ttk.Frame(content_frame)
        left_column.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Right column: Preview and controls
        right_column = ttk.Frame(content_frame)
        right_column.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # File selection section
        self.create_file_section(left_column)
        
        # Compression settings section
        self.create_settings_section(left_column)
        
        # Preview section
        self.create_preview_section(right_column)
        
        # Control buttons
        self.create_control_buttons(right_column)
        
        # Progress and log section
        self.create_progress_section(main_frame)
        
    def create_file_section(self, parent):
        # File selection frame
        file_frame = ttk.LabelFrame(parent, text="File Selection", padding="8")
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 8))
        file_frame.columnconfigure(1, weight=1)
        
        # Input files
        ttk.Label(file_frame, text="Input Files:", font=self.bold_font).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.files_listbox = tk.Listbox(file_frame, height=3, selectmode=tk.EXTENDED, width=50, font=self.regular_font)
        self.files_listbox.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        files_buttons_frame = ttk.Frame(file_frame)
        files_buttons_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Button(files_buttons_frame, text="Add Files", 
                  command=self.add_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(files_buttons_frame, text="Add Folder", 
                  command=self.add_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(files_buttons_frame, text="Clear All", 
                  command=self.clear_files).pack(side=tk.LEFT)
        
        # Output directory
        ttk.Label(file_frame, text="Output Directory:", font=self.bold_font).grid(row=3, column=0, sticky=tk.W, pady=(8, 5))
        
        output_frame = ttk.Frame(file_frame)
        output_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        output_frame.columnconfigure(0, weight=1)
        
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(output_frame, text="Browse", 
                  command=self.select_output_dir).grid(row=0, column=1)
        
    def create_settings_section(self, parent):
        # Settings frame
        settings_frame = ttk.LabelFrame(parent, text="Compression Settings", padding="8")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 8))
        
        # Create two columns for settings
        left_settings = ttk.Frame(settings_frame)
        left_settings.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 8))
        
        right_settings = ttk.Frame(settings_frame)
        right_settings.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Left column settings - more compact layout
        # Quality and dimensions in one row
        quality_frame = ttk.Frame(left_settings)
        quality_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        quality_frame.columnconfigure(1, weight=1)
        
        ttk.Label(quality_frame, text="Quality:").grid(row=0, column=0, sticky=tk.W)
        self.quality_var = tk.IntVar(value=self.compression_settings['quality'])
        quality_scale = ttk.Scale(quality_frame, from_=1, to=100, 
                                 variable=self.quality_var, orient=tk.HORIZONTAL)
        quality_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        self.quality_label = ttk.Label(quality_frame, text=str(self.quality_var.get()), width=3, font=self.regular_font)
        self.quality_label.grid(row=0, column=2, padx=(5, 0))
        quality_scale.configure(command=self.update_quality_label)
        
        # Dimensions in one row
        dim_frame = ttk.Frame(left_settings)
        dim_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(dim_frame, text="Max W:").grid(row=0, column=0, sticky=tk.W)
        self.max_width_var = tk.IntVar(value=self.compression_settings['max_width'])
        ttk.Entry(dim_frame, textvariable=self.max_width_var, width=8).grid(row=0, column=1, sticky=tk.W, padx=(5, 10))
        
        ttk.Label(dim_frame, text="Max H:").grid(row=0, column=2, sticky=tk.W)
        self.max_height_var = tk.IntVar(value=self.compression_settings['max_height'])
        ttk.Entry(dim_frame, textvariable=self.max_height_var, width=8).grid(row=0, column=3, sticky=tk.W, padx=(5, 0))
        
        # Resample method
        ttk.Label(left_settings, text="Resample:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.resample_var = tk.StringVar(value=self.compression_settings['resample_method'])
        resample_combo = ttk.Combobox(left_settings, textvariable=self.resample_var, 
                                     values=['LANCZOS', 'BICUBIC', 'BILINEAR', 'NEAREST', 'BOX', 'HAMMING'])
        resample_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Right column settings - more compact
        # Format and checkboxes in one column
        ttk.Label(right_settings, text="Format:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.format_var = tk.StringVar(value=self.compression_settings['format'])
        format_combo = ttk.Combobox(right_settings, textvariable=self.format_var, 
                                   values=['auto', 'JPEG', 'PNG', 'WEBP'])
        format_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Checkboxes in a more compact layout
        checkbox_frame = ttk.Frame(right_settings)
        checkbox_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        self.optimize_var = tk.BooleanVar(value=self.compression_settings['optimize'])
        ttk.Checkbutton(checkbox_frame, text="Optimize", 
                       variable=self.optimize_var).pack(side=tk.LEFT, padx=(0, 10))
        
        self.progressive_var = tk.BooleanVar(value=self.compression_settings['progressive'])
        ttk.Checkbutton(checkbox_frame, text="Progressive", 
                       variable=self.progressive_var).pack(side=tk.LEFT, padx=(0, 10))
        
        self.keep_exif_var = tk.BooleanVar(value=self.compression_settings['keep_exif'])
        ttk.Checkbutton(checkbox_frame, text="Keep EXIF", 
                       variable=self.keep_exif_var).pack(side=tk.LEFT)
        
        # Configure column weights
        left_settings.columnconfigure(1, weight=1)
        right_settings.columnconfigure(1, weight=1)
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        
    def create_preview_section(self, parent):
        # Preview frame
        preview_frame = ttk.LabelFrame(parent, text="Preview", padding="8")
        preview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 8))
        preview_frame.columnconfigure(1, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(preview_frame, width=300, height=180, bg='white')
        self.preview_canvas.grid(row=0, column=0, padx=(0, 8))
        
        # File info
        info_frame = ttk.Frame(preview_frame)
        info_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.info_text = scrolledtext.ScrolledText(info_frame, width=45, height=7, font=self.regular_font)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure weights
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        # Bind file selection
        self.files_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
    def create_control_buttons(self, parent):
        # Control buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        
        ttk.Button(buttons_frame, text="Compress Images", 
                  command=self.start_compression).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(buttons_frame, text="Save Settings", 
                  command=self.save_settings).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(buttons_frame, text="Reset Settings", 
                  command=self.reset_settings).pack(side=tk.LEFT)
        
    def create_progress_section(self, parent):
        # Progress frame
        progress_frame = ttk.LabelFrame(parent, text="Progress & Log", padding="8")
        progress_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(progress_frame, textvariable=self.status_var, font=self.regular_font).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Log text
        self.log_text = scrolledtext.ScrolledText(progress_frame, height=4, font=self.regular_font)
        self.log_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure weights
        parent.rowconfigure(2, weight=1)
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(2, weight=1)
        
    def update_quality_label(self, value):
        self.quality_label.config(text=str(int(float(value))))
        
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.files_listbox.insert(tk.END, os.path.basename(file))
        self.update_file_count()
        
    def add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder with Images")
        if folder:
            image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if Path(file).suffix.lower() in image_extensions:
                        file_path = os.path.join(root, file)
                        if file_path not in self.input_files:
                            self.input_files.append(file_path)
                            self.files_listbox.insert(tk.END, os.path.basename(file))
        self.update_file_count()
        
    def clear_files(self):
        self.input_files.clear()
        self.files_listbox.delete(0, tk.END)
        self.preview_canvas.delete("all")
        self.info_text.delete(1.0, tk.END)
        self.update_file_count()
        
    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_var.set(directory)
            
    def update_file_count(self):
        count = len(self.input_files)
        self.status_var.set(f"Ready - {count} file(s) selected")
        
    def on_file_select(self, event):
        selection = self.files_listbox.curselection()
        if selection:
            file_path = self.input_files[selection[0]]
            self.show_preview(file_path)
            
    def show_preview(self, file_path):
        try:
            # Load and resize image for preview
            with Image.open(file_path) as img:
                # Get original file size
                original_size = os.path.getsize(file_path)
                
                # Resize for preview
                preview_width, preview_height = 300, 180
                img_preview = img.copy()
                img_preview.thumbnail((preview_width, preview_height), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(img_preview)
                
                # Update canvas
                self.preview_canvas.delete("all")
                self.preview_canvas.create_image(
                    preview_width//2, preview_height//2, 
                    image=photo, anchor=tk.CENTER
                )
                self.preview_canvas.image = photo  # Keep reference
                
                # Update info
                info = f"File: {os.path.basename(file_path)}\n"
                info += f"Original Size: {self.format_size(original_size)}\n"
                info += f"Dimensions: {img.width} x {img.height}\n"
                info += f"Format: {img.format}\n"
                info += f"Mode: {img.mode}\n"
                
                # Calculate estimated compressed size
                estimated_size = self.estimate_compressed_size(img, original_size)
                info += f"Estimated Compressed: {self.format_size(estimated_size)}\n"
                info += f"Compression Ratio: {((original_size - estimated_size) / original_size * 100):.1f}%"
                
                self.info_text.delete(1.0, tk.END)
                self.info_text.insert(1.0, info)
                
        except Exception as e:
            self.log_message(f"Error loading preview: {str(e)}")
            
    def estimate_compressed_size(self, img, original_size):
        # Simple estimation based on quality and dimensions
        quality_factor = self.quality_var.get() / 100.0
        dimension_factor = min(1.0, (self.max_width_var.get() * self.max_height_var.get()) / (img.width * img.height))
        
        # Format-specific estimation
        if img.format == 'JPEG':
            return int(original_size * quality_factor * dimension_factor * 0.8)
        elif img.format == 'PNG':
            return int(original_size * dimension_factor * 0.6)
        else:
            return int(original_size * quality_factor * dimension_factor)
            
    def format_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_names = ["B", "KB", "MB", "GB"]
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
        
    def get_compression_settings(self):
        return {
            'quality': self.quality_var.get(),
            'max_width': self.max_width_var.get(),
            'max_height': self.max_height_var.get(),
            'resample_method': self.resample_var.get(),
            'optimize': self.optimize_var.get(),
            'progressive': self.progressive_var.get(),
            'keep_exif': self.keep_exif_var.get(),
            'format': self.format_var.get()
        }
        
    def start_compression(self):
        if not self.input_files:
            messagebox.showwarning("Warning", "Please select input files first!")
            return
            
        if not self.output_var.get():
            messagebox.showwarning("Warning", "Please select output directory!")
            return
            
        # Start compression in separate thread
        thread = threading.Thread(target=self.compress_images)
        thread.daemon = True
        thread.start()
        
    def compress_images(self):
        try:
            settings = self.get_compression_settings()
            total_files = len(self.input_files)
            processed = 0
            
            self.log_message("Starting compression...")
            
            for file_path in self.input_files:
                try:
                    self.status_var.set(f"Processing: {os.path.basename(file_path)}")
                    self.root.update_idletasks()
                    
                    # Compress single image
                    result = self.compress_single_image(file_path, settings)
                    
                    if result:
                        self.log_message(f"✓ {os.path.basename(file_path)} - {result}")
                    else:
                        self.log_message(f"✗ {os.path.basename(file_path)} - Failed")
                        
                    processed += 1
                    self.progress_var.set((processed / total_files) * 100)
                    self.root.update_idletasks()
                    
                except Exception as e:
                    self.log_message(f"✗ {os.path.basename(file_path)} - Error: {str(e)}")
                    processed += 1
                    self.progress_var.set((processed / total_files) * 100)
                    
            self.status_var.set(f"Completed! {processed} files processed")
            self.log_message("Compression completed!")
            messagebox.showinfo("Success", f"Compression completed!\n{processed} files processed.")
            
        except Exception as e:
            self.log_message(f"Compression error: {str(e)}")
            messagebox.showerror("Error", f"Compression failed: {str(e)}")
            
    def compress_single_image(self, input_path, settings):
        try:
            with Image.open(input_path) as img:
                # Get original size
                original_size = os.path.getsize(input_path)
                
                # Determine output format
                output_format = self.determine_output_format(input_path, settings['format'])
                
                # Resize if needed
                img_resized = self.resize_image(img, settings)
                
                # Prepare output path
                output_path = self.get_output_path(input_path, output_format)
                
                # Save with compression
                save_kwargs = self.get_save_kwargs(output_format, settings)
                img_resized.save(output_path, **save_kwargs)
                
                # Get compressed size
                compressed_size = os.path.getsize(output_path)
                compression_ratio = ((original_size - compressed_size) / original_size) * 100
                
                return f"{self.format_size(original_size)} → {self.format_size(compressed_size)} ({compression_ratio:.1f}% reduction)"
                
        except Exception as e:
            raise e
            
    def determine_output_format(self, input_path, format_setting):
        if format_setting == 'auto':
            # Keep original format
            ext = Path(input_path).suffix.lower()
            if ext in ['.jpg', '.jpeg']:
                return 'JPEG'
            elif ext == '.png':
                return 'PNG'
            elif ext == '.webp':
                return 'WEBP'
            else:
                return 'JPEG'  # Default
        else:
            return format_setting
            
    def resize_image(self, img, settings):
        # Calculate new dimensions
        width, height = img.size
        max_width = settings['max_width']
        max_height = settings['max_height']
        
        if width <= max_width and height <= max_height:
            return img  # No resize needed
            
        # Calculate aspect ratio
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        # Get resample method
        resample_methods = {
            'NEAREST': Image.Resampling.NEAREST,
            'BILINEAR': Image.Resampling.BILINEAR,
            'BICUBIC': Image.Resampling.BICUBIC,
            'LANCZOS': Image.Resampling.LANCZOS,
            'BOX': Image.Resampling.BOX,
            'HAMMING': Image.Resampling.HAMMING
        }
        resample = resample_methods.get(settings['resample_method'], Image.Resampling.LANCZOS)
        
        return img.resize((new_width, new_height), resample)
        
    def get_output_path(self, input_path, output_format):
        filename = Path(input_path).stem
        output_dir = self.output_var.get()
        
        if output_format == 'JPEG':
            return os.path.join(output_dir, f"{filename}_compressed.jpg")
        elif output_format == 'PNG':
            return os.path.join(output_dir, f"{filename}_compressed.png")
        elif output_format == 'WEBP':
            return os.path.join(output_dir, f"{filename}_compressed.webp")
        else:
            return os.path.join(output_dir, f"{filename}_compressed.jpg")
            
    def get_save_kwargs(self, output_format, settings):
        kwargs = {}
        
        if output_format == 'JPEG':
            kwargs.update({
                'quality': settings['quality'],
                'optimize': settings['optimize'],
                'progressive': settings['progressive']
            })
        elif output_format == 'PNG':
            kwargs.update({
                'optimize': settings['optimize']
            })
        elif output_format == 'WEBP':
            kwargs.update({
                'quality': settings['quality'],
                'method': 6 if settings['optimize'] else 4
            })
            
        return kwargs
        
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def save_settings(self):
        settings = self.get_compression_settings()
        try:
            with open('compression_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
            self.log_message("Settings saved successfully!")
        except Exception as e:
            self.log_message(f"Error saving settings: {str(e)}")
            
    def load_settings(self):
        try:
            if os.path.exists('compression_settings.json'):
                with open('compression_settings.json', 'r') as f:
                    settings = json.load(f)
                    
                # Update UI with loaded settings
                self.quality_var.set(settings.get('quality', 85))
                self.max_width_var.set(settings.get('max_width', 1920))
                self.max_height_var.set(settings.get('max_height', 1080))
                self.resample_var.set(settings.get('resample_method', 'LANCZOS'))
                self.optimize_var.set(settings.get('optimize', True))
                self.progressive_var.set(settings.get('progressive', False))
                self.keep_exif_var.set(settings.get('keep_exif', True))
                self.format_var.set(settings.get('format', 'auto'))
                
                self.log_message("Settings loaded successfully!")
        except Exception as e:
            self.log_message(f"Error loading settings: {str(e)}")
            
    def reset_settings(self):
        # Reset to default values
        self.quality_var.set(85)
        self.max_width_var.set(1920)
        self.max_height_var.set(1080)
        self.resample_var.set('LANCZOS')
        self.optimize_var.set(True)
        self.progressive_var.set(False)
        self.keep_exif_var.set(True)
        self.format_var.set('auto')
        
        self.log_message("Settings reset to defaults!")
        
    def apply_styling(self):
        """Apply modern styling to the UI"""
        try:
            # Configure ttk styles for a more modern look
            style = ttk.Style()
            
            # Configure frame styles
            style.configure('TLabelframe', borderwidth=1, relief='solid')
            style.configure('TLabelframe.Label', font=self.bold_font)
            
            # Configure button styles
            style.configure('TButton', padding=6, font=self.bold_font)
            
            # Configure entry styles
            style.configure('TEntry', padding=4, font=self.regular_font)
            
            # Configure combobox styles
            style.configure('TCombobox', padding=4, font=self.regular_font)
            
            # Configure scale styles
            style.configure('Horizontal.TScale', sliderlength=20)
            
            # Configure label styles
            style.configure('TLabel', font=self.regular_font)
            
        except Exception as e:
            # If styling fails, continue without it
            pass

def main():
    root = tk.Tk()
    app = ImageCompressor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
