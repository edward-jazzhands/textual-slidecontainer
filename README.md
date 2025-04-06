# textual-slidecontainer

![textual-slidecontainer](https://github.com/user-attachments/assets/aec1fa21-2994-40e7-9c02-e22b299b837a)

This is a library that provides a custom container (widget) called the SlideContainer.

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

Install with:

```sh
pip install textual-slidecontainer
```

Import into your project with:

```py
from textual_slidecontainer import SlideContainer
```

## Demo app

You can instantly try out the demo app using uv or pipx:

```sh
uvx textual-slidecontainer
```

```sh
pipx textual-slidecontainer
```

Or if you have it downloaded into your python environment, just run it using the entry script:

```sh
textual-slidecontainer
```

For uv users:

```sh
uv run textual-slidecontainer
```

## Usage

Most basic usage.:

```py
from textual_slidecontainer import SlideContainer

def compose(self):
    with SlideContainer(id = "my_slidecontainer", slide_direction = "up"):
        yield Static("Your widgets here")
```

Set the container's width and height in CSS as you usually would. Note that the above example will dock to the top of your screen automatically because it is in floating mode (floating is the default).

Many people will want it to start closed / hidden. Simply set the default state to False:

```py
def compose(self):
    with SlideContainer(
        id = "my_slidecontainer", slide_direction = "left", default_state = False      
    ):
        yield Static("Your widgets here")
```

You can keep it docked to the top, but change the slight direction:

```py
def compose(self):
    with SlideContainer(
        id = "my_slidecontainer", slide_direction = "right", dock_direction = "top"       
    ):
        yield Static("Your widgets here")
```

Here's an example using all the arguments:

```py
with SlideContainer(
    classes = "my_container_classes",
    id = "my_slidecontainer",
    default_state = False        # False = closed
    slide_direction = "left",
    dock_direction = "top",      # dock to the top but slide left
    floating = False,            # default is True
    fade = True,
    duration = 0.6,                   # the default is 0.8     
    easing_function = "out_cubic",    # default is the same as Textual's default: "in_out_cubic".                           
):
    yield Static("Your widgets here")
```

Here's a demonstration of it being used in a full app:

```py
from textual.app import App
from textual import on
from textual.widgets import Static, Footer, Button
from textual.containers import Container

from textual_slidecontainer import SlideContainer

class TextualApp(App):

    DEFAULT_CSS = """
    #my_container {
        width: 1fr; height: 1fr; border: solid red;
        align: center middle; content-align: center middle;
    }
    Static { border: solid blue; width: 1fr;}
    SlideContainer {
        width: 25; height: 1fr;
        background: $panel; align: center middle;
    }
    """
    def compose(self):

        with SlideContainer(slide_direction="left", default_state=False):
            yield Static("This is content in the slide container.")
        with Container(id="my_container"):
            yield Button("Show/Hide slide container", id="toggle_slide")
        yield Footer()

    @on(Button.Pressed, "#toggle_slide")
    def toggle_slide(self) -> None:
        self.query_one(SlideContainer).toggle()

TextualApp().run()
```

## Questions, issues, suggestions?

Feel free to post an issue.
