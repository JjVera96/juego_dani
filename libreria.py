# -*- coding: utf-8 -*-
import pygame
import sys
import random

pygame.init()
ls_todos = pygame.sprite.Group()
ls_muros = pygame.sprite.Group()
ls_jugadores = pygame.sprite.Group()
ls_enemigos = pygame.sprite.Group()
ls_estrellas_amarillas = pygame.sprite.Group()
ls_estrellas_rojas = pygame.sprite.Group()
ls_estrellas_azules = pygame.sprite.Group()
ls_enemigos = pygame.sprite.Group()
ls_puertas = pygame.sprite.Group()
ls_copas = pygame.sprite.Group()
ls_balas = pygame.sprite.Group()
sonido_ganar = pygame.mixer.Sound("Sonidos/Win.ogg")
sonido_perder = pygame.mixer.Sound("Sonidos/Game_over.ogg")
sonido_cargando = pygame.mixer.Sound("Sonidos/Loading.ogg")
sonido_nivel = pygame.mixer.Sound("Sonidos/Level.ogg")
sonido_estrellas = pygame.mixer.Sound("Sonidos/Coin.ogg")
sonido_bala = pygame.mixer.Sound("Sonidos/Shot.ogg")
pygame.mixer.music.set_volume(1)
ANCHO = 700
ALTO = 500
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

#Funcion para crear nivel que devuelve el tamaño en filas y columnas del archivo
def Crear_Nivel():
	x = 0
	y = 0
	iterlen = lambda it: sum(1 for _ in it)
	archivo = open('Niveles/Nivel.txt', 'r')
	lenlineas = 0
	for Fila in archivo:
		lenlineas += 1
		lencolumnas = len(Fila)
		for Columna in Fila:
			if Columna == 'X':
				m = Muro(x,y)
				ls_todos.add(m)
				ls_muros.add(m)
			if Columna == 'P':
				p = Puerta(x,y)
				ls_todos.add(p)
				ls_puertas.add(p)
				ls_muros.add(p)
			if Columna == 'A':
				a = Estrella_Azul(x,y)
				ls_todos.add(a)
				ls_estrellas_azules.add(a)
			if Columna == 'R':
				r = Estrella_Roja(x,y)
				ls_todos.add(r)
				ls_estrellas_rojas.add(r)
			if Columna == 'V':
				v = Estrella_Amarilla(x,y)
				ls_todos.add(v)
				ls_estrellas_amarillas.add(v)
			if Columna == 'Z':
				e = Enemigo_Uno(x,y)
				ls_enemigos.add(e)
				ls_todos.add(e)
			if Columna == 'E':
				z = Enemigo_Dos(x,y)
				ls_enemigos.add(z)
				ls_todos.add(z)
			if Columna == 'C':
				c = Copa(x,y)
				ls_todos.add(c)
				ls_copas.add(c)
			x += 25
		y += 25
		x = 0
	return (lenlineas, lencolumnas)

#Funcion que asegura que no haya nada en las listas para iniciar el nivel
def Limpiar_Nivel(jugador_uno, jugador_dos):
	ls_todos.empty()
	ls_muros.empty()
	ls_enemigos.empty()
	ls_estrellas_amarillas.empty()
	ls_estrellas_azules.empty()
	ls_estrellas_rojas.empty()
	ls_puertas.empty()
	ls_copas.empty()
	ls_enemigos.empty()
	ls_balas.empty()
	ls_todos.add(jugador_uno)
	ls_todos.add(jugador_dos)
	jugador_uno.movex = 0
	jugador_uno.movey = 0
	jugador_dos.movex = 0
	jugador_dos.movey = 0

#Funcion para pantalla de inicio del juego
def Inicio_Juego(Pantalla, reloj):
	sonido_cargando.play(-1)
	Cargando = 0
	time = 1
	font = pygame.font.Font(None, 80)
	while(Cargando < 100):
		Pantalla.fill(NEGRO)
		texto = font.render("Cargando " + str(Cargando) + "%", True, BLANCO)
		Cargando += time
		time += random.randrange(2)
		Pantalla.blit(texto, (ANCHO/2-150 , ALTO/2))
		reloj.tick(10) 
		pygame.display.flip()
	sonido_cargando.stop()

