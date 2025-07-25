# Changelog

## [0.0.1] – 2025-07-25

### Added
- Initial release of ImageCompressor
- Advanced image compression with multiple format support
- Batch processing of JPG, PNG, BMP, TIFF, and WebP images
- Multi-file and folder selection with drag-and-drop support
- Advanced compression settings with quality control (1–100)
- Smart resizing with maximum width/height limits and aspect ratio preservation
- Six resampling algorithms: LANCZOS, BICUBIC, BILINEAR, NEAREST, BOX, HAMMING
- Multiple output formats: JPEG, PNG, WebP with auto-detection
- Progressive JPEG support for better web loading
- EXIF data preservation option
- Real-time image preview with compression estimation
- File size analysis and compression ratio prediction
- Two-column modern UI layout for efficient space usage
- Custom font and icon support (fccTYPO-Regular, fccTYPO-Bold)
- Settings persistence and management
- Progress tracking with detailed logging
- Cross-platform application icon support

### Improved
- Optimized UI layout with reduced height and better space utilization
- Responsive design with minimum window size constraints
- Real-time preview updates when selecting files
- Automatic output directory suggestion
- Multi-threaded compression to keep UI responsive
- Comprehensive error handling for missing files and conversion issues
- Professional styling with custom fonts throughout the interface
- Efficient file list management with clear all functionality

### Technical Details
- Built with Python and Tkinter (ttk)
- Uses Pillow for advanced image processing and compression
- Threading for non-blocking UI during compression operations
- Custom font and icon loading from assets directory
- JSON-based settings persistence
- Platform-specific icon handling (PNG for macOS/Linux, ICO for Windows)

### Dependencies
- Pillow >= 10.0.0
- tkinter (Python standard library)
- Custom fonts: fccTYPO-Regular.ttf, fccTYPO-Bold.ttf 