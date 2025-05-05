# Changelog

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
