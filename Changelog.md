# Changelog

## 0.5.0 (2025-06-17) - Better positioning features

- Breaking Change: The `dock_direction` argument has been removed and replaced with a new `dock_position` argument. The dock_position argument now allows for direct positioning of the SlideContainer in more specific locations:
    topleft, top, topright
    left, right
    bottomleft, bottom, bottomright
This makes it significantly easier to make SlideContainers of variable height (no longer need to be 1fr). Previously it was a headache to get them aligned in a specific location, this makes it easy.
- New feature: added arguments `offset_x` and `offset_y` to the SlideContainer. These will override the dock positioning when set, so that it's possible to dial in absolute values if desired.
- Breaking Change: The `InitClosed` message was renamed to `InitCompleted` because it's now called regardless of starting closed or not.
- Added a new `set_slide_direction` method. This makes it possible to change the slide direction while the program is running. It's a bit silly, but why not.
- Updated the demo to show off some of the new features.

## 0.4.2 (2025-06-14)

- Modified the SlideContainer so now it will always set display to False when it is closed. This will prevent anything in the container from being focused while it is closed, which is what most people will expect. Previously it was not doing this behavior consistently.
- Moved TCSS for demo app from CSS block in App class to demostyles.tcss
- Modified demo to allow cycling focus with Tab, which makes it more obvious what setting display to False on the containers is actually doing.

## 0.4.1

- `on_mount` method was renamed to `_on_mount` to avoid conflicting with people making their own on_mount method

## 0.4.0

- Added `open` and `close` methods to the container to improve API.
- Changed layering so each container is on its own layer.
- Enhanced type hinting: Package now passes MyPy and Pyright in strict mode.
- Added py.typed file to mark package as typed for Pyright/MyPy.
- Changed animations to use self.animate's `on_complete` argument (more idiomatic).
- Added error checking for valid easing functions.
- Moved the widget to slidecontainer.py for better package organization.
- Added Ruff, Black, and MyPy to project dev dependencies, and set all of them to run automatically using the justfile before publishing.
- Added URLs and metadata to pyproject.toml file.
- Modified demo to show that all 3 methods of adding children can be used - the context manager (with: command), passing a list of widgets, and making a custom SlideContainer with a compose method.
- Made demo look a bit prettier with a center RichLog widget. Also refactored some of the demo app code to make it shorter and cleaner.

## 0.3.3

- Also changed easing_function argument to string Literal for type hinting
- Added `control` property for the messages so that a selector can be used.

## 0.3.1

- Changed slide_direction and dock_direction arguments to Literals to improve type hinting.

## 0.3.0

- Added a `SlideCompleted` message to the container. This will be sent when the container is finished sliding and contains the state of the slide (True = open, False = closed) as well as a reference to the slide container.
- Added a notification to the demo to show off the SlideCompleted message.
- `FinishedLoading` message was renamed to `InitClosed` to make it more obvious that it's only sent when initialized in the closed position.
- Lowered required Python version down to 3.8.1 and added `from __future__ import annotations` to improve compatibility.

## 0.2.5

- First public release
