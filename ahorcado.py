import random
import sys
from typing import List, Tuple

MAX_INTENTOS_POR_DEFECTO = 6

PALABRAS_POR_DEFECTO = [
    "PYTHON", "PROGRAMACION", "AHORCADO", "ALGORITMO", "VARIABLE",
    "FUNCION", "ESTUDIANTE", "UNIVERSIDAD", "DATOS", "DESARROLLO"
]

def cargar_palabras_desde_archivo(ruta: str = "palabras.txt") -> List[str]:
    try:
        with open(ruta, encoding="utf-8") as f:
            palabras = [line.strip().upper() for line in f if line.strip()]
        if palabras:
            return palabras
        else:
            return PALABRAS_POR_DEFECTO
    except:
        return PALABRAS_POR_DEFECTO

def seleccionar_palabra(palabras: List[str]) -> str:
    return random.choice(palabras)

def crear_progreso(palabra: str) -> List[str]:
    return ["_" for _ in palabra]

def mostrar_progreso(progreso: List[str]) -> None:
    print("Palabra: " + " ".join(progreso))

def es_entrada_valida(entrada: str) -> bool:
    return len(entrada) == 1 and entrada.isalpha()

def actualizar_progreso_con_letra(palabra: str, progreso: List[str], letra: str) -> int:
    reveladas = 0
    for i, ch in enumerate(palabra):
        if ch == letra and progreso[i] == "_":
            progreso[i] = letra
            reveladas += 1
    return reveladas

def solicitar_letra(letras_usadas: List[str]) -> str:
    while True:
        entrada = input("Ingresa una letra: ").strip().upper()
        if not es_entrada_valida(entrada):
            print("⚠ Debes ingresar solo UNA letra válida (A-Z).")
            continue
        if entrada in letras_usadas:
            print("⚠ Esa letra ya fue ingresada.")
            continue
        return entrada

def mostrar_intentos_restantes(intentos_restantes: int) -> None:
    print(f"Intentos restantes: {intentos_restantes}")

def jugar_una_partida(palabra: str, max_intentos: int = MAX_INTENTOS_POR_DEFECTO) -> Tuple[bool, int]:
    palabra = palabra.upper()
    progreso = crear_progreso(palabra)
    letras_usadas: List[str] = []
    intentos_restantes = max_intentos
    intentos_usados = 0

    print("\n--- Nueva Partida ---")
    mostrar_progreso(progreso)
    mostrar_intentos_restantes(intentos_restantes)

    while "_" in progreso and intentos_restantes > 0:
        letra = solicitar_letra(letras_usadas)
        letras_usadas.append(letra)

        if letra in palabra:
            cantidad = actualizar_progreso_con_letra(palabra, progreso, letra)
            print(f"✔ Correcto, la letra '{letra}' aparece {cantidad} veces.")
        else:
            intentos_restantes -= 1
            intentos_usados += 1
            print(f"✖ La letra '{letra}' no está en la palabra.")
            mostrar_intentos_restantes(intentos_restantes)

        print("Letras usadas:", " ".join(letras_usadas))
        mostrar_progreso(progreso)

    if "_" not in progreso:
        print("\n🎉 Adivinaste la palabra:", palabra)
        return True, intentos_usados
    else:
        print("\n☠️  Perdiste. La palabra era:", palabra)
        return False, intentos_usados

def elegir_dificultad() -> int:
    opciones = {"1": 8, "2": 6, "3": 4}
    print("\nElige dificultad:")
    print("1) Fácil (8 intentos)")
    print("2) Normal (6 intentos)")
    print("3) Difícil (4 intentos)")
    while True:
        elec = input("Opción (1-3) [2]: ").strip() or "2"
        if elec in opciones:
            return opciones[elec]
        else:
            print("Selecciona 1, 2 o 3.")

def resumen_partidas(estados: List[Tuple[bool, int]]) -> None:
    partidas_ganadas = sum(1 for res, _ in estados if res)
    partidas_totales = len(estados)
    print("\n=== Resumen de sesión ===")
    print(f"Partidas jugadas: {partidas_totales}")
    print(f"Partidas ganadas: {partidas_ganadas}")
    for i, (victoria, intentos) in enumerate(estados, 1):
        estado = "Gané" if victoria else "Perdí"
        print(f"Partida {i}: {estado}, fallos: {intentos}")

def main():
    print("=== AHORCADO ===\n")
    palabras = cargar_palabras_desde_archivo()
    max_intentos = elegir_dificultad()
    sesiones: List[Tuple[bool, int]] = []

    while True:
        palabra = seleccionar_palabra(palabras)
        resultado, intentos_usados = jugar_una_partida(palabra, max_intentos)
        sesiones.append((resultado, intentos_usados))

        opcion = input("\n¿Jugar otra partida? (S/N): ").strip().upper()
        if opcion.startswith("N"):
            break

    resumen_partidas(sesiones)
    print("\nFin del programa.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        sys.exit(0)
