from abc import ABC, abstractmethod


class Personaje(ABC):
    def __init__(self, nombre, vida, ataque, defensa):
        self.set_nombre(nombre)
        self.set_vida(vida)
        self.set_ataque(ataque)
        self.set_defensa(defensa)

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = nombre.strip()

    def get_vida(self):
        return self.__vida

    def set_vida(self, vida):
        if isinstance(vida, bool) or not isinstance(vida, int) or not 0 <= vida <= 100:
            raise ValueError("La vida debe ser un entero entre 0 y 100.")
        self.__vida = vida

    def get_ataque(self):
        return self.__ataque

    def set_ataque(self, ataque):
        if isinstance(ataque, bool) or not isinstance(ataque, int) or ataque <= 0:
            raise ValueError("El ataque debe ser un entero positivo.")
        self.__ataque = ataque

    def get_defensa(self):
        return self.__defensa

    def set_defensa(self, defensa):
        if isinstance(defensa, bool) or not isinstance(defensa, int) or defensa < 0:
            raise ValueError("La defensa debe ser un entero no negativo.")
        self.__defensa = defensa

    def recibir_danio(self, cantidad):
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("El daño debe ser un entero no negativo.")
        recibido = min(cantidad, self.__vida)
        self.__vida -= recibido
        return recibido

    def esta_vivo(self):
        return self.__vida > 0

    def mostrar_estado(self):
        return (
            f"{self.__nombre} | Vida: {self.__vida} | "
            f"Ataque: {self.__ataque} | Defensa: {self.__defensa}"
        )

    def _validar_objetivo(self, objetivo):
        if not isinstance(objetivo, Personaje):
            raise TypeError("El objetivo debe ser un personaje.")
        if not self.esta_vivo():
            raise ValueError(f"{self.__nombre} está derrotado y no puede atacar.")
        if not objetivo.esta_vivo():
            raise ValueError(f"{objetivo.get_nombre()} ya está derrotado.")

    @abstractmethod
    def atacar(self, objetivo):
        raise NotImplementedError


class Guerrero(Personaje):
    def atacar(self, objetivo):
        self._validar_objetivo(objetivo)
        ataque_potenciado = self.get_ataque() * 120 // 100
        danio = max(0, ataque_potenciado - objetivo.get_defensa())
        return objetivo.recibir_danio(danio)


class Mago(Personaje):
    def atacar(self, objetivo):
        self._validar_objetivo(objetivo)
        return objetivo.recibir_danio(self.get_ataque())


class Arquero(Personaje):
    def atacar(self, objetivo):
        self._validar_objetivo(objetivo)
        if self.get_ataque() > objetivo.get_defensa():
            danio_base = self.get_ataque() - objetivo.get_defensa()
            danio = danio_base * 2
        else:
            danio = 0
        return objetivo.recibir_danio(danio)


class Combate:
    def __init__(self, personaje1, personaje2):
        if not isinstance(personaje1, Personaje) or not isinstance(personaje2, Personaje):
            raise TypeError("El combate requiere dos personajes válidos.")
        if personaje1 is personaje2:
            raise ValueError("Un personaje no puede combatir contra sí mismo.")
        self.__personaje1 = personaje1
        self.__personaje2 = personaje2
        self.__turno_actual = personaje1
        self.__rondas = 0
        self.__resultado = None

    def cambiar_turno(self):
        self.__turno_actual = (
            self.__personaje2
            if self.__turno_actual is self.__personaje1
            else self.__personaje1
        )
        return self.__turno_actual

    def verificar_ganador(self):
        if not self.__personaje1.esta_vivo() and not self.__personaje2.esta_vivo():
            return "Empate"
        if not self.__personaje1.esta_vivo():
            return self.__personaje2
        if not self.__personaje2.esta_vivo():
            return self.__personaje1
        return None

    def mostrar_resultado(self):
        if self.__resultado is None:
            ganador = self.verificar_ganador()
            if ganador is None:
                return "El combate sigue en curso."
            self.__resultado = "Empate." if ganador == "Empate" else f"Ganador: {ganador.get_nombre()}."
        return self.__resultado

    def iniciar(self, mostrar=True):
        if self.__resultado is not None:
            return self.__resultado

        sin_danio_consecutivo = 0
        while self.__rondas < 50:
            atacante = self.__turno_actual
            objetivo = self.__personaje2 if atacante is self.__personaje1 else self.__personaje1

            if atacante.esta_vivo() and objetivo.esta_vivo():
                danio = atacante.atacar(objetivo)
                if mostrar:
                    print(f"{atacante.get_nombre()} ataca a {objetivo.get_nombre()} y causa {danio} de daño.")
                    print(self.__personaje1.mostrar_estado())
                    print(self.__personaje2.mostrar_estado())

                if danio == 0:
                    sin_danio_consecutivo += 1
                else:
                    sin_danio_consecutivo = 0

                ganador = self.verificar_ganador()
                if ganador is not None:
                    self.__resultado = "Empate." if ganador == "Empate" else f"Ganador: {ganador.get_nombre()}."
                    break

                if sin_danio_consecutivo >= 2:
                    self.__resultado = "Empate técnico: ambos personajes completaron una ronda sin causar daño."
                    break

            self.cambiar_turno()
            if self.__turno_actual is self.__personaje1:
                self.__rondas += 1

        if self.__resultado is None:
            self.__resultado = "Empate: se alcanzó el límite de 50 rondas."

        if mostrar:
            print(self.mostrar_resultado())
        return self.__resultado
