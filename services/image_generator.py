from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

class ImageGenerator:
    def __init__(self, template_path):
        self.template_path = template_path
        self.output_dir = Path("assets/images/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_image(self, name, date, font_size=40, color="#000000", 
                      name_pos=(100, 100), date_pos=(100, 200)):
        """
        Generate personalized image with name and date
        
        Args:
            name: Person's name
            date: Date string or combined dates
            font_size: Size of the text
            color: Text color in hex
            name_pos: (x, y) position for name
            date_pos: (x, y) position for date
            
        Returns:
            Path to generated image
        """
        try:
            # Open template image
            img = Image.open(self.template_path).convert('RGBA')
            
            # Create drawing context
            draw = ImageDraw.Draw(img)
            
            # Try to load custom font, fallback to default
            try:
                font_path = Path("assets/fonts/arial.ttf")
                if font_path.exists():
                    font = ImageFont.truetype(str(font_path), font_size)
                else:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            # Convert hex color to RGB
            color_rgb = self._hex_to_rgb(color)
            
            # Draw name
            draw.text(name_pos, f"{name}", fill=color_rgb, font=font)
            
            # Draw date
            draw.text(date_pos, f"{date}", fill=color_rgb, font=font)
            
            # Save image
            output_filename = f"{name.replace(' ', '_')}_{date.replace('/', '-').replace(', ', '_')}.png"
            output_path = self.output_dir / output_filename
            
            img.save(output_path, 'PNG')
            return str(output_path)
            
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return None
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))