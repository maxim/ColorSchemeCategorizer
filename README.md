# Color Scheme Categorizer

List light and dark color schemes in Sublime Text separately. Uses a luminance calculation on theme background color to auto-determine the type of color scheme.

## Usage

2 new commands are added to the command palette:

1. UI: Select Color Scheme: Light
2. UI: Select Color Scheme: Dark

## Installation

Find Color Scheme Categorizer in Package Control.

## Changelog

### 1.0.0

- Schemes that share a name across packages no longer get merged into one arbitrary entry ([#1](https://github.com/maxim/ColorSchemeCategorizer/issues/1)). E.g. with LSP installed, picking Celeste could set LSP's partial `Celeste.sublime-color-scheme` instead of the built-in one. Schemes are now listed and set the same way Sublime's own "UI: Select Color Scheme" does.
- The list looks like Sublime's own picker too: each scheme shows its package underneath, and the current scheme has a ✓ and is preselected.
- Your choice is now saved to Preferences, so it survives a restart.
- Legacy color schemes are hidden unless `show_legacy_color_schemes` is on, same as in Sublime's picker.
- Scheme names with dots (e.g. "Solarized v1.2") are no longer cut off.

### 0.0.1

- Initial release.

## License

Copyright 2024 Max Chernyak

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
