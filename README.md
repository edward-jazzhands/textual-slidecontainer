# textual-slidecontainer

![badge](https://img.shields.io/badge/linted-Ruff-blue?style=for-the-badge&logo=ruff)
![badge](https://img.shields.io/badge/formatted-black-black?style=for-the-badge)
![badge](https://img.shields.io/badge/type_checked-MyPy-blue?style=for-the-badge&logo=python)
![badge](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)
![badge](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fedward-jazzhands%2Ftextual-slidecontainer%2Frefs%2Fheads%2Fmaster%2Fpyproject.toml&style=for-the-badge)

This is a library that provides a custom container (widget) called the SlideContainer.

It is designed to make it extremely simple to implement a sliding menu bar in yor [Textual](https://github.com/Textualize/textual) apps.

## Features

- Usage is a single line of code with the default settings. Everything is handled automatically.
- Set the direction - Containers can slide to the left, right, top, or bottom, independently of where they are on the screen.
- Enable or disable Floating mode - With a simple boolean, containers can switch between floating on top of your app, or being a part of it and affecting the layout.
- Set the default state - Containers can be set to start in closed mode.
- Set the container to dock as an initialization argument.
- Floating containers automatically dock to the edge they move towards (this can be changed).
- Change how the animation looks with the duration, fade, and easing_function arguments.
- Included demo application which has comments in the code.

## Documentation

### [Click here for documentation](https://edward-jazzhands.github.io/libraries/textual-slidecontainer/)

## Questions, issues, suggestions?

Feel free to post an issue.

## Gif

![textual-slidecontainer](https://github.com/user-attachments/assets/aec1fa21-2994-40e7-9c02-e22b299b837a)
