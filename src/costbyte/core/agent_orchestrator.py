
**src/costbyte/core/agent_orchestrator.py**
```python
"""
Core orchestrator for managing AI agents and task workflows.
"""
from typing import Dict, List, Any
from ..agents.base_agent import BaseAgent
from .synthetic_intelligence import SyntheticIntelligence
from .strategic_intelligence import StrategicIntelligence

class AgentOrchestrator:
    """Orchestrates complex tasks using multiple AI agents."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.synthetic_intel = SyntheticIntelligence(config)
        self.strategic_intel = StrategicIntelligence(config)
        self.agents: Dict[str, BaseAgent] = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all required agents."""
        # Initialize deep agents
        from ..agents.deep_agents.task_decomposer import TaskDecomposer
        from ..agents.deep_agents.reasoning_engine import ReasoningEngine
        
        self.agents['decomposer'] = TaskDecomposer(self.config)
        self.agents['reasoner'] = ReasoningEngine(self.config)
    
    async def execute_complex_task(self, task_description: str) -> Any:
        """Execute a complex task using coordinated agents."""
        # Use strategic intelligence to plan
        plan = await self.strategic_intel.create_execution_plan(task_description)
        
        # Use synthetic intelligence to generate solutions
        solutions = await self.synthetic_intel.generate_solutions(plan)
        
        # Coordinate agents for execution
        results = await self._coordinate_agents(plan, solutions)
        
        return results
    
    async def _coordinate_agents(self, plan: Any, solutions: List[Any]) -> Dict[str, Any]:
        """Coordinate multiple agents to execute the plan."""
        results = {}
        
        for step in plan.steps:
            agent = self.agents.get(step.agent_type)
            if agent:
                results[step.name] = await agent.execute(step, solutions)
        
        return results
