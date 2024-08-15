from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips

app = Flask(__name__)

# Ensure the static directory exists
os.makedirs('static', exist_ok=True)

def get_character_folders():
    character_path = 'static/Assets/Characters/'
    return sorted([folder for folder in os.listdir(character_path) if os.path.isdir(os.path.join(character_path, folder))])

def get_background_files():
    background_path = 'static/Assets/Backgrounds/'
    return sorted([file for file in os.listdir(background_path) if file.endswith(('.jpg', '.jpeg', '.png'))])

def get_emotions_for_character(character):
    character_path = f'static/Assets/Characters/{character}/'
    emotions = set()
    for file in os.listdir(character_path):
        if file.endswith('.png'):
            parts = file.split('_')
            if len(parts) > 1:
                emotion = parts[1].split('.')[0]
                emotions.add(emotion.capitalize())
    return sorted(emotions)

def create_text_bubble(text, position):
    """Create a text bubble with the specified text and position."""
    bubble_size = (len(text)*15, 50)
    bubble_clip = TextClip(text, fontsize=20, color='black', bg_color='white', size=bubble_size, print_cmd=True)
    bubble_clip = bubble_clip.set_duration(1 + 0.1*len(text)).set_position(position)
    return bubble_clip

@app.route('/')
def index():
    characters = get_character_folders()
    backgrounds = get_background_files()
    emotions = {character: get_emotions_for_character(character) for character in characters}
    return render_template('index.html', characters=characters, backgrounds=backgrounds, emotions=emotions)

@app.route('/generate_video', methods=['POST'])
def generate_video():
    character1 = request.form.get('character1')
    character2 = request.form.get('character2')
    background = request.form.get('background')
    
    dialogues1 = request.form.getlist('dialogue1[]')
    emotions1 = request.form.getlist('emotion1[]')
    
    dialogues2 = request.form.getlist('dialogue2[]')
    emotions2 = request.form.getlist('emotion2[]')

    # Check for mismatched lists
    if len(dialogues1) != len(emotions1) or len(dialogues2) != len(emotions2):
        return "Error: Mismatched dialogues and emotions.", 400

    clips = []

    max_length = max(len(dialogues1), len(dialogues2))
    
    for i in range(max_length):
        clip_duration = 2 + 0.1*(len(dialogues1[i])+len(dialogues2[i]))

        # Prepare clips for both characters
        char1_image = f'static/Assets/Characters/{character1}/{character1.lower()}_{emotions1[i].lower()}.png' if i < len(emotions1) else f'static/Assets/Characters/{character1}/{character1.lower()}_neutral.png'
        char2_image = f'static/Assets/Characters/{character2}/{character2.lower()}_{emotions2[i].lower()}.png' if i < len(emotions2) else f'static/Assets/Characters/{character2}/{character2.lower()}_neutral.png'

        char1_clip = ImageClip(char1_image).resize(height=400).set_duration(clip_duration).set_position(('left', 'bottom'))
        char2_clip = ImageClip(char2_image).resize(height=400).set_duration(clip_duration).set_position(('right', 'bottom'))

        background_clip = ImageClip(f'static/Assets/Backgrounds/{background}').resize((1280, 480)).set_duration(clip_duration)  # Set duration to match clip duration

        for j in range(2):
            # Create a combined clip for this frame
            clip_elements = [background_clip, char1_clip, char2_clip]

            # Alternate the text bubbles
            if j % 2 == 0:
                text_bubble1 = create_text_bubble(f"{dialogues1[i]}", position=('left', 'top')) if i < len(dialogues1) and dialogues1[i] else None
                if text_bubble1:
                    clip_elements.append(text_bubble1)
            else:
                text_bubble2 = create_text_bubble(f"{dialogues2[i]}", position=('right', 'top')) if i < len(dialogues2) and dialogues2[i] else None
                if text_bubble2:
                    clip_elements.append(text_bubble2)

            clip = CompositeVideoClip(clip_elements, size=(960, 480))
        
            # Add the composite clip to the list of clips
            clips.append(clip)

    # Handle the case where there are no clips
    if not clips:
        return "Error: No dialogues provided.", 400

    # Concatenate all clips
    try:
        video = concatenate_videoclips(clips, method="compose")
    except Exception as e:
        return f"Error concatenating clips: {str(e)}", 500
    
    # Save the video
    output_path = 'static/animation.mp4'
    video.write_videofile(output_path, fps=24)

    return redirect(url_for('static', filename='animation.mp4'))

# Route to serve files from static directory
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

