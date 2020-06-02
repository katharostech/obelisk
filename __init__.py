# Kivy for windoing, graphics, and input
import kivy
kivy.require('1.1.1')
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.vertex_instructions import Rectangle

# The esper entity component system
from . import esper

# Our core Obelisk components
from .components import *

class GameWidget(Widget):
    """The main and only widget that goes into the game app and handles rendering"""
    
    def __init__(self, world, **kwargs):
        """Initialize the game widget, taking the esper world as an argment"""

        super(GameWidget, self).__init__(**kwargs)

        self.world = world
 
    def update(self):
        """
        Update the game rendering.

        This will look through the esper world for components related to rendering and
        update the apps render view with the information from the world's components.
        """

        # Clear the canvas
        # TODO: Find a more efficient way to do this than clearing the canvas every frame
        # that attempts to keep references to commands that only need to be changed and not
        # completely recreated every frame.
        self.canvas.clear()

        # Add the render commands
        for entid, (pos, size, image) in self.world.get_components(Position, Size, Image):
            with self.canvas:
                Rectangle(pos=[pos.x, pos.y], size=[size.width, size.height], source=image.source)

class GraphicsProcessor(esper.Processor):
    """Esper processor responsible for rendering the graphics"""

    def __init__(self, game_widget):
        # Run our parent's init
        super(GraphicsProcessor, self).__init__()

        # Set the game widget 
        self.game_widget = game_widget

    def process(self, delta_time):
        self.game_widget.update()

class InputProcessor(esper.Processor):
    """Esper processor responsible for creating input entitities"""

    def __init__(self):
        super(InputProcessor, self).__init__()

        self.event_list = []

    def process(self, delta_time):
        for event in self.event_list:
            # Create a new event entity
            entity = self.world.create_entity()

            # Add the event component to the entity
            self.world.add_component(entity, event)

            # Add the input event marker component
            # ( used to clean up the input event entitites later )
            self.world.add_component(entity, InputEvent())

        self.event_list.clear()

    # Event listeners

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        self.event_list.append(KeyDown(key, scancode, codepoint, modifier))
    
    def on_key_up(self, window, key, scancode):
        self.event_list.append(KeyUp(key, scancode))

class InputCleanupProcessor(esper.Processor):
    """Processor to go and clean up event entities before the next process loop"""

    def process(self, delta_time):
        for entity, (_,) in self.world.get_components(InputEvent):
            self.world.delete_entity(entity)

class GameApp(App):
    """The Kivy app that contains the game creates the window, etc."""

    def __init__(self, world, game_widget, refresh_rate, **kwargs):
        """Initialize the app, taking the esper world and a game widget as an argument"""

        # Call our parent classes constructor
        super(GameApp, self).__init__(**kwargs)

        # Set the esper world
        self.world = world

        # And the game widget
        self.game_widget = game_widget

        # Set our refresh rate
        self.refresh_rate = refresh_rate

    # Build the user interface
    def build(self):
        # Process the world at 60 frames per second
        Clock.schedule_interval(self.world.process, 1.0 / self.refresh_rate)

        # Return the game widget so Kivy can add it to the window
        return self.game_widget

class Game:
    """
    An Obelisk game
    """

    def __init__(self, refresh_rate=60):
        """
        Creating a new Obelisk game will create an ECS world and set up the core systems in
        the world so you don't have to. Then you just have to add your own processors to the
        world.
        """

        # Create the esper world
        self.world = esper.World()
        
        # Create our game widget
        game_widget = GameWidget(self.world)

        # Create out input processor
        input_processor = InputProcessor()

        # Bind our event listeners to our input processor
        Window.bind(on_key_down=input_processor.on_key_down)
        Window.bind(on_key_up=input_processor.on_key_up)

        # Add our input processor to the world
        self.world.add_processor(input_processor, priority=-1000000)
        self.world.add_processor(InputCleanupProcessor(), priority=1000000)
        
        # Add the graphis processor to the world
        self.world.add_processor(GraphicsProcessor(game_widget), priority=1000000)

        # Create the game application ( but it won't display until we run() it )
        self.app = GameApp(self.world, game_widget, refresh_rate)

    def start(self):
        self.app.run()