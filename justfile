# Run the demo
run:
  uv run src/textual_slidecontainer/demo.py

# Run the demo in dev mode
run-dev:
  uv run textual run --dev textual_slidecontainer.demo:SlideContainerDemo

# Remove the build and dist directories
clean:
  rm -rf build dist
  find . -name "*.pyc" -delete

# Remove the virtual environment and lock file
del-env:
  rm -rf .venv
  rm -rf uv.lockjust

# Removes all environment and build stuff
reset: clean del-env
  echo "All environment and build stuff removed."

build: clean
  uv build

publish: build
  uv publish