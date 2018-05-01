# -*- coding: utf-8 -*-
import pygame
import sys
import random

pygame.init()
ls_todos = pygame.sprite.Group()
ls_muros = pygame.sprite.Group()
ls_jugadores = pygame.sprite.Group()
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
def Crear_Nivel(nivel):
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
			x += 25
		y += 25
		x = 0
	return (lenlineas, lencolumnas)

#Funcion que asegura que no haya nada en las listas para iniciar el nivel
def Limpiar_Nivel(jugador_uno, jugador_dos):
	ls_todos.empty()
	ls_muros.empty()
	ls_enemigos.empty()
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
	
	def __init__(self, pantalla, jugador, anchoNivel, largoNivel):
		self.jugador = jugador
		self.rect = pantalla.get_rect()
		self.rect.center = self.jugador.center
		self.mundo_rect = pygame.Rect(0, 0, anchoNivel, largoNivel)

	def update(self):
	  if self.jugador.centerx > self.rect.centerx + 25:
		  self.rect.centerx = self.jugador.centerx - 25
		  
	  if self.jugador.centerx < self.rect.centerx - 25:
		  self.rect.centerx = self.jugador.centerx + 25

	  if self.jugador.centery > self.rect.centery + 25:
		  self.rect.centery = self.jugador.centery - 25

	  if self.jugador.centery < self.rect.centery - 25:
		  self.rect.centery = self.jugador.centery + 25
	  self.rect.clamp_ip(self.mundo_rect)

	def dibujarSprites(self, pantalla, sprites):
		for s in sprites:
			if s.rect.colliderect(self.rect):
				pantalla.blit(s.image, RelRect(s, self))

#Clase para el jugador uno
class Jugador_Uno(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Jugador/D.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vida = 600
		self.movex = 0
		self.movey = 0
		self.win = False
		self.cant = 0
		self.nivel = 1
		self.puntaje = 0
		self.direccion = 0
		self.frame = 0
		self.contacto = False
		self.arriba = False
		self.salto = False
		self.saltar = 8
		self.pausa = False
		self.avanzarIzquierda = ['Jugador/I1.png' , 'Jugador/I3.png', 'Jugador/I4.png', 'Jugador/I5.png']
		self.avanzarDerecha = ['Jugador/D1.png' , 'Jugador/D3.png', 'Jugador/D4.png', 'Jugador/D5.png']
		self.frame = 0
		self.direccion = 0

	def mas_puntaje1(self):
		self.puntaje += 100 
		self.puntaje += self.vida

	def mas_puntaje2(self):
		self.puntaje += 200
		self.puntaje += self.vida


	def puntaje_final(self):
		self.puntaje += 500
		self.puntaje += self.vida

	def menos_puntaje(self):
		self.puntaje -= 10

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
					self.image = pygame.image.load('Jugador/D.png').convert_alpha()
			else:
				if self.movex != 0:
					self.image = pygame.image.load(self.avanzarIzquierda[int(self.frame/6)]).convert_alpha()
				else:
					self.image = pygame.image.load('Jugador/I.png').convert_alpha()

			if self.frame == 18:
				self.frame = 0
			else:
				self.frame += 1

			if self.arriba:
				if self.contacto:
					self.salto = True
					self.movey -= self.saltar

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