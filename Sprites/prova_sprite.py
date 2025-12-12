import arcade

SPEED = 200

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.sprite = None
        self.playerSpriteList = arcade.SpriteList()
        self.rockSpriteList = arcade.SpriteList()

        self.setup()

        self.direction = [0, 0]

        self.collided = False

    def setup(self):
        
        self.sprite = arcade.Sprite('./assets/pacman.png')

        self.sprite.center_x = 100
        self.sprite.center_y = 100
        self.sprite.scale_x = .1
        self.sprite.scale_y = .1

        self.aggiungi_ostacolo(200, 200, 0.1, 0.1)
        self.aggiungi_ostacolo(200, 400, 0.1, 0.1)
        self.aggiungi_ostacolo(400, 200, 0.1, 0.1)
        self.aggiungi_ostacolo(400, 400, 0.1, 0.1)
        self.aggiungi_ostacolo(300, 300, 0.1, 0.1)

        self.lastX = None
        self.lastY = None

        self.playerSpriteList.append(self.sprite)
    
    def aggiungi_ostacolo(self, position_x, position_y, scale_x, scale_y):

        rock_sprite = arcade.Sprite('./assets/rock.png')

        rock_sprite.center_x = position_x
        rock_sprite.center_y = position_y
        rock_sprite.scale_x = scale_x
        rock_sprite.scale_y = scale_y
        
        self.rockSpriteList.append(rock_sprite)

    def on_draw(self):
        self.clear()
        self.playerSpriteList.draw()
        self.rockSpriteList.draw()
        
    def on_update(self, deltaTime):

        if not self.collided:
            self.sprite.center_x += self.direction[0] * SPEED * deltaTime
            self.sprite.center_y += self.direction[1] * SPEED * deltaTime

        if len(arcade.check_for_collision_with_list(self.sprite, self.rockSpriteList)) != 0:
            self.collided = True
            self.sprite.center_x = self.lastX
            self.sprite.center_y = self.lastY
        else:
            self.lastX = self.sprite.center_x
            self.lastY = self.sprite.center_y
            self.collided = False

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.direction[1] = 1
        if key == arcade.key.DOWN:
            self.direction[1] = -1
        if key == arcade.key.RIGHT:
            self.direction[0] = 1
        if key == arcade.key.LEFT:
            self.direction[0] = -1
        
    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP:
            self.direction[1] = 0
        if key == arcade.key.DOWN:
            self.direction[1] = 0
        if key == arcade.key.RIGHT:
            self.direction[0] = 0
        if key == arcade.key.LEFT:
            self.direction[0] = 0

def main():
    game = MyGame(
        600, 600, "Il mio giochino"
    )
    arcade.run()

if __name__ == "__main__":
    main()

