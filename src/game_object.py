# Game Object Handler for Mice and Mazes AI
"""This module implements the game object creation and handling logic for the Mice and Mazes AI game."""

import json
from typing import Dict, Optional, Any
import os


# ============================================================================
# BASE GAME OBJECT CLASS
# ============================================================================

class GameObject:
    """
    Represents a single game object instance.
    All behavior is defined by template data (actions dict with delays and impacts).
    Intelligently filters impacts based on action context (passive vs active).
    """
    
    def __init__(self, obj_id: str, obj_type: str, template_data: Dict[str, Any]):
        """
        Args:
            obj_id: Unique hex ID (e.g., "0x000001")
            obj_type: Type of object (e.g., "water_bottle", "food_pellet")
            template_data: Dict from objects.json containing actions and properties
        """
        self.id = obj_id
        self.type = obj_type
        self.actions = template_data.get("actions", {})  # {action_name: {delay, impacts}}
        # Copy properties so each instance can have mutable state
        self.properties = template_data.get("properties", {}).copy()
    
    def get_available_actions(self) -> list:
        """Return list of available action names (keys of actions dict)."""
        return list(self.actions.keys())
    
    def can_perform_action(self, action_name: str) -> bool:
        """Check if this object supports the given action."""
        return action_name in self.actions
    
    def get_action_delay(self, action_name: str) -> int:
        """Get the delay (in ticks) for performing an action."""
        if action_name in self.actions:
            return self.actions[action_name].get("delay", 0)
        return 0
    
    def get_action_impacts(self, action_name: str) -> list:
        """
        Get impacts for a specific action.
        
        Args:
            action_name: The action being performed (e.g., "consume", "use")
        
        Returns:
            List of impact dicts for this action
        """
        if action_name in self.actions:
            return self.actions[action_name].get("impacts", [])
        return []
    
    def get_passive_impacts(self) -> list:
        """Get all impacts marked as passive (proximity-based)."""
        passive = []
        for action_name, action_data in self.actions.items():
            for impact in action_data.get("impacts", []):
                if impact.get("apply_when") == "passive":
                    passive.append(impact)
        return passive
    
    def get_scent(self) -> Optional[Dict]:
        """Get the scent profile from this object's properties."""
        scent_list = self.properties.get("scent", [])
        if scent_list:
            return scent_list[0]  # Return first scent in list
        return None
    
    def __repr__(self) -> str:
        actions = self.get_available_actions()
        return f"GameObject(id={self.id}, type={self.type}, actions={actions}, pos={self.properties.get('position')})"


# ============================================================================
# GAME OBJECT FACTORY
# ============================================================================

class GameObjectFactory:
    """
    Loads object templates from JSON and creates GameObject instances.
    Tracks ID counter to ensure unique IDs.
    """
    
    def __init__(self, templates_path: str = "src/objects.json"):
        """
        Args:
            templates_path: Path to objects.json file
        """
        self.templates_path = templates_path
        self.templates = {}
        self.id_counter = 0
        self.load_templates()
    
    def load_templates(self) -> None:
        """Load object templates from JSON file."""
        if not os.path.exists(self.templates_path):
            raise FileNotFoundError(f"Templates file not found: {self.templates_path}")
        
        with open(self.templates_path, "r") as f:
            self.templates = json.load(f)
    
    def get_template(self, obj_type: str) -> Optional[Dict]:
        """Get template data for an object type."""
        return self.templates.get(obj_type)
    
    def create(self, obj_type: str) -> Optional[GameObject]:
        """
        Create a new GameObject instance from template.
        Auto-increments ID counter.
        
        Args:
            obj_type: Type of object (key from objects.json)
        
        Returns:
            GameObject instance or None if type not found
        """
        template = self.get_template(obj_type)
        if template is None:
            return None
        
        # Generate unique hex ID
        obj_id = f"0x{self.id_counter:06x}"
        self.id_counter += 1
        
        # Create and return GameObject
        obj = GameObject(obj_id, obj_type, template)
        return obj
    
    def list_generative_objects(self) -> Dict[str, int]:
        """
        Returns dict of all objects marked with generate=true and their quantities.
        Used during world initialization.
        """
        generative = {}
        for obj_type, template in self.templates.items():
            if template.get("generate", False):
                quantity = template.get("quantity", 1)
                generative[obj_type] = quantity
        return generative


# ============================================================================
# UTILITY METHODS
# ============================================================================

def apply_impacts(impact_list: list, mouse) -> Dict:
    """
    Apply impact values to a mouse object.
    
    Args:
        impact_list: List of {need: str, value: float} dicts
        mouse: Mouse object to apply impacts to
    
    Returns:
        Dict of {need: {old, new, delta}} showing what changed
    """
    changes = {}
    
    for impact in impact_list:
        need_name = impact.get("need")
        value = impact.get("value", 0)
        
        if need_name and need_name in mouse.needs:
            old_value = mouse.needs[need_name]
            mouse.needs[need_name] += value
            # Clamp to 0-100
            mouse.needs[need_name] = max(0, min(100, mouse.needs[need_name]))
            changes[need_name] = {"old": old_value, "new": mouse.needs[need_name], "delta": value}
    
    return changes


# ============================================================================
# SCENT TYPE HELPER (for logging)
# ============================================================================

SCENT_TYPES = {
    "water": "Fresh water",
    "food": "Food source",
    "treat": "Treat reward",
    "waste": "Fecal waste",
    "debris": "Debris",
    "bedding": "Nesting material",
    "sand": "Sand bath",
    "pheromone": "Mouse pheromone",
    "neutral": "Neutral"
}