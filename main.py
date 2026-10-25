from personajes import Guerrero, Mago, Arquero, Combate


def ejecutar_demostracion():
    print("=== Guardians of the Ancient Kingdom ===")
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)

    print("\nEstado inicial:")
    print(arthas.mostrar_estado())
    print(gandalf.mostrar_estado())

    print("\nCombate de demostración:")
    combate = Combate(arthas, gandalf)
    combate.iniciar()

    print("\n=== Demostración de habilidades ===")
    guerrero = Guerrero("Brienne", 100, 30, 10)
    objetivo1 = Mago("Merlin", 100, 10, 10)
    print(f"Guerrero causa {guerrero.atacar(objetivo1)} de daño.")

    mago = Mago("Morgana", 100, 40, 5)
    objetivo2 = Guerrero("Ragnar", 100, 10, 20)
    print(f"Mago causa {mago.atacar(objetivo2)} de daño ignorando la defensa.")

    arquero = Arquero("Legolas", 100, 35, 5)
    objetivo3 = Guerrero("Guardia", 100, 10, 15)
    print(f"Arquero causa {arquero.atacar(objetivo3)} de daño con disparo crítico.")


if __name__ == "__main__":
    ejecutar_demostracion()
