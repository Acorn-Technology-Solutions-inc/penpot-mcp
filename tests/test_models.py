"""
Tests for data models.
"""

from penpot_mcp.models.shape import ShapeModel, ShapeType


class TestShapeModel:
    """Test shape model functionality."""

    def test_create_rectangle(self):
        """Test creating a rectangle shape."""
        shape = ShapeModel(
            type=ShapeType.RECT,
            name="Test Rect",
            x=100,
            y=200,
            width=300,
            height=150,
            fill_color="#FF0000",
        )

        assert shape.type == ShapeType.RECT
        assert shape.name == "Test Rect"
        assert shape.x == 100
        assert shape.y == 200
        assert shape.width == 300
        assert shape.height == 150
        assert shape.fill_color == "#FF0000"

    def test_create_text(self):
        """Test creating a text shape."""
        shape = ShapeModel(
            type=ShapeType.TEXT,
            name="Test Text",
            x=50,
            y=75,
            content="Hello World",
            font_size=24,
            font_family="Arial",
        )

        assert shape.type == ShapeType.TEXT
        assert shape.content == "Hello World"
        assert shape.font_size == 24
        assert shape.font_family == "Arial"

    def test_to_penpot_format(self):
        """Test conversion to Penpot API format."""
        shape = ShapeModel(
            type=ShapeType.RECT,
            name="Test",
            x=10,
            y=20,
            width=100,
            height=50,
            fill_color="#0000FF",
        )

        penpot_data = shape.to_penpot_format()

        assert penpot_data["type"] == "rect"
        assert penpot_data["name"] == "Test"
        assert penpot_data["x"] == 10
        assert penpot_data["y"] == 20
        assert penpot_data["width"] == 100
        assert penpot_data["height"] == 50
        assert penpot_data["fill-color"] == "#0000FF"

    def test_default_values(self):
        """Test default values are set correctly."""
        shape = ShapeModel(type=ShapeType.FRAME, name="Frame")

        assert shape.x == 0.0
        assert shape.y == 0.0
        assert shape.rotation == 0.0
        assert shape.opacity == 1.0
        assert shape.blocked is False
        assert shape.hidden is False
