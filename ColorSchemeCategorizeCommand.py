import os
from collections import namedtuple

import sublime
import sublime_plugin

# setting is the scheme's value for the color_scheme preference.
Scheme = namedtuple('Scheme', 'name package setting')

class ColorSchemesCategorizeCommand(sublime_plugin.WindowCommand):
  SUBLIME_PREF = 'Preferences.sublime-settings'
  PANEL = 'color_scheme_categorizer_panel'
  CURRENT_KIND = (sublime.KIND_ID_COLOR_GREENISH, '✓', 'Current')

  def run(self, category):
    self.prefs = sublime.load_settings(self.SUBLIME_PREF)
    self.current = self.prefs.get('color_scheme')
    self.schemes = []

    all_schemes = self.collect_all_schemes()
    temp_view = self.window.create_output_panel(self.PANEL, unlisted=True)

    for scheme in all_schemes:
      background = self.find_background(temp_view, scheme.setting)
      is_dark = self.is_dark(background)
      append = is_dark if category == "dark" else not is_dark
      if append:
        self.schemes.append(scheme)

    self.window.destroy_output_panel(self.PANEL)

    current = self.as_setting(self.current)
    items = []
    selected = -1
    for scheme in self.schemes:
      kind = sublime.KIND_AMBIGUOUS
      if scheme.setting == current:
        kind = self.CURRENT_KIND
        selected = len(items)
      items.append(sublime.QuickPanelItem(scheme.name, details=scheme.package, kind=kind))

    self.window.show_quick_panel(
      items,
      self.on_done,
      selected_index=selected,
      on_highlight=self.on_highlight
    )

  # Lists schemes the way Sublime's own "UI: Select Color Scheme" does:
  #
  # - Each .tmTheme is its own scheme, set by its full path.
  # - A .sublime-color-scheme is set by file name only, and Sublime merges all
  #   files with that name (e.g. LSP's Celeste.sublime-color-scheme just adds
  #   rules to the built-in Celeste). So each name is listed once, under the
  #   first package that has it, unless a .tmTheme already has that name.
  def collect_all_schemes(self):
    show_legacy = self.prefs.get('show_legacy_color_schemes', False)
    paths = []
    names = set()

    for path in sublime.find_resources('*.tmTheme'):
      paths.append(path)
      names.add(self.get_scheme_name(path))

    for path in sublime.find_resources('*.sublime-color-scheme'):
      name = self.get_scheme_name(path)
      if name not in names:
        names.add(name)
        paths.append(path)

    schemes = []
    for path in paths:
      package = os.path.dirname(path)[len('Packages/'):]
      if package == 'Color Scheme - Legacy' and not show_legacy:
        continue

      schemes.append(Scheme(self.get_scheme_name(path), package, self.as_setting(path)))

    schemes.sort()
    return schemes

  # The color_scheme value for a scheme path, as Sublime's own picker sets it.
  def as_setting(self, path):
    if path.endswith('.sublime-color-scheme'):
      return os.path.basename(path)
    return path

  def find_background(self, view, scheme):
    view.settings().set('color_scheme', scheme)
    return view.style()['background']

  # ChatGPT made this, I don't know how it works exactly.
  def is_dark(self, color):
    rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
    return luminance < 128

  def on_highlight(self, index):
    self.set_pref_scheme(self.schemes[index].setting)

  def on_done(self, index):
    if index == -1:
      self.set_pref_scheme(self.current)
    else:
      self.set_pref_scheme(self.schemes[index].setting)

    sublime.save_settings(self.SUBLIME_PREF)

  def get_scheme_name(self, scheme_path):
    return os.path.splitext(os.path.basename(scheme_path))[0]

  def set_pref_scheme(self, scheme):
    self.prefs.set('color_scheme', scheme)
