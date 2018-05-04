# -*- coding: utf-8 -*-
import pygame
import sys
import random

pygame.init()
ls_todos = pygame.sprite.Group()
ls_muros = pygame.sprite.Group()
ls_jugadores = pygame.sprite.Group()
ls_enemigos = pygame.sprite.Group()
ls_estrellas_rojas = pygame.sprite.Group()
ls_estrellas_azules = pygame.sprite.Group()
ls_enemigos = pygame.sprite.Group()
sonido_ganar = pygame.mixer.Sound("Sonidos/Win.ogg")
sonido_perder = pygame.mixer.Sound("Sonidos/Game_over.ogg")
sonido_cargando = pygame.mixer.Sound("Sonidos/Loading.ogg")
sonido_nivel = pygame.mixer.Sound("Sonidos/Level.ogg")
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
			if Columna == 'A':
				e = Estrella_Azul(x,y)
				ls_todos.add(e)
				ls_estrellas_azules.add(e)
			if Columna == 'R':
				e = Estrella_Roja(x,y)
				ls_todos.add(e)
				ls_estrellas_rojas.add(e)
			x += 25
		y += 25
		x = 0
	return (lenlineas, lencolumnas)

#Funcion que asegura que no haya nada en las listas para iniciar el nivel
def Limpiar_Nivel(jugador_uno, jugador_dos):
	ls_todos.empty()
	ls_muros.empty()
	ls_enemigos.empty()
	ls_estrellas_azules.empty()
	ls_estrellas_rojas.empty()
	ls_todos.add(jugador_uno)
	ls_todos.add(jugador_dos)
	jugador_uno.movex = 0
	jugador_uno.movey = 0
	jugador_dos.movex = 0
	jugador_dos.movey = 0

#Funcion para pantalla de inicio del juego
def Inicio_Juego(Pantalla, reloj):
	sonido_cargando.play()
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

	def dibujarSprites(self, pantalla, sprites):
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
		self.pausa = False
		self.avanzarIzquierda = ['Jugador/1I1.png' , 'Jugador/1I3.png', 'Jugador/1I4.png', 'Jugador/1I5.png']
		self.avanzarDerecha = ['Jugador/1D1.png' , 'Jugador/1D3.png', 'Jugador/1D4.png', 'Jugador/1D5.png']
		self.frame = 0
		self.direccion = 0
		self.max_pared_der = False
		self.max_pared_izq = False

	def ir_arriba(self):
		self.arriba = True

	def no_arriba(self):
		self.arriba = False

	def update(self):
		if not self.pausa:
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

			if self.frame == 18:
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
		self.pausa = False
		self.avanzarIzquierda = ['Jugador/2I1.png' , 'Jugador/2I3.png', 'Jugador/2I4.png', 'Jugador/2I5.png']
		self.avanzarDerecha = ['Jugador/2D1.png' , 'Jugador/2D3.png', 'Jugador/2D4.png', 'Jugador/2D5.png']
		self.frame = 0
		self.direccion = 0
		self.max_pared_der = False
		self.max_pared_izq = False

	def ir_arriba(self):
		self.arriba = True

	def no_arriba(self):
		self.arriba = False

	def update(self):
		if not self.pausa:
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

			if self.frame == 18:
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


class Muro(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Images/Muro.png').convert_alpha()
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