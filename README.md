# OpenData.py
Descarga las bases de datos de la pagina web y las guarda dentro de una capeta madre segun el conjunto de datos al que pertenecen y nos da un archivo
.csv con la informacion de las bases como el autor, fecha de actualizacion, contactos, etc.

# OpenData_Tags.py 
Descarga las bases de datos de la pagina web y las guarda dentro de una capeta madre segun el conjunto de datos al que pertenecen y nos da un archivo
.csv con la informacion de las bases como el autor, fecha de actualizacion, contactos, ademas que tambien extrae la principal etiqueta a la que pertenece
ese conjunto de datos.

# Data_SITREP.py
Recopila los href de la pagina y los almacena en un .csv, luego de eso examina el archivo y va accediendo a cada uno de los links y los descarga. Para la 
descarga utiliza reconocimiento optico de imagenes para lo cual dependerá mucho el navegador y la ventana de "guardar archivo", ya que esto podria cambiar 
según el navegador que se esta o se va a utilizar. Los archivos "Situacion_(SITREP).csv" y con extensión .png también deben ser descargados, en el caso 
de los .png pueden ser reemplazados segun el navegador.
