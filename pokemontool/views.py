from django.shortcuts import render, redirect
from .forms import PokemonCardForm
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import os
import textwrap

def generate_card(request):
    if request.method == 'POST':
        form = PokemonCardForm(request.POST, request.FILES)
        if form.is_valid():
            # Create card instance but don't save yet
            card = form.save(commit=False)
            
            # Set default value for required attack1_name if not provided
            if not card.attack1_name:
                card.attack1_name = "Basic Attack"
                
            # Now save the card
            card.save()

            # Load card template based on type
            card_type = card.type if card.type else 'normal'
            template_name = f'card_template_{card_type}.png'
            base_image_path = os.path.join(settings.BASE_DIR, 'pokemontool', 'static', template_name)
            
            # Fallback to default template if type-specific template doesn't exist
            if not os.path.exists(base_image_path):
                base_image_path = os.path.join(settings.BASE_DIR, 'pokemontool', 'static', 'card_template.png')
            
            card_image = Image.open(base_image_path)
            draw = ImageDraw.Draw(card_image)

            # Load fonts with different sizes
            font_path = os.path.join(settings.BASE_DIR, 'pokemontool', 'static', 'fonts', 'Sansation_Bold.ttf')
            if not os.path.exists(font_path):
                raise FileNotFoundError(f"Font file not found at {font_path}")
            
            # Adjust font sizes for smaller card
            title_font = ImageFont.truetype(font_path, 24)  # Reduced from 32
            large_font = ImageFont.truetype(font_path, 20)  # Reduced from 24
            medium_font = ImageFont.truetype(font_path, 16)  # Reduced from 20
            small_font = ImageFont.truetype(font_path, 12)   # Reduced from 16

            # Header section - adjusted x,y coordinates
            if card.name:
                draw.text((30, 20), card.name, fill="black", font=title_font)
            if card.hp:
                draw.text((220, 30), f"HP {card.hp}", fill="red", font=large_font)
            
            # Pokemon image - precise positioning and sizing
            if card.image:
                # Calculate image dimensions
                image_width = 315 - 43  # = 272 pixels
                image_height = 257 - 62  # = 195 pixels
                
                # Open and convert image to RGBA
                pokemon_image = Image.open(card.image).convert("RGBA")
                
                # Resize image to cover the entire space (might crop some parts)
                original_width, original_height = pokemon_image.size
                ratio = max(image_width/original_width, image_height/original_height)
                new_size = (int(original_width * ratio), int(original_height * ratio))
                pokemon_image = pokemon_image.resize(new_size, Image.Resampling.LANCZOS)
                
                # Calculate cropping coordinates to center the image
                left = (new_size[0] - image_width) // 2
                top = (new_size[1] - image_height) // 2
                right = left + image_width
                bottom = top + image_height
                
                # Crop the image to fit exactly
                pokemon_image = pokemon_image.crop((left, top, right, bottom))
                
                # Paste the final image onto the card at the exact coordinates
                card_image.paste(pokemon_image, (43, 62), pokemon_image)

            # Add evolution photo handling
            if card.evolution_photo:
                # Calculate evolution image dimensions
                evo_width = 60
                evo_height = 60
                
                # Open and convert evolution image to RGBA
                evo_image = Image.open(card.evolution_photo).convert("RGBA")
                
                # Resize evolution image
                evo_image = evo_image.resize((evo_width, evo_height), Image.Resampling.LANCZOS)
                
                # Create a circular mask
                mask = Image.new('L', (evo_width, evo_height), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0, evo_width, evo_height), fill=255)
                
                # Apply the circular mask to the evolution image
                output = Image.new('RGBA', (evo_width, evo_height), (0, 0, 0, 0))
                output.paste(evo_image, (0, 0))
                output.putalpha(mask)
                
                # Position the evolution image in the top right corner
                evo_x = 27  # 10 pixels from right edge
                evo_y = 50  # Same y-position as main image
                
                # Paste the circular evolution image
                card_image.paste(output, (evo_x, evo_y), output)

            # Pokemon info - adjusted positioning
            if card.type:
                draw.text((60, 265), f"Type: {card.type}", fill="black", font=medium_font)
            if card.length or card.weight:
                length_str = card.length if card.length else ""
                weight_str = card.weight if card.weight else ""
                draw.text((220, 265), f"{length_str} / {weight_str}", fill="black", font=medium_font)

            # Attacks - adjusted y_pos starting point and spacing
            y_pos = 290
            if card.attack1_name:
                attack1_text = card.attack1_name
                if card.attack1_damage:
                    attack1_text += f" - {card.attack1_damage}"
                draw.text((30, y_pos), attack1_text, fill="black", font=medium_font)
                if card.attack1_info:
                    draw.text((30, y_pos + 20), card.attack1_info, fill="black", font=small_font)
                y_pos += 45  # Reduced spacing

            if card.attack2_name:
                attack2_text = card.attack2_name
                if card.attack2_damage:
                    attack2_text += f" - {card.attack2_damage}"
                draw.text((30, y_pos), attack2_text, fill="black", font=medium_font)
                if card.attack2_info:
                    draw.text((30, y_pos + 20), card.attack2_info, fill="black", font=small_font)
                y_pos += 45  # Reduced spacing

            # Weakness/Resistance/Retreat - adjusted positioning
            if card.weakness_element and card.weakness_amount:
                draw.text((30, y_pos), f"Weakness: {card.weakness_element} {card.weakness_amount}×", fill="black", font=small_font)
            if card.resistance_element and card.resistance_amount:
                draw.text((150, y_pos), f"Resistance: {card.resistance_element} {card.resistance_amount}", fill="black", font=small_font)
            if card.retreat_cost is not None:
                draw.text((270, y_pos), f"Retreat: {card.retreat_cost}", fill="black", font=small_font)

            # Footer - adjusted positioning
            if card.description:
                y_pos += 40
                # Wrap description text to fit width
                description_lines = textwrap.wrap(card.description, width=40)  # Adjust width as needed
                for line in description_lines:
                    draw.text((30, y_pos), line, fill="black", font=small_font)
                    y_pos += 15

            # Final footer line
            y_pos = 450  # Fixed position from bottom
            if card.illustrator:
                draw.text((50, y_pos), f"Illus. {card.illustrator}", fill="black", font=small_font)
            if card.collection_number or card.rarity:
                collection_str = f"#{card.collection_number}" if card.collection_number else ""
                rarity_str = f" {card.rarity}" if card.rarity else ""
                draw.text((220, y_pos), f"{collection_str}{rarity_str}", fill="black", font=small_font)

            # Save the final card image
            output_path = os.path.join(settings.MEDIA_ROOT, 'cards', f"{card.id}_card.png")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            card_image.save(output_path)

            # Store the generated image URL in session
            generated_card_url = f"{settings.MEDIA_URL}cards/{card.id}_card.png"
            request.session['generated_card_url'] = generated_card_url

            return redirect('card_generated')
    else:
        form = PokemonCardForm()

    return render(request, 'pokemontool/card_form.html', {'form': form})


def card_generated(request):
    # Retrieve the generated image URL from the session
    generated_card_url = request.session.get('generated_card_url')
    return render(request, 'pokemontool/card_generated.html', {'generated_card_url': generated_card_url})
