"""
Pide Turtle Backend - A turtle graphics implementation that outputs drawing commands.

This module provides a turtle graphics API compatible with Python's standard turtle module,
but instead of drawing to a Tk window, it outputs JSON commands that can be rendered
by the Pide graphics panel.
"""

import json
import math
import sys
import time

# Global state
_turtles = []
_screen = None


def _emit(cmd):
    """Emit a drawing command as JSON to stdout."""
    print(f"__PIDE_TURTLE__:{json.dumps(cmd)}", flush=True)


class Vec2:
    """Simple 2D vector."""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Turtle:
    """Turtle graphics cursor."""

    def __init__(self):
        self._pos = Vec2(0, 0)
        self._heading = 90  # degrees, 0 = east, 90 = north
        self._pen_down = True
        self._pen_color = "black"
        self._fill_color = "black"
        self._pen_size = 1
        self._visible = True
        self._speed_val = 6
        self._filling = False
        self._fill_points = []
        _turtles.append(self)
        _emit({"type": "turtle_create", "id": id(self)})
        self._update_turtle()

    def _delay(self):
        """Sleep based on speed() so animation is visible. 0=no delay, 1=slowest, 10=fast."""
        if 1 <= self._speed_val <= 10:
            # ~0.12s at 1, ~0.01s at 10
            time.sleep(0.13 - 0.012 * self._speed_val)

    def _update_turtle(self):
        """Send turtle state update."""
        _emit({
            "type": "turtle_update",
            "id": id(self),
            "x": self._pos.x,
            "y": self._pos.y,
            "heading": self._heading,
            "visible": self._visible,
            "pen_color": self._pen_color,
        })

    def forward(self, distance):
        """Move forward by distance pixels."""
        rad = math.radians(self._heading)
        new_x = self._pos.x + distance * math.cos(rad)
        new_y = self._pos.y + distance * math.sin(rad)

        if self._pen_down:
            _emit({
                "type": "line",
                "x1": self._pos.x,
                "y1": self._pos.y,
                "x2": new_x,
                "y2": new_y,
                "color": self._pen_color,
                "width": self._pen_size,
            })

        self._pos.x = new_x
        self._pos.y = new_y

        if self._filling:
            self._fill_points.append((new_x, new_y))

        self._update_turtle()
        self._delay()

    fd = forward

    def backward(self, distance):
        """Move backward by distance pixels."""
        self.forward(-distance)

    bk = backward
    back = backward

    def right(self, angle):
        """Turn right by angle degrees."""
        self._heading -= angle
        self._update_turtle()
        self._delay()

    rt = right

    def left(self, angle):
        """Turn left by angle degrees."""
        self._heading += angle
        self._update_turtle()
        self._delay()

    lt = left

    def goto(self, x, y=None):
        """Move to absolute position."""
        if y is None:
            x, y = x

        if self._pen_down:
            _emit({
                "type": "line",
                "x1": self._pos.x,
                "y1": self._pos.y,
                "x2": x,
                "y2": y,
                "color": self._pen_color,
                "width": self._pen_size,
            })

        self._pos.x = x
        self._pos.y = y

        if self._filling:
            self._fill_points.append((x, y))

        self._update_turtle()
        self._delay()

    setpos = goto
    setposition = goto

    def setx(self, x):
        """Set x coordinate."""
        self.goto(x, self._pos.y)

    def sety(self, y):
        """Set y coordinate."""
        self.goto(self._pos.x, y)

    def setheading(self, angle):
        """Set heading to angle degrees."""
        self._heading = angle
        self._update_turtle()
        self._delay()

    seth = setheading

    def home(self):
        """Move to origin and reset heading."""
        self.goto(0, 0)
        self.setheading(90)

    def circle(self, radius, extent=360, steps=None):
        """Draw a circle or arc."""
        if steps is None:
            steps = max(int(abs(extent) / 3), 20)

        step_angle = extent / steps
        step_length = 2 * math.pi * radius * abs(extent) / 360 / steps

        for _ in range(steps):
            self.forward(step_length)
            if extent > 0:
                self.left(step_angle)
            else:
                self.right(-step_angle)

    def dot(self, size=None, color=None):
        """Draw a dot."""
        if size is None:
            size = max(self._pen_size + 4, 2 * self._pen_size)
        if color is None:
            color = self._pen_color

        _emit({
            "type": "dot",
            "x": self._pos.x,
            "y": self._pos.y,
            "size": size,
            "color": color,
        })
        self._delay()

    def stamp(self):
        """Stamp turtle shape (simplified as triangle)."""
        _emit({
            "type": "stamp",
            "x": self._pos.x,
            "y": self._pos.y,
            "heading": self._heading,
            "color": self._pen_color,
        })
        self._delay()

    def penup(self):
        """Lift pen up."""
        self._pen_down = False

    pu = penup
    up = penup

    def pendown(self):
        """Put pen down."""
        self._pen_down = True

    pd = pendown
    down = pendown

    def isdown(self):
        """Return True if pen is down."""
        return self._pen_down

    def pensize(self, width=None):
        """Set or return pen width."""
        if width is None:
            return self._pen_size
        self._pen_size = width

    width = pensize

    def pencolor(self, *args):
        """Set or return pen color."""
        if not args:
            return self._pen_color
        if len(args) == 1:
            self._pen_color = args[0]
        elif len(args) == 3:
            r, g, b = args
            if isinstance(r, float):
                r, g, b = int(r * 255), int(g * 255), int(b * 255)
            self._pen_color = f"#{r:02x}{g:02x}{b:02x}"

    def fillcolor(self, *args):
        """Set or return fill color."""
        if not args:
            return self._fill_color
        if len(args) == 1:
            self._fill_color = args[0]
        elif len(args) == 3:
            r, g, b = args
            if isinstance(r, float):
                r, g, b = int(r * 255), int(g * 255), int(b * 255)
            self._fill_color = f"#{r:02x}{g:02x}{b:02x}"

    def color(self, *args):
        """Set pen and fill color."""
        if not args:
            return self._pen_color, self._fill_color
        if len(args) == 1:
            self._pen_color = args[0]
            self._fill_color = args[0]
        elif len(args) == 2:
            self._pen_color = args[0]
            self._fill_color = args[1]

    def begin_fill(self):
        """Begin filling a shape."""
        self._filling = True
        self._fill_points = [(self._pos.x, self._pos.y)]

    def end_fill(self):
        """End filling and draw filled shape."""
        if self._filling and len(self._fill_points) > 2:
            _emit({
                "type": "fill",
                "points": self._fill_points,
                "color": self._fill_color,
            })
        self._filling = False
        self._fill_points = []

    def filling(self):
        """Return True if currently filling."""
        return self._filling

    def hideturtle(self):
        """Hide the turtle."""
        self._visible = False
        self._update_turtle()

    ht = hideturtle

    def showturtle(self):
        """Show the turtle."""
        self._visible = True
        self._update_turtle()

    st = showturtle

    def isvisible(self):
        """Return True if turtle is visible."""
        return self._visible

    def speed(self, speed=None):
        """Set or return speed (ignored in this backend, but API compatible)."""
        if speed is None:
            return self._speed_val
        self._speed_val = speed

    def position(self):
        """Return current position."""
        return (self._pos.x, self._pos.y)

    pos = position

    def xcor(self):
        """Return x coordinate."""
        return self._pos.x

    def ycor(self):
        """Return y coordinate."""
        return self._pos.y

    def heading(self):
        """Return current heading."""
        return self._heading

    def distance(self, x, y=None):
        """Return distance to point."""
        if y is None:
            x, y = x
        return math.sqrt((x - self._pos.x) ** 2 + (y - self._pos.y) ** 2)

    def towards(self, x, y=None):
        """Return angle towards point."""
        if y is None:
            x, y = x
        return math.degrees(math.atan2(y - self._pos.y, x - self._pos.x))

    def write(self, text, move=False, align="left", font=("Arial", 8, "normal")):
        """Write text at current position."""
        _emit({
            "type": "text",
            "x": self._pos.x,
            "y": self._pos.y,
            "text": str(text),
            "align": align,
            "font": font[0],
            "size": font[1],
            "color": self._pen_color,
        })


