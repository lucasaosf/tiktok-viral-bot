import random
from typing import Dict, List

# Pool of viral, high-retention English story scripts tailored for TikTok US & Europe
# Each script is crafted with:
# 1. 3-second hook (critical for retention)
# 2. Rising action and intrigue
# 3. Twist ending
# 4. Word count ~150-210 words (delivers 62-75 seconds of spoken audio at natural pace)

VIRAL_STORIES: List[Dict[str, str]] = [
    {
        "id": "mystery_grandfather_lockbox",
        "title": "The Rule You Never Break",
        "hook": "My grandfather left me a locked steel box with only one rule: never open it on a Tuesday.",
        "text": """My grandfather left me a locked steel box with only one rule: never open it on a Tuesday. He was an antique collector and always had strange habits, but on his deathbed, he held my hand and made me swear. 
For two months, I kept that box on my shelf, staring at it every single day. The lock was heavy brass, without a keyhole, only a mechanical timer dial. Last week, curiosity finally won. It was a Thursday afternoon. I grabbed my tools, worked on the latch for twenty minutes, and finally heard a soft click.
Inside, resting on black velvet, was an old cassette tape labeled June 14, 1994, and a polaroid picture. The picture was taken inside my current living room, thirty years ago. In the corner of the frame stood a tall silhouette facing the wall. 
When I turned the photograph over, my blood ran cold. Written in my grandfather's neat handwriting were the words: It only leaves when someone opens it on a Tuesday. Today is Tuesday, and I just heard footsteps upstairs."""
    },
    {
        "id": "abandoned_subway_worker",
        "title": "The Closed Subway Station",
        "hook": "I work the night maintenance shift in the New York subway, and there is one station that does not exist on any map.",
        "text": """I work the night maintenance shift in the New York subway, and there is one station that does not exist on any map. Every track inspector is given a strict set of protocols, and Rule Number Seven simply reads: If train twelve stops at 91st Street, do not look at the platform.
Last night at 3:15 AM, our service engine suddenly lost power right before the abandoned tunnel. The brakes screeched to a halt, and the cabin lights flickered off. Through the dusty front window, I saw warm yellow lights illuminate a vintage tiled platform. 
Dozens of people in 1940s clothing were standing completely motionless along the edge, staring straight into our windshield. None of them were blinking. My partner grabbed my arm and whispered not to make a sound. 
Then, over the broken radio speaker that was disconnected from the battery, a calm automated voice announced: Final boarding for all passengers. All the figures simultaneously took one synchronized step toward our train door."""
    },
    {
        "id": "psychological_test_simulation",
        "title": "The Two-Door Paradox",
        "hook": "Scientists in 1978 conducted an experiment that was immediately classified by the government.",
        "text": """Scientists in 1978 conducted an experiment that was immediately classified by the government. They placed twenty volunteers in identical soundproof white rooms with two doors labeled A and B. 
Every morning at 8:00 AM, a buzzer sounded, and the participants had five seconds to choose a door. Door A dispensed a gourmet meal and fresh water. Door B was always locked from the outside. 
On the fourteenth day, without any warning, the researchers reversed the mechanism. When the buzzer sounded, Door A remained locked, while Door B unlocked with a loud click. Nineteen of the twenty volunteers panicked and spent hours trying to force Door A open, refusing to touch Door B even when starving. 
Only one participant walked through Door B. When researchers entered to document his reaction, they found the room completely empty, with a handwritten note on the floor that read: You think you are observing us, but you are the ones inside the simulation."""
    },
    {
        "id": "deep_sea_diver_signal",
        "title": "What They Found at the Ocean Floor",
        "hook": "In 2018, deep-sea saturation divers found something buried under the Mariana Trench that was never made public.",
        "text": """In 2018, deep-sea saturation divers found something buried under the Mariana Trench that was never made public. Working at a depth of over thirty thousand feet, where the pressure can instantly crush a submarine, their sonar detected a massive geometric structure protruding from the seabed.
It was a metallic cylinder, five hundred feet tall, completely free of rust or barnacles. When the lead diver touched the surface with his robotic arm, a rhythmic vibration pulsed through the hull of their exploration vessel.
The audio sensors picked up a repeating low-frequency acoustic signal. When scientists back at the university sped up the recording by four hundred percent, the sound resolved into a human heartbeat, accompanied by faint Morse code. 
The translated message repeated every eighty seconds without stopping: We buried it here so it would never wake up. Why did you bring light into the dark?"""
    }
]

def get_random_story() -> Dict[str, str]:
    """Returns a random viral story crafted for high retention on TikTok US/Europe."""
    return random.choice(VIRAL_STORIES)

def get_story_by_id(story_id: str) -> Dict[str, str]:
    for story in VIRAL_STORIES:
        if story["id"] == story_id:
            return story
    return VIRAL_STORIES[0]

if __name__ == "__main__":
    s = get_random_story()
    print("Sample Story Title:", s["title"])
    print("Hook:", s["hook"])
    words = s["text"].split()
    print("Word count:", len(words))
    print("Est. Duration:", round(len(words) / 2.5, 1), "seconds")
