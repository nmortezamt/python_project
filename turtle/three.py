import turtle
tr = turtle.Turtle()
tr.screen.bgcolor('black')
tr.pensize(2)
tr.color('green')
tr.left(90)
tr.backward(100)
tr.speed(0)
tr.shape('turtle')
def tree(i):
    if i < 10:
        return
    else:
        tr.forward(i)
        tr.color('orange')
        tr.circle(2)
        tr.color('brown')
        tr.left(30)
        tree(3*i/4)
        tr.right(60)
        tree(3*i/4)
        tr.left(30)
        tr.backward(i)

tree(100)
turtle.done()
