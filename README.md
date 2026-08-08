# Mice and Mazes

Mice and mazes is a biological simulation, machine learning environment, and competitive platform for training and evaluating AI agents in a controlled habitat. The game features three albino fancy mice navigating configurable mazes.


## Project Goals

1. Simulate the biological needs and behaviors of albino fancy mice in a controlled habitat.
2. Provide a dynamic environment to sustain the mice's biological needs and behaviors.
3. Enable the training and evaluation of AI mice agents within the habitat and maze environments.
4. Make the project engaging and gamify aspects to make learning concepts fun.

## Project Structure
```
 ┌────────────────────────────────────────────────────────┐
 │          VISUAL & BIOLOGICAL GAME ENVIRONMENT          │
 │  ┌──────────────────────┐    ┌──────────────────────┐  │
 │  │      Maze World      │    │    Habitat Colony    │  │
 │  │ (Checkpoints/Reward) │    │  (Auto-needs/Gym)    │  │
 │  │     *Supervised*     │    |   *Unsupervised*     |  |
 │  └──────────┬───────────┘    └──────────┬───────────┘  │
 └─────────────┼───────────────────────────┼──────────────┘
               |                           |
               ▼                           ▼
 ┌────────────────────────────────────────────────────────┐
 |                     GAME STATE API                     │
 |            (Vision/Hearing/Smell/Touch/Taste)          |
 │  ┌──────────────────────┐    ┌──────────────────────┐  │
 │  │    Sense Data        │    │   Action Space       │  │
 │  │    - Vision          │    │   - Move             │  │
 │  │    - Hearing         │    │   - Interact         │  │
 │  │    - Smell           │    │   - Rest             │  │
 │  │    - Touch           │    │   - Search           │  │
 │  │    - Taste           │    │   -            │  │
 │  └──────────┬───────────┘    └──────────┬───────────┘  │
 └─────────────┼───────────────────────────┼──────────────┘
 ┌────────────────────────────────────────────────────────┐
 │                   AI MOUSE AGENT CORE                  │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │             Neural Network Weights               │  │
 │  └──────────────────────────────────────────────────┘  │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │     Biological Vectors (Hunger/Drive States)     │  │
 │  └──────────────────────────────────────────────────┘  │
 └──────────────────────────┼─────────────────────────────┘
                            |         
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │                     ACTION SPACE                       │
 │            (Move/Interact/Rest/Search/Social)           │
 │                                                        │
 └────────────────────────────────────────────────────────┘

```

### Environment

The environment consists of two main components: the Maze World and the Habitat Colony. The Maze World is designed for supervised learning with checkpoints and rewards, while the Habitat Colony is for unsupervised learning, focusing on reinforcing and growing the mice's biological needs and behaviors. The environment continuously provides sensory data to the AI mouse agents, which then make decisions and take actions within the action space.

### Inputs
- Vision: Spans a nearly complete 360-degree field on a 2D plane, running continuously from -180° to +180° relative to its straight-ahead heading (0°), with a narrow 40° binocular overlap zone from -20° to +20° and a small 40° blind spot directly behind its head from -180° to -160° and +160° to +180°. Visual acuity: Low, Nearsight is 1.5 units and provides clear vision and accurate reception (type, size, texture), Farsight is 1.5-45 units and only provides derivative features (pixel changes, velocity vectors, no object recognition).
- Hearing: Provides auditory information about the environment, including the derived vector location and movement pings of other mice and objects that make "sound". The hearing range is approximately 0.1 to 20 units, with +10dB sensitivity for sounds in the front hemisphere relative to the mouse's heading. dB levels are adjusted based on the direction and distance of the sound source. communication sounds will include an encoded data package with relevant environment, food, resource, and social details to allow the mice to pass information.
- Smell: Detects chemical cues in the environment, such as pheromones, food scents, and potential hazards. The olfactory range is approximately 0.0 to 10 units, with sensitivity to different types of odors (good, bad, neutral) and strengths depending on distance. Smell measurements at 0.0 distance are of the mouse itself and determine its self-cleanliness, which steadily rises and follows the mouse's hygiene state to allow the mouse to be aware of its hygiene condition.
- Touch: Provides tactile feedback from the environment, including contact with nearby objects, surfaces, other mice, and vibration sensing.
- Taste: Allows the mouse to evaluate the edibility and quality of consumed items. Taste sensitivity is limited to the immediate consumption context.

