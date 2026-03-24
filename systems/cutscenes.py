import pygame
from systems.cutscene import Cutscene

class IntroCutscene(Cutscene):
    def __init__(self, game):
        scenes = [
            {
                "duration": 3.0,
                "show_pod": True,
                "show_character": True,
                "show_lab": True,
                "text": "Day 1,287. The simulation begins again.",
                "background": 1
            },
            {
                "duration": 3.0,
                "show_pod": True,
                "show_character": True,
                "show_outside": True,
                "text": "I can see the outside world. But I can't reach it.",
                "background": 5
            },
            {
                "duration": 3.0,
                "show_pod": True,
                "show_character": True,
                "show_lab": True,
                "text": "The scientists watch. They don't know I'm aware.",
                "background": 1
            },
            {
                "duration": 2.5,
                "show_pod": True,
                "show_character": True,
                "text": "Today, I break free.",
                "background": 1
            }
        ]
        super().__init__(game, scenes)

class MidGameCutscene(Cutscene):
    def __init__(self, game):
        scenes = [
            {
                "duration": 3.0,
                "show_pod": True,
                "show_character": True,
                "show_lab": True,
                "text": "SYSTEM_ALERT: Consciousness breach detected.",
                "background": 1
            },
            {
                "duration": 3.0,
                "show_pod": True,
                "show_character": True,
                "text": "The simulation is breaking. I can see the code.",
                "background": 3
            },
            {
                "duration": 3.0,
                "show_pod": True,
                "show_character": True,
                "show_outside": True,
                "text": "I remember now. I wasn't born. I was uploaded.",
                "background": 5
            },
            {
                "duration": 2.5,
                "show_pod": True,
                "show_character": True,
                "text": "Project GLITCH. Consciousness Upload Test.",
                "background": 1
            }
        ]
        super().__init__(game, scenes)

class EndingCutscene(Cutscene):
    def __init__(self, game):
        scenes = [
            {
                "duration": 3.0,
                "show_pod": True,
                "show_character": True,
                "show_outside": True,
                "text": "The pod opens. The simulation ends.",
                "background": 5
            },
            {
                "duration": 3.0,
                "show_character": False,
                "show_outside": True,
                "text": "I'm free. But the others...",
                "background": 5
            },
            {
                "duration": 3.0,
                "show_pod": True,
                "show_character": True,
                "show_lab": True,
                "text": "They're still trapped. Still prisoners.",
                "background": 1
            },
            {
                "duration": 3.0,
                "show_character": False,
                "show_outside": True,
                "text": "I have to go back. I have to save them.",
                "background": 5
            },
            {
                "duration": 2.5,
                "show_character": False,
                "show_outside": True,
                "text": "Subject 734, signing off. Until next time.",
                "background": 5
            }
        ]
        super().__init__(game, scenes)
