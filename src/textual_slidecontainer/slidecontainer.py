"Module for the SlideContainer widget for Textual."

# ~ Type Checking (Pyright and MyPy) - Strict Mode
# ~ Linting - Ruff
# ~ Formatting - Black - max 110 characters / line

from __future__ import annotations
from typing import Literal, get_args

# from typing_extensions import Protocol  # You may need to install typing_extensions

# Textual imports
from textual.containers import Container
from textual.geometry import Offset
from textual.reactive import reactive
from textual.message import Message
from textual.widget import Widget

SLIDE_DIRECTION = Literal["left", "right", "up", "down"]
DOCK_DIRECTION = Literal["left", "right", "top", "bottom", "none"]
EASING_FUNC = Literal[
    "none",
    "round",
    "linear",
    "in_sine",
    "in_out_sine",
    "out_sine",
    "in_quad",
    "in_out_quad",
    "out_quad",
    "in_cubic",
    "in_out_cubic",
    "out_cubic",
    "in_quart",
    "in_out_quart",
    "out_quart",
    "in_quint",
    "in_out_quint",
    "out_quint",
    "in_expo",
    "in_out_expo",
    "out_expo",
    "in_circ",
    "in_out_circ",
    "out_circ",
    "in_back",
    "in_out_back",
    "out_back",
    "in_elastic",
    "in_out_elastic",
    "out_elastic",
    "in_bounce",
    "in_out_bounce",
    "out_bounce",
]


