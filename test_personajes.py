import pytest

from personajes import Personaje, Guerrero, Mago, Arquero, Combate


def test_creacion_de_tres_personajes():
    assert Guerrero("A", 100, 20, 5).esta_vivo()
    assert Mago("B", 80, 30, 2).esta_vivo()
    assert Arquero("C", 70, 25, 3).esta_vivo()


@pytest.mark.parametrize("vida", [-1, 101, 1.5, True])
def test_rechaza_vida_invalida(vida):
    with pytest.raises(ValueError):
        Guerrero("A", vida, 20, 5)


@pytest.mark.parametrize("nombre", ["", "   ", None])
def test_rechaza_nombre_invalido(nombre):
    with pytest.raises(ValueError):
        Guerrero(nombre, 100, 20, 5)


@pytest.mark.parametrize("ataque", [0, -1, 1.2, True])
def test_rechaza_ataque_invalido(ataque):
    with pytest.raises(ValueError):
        Guerrero("A", 100, ataque, 5)


@pytest.mark.parametrize("defensa", [-1, 1.2, True])
def test_rechaza_defensa_invalida(defensa):
    with pytest.raises(ValueError):
        Guerrero("A", 100, 20, defensa)


def test_personaje_es_abstracto():
    with pytest.raises(TypeError):
        Personaje("A", 100, 20, 5)


def test_habilidad_guerrero():
    atacante = Guerrero("G", 100, 30, 10)
    objetivo = Mago("M", 100, 10, 10)
    assert atacante.atacar(objetivo) == 26
    assert objetivo.get_vida() == 74


def test_habilidad_mago_ignora_defensa():
    atacante = Mago("M", 100, 40, 0)
    objetivo = Guerrero("G", 100, 10, 90)
    assert atacante.atacar(objetivo) == 40
    assert objetivo.get_vida() == 60


def test_habilidad_arquero_critico():
    atacante = Arquero("A", 100, 35, 5)
    objetivo = Guerrero("G", 100, 10, 15)
    assert atacante.atacar(objetivo) == 40
    assert objetivo.get_vida() == 60


def test_arquero_no_hace_danio_si_no_supera_defensa():
    atacante = Arquero("A", 100, 15, 5)
    objetivo = Guerrero("G", 100, 10, 15)
    assert atacante.atacar(objetivo) == 0
    assert objetivo.get_vida() == 100


def test_vida_nunca_es_negativa():
    objetivo = Guerrero("G", 5, 10, 0)
    assert objetivo.recibir_danio(100) == 5
    assert objetivo.get_vida() == 0


def test_recibir_danio_rechaza_negativo():
    objetivo = Guerrero("G", 50, 10, 0)
    with pytest.raises(ValueError):
        objetivo.recibir_danio(-1)


def test_personaje_derrotado_no_ataca():
    atacante = Guerrero("G", 0, 30, 0)
    objetivo = Mago("M", 100, 10, 0)
    with pytest.raises(ValueError):
        atacante.atacar(objetivo)


def test_objetivo_derrotado_no_recibe_ataque():
    atacante = Guerrero("G", 100, 30, 0)
    objetivo = Mago("M", 0, 10, 0)
    with pytest.raises(ValueError):
        atacante.atacar(objetivo)


def test_combate_determina_ganador():
    atacante = Mago("M", 100, 40, 0)
    objetivo = Guerrero("G", 20, 10, 0)
    resultado = Combate(atacante, objetivo).iniciar(mostrar=False)
    assert resultado == "Ganador: M."


def test_empate_tecnico_sin_danio():
    primero = Guerrero("A", 100, 10, 20)
    segundo = Guerrero("B", 100, 10, 20)
    resultado = Combate(primero, segundo).iniciar(mostrar=False)
    assert resultado.startswith("Empate técnico")


def test_getters_y_setters():
    personaje = Guerrero("G", 50, 20, 5)
    personaje.set_nombre("Nuevo")
    personaje.set_vida(40)
    personaje.set_ataque(25)
    personaje.set_defensa(8)
    assert (personaje.get_nombre(), personaje.get_vida(),
            personaje.get_ataque(), personaje.get_defensa()) == ("Nuevo", 40, 25, 8)
