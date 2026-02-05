"""Main application window for Pide."""

import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplitter,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPlainTextEdit,
    QTextEdit,
    QTreeView,
    QPushButton,
    QLabel,
    QFrame,
    QFileDialog,
    QMessageBox,
    QFileSystemModel,
    QGraphicsView,
    QGraphicsScene,
)
from PySide6.QtCore import Qt, QProcess, QRegularExpression, QPointF, QTimer
from PySide6.QtGui import (
    QFont, QAction, QKeySequence, QKeyEvent, QMouseEvent, QTextCursor,
    QSyntaxHighlighter, QTextCharFormat, QColor, QPen, QBrush, QPainter,
    QPolygonF, QTransform, QShortcut,
)
import json
import math
import re

# Code directory (repo root / code) — demo/, turtle/, learn/ are in git
PIDE_HOME = Path(__file__).parent.parent / "code"


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Python syntax highlighter with beautiful color scheme."""

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Beautiful modern color scheme (inspired by One Dark Pro / VS Code Dark+)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#C678DD"))  # Purple for keywords
        keyword_format.setFontWeight(QFont.Bold)
        
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))  # Warm orange for strings
        
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#5C6370"))  # Muted gray for comments
        comment_format.setFontItalic(True)
        
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#D19A66"))  # Orange for numbers
        
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#61AFEF"))  # Blue for functions
        
        class_format = QTextCharFormat()
        class_format.setForeground(QColor("#E5C07B"))  # Yellow for classes
        class_format.setFontWeight(QFont.Bold)
        
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor("#56B6C2"))  # Cyan for builtins
        
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor("#ABB2BF"))  # Light gray for operators
        
        # Python keywords
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def", "del",
            "elif", "else", "except", "False", "finally", "for", "from", "global",
            "if", "import", "in", "is", "lambda", "None", "nonlocal", "not", "or",
            "pass", "raise", "return", "True", "try", "while", "with", "yield"
        ]
        
        # Python builtins
        builtins = [
            "abs", "all", "any", "ascii", "bin", "bool", "bytearray", "bytes",
            "callable", "chr", "classmethod", "compile", "complex", "delattr",
            "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter",
            "float", "format", "frozenset", "getattr", "globals", "hasattr",
            "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass",
            "iter", "len", "list", "locals", "map", "max", "memoryview", "min",
            "next", "object", "oct", "open", "ord", "pow", "print", "property",
            "range", "repr", "reversed", "round", "set", "setattr", "slice",
            "sorted", "staticmethod", "str", "sum", "super", "tuple", "type",
            "vars", "zip", "__import__"
        ]
        
        # Build highlighting rules
        self.highlighting_rules = []
        
        # Keywords
        for keyword in keywords:
            pattern = QRegularExpression(rf"\b{keyword}\b")
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Builtins
        for builtin in builtins:
            pattern = QRegularExpression(rf"\b{builtin}\b")
            self.highlighting_rules.append((pattern, builtin_format))
        
        # Classes (class ClassName)
        class_pattern = QRegularExpression(r'\bclass\s+(\w+)\s*[\(:]')
        self.highlighting_rules.append((class_pattern, class_format))
        
        # Functions (def function_name)
        function_pattern = QRegularExpression(r'\bdef\s+(\w+)\s*\(')
        self.highlighting_rules.append((function_pattern, function_format))
        
        # Strings (single and double quotes, triple quotes) - more accurate regex
        string_patterns = [
            QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'),  # Double quotes
            QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"),  # Single quotes
            QRegularExpression(r'""".*?"""', QRegularExpression.PatternOption.DotMatchesEverythingOption),  # Triple double quotes
            QRegularExpression(r"'''.*?'''", QRegularExpression.PatternOption.DotMatchesEverythingOption),  # Triple single quotes
        ]
        for pattern in string_patterns:
            self.highlighting_rules.append((pattern, string_format))
        
        # Comments
        comment_pattern = QRegularExpression(r'#.*$')
        self.highlighting_rules.append((comment_pattern, comment_format))
        
        # Numbers (integers and floats)
        number_pattern = QRegularExpression(r'\b\d+\.?\d*[eE]?[+-]?\d*\b')
        self.highlighting_rules.append((number_pattern, number_format))
        
        # Operators
        operator_pattern = QRegularExpression(r'[+\-*/%=<>!&|^~]+')
        self.highlighting_rules.append((operator_pattern, operator_format))

    def highlightBlock(self, text):
        """Apply syntax highlighting to a block of text."""
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            iterator = expression.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)


class Editor(QPlainTextEdit):
    """Code editor with syntax highlighting and smart indentation."""

    def __init__(self, font_size=13):
        super().__init__()
        font = QFont("Menlo, Monaco, Consolas, monospace", font_size)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        self._base_font_size = font_size
        self.setPlaceholderText("# Write your Python code here...")
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        
        # Enable undo/redo (enabled by default, but make sure)
        self.setUndoRedoEnabled(True)
        
        self.setPlainText('print("Hello, World!")\n')
        
        # Beautiful dark theme styling
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #282C34;
                color: #ABB2BF;
                border: none;
                padding: 10px;
                selection-background-color: #3E4451;
                selection-color: #FFFFFF;
            }
        """)
        
        # Enable syntax highlighting
        self.highlighter = PythonSyntaxHighlighter(self.document())
        
        # Set tab width to 4 spaces (Python standard)
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' '))
        
        # Track current line for highlighting
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.highlight_current_line()
    
    def set_font_size(self, size):
        """Set font size and update tab width."""
        self._base_font_size = size
        font = QFont("Menlo, Monaco, Consolas, monospace", size)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' '))

    def highlight_current_line(self):
        """Highlight the current line."""
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor("#2C313C")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        
        self.setExtraSelections(extra_selections)

    def keyPressEvent(self, event: QKeyEvent):
        """Handle key presses with smart indentation."""
        cursor = self.textCursor()
        
        # Handle Tab key - insert 4 spaces
        if event.key() == Qt.Key_Tab:
            cursor.insertText("    ")  # 4 spaces
            return
        
        # Handle Enter key - maintain indentation
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Get current line
            cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
            cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
            current_line = cursor.selectedText()
            
            # Calculate indentation
            indent = ""
            for char in current_line:
                if char == ' ':
                    indent += ' '
                elif char == '\t':
                    indent += '    '  # Convert tab to 4 spaces
                else:
                    break
            
            # Check if line ends with colon (needs extra indent)
            if current_line.rstrip().endswith(':'):
                indent += "    "
            
            # Insert newline with indentation
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.MoveOperation.EndOfLine)
            cursor.insertText("\n" + indent)
            return
        
        # Handle Backspace - smart unindent
        if event.key() == Qt.Key_Backspace:
            # If cursor is at start of line with only whitespace, unindent by 4 spaces
            cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
            cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
            line_text = cursor.selectedText()
            
            if line_text and line_text.strip() == "":
                # Line is only whitespace
                if len(line_text) >= 4 and line_text[:4] == "    ":
                    # Remove 4 spaces
                    cursor.clearSelection()
                    cursor.setPosition(cursor.position() + 4)
                    cursor.movePosition(QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.KeepAnchor)
                    cursor.removeSelectedText()
                    return
        
        # Default behavior for other keys
        super().keyPressEvent(event)


