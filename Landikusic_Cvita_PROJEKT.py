import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.WGL import *
import win32ui

window = 0
width, height = 900, 600

xcor, ycor, zcor = 0, 0, 0 #koordinate kvadra
osX, osY, osZ = 0, 0, 0 #osi oko kojih ce se kvadar rotirati
kutRotacije = 0

br1, br2 = 0, 0 #brojac za pomake lijevo-desno i pomake gore-dolje

kvadar_lezi = False
game_over = False

#tipke
ESC = b'\033'

povrsine = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

rubovi = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

boje = (
    (1,0,0),
    (1,1,1),
    (1,1,0),
    (0,0,1),
    (0,1,1),
    (1,0,1),
    (0,1,0)
    )

#######################################################################################################

def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 1.0, 150.0)
    glMatrixMode(GL_MODELVIEW)
    
#######################################################################################################

#za ispis teksta
def BuildFont():
    global base
    
    wgldc = wglGetCurrentDC()
    hDC = win32ui.CreateDCFromHandle(wgldc)
    base = glGenLists(96);
    #CreateFont()
    
    font_properties = {"name" : "Broadway",
                       "width" : 40,
                       "height" : 100,
                       "weight" : 400} #debljina fonta

    
    font = win32ui.CreateFont(font_properties)
    oldfont = hDC.SelectObject(font) #odabir fonta
    wglUseFontBitmaps(wgldc, 32, 96, base) #stvaranje 96 znakova pocevsi od 32. znaka
    hDC.SelectObject(oldfont) #reset font

def glPrint(str):
    global base
    glPushAttrib(GL_LIST_BIT); #za ispisivanje teksta u OpenGL-u
    glListBase(base - 32); #stvara listu znakova od 32. znaka
    glCallLists(str) #iscrtavanje teksta
    glPopAttrib(); #resetiranje liste bitova

###########################################################################################################
    
#klasa za polje   
class Polje:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def create(self):
        vrhovi = (
            (self.x + 1, self.y - 1, self.z - 0.5),
            (self.x + 1, self.y + 1, self.z - 0.5),
            (self.x - 1, self.y + 1, self.z - 0.5),
            (self.x - 1, self.y - 1, self.z - 0.5),
            (self.x + 1, self.y - 1, self.z + 0.5),
            (self.x + 1, self.y + 1, self.z + 0.5),
            (self.x - 1, self.y - 1, self.z + 0.5),
            (self.x - 1, self.y + 1, self.z + 0.5)
        )

        glBegin(GL_QUADS)
        for povrsina in povrsine:
            k = 0
            for vrh in povrsina:
                k += 1
                glColor3fv(boje[k])
                glVertex3fv(vrhovi[vrh])
        glEnd()

        glBegin(GL_LINES)
        for rub in rubovi:
            for vrh in rub:
                glColor3f(1.0, 1.0, 1.0)
                glVertex3fv(vrhovi[vrh])
        glEnd()
     
##########################################################################################################
        
#crtanje polja     
niz_kocaka = []
Cilj = Polje(12, 0, -2.5)

def crtaj_polje():
    for i in range(0, 5, 2):
        P = Polje(i, -10, -2.5).create()
        niz_kocaka.append((i, -10, -2.5))
    for i in range(-2, 7, 2):
        for j in range(-8, -5, 2):
            P = Polje(i, j, -2.5).create()
            niz_kocaka.append((i, j, -2.5))
    for i in range(4, 7, 2):
        P = Polje(i, -4, -2.5).create()
        niz_kocaka.append((i, -4, -2.5))
    for i in range(-6, -1, 2):
        for j in range(-2, 1, 2):
            P = Polje(i, j, -2.5).create()
            niz_kocaka.append((i, j, -2.5))
    for i in range(-14, -3, 2):
        P = Polje(i, 2, -2.5).create()
        niz_kocaka.append((i, 2, -2.5))
    for i in range(-4, 7, 2):
        P = Polje(i, 8, -2.5).create()
        niz_kocaka.append((i, 8, -2.5))
    for i in range(2, 7, 2):
        P = Polje(i, 6, -2.5).create()
        niz_kocaka.append((i, 6, -2.5))
    for i in range(2, 11, 2):
        P = Polje(i, 4, -2.5).create()
        niz_kocaka.append((i, 4, -2.5))
    for i in range(8, 15, 2):
        P = Polje(i, 2, -2.5).create()
        niz_kocaka.append((i, 2, -2.5))
    for i in range(8, 11, 2):
        P = Polje(i, 0, -2.5).create()
        niz_kocaka.append((i, 0, -2.5))
    for i in range(10, 15, 2):
        P = Polje(i, -2, -2.5).create()
        niz_kocaka.append((i, -2, -2.5))
    for i in range(4, 7, 2):
        P = Polje(-4, i, -2.5).create()
        niz_kocaka.append((-4, i, -2.5))
    P = Polje(-2, -4, -2.5).create()
    niz_kocaka.append((-2, -4, -2.5))
    P = Polje(14, 0, -2.5).create()
    niz_kocaka.append((14, 0, -2.5))

    niz_kocaka.append((12, 0, -2.5))

