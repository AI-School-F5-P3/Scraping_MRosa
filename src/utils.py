from datetime import datetime

def transform_date(date_string):
    """
    Transforma una fecha del formato 'Month Day, Year' al formato 'dd-mm-yyyy'.
    
    Args:
    date_string (str): La fecha en formato 'Month Day, Year' (e.g., 'July 31, 1965')
    
    Returns:
    str: La fecha en formato 'dd-mm-yyyy' o None si la conversión falla.
    """
    try:
        # Parsea la fecha de entrada
        date_object = datetime.strptime(date_string, "%B %d, %Y")
        
        # Formatea la fecha al formato deseado
        return date_object.strftime("%d-%m-%Y")
    except ValueError:
        # Si hay un error en el parseo, retorna None
        return None

# # Ejemplo de uso
# input_date = "July 31, 1965"
# formatted_date = transform_date(input_date)

# if formatted_date:
#     print(f"Fecha original: {input_date}")
#     print(f"Fecha transformada: {formatted_date}")
# else:
#     print("Formato de fecha inválido")