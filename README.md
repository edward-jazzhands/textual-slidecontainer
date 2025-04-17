# textual-slidecontainer

![textual-slidecontainer](https://github.com/user-attachments/assets/aec1fa21-2994-40e7-9c02-e22b299b837a)

This is a library that provides a custom container (widget) called the SlideContainer.

It is designed to make it extremely simple to implement a sliding menu bar in yor [Textual](https://github.com/Textualize/textual) apps.

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

or for uv users:

```sh
uv add textual-slidecontainer
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

Or if you have it downloaded into your python environment, run it using the entry script:

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

If you'd like the container to start closed/hidden, simply set `start_open` to False:

```py
def compose(self):
    with SlideContainer(
        id = "my_slidecontainer", slide_direction = "left", start_open = False      
    ):
        yield Static("Your widgets here")
```

You can set the slide direction and dock direction to be different:

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
    start_open = False         
    slide_direction = "left",
    dock_direction = "top",      # dock to the top but slide left
    floating = False,            # default is True
    fade = True,
    duration = 0.6,                   # the default is 0.8     
    easing_function = "out_bounce",   # default is "out_cubic".                           
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
    #my_static { border: solid blue; width: 1fr;}
    SlideContainer {
        width: 25; height: 1fr;
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
- `InitClosed`

### SlideCompleted

This message will be posted every time that a slide is completed. This is useful if you need something to refresh every time the container slides open or closed (ie. refreshing elements on your screen affected by layout changes, or something inside the SlideContainer itself). It contains two attributes:

- `state`: bool - Whether it just slid open or closed.  
    True = open, False = closed.
- `container` - The container that did the sliding.

Example usage:

```py
from textual import on

@on(SlideContainer.SlideCompleted)
def my_slide_completed(self, event: SlideContainer.SlideCompleted):

    self.notify(f"Slide completed: {event.container}: {event.state}")

# OR using the other method:
def on_slide_container_slide_completed(self, event: SlideContainer.SlideCompleted):
    # handle your loading screen here.
```

### InitClosed

Because the container needs to know where it should be on the screen in open mode, starting in closed mode can sometimes reveal some graphical glitches that are tricky to deal with. In order to help solve this problem, the container provides an `InitClosed` message. This is only posted after the container has been mounted and moved to its closed position. It contains one attribute:

- `container` - The container that just initialized in the closed position.

```py
from textual import on

@on(SlideContainer.InitClosed)
def my_container_loaded(self, event: SlideContainer.InitClosed):
    self.log(f"Slide container initialized closed: {event.container}")
    # However you want to deal with your loading logic  here.

# OR using the other method:
def on_slide_container_init_closed(self, event: SlideContainer.InitClosed):
    # handle your loading logic  here.
```

You can see an example of this being used in the demo app.

## Questions, issues, suggestions?

Feel free to post an issue.
