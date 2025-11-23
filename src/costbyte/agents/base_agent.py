"""
Base class for all AI agents in the CostByte system.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from ..utils.logger import get_logger

class BaseAgent(ABC):
    """Abstract base class for AI agents."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.logger = get_logger(name)
        self.memory = {}
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the agent with required resources."""
        pass
    
    @abstractmethod
    async def execute(self, task: Any, context: Dict[str, Any] = None) -> Any:
        """Execute a task with optional context."""
        pass
    
    @abstractmethod
    async def learn(self, experience: Any) -> None:
        """Learn from experience to improve future performance."""
        pass
    
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities."""
        return getattr(self, 'capabilities', [])
