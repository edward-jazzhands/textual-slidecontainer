"Package for the SlideContainer widget for Textual."
from __future__ import annotations
from typing import Literal
from textual.containers import Container
from textual.geometry import Offset
from textual.reactive import reactive
from textual.message import Message

slide_directions = Literal["left", "right", "up", "down"]
dock_directions = Literal["left", "right", "top", "bottom", "none"]

class SlideContainer(Container):
    """See init for usage and information."""

    class InitClosed(Message):
        """Message sent when the container is ready.   
        This is only sent if the container is starting closed."""
        def __init__(self, container: SlideContainer) -> None:
            super().__init__()
            self.container = container
            """The container that is ready."""

    class SlideCompleted(Message):
        """Message sent when the container is opened or closed.   
        This is sent after the animation is complete."""
        def __init__(self, state: bool, container: SlideContainer) -> None:
            super().__init__()
            self.state = state
            """The state of the container.  \n True = container open, False = container closed."""
            self.container = container
            """The container that has finished sliding."""        
        

    state: reactive[bool] = reactive(True)
    """State of the container.  \n True = container open, False = container closed.   
    You can set this directly, or you can use the toggle() method."""

    def toggle(self):
        "Toggle the state of the container. Opens or closes the container."
        self.state = not self.state   

    def __init__(
            self,
            slide_direction: slide_directions,
            *args,
            floating: bool = True,
            start_open: bool = True,
            fade: bool = False,
            dock_direction: dock_directions = "none",
            duration: float = 0.8,            
            easing_function: str = "out_cubic",
            **kwargs
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
                See https://textual.textualize.io/guide/animation/#easing-functions
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes for the widget.
            disabled: Whether the widget is disabled or not.
        """
        super().__init__(*args, **kwargs)

        if slide_direction not in ["left", "right", "up", "down"]:
            raise ValueError("slide_direction must be one of 'left', 'right', 'up', or 'down'.")
        if dock_direction not in ["left", "right", "top", "bottom", "none"]:
            raise ValueError("dock_direction must be one of 'left', 'right', 'top', 'bottom', or 'none'.")

        self.slide_direction = slide_direction
        self.floating = floating
        self.set_reactive(SlideContainer.state, start_open)  # need to handle this manually
        self.fade = fade
        self.duration = duration
        self.easing_function = easing_function

        if self.floating:

            current_layers = self.app.screen.layers
            if "sliding_containers" not in current_layers:
                layers = [layer for layer in current_layers if not layer.startswith("_")]
                new_layers = tuple(layers) + ("sliding_containers",)
                self.app.screen.styles.layers = new_layers  # type: ignore  |  Pylance complains but this is fine.
            self.styles.layer = "sliding_containers"

            if dock_direction == "none":                  # NOTE: If floating, then it must be docked *somewhere*.
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

        self.styles.dock = dock_direction     # default is "none" - but only if floating is False.

    def on_mount(self):
        if self.styles.border != "none":
            self.bo = 2
        self.call_after_refresh(self.init_closed_state)  

    def init_closed_state(self):

        if self.state is False:    # This means the container is starting closed.

            if self.slide_direction == "left":
                self.styles.offset = Offset(-(self.size.width+self.bo), 0)
            elif self.slide_direction == "right":
                self.styles.offset = Offset(self.size.width+self.bo, 0)
            elif self.slide_direction == "up":
                self.styles.offset = Offset(0, -(self.size.height+self.bo))           
            elif self.slide_direction == "down":
                self.styles.offset = Offset(0, self.size.height+self.bo)

            if not self.floating:
                self.display = False   # If not floating, hide the container to allow layout to change.
            else:                      
                if self.fade is False:      # if it is floating, it was set to 0 opacity earlier.
                    self.styles.opacity = 1.0     #  Must change back.

        self.post_message(self.InitClosed(self))  # Notify that the container is ready.

    def watch_state(self, old_state: bool, new_state: bool) -> None:
        if new_state == old_state:
            return
        if new_state is True:
            self._slide_open()
        else:
            self._slide_closed()

    def _slide_open(self):
        """Technically you can call this directly. It should be fine.   
        But you should use the toggle() method or set the state property instead."""

        # This is here in case anyone calls this method manually:
        if self.state is not True:
            self.set_reactive(SlideContainer.state, True)   # set state without calling the watcher
        
        # if not self.floating:
        self.display = True
        self.animate(
            "offset", Offset(0, 0),
            duration=self.duration, easing=self.easing_function
        )
        if self.fade:
            self.styles.animate(
                "opacity", value=1.0,
                duration=self.duration, easing=self.easing_function
            ) # reset to original opacity         

        self.set_timer(self.duration, lambda: self.post_message(self.SlideCompleted(True, self)))            
               
    def _slide_closed(self):
        """Technically you can call this directly. It should be fine.   
        But you should use the toggle() method or set the state property instead."""      

        # This is here in case anyone calls this method manually:
        if self.state is not False:
            self.set_reactive(SlideContainer.state, False)  # set state without calling the watcher          

        if self.slide_direction == "left":
            self.animate(
                "offset", Offset(-(self.size.width+self.bo), 0),
                duration=self.duration, easing=self.easing_function
            )
        elif self.slide_direction == "right":
            self.animate(
                "offset", Offset(self.size.width+self.bo, 0),
                duration=self.duration, easing=self.easing_function
            )
        elif self.slide_direction == "up":
            self.animate(
                "offset", Offset(0, -(self.size.height+self.bo)),
                duration=self.duration, easing=self.easing_function
            )            
        elif self.slide_direction == "down":
            self.animate(
                "offset", Offset(0, self.size.height+self.bo),
                duration=self.duration, easing=self.easing_function
            )            

        if self.fade:
            self.styles.animate(
                "opacity", value=0.0,
                duration=self.duration, easing=self.easing_function
            )
        if not self.floating:
            self.set_timer(self.duration, lambda: setattr(self, "display", False))

        self.set_timer(self.duration, lambda: self.post_message(self.SlideCompleted(False, self)))