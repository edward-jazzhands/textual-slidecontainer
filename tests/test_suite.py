from pathlib import Path
from textual_slidecontainer import SlideContainer
from textual_slidecontainer.demo import SlideContainerDemo

DEMO_DIR = Path(__file__).parent.parent / "src" / "textual_slidecontainer"
TERINAL_SIZE = (110, 36)

async def test_launch():  
    """Test launching the SlideContainerDemo app."""
    app = SlideContainerDemo()
    async with app.run_test() as pilot:
        await pilot.pause()
        await pilot.exit(None) 

async def test_sliding_state():  
    """Test sliding containers open and close with key bindings."""
    app = SlideContainerDemo()
    async with app.run_test() as pilot:  

        assert app.query_one("#top_slidecontainer", SlideContainer).state is True
        await pilot.press("ctrl+w")  
        await pilot.wait_for_animation()
        assert app.query_one("#top_slidecontainer", SlideContainer).state is False

        assert app.query_one("#left_slidecontainer", SlideContainer).state is True
        await pilot.press("ctrl+a")  
        await pilot.wait_for_animation()
        assert app.query_one("#left_slidecontainer", SlideContainer).state is False

        assert app.query_one("#bottom_slidecontainer", SlideContainer).state is False
        await pilot.press("ctrl+s")  
        await pilot.wait_for_animation()
        assert app.query_one("#bottom_slidecontainer", SlideContainer).state is True

        assert app.query_one("#right_slidecontainer", SlideContainer).state is False
        await pilot.press("ctrl+d")  
        await pilot.wait_for_animation()
        assert app.query_one("#right_slidecontainer", SlideContainer).state is True    

def test_snapshot_only_left(snap_compare):

    async def run_before(pilot) -> None:
        await pilot.press("ctrl+a")  
        await pilot.wait_for_animation()

    assert snap_compare(
        DEMO_DIR / "demo.py",
        terminal_size=TERINAL_SIZE,
        run_before=run_before,
    )         
    
def test_snapshot_only_right(snap_compare):

    async def run_before(pilot) -> None:
        await pilot.press("ctrl+d")  
        await pilot.wait_for_animation()

    assert snap_compare(
        DEMO_DIR / "demo.py",
        terminal_size=TERINAL_SIZE,
        run_before=run_before,
    )         
    
def test_snapshot_left_and_right(snap_compare):

    async def run_before(pilot) -> None:
        await pilot.press("ctrl+a")  
        await pilot.press("ctrl+d")  
        await pilot.wait_for_animation()

    assert snap_compare(
        DEMO_DIR / "demo.py",
        terminal_size=TERINAL_SIZE,
        run_before=run_before,
    )         

def test_snapshot_top_and_bottom(snap_compare):

    async def run_before(pilot) -> None:
        await pilot.press("ctrl+w")  
        await pilot.press("ctrl+s")  
        await pilot.wait_for_animation()

    assert snap_compare(
        DEMO_DIR / "demo.py",
        terminal_size=TERINAL_SIZE,
        run_before=run_before,
    )             

def test_snapshot_all(snap_compare):

    async def run_before(pilot) -> None:
        await pilot.press("ctrl+w")  
        await pilot.press("ctrl+s")
        await pilot.press("ctrl+a")  
        await pilot.press("ctrl+d")          
        await pilot.wait_for_animation()

    assert snap_compare(
        DEMO_DIR / "demo.py",
        terminal_size=TERINAL_SIZE,
        run_before=run_before,
    )       