class Opcion:
	ver = False
	def __init__(self, texto, pos, valor, fuente, pantalla):
		self.texto = texto
		self.fuente = fuente
		self.valor = valor
		self.pos = pos
		self.setRect()
		self.dibujar(pantalla)

	def dibujar(self, pantalla):
		self.setRect()
		pantalla.blit(self.rend, self.rect)

	def setRend(self):
		self.rend = self.fuente.render(self.texto, True, self.getColor())

	def getColor(self):
		if(self.ver):
			return AZUL
		else:
			return BLANCO

	def setRect(self):
		self.setRend()
		self.rect = self.rend.get_rect()
		self.rect.topleft = self.pos


#Clase para centrar el jugador en la pantalla
def RelRect(actor, camara):
	return pygame.Rect(actor.rect.x-camara.rect.x, actor.rect.y-camara.rect.y, actor.rect.w, actor.rect.h)

class Camara(object): 	
	def __init__(self, pantalla, jugador_uno, jugador_dos, anchoNivel, largoNivel):
		self.jugador_uno = jugador_uno
		self.jugador_dos = jugador_dos
		self.rect = pantalla.get_rect()
		self.rect.center = self.jugador_uno.center
		self.mundo_rect = pygame.Rect(0, 0, anchoNivel, largoNivel)
		self.jugador_centerx = (self.jugador_uno.centerx + self.jugador_dos.centerx)/2
		self.jugador_centery = (self.jugador_uno.centery + self.jugador_dos.centery)/2


	def update(self, jg_uno, jg_dos):
		self.jugador_centerx = (self.jugador_uno.centerx + self.jugador_dos.centerx)/2
		self.jugador_centery = (self.jugador_uno.centery + self.jugador_dos.centery)/2

		if self.jugador_centerx > self.rect.centerx + 25:
			  self.rect.centerx = self.jugador_centerx - 25
		  
		if self.jugador_centerx < self.rect.centerx - 25:
			  self.rect.centerx = self.jugador_centerx + 25

		if self.jugador_centery > self.rect.centery + 25:
			  self.rect.centery = self.jugador_centery - 25

		if self.jugador_centery < self.rect.centery - 25:
			self.rect.centery = self.jugador_centery + 25

		if abs(self.jugador_uno.centerx - self.jugador_dos.centerx) > 613:
			if self.jugador_uno.centerx > self.jugador_dos.centerx:
				if jg_uno.movex > 0:
					jg_uno.max_pared_der = True
				else:
					jg_uno.max_pared_der = False
				
				if jg_dos.movex < 0:
					jg_dos.max_pared_der = True
				else:
					jg_dos.max_pared_der = False

			if self.jugador_uno.centerx < self.jugador_dos.centerx:
				if jg_uno.movex < 0:
					jg_uno.max_pared_izq = True
				else:
					jg_uno.max_pared_izq = False

				if jg_dos.movex > 0:
					jg_dos.max_pared_der = True
				else:
					jg_dos.max_pared_der = False			
		else:
			jg_uno.max_pared_der = False
			jg_uno.max_pared_izq = False
			jg_dos.max_pared_der = False
			jg_dos.max_pared_izq = False

		self.rect.clamp_ip(self.mundo_rect)

	def dibujarSprites(self, pantalla, fondo,sprites):
		pantalla.blit(fondo.image, RelRect(fondo, self))
		for s in sprites:
			if s.rect.colliderect(self.rect):
				pantalla.blit(s.image, RelRect(s, self))

