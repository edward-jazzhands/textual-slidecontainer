# Textual-SlideContainer<br>Documentation and Guide

## Installation

```sh
pip install textual-slidecontainer
```

Or using uv:

```sh
uv add textual-slidecontainer
```

## Demo app

You can instantly try out the demo app using uv or pipx:

```sh
uvx textual-slidecontainer
```

```sh
pipx run textual-slidecontainer
```

Or if you have it downloaded into your python environment, run it using the entry script:

```sh
textual-slidecontainer
```

For uv users, after adding it to your environment:

```sh
uv run textual-slidecontainer
```

## Getting Started

Import into your project with:

```py
from textual_slidecontainer import SlideContainer
```

Here is an example of the most basic usage:

```py
from textual_slidecontainer import SlideContainer

def compose(self):
    with SlideContainer(id = "my_slidecontainer", slide_direction = "up"):
        yield Static("Your widgets here")
```

You can set the container's width and height in CSS as you usually would. Note that the above example will dock to the top of your screen automatically because it is in floating mode (floating is the default).

## Dock position

The container has a `dock_position` argument which adds 4 new dock positions to the base 4 of top, left, right, and bottom. The 8 possible dock positions are:

- topleft
- top
- topright
- left
- right
- bottomleft
- bottom
- bottomright

The slide direction and dock position can be changed independently. For example, you might set the dock position to "bottomright" and then set the slide direction to be either right or down.

```py
def compose(self):
    with SlideContainer(
        id = "my_slidecontainer", slide_direction = "bottom", dock_position = "bottomright"       
    ):
        yield Static("Your widgets here")
```

## Start closed / Hidden

If you'd like the container to start closed/hidden, simply set `start_open` to False:

```py
def compose(self):
    with SlideContainer(
        id = "my_slidecontainer", slide_direction = "left", start_open = False      
    ):
        yield Static("Your widgets here")
```

## All Arguments

Here's an example using all the arguments:

```py
with SlideContainer(
    classes = "my_container_classes",
    id = "my_slidecontainer",
    start_open = False,         
    slide_direction = "down",
    dock_position = "bottomleft",  
    floating = False,                 # default is True
    fade = True,
    duration = 0.6,                   # the default is 0.8     
    easing_function = "out_bounce"    # default is "out_cubic".                           
):
    yield Static("Your widgets here")
```

## Ways of Making the Container

You can also use the other Textual methods of using a container: passing in a list of children, or making a custom class that inherits from SlideContainer.

Passing in a list of children (the normal Textual syntax):

```py
window_widgets: list[Widget] = [
    Button("Label", id="button_foo"),
    Static("Your widgets here")
]
yield SlideContainer(*window_widgets)
```

You can just as easily define everything you want in a custom container (again, the normal Textual syntax):

```py
class MySlideContainer(SlideContainer):

    def __init__(self):
        super().__init__(
            slide_direction="top",
            start_open=False,
            id="your_slidecontainer"
        )

    def compose(self):
        yield Button("Label", id="button_foo")
        yield Static("Your widgets here")
```

## Full demonstration

Here's a full demonstration of it being used in a small app. You can copy and paste this code.

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
    #my_static { border: solid blue; width: 1fr;}
    SlideContainer {
        width: 25; height: 75%;
        background: $panel; align: center middle;
    }
    """
    def compose(self):

        # The container will start closed / hidden:
        with SlideContainer(slide_direction="left", start_open=False):
            yield Static("This is content in the slide container", id="my_static")
        with Container(id="my_container"):
            yield Button("Show/Hide slide container", id="toggle_slide")
        yield Footer()

    @on(Button.Pressed, "#toggle_slide")
    def toggle_slide(self) -> None:
        self.query_one(SlideContainer).toggle()

TextualApp().run()
```

Check out the [source code of the demo app](https://github.com/edward-jazzhands/textual-slidecontainer/blob/master/src/textual_slidecontainer/demo.py) to see a more in-depth example.

## Messages

The SlideContainer posts two messages:

- `SlideCompleted`
- `InitCompleted`

### SlideCompleted

This message will be posted every time that a slide is completed. This is useful if you need something to refresh every time the container slides open or closed (ie. refreshing elements on your screen affected by layout changes, or something inside the SlideContainer itself). It contains two attributes:

- `state`: bool - Whether it just slid open or closed.  
    True = open, False = closed.
- `container` - The container that did the sliding.

Example usage:

```py
from textual import on

@on(SlideContainer.SlideCompleted, "#my_container")    # Note the selector is optional.
def my_slide_completed(self, event: SlideContainer.SlideCompleted):

    self.notify(f"Slide completed: {event.container}: {event.state}")

# OR using the other method:
def on_slide_container_slide_completed(self, event: SlideContainer.SlideCompleted):
    # handle your loading screen here.
```

### InitCompleted

Because the container needs to know where it should be on the screen in open mode, starting in closed mode can sometimes reveal some graphical glitches that are tricky to deal with. In order to help solve this problem, the container provides an `InitCompleted` message. This is only posted after the container has been mounted and moved to its starting position. Note this message is sent regardless of whether the container starts closed, but its usefulness is most likely for the ones that do.

It contains one attribute:

- `container` - The container that just initialized.

```py
from textual import on

@on(SlideContainer.InitCompleted, "#my_container")    # Note the selector is optional.
def my_container_loaded(self, event: SlideContainer.InitCompleted):
    self.log(f"Slide container initialized: {event.container}")
    # However you want to deal with your loading logic  here.

# OR using the other method:
def on_slide_container_init_completed(self, event: SlideContainer.InitCompleted):
    # handle your loading logic  here.
```

You can see an example of this being used in the [demo app](https://github.com/edward-jazzhands/textual-slidecontainer/blob/master/src/textual_slidecontainer/demo.py).

## API Reference

You can find the full API reference on the [reference page](reference.md).
