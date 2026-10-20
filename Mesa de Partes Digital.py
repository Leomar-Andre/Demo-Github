using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;

namespace SolicitudesUPN
{
    internal class Program
    {
        // Aquí se define la ruta donde se guardará el archivo de solicitudes.
        private static readonly string Archivo =
            Path.Combine(AppContext.BaseDirectory, "solicitudes.txt");

        // Esta lista permite trabajar con todas las solicitudes registradas.
        private static readonly List<Solicitud> Solicitudes =
            new List<Solicitud>();

        static void Main()
        {
            // Permite mostrar correctamente las tildes y otros caracteres.
            Console.OutputEncoding = Encoding.UTF8;

            // Al iniciar, se recuperan las solicitudes guardadas anteriormente.
            CargarSolicitudes();

            bool salir = false;

            // El menú se repite hasta que el usuario decida salir.
            while (!salir)
            {
                Console.WriteLine("\n======================================");
                Console.WriteLine(" SISTEMA DE SOLICITUDES UNIVERSITARIAS");
                Console.WriteLine("======================================");
                Console.WriteLine("1. Registrar solicitud");
                Console.WriteLine("2. Buscar solicitud por código");
                Console.WriteLine("3. Ordenar y listar solicitudes");
                Console.WriteLine("4. Actualizar estado del trámite");
                Console.WriteLine("5. Guardar solicitudes");
                Console.WriteLine("0. Guardar y salir");

                // Se valida que la opción ingresada esté dentro del menú.
                int opcion = LeerEntero(
                    "Selecciona una opción: ", 0, 5);

                // Según la opción elegida, se ejecuta una función diferente.
                switch (opcion)
                {
                    case 1:
                        RegistrarSolicitud();
                        break;

                    case 2:
                        BuscarSolicitud();
                        break;

                    case 3:
                        OrdenarYListar();
                        break;

                    case 4:
                        ActualizarEstado();
                        break;

                    case 5:
                        GuardarSolicitudes();
                        Console.WriteLine(
                            "Solicitudes guardadas correctamente.");
                        break;

                    case 0:
                        // Antes de cerrar, se guardan los datos registrados.
                        GuardarSolicitudes();
                        salir = true;
                        break;
                }
            }

            Console.WriteLine(
                "Programa finalizado. Los datos están guardados.");
        }

        // 1. REGISTRAR Y VALIDAR SOLICITUDES
        private static void RegistrarSolicitud()
        {
            Console.WriteLine("\n--- REGISTRO DE SOLICITUD ---");

            // Se solicita un código para identificar cada trámite.
            string codigo = LeerTexto("Código de solicitud: ");

            // Se comprueba que el código no se encuentre registrado.
            // La comparación no diferencia entre mayúsculas y minúsculas.
            if (Solicitudes.Any(s =>
                s.Codigo.Equals(
                    codigo,
                    StringComparison.OrdinalIgnoreCase)))
            {
                Console.WriteLine(
                    "Error: ya existe una solicitud con ese código.");
                return;
            }

            // Se piden los datos del estudiante y el motivo del trámite.
            string codigoEstudiante =
                LeerTexto("Código del estudiante: ");

            string nombre =
                LeerTexto("Nombres y apellidos del estudiante: ");

            string tipo =
                LeerTexto("Tipo de solicitud: ");

            string descripcion =
                LeerTexto("Descripción de la solicitud: ");

            // Se crea el objeto con los datos ingresados.
            // El estado inicial es "Registrada" y se toma la fecha actual.
            Solicitud nueva = new Solicitud(
                codigo,
                codigoEstudiante,
                nombre,
                tipo,
                descripcion,
                "Registrada",
                DateTime.Now
            );

            // Se agrega la nueva solicitud a la lista.
            Solicitudes.Add(nueva);

            // Se guarda para no perder la información registrada.
            GuardarSolicitudes();

            Console.WriteLine(
                "Solicitud registrada correctamente.");
        }

