import dearpygui.dearpygui as dpg
import subprocess
from pathlib import Path
import pyperclip
import re
downloads_path = str(Path.home() / "Downloads")

dpg.create_context()

width, height, channels, data = dpg.load_image("iconpaste.png")

with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="iconpaste")

def pobierz(sender, app_data):
    subprocess.run(["gallery-dl", dpg.get_value("textbox"), "-d", dpg.get_value("textbox2")])

def filecallback(sender, app_data):
    dpg.set_value("textbox2", app_data["file_path_name"])

def wklej(sender, app_data):
    dpg.set_value("textbox", pyperclip.paste())

def validation(sender, app_data):
    result = subprocess.run(["gallery-dl", "-E", dpg.get_value("textbox")], capture_output=True, text=True).stderr
    x = re.search("Unsupported URL", result)
    if x!=None:
        dpg.set_value("validate", "Bledny link")
    else:
        dpg.set_value("validate", "")

dpg.add_file_dialog(
    directory_selector=True, show=False, callback=filecallback, tag="file_dialog_id", width=700, height=400)

with dpg.item_handler_registry(tag="widget handler") as handler:
    dpg.add_item_clicked_handler(callback=pobierz)

with dpg.font_registry():    
    with dpg.font("Anonymous_Pro.ttf", 20) as font1:
        dpg.add_font_chars([0x0105, 0x0104, 0x0107, 0x0106, 0x0119, 0x0118, 0x0142, 0x0141, 0x0144, 0x0143, 0x00f3, 0x00d3, 0x015b, 0x015b, 0x015a, 0x017a, 0x0179, 0x017c, 0x017b])
        default_font = font1

with dpg.window(width=500, height=300, label="GUI"):
    dpg.add_text("Podaj link do galerii", tag="text item")
    with dpg.group(horizontal=True):
        dpg.add_input_text(hint="http://", tag="textbox", callback=validation)
        dpg.add_image_button(label="Wklej", tag="przyciskwklej", width=15, height=15, texture_tag="iconpaste", callback=wklej)
        dpg.add_text(default_value="", tag="validate")    
    dpg.add_button(label="Wybierz ścieżkę", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_input_text(default_value=downloads_path, tag="textbox2")
    dpg.add_text()
    dpg.add_button(label="Pobierz", tag="przyciskpobierz", callback=pobierz)
    dpg.bind_font(default_font)

# bind item handler registry to item
dpg.bind_item_handler_registry("przyciskpobierz", "widget handler")

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()