############################################################################

#crtanje pravokutnika 
def crtaj_kvadar(x, y, z):
    vrhovi = (
            (x + 1, y - 1, z - 2),
            (x + 1, y + 1, z - 2),
            (x - 1, y + 1, z - 2),
            (x - 1, y - 1, z - 2),
            (x + 1, y - 1, z + 2),
            (x + 1, y + 1, z + 2),
            (x - 1, y - 1, z + 2),
            (x - 1, y + 1, z + 2)
        )
    glBegin(GL_QUADS)
    for povrsina in povrsine:
        k = 5
        for vrh in povrsina:
            k -= 2
            glColor3fv(boje[k])
            glVertex3fv(vrhovi[vrh])
    glEnd()

    glBegin(GL_LINES)
    for rub in rubovi:
        for vrh in rub:
            glColor3f(1.0, 1.0, 1.0)
            glVertex3fv(vrhovi[vrh])
    glEnd()

######################################################################################################

#upravljanje tipkovnicom(pomicanje kvadra)    
def special(key, x, y):
    global xcor, ycor, zcor, osX, osY, osZ, kutRotacije, br1, br2, br_koraka
    global kvadar_lezi, game_over
    
    if key == GLUT_KEY_RIGHT:
        if(br2 % 2 == 0):
            br1 += 1
            kutRotacije += 90
            osX = 0
            osY = 1
            osZ = 0
            xcor += 3
            if(kvadar_lezi == True):
                kvadar_lezi = False
            else:
                kvadar_lezi = True
                
            if(kvadar_lezi == True):
                jeLiPolje(xcor - 13, ycor + 2) and jeLiPolje(xcor - 15, ycor + 2)
                if(kvadar_na_polju == False):
                    game_over = True
            else:
                jeLiPolje(xcor - 14, ycor + 2)
                if(kvadar_na_polju == False):
                    game_over = True
        else:
            #kutRotacije += 90
            osX = 1
            osY = 0
            osZ = 0
            xcor += 2           
            kvadar_lezi = True

            jeLiPolje(xcor - 14, ycor + 1) and jeLiPolje(xcor - 14, ycor + 3)
            if(kvadar_na_polju == False):
                game_over = True
            
    elif key == GLUT_KEY_LEFT:
        if(br2 % 2 == 0):
            br1 += 1
            kutRotacije -= 90
            osX = 0
            osY = 1
            osZ = 0
            xcor -= 3
            if(kvadar_lezi == True):
                kvadar_lezi = False
            else:
                kvadar_lezi = True

            if(kvadar_lezi == True):
                jeLiPolje(xcor - 13, ycor + 2) and jeLiPolje(xcor - 15, ycor + 2)
                if(kvadar_na_polju == False):
                    game_over = True
            else:
                jeLiPolje(xcor - 14, ycor + 2)
                if(kvadar_na_polju == False):
                    game_over = True
        else:
            #kutRotacije -= 90
            osX = 1
            osY = 0
            osZ = 0
            xcor -= 2
            kvadar_lezi = True
            
            jeLiPolje(xcor - 14, ycor + 1) and jeLiPolje(xcor - 14, ycor + 3)
            if(kvadar_na_polju == False):
                game_over = True
        
    elif key == GLUT_KEY_UP:
        if(br1 % 2 == 0):
            br2 += 1
            kutRotacije -= 90
            osX = 1
            osY = 0
            osZ = 0
            ycor += 3
            if(kvadar_lezi == True):
                kvadar_lezi = False
            else:
                kvadar_lezi = True

            if(kvadar_lezi == True):
                jeLiPolje(xcor - 14, ycor + 1) and jeLiPolje(xcor - 14, ycor + 3)
                if(kvadar_na_polju == False):
                    game_over = True
            else:
                jeLiPolje(xcor - 14, ycor + 2)
                if(kvadar_na_polju == False):
                    game_over = True
        else:
            #kutRotacije -= 90
            osX = 0
            osY = 1
            osZ = 0
            ycor += 2
            kvadar_lezi = True

            jeLiPolje(xcor - 13, ycor + 2) and jeLiPolje(xcor - 15, ycor + 2)
            if(kvadar_na_polju == False):
                game_over = True
        
    elif key == GLUT_KEY_DOWN:
        if(br1 % 2 == 0):
            br2 += 1
            kutRotacije += 90
            osX = 1
            osY = 0
            osZ = 0
            ycor -= 3
            if(kvadar_lezi == True):
                kvadar_lezi = False
            else:
                kvadar_lezi = True

            if(kvadar_lezi == True):
                jeLiPolje(xcor - 14, ycor + 1) and jeLiPolje(xcor - 14, ycor + 3)
                if(kvadar_na_polju == False):
                    game_over = True
            else:
                jeLiPolje(xcor - 14, ycor + 2)
                if(kvadar_na_polju == False):
                    game_over = True
        else:
            #kutRotacije += 90
            osX = 0
            osY = 1
            osZ = 0
            ycor -= 2
            kvadar_lezi = True

            jeLiPolje(xcor - 13, ycor + 2) and jeLiPolje(xcor - 15, ycor + 2)
            if(kvadar_na_polju == False):
                game_over = True