        // 2. BUSCAR UNA SOLICITUD POR SU CÓDIGO
        private static void BuscarSolicitud()
        {
            Console.Write("\nCódigo de solicitud: ");

            // Se lee el código y se quitan los espacios de los extremos.
            string codigo =
                (Console.ReadLine() ?? "").Trim();

            // Se busca en la lista la solicitud que tenga ese código.
            Solicitud solicitud = Solicitudes.FirstOrDefault(s =>
                s.Codigo.Equals(
                    codigo,
                    StringComparison.OrdinalIgnoreCase));

            // Si no existe, se informa al usuario y termina la búsqueda.
            if (solicitud == null)
            {
                Console.WriteLine(
                    "No se encontró una solicitud con ese código.");
                return;
            }

            // Si se encuentra, se muestran todos sus datos.
            MostrarSolicitud(solicitud);
        }

        // 3. ORDENAR Y LISTAR SOLICITUDES
        private static void OrdenarYListar()
        {
            // Se verifica si hay información antes de listar.
            if (Solicitudes.Count == 0)
            {
                Console.WriteLine(
                    "Todavía no hay solicitudes registradas.");
                return;
            }

            // Se utiliza el algoritmo de ordenamiento por inserción.
            // Este método compara los códigos y coloca cada solicitud
            // en la posición que le corresponde dentro de la lista.
            for (int i = 1; i < Solicitudes.Count; i++)
            {
                Solicitud actual = Solicitudes[i];
                int j = i - 1;

                // Se desplazan los elementos mayores hacia la derecha
                // hasta encontrar la posición correcta del elemento actual.
                while (j >= 0 &&
                    string.Compare(
                        Solicitudes[j].Codigo,
                        actual.Codigo,
                        StringComparison.OrdinalIgnoreCase) > 0)
                {
                    Solicitudes[j + 1] = Solicitudes[j];
                    j--;
                }

                // Se coloca la solicitud en su posición ordenada.
                Solicitudes[j + 1] = actual;
            }

            Console.WriteLine(
                "\n--- SOLICITUDES ORDENADAS POR CÓDIGO ---");

            // Se recorre la lista para mostrar cada solicitud.
            foreach (Solicitud solicitud in Solicitudes)
            {
                MostrarSolicitud(solicitud);
            }

            // Se guardan los datos después de ordenar la lista.
            GuardarSolicitudes();
        }

        // 4. ACTUALIZAR EL ESTADO DE UN TRÁMITE
        private static void ActualizarEstado()
        {
            Console.Write("\nCódigo de solicitud a actualizar: ");

            // Se ingresa el código del trámite que se desea modificar.
            string codigo =
                (Console.ReadLine() ?? "").Trim();

            // Se busca la solicitud que se va a actualizar.
            Solicitud solicitud = Solicitudes.FirstOrDefault(s =>
                s.Codigo.Equals(
                    codigo,
                    StringComparison.OrdinalIgnoreCase));

            // Si el código no existe, no se realiza ningún cambio.
            if (solicitud == null)
            {
                Console.WriteLine(
                    "No se encontró esa solicitud.");
                return;
            }

            // Se muestran los estados disponibles para el trámite.
            Console.WriteLine("\nEstados disponibles:");
            Console.WriteLine("1. Registrada");
            Console.WriteLine("2. En revisión");
            Console.WriteLine("3. Observada");
            Console.WriteLine("4. Aprobada");
            Console.WriteLine("5. Rechazada");
            Console.WriteLine("6. Finalizada");

            // Se valida que el usuario elija un estado permitido.
            int opcion = LeerEntero(
                "Selecciona el nuevo estado: ", 1, 6);

            // Se actualiza el estado según la opción seleccionada.
            switch (opcion)
            {
                case 1:
                    solicitud.Estado = "Registrada";
                    break;

                case 2:
                    solicitud.Estado = "En revisión";
                    break;

                case 3:
                    solicitud.Estado = "Observada";
                    break;

                case 4:
                    solicitud.Estado = "Aprobada";
                    break;

                case 5:
                    solicitud.Estado = "Rechazada";
                    break;

                case 6:
                    solicitud.Estado = "Finalizada";
                    break;
            }

            // Se guarda el cambio para que se mantenga al cerrar el programa.
            GuardarSolicitudes();

            Console.WriteLine(
                "Estado actualizado correctamente: " +
                solicitud.Estado);
        }

