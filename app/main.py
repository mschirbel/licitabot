from empresas.dados import carregar_texto_empresa
from contratos.consulta import buscar_contratos
import time

def main():
    time.sleep(60)
    texto_empresa = carregar_texto_empresa()
    buscar_contratos(texto_empresa)

if __name__ == "__main__":
    main()
