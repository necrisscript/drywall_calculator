from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from app.services.drywall_service import calculate_drywall_materials
from app.services.translation_service import get_text

Builder.load_file("app/ui/theme.kv")
Builder.load_file("app/ui/main.kv")


class DrywallLayout(BoxLayout):
  current_lang = StringProperty("en")
  current_unit = StringProperty("metric")

  t_subtitle = StringProperty("")
  t_area = StringProperty("")
  t_perimeter = StringProperty("")
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
    if self.ids.input_area.text and self.ids.input_perimeter.text:
      self.calculate()
    else:
      self.resultado_texto = get_text(self.current_lang, "enter_data")

  def toggle_unit(self):
    self.current_unit = (
        "imperial" if self.current_unit == "metric" else "metric"
    )
    self.update_ui_texts()

    try:
      if self.ids.input_area.text:
        val_area = float(self.ids.input_area.text)
        if self.current_unit == "imperial":
          self.ids.input_area.text = str(round(val_area * 10.7639, 2))
        else:
          self.ids.input_area.text = str(round(val_area / 10.7639, 2))

      if self.ids.input_perimeter.text:
        val_peri = float(self.ids.input_perimeter.text)
        if self.current_unit == "imperial":
          self.ids.input_perimeter.text = str(round(val_peri * 3.28084, 2))
        else:
          self.ids.input_perimeter.text = str(round(val_peri / 3.28084, 2))

      if self.ids.input_area.text and self.ids.input_perimeter.text:
        self.calculate()
    except ValueError:
      pass

  def update_ui_texts(self):
    self.t_subtitle = get_text(self.current_lang, "subtitle")
    self.t_calculate = get_text(self.current_lang, "calculate")
    self.t_results = get_text(self.current_lang, "results")

    if self.current_unit == "metric":
      self.t_area = get_text(self.current_lang, "area_m")
      self.t_perimeter = get_text(self.current_lang, "perimeter_m")
    else:
      self.t_area = get_text(self.current_lang, "area_ft")
      self.t_perimeter = get_text(self.current_lang, "perimeter_ft")

  def calculate(self):
    try:
      raw_area = float(self.ids.input_area.text)
      raw_perimeter = float(self.ids.input_perimeter.text)

      if self.current_unit == "imperial":
        area = raw_area / 10.7639
        perimeter = raw_perimeter / 3.28084
      else:
        area = raw_area
        perimeter = raw_perimeter

      results = calculate_drywall_materials(area, perimeter)
      if results:
        est_height_label = get_text(self.current_lang, "est_height")
        est_height_val = results["Estimated Height"]
        if self.current_unit == "imperial":
          est_height_val = round(est_height_val * 3.28084, 2)
          height_unit = "ft"
        else:
          height_unit = "m"

        text = f"{est_height_label}: {est_height_val} {height_unit}\n\n"

        key_mapping = {
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
          if k != "Estimated Height":
            translated_key = get_text(self.current_lang, key_mapping.get(k, ""))
            if k == "Paper Tape (m)" and self.current_unit == "imperial":
              v = round(v * 3.28084, 2)
              unit_label = "ft"
            elif k == "Paper Tape (m)":
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