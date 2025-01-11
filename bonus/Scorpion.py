import os
from PIL import Image
from PIL.ExifTags import TAGS

passData = [34970, "ImageDescription", 39594, "ComponentsConfiguration", "ExposureProgram"]

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if not exif_data:
            return {"Error": "No EXIF data found in this image."}
        
        exif_info = {}
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name in passData:
                continue
            exif_info[tag_name] = value

        return exif_info
    except Exception as e:
        return {"Error": f"Error reading EXIF data: {e}"}

def get_file_metadata(file_path):
    try:
        file_stats = os.stat(file_path)
        creation_date = os.path.getctime(file_path)
        metadata = {
            "File Name": os.path.basename(file_path),
            "File Size (bytes)": file_stats.st_size,
            "Creation Date": creation_date
        }
        return metadata
    except Exception as e:
        return {"Error": f"Error retrieving file metadata: {e}"}
