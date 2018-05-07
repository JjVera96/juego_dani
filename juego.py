# -*- coding: cp1252 -*-
from libreria import *

def Juego(Pantalla):
	pygame.mouse.set_visible(False)
	reloj = pygame.time.Clock()
	fondo = Fondo('Images/Fondo.png')
	font = pygame.font.Font(None, 20)
	mini_azul = pygame.image.load('Images/mini_ea.png').convert_alpha()
	mini_roja = pygame.image.load('Images/mini_er.png').convert_alpha()


	#jugador_uno = Jugador_Uno(25,931)
	#jugador_dos = Jugador_Dos(50,931)

	jugador_uno = Jugador_Uno(450,25)
	jugador_dos = Jugador_Dos(425,25)
	jugador_uno.estrellas = 2
	jugador_dos.estrellas = 2

	#jugador_uno = Jugador_Uno(1650,931)
	#jugador_dos = Jugador_Dos(1625,931)

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
	fin = False
	objetivo = 0

	while fin == False and jugador_uno.vida > 0 and jugador_dos.vida > 0:
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
			sonido_estrellas.play()
			jugador_dos.estrellas += 1
			ls_estrellas_rojas.remove(es)
			ls_todos.remove(es)
			if jugador_dos.estrellas == 3 and jugador_uno.estrellas == 3:
				for p in ls_puertas:
					ls_puertas.remove(p)
					ls_muros.remove(p)
					ls_todos.remove(p)

		col_estrellas = pygame.sprite.groupcollide(ls_estrellas_amarillas, ls_jugadores, True, False)
		for estrella in col_estrellas:
			if col_estrellas[estrella][0].vida < 1000:
				col_estrellas[estrella][0].vida = 1000
			ls_estrellas_amarillas.remove(estrella)
			ls_todos.remove(estrella)

		col_estrellas_azules = pygame.sprite.spritecollide(jugador_uno, ls_estrellas_azules, True)
		for es in col_estrellas_azules:
			sonido_estrellas.play()
			jugador_uno.estrellas += 1
			ls_estrellas_azules.remove(es)
			ls_todos.remove(es)
			if jugador_dos.estrellas == 3 and jugador_uno.estrellas == 3:
				for p in ls_puertas:
					ls_puertas.remove(p)
					ls_muros.remove(p)
					ls_todos.remove(p)

		for e in ls_enemigos:
			if e.disparar:
				sonido_bala.play()
				if objetivo:
					b = Bala(e.rect, Direccion_Bala(jugador_uno, e))
					objetivo += 1
				else:
					b = Bala(e.rect, Direccion_Bala(jugador_dos, e))
					objetivo -= 1
				ls_balas.add(b)
				ls_todos.add(b)

		col_be = pygame.sprite.groupcollide(ls_balas, ls_jugadores, True, False)
		for bala in col_be:
			col_be[bala][0].vida -= 100
			ls_balas.remove(bala)
			ls_todos.remove(bala)

		col_bm = pygame.sprite.groupcollide(ls_balas, ls_muros, True, False)
		for bm in col_bm:
			ls_balas.remove(bm)
			ls_todos.remove(bm)

		col_copas = pygame.sprite.groupcollide(ls_jugadores, ls_copas, False, False)
		for jg in col_copas:
			jg.win = True
			if jugador_uno.win and jugador_dos.win:
				for c in ls_copas:
					ls_copas.remove(c)
					ls_todos.remove(c)

		if not juego_win:
			camara.update(jugador_uno, jugador_dos)
			ls_todos.update()
			camara.dibujarSprites(Pantalla, fondo, ls_todos)
			vida_uno = font.render(str((jugador_uno.vida)/10), True, AZUL)
			vida_dos = font.render(str((jugador_dos.vida)/10), True, ROJO)
			estrellas_uno = font.render("x{}".format(jugador_uno.estrellas), True, AZUL)
			estrellas_dos = font.render("x{}".format(jugador_dos.estrellas), True, ROJO)
			Pantalla.blit(vida_uno, [30, 30])
			Pantalla.blit(mini_azul, [30, 50])
			Pantalla.blit(estrellas_uno, [44, 50])
			Pantalla.blit(vida_dos, [660, 30])
			Pantalla.blit(mini_roja, [660, 50])
			Pantalla.blit(estrellas_dos, [674, 50])

			pygame.display.flip()
			reloj.tick(60)

		if jugador_uno.win and jugador_dos.win:
			if not juego_win:
				sonido_ganar.play()
				font_win = pygame.font.Font(None, 80)
				winners = font_win.render("Ganadores", True, BLANCO)
				Pantalla.blit(winners, [230, 110])
				pygame.display.flip()
				juego_win = True
			else:
				pygame.time.wait(3000)
				fin = True
				
	
	sonido_nivel.stop()
	pygame.mouse.set_visible(True)
