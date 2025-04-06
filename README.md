# textual-slidecontainer

![textual-slidecontainer](https://github.com/user-attachments/assets/aec1fa21-2994-40e7-9c02-e22b299b837a)

This is a library that provides a custom Container (widget) called the SlideContainer.

It is designed to make it extremely simple to implement a sliding menu bar in yor Textual apps.

## Features

- Usage is a single line of code with the default settings. Everything is handled automatically.
- Set the direction - Containers can slide to the left, right, top, or bottom, independently of where they are on the screen.
- Enable or disable Floating mode - With a simple boolean, containers can switch between floating on top of your app, or being a part of it and affecting the layout.
- Set the default state - Containers can be set to start in closed mode.
- Fade in/out - Containers can be set to fade while they slide
- Set the container to dock as an initialization argument.
- Floating containers automatically dock to the edge they move towards (this can be changed).
- Change how the animation looks with the duration and easing_function arguments.
- Included demo application which has comments in the code.

## Installation

```sh
pip install textual-slidecontainer
```
