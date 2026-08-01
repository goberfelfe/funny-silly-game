import math
import textwrap
import numpy as np
import pygame
import pgzrun

ICON = 'gay.png'
WIDTH = 700
HEIGHT = 600
TITLE = "funny silly game"

player_x = (WIDTH // 2) - 15
player_y = 300
speed = 4
player_size = 30

pygame.mixer.init(frequency=22050, size=-16, channels=1)

def generate_blip_sound():
    duration = 0.04
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    buf = np.zeros((n_samples,), dtype=np.int16)
    
    for i in range(n_samples):
        t = float(i) / sample_rate
        value = 32767 if (math.sin(2 * math.pi * 440 * t) > 0) else -32767
        decay = (n_samples - i) / n_samples
        buf[i] = int(value * decay * 0.3)
        
    return pygame.mixer.Sound(buf)

default_blip = generate_blip_sound()

dialogue_active = False
dialogue_queue = []
full_text = ""
displayed_text = ""
speaker_name = ""
char_index = 0
type_speed = 0.03
time_since_last_char = 0

def say(text, speaker="chatter"):
    global dialogue_active
    
    speaker_clean = speaker.lower()
    
    char_limit = 42
    wrapped_lines = textwrap.wrap(text, width=char_limit)
    
    max_lines_per_box = 2 if (speaker_clean and speaker_clean != "chatter") else 3
    for i in range(0, len(wrapped_lines), max_lines_per_box):
        chunk = wrapped_lines[i:i + max_lines_per_box]
        formatted_text = "\n".join(chunk)
        dialogue_queue.append((formatted_text, speaker_clean))
    
    if not dialogue_active:
        advance_dialogue()

def advance_dialogue():
    global dialogue_active, full_text, displayed_text, speaker_name, char_index, time_since_last_char
    
    if dialogue_queue:
        full_text, speaker_name = dialogue_queue.pop(0)
        displayed_text = ""
        char_index = 0
        time_since_last_char = 0
        dialogue_active = True
    else:
        dialogue_active = False

def play_speaker_sound(speaker):
    try:
        sound_to_play = getattr(sounds, speaker)
        sound_to_play.play()
    except AttributeError:
        default_blip.play()

say("AGHHHH I CAN SEE MY BONES", "gober")
say("THEY ARE MELTING MY BRAIN IT HURTSSS", "rebog")
say("OR MAYBE YOURE JUST DUMB???!?!??", "gober")
say("omfg...", "rebog")
say("im js playin with u im gay af ;u;", "gober")
say("Geometry Dash is an addicting 2D platformer where you will find the most difficult puzzle levels, many challenges, adventures and fun As such, there is no plot in this game, but it is not needed, because the essence of the game is not to go through the storyline, but to overcome levels with obstacles, on each of which you will find traps, various obstacles, physical puzzles and much, much more.", "rebog")

title_set = False

def update(dt):
    global player_x, player_y, title_set
    global char_index, displayed_text, time_since_last_char
    
    if not title_set:
        pygame.display.set_caption("funny silly game")
        title_set = True

    if not dialogue_active:
        if (keyboard.left or keyboard.a) and player_x > 0:
            player_x -= speed
        if (keyboard.right or keyboard.d) and player_x < WIDTH - player_size:
            player_x += speed
        if (keyboard.up or keyboard.w) and player_y > 0:
            player_y -= speed
        if (keyboard.down or keyboard.s) and player_y < HEIGHT - player_size:
            player_y += speed

    if dialogue_active and char_index < len(full_text):
        time_since_last_char += dt
        if time_since_last_char >= type_speed:
            displayed_text += full_text[char_index]
            
            if full_text[char_index] not in (" ", "\n"):
                play_speaker_sound(speaker_name)
                
            char_index += 1
            time_since_last_char = 0

def on_key_down(key):
    global dialogue_active, displayed_text, char_index
    
    if key == keys.Z and dialogue_active:
        if char_index < len(full_text):
            displayed_text = full_text
            char_index = len(full_text)
        else:
            advance_dialogue()

def draw():
    screen.fill((0, 0, 0))
    
    screen.draw.filled_rect(Rect((player_x, player_y), (player_size, player_size)), (255, 0, 0))
    
    if dialogue_active:
        box_margin = 40
        box_width = WIDTH - (box_margin * 2)
        
        box_rect = Rect((box_margin, 440), (box_width, 130))
        border_rect = Rect((box_margin - 5, 435), (box_width + 10, 140))
        
        screen.draw.filled_rect(border_rect, (255, 255, 255))
        screen.draw.filled_rect(box_rect, (0, 0, 0))
        
        text_x = box_rect.x + 20
        header_y = box_rect.y + 15
        text_y = box_rect.y + 42
        max_width = box_rect.width - 40
        
        if speaker_name and speaker_name != "chatter":
            screen.draw.text(
                f"* {speaker_name.capitalize()}:", 
                (text_x, header_y), 
                color="yellow", 
                fontsize=16, 
                fontname="undertale"
            )

        screen.draw.text(
            displayed_text, 
            (text_x, text_y), 
            color="white", 
            fontsize=16, 
            fontname="undertale",
            width=max_width,
            lineheight=1.2
        )

pgzrun.go()