class Screen:
    """Turtle graphics screen."""

    def __init__(self):
        self._bgcolor = "white"
        self._title = "Pide Turtle Graphics"

    def bgcolor(self, color=None):
        """Set or return background color."""
        if color is None:
            return self._bgcolor
        self._bgcolor = color
        _emit({"type": "bgcolor", "color": color})

    def clear(self):
        """Clear the screen."""
        _emit({"type": "clear"})

    def reset(self):
        """Reset the screen."""
        _emit({"type": "reset"})

    def title(self, text):
        """Set window title (no-op in embedded mode)."""
        self._title = text

    def setup(self, width=None, height=None, startx=None, starty=None):
        """Setup screen size (no-op in embedded mode)."""
        pass

    def screensize(self, canvwidth=None, canvheight=None, bg=None):
        """Set screen size (no-op in embedded mode)."""
        if bg:
            self.bgcolor(bg)

    def tracer(self, n=None, delay=None):
        """Set tracer (no-op in embedded mode)."""
        pass

    def update(self):
        """Update screen (no-op in embedded mode)."""
        pass

    def bye(self):
        """Close the screen."""
        _emit({"type": "done"})

    def exitonclick(self):
        """Wait for click then exit (simplified)."""
        _emit({"type": "done"})

    def mainloop(self):
        """Enter main loop (no-op)."""
        _emit({"type": "done"})

    done = mainloop


