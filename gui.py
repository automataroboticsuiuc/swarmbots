import pyglet

window = pyglet.window.Window()

""" DEFINE LABELS HERE """
label1 = pyglet.text.Label('Choose Pattern',
                          font_name='Times New Roman',
                          font_size=20,
                          x=window.width//2, y=window.height//2,
                          color= (0,0,0,255),
                          anchor_x='center', anchor_y='center')




button1_texture = pyglet.image.load('button_unpushed.png')
button1_sprite = pyglet.sprite.Sprite(button1_texture, x = 200, y = 200)
button2_texture = pyglet.image.load('button_pushed.png')
button2_sprite = pyglet.sprite.Sprite(button2_texture,x = 0, y = 200)
from pyglet.window import key
@window.event
def on_mouse_press(x,y,button,modifiers):
    if x > button1_sprite.x and x < (button1_sprite.x + button1_sprite.width):
    	if y >button1_sprite.y and y < (button1_sprite.y + button1_sprite.height):
    		print 'click'
@window.event
def on_key_press(symbol,modifiers):
		if symbol == key.SPACE:
				print 'space'

#@window.event
#def on_mouse_release(x,y,button,modifiers):
#	button2_sprite.delete()
#	button1_sprite.draw()

@window.event
def on_draw():
	pyglet.gl.glClearColor(240,240,240,255)
	window.clear()
	button1_sprite.draw()
	label1.draw()
pyglet.app.run()