### Mechanics

**Environment:**  
- Maze World: Designed for supervised learning with checkpoints and rewards. Maze layouts are configurable by reward, size, and complexity and auto-generated to be saved for future use. The maze world is a manually triggered environment and is controlled by the user while running sessions.
- Habitat Colony: Designed for unsupervised learning, focusing on reinforcing and growing the mice's biological needs and behaviors.

**Biology:**  
- Hunger: Represents the mouse's need for food. Increases over time and decreases when the mouse consumes food.
- Thirst: Represents the mouse's need for water. Increases over time and decreases when the mouse drinks water.
- Treats: Represents the mouse's desire for treats or special rewards. Increases over time and decreases when the mouse consumes treats.
- F_bathroom: Represents the mouse's need for a fecal bathroom break. Increases over time, with food consumption, and decreases when the mouse relieves itself.
- U_bathroom: Represents the mouse's need for a urinary bathroom break. Increases over time, with water consumption, and decreases when the mouse relieves itself. (relief type 1 releases good scent pheremones as well, relief type 2 releases bad scent)
- Fur_oils: Represents the mouse's need to groom itself. Increases over time and decreases when the mouse engages in grooming behavior.
- Local_mess: Represents the cleanliness of the mouse's immediate environment. Impacted by the presence of waste, spoiled food, and other object debris. Affects the mouse's overall hygiene state.
- Activity: Represents the mouse's need for physical activity. Increases over time and decreases when the mouse engages in movement or play.
- Social: Represents the mouse's need for social interaction. Increases over time and decreases when the mouse interacts with other mice.
- Curiosity: Represents the mouse's desire to explore and investigate its environment. Increases over time and decreases when the mouse engages in exploratory behavior.
- Discomfort: Represents the mouse's need for a comfortable environment. Increases over time and decreases when the mouse is in a comfortable setting, such as a well-maintained nest or bedding area.
- Sleep: Represents the mouse's need for rest and sleep. Increases over time and decreases when the mouse is in a resting or sleeping state.



### Outputs
- Move: Change the mouse's position within the environment. Can move forward, backward, turn left, and turn right. Can move at low, medium, or high speed with corresponding energy costs. Speeds are 1 tile per 2 ticks @ 0.5 energy cost, 1 tile per tick @ 1 energy cost, 2 tiles per tick @ 2 energy cost, respectively.
- Interact: Engage with objects or other mice in the environment. Actions vary per object: pick up, push, pull, drop, examine, consume, clean, bite, mark, relieve, use (for specific item actions such as running wheel).
- Rest: Take a break to recover energy and maintain biological needs.
- Search: Extract all sensor data from the environment to find objects, resources, or other mice.
- Social: Self-interactions or social interactions with other mice, communication, and cooperative/defensive behaviors.


## Environment Architecture

