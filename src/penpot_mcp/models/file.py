"""
File and page data models.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PageModel(BaseModel):
    """Model for a Penpot page."""

    id: str
    name: str
    objects: Dict[str, Any] = Field(default_factory=dict)
    options: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic config."""

        populate_by_name = True


class FileModel(BaseModel):
    """Model for a Penpot file."""

    id: str
    name: str
    project_id: str = Field(..., alias="project-id")
    created_at: Optional[str] = Field(None, alias="created-at")
    modified_at: Optional[str] = Field(None, alias="modified-at")
    pages: List[PageModel] = Field(default_factory=list)
    data: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic config."""

        populate_by_name = True
