"""
Shape data models.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ShapeType(str, Enum):
    """Penpot shape types."""

    FRAME = "frame"
    RECT = "rect"
    CIRCLE = "circle"
    PATH = "path"
    TEXT = "text"
    IMAGE = "image"
    GROUP = "group"
    BOOL = "bool"
    SVG_RAW = "svg-raw"


class ShapeModel(BaseModel):
    """Model for a Penpot shape."""

    id: Optional[str] = None
    type: ShapeType
    name: str
    x: float = 0.0
    y: float = 0.0
    width: Optional[float] = None
    height: Optional[float] = None
    rotation: float = 0.0
    opacity: float = 1.0
    blocked: bool = False
    hidden: bool = False
    fill_color: Optional[str] = Field(None, alias="fillColor")
    fill_opacity: Optional[float] = Field(None, alias="fillOpacity")
    stroke_color: Optional[str] = Field(None, alias="strokeColor")
    stroke_width: Optional[float] = Field(None, alias="strokeWidth")
    content: Optional[str] = None  # For text shapes
    font_family: Optional[str] = Field(None, alias="fontFamily")
    font_size: Optional[int] = Field(None, alias="fontSize")
    font_weight: Optional[str] = Field(None, alias="fontWeight")
    text_align: Optional[str] = Field(None, alias="textAlign")
    children: List[str] = Field(default_factory=list)  # Child shape IDs

    class Config:
        """Pydantic config."""

        populate_by_name = True
        use_enum_values = True

    def to_penpot_format(self) -> Dict[str, Any]:
        """
        Convert to Penpot API format.

        Returns:
            Dictionary in Penpot format.
        """
        data: Dict[str, Any] = {
            "type": self.type,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "rotation": self.rotation,
            "opacity": self.opacity,
            "blocked": self.blocked,
            "hidden": self.hidden,
        }

        if self.id:
            data["id"] = self.id
        if self.width is not None:
            data["width"] = self.width
        if self.height is not None:
            data["height"] = self.height
        if self.fill_color:
            data["fill-color"] = self.fill_color
        if self.fill_opacity is not None:
            data["fill-opacity"] = self.fill_opacity
        if self.stroke_color:
            data["stroke-color"] = self.stroke_color
        if self.stroke_width is not None:
            data["stroke-width"] = self.stroke_width
        if self.content:
            data["content"] = self.content
        if self.font_family:
            data["font-family"] = self.font_family
        if self.font_size:
            data["font-size"] = self.font_size
        if self.font_weight:
            data["font-weight"] = self.font_weight
        if self.text_align:
            data["text-align"] = self.text_align
        if self.children:
            data["children"] = self.children

        return data