#Clase para el jugador uno
class Jugador_Uno(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Jugador/1D.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vida = 1000
		self.movex = 0
		self.movey = 0
		self.win = False
		self.estrellas = 0
		self.direccion = 0
		self.frame = 0
		self.contacto = False
		self.arriba = False
		self.salto = False
		self.saltar = 8
		self.avanzarIzquierda = ['Jugador/1I1.png' , 'Jugador/1I2.png', 'Jugador/1I3.png', 'Jugador/1I4.png', 'Jugador/1I5.png', 
							'Jugador/1I6.png', 'Jugador/1I7.png', 'Jugador/1I8.png', 'Jugador/1I9.png', 'Jugador/1I10.png']
		self.avanzarDerecha = ['Jugador/1D1.png' , 'Jugador/1D2.png', 'Jugador/1D3.png', 'Jugador/1D4.png', 'Jugador/1D5.png', 
							'Jugador/1D6.png', 'Jugador/1D7.png', 'Jugador/1D8.png', 'Jugador/1D9.png', 'Jugador/1D10.png']
		self.frame = 0
		self.direccion = 0
		self.max_pared_der = False
		self.max_pared_izq = False

	def update(self):
		if not self.win:
			if self.direccion == 0:
				if self.movex != 0:
					self.image = pygame.image.load(self.avanzarDerecha[int(self.frame/6)]).convert_alpha()
				else:
					self.image = pygame.image.load('Jugador/1D.png').convert_alpha()
			else:
				if self.movex != 0:
					self.image = pygame.image.load(self.avanzarIzquierda[int(self.frame/6)]).convert_alpha()
				else:
					self.image = pygame.image.load('Jugador/1I.png').convert_alpha()

			if self.frame == 59:
				self.frame = 0
			else:
				self.frame += 1

			if self.arriba:
				if self.contacto:
					self.salto = True
					self.img_salto = True
					self.movey -= self.saltar

			if not self.max_pared_der and not self.max_pared_izq:
				self.rect.x += self.movex

			col_muro = pygame.sprite.spritecollide(self, ls_muros, False)
			for muro in col_muro:
				if self.movex > 0:
					self.rect.right = muro.rect.left
				if self.movex <0:
					self.rect.left = muro.rect.right

			if not self.contacto:
				self.movey += 0.3
				if self.movey > 10:
					self.movey = 10
				self.rect.top += self.movey

			if self.salto: 
				self.movey += 2
				self.rect.top += self.movey
				if self.contacto:
					self.salto = False

			self.contacto = False
			self.rect.y += self.movey
			if self.movey != 0:
				col_muro = pygame.sprite.spritecollide(self, ls_muros, False)
				for muro in col_muro:
					if self.movey > 0:
						self.rect.bottom = muro.rect.top
						self.contacto = True
						self.movey = 0
					if self.movey < 0:
						self.rect.top = muro.rect.bottom
						self.movey = 0
		else:
			self.image = pygame.image.load('Jugador/1Win.png').convert_alpha()


class Jugador_Dos(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Jugador/2D.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vida = 1000
		self.movex = 0
		self.movey = 0
		self.win = False
		self.estrellas = 0
		self.direccion = 0
		self.frame = 0
		self.contacto = False
		self.arriba = False
		self.salto = False
		self.saltar = 8
		self.avanzarIzquierda = ['Jugador/2I1.png' , 'Jugador/2I2.png', 'Jugador/2I3.png', 'Jugador/2I4.png', 'Jugador/2I5.png', 
							'Jugador/2I6.png', 'Jugador/2I7.png', 'Jugador/2I8.png', 'Jugador/2I9.png', 'Jugador/2I10.png']
		self.avanzarDerecha = ['Jugador/2D1.png' , 'Jugador/2D2.png', 'Jugador/2D3.png', 'Jugador/2D4.png', 'Jugador/2D5.png', 
							'Jugador/2D6.png', 'Jugador/2D7.png', 'Jugador/2D8.png', 'Jugador/2D9.png', 'Jugador/2D10.png']
		self.direccion = 0
		self.max_pared_der = False
		self.max_pared_izq = False

	def update(self):
		if not self.win:
			if self.direccion == 0:
				if self.movex != 0:
					self.image = pygame.image.load(self.avanzarDerecha[int(self.frame/6)]).convert_alpha()
				else:
					self.image = pygame.image.load('Jugador/2D.png').convert_alpha()
			else:
				if self.movex != 0:
					self.image = pygame.image.load(self.avanzarIzquierda[int(self.frame/6)]).convert_alpha()
				else:
					self.image = pygame.image.load('Jugador/2I.png').convert_alpha()

			if self.frame == 59:
				self.frame = 0
			else:
				self.frame += 1

			if self.arriba:
				if self.contacto:
					self.salto = True
					self.movey -= self.saltar

			if not self.max_pared_der and not self.max_pared_izq:
				self.rect.x += self.movex

			col_muro = pygame.sprite.spritecollide(self, ls_muros, False)
			for muro in col_muro:
				if self.movex > 0:
					self.rect.right = muro.rect.left
				if self.movex <0:
					self.rect.left = muro.rect.right

			if not self.contacto:
				self.movey += 0.3
				if self.movey > 10:
					self.movey = 10
				self.rect.top += self.movey

			if self.salto: 
				self.movey += 2
				self.rect.top += self.movey
				if self.contacto:
					self.salto = False

			self.contacto = False
			self.rect.y += self.movey
			col_muro = pygame.sprite.spritecollide(self, ls_muros, False)
			for muro in col_muro:
				if self.movey > 0:
					self.rect.bottom = muro.rect.top
					self.contacto = True
					self.movey = 0
				if self.movey < 0:
					self.rect.top = muro.rect.bottom
					self.movey = 0
		else:
			self.image = pygame.image.load('Jugador/2Win.png').convert_alpha()


class Muro(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Images/Muro.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self):
		pass

class Puerta(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Images/Puerta.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self):
		pass

class Copa(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Images/Copa.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self):
		pass

class Estrella_Amarilla(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Images/Estrella.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self):
		pass

class Estrella_Roja(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Images/EstrellaR.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self):
		pass

class Estrella_Azul(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Images/EstrellaA.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self):
		pass

class Fondo(pygame.sprite.Sprite):
	def __init__(self, Imagen):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(Imagen).convert_alpha()
		self.rect = self.image.get_rect()

	def update(self, Pantalla, vx, vy):
		pass

class Enemigo_Uno(pygame.sprite.Sprite): 
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Enemigos/Enemigo_1.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y-5
		self.dano = 0
		self.disparar = False
		self.recarga = 300

	def update(self):
		if self.recarga == 0:
			self.disparar = True
			self.recarga = 300
		else:
			self.recarga -= 1
			self.disparar = False

class Bala(pygame.sprite.Sprite):
	def __init__(self, pos, tipo):
		pygame.sprite.Sprite.__init__(self)
		self.direccion = tipo
		self.balas = ["Enemigos/Bala_Der.png", "Enemigos/Bala_Izq.png"]
		self.image = pygame.image.load(self.balas[self.direccion]).convert_alpha()
		self.rect = self.image.get_rect()
		self.contador = 1
		self.rect.y = pos[1]+10
		if self.direccion:
			self.rect.x = pos[0]+10
		else:
			self.rect.x = pos[0]-10

	def update(self):
		if self.direccion == 0:
			self.rect.x += 8
		else:
			self.rect.x -= 8

def Direccion_Bala(jugador, enemigo):
	if(jugador.rect.x - enemigo.rect.x > 0):
		return 0
	else:
		return 1

class Enemigo_Dos(pygame.sprite.Sprite): 
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.movey = 0
		self.movex = 0
		self.x = x
		self.y = y
		self.ciclo = False
		self.contacto = False
		self.salto = False
		self.recarga = random.randrange(200, 400)
		self.disparar = False
		self.image = pygame.image.load('Enemigos/Enemigo_2_D1.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.topleft = [x, y]
		self.frame = 0
		self.direccion = "derecha"
		self.dano = 20
		self.disparar = False
		self.avanzarDerecha = ['Enemigos/Enemigo_2_D1.png', 'Enemigos/Enemigo_2_D2.png', 'Enemigos/Enemigo_2_D3.png']
		self.avanzarIzquierda = ['Enemigos/Enemigo_2_I1.png', 'Enemigos/Enemigo_2_I2.png', 'Enemigos/Enemigo_2_I3.png']

	def update(self):
		if self.direccion == "izquierda":
			self.movex = -5
			self.image = pygame.image.load(self.avanzarIzquierda[int(self.frame/6)]).convert_alpha()
			
		if self.direccion == "derecha":
			self.movex = +5
			self.image = pygame.image.load(self.avanzarDerecha[int(self.frame/6)]).convert_alpha()

		if self.frame == 14:
			self.frame = 0
		else:
			self.frame += 1

		self.rect.x += self.movex
		col_muro = pygame.sprite.spritecollide(self, ls_muros, False)
		for muro in col_muro:
			if self.movex > 0:
				self.rect.right = muro.rect.left
				self.direccion = "izquierda"
			if self.movex <0:
				self.rect.left = muro.rect.right
				self.direccion = "derecha"

		if not self.contacto:
			self.movey += 0.3
			if self.movey > 10:
				self.movey = 10
			self.rect.top += self.movey

		if self.salto: 
			self.movey += 2
			self.rect.top += self.movey
			if self.contacto:
				self.salto = False

		self.contacto = False
		self.rect.y += self.movey
		col_muro = pygame.sprite.spritecollide(self, ls_muros, False)
		for muro in col_muro:
			if self.movey > 0:
				self.rect.bottom = muro.rect.top
				self.contacto = True
				self.movey = 0
			if self.movey < 0:
				self.rect.top = muro.rect.bottom
				self.movey = 0