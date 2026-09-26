<div align="center">

# ⚔️ Meridian

**An infinite, procedurally generated medieval world that runs entirely in your browser.**

Mountains, rivers, deserts, and jungles as far as you can walk. Towns full of people with names, homes, jobs, and opinions about you. Ruins with stories, wizards on hilltops, skirmishes on the road. And villagers who talk back through a small language model and a neural voice, both running locally on your own GPU.

**[▶ Play in your browser](https://kuczmama.github.io/meridian/)**

![A valley town at golden hour](docs/screenshots/valley.jpg)

| | |
|---|---|
| ![A winding cobbled street](docs/screenshots/street.jpg) | ![Friday night in the tavern](docs/screenshots/tavern.jpg) |
| ![Christmas in the snow](docs/screenshots/winter.jpg) | ![Autumn woods](docs/screenshots/forest.jpg) |

</div>

---

## What's in the world

### 🌍 An endless planet
- A seeded, infinite world with continents, oceans, lakes, and rivers. Terrain is shaped by ridged and eroded noise, and each region gets a climate and biome: tundra, taiga, temperate forest, grassland, savanna, desert, badlands, and rainforest.
- Terrain streams in levels of detail around you on a pool of background workers. Forests, rocks, and grass are placed per biome, and every tree trunk and boulder is solid.
- A dynamic sky with a day/night cycle, drifting cloud shadows, aerial perspective, bloom, and ambient occlusion.

### 🏘️ Living towns
- Hamlets, villages, towns, and cities in four cultures: temperate, northern, desert, and tropical. Each has its own architecture, landmark hall (chapel, longhall, domed hall, or great house), market, inn, and streets.
- **Towns grow from their streets.** Winding main streets follow the lie of the land from the square out to every road; side lanes wander off them, and every lane ends at a house, a graveyard, a park, a cloister, or the castle. Hillside towns keep their slopes, and each house stands on its own ground.
- **Every town lives by a trade**, chosen from the land around it, and is laid out to suit:
  - *fishing towns* along a waterfront promenade either side of the jetty;
  - *seaside resorts* with villas, bathhouses, cabanas, parasols and holidaymakers on the beach;
  - *mining towns* whose street switches back up the hill to a timber headframe and a mine you can walk down into, level after level, to chip gold from the veins;
  - *logging towns* with a long high street out to the sawmill and its log yard;
  - *hunters' camps* where the houses stand in a ring round the lodge;
  - *craft towns and cities* built on a planned avenue with side streets at right angles, full of workshops;
  - *farming villages* with lanes out to the barns; *seminaries* with a cloister and chanting monks; *castle towns* and cities with a keep, a moat and drawbridge, and a lord.
- Towns are close together, a couple of kilometres apart, with hamlets between the cities.
- **Trade:** each town's goods (salt fish, gold and iron ore, timber, furs, cloth, tools, grain) are cheap where they're made and dearer the further you carry them, dearest in the cities. Buy gold ore at the mine for half what the city pays. Carters haul loads between the towns and will tell you the prices.
- The number of buildings matches the number of people: a hamlet of twelve has five homes, a city of seventy about forty-five buildings.
- Roads link the towns, cobbled near the cities, crossing rivers on timber or stone bridges, with milestones, wayside shrines, rest stops and benches at the best views. Walkers, pilgrims and carters travel them. Dirt tracks lead out to the places worth finding, over plank-and-rope footbridges, and animal trails wind through the woods.
- **Every resident is a real person.** Each town's stated population is exactly the number of people who live there, and every one of them has a name, a job, a home, and a daily routine.
- Households of people living alone, couples, and families. People work their stations (chopping, smithing, selling, farming) and eat lunch at the inn and supper at home. Children go to school, and everyone sleeps in their own beds at night.
- Chapels ring their bells before services, and the congregation walks in to fill the pews while the priest preaches. Latecomers stand at the back or kneel outside.
- Civic buildings: a healer's house, an undertaker, a bakery, and a schoolhouse, alongside the inn, smithy, stables, and shops.
- Every building has a swinging door you can walk through, with no loading screen. Inside you'll find furnished rooms lit by hearths, candles, and daylight from the windows.
- **Homes are lived in.** A nameplate by each door says whose house it is. Inside there's a bed for everyone who lives there, a kitchen and a table laid for the household, and the tools of the owner's trade: the smith's rack, the fisher's nets, the hunter's pelts, the priest's icons. Two-storey houses have stairs you can climb to the bedrooms. People cook, eat together, sweep, chat and sleep in their own beds.
- **Taverns** are big halls with a bar and kegs, long tables laid with roast fowl, fish, cheese and ale, and a band on the stage playing jigs on whistle, lute and drum. The chapel organ plays at services, monks chant in the cloister, and horses whinny in the stables.
- **By the water**, towns have a jetty you can walk out on, fishers fishing off it, gutting tables and drying racks, and a seafood tavern. On days off people stroll the beach and children build sandcastles while the surf rolls in. Reeds grow in the shallows.
- **Inland**, hunters head for the woods at dawn, foragers go out with baskets, and meat and hides hang drying behind the houses.

![Morning service in a village chapel](docs/screenshots/chapel.jpg)

| | |
|---|---|
| ![A hunters' camp, its houses in a ring round the lodge](docs/screenshots/camp.jpg) | ![Gold in the deep workings of a mine](docs/screenshots/mine.jpg) |

### 📅 Days, seasons and weather
- **A real calendar.** Every day has a weekday and a date (the world's year runs 800 years behind ours, so the weekdays line up with today's). The seasons turn: summer days are long and winter suns hang low, more so the further north you go.
- **The week shapes town life.** People sleep at night, eat lunch at noon and work their trades on weekdays, and children go to school Monday to Friday. Friday nights the inn is packed and spills into the street. Saturday is market day with a dance at the fire. Each culture keeps its own holy day: the chapel fills on Sunday, the northern hall holds its moot on Thursday, the desert dome gathers on Friday, and the island great house on Monday. Nobody works on a holy day.
- **Holidays from each culture's own lore.** Christmas Eve with midnight mass and Christmas Day with a tree in the square, New Year, Easter, May Day and its maypole, Midsummer bonfires and All Hallows' Eve in the lowlands. Yule, Midsummer and Winter Nights in the north. The Star New Year and the Night of Falling Stars in the desert. Full-moon gatherings and the Rising of the Seven Stars on the islands. Villagers decorate the square, feast, dance and talk about it.
- **Weather** drifts across the land in fronts shaped by climate and season, mostly fair: clear skies and cloud, morning fog, rain or snow about a sixth of the time, and now and then a thunderstorm or a blizzard. Snow settles on the ground, roofs and roads and melts in the warm. Leaves turn and fall in autumn. People head indoors when it pours.
- The date, the season, the weather and what they are doing all feed into what villagers say.

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

### ⚔️ Combat, hunting, fishing and reputation
- First-person sword combat with light and heavy (charged) attacks, blocking, and a timed parry.
- **A bow:** buy one from a hunter, draw and loose arrows that fly true under gravity, and pick them up again where they land. Fresh hoof and paw prints in the mud lead you to the game.
- **Fishing:** stand at the water and cast. Wait for the float to dip, strike, then reel without snapping the line. What bites depends on the water and the climate: herring and cod in cold seas, snapper and tuna in the tropics, trout, pike and salmon in the lakes. Sell your catch or cook it.
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
- Roads and tracks are drawn on the minimap and the map. Places villagers tell you about, in their own words or when you ask for news, go straight onto your map.

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
| **B** | Switch between sword and bow |
| **E** at the water | Cast a line; E to strike, hold E to reel |
| **V** | Mount or dismount your horse |
| **J** | Journal (quests, atlas, bestiary, people) |
| **M** | Map |
| **F** | Toggle walking and flying |
| **G** | Glide |
| **[ ]** | Change the time of day |
| **Shift + [ ]** | Change the day |
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
- more varied architecture, and interiors that match every building's outside;
- new weapon types, and arrows that can fell bandits as well as game;
- supply chains the townsfolk run themselves (fields to mill to bakery to market), with prices that rise and fall.

---

<div align="center">

Made with a lot of noise functions. ✦ Seed 7741 is a good place to start.

</div>
