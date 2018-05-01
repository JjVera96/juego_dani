# -*- coding: cp1252 -*-
from libreria import *

def Juego(Pantalla):
	pygame.mouse.set_visible(False)
	reloj = pygame.time.Clock()
	Fondo = pygame.image.load('Images/Fondo.png').convert()
	font = pygame.font.Font(None, 20)
	jugador_uno = Jugador_Uno(50,0)
	jugador_dos = Jugador_Dos(25,0)
	ls_todos.add(jugador_uno)
	ls_jugadores.add(jugador_uno)
	ls_todos.add(jugador_dos)
	ls_jugadores.add(jugador_dos)
	Limpiar_Nivel(jugador_uno, jugador_dos)
	Inicio_Juego(Pantalla, reloj)
	tamano = Crear_Nivel(jugador_uno.nivel)
	camara = Camara(Pantalla, jugador_uno.rect, jugador_dos.rect, tamano[1]*25, tamano[0]*25)
	sonido_nivel.play(-1)
	Pantalla.blit(Fondo, (0,0))

	while jugador_uno.win == False and jugador_dos.win == False and jugador_uno.vida > 0 and jugador_dos.vida > 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
			jugador_uno.movex = -5
			jugador_uno.direccion = 1
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
			jugador_uno.movex = 5
			jugador_uno.direccion = 0
		if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
			jugador_uno.ir_arriba()
		if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
			jugador_uno.movex = 0
		if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
			jugador_uno.movex = 0
		if event.type == pygame.KEYUP and event.key == pygame.K_UP:
			jugador_uno.no_arriba()
		if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
			jugador_uno.movex = 0
		if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
			jugador_uno.movex = 0

		if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
			jugador_dos.movex = -5
			jugador_dos.direccion = 1
		if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
			jugador_dos.movex = 5
			jugador_dos.direccion = 0
		if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
			jugador_dos.ir_arriba()
		if event.type == pygame.KEYUP and event.key == pygame.K_a:
			jugador_dos.movex = 0
		if event.type == pygame.KEYUP and event.key == pygame.K_d:
			jugador_dos.movex = 0
		if event.type == pygame.KEYUP and event.key == pygame.K_w:
			jugador_dos.no_arriba()
		if event.type == pygame.KEYUP and event.key == pygame.K_a:
			jugador_dos.movex = 0
		if event.type == pygame.KEYUP and event.key == pygame.K_d:
			jugador_dos.movex = 0

		Pantalla.blit(Fondo, (0,0))
		camara.update(jugador_uno, jugador_dos)
		ls_todos.update()
		camara.dibujarSprites(Pantalla, ls_todos)
		texto = font.render(str((jugador_uno.vida)/6), True, VERDE)
		Pantalla.blit(texto,(30, 0))
		pygame.display.flip()
		reloj.tick(60)

	sonido_nivel.stop()
	pygame.mouse.set_visible(True)