# Module-level functions that create/use default turtle
_default_turtle = None


def _get_default_turtle():
    global _default_turtle
    if _default_turtle is None:
        _default_turtle = Turtle()
    return _default_turtle


def _get_screen():
    global _screen
    if _screen is None:
        _screen = Screen()
    return _screen


# Turtle movement
def forward(distance): _get_default_turtle().forward(distance)
def fd(distance): _get_default_turtle().forward(distance)
def backward(distance): _get_default_turtle().backward(distance)
def bk(distance): _get_default_turtle().backward(distance)
def back(distance): _get_default_turtle().backward(distance)
def right(angle): _get_default_turtle().right(angle)
def rt(angle): _get_default_turtle().right(angle)
def left(angle): _get_default_turtle().left(angle)
def lt(angle): _get_default_turtle().left(angle)
def goto(x, y=None): _get_default_turtle().goto(x, y)
def setpos(x, y=None): _get_default_turtle().goto(x, y)
def setposition(x, y=None): _get_default_turtle().goto(x, y)
def setx(x): _get_default_turtle().setx(x)
def sety(y): _get_default_turtle().sety(y)
def setheading(angle): _get_default_turtle().setheading(angle)
def seth(angle): _get_default_turtle().setheading(angle)
def home(): _get_default_turtle().home()
def circle(radius, extent=360, steps=None): _get_default_turtle().circle(radius, extent, steps)
def dot(size=None, color=None): _get_default_turtle().dot(size, color)
def stamp(): _get_default_turtle().stamp()

# Pen control
def penup(): _get_default_turtle().penup()
def pu(): _get_default_turtle().penup()
def up(): _get_default_turtle().penup()
def pendown(): _get_default_turtle().pendown()
def pd(): _get_default_turtle().pendown()
def down(): _get_default_turtle().pendown()
def isdown(): return _get_default_turtle().isdown()
def pensize(width=None): return _get_default_turtle().pensize(width)
def width(w=None): return _get_default_turtle().pensize(w)
def pencolor(*args): return _get_default_turtle().pencolor(*args)
def fillcolor(*args): return _get_default_turtle().fillcolor(*args)
def color(*args): return _get_default_turtle().color(*args)
def begin_fill(): _get_default_turtle().begin_fill()
def end_fill(): _get_default_turtle().end_fill()
def filling(): return _get_default_turtle().filling()

# Turtle state
def hideturtle(): _get_default_turtle().hideturtle()
def ht(): _get_default_turtle().hideturtle()
def showturtle(): _get_default_turtle().showturtle()
def st(): _get_default_turtle().showturtle()
def isvisible(): return _get_default_turtle().isvisible()
def speed(s=None): return _get_default_turtle().speed(s)
def position(): return _get_default_turtle().position()
def pos(): return _get_default_turtle().position()
def xcor(): return _get_default_turtle().xcor()
def ycor(): return _get_default_turtle().ycor()
def heading(): return _get_default_turtle().heading()
def distance(x, y=None): return _get_default_turtle().distance(x, y)
def towards(x, y=None): return _get_default_turtle().towards(x, y)
def write(text, move=False, align="left", font=("Arial", 8, "normal")):
    _get_default_turtle().write(text, move, align, font)

# Screen functions
def bgcolor(color=None): return _get_screen().bgcolor(color)
def clear(): _get_screen().clear()
def reset(): _get_screen().reset()
def title(text): _get_screen().title(text)
def setup(width=None, height=None, startx=None, starty=None):
    _get_screen().setup(width, height, startx, starty)
def screensize(canvwidth=None, canvheight=None, bg=None):
    _get_screen().screensize(canvwidth, canvheight, bg)
def tracer(n=None, delay=None): _get_screen().tracer(n, delay)
def update(): _get_screen().update()
def bye(): _get_screen().bye()
def exitonclick(): _get_screen().exitonclick()
def mainloop(): _get_screen().mainloop()
def done(): _get_screen().done()

# Alias
Screen = Screen
