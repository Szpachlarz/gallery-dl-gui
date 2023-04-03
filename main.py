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
    print("link: ", dpg.get_value("textbox"))
    print("sciezka: ", dpg.get_value("textbox2"))
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

with dpg.window(width=500, height=300, label="GUI"):
    dpg.add_text("Podaj link do galerii", tag="text item")
    dpg.add_input_text(hint="http://", tag="textbox", callback=validation)
    dpg.add_text(default_value="", tag="validate")
    dpg.add_image_button(label="Wklej", tag="przyciskwklej", width=15, height=15, texture_tag="iconpaste", callback=wklej)
    dpg.add_button(label="Pobierz", tag="przyciskpobierz", callback=pobierz)
    dpg.add_button(label="Wybierz sciezke", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_input_text(hint=downloads_path, tag="textbox2")

# bind item handler registry to item
dpg.bind_item_handler_registry("przyciskpobierz", "widget handler")

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()