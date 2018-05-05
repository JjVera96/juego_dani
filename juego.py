# -*- coding: cp1252 -*-
from libreria import *

def Juego(Pantalla):
	pygame.mouse.set_visible(False)
	reloj = pygame.time.Clock()
	fondo = Fondo('Images/Fondo.png')
	font = pygame.font.Font(None, 20)

	#jugador_uno = Jugador_Uno(25,931)
	#jugador_dos = Jugador_Dos(50,931)

	jugador_uno = Jugador_Uno(450,25)
	jugador_dos = Jugador_Dos(425,25)
	jugador_uno.estrellas = 2
	jugador_dos.estrellas = 2

	ls_todos.add(jugador_uno)
	ls_jugadores.add(jugador_uno)
	ls_todos.add(jugador_dos)
	ls_jugadores.add(jugador_dos)
	Limpiar_Nivel(jugador_uno, jugador_dos)
	Inicio_Juego(Pantalla, reloj)
	tamano = Crear_Nivel()
	camara = Camara(Pantalla, jugador_uno.rect, jugador_dos.rect, tamano[1]*25, tamano[0]*25)
	sonido_nivel.play(-1)
	juego_win = False
	Fin = False

	while Fin == False and jugador_uno.vida > 0 and jugador_dos.vida > 0:
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
			jugador_uno.arriba = True
		if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
			jugador_uno.movex = 0
		if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
			jugador_uno.movex = 0
		if event.type == pygame.KEYUP and event.key == pygame.K_UP:
			jugador_uno.arriba = False
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
			jugador_dos.arriba = True
		if event.type == pygame.KEYUP and event.key == pygame.K_a:
			jugador_dos.movex = 0
		if event.type == pygame.KEYUP and event.key == pygame.K_d:
			jugador_dos.movex = 0
		if event.type == pygame.KEYUP and event.key == pygame.K_w:
			jugador_dos.arriba = False
		if event.type == pygame.KEYUP and event.key == pygame.K_a:
			jugador_dos.movex = 0
		if event.type == pygame.KEYUP and event.key == pygame.K_d:
			jugador_dos.movex = 0

		col_estrellas_rojas = pygame.sprite.spritecollide(jugador_dos, ls_estrellas_rojas, True)
		for es in col_estrellas_rojas:
			jugador_dos.estrellas += 1
			ls_estrellas_rojas.remove(es)
			ls_todos.remove(es)
			if jugador_dos.estrellas == 3 and jugador_uno.estrellas == 3:
				for p in ls_puertas:
					ls_puertas.remove(p)
					ls_muros.remove(p)
					ls_todos.remove(p)

		col_copas = pygame.sprite.groupcollide(ls_jugadores, ls_copas, False, False)
		for jg in col_copas:
			jg.win = True
			if jugador_uno.win and jugador_dos.win:
				for c in ls_copas:
					ls_copas.remove(c)
					ls_todos.remove(c)


		col_estrellas_azules = pygame.sprite.spritecollide(jugador_uno, ls_estrellas_azules, True)
		for es in col_estrellas_azules:
			jugador_uno.estrellas += 1
			ls_estrellas_azules.remove(es)
			ls_todos.remove(es)
			if jugador_dos.estrellas == 3 and jugador_uno.estrellas == 3:
				for p in ls_puertas:
					ls_puertas.remove(p)
					ls_muros.remove(p)
					ls_todos.remove(p)

		if not juego_win:
			camara.update(jugador_uno, jugador_dos)
			ls_todos.update()
			camara.dibujarSprites(Pantalla, fondo, ls_todos)
			vida_uno = font.render(str((jugador_uno.vida)/10), True, AZUL)
			vida_dos = font.render(str((jugador_dos.vida)/10), True, ROJO)
			Pantalla.blit(vida_uno,(30, 30))
			Pantalla.blit(vida_dos,(60, 30))
			pygame.display.flip()
			reloj.tick(60)

		if jugador_uno.win and jugador_dos.win:
			if not juego_win:
				font_win = pygame.font.Font(None, 80)
				winners = font_win.render("Ganadores", True, NEGRO)
				Pantalla.blit(winners, [230, 110])
				pygame.display.flip()
				juego_win = True
			else:
				pygame.time.wait(3000)
				Fin = True
				
	
	sonido_nivel.stop()
	pygame.mouse.set_visible(True)