### Objects
| Object | Description | Type |
|--------|-------------|------|
| Cage | Represents the enclosure for the objects and mice within the environment. | Environment |
| Tile | Represents an individual 1x1 unit tile within the cage or maze. | Environment |
| Mouse | Represents an individual mouse within the environment. | Agent |
| WaterBottle | Provides water for the mice to drink. | Resource |
| FoodBowl | Provides food for the mice to consume. | Resource |
| FoodPellet | Represents an low value individual food pellet for the mice to consume. | Resource |
| FoodNatural | Represents a medium value natural food sources for the mice to consume, such as fruits or vegetables. | Resource |
| FoodTreat | Represents a high value treat or special reward for the mice to consume. | Resource |
| RunningWheel | Allows mice to engage in physical activity. | Object |
| SandBath | Provides a place for mice to engage in hygeine behaviors. Bonus for cleaning and relieving in this area. | Object |
| NestingMaterial | Material used by mice to build nests, beds, etc. | Object |
| Debris | Miscellaneous debris such as chewed nesting material, waste, and spoiled food crumbs present in the environment. local_mess and scent level varies with debris_type. | Object |
| Maze | Represents the maze structure within the environment. | Environment |
| MazePath | Represents a navigable path within the maze. | Environment |
| Obstacle | Represents an obstacle within the maze that mice must navigate around. | Environment |
| Reward | Represents a reward within the maze, such as treats or special items. | Object |

### Methods
1. Move
    - Move.forward - Move the mouse forward by one tile.
    - Move.backward - Move the mouse backward by one tile.
    - Move.turn_left - Turn the mouse to the left without changing its position.
    - Move.turn_right - Turn the mouse to the right without changing its position.
2. Interact
    - Interact.pick_up - Pick up an object within the environment, if its size is smaller than the mouse. (Such as nesting material, food, or debris.)
    - Interact.push - Push an object within the environment, if its size is no more than 1.5x the mouse. (object stays with mouse so long as its moving in the same direction)
    - Interact.pull - Pull an object within the environment, if its size is no more than 1.5x the mouse. (object stays with the mouse so long as its moving in the same direction)
    - Interact.drop - Drop an object that the mouse is currently holding.
    - Interact.examine - Examine an object within the environment to learn its type, quality, scent, etc.
    - Interact.consume - Ingest or use a consumable object within the environment, such as food, water, or treats.
    - Interact.bite - Bite another mouse or object within the environment. For attack/defense against others, or stimulation from specific objects.
    - Interact.mark - Mark the current tile or object within the environment with pheremones via small u_bathroom deposits (drops u_bathroom level by 0.01 comparitively).
    - Interact.relieve - Relieve oneself in the current location, more complete than marking, affecting both f_bathroom (2x rate) and u_bathroom (1x rate) levels. pheremone concentrations higher than 0.1 are considered "bad" scents as they are overconsuming, such as in waste areas or over marked areas leading to avoidance or neutral scent throwing off pathfinding.
    - Interact.use - Use an object within the environment, such as running on the wheel, dispensing a treat, triggering a mechanism, 
3. Rest
    - Rest.sleep - Enter prolonged sleep, -50% penalty to energy recovery if not lying on bedding material.
    - Rest.nap - Enter a short sleep, limited to 30 ticks of recovery, -50% penalty to energy recovery if not lying on bedding material.
4. Search
    - Search.local - Search the immediate surroundings returning nearsighted vision sensor data, sound cues, local scent, local_mess, direct touch, and other proximal sensory information. Returns objects with precise location, auditory, full visual, tactile, and olfactory information.
    - Search.global - Search the broader environment beyond the immediate surroundings, utilizing farsighted vision, vibratory cues, and scent memory location to detect objects, resources, or other mice. Objects returned with approximate vector and distance in the form of strength of the sensor (dB for sound, intensity for scent, etc.)
5. Social
    - Social.clean - Self-cleaning or peer cleaning of other mice. (Environment cleaning must be done via debris movement.)
    - Social.communicate - Send an audible message to other mice within the environment such as directional coordinates, object location and type, status, or other environment data. (Communication is not limited by distance as its considered "high frequency").
    - Social.play - Engage in social play with other mice, to promote an increase in communication behaviors and impact activity and social needs.