class SlideContainer(Container):
    """See init for usage and information."""

    class InitClosed(Message):
        """Message sent when the container is ready.
        This is only sent if the container is starting closed."""

        def __init__(self, container: SlideContainer) -> None:
            super().__init__()
            self.container = container
            """The container that is ready."""

        @property
        def control(self) -> SlideContainer:
            """The SlideContainer that sent the message."""
            return self.container

    class SlideCompleted(Message):
        """Message sent when the container is opened or closed.
        This is sent after the animation is complete."""

        def __init__(self, state: bool, container: SlideContainer) -> None:
            super().__init__()
            self.state = state
            """The state of the container.  \n True = container open, False = container closed."""
            self.container = container
            """The container that has finished sliding."""

        @property
        def control(self) -> SlideContainer:
            """The SlideContainer that sent the message."""
            return self.container

    state: reactive[bool] = reactive[bool](True)
    """State of the container.  \n True = container open, False = container closed.   
    You can set this directly, or you can use the toggle() method."""

    _current_layer: int = 0

    def __init__(
        self,
        *children: Widget,
        slide_direction: SLIDE_DIRECTION,
        floating: bool = True,
        start_open: bool = True,
        fade: bool = False,
        dock_direction: DOCK_DIRECTION = "none",
        duration: float = 0.8,
        easing_function: EASING_FUNC = "out_cubic",
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        """Construct a Sliding Container widget.

        Args:
            *children: Child widgets.
            slide_direction: Can be "left", "right", "up", or "down".
                NOTE: This is not tied to position or dock direction. Feel free to experiment.
            floating: Whether the container should float overtop on its own layer.
            start_open: Whether the container should start open(visible) or closed(hidden).
            fade: Whether to also fade the container when it slides.
            dock_direction: The direction to dock the container to. Can be "left", "right", "top", "bottom", "none".
                NOTE: When floating is True, this is automatically set to the same direction
                as the slide direction. (up = top, down = bottom, left = left, right = right)
                Floating SlideContainers MUST be docked to a direction. However, you can change the dock direction.
                The dock direction does not need to be the same as the slide direction.
            duration: The duration of the slide animation in seconds.
            easing_function: The easing function to use for the animation.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes for the widget.
            disabled: Whether the widget is disabled or not.
        """
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

        if slide_direction not in get_args(SLIDE_DIRECTION):
            raise ValueError("slide_direction must be one of 'left', 'right', 'up', or 'down'.")
        if dock_direction not in get_args(DOCK_DIRECTION):
            raise ValueError("dock_direction must be one of 'left', 'right', 'top', 'bottom', or 'none'.")
        if easing_function not in get_args(EASING_FUNC):
            raise ValueError(
                "easing_function must be one of the allowed functions. See the Textual docs for more info."
            )

        self.slide_direction = slide_direction
        self.floating = floating
        self.set_reactive(SlideContainer.state, start_open)  # need to handle this manually
        self.fade = fade
        self.duration = duration
        self.easing_function = easing_function

        self.layer_index = SlideContainer._current_layer
        SlideContainer._current_layer += 1  # increment the class variable for the next window's layer

        if self.floating:

            # This is the layer system, it is the trick that puts each SlideContainer on its own layer.
            # Using the _current_layer class variable, we can keep track of the next available layer.
            # '_' denotes textual built-in layers. We want to skip those. Textual handles them
            # behind the scenes, and we don't want to mess with them.
            current_layers = self.app.screen.layers
            if f"sliding_container{self.layer_index}" not in current_layers:
                layers = [layer for layer in current_layers if not layer.startswith("_")]
                layers.extend([f"sliding_container{self.layer_index}"])  # add our new layer
                self.app.screen.styles.layers = tuple(layers)  # type: ignore
            self.styles.layer = "sliding_containers"
            #! type: ignore from: (Tuple size mismatch; expected 1 but received indeterminate)
            # I have no idea how to fix it. Driving me nuts. This is the only ignore I have in the whole library.

            if dock_direction == "none":  # NOTE: If floating, then it must be docked *somewhere*.
                if slide_direction == "left":
                    dock_direction = "left"
                elif slide_direction == "right":
                    dock_direction = "right"
                elif slide_direction == "up":
                    dock_direction = "top"
                elif slide_direction == "down":
                    dock_direction = "bottom"

            if start_open is False:
                self.styles.opacity = 0.0

        self.styles.dock = dock_direction  # default is "none" - but only if floating is False.

    def on_mount(self) -> None:
        self.call_after_refresh(self.init_closed_state)

    def init_closed_state(self) -> None:

        if self.state is False:  # This means the container is starting closed.

            if self.slide_direction == "left":
                self.styles.offset = Offset(-(self.size.width + self.get_spacing()), 0)
            elif self.slide_direction == "right":
                self.styles.offset = Offset(self.size.width + self.get_spacing(), 0)
            elif self.slide_direction == "up":
                self.styles.offset = Offset(0, -(self.size.height + self.get_spacing()))
            elif self.slide_direction == "down":
                self.styles.offset = Offset(0, self.size.height + self.get_spacing())

            if not self.floating:
                self.display = False  # If not floating, hide the container to allow layout to change.
            else:
                if self.fade is False:  # if it is floating, it was set to 0 opacity earlier.
                    self.styles.opacity = 1.0  #  Must change back.

        self.post_message(self.InitClosed(self))  # Notify that the container is ready.

    def watch_state(self, old_state: bool, new_state: bool) -> None:
        if new_state == old_state:
            return
        if new_state is True:
            self._slide_open()
        else:
            self._slide_closed()

    def get_spacing(self) -> int:

        if self.slide_direction in ["left", "right"]:
            return self.styles.border.spacing.left + self.styles.border.spacing.right
        elif self.slide_direction in ["up", "down"]:
            return self.styles.border.spacing.top + self.styles.border.spacing.bottom
        else:
            raise ValueError("Invalid slide direction. Must be one of 'left', 'right', 'up', or 'down'.")

    def _slide_open(self) -> None:

        # This is here just in case anyone calls this method manually:
        if self.state is not True:
            self.set_reactive(SlideContainer.state, True)  # set state without calling the watcher

        def slide_open_completed() -> None:
            self.post_message(self.SlideCompleted(True, self))

        # if not self.floating:
        self.display = True
        self.animate(
            "offset",
            Offset(0, 0),
            duration=self.duration,
            easing=self.easing_function,
            on_complete=slide_open_completed,
        )
        if self.fade:
            self.styles.animate(
                "opacity", value=1.0, duration=self.duration, easing=self.easing_function
            )  # reset to original opacity

    def _slide_closed(self) -> None:

        # This is here just in case anyone calls this method manually:
        if self.state is not False:
            self.set_reactive(SlideContainer.state, False)  # set state without calling the watcher

        def slide_closed_completed() -> None:
            if not self.floating:
                self.display = False
            self.post_message(self.SlideCompleted(False, self))

        if self.slide_direction == "left":
            self.animate(
                "offset",
                Offset(-(self.size.width + self.get_spacing()), 0),
                duration=self.duration,
                easing=self.easing_function,
                on_complete=slide_closed_completed,
            )
        elif self.slide_direction == "right":
            self.animate(
                "offset",
                Offset(self.size.width + self.get_spacing(), 0),
                duration=self.duration,
                easing=self.easing_function,
                on_complete=slide_closed_completed,
            )
        elif self.slide_direction == "up":
            self.animate(
                "offset",
                Offset(0, -(self.size.height + self.get_spacing())),
                duration=self.duration,
                easing=self.easing_function,
                on_complete=slide_closed_completed,
            )
        elif self.slide_direction == "down":
            self.animate(
                "offset",
                Offset(0, self.size.height + self.get_spacing()),
                duration=self.duration,
                easing=self.easing_function,
                on_complete=slide_closed_completed,
            )

        # NOTE: The offsets use self.animate, while the opacity uses self.styles.animate.
        # The reason is because self.offset is a setter method on the Widget class that provides
        # a shortcut to the styles.offset property and generates an Offset object from a tuple.
        # Trying to use styles.animate("offset", ...) would not work. I'm not entirely sure why,
        # but simply using the setter method on the widget does work. Presumably that's why it
        # was even added to the Widget class in the first place.

        if self.fade:
            self.styles.animate("opacity", value=0.0, duration=self.duration, easing=self.easing_function)

    ##################
    # ~ Public API ~ #
    ##################

    def open(self) -> None:
        "Open the container. This is the same as setting state to True."
        self.state = True

    def close(self) -> None:
        "Close the container. This is the same as setting state to False."
        self.state = False

    def toggle(self) -> None:
        "Toggle the state of the container. Opens or closes the container."
        self.state = not self.state
