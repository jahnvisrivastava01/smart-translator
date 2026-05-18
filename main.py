import customtkinter as ctk
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import threading
import time


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#020817"
CARD = "#07122A"
CARD2 = "#0F172A"
ACCENT = "#00D4FF"
TEXT = "#E5E7EB"
MUTED = "#64748B"
BORDER = "#1E293B"


app = ctk.CTk()

app.geometry("1200x950")

app.title("Smart Translator")

app.configure(fg_color=BG)

pygame.mixer.init()


header = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

header.pack(
    fill="x",
    padx=30,
    pady=(20, 10)
)

title = ctk.CTkLabel(
    header,
    text="Smart Translator",
    font=("Arial", 38, "bold"),
    text_color=ACCENT
)

title.pack(anchor="w")

subtitle = ctk.CTkLabel(
    header,
    text="The only translator you need",
    font=("Segoe UI", 16),
    text_color=MUTED
)

subtitle.pack(anchor="w")


main_card = ctk.CTkFrame(
    app,
    fg_color=CARD,
    corner_radius=25,
    border_width=1,
    border_color=BORDER
)

main_card.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=20
)


input_label = ctk.CTkLabel(
    main_card,
    text="INPUT TEXT",
    font=("Segoe UI", 14, "bold"),
    text_color=MUTED
)

input_label.pack(
    anchor="w",
    padx=35,
    pady=(25, 10)
)


input_box = ctk.CTkTextbox(
    main_card,
    height=140,
    corner_radius=18,
    fg_color=CARD2,
    border_width=1,
    border_color=BORDER,
    font=("Segoe UI", 20),
    text_color=TEXT
)

input_box.pack(
    fill="x",
    padx=35
)


lang_frame = ctk.CTkFrame(
    main_card,
    fg_color="transparent"
)

lang_frame.pack(pady=20)

languages = [
    "english",
    "french",
    "hindi",
    "spanish",
    "german",
    "italian"
]


source_lang = ctk.CTkOptionMenu(
    lang_frame,
    values=languages,
    width=260,
    height=55,
    corner_radius=14,
    fg_color=CARD2,
    button_color=CARD2,
    button_hover_color=CARD2,
    dropdown_fg_color=CARD2,
    font=("Segoe UI", 16)
)

source_lang.set("english")

source_lang.grid(
    row=0,
    column=0,
    padx=10
)


target_lang = ctk.CTkOptionMenu(
    lang_frame,
    values=languages,
    width=260,
    height=55,
    corner_radius=14,
    fg_color=CARD2,
    button_color=CARD2,
    button_hover_color=CARD2,
    dropdown_fg_color=CARD2,
    font=("Segoe UI", 16)
)

target_lang.set("french")

target_lang.grid(
    row=0,
    column=2,
    padx=10
)


def swap_languages():

    current_source = source_lang.get()

    current_target = target_lang.get()

    source_lang.set(current_target)

    target_lang.set(current_source)


swap_btn = ctk.CTkButton(
    lang_frame,
    text="⇄",
    command=swap_languages,
    width=65,
    height=55,
    font=("Arial", 24, "bold"),
    fg_color=CARD2,
    hover_color="#162033",
    corner_radius=14
)

swap_btn.grid(
    row=0,
    column=1,
    padx=10
)


def translate_text():

    text = input_box.get(
        "1.0",
        "end"
    ).strip()

    if text == "":
        return

    translated = GoogleTranslator(
        source=source_lang.get(),
        target=target_lang.get()
    ).translate(text)

    output_box.configure(state="normal")

    output_box.delete(
        "1.0",
        "end"
    )

    output_box.insert(
        "1.0",
        translated
    )


translate_btn = ctk.CTkButton(
    main_card,
    text="Translate",
    command=translate_text,
    height=55,
    font=("Segoe UI", 18, "bold"),
    fg_color=ACCENT,
    hover_color="#00B8E6",
    text_color="black",
    corner_radius=16
)

translate_btn.pack(
    fill="x",
    padx=35
)


output_label = ctk.CTkLabel(
    main_card,
    text="TRANSLATION",
    font=("Segoe UI", 14, "bold"),
    text_color=MUTED
)

output_label.pack(
    anchor="w",
    padx=35,
    pady=(20, 10)
)


output_box = ctk.CTkTextbox(
    main_card,
    height=140,
    corner_radius=18,
    fg_color=CARD2,
    border_width=1,
    border_color=BORDER,
    font=("Segoe UI", 20),
    text_color=TEXT
)

output_box.pack(
    fill="x",
    padx=35,
    pady=(0, 15)
)


actions_frame = ctk.CTkFrame(
    main_card,
    fg_color="transparent"
)

actions_frame.pack(
    fill="x",
    padx=35,
    pady=(0, 25)
)


def _speak():

    translated_text = output_box.get(
        "1.0",
        "end"
    ).strip()

    if translated_text == "":
        return

    language_code = {
        "english": "en",
        "french": "fr",
        "hindi": "hi",
        "spanish": "es",
        "german": "de",
        "italian": "it"
    }

    lang = language_code.get(
        target_lang.get(),
        "en"
    )

    speech = gTTS(
        text=translated_text,
        lang=lang
    )

    filename = f"voice_{int(time.time())}.mp3"
    speech.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def speak_translation():

    threading.Thread(
        target=_speak,
        daemon=True
    ).start()


def copy_translation():

    text = output_box.get(
        "1.0",
        "end"
    ).strip()

    app.clipboard_clear()

    app.clipboard_append(text)


speak_btn = ctk.CTkButton(
    actions_frame,
    text="🔊 Listen",
    command=speak_translation,
    height=50,
    width=220,
    font=("Segoe UI", 16, "bold"),
    fg_color=CARD2,
    hover_color="#162033",
    border_width=1,
    border_color=ACCENT,
    text_color=ACCENT,
    corner_radius=16
)

speak_btn.pack(
    side="left"
)


copy_btn = ctk.CTkButton(
    actions_frame,
    text="⎘ Copy",
    command=copy_translation,
    height=50,
    width=220,
    font=("Segoe UI", 16, "bold"),
    fg_color=CARD2,
    hover_color="#162033",
    border_width=1,
    border_color=BORDER,
    text_color=MUTED,
    corner_radius=16
)

copy_btn.pack(
    side="right"
)


app.mainloop()