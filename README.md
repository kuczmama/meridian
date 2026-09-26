<div align="center">

# ⚔️ Meridian

**An infinite, procedurally generated medieval world that runs entirely in your browser.**

Mountains, rivers, deserts, and jungles as far as you can walk. Towns full of people with names, homes, jobs, and opinions about you. Ruins with stories, wizards on hilltops, skirmishes on the road. And villagers who talk back through a small language model and a neural voice, both running locally on your own GPU.

**[▶ Play in your browser](https://kuczmama.github.io/meridian/)**

![A valley town at golden hour](docs/screenshots/valley.jpg)

</div>

---

## What's in the world

### 🌍 An endless planet
- A seeded, infinite world with continents, oceans, lakes, and rivers. Terrain is shaped by ridged and eroded noise, and each region gets a climate and biome: tundra, taiga, temperate forest, grassland, savanna, desert, badlands, and rainforest.
- Terrain streams in levels of detail around you on a pool of background workers. Forests, rocks, and grass are placed per biome, and every tree trunk and boulder is solid.
- A dynamic sky with a day/night cycle, drifting cloud shadows, aerial perspective, bloom, and ambient occlusion.

### 🏘️ Living towns
- Hamlets, villages, towns, and cities in four cultures: temperate, northern, desert, and tropical. Each has its own architecture, landmark hall (chapel, longhall, domed hall, or great house), market, inn, and streets. Towns are linked by roads that curve around mountains and cross rivers on bridges.
- **Every resident is a real person.** Each town's stated population is exactly the number of people who live there, and every one of them has a name, a job, a home, and a daily routine.
- Households of people living alone, couples, and families. People work their stations (chopping, smithing, selling, farming) and eat lunch at the inn and supper at home. Children go to school, and everyone sleeps in their own beds at night.
- Chapels ring their bells before services, and the congregation walks in to fill the pews while the priest preaches. Latecomers stand at the back or kneel outside.
- Civic buildings: a healer's house, an undertaker, a bakery, and a schoolhouse, alongside the inn, smithy, stables, and shops.
- Every building has a swinging door you can walk through, with no loading screen. Inside you'll find furnished rooms lit by hearths, candles, and daylight from the windows.

![Morning service in a village chapel](docs/screenshots/chapel.jpg)

### 🗺️ Over a hundred things to find
- **About 60 kinds of places**, each chosen to suit its terrain and climate:
  - wizard towers on hilltops and hedge-witch huts in the woods;
  - stone circles that glow at night, and fairy rings;
  - barrow mounds, desert tombs, and battlefields where the dead rise after dark;
  - shipwrecks, lighthouses, frozen longships, and hot springs;
  - dragon bones, fallen stars, and a sword in a stone (you'll need to be level 4 to draw it);
  - bandit camps, ogre dens, goblin warrens, and more.
- **Abandoned villages that tell you what happened**: plague, raiders, dragon fire, flood, a curse, or drought. Each has its own clues and a journal you can read.
- **About 60 kinds of roaming events** near you:
  - skirmishes you can join on either side, and wizard duels;
  - bandit ambushes and highwaymen;
  - wedding and funeral processions;
  - lost children, wounded soldiers, and riddling strangers;
  - shooting stars and the northern lights.

![An abandoned village at dusk, with its ghost](docs/screenshots/ruins.jpg)

### ⚔️ Combat, loot and reputation
- First-person sword combat with light and heavy (charged) attacks, blocking, and a timed parry.
- Enemies use three attack styles (overhead, side cut, and thrust) along with shields, stagger, casting, and death animations.
- Enemies drop loot pouches you can pick up. Weapons improve from a traveller's sword up to a ranger's blade.
- **Every town remembers you.** Good deeds raise your standing from Neutral through Liked and Honoured to Hero, which brings gifts and warm greetings. Attack someone and bystanders flee, guards hunt you, and you're wanted with a bounty until you pay it off.

![Knights fighting goblins in the forest](docs/screenshots/battle.jpg)

### 🗣️ Villagers who talk back, running locally and free
- Characters speak through **Llama 3.2 1B** running in your browser via [WebLLM](https://github.com/mlc-ai/web-llm). Each one gets a persona built from their job, quirks, relationships, town, and the time of day.
- Their lines are voiced by **[Kokoro 82M](https://github.com/hexgrad/kokoro)** on WebGPU. Voices are matched to each character's culture, gender, and age: children sound young, elders slower, and giants deep.
- Nothing leaves your computer. The models download once from the web and are cached by your browser. With them turned off, over 100 handwritten lines per role keep the world chatty.

### 🎵 A generative score
- An orchestra synthesized with Web Audio, with around 18 pieces chosen by mood and region:
  - Highland horns and harp pastorales in the temperate lands;
  - oud and frame drum in the desert, drones and choir in the frozen north;
  - marimba on tropical coasts, fiddle jigs in town, and a music box at night;
  - taiko drums that cut in the moment a fight starts.
- A soundscape of footsteps that change with the ground underfoot, owls, wolves, frogs, cicadas, gulls, roosters, town chatter, and crackling fires.

### 🧭 A map that helps you explore
- A survey map with contour lines. Discovered towns, peaks, caves, and places appear on it, and rumoured places show near towns you've visited.
- Every active quest has a marked destination, and live events show where they're happening.
- You can drop your own markers (cave, mine, camp, treasure, danger, landmark), then track one on the compass or fly to it.

![The survey map](docs/screenshots/map.jpg)

---

## Controls

| | |
|---|---|
| **WASD** | Move |
| **Shift** | Sprint |
| **Space** | Jump |
| **Mouse** | Look (click the view to capture the mouse) |
| **Left click** | Attack (hold for a heavy attack) |
| **Right click** | Block (well-timed to parry) |
| **E** | Talk, open doors, loot, interact |
| **R** | Eat or drink a healing draught |
| **V** | Mount or dismount your horse |
| **J** | Journal (quests, atlas, bestiary, people) |
| **M** | Map |
| **F** | Toggle walking and flying |
| **G** | Glide |
| **[ ]** | Change the time of day |
| **H** | Hide the HUD |

---

## Running it locally

It's a single HTML file with no build step. Serve the folder with any static web server:

```bash
git clone https://github.com/kuczmama/meridian.git
cd meridian
python3 -m http.server 8000
# open http://localhost:8000
```

Opening `index.html` directly from disk won't work, because the terrain workers and modules need to be served over HTTP.

**Browser:** you need a recent Chrome, Edge, Brave, or Arc on desktop. Talking villagers and neural voices need **WebGPU**; without it the game still runs, using the handwritten lines and your system's voices. If Brave shows only the intro screen, click the lion icon (Shields) and allow scripts for the site.

**First launch with AI:** after you begin your journey, the language model (~0.8 GB) and voice model (~330 MB) download in the background and are cached for next time. The game is fully playable while they load. You can switch either of them off in **World → settings**.

---

## How it's built

- **Rendering:** [three.js](https://threejs.org/) r160, bundled locally in `vendor/`, with custom patched materials for terrain, foliage, and buildings. Buildings are drawn procedurally in a shader (windows, timber framing, stained glass), and post-processing adds bloom and GTAO.
- **World generation:** a pure, seeded `WorldGen` handles noise, climate, rivers, settlements, and A*-routed roads. It runs on a pool of Web Workers built from blob URLs, with a main-thread fallback.
- **People:** jointed, vertex-coloured figures merged per bone for speed, with procedural animation covering walking, work, sitting, praying, dancing, and a full set of combat poses.
- **AI:** WebLLM runs in its own worker so it never blocks the game. Kokoro TTS output is streamed clause by clause, so voices start quickly.
- **Everything is procedural:** there are no image or model assets beyond generated canvas textures.

```
index.html          the whole game
vendor/three/       three.js and the post-processing passes it uses
docs/screenshots/   images for this README
```

---

## Roadmap

Still to come:
- climbable watchtowers, bell towers, and lighthouses, with windows placed where people would look out;
- caves you walk into seamlessly, with no loading screen;
- more varied architecture, and more realistic plants;
- bows, arrows, and new weapon types;
- towns shaped by the land around them, with a working economy (fields to mill to bakery to market).

---

<div align="center">

Made with a lot of noise functions. ✦ Seed 7741 is a good place to start.

</div>
