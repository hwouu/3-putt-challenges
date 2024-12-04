# src/utils/asset_loader.py

from PIL import Image
import os

def get_asset_path(category, filename):
    """에셋 파일의 전체 경로를 반환합니다."""
    return os.path.join('src', 'assets', 'images', category, filename)

def load_and_resize_image(image_path, width, height):
    """이미지를 로드하고 지정된 크기로 리사이즈합니다."""
    image = Image.open(image_path)
    return image.resize((width, height), Image.Resampling.LANCZOS)