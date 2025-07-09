<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/6cf8667e-cb64-435d-9c8e-67b3acb0e072">
  <img src="https://github.com/user-attachments/assets/c424f213-8fa8-4a97-9f0f-6d1fefdfd183">
</picture>

# textual-slidecontainer

![badge](https://img.shields.io/badge/linted-Ruff-blue?style=for-the-badge&logo=ruff)
![badge](https://img.shields.io/badge/formatted-black-black?style=for-the-badge)
![badge](https://img.shields.io/badge/type_checked-MyPy-blue?style=for-the-badge&logo=python)
![badge](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

This is a library that provides a custom container (widget) called the SlideContainer.

It is designed to make it extremely simple to implement sliding menu bars in your [Textual](https://github.com/Textualize/textual) apps.

## Features

- Usage is a single line of code with the default settings. Everything is handled automatically.
- Set a precise dock position - The dock position argument adds topleft, topright, bottomleft, and bottomright to Textual's 4 arguments of top, bottom, left, and right for 8 dock positions total.
- Set the slide direction - Containers can slide to the left, right, top, or bottom. This can be changed or tweaked independently of the dock position (For example, dock to bottom right, then you can slide down or slide right.)
- Enable or disable Floating mode - With a boolean, containers can switch between floating on top of your app, or being a part of it and affecting the layout.
- Set the default state - Containers can be set to start in closed mode.
- Set the container to dock as an initialization argument.
- Floating containers automatically dock to the edge they move towards (this can be changed).
- Change how the animation looks with the duration, fade, and easing_function arguments.
- Included demo application which has comments in the code.

## Demo App

If you have uv or Pipx, you can immediately try the demo app:

```sh
uvx textual-slidecontainer
```

```sh
pipx run textual-pyfiglet
```

## Documentation

### [Click here for documentation](https://edward-jazzhands.github.io/libraries/textual-slidecontainer/)

## Questions, issues, suggestions?

Feel free to post an issue.

## Video

https://github.com/user-attachments/assets/0c96a18f-958d-421b-950d-e0c303e774d9
