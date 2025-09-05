#!/usr/bin/env python3
"""
Automated Image Generation System for TechReview Hub
Generates all required background images and product images using AI
"""

import os
import requests
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_generation.log'),
        logging.StreamHandler()
    ]
)

class ImageGenerator:
    def __init__(self):
        """Initialize the image generation system"""
        self.images_dir = "images"
        self.ensure_images_directory()
        self.required_images = self.load_image_requirements()
        
    def ensure_images_directory(self):
        """Create images directory if it doesn't exist"""
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
            logging.info(f"✅ Created images directory: {self.images_dir}")
    
    def load_image_requirements(self) -> Dict:
        """Load all required images with specifications"""
        return {
            # Homepage Images
            "hero-tech.jpg": {
                "size": (1200, 600),
                "description": "Modern smart home devices and tech gadgets hero image",
                "type": "hero_background"
            },
            "echo-dot.jpg": {
                "size": (400, 300),
                "description": "Amazon Echo Dot 5th generation smart speaker",
                "type": "product"
            },
            "nest-thermostat.jpg": {
                "size": (400, 300),
                "description": "Google Nest Learning Thermostat smart home device",
                "type": "product"
            },
            "airpods-pro.jpg": {
                "size": (400, 300),
                "description": "Apple AirPods Pro 2nd generation wireless earbuds",
                "type": "product"
            },
            
            # Blog Images
            "blog-smart-home-2025.jpg": {
                "size": (800, 400),
                "description": "Smart home technology trends for 2025",
                "type": "blog_header"
            },
            "blog-buying-guide.jpg": {
                "size": (800, 400),
                "description": "Tech buying guide and recommendations",
                "type": "blog_header"
            },
            "blog-security.jpg": {
                "size": (800, 400),
                "description": "Smart home security and privacy",
                "type": "blog_header"
            },
            
            # Review Page Images
            "echo-dot-hero.jpg": {
                "size": (600, 400),
                "description": "Amazon Echo Dot review hero image with product details",
                "type": "review_hero"
            },
            "echo-dot-design.jpg": {
                "size": (600, 300),
                "description": "Echo Dot design details and build quality",
                "type": "review_detail"
            },
            
            # Blog Article Images
            "smart-home-2025-hero.jpg": {
                "size": (800, 400),
                "description": "Smart home technology trends 2025 hero image",
                "type": "article_hero"
            },
            "matter-ecosystem.jpg": {
                "size": (600, 300),
                "description": "Matter protocol ecosystem diagram",
                "type": "infographic"
            },
            "google-nest-hub-max.jpg": {
                "size": (200, 150),
                "description": "Google Nest Hub Max smart display",
                "type": "product_small"
            },
            "amazon-echo-show-15.jpg": {
                "size": (200, 150),
                "description": "Amazon Echo Show 15 smart display",
                "type": "product_small"
            },
            "sense-energy-monitor.jpg": {
                "size": (200, 150),
                "description": "Sense Energy Monitor device",
                "type": "product_small"
            },
            "tesla-powerwall.jpg": {
                "size": (200, 150),
                "description": "Tesla Powerwall home battery system",
                "type": "product_small"
            },
            
            # Starter Kit Images
            "starter-kit-hub.jpg": {
                "size": (150, 150),
                "description": "Smart home hub device",
                "type": "product_icon"
            },
            "starter-kit-lights.jpg": {
                "size": (150, 150),
                "description": "Smart light bulbs and lighting",
                "type": "product_icon"
            },
            "starter-kit-thermostat.jpg": {
                "size": (150, 150),
                "description": "Smart thermostat device",
                "type": "product_icon"
            },
            "starter-kit-security.jpg": {
                "size": (150, 150),
                "description": "Smart security camera",
                "type": "product_icon"
            },
            
            # Thumbnail Images
            "nest-thermostat-thumb.jpg": {
                "size": (80, 80),
                "description": "Nest thermostat thumbnail",
                "type": "thumbnail"
            },
            "airpods-pro-thumb.jpg": {
                "size": (80, 80),
                "description": "AirPods Pro thumbnail",
                "type": "thumbnail"
            },
            "featured-echo-dot.jpg": {
                "size": (80, 80),
                "description": "Featured Echo Dot thumbnail",
                "type": "thumbnail"
            },
            "featured-nest-thermostat.jpg": {
                "size": (80, 80),
                "description": "Featured Nest thermostat thumbnail",
                "type": "thumbnail"
            },
            
            # Article Thumbnails
            "smart-speaker-guide-thumb.jpg": {
                "size": (60, 60),
                "description": "Smart speaker guide thumbnail",
                "type": "article_thumb"
            },
            "smart-security-thumb.jpg": {
                "size": (60, 60),
                "description": "Smart security article thumbnail",
                "type": "article_thumb"
            },
            
            # Logo and Branding
            "amazon-logo.png": {
                "size": (40, 40),
                "description": "Amazon logo for retailer links",
                "type": "logo"
            },
            "logo.png": {
                "size": (200, 60),
                "description": "TechReview Hub logo",
                "type": "brand_logo"
            }
        }
    
    def generate_placeholder_image(self, filename: str, specs: Dict) -> bool:
        """Generate a professional placeholder image"""
        try:
            width, height = specs["size"]
            description = specs["description"]
            image_type = specs["type"]
            
            # Create image with appropriate background
            if image_type in ["hero_background", "blog_header", "article_hero"]:
                # Gradient background for headers
                img = self.create_gradient_background(width, height)
            elif image_type in ["product", "product_small", "product_icon"]:
                # Clean white background for products
                img = self.create_product_background(width, height)
            elif image_type == "infographic":
                # Light blue background for diagrams
                img = self.create_infographic_background(width, height)
            else:
                # Default gray background
                img = self.create_default_background(width, height)
            
            # Add text overlay
            self.add_text_overlay(img, description, image_type)
            
            # Add decorative elements based on type
            if image_type == "product":
                self.add_product_elements(img)
            elif image_type in ["hero_background", "blog_header"]:
                self.add_tech_elements(img)
            
            # Save image
            filepath = os.path.join(self.images_dir, filename)
            img.save(filepath, quality=95, optimize=True)
            
            logging.info(f"✅ Generated: {filename} ({width}x{height})")
            return True
            
        except Exception as e:
            logging.error(f"❌ Error generating {filename}: {e}")
            return False
    
    def create_gradient_background(self, width: int, height: int) -> Image.Image:
        """Create gradient background for hero images"""
        img = Image.new('RGB', (width, height), '#667eea')
        draw = ImageDraw.Draw(img)
        
        # Create gradient effect
        for y in range(height):
            # Gradient from blue to purple
            ratio = y / height
            r = int(102 + (118 - 102) * ratio)  # 102 to 118
            g = int(126 + (75 - 126) * ratio)   # 126 to 75
            b = int(234 + (162 - 234) * ratio)  # 234 to 162
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        return img
    
    def create_product_background(self, width: int, height: int) -> Image.Image:
        """Create clean background for product images"""
        img = Image.new('RGB', (width, height), '#f8fafc')
        draw = ImageDraw.Draw(img)
        
        # Add subtle border
        border_color = '#e2e8f0'
        draw.rectangle([2, 2, width-3, height-3], outline=border_color, width=2)
        
        return img
    
    def create_infographic_background(self, width: int, height: int) -> Image.Image:
        """Create background for infographic images"""
        img = Image.new('RGB', (width, height), '#f0f7ff')
        draw = ImageDraw.Draw(img)
        
        # Add grid pattern
        grid_color = '#e3f2fd'
        for x in range(0, width, 50):
            draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
        for y in range(0, height, 50):
            draw.line([(0, y), (width, y)], fill=grid_color, width=1)
        
        return img
    
    def create_default_background(self, width: int, height: int) -> Image.Image:
        """Create default background"""
        return Image.new('RGB', (width, height), '#f1f5f9')
    
    def add_text_overlay(self, img: Image.Image, text: str, image_type: str):
        """Add text overlay to image"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Choose font size based on image size
        if width >= 800:
            font_size = 36
        elif width >= 400:
            font_size = 24
        elif width >= 200:
            font_size = 16
        else:
            font_size = 12
        
        try:
            # Try to use a nice font (may not be available on all systems)
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Wrap text for better display
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), line_text, font=font)
            line_width = bbox[2] - bbox[0]
            
            if line_width > width - 40:  # Leave 20px margin on each side
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate total text height
        line_height = font_size + 5
        total_height = len(lines) * line_height
        
        # Center text vertically
        start_y = (height - total_height) // 2
        
        # Draw text with shadow effect
        text_color = '#333333' if image_type in ['product', 'product_small'] else '#ffffff'
        shadow_color = '#000000' if text_color == '#ffffff' else '#cccccc'
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x = (width - line_width) // 2
            y = start_y + i * line_height
            
            # Draw shadow
            draw.text((x + 1, y + 1), line, font=font, fill=shadow_color)
            # Draw main text
            draw.text((x, y), line, font=font, fill=text_color)
    
    def add_product_elements(self, img: Image.Image):
        """Add decorative elements for product images"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Add corner accent
        accent_color = '#667eea'
        corner_size = min(width, height) // 10
        
        # Top-right corner accent
        draw.polygon([
            (width - corner_size, 0),
            (width, 0),
            (width, corner_size)
        ], fill=accent_color)
    
    def add_tech_elements(self, img: Image.Image):
        """Add tech-themed decorative elements"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Add circuit-like lines
        line_color = 'rgba(255, 255, 255, 0.3)'
        
        # Draw some geometric shapes
        for i in range(3):
            x = random.randint(50, width - 50)
            y = random.randint(50, height - 50)
            size = random.randint(20, 40)
            
            # Draw circle
            draw.ellipse([x, y, x + size, y + size], outline='#ffffff', width=2)
    
    def generate_all_images(self) -> bool:
        """Generate all required images"""
        logging.info("🎨 Starting image generation for TechReview Hub...")
        
        success_count = 0
        total_count = len(self.required_images)
        
        for filename, specs in self.required_images.items():
            if self.generate_placeholder_image(filename, specs):
                success_count += 1
            else:
                logging.error(f"❌ Failed to generate {filename}")
        
        logging.info(f"✅ Generated {success_count}/{total_count} images successfully")
        
        if success_count == total_count:
            logging.info("🎉 All images generated successfully!")
            return True
        else:
            logging.warning(f"⚠️ {total_count - success_count} images failed to generate")
            return False
    
    def create_favicon(self):
        """Create favicon.ico for the website"""
        try:
            # Create 32x32 favicon
            img = Image.new('RGB', (32, 32), '#667eea')
            draw = ImageDraw.Draw(img)
            
            # Draw simple tech icon (microchip-like)
            draw.rectangle([4, 4, 28, 28], fill='#ffffff', outline='#333333', width=2)
            draw.rectangle([8, 8, 24, 24], fill='#667eea')
            
            # Add small squares (like a microchip)
            for x in range(10, 23, 4):
                for y in range(10, 23, 4):
                    draw.rectangle([x, y, x+2, y+2], fill='#ffffff')
            
            # Save as ICO
            favicon_path = "favicon.ico"
            img.save(favicon_path, format='ICO', sizes=[(32, 32)])
            
            logging.info("✅ Generated favicon.ico")
            return True
            
        except Exception as e:
            logging.error(f"❌ Error generating favicon: {e}")
            return False
    
    def optimize_images(self):
        """Optimize all generated images for web"""
        logging.info("🔧 Optimizing images for web...")
        
        for filename in os.listdir(self.images_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                try:
                    filepath = os.path.join(self.images_dir, filename)
                    img = Image.open(filepath)
                    
                    # Optimize and save
                    if filename.lower().endswith('.png'):
                        img.save(filepath, 'PNG', optimize=True)
                    else:
                        img.save(filepath, 'JPEG', quality=85, optimize=True)
                    
                    logging.info(f"✅ Optimized: {filename}")
                    
                except Exception as e:
                    logging.error(f"❌ Error optimizing {filename}: {e}")
        
        logging.info("🎉 Image optimization complete!")
    
    def generate_image_manifest(self):
        """Generate manifest of all images"""
        manifest = {
            "generated_at": datetime.now().isoformat(),
            "total_images": len(self.required_images),
            "images": {}
        }
        
        for filename, specs in self.required_images.items():
            filepath = os.path.join(self.images_dir, filename)
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                manifest["images"][filename] = {
                    "size": specs["size"],
                    "description": specs["description"],
                    "type": specs["type"],
                    "file_size": file_size,
                    "status": "generated"
                }
            else:
                manifest["images"][filename] = {
                    "size": specs["size"],
                    "description": specs["description"],
                    "type": specs["type"],
                    "status": "missing"
                }
        
        # Save manifest
        with open(os.path.join(self.images_dir, "manifest.json"), 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logging.info("✅ Generated image manifest")

def main():
    """Main function to run image generation"""
    print("🎨 TechReview Hub - Automated Image Generation System")
    print("==================================================")
    
    generator = ImageGenerator()
    
    print("\nOptions:")
    print("1. Generate all images")
    print("2. Generate specific image type")
    print("3. Create favicon only")
    print("4. Optimize existing images")
    print("5. Generate image manifest")
    print("6. Exit")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == '1':
        print("\n🎨 Generating all images...")
        success = generator.generate_all_images()
        generator.create_favicon()
        generator.optimize_images()
        generator.generate_image_manifest()
        
        if success:
            print("🎉 All images generated successfully!")
            print(f"📁 Images saved in: {generator.images_dir}/")
        else:
            print("⚠️ Some images failed to generate. Check logs for details.")
    
    elif choice == '2':
        print("\nImage types:")
        print("1. Product images")
        print("2. Hero/background images")
        print("3. Blog images")
        print("4. Thumbnails")
        print("5. Logos")
        
        type_choice = input("Choose type (1-5): ").strip()
        type_map = {
            '1': ['product', 'product_small', 'product_icon'],
            '2': ['hero_background', 'blog_header', 'article_hero'],
            '3': ['blog_header', 'article_hero', 'infographic'],
            '4': ['thumbnail', 'article_thumb'],
            '5': ['logo', 'brand_logo']
        }
        
        if type_choice in type_map:
            target_types = type_map[type_choice]
            for filename, specs in generator.required_images.items():
                if specs['type'] in target_types:
                    generator.generate_placeholder_image(filename, specs)
            print(f"✅ Generated images for selected type")
        else:
            print("❌ Invalid choice")
    
    elif choice == '3':
        print("\n🎨 Creating favicon...")
        generator.create_favicon()
        print("✅ Favicon created!")
    
    elif choice == '4':
        print("\n🔧 Optimizing images...")
        generator.optimize_images()
        print("✅ Images optimized!")
    
    elif choice == '5':
        print("\n📋 Generating image manifest...")
        generator.generate_image_manifest()
        print("✅ Manifest generated!")
    
    elif choice == '6':
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()