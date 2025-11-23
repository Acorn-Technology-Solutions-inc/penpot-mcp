"""
Example 1: Basic file operations and shape creation.

This example demonstrates:
1. Connecting to Penpot API
2. Creating a new file
3. Adding basic shapes (rectangle, text, circle)
4. Retrieving file information
"""

import asyncio
import os

from penpot_mcp.penpot_client import PenpotClient


async def main():
    """Run basic example."""
    # Make sure you have PENPOT_ACCESS_TOKEN set in your environment
    if not os.getenv("PENPOT_ACCESS_TOKEN"):
        print("Error: PENPOT_ACCESS_TOKEN environment variable not set")
        print("Get your token from: https://design.penpot.app -> Settings -> Access Tokens")
        return

    async with PenpotClient() as client:
        print("Connected to Penpot!")

        # Get user profile
        profile = await client.get_profile()
        print(f"\nLogged in as: {profile.get('fullname', 'Unknown')}")

        # Get first team
        teams = profile.get("teams", [])
        if not teams:
            print("No teams found!")
            return

        team_id = teams[0]["id"]
        print(f"Using team: {teams[0].get('name', 'Unnamed')}")

        # List projects
        projects = await client.list_projects(team_id)
        if not projects:
            print("No projects found! Please create a project in Penpot first.")
            return

        project_id = projects[0]["id"]
        print(f"Using project: {projects[0].get('name', 'Unnamed')}")

        # Create a new file
        print("\nCreating new file...")
        file = await client.create_file(project_id, "MCP Example - Basic Shapes")
        file_id = file["id"]
        print(f"Created file: {file_id}")

        # Get file data
        file_data = await client.get_file(file_id)
        pages = list(file_data.get("data", {}).get("pages-index", {}).values())
        page_id = pages[0]["id"]
        print(f"Using page: {page_id}")

        # Create a blue rectangle
        print("\nAdding blue rectangle...")
        rect_data = {
            "type": "rect",
            "name": "Blue Rectangle",
            "x": 100,
            "y": 100,
            "width": 200,
            "height": 100,
            "fill-color": "#3B82F6",
        }
        await client.add_shape(file_id, page_id, rect_data)
        print("Rectangle added!")

        # Create a text element
        print("\nAdding text...")
        text_data = {
            "type": "text",
            "name": "Welcome Text",
            "x": 120,
            "y": 130,
            "content": "Hello from MCP!",
            "font-size": 24,
            "font-family": "Arial",
            "fill-color": "#FFFFFF",
        }
        await client.add_shape(file_id, page_id, text_data)
        print("Text added!")

        # Create a red circle
        print("\nAdding red circle...")
        circle_data = {
            "type": "circle",
            "name": "Red Circle",
            "x": 400,
            "y": 100,
            "width": 100,
            "height": 100,
            "fill-color": "#EF4444",
        }
        await client.add_shape(file_id, page_id, circle_data)
        print("Circle added!")

        print(f"\n✓ Success! View your file at: https://design.penpot.app/#/workspace/{file_id}")


if __name__ == "__main__":
    asyncio.run(main())
