
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000L")
db = cluster["MongoDB"]
col = db["Diccionario"]


def verif(Palabra):
    verificar = col.find_one(
        {"palabra": Palabra})
    if verificar is None:
        return False
    else:
        return True


def editSlang(prevSlang, newSlang, newDef):
    col.update_one({"palabra": prevSlang}, {"$set": {
        "palabra": newSlang,
        "definicion": newDef
    }})


def delSlang(slang):
    col.delete_one({"palabra": slang})


def get_slangs():
    print("\n--------Diccionario de Slangs--------\n")
    palabras = col.find()
    i = 0
    for row in palabras:
        i = i + 1
        print(
            f'{i}. Slang: {row["palabra"]} Definición: {row["definicion"]}')


def menu():
    men = """
    ¡Bienvenido/a!\n 
    1). Agregar nuevo slang 
    2). Editar slang 
    3). Eliminar slang 
    4). Ver diccionario 
    5). Buscar definición 
    6). Salir
    Seleccione una opción: """
    opt = 0
    while opt != 6:
        opt = int(input(men))
        if opt == 1:
            inputSlang = input("\nIngrese palabra a agregar:\n")
            inputSlang = inputSlang.capitalize()
            inputDef = input("\nIngrese definición:\n")
            if len(inputSlang) and len(inputDef):
                if verif(inputSlang):
                    print(f"El slang '{inputSlang}' ya existe")
                else:
                    col.insert_one({
                        "palabra": inputSlang,
                        "definicion": inputDef
                    })
                    print("¡Slang agregado con éxito!")
            else:
                print("\n Favor introducir los datos requeridos")

        elif opt == 2:
            inputSlang = input("\nIngrese el slang que desea modificar: \n")
            inputSlang = inputSlang.capitalize()
            new = input("\nIngrese el nuevo slang: ")
            inputDef = input("\nIngrese el nuevo significado del slang: ")
            if len(new) and len(inputDef) and len(inputSlang):
                if verif(inputSlang):
                    editSlang(inputSlang, new, inputDef)
                    print("¡Slang editado con éxito!")
                else:
                    print("\n Este slang no existe. Puede agregarlo presionando 1 en el menú.")
            else:
                print("\n Favor introducir los datos requeridos")
        elif opt == 3:
            inputSlang = input("\n ¿Qué palabra desea eliminar?: ")
            inputSlang = inputSlang.capitalize()
            if len(inputSlang):
                if verif(inputSlang):
                    delSlang(inputSlang)
                    print(f"El slang '{inputSlang}' ha sido eliminado")
                else:
                    print("\n La palabra no existe!")
            else:
                print("\n Por favor llenar los campos de informacion")
        elif opt == 4:
            get_slangs()
        elif opt == 5:
            inputSlang = input("\n ¿Qué significado deseas saber?: ")
            inputSlang = inputSlang.capitalize()
            if len(inputSlang):
                if verif(inputSlang):
                    getSlang = col.find_one({"palabra": inputSlang})
                    print(f'La definicion es: {getSlang["definicion"]}')
                else:
                    print("\n La palabra no existe.")
            else:
                print("\n Por favor llenar los campos de informacion")
        elif opt == 6:
            exit()
        else:
            print("\n Opción inválida \n")


if __name__ == "__main__":
    menu()
