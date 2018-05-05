# -*- coding: cp1252 -*-
from juego import *

def main():
	Pantalla = pygame.display.set_mode([ANCHO, ALTO])
	pygame.display.set_caption("Mi Juego")
	terminar = False
	Menu = pygame.font.Font(None, 60)
	Menu.set_bold(True)
	MenuT = pygame.font.Font(None, 160)
	Title = MenuT.render("Mi", True, BLANCO)
	Title2 = MenuT.render("Juego", True, BLANCO)
	Menu = [Opcion("Jugar", (440, 350), 0, Menu, Pantalla), Opcion("Salir", (448, 450), 1, Menu, Pantalla)]
	
	while not terminar:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
						terminar = True
		Pantalla.fill((0, 0, 0))
		Pantalla.blit(Title, [300, 30])
		Pantalla.blit(Title2, [230, 110])
		
		for opcion in Menu:
				if opcion.rect.collidepoint(pygame.mouse.get_pos()):
						opcion.ver=True
						if event.type == pygame.MOUSEBUTTONDOWN:
								if(opcion.valor == 0):
									Juego(Pantalla)
								elif(opcion.valor == 1):
										terminar = True
				else:
						opcion.ver = False
				opcion.dibujar(Pantalla)
		pygame.display.flip()
	pygame.quit()

if __name__ == '__main__':
	main()