import sublime
import sublime_plugin

class ColorSchemesCategorizeCommand(sublime_plugin.WindowCommand):
  SUBLIME_PREF = 'Preferences.sublime-settings'
  PANEL = 'color_scheme_categorizer_panel'

  def run(self, category):
    self.current = sublime.load_settings(self.SUBLIME_PREF).get('color_scheme')
    self.schemes = []

    all_schemes = self.collect_all_schemes()
    temp_view = self.window.create_output_panel(self.PANEL, unlisted=True)

    for (name, path) in all_schemes:
      background = self.find_background(temp_view, path)
      is_dark = self.is_dark(background)
      append = is_dark if category == "dark" else not is_dark
      if append:
        self.schemes.append((name, path))

    self.window.destroy_output_panel(self.PANEL)

    self.window.show_quick_panel(
      [t[0] for t in self.schemes],
      self.on_done,
      on_highlight=self.on_highlight
    )

  def collect_all_schemes(self):
    scheme_paths = sublime.find_resources("*.sublime-color-scheme")
    scheme_paths.extend(sublime.find_resources("*.tmTheme"))
    scheme_dict = { self.get_scheme_name(s): s for s in scheme_paths }
    schemes = [(k, v) for k, v in scheme_dict.items()]
    schemes.sort()
    return schemes

  def find_background(self, view, scheme_path):
    view.settings().set('color_scheme', scheme_path)
    return view.style()['background']

  # ChatGPT made this, I don't know how it works exactly.
  def is_dark(self, color):
    rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
    return luminance < 128

  def on_highlight(self, index):
    self.set_pref_scheme(self.schemes[index][1])

  def on_done(self, index):
    if index == -1:
      self.set_pref_scheme(self.current)
      return

    self.set_pref_scheme(self.schemes[index][1])

  def get_scheme_name(self, scheme_path):
    name_with_extension = scheme_path.split('/')[-1]
    name = name_with_extension.split('.')[0]
    return name

  def set_pref_scheme(self, path):
    sublime.load_settings(self.SUBLIME_PREF).set('color_scheme', path)
