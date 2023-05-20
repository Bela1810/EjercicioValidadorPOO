from abc import ABC, abstractmethod
from validadorclave.modelo import errores
from errores import *


class ReglaValidacion(ABC):
    _longitud_esperada: int

    def __init__(self, longitud_esperada: int):
        self.longitud_esperada: int = longitud_esperada

    def _validar_longitud(self, clave: str) -> bool:
        if self.longitud_esperada == 6:
            return len(clave) > self.longitud_esperada
        elif self.longitud_esperada == 8:
            return len(clave) > 8

    def _contiene_mayuscula(self, clave: str) -> bool:
        for letra in clave:
            if letra.isupper():
                return True
            else:
                raise NoTieneLetraMayusculaError("La clave debe contener letras mayusculas")

    def _contiene_minuscula(self, clave: str) -> bool:
        for letra in clave:
            if letra.islower():
                 return True
            else:
                raise NoTieneLetraMinusculaError("La clave debe contener letras minusculas")

    def _contiene_numero(self, clave: str) -> bool:
        for letra in clave:
            if letra.isdigit():
                return True
            else:
                raise NoTieneNumeroError

    @abstractmethod
    def es_valida(self, clave) -> bool:
        raise


class ReglaValidacionGanimedes(ReglaValidacion):
    def __init__(self):
        super().__init__(longitud_esperada=8)
        self.longitud_esperada = 8
        self.reglaValidacion = ReglaValidacion

    def contiene_caracter_especial(self, clave):
        caracteres_especiales = ['@', '_', '#', '$', '%']
        if not any(c in caracteres_especiales for c in clave):
            raise NoTieneCaracterEspecialError("La clave debe contener al menos uno de los siguientes caracteres especiales: @ _ # $ %")

    def es_valida(self, clave) -> bool:
        self._validar_longitud(clave)
        self._contiene_mayuscula(clave)
        self._contiene_minuscula(clave)
        self._contiene_numero(clave)
        self.contiene_caracter_especial(clave)

class ReglaValidacionCalisto(ReglaValidacion):
    def __init__(self):
        super().__init__(longitud_esperada=6)

    def contiene_calisto(self, clave):
        contador_mayusculas = 0
        clave_mayuscula = clave.upper()
        if clave.find(clave_mayuscula):
            for letra in clave:
                if letra.isupper():
                    contador_mayusculas += 1
                if contador_mayusculas >= 2 and contador_mayusculas != len(clave):
                    return True
            return False

    def es_valida(self, clave) -> bool:
        self._validar_longitud(clave)
        self._contiene_mayuscula(clave)
        self._contiene_minuscula(clave)
        self._contiene_numero(clave)
        self.contiene_calisto(clave)


class Validador:
    def __init__(self, regla: ReglaValidacion):
        self.regla = regla

    def es_valida(self, clave):
        return self.regla.es_valida(clave)


