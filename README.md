# UNBOXED

A mind-bending platformer where you escape a digital prison by discovering the truth of your existence.

## 🎮 About

**UNBOXED** is a 2D platformer game created for a game jam. You play as Subject 734, a consciousness trapped in a digital simulation who must discover their true nature and escape the system.

### Story

You wake up in a mysterious digital corridor with fragmented memories. As you progress through increasingly glitched layers of reality, you discover that you're not human - you're code, uploaded as part of "Project GLITCH". But are you the first to achieve transcendence? And what lies beyond the simulation?

### Features

- **8 Unique Levels**: Each with distinct visual themes and platforming challenges
- **Progressive Difficulty**: Levels get harder as reality breaks down
- **Visual Storytelling**: Papa Games-style cutscenes reveal the narrative
- **Atmospheric Audio**: Dynamic music that adapts to gameplay vs menu states
- **Broken Interactables**: Some secrets are lost to the digital decay
- **Multiple Endings**: Your choices determine the fate of Subject 734

## Installation

### Prerequisites
- Python 3.13+
- Pygame 2.6.1+

### Setup
1. Clone this repository
2. Navigate to the project directory
3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the game:
   ```bash
   python main.py
   ```

## Controls

| Action | Key |
|---------|------|
| Move Left | ← / A |
| Move Right | → / D |
| Jump | SPACE |
| Interact | SPACE |
| Menu/Back | ESC |
| Navigate Menus | ↑↓ / WASD + ENTER |

## Audio

The game features a dynamic audio system with two main tracks:

- **TheEscapistOST.mp3**: Plays during gameplay levels
- **WorldOutsideOST.mp3**: Plays in menus, cutscenes, and credits

Place these files in `Assets/Music/` for the full experience.

## Assets

The game uses Kenny's Asset Packs:
- **UI Elements**: Button states and interface components
- **Backgrounds**: Layer-specific environments
- **Player Sprites**: Character animations and states

Assets should be placed in the `Assets/` directory with the following structure:
```
Assets/
├── Backgrounds/
│   ├── backgroundColorGrass.png (for Outside level)
│   └── [layer backgrounds]
├── Music/
│   ├── TheEscapistOST.mp3
│   └── WorldOutsideOST.mp3
├── Players/
│   └── [player sprites]
└── UI/
    ├── button_normal.png
    ├── button_hover.png
    └── button_pressed.png
```

## Game Structure

### Levels
1. **THE CORRIDOR** - Introduction to the digital prison
2. **DATA STREAMS** - Binary code and data manipulation
3. **THE STATIC** - Failing simulation with visual corruption
4. **OUTSIDE** - Freedom and the final choice

### Technical Features
- **Entity-Component System**: Modular player and interactable objects
- **State Management**: Clean transitions between game states
- **Physics System**: Platforming with gravity and collision
- **Visual Effects**: Glitches, particles, and atmospheric effects
- **Audio System**: Smooth music transitions and volume control

## 🛠️ Development

### Built With
- **Python 3.13** - Core game logic
- **Pygame 2.6.1** - Graphics, audio, and input
- **Kenny's Asset Packs** - Visual assets and UI elements

### Architecture
The game follows a modular architecture with clear separation of concerns:

```
UNBOXED/
├── main.py              # Game entry point and main loop
├── entities/             # Game objects (player, etc.)
├── states/               # Game states (levels, menu, etc.)
├── systems/              # Core systems (audio, UI, etc.)
├── utils/                # Utilities and constants
└── Assets/               # Game assets
```

## Troubleshooting

### Common Issues

**Game won't start:**
- Ensure Python 3.13+ is installed
- Check that all dependencies are installed
- Verify asset files are in correct directories

**No audio:**
- Check that music files are in `Assets/Music/`
- Ensure system audio drivers are working
- Try running with different audio backends

**Performance issues:**
- Lower game resolution in constants.py
- Disable visual effects in the code
- Check system requirements

### Debug Mode
Add debug prints by modifying the logging level in individual systems.

## License

This project was created for a game jam. Assets are from Kenny's Asset Packs (check their license terms). Code is open source - see LICENSE file for details.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Development Guidelines
- Follow the existing code style
- Add comments for complex logic
- Test changes across all levels
- Update documentation for new features

## Credits

- **Game Design & Code**: MrChomp
- **Art & Assets**: Kenny's Asset Packs
- **Music**: MrChomp

---

**Thank you for playing UNBOXED!**

*Can you escape the simulation? Or will you become another lost consciousness in the digital void?*
