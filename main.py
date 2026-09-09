import os
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from app.services.drywall_service import calculate_drywall_materials
from app.services.translation_service import get_text


def resource_path(relative_path):
  if hasattr(sys, "_MEIPASS"):
    base_path = sys._MEIPASS
  else:
    base_path = os.path.dirname(os.path.abspath(__file__))
  return os.path.join(base_path, relative_path)


Builder.load_file(resource_path("app/ui/theme.kv"))
Builder.load_file(resource_path("app/ui/main.kv"))


class DrywallLayout(BoxLayout):
  current_lang = StringProperty("en")
  current_unit = StringProperty("metric")

  t_subtitle = StringProperty("")
  t_height = StringProperty("")
  t_width = StringProperty("")
  t_calculate = StringProperty("")
  t_results = StringProperty("")
  resultado_texto = StringProperty("")

  def __init__(self, **kwargs):
    super(DrywallLayout, self).__init__(**kwargs)
    self.update_ui_texts()
    self.resultado_texto = get_text(self.current_lang, "enter_data")

  def change_language(self, lang):
    self.current_lang = lang
    self.update_ui_texts()
    if self.ids.input_height.text and self.ids.input_width.text:
      self.calculate()
    else:
      self.resultado_texto = get_text(self.current_lang, "enter_data")

  def toggle_unit(self):
    self.current_unit = (
        "imperial" if self.current_unit == "metric" else "metric"
    )
    self.update_ui_texts()

    try:
      if self.ids.input_height.text:
        val_h = float(self.ids.input_height.text)
        if self.current_unit == "imperial":
          self.ids.input_height.text = str(round(val_h * 3.28084, 2))
        else:
          self.ids.input_height.text = str(round(val_h / 3.28084, 2))

      if self.ids.input_width.text:
        val_w = float(self.ids.input_width.text)
        if self.current_unit == "imperial":
          self.ids.input_width.text = str(round(val_w * 3.28084, 2))
        else:
          self.ids.input_width.text = str(round(val_w / 3.28084, 2))

      if self.ids.input_height.text and self.ids.input_width.text:
        self.calculate()
    except ValueError:
      pass

  def update_ui_texts(self):
    self.t_subtitle = get_text(self.current_lang, "subtitle")
    self.t_calculate = get_text(self.current_lang, "calculate")
    self.t_results = get_text(self.current_lang, "results")

    if self.current_unit == "metric":
      self.t_height = get_text(self.current_lang, "height_m")
      self.t_width = get_text(self.current_lang, "width_m")
    else:
      self.t_height = get_text(self.current_lang, "height_ft")
      self.t_width = get_text(self.current_lang, "width_ft")

  def calculate(self):
    try:
      raw_height = float(self.ids.input_height.text)
      raw_width = float(self.ids.input_width.text)

      if self.current_unit == "imperial":
        height = raw_height / 3.28084
        width = raw_width / 3.28084
      else:
        height = raw_height
        width = raw_width

      results = calculate_drywall_materials(height, width)
      if results:
        text = ""
        key_mapping = {
            "Total Area (m2)": "total_area",
            "Perimeter (m)": "perimeter",
            "Tracks": "tracks",
            "Studs": "studs",
            "Boards": "boards",
            "Anchors": "anchors",
            "T1 Screws": "t1_screws",
            "T2 Screws": "t2_screws",
            "Paper Tape (m)": "tape",
            "Joint Compound (kg)": "compound",
        }

        for k, v in results.items():
          translated_key = get_text(self.current_lang, key_mapping.get(k, k))

          if self.current_unit == "imperial":
            if k == "Total Area (m2)":
              v = round(v * 10.7639, 2)
              unit_label = "sq ft"
            elif k in ["Perimeter (m)", "Paper Tape (m)"]:
              v = round(v * 3.28084, 2)
              unit_label = "ft"
            else:
              unit_label = ""
          else:
            if k == "Total Area (m2)":
              unit_label = "m2"
            elif k in ["Perimeter (m)", "Paper Tape (m)"]:
              unit_label = "m"
            else:
              unit_label = ""

          unit_str = f" {unit_label}" if unit_label else ""
          text += f"- {translated_key}: {v}{unit_str}\n"

        self.resultado_texto = text
      else:
        self.resultado_texto = get_text(self.current_lang, "invalid_zero")
    except ValueError:
      self.resultado_texto = get_text(self.current_lang, "error_value")


class DrywallCalculatorApp(App):

  def build(self):
    self.title = "DRYWALL CALCULATOR"
    return DrywallLayout()


if __name__ == "__main__":
  DrywallCalculatorApp().run()