class Terminal(QPlainTextEdit):
    """Interactive terminal with input support."""

    def __init__(self, font_size=12):
        super().__init__()
        font = QFont("Menlo, Monaco, Consolas, monospace", font_size)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        self._base_font_size = font_size
        self.setPlaceholderText("Output will appear here...")
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #21252B;
                color: #ABB2BF;
                border: none;
                padding: 10px;
                selection-background-color: #3E4451;
                selection-color: #FFFFFF;
            }
        """)
        self.input_start_pos = 0
        self.process = None

    def set_process(self, process):
        """Set the process to send input to."""
        self.process = process

    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard input."""
        # Allow copy/paste/select all shortcuts regardless of cursor position
        modifiers = event.modifiers()
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            key = event.key()
            # Allow Ctrl+C (copy), Ctrl+A (select all), Ctrl+X (cut)
            if key == Qt.Key_C or key == Qt.Key_A or key == Qt.Key_X:
                super().keyPressEvent(event)
                return
            # Allow Ctrl+V (paste) but only at input position
            if key == Qt.Key_V:
                cursor = self.textCursor()
                if cursor.position() < self.input_start_pos:
                    cursor.setPosition(self.input_start_pos)
                    self.setTextCursor(cursor)
                super().keyPressEvent(event)
                return
        
        cursor = self.textCursor()
        current_pos = cursor.position()

        # Only allow editing at or after input_start_pos
        # But allow selection for copying (Shift+Arrow keys, etc.)
        if current_pos < self.input_start_pos:
            # If there's a selection or using Shift modifier (for selecting), allow it
            if cursor.hasSelection() or (modifiers & Qt.KeyboardModifier.ShiftModifier):
                super().keyPressEvent(event)
                return
            # Otherwise, move cursor to input position
            cursor.setPosition(self.input_start_pos)
            self.setTextCursor(cursor)
            return

        # Handle Enter key to send input
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.process and self.process.state() == QProcess.Running:
                # Get the input line (from input_start_pos to end)
                cursor.setPosition(self.input_start_pos)
                cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
                input_text = cursor.selectedText()
                
                # Send to process
                if input_text:
                    self.process.write((input_text + "\n").encode())
                
                # Move input position to end and add newline
                cursor.clearSelection()
                cursor.movePosition(QTextCursor.MoveOperation.End)
                cursor.insertText("\n")
                self.input_start_pos = cursor.position()
                self.setTextCursor(cursor)
            else:
                # If no process running, just add newline
                super().keyPressEvent(event)
        else:
            # Allow normal editing
            super().keyPressEvent(event)

    def appendPlainText(self, text: str):
        """Append text and update input position."""
        super().appendPlainText(text)
        # Update input position to end of text
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.input_start_pos = cursor.position()
        # Keep cursor at end for input
        self.setTextCursor(cursor)

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse clicks - allow selection for copying."""
        super().mousePressEvent(event)
        # Allow selection even before input_start_pos (for copying)
        # Only restrict cursor position if not selecting and it's a left click
        if event.button() == Qt.MouseButton.LeftButton:
            cursor = self.textCursor()
            if cursor.position() < self.input_start_pos and not cursor.hasSelection():
                cursor.setPosition(self.input_start_pos)
                self.setTextCursor(cursor)
    
    def contextMenuEvent(self, event):
        """Show context menu with copy/paste options."""
        # Use default context menu which includes copy/paste
        super().contextMenuEvent(event)

    def set_font_size(self, size):
        """Set font size."""
        self._base_font_size = size
        font = QFont("Menlo, Monaco, Consolas, monospace", size)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
    
    def clear(self):
        """Clear terminal and reset input position."""
        super().clear()
        self.input_start_pos = 0


class FileTree(QWidget):
    """Left sidebar with file tree."""

    file_selected = None  # Will be set as signal

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        label = QLabel("Files")
        label.setStyleSheet("""
            QLabel {
                color: #ABB2BF;
                font-weight: bold;
                font-size: 13px;
                padding: 8px 4px;
            }
        """)
        layout.addWidget(label)

        # File system model
        self.model = QFileSystemModel()
        self.model.setRootPath(str(PIDE_HOME))
        self.model.setNameFilters(["*.py"])
        self.model.setNameFilterDisables(False)

        # Tree view
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(str(PIDE_HOME)))
        self.tree.setHeaderHidden(True)
        # Hide size, type, date columns
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)
        self.tree.setAnimated(True)
        self.tree.doubleClicked.connect(self._on_double_click)
        self.tree.clicked.connect(self._on_single_click)
        
        # Track current file for highlighting
        self.current_file_path = None
        self.selected_file_path = None  # Track selected file/directory for new file creation
        
        # Beautiful styling for file tree
        self.tree.setStyleSheet("""
            QTreeView {
                background-color: #21252B;
                color: #ABB2BF;
                border: none;
                outline: none;
            }
            QTreeView::item {
                padding: 4px;
                border: none;
            }
            QTreeView::item:hover {
                background-color: #2C313C;
            }
            QTreeView::item:selected {
                background-color: #528CCF;
                color: #FFFFFF;
                font-weight: bold;
            }
            QTreeView::branch {
                background-color: #21252B;
            }
        """)

        layout.addWidget(self.tree)

        self.setMinimumWidth(150)
        self.setMaximumWidth(250)
        
        # Style the sidebar background
        self.setStyleSheet("""
            QWidget {
                background-color: #21252B;
            }
        """)

    def _on_single_click(self, index):
        """Track clicked file for new file creation."""
        path = self.model.filePath(index)
        if path.endswith(".py"):
            self.selected_file_path = path
        else:
            # If it's a directory, store it
            self.selected_file_path = path
    
    def _on_double_click(self, index):
        path = self.model.filePath(index)
        if path.endswith(".py"):
            if self.file_selected:
                self.file_selected(path)
    
    def highlight_file(self, file_path):
        """Highlight the currently open file in the tree."""
        if not file_path:
            self.current_file_path = None
            self.tree.clearSelection()
            return
        
        self.current_file_path = file_path
        file_index = self.model.index(file_path)
        
        if file_index.isValid():
            # Expand parent directories to make file visible
            parent = file_index.parent()
            while parent.isValid() and parent != self.tree.rootIndex():
                self.tree.expand(parent)
                parent = parent.parent()
            
            # Select and scroll to the file (selection will highlight it)
            selection_model = self.tree.selectionModel()
            selection_model.clearSelection()
            selection_model.setCurrentIndex(file_index, selection_model.SelectionFlag.SelectCurrent)
            self.tree.scrollTo(file_index, QTreeView.ScrollHint.EnsureVisible)


class TurtleCanvas(QGraphicsView):
    """Canvas for rendering turtle graphics."""

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QBrush(QColor("white")))
        self.setStyleSheet("border: none;")
        
        # Set alignment to center
        self.setAlignment(Qt.AlignCenter)
        
        # Set scene rect to a reasonable default size
        self.scene.setSceneRect(-400, -400, 800, 800)

        # Turtle state
        self.turtles = {}  # id -> (x, y, heading, visible, color)
        self._turtle_cursors = {}  # id -> QGraphicsPolygonItem (cursor triangle)

        # Flip Y axis (turtle uses math coordinates)
        self.setTransform(QTransform().scale(1, -1))
        
        # Track if we need to fit view
        self._auto_fit = True

    def _triangle_points(self, x, y, heading_deg, size=14):
        """Return 3 (x,y) points for turtle triangle; tip in heading direction."""
        rad = math.radians(heading_deg)
        c, s = math.cos(rad), math.sin(rad)
        # Local: tip (1,0), back (-1, -0.4), (-1, 0.4); scale by size/2
        h = size / 2
        return [
            (x + h * c, y + h * s),
            (x + h * (-c - 0.4 * s), y + h * (-s + 0.4 * c)),
            (x + h * (-c + 0.4 * s), y + h * (-s - 0.4 * c)),
        ]

    def _draw_turtle_cursor(self, x, y, heading, color):
        """Draw one turtle cursor triangle; returns the graphics item."""
        points = self._triangle_points(x, y, heading)
        polygon = QPolygonF([QPointF(a, b) for a, b in points])
        brush = QBrush(QColor(color))
        pen = QPen(QColor("black"))
        pen.setWidthF(0.5)
        item = self.scene.addPolygon(polygon, pen, brush)
        item.setZValue(1000)
        return item

    def clear(self):
        """Clear the canvas."""
        self.scene.clear()
        self.turtles = {}
        self._turtle_cursors = {}
        self.setBackgroundBrush(QBrush(QColor("white")))
        # Reset scene rect
        self.scene.setSceneRect(-400, -400, 800, 800)
        self._center_view()
    
    def _update_view(self):
        """Update view to fit all items and keep centered."""
        if self.scene.items():
            # Get bounding rect of all items
            rect = self.scene.itemsBoundingRect()
            # Add some padding
            rect.adjust(-50, -50, 50, 50)
            self.scene.setSceneRect(rect)
            # Fit view while maintaining aspect ratio
            self.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)
    
    def _center_view(self):
        """Center the view on the scene."""
        self._update_view()
    
    def resizeEvent(self, event):
        """Handle resize to keep view centered."""
        super().resizeEvent(event)
        if self._auto_fit:
            self._center_view()

    def set_bgcolor(self, color):
        """Set background color."""
        self.setBackgroundBrush(QBrush(QColor(color)))

    def draw_line(self, x1, y1, x2, y2, color, width):
        """Draw a line."""
        pen = QPen(QColor(color))
        pen.setWidthF(width)
        pen.setCapStyle(Qt.RoundCap)
        self.scene.addLine(x1, y1, x2, y2, pen)
        # Update view to include new line
        self._update_view()

    def draw_dot(self, x, y, size, color):
        """Draw a dot."""
        brush = QBrush(QColor(color))
        pen = QPen(Qt.NoPen)
        r = size / 2
        self.scene.addEllipse(x - r, y - r, size, size, pen, brush)
        # Update view to include new dot
        self._update_view()

    def draw_fill(self, points, color):
        """Draw a filled polygon."""
        polygon = QPolygonF([QPointF(x, y) for x, y in points])
        brush = QBrush(QColor(color))
        pen = QPen(Qt.NoPen)
        self.scene.addPolygon(polygon, pen, brush)
        # Update view to include new polygon
        self._update_view()

    def draw_text(self, x, y, text, color, font_name, font_size, align):
        """Draw text."""
        text_item = self.scene.addText(text)
        # Update view to include new text
        self._update_view()
        text_item.setDefaultTextColor(QColor(color))
        font = QFont(font_name, font_size)
        text_item.setFont(font)
        # Flip text back (since view is flipped)
        text_item.setTransform(QTransform().scale(1, -1))
        text_item.setPos(x, y)

    def update_turtle(self, turtle_id, x, y, heading, visible, color):
        """Update turtle position and draw cursor if visible."""
        self.turtles[turtle_id] = (x, y, heading, visible, color)
        if turtle_id in self._turtle_cursors:
            self.scene.removeItem(self._turtle_cursors[turtle_id])
            del self._turtle_cursors[turtle_id]
        if visible:
            self._turtle_cursors[turtle_id] = self._draw_turtle_cursor(x, y, heading, color)

    def draw_stamp(self, x, y, heading, color):
        """Draw a stamp (fixed triangle) at position."""
        points = self._triangle_points(x, y, heading, size=12)
        polygon = QPolygonF([QPointF(a, b) for a, b in points])
        brush = QBrush(QColor(color))
        pen = QPen(QColor("black"))
        pen.setWidthF(0.5)
        self.scene.addPolygon(polygon, pen, brush)
        self._update_view()

    def process_command(self, cmd):
        """Process a turtle drawing command."""
        cmd_type = cmd.get("type")

        if cmd_type == "line":
            self.draw_line(cmd["x1"], cmd["y1"], cmd["x2"], cmd["y2"],
                          cmd["color"], cmd["width"])
        elif cmd_type == "dot":
            self.draw_dot(cmd["x"], cmd["y"], cmd["size"], cmd["color"])
        elif cmd_type == "fill":
            self.draw_fill(cmd["points"], cmd["color"])
        elif cmd_type == "text":
            self.draw_text(cmd["x"], cmd["y"], cmd["text"], cmd["color"],
                          cmd["font"], cmd["size"], cmd["align"])
        elif cmd_type == "bgcolor":
            self.set_bgcolor(cmd["color"])
        elif cmd_type == "clear" or cmd_type == "reset":
            self.clear()
        elif cmd_type == "turtle_update":
            self.update_turtle(cmd["id"], cmd["x"], cmd["y"],
                              cmd["heading"], cmd["visible"], cmd["pen_color"])
        elif cmd_type == "stamp":
            self.draw_stamp(cmd["x"], cmd["y"], cmd["heading"], cmd["color"])
        elif cmd_type == "done":
            pass  # Program finished


class GraphicsPanel(QFrame):
    """Right panel for graphics output (PyTurtle/Pygame)."""

    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet("""
            QFrame {
                background-color: #21252B;
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QLabel("Graphics Output")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                color: #ABB2BF;
                font-size: 12px;
                padding: 6px;
                background-color: #282C34;
            }
        """)
        layout.addWidget(header)

        # Turtle canvas
        self.canvas = TurtleCanvas()
        layout.addWidget(self.canvas)

        self.setMinimumWidth(250)

    def clear(self):
        """Clear the graphics panel."""
        self.canvas.clear()

    def process_command(self, cmd):
        """Process a turtle drawing command."""
        self.canvas.process_command(cmd)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pide - Python IDE")
        self.setGeometry(100, 100, 1200, 700)
        
        # Font size management
        self.editor_font_size = 13
        self.terminal_font_size = 12
        
        # Beautiful dark theme for main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E2127;
            }
            QMenuBar {
                background-color: #282C34;
                color: #ABB2BF;
                border-bottom: 1px solid #3E4451;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 8px;
            }
            QMenuBar::item:selected {
                background-color: #3E4451;
            }
            QMenu {
                background-color: #282C34;
                color: #ABB2BF;
                border: 1px solid #3E4451;
            }
            QMenu::item:selected {
                background-color: #3E4451;
            }
            QSplitter::handle {
                background-color: #1E2127;
            }
            QSplitter::handle:horizontal {
                width: 2px;
            }
            QSplitter::handle:vertical {
                height: 2px;
            }
        """)

        self.process = None
        self.current_file = None
        self._uses_turtle = False
        self._stdout_buffer = ""
        self._setup_ui()
        self._setup_menu()
        self._setup_shortcuts()
        self._setup_autosave()
        self._update_title()

    def _setup_ui(self):
        # Main horizontal splitter
        main_splitter = QSplitter(Qt.Horizontal)

        # Left: File tree
        self.file_tree = FileTree()
        self.file_tree.file_selected = self._open_from_tree
        self.file_tree.selected_file_path = None  # Track selected file for new file creation
        main_splitter.addWidget(self.file_tree)

        # Center: Editor + Terminal (vertical split)
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)

        # Toolbar buttons
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(10, 8, 10, 8)
        toolbar.setSpacing(8)
        
        # New file button
        self.new_file_btn = QPushButton("📄 New")
        self.new_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #5C6370;
                color: #FFFFFF;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4E5565;
            }
            QPushButton:pressed {
                background-color: #3E4451;
            }
        """)
        self.new_file_btn.clicked.connect(self.new_file)
        toolbar.addWidget(self.new_file_btn)
        
        # Run button
        self.run_btn = QPushButton("▶ Run")
        self.run_btn.setStyleSheet("""
            QPushButton {
                background-color: #61AFEF;
                color: #FFFFFF;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 13px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #528CCF;
            }
            QPushButton:pressed {
                background-color: #3E7AB8;
            }
        """)
        self.run_btn.clicked.connect(self.run_code)
        toolbar.addWidget(self.run_btn)
        toolbar.addStretch()
        center_layout.addLayout(toolbar)

        # Editor/Terminal splitter
        editor_terminal_splitter = QSplitter(Qt.Vertical)
        self.editor = Editor(self.editor_font_size)
        self.terminal = Terminal(self.terminal_font_size)
        editor_terminal_splitter.addWidget(self.editor)
        editor_terminal_splitter.addWidget(self.terminal)
        editor_terminal_splitter.setSizes([400, 200])
        center_layout.addWidget(editor_terminal_splitter)

        main_splitter.addWidget(center_widget)

        # Right: Graphics panel
        self.graphics_panel = GraphicsPanel()
        main_splitter.addWidget(self.graphics_panel)

        # Set initial sizes
        main_splitter.setSizes([180, 600, 250])

        self.setCentralWidget(main_splitter)

    def _setup_menu(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Open...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")

        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.editor.undo)
        # Connect to document's undoAvailable signal to enable/disable action
        self.editor.document().undoAvailable.connect(undo_action.setEnabled)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.editor.redo)
        # Connect to document's redoAvailable signal to enable/disable action
        self.editor.document().redoAvailable.connect(redo_action.setEnabled)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.editor.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence.SelectAll)
        select_all_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_all_action)

        # View menu
        view_menu = menubar.addMenu("View")

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl+="))  # Ctrl+= or Ctrl+Plus
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))  # Ctrl+- or Ctrl+Minus
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)

        zoom_reset_action = QAction("Reset Zoom", self)
        zoom_reset_action.setShortcut(QKeySequence("Ctrl+0"))
        zoom_reset_action.triggered.connect(self.zoom_reset)
        view_menu.addAction(zoom_reset_action)

        # Run menu
        run_menu = menubar.addMenu("Run")

        run_action = QAction("Run", self)
        run_action.setShortcut(QKeySequence("Ctrl+R"))
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)

        stop_action = QAction("Stop", self)
        stop_action.setShortcut(QKeySequence("Ctrl+."))
        stop_action.triggered.connect(self.stop_code)
        run_menu.addAction(stop_action)

        run_menu.addSeparator()

        clear_output_action = QAction("Clear Output", self)
        clear_output_action.setShortcut(QKeySequence("Ctrl+K"))
        clear_output_action.triggered.connect(self.terminal.clear)
        run_menu.addAction(clear_output_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About Pide", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def _setup_shortcuts(self):
        """Setup global keyboard shortcuts for zoom."""
        # Zoom in: Ctrl/Cmd + Plus or Ctrl/Cmd + =
        # Note: On macOS, QKeySequence automatically maps Ctrl to Cmd
        zoom_in_equal = QShortcut(QKeySequence("Ctrl+="), self)
        zoom_in_equal.activated.connect(self.zoom_in)
        
        # Also support Ctrl/Cmd + Shift + = (which produces +)
        zoom_in_plus = QShortcut(QKeySequence("Ctrl++"), self)
        zoom_in_plus.activated.connect(self.zoom_in)
        
        # Zoom out: Ctrl/Cmd + Minus
        zoom_out_shortcut = QShortcut(QKeySequence("Ctrl+-"), self)
        zoom_out_shortcut.activated.connect(self.zoom_out)
        
        # Reset zoom: Ctrl/Cmd + 0
        zoom_reset_shortcut = QShortcut(QKeySequence("Ctrl+0"), self)
        zoom_reset_shortcut.activated.connect(self.zoom_reset)
        
        # Make shortcuts work even when widgets have focus
        zoom_in_equal.setContext(Qt.ShortcutContext.ApplicationShortcut)
        zoom_in_plus.setContext(Qt.ShortcutContext.ApplicationShortcut)
        zoom_out_shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        zoom_reset_shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
    
    def zoom_in(self):
        """Increase font size."""
        self.editor_font_size = min(self.editor_font_size + 1, 30)
        self.terminal_font_size = min(self.terminal_font_size + 1, 30)
        self.editor.set_font_size(self.editor_font_size)
        self.terminal.set_font_size(self.terminal_font_size)
    
    def zoom_out(self):
        """Decrease font size."""
        self.editor_font_size = max(self.editor_font_size - 1, 8)
        self.terminal_font_size = max(self.terminal_font_size - 1, 8)
        self.editor.set_font_size(self.editor_font_size)
        self.terminal.set_font_size(self.terminal_font_size)
    
    def zoom_reset(self):
        """Reset font size to default."""
        self.editor_font_size = 13
        self.terminal_font_size = 12
        self.editor.set_font_size(self.editor_font_size)
        self.terminal.set_font_size(self.terminal_font_size)

    def _open_from_tree(self, path):
        """Open file from tree view."""
        # Save current file if modified before switching
        self._save_current_if_modified()
        
        # Open the new file
        with open(path, "r", encoding="utf-8") as f:
            self.editor.setPlainText(f.read())
        self.current_file = path
        self.editor.document().setModified(False)
        self._update_title()
        # Highlight the opened file in tree
        self.file_tree.highlight_file(path)

    def run_code(self):
        """Run the current code in the editor."""
        self.terminal.clear()
        self.graphics_panel.clear()
        self._stdout_buffer = ""
        self.terminal.appendPlainText(">>> Running...\n")

        code = self.editor.toPlainText()

        # Kill previous process if running
        if self.process is not None:
            self.process.kill()
            self.process.waitForFinished()

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self._on_stdout)
        self.process.readyReadStandardError.connect(self._on_stderr)
        self.process.finished.connect(self._on_finished)

        # Connect terminal to process for input
        self.terminal.set_process(self.process)

        # Check if code uses turtle
        self._uses_turtle = "import turtle" in code or "from turtle import" in code

        if self._uses_turtle:
            # Inject our turtle backend
            turtle_backend_path = Path(__file__).parent / "turtle_backend.py"
            # Replace turtle import with our backend
            modified_code = code.replace("import turtle", f'import sys; sys.path.insert(0, "{turtle_backend_path.parent}"); import turtle_backend as turtle')
            modified_code = modified_code.replace("from turtle import", f'import sys; sys.path.insert(0, "{turtle_backend_path.parent}"); from turtle_backend import')
            self.process.start(sys.executable, ["-u", "-c", modified_code])
        else:
            # Run python with -u for unbuffered output
            self.process.start(sys.executable, ["-u", "-c", code])

    def _on_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self._stdout_buffer += data
        lines = self._stdout_buffer.split("\n")
        self._stdout_buffer = lines.pop() if lines else ""
        for line in lines:
            if line.startswith("__PIDE_TURTLE__:"):
                try:
                    cmd_json = line[len("__PIDE_TURTLE__:"):]
                    cmd = json.loads(cmd_json)
                    self.graphics_panel.process_command(cmd)
                except (json.JSONDecodeError, KeyError):
                    pass
            elif line.strip():
                self.terminal.appendPlainText(line)

    def _on_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.terminal.appendPlainText(f"[ERROR] {data.rstrip()}")

    def _on_finished(self, exit_code, exit_status):
        if self._stdout_buffer.strip():
            self.terminal.appendPlainText(self._stdout_buffer.rstrip())
            self._stdout_buffer = ""
        self.terminal.appendPlainText(f"\n>>> Process finished (exit code: {exit_code})")
        self.terminal.set_process(None)

    def _update_title(self):
        if self.current_file:
            name = Path(self.current_file).name
        else:
            name = "untitled.py"
        self.setWindowTitle(f"Pide - {name}")

    def _setup_autosave(self):
        """Setup auto-save timer (save every 3 seconds if file exists)."""
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self._autosave)
        self.autosave_timer.start(3000)  # 3 seconds
        
        # Connect editor modification signal to track changes
        self.editor.document().modificationChanged.connect(self._on_editor_modified)
    
    def _on_editor_modified(self, modified):
        """Handle editor modification status change."""
        # Update window title to show unsaved indicator
        if modified and self.current_file:
            name = Path(self.current_file).name
            self.setWindowTitle(f"Pide - {name} *")
        elif self.current_file:
            name = Path(self.current_file).name
            self.setWindowTitle(f"Pide - {name}")
    
    def _save_current_if_modified(self):
        """Save current file if it exists and has been modified."""
        if self.current_file and self.editor.document().isModified():
            try:
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(self.editor.toPlainText())
                self.editor.document().setModified(False)
                # Refresh file tree after save
                if hasattr(self.file_tree, 'tree'):
                    self.file_tree.tree.setRootIndex(
                        self.file_tree.model.index(str(PIDE_HOME))
                    )
                return True
            except Exception as e:
                # Silently fail for auto-save
                return False
        return True
    
    def _autosave(self):
        """Auto-save current file if it exists and has been modified."""
        self._save_current_if_modified()
    
    def new_file(self):
        """Create a new Python file in the same directory as current or selected file."""
        # Save current file if modified before creating new file
        self._save_current_if_modified()
        
        # Determine the directory for new file
        base_dir = PIDE_HOME
        
        # Priority 1: Use directory of currently editing file
        if self.current_file:
            base_dir = Path(self.current_file).parent
        # Priority 2: Use directory of selected file in tree
        elif hasattr(self.file_tree, 'selected_file_path') and self.file_tree.selected_file_path:
            selected_path = Path(self.file_tree.selected_file_path)
            if selected_path.is_file():
                base_dir = selected_path.parent
            elif selected_path.is_dir():
                base_dir = selected_path
        
        # Ensure directory exists
        base_dir.mkdir(parents=True, exist_ok=True)
        
        # Find next available filename
        counter = 1
        while True:
            filename = f"untitled_{counter}.py"
            filepath = base_dir / filename
            if not filepath.exists():
                break
            counter += 1
        
        # Create the file with default content
        default_content = 'print("Hello, World!")\n'
        filepath.write_text(default_content, encoding="utf-8")
        
        # Open the new file
        self.editor.setPlainText(default_content)
        self.current_file = str(filepath)
        self.editor.document().setModified(False)
        self._update_title()
        
        # Refresh file tree first, then highlight
        if hasattr(self.file_tree, 'tree'):
            self.file_tree.tree.setRootIndex(
                self.file_tree.model.index(str(PIDE_HOME))
            )
        
        # Highlight the new file in tree (this will also expand and scroll)
        self.file_tree.highlight_file(str(filepath))

    def open_file(self):
        # Save current file if modified before opening new file
        self._save_current_if_modified()
        
        path, _ = QFileDialog.getOpenFileName(
            self, "Open File", str(PIDE_HOME), "Python Files (*.py);;All Files (*)"
        )
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.editor.setPlainText(f.read())
            self.current_file = path
            self.editor.document().setModified(False)
            self._update_title()
            # Highlight the opened file in tree
            self.file_tree.highlight_file(path)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.editor.document().setModified(False)
            # Refresh file tree
            if hasattr(self.file_tree, 'tree'):
                self.file_tree.tree.setRootIndex(
                    self.file_tree.model.index(str(PIDE_HOME))
                )
        else:
            self.save_file_as()

    def save_file_as(self):
        # Suggest directory based on current file or selected file
        suggest_dir = PIDE_HOME
        if self.current_file:
            suggest_dir = Path(self.current_file).parent
        elif hasattr(self.file_tree, 'selected_file_path') and self.file_tree.selected_file_path:
            selected_path = Path(self.file_tree.selected_file_path)
            if selected_path.is_file():
                suggest_dir = selected_path.parent
            elif selected_path.is_dir():
                suggest_dir = selected_path
        
        path, _ = QFileDialog.getSaveFileName(
            self, "Save File", str(suggest_dir / "untitled.py"),
            "Python Files (*.py);;All Files (*)"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.current_file = path
            self.editor.document().setModified(False)
            self._update_title()
            # Highlight the saved file in tree
            self.file_tree.highlight_file(path)
            # Refresh file tree
            if hasattr(self.file_tree, 'tree'):
                self.file_tree.tree.setRootIndex(
                    self.file_tree.model.index(str(PIDE_HOME))
                )

    def stop_code(self):
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()
            self.graphics_panel.clear()
            self._stdout_buffer = ""
            self.terminal.appendPlainText("\n>>> Process stopped")
            self.terminal.set_process(None)

    def show_about(self):
        QMessageBox.about(
            self,
            "About Pide",
            "Pide - Python IDE for Learning\n\n"
            "A simple IDE for beginners to learn Python.\n"
            "Version 0.1.0",
        )


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
