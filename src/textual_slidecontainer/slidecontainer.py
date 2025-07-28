"Module for the SlideContainer widget for Textual."

# ~ Type Checking (Pyright and MyPy) - Strict Mode
# ~ Linting - Ruff
# ~ Formatting - Black - max 110 characters / line

from __future__ import annotations
from typing import Literal, get_args, cast
import asyncio

# Textual imports
from textual import work
from textual.containers import Container
from textual.geometry import Offset, Size
from textual.reactive import reactive
from textual.message import Message
from textual.widget import Widget
from textual._animator import Animatable
import textual.events as events

SLIDE_DIRECTION = Literal["left", "right", "up", "down"]
DOCK_POSITION = Literal[
    "topleft",
    "top",
    "topright",
    "left",
    "right",
    "bottomleft",
    "bottom",
    "bottomright",
    "none",
]

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

    class InitCompleted(Message):
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
        dock_position: DOCK_POSITION = "none",
        floating: bool = True,
        start_open: bool = True,
        fade: bool = False,
        offset_x: int = 0,
        offset_y: int = 0,
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
            slide_direction: Can be:
                - left
                - right
                - up
                - down
                NOTE: This is not tied to dock position. Feel free to experiment.
            dock_position: The position to dock the container. Can be:
                - topleft
                - top
                - topright
                - left
                - right
                - bottomleft
                - bottom
                - bottomright
                - none
                NOTE: When floating is True, this is automatically set to the same direction
                as the slide direction. (up = top, down = bottom, left = left, right = right)
                Floating SlideContainers MUST be docked to a direction. However, you can change the dock direction.
                The dock direction does not need to be the same as the slide direction.
            floating: Whether the container should float overtop on its own layer.
            start_open: Whether the container should start open(visible) or closed(hidden).
            fade: Whether to also fade the container when it slides.
            offset_x: The
            offset_y: The
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
        # if dock_direction not in get_args(DOCK_DIRECTION):
        #     raise ValueError("dock_direction must be one of 'left', 'right', 'top', 'bottom', or 'none'.")
        if dock_position not in get_args(DOCK_POSITION):
            raise ValueError(
                "dock_position must be one of 'topleft', 'top', 'topright', "
                "'left', 'right', 'bottomleft', 'bottom', 'bottomright', or 'none'."
            )

        if easing_function not in get_args(EASING_FUNC):
            raise ValueError(
                "easing_function must be one of the allowed functions. See the Textual docs for more info."
            )
        if slide_direction in ["left", "right"] and offset_x != 0:
            raise ValueError(
                "When slide_direction is 'left' or 'right', offset_x must be 0. "
                "Use offset_y to adjust the vertical position."
            )
        if slide_direction in ["up", "down"] and offset_y != 0:
            raise ValueError(
                "When slide_direction is 'up' or 'down', offset_y must be 0. "
                "Use offset_x to adjust the horizontal position."
            )

        self.slide_direction = str(slide_direction)
        self.floating = floating
        self.set_reactive(SlideContainer.state, start_open)  # need to handle this manually
        self.fade = fade
        self.dock_position = str(dock_position)  # default is "none" - but only if floating is False.
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset = Offset(offset_x, offset_y)  # set the initial offset
        self.duration = duration
        self.easing_function = easing_function

        self.layer_index = SlideContainer._current_layer
        SlideContainer._current_layer += 1  # increment the class variable for the next window's layer

        if self.floating:
            self.styles.layer = f"sliding_container{self.layer_index}"

            slide_dir_to_dock_pos: dict[str, str] = {
                "up": "top",
                "down": "bottom",
                "left": "left",
                "right": "right",
            }
            if dock_position == "none":  # NOTE: If floating, then it must be docked *somewhere*.
                self.dock_position = slide_dir_to_dock_pos[slide_direction]

        dock_pos_to_style_dock = {
            "topleft": "top",
            "top": "top",
            "topright": "right",  # note topright = right
            "left": "left",
            "right": "right",
            "bottomleft": "bottom",
            "bottom": "bottom",
            "bottomright": "right" if slide_direction in ["left", "right"] else "bottom",
            "none": "none",
        }

        # if starting closed, do a little visual trickery:
        if start_open is False:
            self.styles.opacity = 0.0

        self.styles.dock = dock_pos_to_style_dock[self.dock_position]

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

    def set_slide_direction(self, direction: str) -> None:
        """Set the slide direction of the container.

        Args:
            direction: The new slide direction. Must be one of 'left', 'right', 'up', or 'down'.
        """
        if direction not in get_args(SLIDE_DIRECTION):
            raise ValueError("slide_direction must be one of 'left', 'right', 'up', or 'down'.")
        self.slide_direction = direction
        if self.dock_position == "bottomright":
            current_dock = self.styles.dock
            if direction in ["up", "down"]:
                self.styles.dock = "bottom" if direction == "down" else "top"
            else:
                self.styles.dock = "right" if direction == "right" else "left"
            if self.styles.dock != current_dock:
                self.set_to_starting_position()

    #################
    # ~ Internals ~ #
    #################

    def _on_mount(self, event: events.Mount) -> None:
        super()._on_mount(event)
        self.set_to_starting_position()

    @work
    async def set_to_starting_position(self) -> None:

        offset_x, offset_y = await self._calculate_offsets()

        if self.state is False:  # This means the container is starting closed.

            if self.slide_direction == "left":
                self.styles.offset = Offset(-(self.size.width + self.get_spacing("horizontal")), offset_y)
            elif self.slide_direction == "right":
                self.styles.offset = Offset(self.size.width + self.get_spacing("horizontal"), offset_y)
            elif self.slide_direction == "up":
                self.styles.offset = Offset(offset_x, -(self.size.height + self.get_spacing("vertical")))
            elif self.slide_direction == "down":
                self.styles.offset = Offset(offset_x, self.size.height + self.get_spacing("vertical"))

            self.display = False
            self.styles.opacity = 1.0  #  Was set to 0 earlier. Must change back.

        else:  # This means the container is starting open.
            self.styles.offset = Offset(offset_x, offset_y)

        self.post_message(self.InitCompleted(self))  # Notify that the container is ready.

    async def watch_state(self, old_state: bool, new_state: bool) -> None:

        if new_state == old_state:
            return
        if new_state is True:
            await self._slide_open()
        else:
            await self._slide_closed()

    def get_spacing(self, direction: str) -> int:

        if direction == "horizontal":
            return self.styles.border.spacing.left + self.styles.border.spacing.right
        elif direction == "vertical":
            return self.styles.border.spacing.top + self.styles.border.spacing.bottom
        else:
            raise ValueError("Invalid direction for get_spacing func. Must be 'horizontal' or 'vertical'.")

    def _slide_open_completed(self) -> None:
        self.post_message(self.SlideCompleted(True, self))

    def _slide_closed_completed(self) -> None:
        self.display = False
        self.post_message(self.SlideCompleted(False, self))

    async def _slide_open(self) -> None:

        # This is here just in case anyone calls this method manually:
        if self.state is not True:
            self.set_reactive(SlideContainer.state, True)  # set state without calling the watcher

        self.display = True
        offset_x, offset_y = await self._calculate_offsets()

        self.animate(
            "offset",
            cast(Animatable, Offset(offset_x, offset_y)),
            duration=self.duration,
            easing=self.easing_function,
            on_complete=self._slide_open_completed,
        )
        if self.fade:
            self.styles.animate(
                "opacity", value=1.0, duration=self.duration, easing=self.easing_function
            )  # reset to original opacity

    async def _slide_closed(self) -> None:

        # This is here just in case anyone calls this method manually:
        if self.state is not False:
            self.set_reactive(SlideContainer.state, False)  # set state without calling the watcher

        offset_x, offset_y = await self._calculate_offsets()

        # NOTE: The casting to Animatable here is necessary because of an apparent mismatch
        # in type hiting between python versions. When type checking this file using python 3.9,
        # MyPy complains about Offset and says it is not an Animatable type.
        # This problem does not happen in python 

        if self.slide_direction == "left":
            self.animate(
                "offset",
                cast(Animatable, Offset(-(self.size.width + self.get_spacing("horizontal")), offset_y)),
                duration=self.duration,
                easing=self.easing_function,
                on_complete=self._slide_closed_completed,
            )
        elif self.slide_direction == "right":
            self.animate(
                "offset",
                cast(Animatable, Offset(self.size.width + self.get_spacing("horizontal"), offset_y)),
                duration=self.duration,
                easing=self.easing_function,
                on_complete=self._slide_closed_completed,
            )
        elif self.slide_direction == "up":
            self.animate(
                "offset",
                cast(Animatable, Offset(offset_x, -(self.size.height + self.get_spacing("vertical")))),
                duration=self.duration,
                easing=self.easing_function,
                on_complete=self._slide_closed_completed,
            )
        elif self.slide_direction == "down":
            self.animate(
                "offset",
                cast(Animatable, Offset(offset_x, self.size.height + self.get_spacing("vertical"))),
                duration=self.duration,
                easing=self.easing_function,
                on_complete=self._slide_closed_completed,
            )

        # NOTE: The offsets use self.animate, while the opacity uses self.styles.animate.
        # The reason is because self.offset is a setter method on the Widget class that provides
        # a shortcut to the styles.offset property and generates an Offset object from a tuple.
        # Trying to use styles.animate("offset", ...) would not work. I'm not entirely sure why,
        # but simply using the setter method on the widget does work. Presumably that's why it
        # was even added to the Widget class in the first place.

        if self.fade:
            self.styles.animate("opacity", value=0.0, duration=self.duration, easing=self.easing_function)

    async def _calculate_offsets(self) -> tuple[int, int]:
        """Returns the starting position of the window
        based on the parent size and starting position arguments."""

        # This check is to ensure that the size is set before calculating offsets.
        # It fixes a bug caused by setting display to false and then setting it back to true
        # a split second before the offsets are calculated.
        if self.size == Size(0, 0):
            await asyncio.sleep(0.01)
            await self._calculate_offsets()

        assert isinstance(self.parent, Widget)
        max_x, max_y = self.parent.size - self.size
        max_x = max_x - self.get_spacing("horizontal")
        max_y = max_y - self.get_spacing("vertical")

        if self.dock_position in ["left", "right"]:
            horizontal = 0
            vertical = max_y // 2
        elif self.dock_position in ["top", "bottom"]:
            horizontal = max_x // 2
            vertical = 0
        elif self.dock_position == "bottomright":
            if self.slide_direction in ["left", "right"]:  # will be docked to the right
                horizontal = 0
                vertical = max_y
            else:  # slide_direction in ["up", "down"],  will be docked to the bottom
                horizontal = max_x
                vertical = 0
        else:
            horizontal = 0
            vertical = 0

        x_to_return = self.offset_x if self.offset_x else horizontal
        y_to_return = self.offset_y if self.offset_y else vertical
        return x_to_return, y_to_return
