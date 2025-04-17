"""Contains the demo app."""
from __future__ import annotations
from typing import cast

# Textual imports
from textual.app import App
from textual import on
from textual.binding import Binding
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Horizontal, Container

from textual_slidecontainer import SlideContainer

class SlideContainerDemo(App):

    DEFAULT_CSS = """
    .slidecontainer { background: $panel; align: center middle;
        &.leftright {width: 24; height: 1fr; background: $surface;}
        &.topbottom {width: 1fr; height: 6;}
    }
    #right_slidecontainer {border: heavy blue;}    # This demonstrates how it can handle borders fine.
    .top_docked {dock: top;}         
    .bottom_docked {dock: bottom;}  # These are not used for the SlidingContainer
    .right_docked {dock: right;}    # Its just styling for the demo app.
    .left_docked {dock: left;}
    .w_1fr {width: 1fr;}
    .h_1fr {height: 1fr;}

    #main_content {align: center middle; border: heavy red;}
    Static {width: auto;}
    """

    BINDINGS = [
        Binding("ctrl+w", "toggle_top_slidecontainer", "Top menu"),        
        Binding("ctrl+a", "toggle_left_slidecontainer", "Left menu"),
        Binding("ctrl+s", "toggle_bottom_slidecontainer", "Bottom menu"),          
        Binding("ctrl+d", "toggle_right_slidecontainer", "Right menu"),
    ]

    def compose(self):
    
        yield Header(name="Textual-SlideContainer Demo")

        self.main_container = Container(id="main_container")
        self.main_container.styles.opacity = 0.0        # madlad loading screen
        with self.main_container:

            with SlideContainer(
                classes = "slidecontainer topbottom",
                id = "top_slidecontainer",
                slide_direction = "up",
                floating = False,       # Note this is True by default
                fade = True,            # and this is False by default
            ):
                yield Button("Hide", id="button_top")
                yield Static(
                    "Fade is [yellow]on.[/yellow] "
                    "Default is [yellow]open.[/yellow] "
                    "Menu is [red]not floating."
                )

            with Horizontal(id="horizontal_container"):
                with SlideContainer(
                    classes = "slidecontainer leftright",
                    id = "left_slidecontainer",
                    slide_direction = "left", 
                    floating = False,
                    duration = 1.0,                    # <-- you can change the animation duration.
                    easing_function = "out_cubic",     # <-- you can change the easing function.                            
                ):
                    yield Button("Hide", id="button_left")
                    yield Static(
                        "Fade is [red]off.[/red]\n"
                        "Default is [yellow]open.[/yellow]\n"
                        "Menu is [red]not floating."
                    )

                with Container(id="main_content"):
                    yield Static("This is content at the top left.",
                                 classes="top_docked")
                    yield Static("This is content \non the right \nthat can get blocked.",
                                 classes="right_docked")
                    yield Static("This is the main content. \n"
                                "Try expanding / collapsing the menus \nwith the key bindings")
                    yield Static("This is content at the bottom that can get blocked by the floating menu.",
                                 classes="bottom_docked w_1fr")

                with SlideContainer(                        
                    classes = "slidecontainer leftright",   
                    id = "right_slidecontainer",             # Floating mode is the default.
                    slide_direction = "right",      # When floating, It'll auto-dock to the same direction.        
                    start_open = False,
                    fade=True,
                ):
                    yield Button("Hide", id="button_right")
                    yield Static(
                        "Fade is [yellow]on.[/yellow]\n"
                        "Default is [red]closed.[/red]\n"
                        "Menu is [yellow]floating."
                    )
                    
            with SlideContainer(
                classes = "slidecontainer topbottom",     # Dock direction does not have to be the same
                id = "bottom_slidecontainer",         #  as the slide direction.
                slide_direction = "right",      # <-  Try changing this to left or down. (up works but it'll look weird.)
                dock_direction = "bottom",            
                start_open = False,
            ):
                yield Button("Hide", id="button_bottom")
                yield Static(
                    "Fade is [red]off.[/red] "
                    "Default is [yellow]closed.[/yellow] "
                    "Menu is [yellow]floating."
                )   

        yield Footer()
        
    def on_mount(self):

        for item in ["left", "right", "top", "bottom"]:         # this is for aesthetic reasons.
            self.query_one(f"#button_{item}").can_focus = False  # there's bindings set, no need to cycle focus.

    @on(SlideContainer.InitClosed)
    def finished_loading(self):
        """This is a madlad way of making a loading screen. The main container starts
        at opacity 0.0 and fades in to 1.0 when the slidecontainer is done loading."""
        
        self.main_container.styles.animate("opacity", value=1.0, duration=0.3)
        # self.main_container.styles.opacity = 1.0     # this would be the simpler way of doing it.

    @on(SlideContainer.SlideCompleted)
    def slide_completed(self, event: SlideContainer.SlideCompleted):

        self.notify(f"Slide completed: {event.container}: {event.state}")

    #### ACTIONS ###

    def action_toggle_left_slidecontainer(self):
        """Toggle the slidecontainer open and closed."""
        slidecontainer = cast(SlideContainer, self.query_one("#left_slidecontainer"))
        slidecontainer.toggle()

    def action_toggle_right_slidecontainer(self):
        """Toggle the slidecontainer open and closed."""
        slidecontainer = cast(SlideContainer, self.query_one("#right_slidecontainer"))
        slidecontainer.toggle()

    def action_toggle_top_slidecontainer(self):
        """Toggle the slidecontainer open and closed."""
        slidecontainer = cast(SlideContainer, self.query_one("#top_slidecontainer"))
        slidecontainer.toggle()

    def action_toggle_bottom_slidecontainer(self):
        """Toggle the slidecontainer open and closed."""
        slidecontainer = cast(SlideContainer, self.query_one("#bottom_slidecontainer"))
        slidecontainer.toggle()

    #### BUTTONS ####

    @on(Button.Pressed, selector="#button_left")
    def left_slidecontainer_button(self):
        """Toggle the left slidecontainer open and closed."""
        self.action_toggle_left_slidecontainer()
        
    @on(Button.Pressed, selector="#button_right")
    def right_slidecontainer_button(self):
        """Toggle the right slidecontainer open and closed."""
        self.action_toggle_right_slidecontainer()   

    @on(Button.Pressed, selector="#button_top")
    def top_slidecontainer_button(self):
        """Toggle the top slidecontainer open and closed."""
        self.action_toggle_top_slidecontainer()

    @on(Button.Pressed, selector="#button_bottom")
    def bottom_slidecontainer_button(self):
        """Toggle the bottom slidecontainer open and closed."""
        self.action_toggle_bottom_slidecontainer()     


def run_demo():
    SlideContainerDemo().run()

if __name__ == "__main__":
    run_demo()