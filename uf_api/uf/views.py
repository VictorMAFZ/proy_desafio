from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import requests

meses = {
    '01': 'Enero',
    '02': 'Febrero',
    '03': 'Marzo',
    '04': 'Abril',
    '05': 'Mayo',
    '06': 'Junio',
    '07': 'Julio',
    '08': 'Agosto',
    '09': 'Septiembre',
    '10': 'Octubre',
    '11': 'Noviembre',
    '12': 'Diciembre'
}


@csrf_exempt
def uf_view(request):
    # Obtener el parámetro fecha de la solicitud GET
    fecha = request.GET.get('fecha')

    # Validar que el parámetro fecha no esté vacío
    if not fecha:
        return JsonResponse({'error': 'Debe proporcionar una fecha.'})

    # Separar la fecha en día, mes y año
    dia, mes, anio = fecha.split('-')

    # Quitar el cero inicial del día, si lo hay
    dia = dia.lstrip('0')

    # Obtener el nombre del mes correspondiente
    nombre_mes = meses[mes]

    # Validar que la fecha no sea anterior a 01-01-2013
    if int(anio) < 2013 or (int(anio) == 2013 and (int(mes) < 1 or (int(mes) == 1 and int(dia) < 1))):
        return JsonResponse({'error': 'La fecha mínima de búsqueda es: 01-01-2013'})

    # Construir la URL para obtener la tabla de valores UF
    url = f'https://www.sii.cl/valores_y_fechas/uf/uf{anio}.htm'

    # Obtener la respuesta de la página web
    response = requests.get(url)

    # Crear un objeto Beautiful Soup para analizar el HTML de la página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar todas las filas de la tabla
    table_rows = soup.find_all('tr')

    # Inicializar una variable auxiliar para almacenar el nombre del mes actual
    aux_mes = ""

    # Recorrer todas las filas de la tabla
    for tr in table_rows:
        # Obtener todas las celdas de encabezado (th) y de datos (td) de la fila
        ths = tr.find_all('th')
        tds = tr.find_all('td')

        # Recorrer todas las celdas de encabezado (th) de la fila
        for i in range(len(ths)):
            # Obtener el texto de la celda de encabezado (th) y de la celda de datos (td) correspondiente
            th_text = ths[i].get_text().strip()
            td_text = tds[i].get_text().strip() if i < len(tds) else ""

            # Si el texto de la celda de encabezado contiene el nombre del mes, almacenarlo en la variable auxiliar
            if nombre_mes in th_text:
                aux_mes = th_text
                continue

            # Si el texto de la celda de encabezado contiene el día y la variable auxiliar no está vacía, devolver el valor de UF correspondiente
            if dia in th_text and aux_mes:
                return JsonResponse({'uf': td_text})

    # Si no se encontró el valor
    return JsonResponse({'error': 'No se encontró el valor de UF para la fecha especificada.'})
