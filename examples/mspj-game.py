# Run with:
#
# (Linux & Mac) python3.5 test.py -m ./mygameengine.so
# (Windows) python3.6 test.py -m ./mygameengine.pyd
#
# The program should also run with 'python2.7' but you will have
# to change the 3.5's to 2.7's in your respective build script as
# well as make sure you compiled with 3.5 or 2.7 load flags.
#
# You will see `python3.5-config --includes` for example which corresponds
# to which version of python you are building.
# (In fact, run `python3.5-config --includes` in the terminal to see what it does!)
import mspj_engine

engine = mspj_engine.Engine();

# Initialize the Engine Subsystems
engine.InitializeGraphicsSubSystem();	 
engine.InitializeInputSystem();
# Once all subsystems have been initialized
# Start the engine
engine.Start();

# ------- all scene setup should happen after this line -------

# Load the texture atlas for the tilemap
engine.LoadTextureAtlas("./images/character-sprite/path/path-sheet.bmp", 32, 32);

# Setup our TileMap
tileMapObject = engine.InstantiateGameObject();
tileMapComponent = engine.InstantiateTileMapComponent(tileMapObject);
# Each 32x32 tile is scaled up to 64x64 pixels.
tileMapComponent.SetDisplayTileSize(64, 64);
# This example tile map is 20x11 in our game.
tileMapComponent.GenerateMapFromFile("./tilemap-levels/level1");
tileMapColliderComponent = engine.InstantiateTileMapColliderComponent(tileMapObject);

# Note: Player must be created after the tilemap to be rendered after (above) the tilemap
# Create our player game object, all components created here
# are to be deleted by the Player
player = engine.InstantiateGameObject();
# Prepare the controller
controller = engine.InstantiateControllerComponent(player);
player.GetTransform().SetPosition(129, 65);
# Prepare the sprite
sprite = engine.InstantiateSpriteAnimatorComponent(player);
playerSpritesheet = mspj_engine.LoadSpritesheet("./images/character-sprite/walk-cycle/character-walk-spritesheet.bmp");
playerSpritesheet.SetSpriteSize(32, 32);
sprite.SetSpritesheet(playerSpritesheet);
sprite.SetDisplaySize(32, 32);
sprite.SetAnimation("move_down", 0, 4);
sprite.SetAnimation("move_up", 1, 4);
sprite.SetAnimation("move_left", 2, 4);
sprite.SetAnimation("move_right", 3, 4);
sprite.SetAnimation("idle", 4, 2);
spriteColliderComponent = engine.InstantiateSpriteColliderComponent(player);

numberOfMushrooms = 3;
collectedCount = 0;

# Mushroom collactable behavior
def update(this, updateCtx):
    # gameObject = this.GetGameObject();
    i = 0;

def receive(this, str):
    if str != "trigger_collided": return;
    print("You collected a mushroom!");
    gameObject = this.GetGameObject();
    gameObject.SetActive(False);

    global collectedCount;
    collectedCount += 1;
    if collectedCount == numberOfMushrooms: 
        print("You won the game!");


mushroomSpritesheet = mspj_engine.LoadSpritesheet("./images/character-sprite/objects/mushroom-coin.bmp");
mushrooms = [];

for x in range(numberOfMushrooms):
    mushroom = engine.InstantiateGameObject();
    mushroomSprite = engine.InstantiateSpriteRendererComponent(mushroom);
    mushroomSprite.SetSpritesheet(mushroomSpritesheet);
    mushroomSprite.SetDisplaySize(32, 32);
    mushroomCollider = engine.InstantiateSpriteColliderComponent(mushroom);
    mushroomCollider.SetTrigger(True);
    
    engine.InstantiateBehaviorComponent(mushroom, "collectable", update, receive);

    mushrooms.append(mushroom);

mushrooms[0].GetTransform().SetPosition(144, 128);
mushrooms[1].GetTransform().SetPosition(720, 144);
mushrooms[2].GetTransform().SetPosition(400, 1150);

# ------- all scene setup should finish before this line -------

# Run our program forever
engine.MainGameLoop();

# Explicitly call Shutdown to terminate our engine
engine.Shutdown();
