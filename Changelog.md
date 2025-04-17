# Changelog

## 0.3.1

- Changed slide_direction and dock_direction arguments to Literals to improve type hinting.

## 0.3.0

- Added a `SlideCompleted` message to the container. This will be sent when the container is finished sliding and contains the state of the slide (True = open, False = closed) as well as a reference to the slide container.
- Added a notification to the demo to show off the SlideCompleted message.
- `FinishedLoading` message was renamed to `InitClosed` to make it more obvious that it's only sent when initialized in the closed position.
- Lowered required Python version down to 3.8.1 and added `from __future__ import annotations` to improve compatibility.

## 0.2.5

- First public release