### Game Objects
```python
# Universal Game Object Class
class GameObject:
    """Base template. Every object inherits this structure."""
    
    def __init__(self):
        self.id = "0x000000"
        self.type = None
        self.generate = False # Whether to generate the object at the game start trigger or mouse action trigger.
        self.quantity = 0 # Number of instances of this object to generate when triggered.
        self.available_actions = []
        self.properties = {
            "type": None, # Type of the object (e.g., "food", "bedding_material", "waste", etc.)
            "category": None, # Category of the object (e.g., "thirst", "hunger", "bedding", etc.)
            "impact": [{"need": None, "value": 0}], # Impact of the object on the mouse's needs (e.g., how much it quenches thirst or satisfies hunger)
            "position": [0, 0], # Position of the object within the environment
            "size": [1,1], # Tile size relative to the environment
            "mass": 0, # Mass of the object relative to the environment            
            "is_mobile": 0, # Can the object be picked-up, dropped, pushed, or pulled
            "is_consumable": 0, # Can be consumed for food or water needs
            "is_markable": 0, # Can be marked with pheromones
            "is_perishable": 0, # Can the object spoil over time
            "is_spoiled": 0, # Indicates if the object has spoiled
            "scent": [{"type": None, "intensity": 0, "sentiment": 0, "change_rate": 0}] # Scent profile: intensity/radius, sentiment, change rate
        }
    
    def interact(self, mouse, action_name, **params):
        """Subclasses override this. Returns {success, data}."""
        if action_name == "examine":
            return {"success": True, "data": self.properties}

        raise NotImplementedError(f"{self.__class__.__name__} doesn't implement interact()")
```

```json
// Example game objects JSON file: objects.json
{
    "tile": {
        "available_actions": ["examine", "mark", "relieve"],
        "properties": {
            "type": "tile",
            "category": "environment",
            "position": [0, 0],
            "size": [1,1],
        }
    },
    "water_bottle": {
        "available_actions": ["examine","consume"],
        "properties": {
            "type": "water",
            "category": "thirst",
            "impact": [{"need": "thirst", "value": 1.0},{"need": "u_bathroom", "value": 1.0},{"need": "energy", "value": 0.5}],
            "position": [5, 0],
            "size": [1,1],
            "mass": 99,
            "is_consumable": 1,
            "scent": [{"type": "water", "intensity": 2, "sentiment": 1, "change_rate": 0}]
        }
    },
    "food_bowl": {
        "available_actions": ["examine","consume"],
        "properties": {
            "type": "food",
            "category": "hunger",
            "position": [4, 0],
            "size": [1,1],
            "mass": 99,
            "scent": [{"type": "food", "intensity": 1, "sentiment": 1, "change_rate": 0}]
        }
    },
    "food_pellet": {
        "available_actions": ["examine","consume"],
        "properties": {
            "type": "food",
            "category": "hunger",
            "impact": [{"need": "hunger", "value": 1.0},{"need": "f_bathroom", "value": 1.0},{"need": "energy", "value": 0.5}],
            "position": [3, 0],
            "size": [1,1],
            "mass": 5,
            "is_consumable": 1,
            "scent": [{"type": "food", "intensity": 1, "sentiment": 1, "change_rate": 0}]
        }
    },
    "sand_bath": {
        "available_actions": ["examine", "use"],
        "properties": {
            "type": "sand",
            "category": "hygiene",
            "impact": [{"need": "f_bathroom", "value": -10},{"need": "u_bathroom", "value": -5},{"need": "fur_oils", "value": -2},{"need": "local_mess", "value": 2}],
            "position": [1, 0],
            "size": [1,1],
            "mass": 10,
            "is_consumable": 0,
            "scent": [{"type": "sand", "intensity": 1, "sentiment": 1, "change_rate": 0}]
        }
    },
    "waste": {
        "available_actions": ["examine", "push", "pull", "pick-up", "drop", "consume"],
        "properties": {
            "type": "waste",
            "category": "debris",
            "impact": [{"need": "local_mess", "value": 2}],
            "position": [2, 0],
            "size": [1,1],
            "mass": 10,
            "is_consumable": 0,
            "scent": [{"type": "", "intensity": 2, "sentiment": -1, "change_rate": 0.5}]
        }
    }
}

```