#######################################################################################################

#zatvaranje prozora
def keyPressed(*args):
    if args[0] == ESC:
        glutDestroyWindow(window)
        sys.exit()
            
########################################################################################################

#ispituje je li kvadar izasao sa polja

kvadar_na_polju = True
def jeLiPolje(koord_x, koord_y):
    global kvadar_na_polju
    for i in range(0, len(niz_kocaka)):
        if(niz_kocaka[i][0] == koord_x and niz_kocaka[i][1] == koord_y):
            kvadar_na_polju = True
            break
        else:
            kvadar_na_polju = False
    return kvadar_na_polju

########################################################################################################        
            
def main():
    global xcor, ycor, zcor, kutRotacije, osX, osY, osZ
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0, 3, -30)
    glRotatef(-55, 1.0, 0.0, 0.0)
    crtaj_polje()

    if(game_over == True):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        zcor = -500
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos2f(-9, 0)
        glPrint(b'Game over!')

    #Cilj.create()
    #provjera jesmo li dosli do cilja
    if(xcor - 14 == 12 and ycor + 2 == 0):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        zcor = -500
        glColor3f(1.0, 1.0, 0.0)
        glRasterPos2f(-7, 1)
        glPrint(b'You win!')

    if(kvadar_lezi == True):
       glTranslatef(-14, 2, -1)
    else:
        glTranslatef(-14, 2, 0)
    
    glPushMatrix()
    glTranslatef(xcor, ycor, 0)
    glRotatef(kutRotacije, osX, osY, osZ)
    glTranslatef(-xcor, -ycor, 0)
    crtaj_kvadar(xcor, ycor, zcor)
    glPopMatrix()
        
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
window = glutCreateWindow(b'Bloxorz')
InitGL(width, height)
glutDisplayFunc(main)
glutIdleFunc(main)
glutSpecialFunc(special)
glutKeyboardFunc(keyPressed)
print (b'Pritisnite ESC za zatvaranje prozora')
BuildFont()
glutMainLoop()
