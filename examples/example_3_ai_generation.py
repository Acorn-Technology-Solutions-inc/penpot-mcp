"""
Example 3: AI-powered design generation.

This example demonstrates:
1. Generating designs from natural language prompts
2. Creating login forms, pricing tables, etc.
3. AI-powered accessibility validation
"""

import asyncio
import os

from penpot_mcp.penpot_client import PenpotClient
from penpot_mcp.tools.advanced import (
    generate_design_from_prompt_tool,
    validate_accessibility_tool,
)


async def main():
    """Run AI generation example."""
    if not os.getenv("PENPOT_ACCESS_TOKEN"):
        print("Error: PENPOT_ACCESS_TOKEN environment variable not set")
        return

    async with PenpotClient() as client:
        # Get project
        profile = await client.get_profile()
        teams = profile.get("teams", [])
        if not teams:
            print("No teams found!")
            return

        projects = await client.list_projects(teams[0]["id"])
        if not projects:
            print("No projects found! Please create a project in Penpot first.")
            return

        project_id = projects[0]["id"]
        print(f"Using project: {projects[0].get('name')}\n")

        # Example prompts
        prompts = [
            "Create a login form with email and password fields",
            "Design a blue button",
            "Make a pricing table with 3 tiers",
        ]

        print("Available prompts:")
        for i, prompt in enumerate(prompts, 1):
            print(f"{i}. {prompt}")

        choice = input("\nChoose a prompt (1-3) or enter your own: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(prompts):
            prompt = prompts[int(choice) - 1]
        else:
            prompt = choice

        print(f"\nGenerating design from: '{prompt}'")

        # Generate design
        result = await generate_design_from_prompt_tool(client, project_id, prompt)

        if result.get("success"):
            file_id = result["file"]["id"]
            print(f"\n✓ Design created successfully!")
            print(f"File ID: {file_id}")
            print(f"File name: {result['file']['name']}")
            print(f"Created shapes: {', '.join(result['created_shapes'])}")
            print(f"\nView at: https://design.penpot.app/#/workspace/{file_id}")

            # Validate accessibility
            print("\n" + "=" * 60)
            print("ACCESSIBILITY CHECK")
            print("=" * 60)
            accessibility = await validate_accessibility_tool(client, file_id)
            if accessibility.get("success"):
                print(f"Score: {accessibility['accessibility_score']}%")
                print(f"Issues: {accessibility['total_issues']}")
                print(f"Warnings: {accessibility['total_warnings']}")
                print(f"\n{accessibility['summary']}")

                if accessibility["issues"]:
                    print("\nIssues found:")
                    for issue in accessibility["issues"]:
                        print(f"  - {issue['message']}")
            else:
                print(f"Error: {accessibility.get('error')}")
        else:
            print(f"\n✗ Error: {result.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())
