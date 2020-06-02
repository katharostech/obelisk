class Position:
    """A component with an `x` and a `y` position"""

    def __init__(self, x, y):
        """Create a position with a specified `x` and `y`"""
        
        self.x = x
        self.y = y

class Size:
    """A component with a width and a height"""

    def __init__(self, width, height):
        """Create a size with the specified height and width"""
        
        self.width = width
        self.height = height


class Image:
    """A component used to create an image that will be rendered on the screen"""

    def __init__(self, source):
        """
        Create a new image given the path to the imaage file.

        Note that in order to be rendered, the entity must also have a `Position` and
        a `Size` component.
        """
        
        self.source = source

class InputEvent:
    """Marker component added to all input events"""
    pass

class KeyDown:
    """A component that indicates a key that has been pressed down"""

    def __init__(self, key, scancode, codepoint, modifier):
        self.key = key
        self.scancode = scancode
        self.codepoint = codepoint
        self.modifier = modifier

class KeyUp:
    """A component that indicates a key has been released"""

    def __init__(self, key, scancode):
        self.key = key
        self.scancode = scancode