        // 5. GUARDAR SOLICITUDES EN EL ARCHIVO
        private static void GuardarSolicitudes()
        {
            try
            {
                // Se obtiene la carpeta donde se encuentra el archivo.
                string carpeta =
                    Path.GetDirectoryName(Archivo);

                // Si la carpeta no existe, se crea antes de guardar.
                if (!string.IsNullOrEmpty(carpeta))
                {
                    Directory.CreateDirectory(carpeta);
                }

                // Cada solicitud se convierte en una línea de texto.
                // WriteAllLines escribe la información de toda la lista.
                File.WriteAllLines(
                    Archivo,
                    Solicitudes.Select(s => s.ToLinea()),
                    Encoding.UTF8
                );
            }
            // Se controlan los errores relacionados con el acceso al archivo.
            catch (Exception ex) when (
                ex is IOException ||
                ex is UnauthorizedAccessException)
            {
                Console.WriteLine(
                    "Error al guardar el archivo: " + ex.Message);
            }
        }

        // 6. CARGAR LOS DATOS AL INICIAR EL PROGRAMA
        private static void CargarSolicitudes()
        {
            // Si el archivo todavía no existe, no hay datos que cargar.
            if (!File.Exists(Archivo))
            {
                return;
            }

            try
            {
                // Se lee el archivo línea por línea para recuperar los datos.
                foreach (string linea in
                    File.ReadAllLines(Archivo, Encoding.UTF8))
                {
                    // Cada línea se convierte nuevamente en una solicitud.
                    Solicitud solicitud =
                        Solicitud.DesdeLinea(linea);

                    // Se agrega solo si los datos son válidos
                    // y el código todavía no está en la lista.
                    if (solicitud != null &&
                        !Solicitudes.Any(s =>
                            s.Codigo.Equals(
                                solicitud.Codigo,
                                StringComparison.OrdinalIgnoreCase)))
                    {
                        Solicitudes.Add(solicitud);
                    }
                }
            }
            // Se informa si ocurre algún problema al leer el archivo.
            catch (Exception ex) when (
                ex is IOException ||
                ex is UnauthorizedAccessException)
            {
                Console.WriteLine(
                    "Error al cargar solicitudes: " + ex.Message);
            }
        }

        // MÉTODO PARA MOSTRAR LOS DATOS DE UNA SOLICITUD
        private static void MostrarSolicitud(Solicitud s)
        {
            // Se imprime cada campo para facilitar la consulta del trámite.
            Console.WriteLine("--------------------------------------");
            Console.WriteLine(
                "Código de solicitud : " + s.Codigo);
            Console.WriteLine(
                "Código estudiante   : " + s.CodigoEstudiante);
            Console.WriteLine(
                "Estudiante          : " + s.NombreEstudiante);
            Console.WriteLine(
                "Tipo                : " + s.TipoSolicitud);
            Console.WriteLine(
                "Descripción         : " + s.Descripcion);
            Console.WriteLine(
                "Estado              : " + s.Estado);
            Console.WriteLine(
                "Fecha de registro   : " +
                s.FechaRegistro.ToString("dd/MM/yyyy HH:mm"));
        }

        // MÉTODO PARA VALIDAR LOS CAMPOS OBLIGATORIOS
        private static string LeerTexto(string mensaje)
        {
            // Se repite la pregunta hasta que el usuario ingrese un dato válido.
            while (true)
            {
                Console.Write(mensaje);

                // Se lee el texto y se eliminan los espacios de los extremos.
                string valor =
                    (Console.ReadLine() ?? "").Trim();

                // No se permiten campos vacíos.
                if (string.IsNullOrWhiteSpace(valor))
                {
                    Console.WriteLine(
                        "El campo es obligatorio.");
                    continue;
                }

                // Se evita el uso de "|" porque sirve para separar los campos
                // al guardar la información en el archivo.
                if (valor.Contains("|"))
                {
                    Console.WriteLine(
                        "No utilices el carácter | en el texto.");
                    continue;
                }

                // Si pasa las validaciones, se devuelve el dato ingresado.
                return valor;
            }
        }

