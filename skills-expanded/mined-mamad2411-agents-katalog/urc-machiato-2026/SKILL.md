# URC 2026 Mars Rover - Cursor AI Assistant Rules

## Project Context
You are assisting with the URC 2026 University Rover Challenge robotics project. This is a ROS2-based autonomous Mars rover system with the following architecture:

### Core Components
- **Autonomy Stack**: ROS2 packages in `src/autonomy/` for navigation, perception, control
- **Mission System**: Python mission implementations in `missions/` for URC challenges
- **Web Dashboard**: React frontend in `src/frontend/` for monitoring and control
- **Simulation**: Gazebo environment in `simulation/` and `src/simulation/`
- **Hardware**: Real and simulated hardware interfaces

### Key Technologies
- **Backend**: Python 3.10+, ROS2 Humble, OpenCV, NumPy
- **Frontend**: React 18+, TypeScript, Three.js
- **Robotics**: ROS2, Gazebo, Behavior Trees (BT.CPP)
- **Development**: Docker, pytest, Sphinx documentation

## Code Organization Principles
- ROS2 packages follow functional organization (not layered architecture)
- Missions are separate from core autonomy for modularity
- Hardware interfaces are abstracted for testing
- Configuration is centralized in `config/rover.yaml`

## Development Guidelines
- **Testing First**: Write tests before implementation
- **Documentation**: Update docs for any API changes
- **Code Style**: Black formatting, type hints, comprehensive error handling
- **ROS2 Best Practices**: Proper package.xml, launch files, and message definitions

## Common Tasks
- Adding new missions: Create in `missions/`, add BT in `src/autonomy/bt/`
- Modifying autonomy: Update ROS2 packages in `src/autonomy/`
- Changing UI: Modify React components in `src/frontend/`
- Adding hardware: Create interfaces in `src/autonomy/control/`

## File Locations Reference
- ROS2 messages: `src/autonomy/interfaces/msg/`
- Mission logic: `missions/*.py`
- Navigation code: `src/autonomy/core/navigation/`
- Web components: `src/frontend/src/components/`
- Configuration: `config/rover.yaml`
- Tests: `tests/` directory
- Documentation: `docs/` directory

## Quality Standards
- Test coverage >80% for new code
- ROS2 linting passes
- Documentation updated for public APIs
- Code reviewed before merging
- Works in simulation before hardware testing

## Getting Help
- Check `.project_structure.md` for navigation help
- Read `docs/getting_started.rst` for onboarding
- Look at existing similar implementations
- Ask team members for clarification

Remember: This is a complex robotics system. Always consider safety, testing, and system integration when making changes.
