"""
Basic example of using CostByte AI agents.
"""
import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.costbyte.core.agent_orchestrator import AgentOrchestrator
from src.utils.config_loader import load_config

async def main():
    """Demonstrate basic CostByte AI functionality."""
    
    # Load configuration
    config = load_config("config/development.yaml")
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator(config)
    
    # Define a complex task
    complex_task = """
    Analyze the current market trends for AI agents and provide 
    strategic recommendations for investment and development.
    """
    
    print("Executing complex task with CostByte AI...")
    
    # Execute the task
    results = await orchestrator.execute_complex_task(complex_task)
    
    print("Task completed!")
    print(f"Results: {results}")

if __name__ == "__main__":
    asyncio.run(main())