        // MÉTODO PARA VALIDAR LAS OPCIONES NUMÉRICAS DEL MENÚ
        private static int LeerEntero(
            string mensaje, int minimo, int maximo)
        {
            // Se vuelve a pedir el número si no cumple con las condiciones.
            while (true)
            {
                Console.Write(mensaje);

                // TryParse comprueba que la entrada sea un número entero
                // y que esté dentro del rango permitido.
                if (int.TryParse(
                    Console.ReadLine(), out int numero) &&
                    numero >= minimo &&
                    numero <= maximo)
                {
                    return numero;
                }

                // Se muestra el rango correcto cuando hay un error.
                Console.WriteLine(
                    "Ingresa un número entre " +
                    minimo + " y " + maximo + ".");
            }
        }
    }

    // CLASE QUE REPRESENTA LOS DATOS DE CADA SOLICITUD
    internal class Solicitud
    {
        // Estas propiedades guardan la información de cada trámite.
        // Los campos privados de escritura evitan modificarlos directamente
        // desde otras clases, excepto el estado, que sí puede actualizarse.
        public string Codigo { get; private set; }
        public string CodigoEstudiante { get; private set; }
        public string NombreEstudiante { get; private set; }
        public string TipoSolicitud { get; private set; }
        public string Descripcion { get; private set; }
        public string Estado { get; set; }
        public DateTime FechaRegistro { get; private set; }

        // El constructor recibe los datos y los asigna al nuevo objeto.
        public Solicitud(
            string codigo,
            string codigoEstudiante,
            string nombreEstudiante,
            string tipoSolicitud,
            string descripcion,
            string estado,
            DateTime fechaRegistro)
        {
            Codigo = codigo;
            CodigoEstudiante = codigoEstudiante;
            NombreEstudiante = nombreEstudiante;
            TipoSolicitud = tipoSolicitud;
            Descripcion = descripcion;
            Estado = estado;
            FechaRegistro = fechaRegistro;
        }

        // Convierte los datos de la solicitud en una sola línea de texto.
        // Así se pueden almacenar en el archivo solicitudes.txt.
        public string ToLinea()
        {
            return string.Join("|",
                Codificar(Codigo),
                Codificar(CodigoEstudiante),
                Codificar(NombreEstudiante),
                Codificar(TipoSolicitud),
                Codificar(Descripcion),
                Codificar(Estado),
                FechaRegistro.ToString(
                    "O", CultureInfo.InvariantCulture));
        }

        // Recupera los datos de una línea del archivo
        // y los convierte nuevamente en un objeto Solicitud.
        public static Solicitud DesdeLinea(string linea)
        {
            // Se separan los campos utilizando el carácter "|".
            string[] p = linea.Split('|');

            // Cada registro debe contener exactamente siete campos.
            if (p.Length != 7)
            {
                return null;
            }

            // Se comprueba que la fecha tenga un formato válido.
            if (!DateTime.TryParse(
                p[6],
                CultureInfo.InvariantCulture,
                DateTimeStyles.RoundtripKind,
                out DateTime fecha))
            {
                return null;
            }

            try
            {
                // Se decodifica cada campo y se crea el objeto recuperado.
                return new Solicitud(
                    Decodificar(p[0]),
                    Decodificar(p[1]),
                    Decodificar(p[2]),
                    Decodificar(p[3]),
                    Decodificar(p[4]),
                    Decodificar(p[5]),
                    fecha
                );
            }
            // Si algún dato no está codificado correctamente, se descarta.
            catch (FormatException)
            {
                return null;
            }
        }

        // Codifica el texto en Base64 para almacenarlo en el archivo.
        // Esto evita que los caracteres de los datos se confundan
        // con el separador utilizado para dividir los campos.
        private static string Codificar(string valor)
        {
            return Convert.ToBase64String(
                Encoding.UTF8.GetBytes(valor));
        }

        // Convierte el texto codificado en Base64 a su valor original.
        private static string Decodificar(string valor)
        {
            return Encoding.UTF8.GetString(
                Convert.FromBase64String(valor));
        }
    }
}
