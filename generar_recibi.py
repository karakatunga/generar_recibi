import os
import sys
import pandas as pd
from docxtpl import DocxTemplate
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import locale
from typing import Tuple, Dict, Optional
from dateutil.relativedelta import relativedelta
from tkinter import PhotoImage

def resource_path(relative_path):
    """Obtener la ruta absoluta al recurso, funciona tanto en el script como en el ejecutable."""
    try:
        # PyInstaller crea una carpeta temporal y almacena el archivo en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class DocumentGenerator:
    def __init__(self):
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'spanish')
            except locale.Error:
                messagebox.showwarning("Advertencia", "No se pudo configurar el idioma español para las fechas.")

        self.df = None
        self.df_oculta = None
        self.setup_constants()
        self.init_ui()

    def setup_constants(self):
        """Initialize constant values and mappings used in the application."""
        self.WIDGET_WIDTH = 40
        self.EDAD_MAYORIA = 18
        
        self.codigos_ayuda_descripcion = {
            "1FGBI": "Gastos de bolsillo",
            "1FGBM": "Gastos de bolsillo menores 18 años",
            "1FMI": "Manutención UC 1",
            "1FMUC2": "Manutención UC 2",
            "1FMUC3": "Manutención UC 3",
            "1FMUC4": "Manutención UC 4",
            "1FMUC5": "Manutención UC 5",
            "1FMUC6": "Manutención UC 6",
            "1FMUC7": "Manutención UC 7",
            "1FMUC8": "Manutención UC 8",
            "1FMUC9": "Manutención UC 9 o más",
            "ATNH": "Nacimiento hijos/as",
            "ATSANMED": "Medicamentos",
            "ATSANGA": "Gafas",
            "ATSANMO": "Material ortoprotésico",
            "ATSANTDE": "Tratamientos dentales",
            "ATSANPR": "Prótesis dentales removibles",
            "ATVES": "Adquisición vestuario",
            "ATTPINCO": "Transporte Incorporación dispositivo",
            "ATTPTIN": "Transporte Intraprovincial",
            "ATTPTEXT": "Transporte Intraprovincial",
            "ATTPTEXA": "Transporte Intraprovincial",
            "ATTPTEXM": "Transporte Intraprovincial",
            "ATEDUGUME": "Guardería Mensualidad",
            "ATEDUGUMA": "Guardería Matrícula",
            "ATEDURMA": "Educación reglada Matrícula",
            "ATEDURMATE": "Educación reglada Material escolar",
            "ATEDURUNI": "Educación reglada Uniformes escolares",
            "ATEDURCOM": "Educación reglada Comedor escolar",
            "ATEDUREXTR": "Educación reglada Actividades extraescolares",
            "ATEDURTPT": "Educación reglada Transporte escolar",
            "ATEDURSEO": "Educación reglada Seguro escolar obligatorio",
            "ATEDURAMPA": "Educación reglada AMPA",
            "ATCONMM": "Contextualiz y habilidades sociales Matrícula y/o mensualidades",
            "ATCONMAT": "Contextualiz y habilidades sociales Material didáctico",
            "ATOCCAMP": "Campamentos de verano infantil y juvenil",
            "ATDOCU": "Obtención de documentos",
            "ATREADOCU": "Reagrupación familiar Obtención de documentos",
            "ATREALLEG": "Reagrupación familiar Viajes, traslados, estancias para llegar a España",
            "ATREAESTA": "Reagrupación familiar Viajes, traslados, estancias en España",
            "ATEMPEDUGUME": "Empleo Facilitar formación Mensualidad guardería",
            "ATEMPEDUGUMA": "Empleo Facilitar formación Matrícula de guardería",
            "ATEMPEDUCOM": "Empleo Facilitar formación Comedor escolar",
            "ATPREMAME": "Empleo Preformación Matrícula y/o mensualidades",
            "ATPREMAT": "Empleo Preformación Material didáctico",
            "ATFORMAME": "Empleo Formación ocupacional Matrícula y/o mensualidades",
            "ATFORMAT": "Empleo Formación ocupacional Material didáctico para la formación",
            "ATTPT": "Empleo Transporte asistencia cursos o búsqueda empleo",
            "ATEHT": "Empleo Obtención documentos (expedición, homologación, tramitación…)",
            "2FNB1": "Necesidades básicas UC1",
            "2FNB2": "Necesidades básicas UC2",
            "2FNB3": "Necesidades básicas UC3",
            "2FNB4": "Necesidades básicas UC4",
            "2FNB5": "Necesidades básicas UC5",
            "2FNB6": "Necesidades básicas UC6",
            "2FNB7": "Necesidades básicas UC7",
            "2FNB8": "Necesidades básicas UC8",
            "2FNB9": "Necesidades básicas UC9 o más",
            "2FAV1": "Alquiler UC1",
            "2FAV2": "Alquiler UC2",
            "2FAV3": "Alquiler UC3",
            "2FAV4": "Alquiler UC4",
            "2FAV5": "Alquiler UC5",
            "2FAV6": "Alquiler UC6",
            "2FAV7": "Alquiler UC7",
            "2FAV8": "Alquiler UC8",
            "2FAV9": "Alquiler UC9 o más"
        }
        
        # Diccionario de cuantías predefinidas
        self.cuantias_predefinidas = {
            "1FGBI": 56,
            "1FGBM": 22,
            "1FMI": 226,
            "1FMUC2": 338,
            "1FMUC3": 362,
            "1FMUC4": 386,
            "1FMUC5": 454,
            "1FMUC6": 504,
            "1FMUC7": 555,
            "1FMUC8": 604,
            "1FMUC9": 654,
            "ATNH": 201,
            "ATSANGA": 200,
            "ATVES": 100,      
            "ATSANTDE": 400,
            "ATEDURMATE": 279,
            "ATEDUREXTR": 33,
            "ATCONMM": 600,
            "ATCONMAT": 100,
            "ATOCCAMP": 223,
            "ATPREMAME": 1364,
            "ATPREMAT": 250,
            "ATFORMAME": 1364,
            "ATFORMAT": 250,
            "2FNB1": 466,
            "2FNB2": 692,
            "2FNB3": 758,
            "2FNB4": 825,
            "2FNB5": 891,
            "2FNB6": 958,
            "2FNB7": 1024,
            "2FNB8": 1091,
            "2FNB9": 1157,
            "2FAV1": 445,
            "2FAV2": 578,
            "2FAV3": 668,
            "2FAV4": 758,
            "2FAV5": 848,
            "2FAV6": 848,
            "2FAV7": 848,
            "2FAV8": 923,
            "2FAV9": 923,
        }

        # Imprimir las cuantías predefinidas y sus valores
        print("Cuantías predefinidas:")
        for codigo, cuantia in self.cuantias_predefinidas.items():
            print(f"Código: {codigo}, Cuantía: {cuantia}")

        self.maximos_ayuda = {
            "1FGBI": 56,
            "1FGBM": 22,
            "1FMI": 226,
            "1FMUC2": 338,
            "1FMUC3": 362,
            "1FMUC4": 386,
            "1FMUC5": 454,
            "1FMUC6": 504,
            "1FMUC7": 555,
            "1FMUC8": 604,
            "1FMUC9": 654,
            "ATNH": 201,
            "ATSANGA": 200,
            "ATVES": 100,      
            "ATSANTDE": 400,
            "ATEDURMATE": 279,
            "ATEDUREXTR": 33,
            "ATCONMM": 600,
            "ATCONMAT": 100,
            "ATOCCAMP": 223,
            "ATPREMAME": 1364,
            "ATPREMAT": 250,
            "ATFORMAME": 1364,
            "ATFORMAT": 250,
            "2FNB1": 466,
            "2FNB2": 692,
            "2FNB3": 758,
            "2FNB4": 825,
            "2FNB5": 891,
            "2FNB6": 958,
            "2FNB7": 1024,
            "2FNB8": 1091,
            "2FNB9": 1157,
            "2FAV1": 445,
            "2FAV2": 578,
            "2FAV3": 668,
            "2FAV4": 758,
            "2FAV5": 848,
            "2FAV6": 848,
            "2FAV7": 848,
            "2FAV8": 923,
            "2FAV9": 923,
        }

    def load_excel_file(self) -> bool:
        """Load Excel file and return success status."""
        archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if not archivo:
            messagebox.showerror("Error", "No se seleccionó ningún archivo.")
            return False

        try:
            self.df = pd.read_excel(archivo, header=4)
            self.df_oculta = pd.read_excel(archivo, sheet_name='LISTADOS (no tocar)', header=None)
            self.df['Nº SIRIA BENEFICIARIA/O'] = self.df['Nº SIRIA BENEFICIARIA/O'].astype(str)
            self.load_professional_values()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo Excel: {str(e)}")
            return False

    def load_professional_values(self):
        """Load professional values from hidden sheet."""
        valores_b = self.df_oculta.iloc[3:7, 1].dropna().tolist()
        valores_c = self.df_oculta.iloc[3:7, 2].dropna().tolist()
        self.valores_combined = valores_b + valores_c
        self.valor_combobox['values'] = self.valores_combined
        
        # Imprimir para depuración
        print(f"Valores de profesionales cargados: {self.valores_combined}")

    def calculate_age(self, birthdate) -> Optional[int]:
        """Calculate age from birthdate."""
        if pd.isna(birthdate):
            return None
        try:
            return relativedelta(datetime.now(), pd.to_datetime(birthdate)).years
        except:
            return None

    def is_minor(self, numero_siria: str) -> Tuple[bool, Optional[pd.Timestamp], Optional[str]]:
        """Check if a person is a minor and return their titular's SIRIA number if available."""
        persona = self.df[self.df['Nº SIRIA BENEFICIARIA/O'] == numero_siria]
        if persona.empty:
            return False, None, None
        
        fecha_nacimiento = persona.iloc[0]['FECHA NACIMIENTO']
        siria_titular = persona.iloc[0]['Nº DE SIRIA TITULAR UNIDAD FAMILIAR']
        
        if pd.isna(fecha_nacimiento):
            return False, None, None
            
        age = self.calculate_age(fecha_nacimiento)
        return (age is not None and age < self.EDAD_MAYORIA), fecha_nacimiento, siria_titular

    def init_ui(self):
        """Initialize the user interface."""
        self.root = tk.Tk()
        self.root.title("Generador de Documentos")
        
        # Cambiar el icono de la ventana usando un archivo ICO
        self.root.iconbitmap(resource_path("mi_icono.ico"))  # Asegúrate de que la ruta sea correcta
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.create_input_fields(main_frame)
        self.create_buttons(main_frame)

        if not self.load_excel_file():
            self.root.quit()

        # Llamar a calculate_copago para mostrar la descripción de la ayuda seleccionada por defecto
        self.calculate_copago()

    def create_input_fields(self, parent):
        """Create input fields for the form."""
        print("Método create_input_fields llamado.")  # Mensaje de depuración
        # SIRIA number input
        ttk.Label(parent, text="Número de SIRIA:").grid(column=0, row=0, sticky=tk.W)
        self.numero_siria_entry = ttk.Entry(parent, width=self.WIDGET_WIDTH)
        self.numero_siria_entry.grid(column=1, row=0, padx=5, pady=5)

        # Ayuda code selection
        ttk.Label(parent, text="Código de ayuda:").grid(column=0, row=1, sticky=tk.W)
        self.codigo_ayuda_combobox = ttk.Combobox(
            parent, 
            values=list(self.codigos_ayuda_descripcion.keys()), 
            state="readonly", 
            width=self.WIDGET_WIDTH-2
        )
        self.codigo_ayuda_combobox.grid(column=1, row=1, padx=5, pady=5)
        self.codigo_ayuda_combobox.current(0)

        # Cuantía de ayuda
        ttk.Label(parent, text="Cuantía de ayuda:").grid(column=0, row=2, sticky=tk.W)
        self.cuantia_ayuda_entry = ttk.Entry(parent, width=self.WIDGET_WIDTH)
        self.cuantia_ayuda_entry.grid(column=1, row=2, padx=5, pady=5)

        # Botón "Máximo" y etiqueta de copago en la misma línea
        copago_frame = ttk.Frame(parent)
        copago_frame.grid(column=0, row=3, columnspan=2, pady=5, sticky=tk.W)

        ttk.Button(copago_frame, text="Máximo", command=self.set_max_cuantia).pack(side=tk.LEFT, padx=5)
        
        # Etiqueta de copago centrada hacia la derecha
        self.copago_label = ttk.Label(copago_frame, text="")
        self.copago_label.pack(side=tk.LEFT, padx=(20, 5))
        
        # Añadir evento para calcular copago al cambiar la cuantía
        self.cuantia_ayuda_entry.bind("<KeyRelease>", self.calculate_copago)

        # Profesional selection
        ttk.Label(parent, text="Profesional:").grid(column=0, row=4, sticky=tk.W)
        self.valor_combobox = ttk.Combobox(
            parent,
            state="readonly",
            width=self.WIDGET_WIDTH-2
        )
        self.valor_combobox.grid(column=1, row=4, padx=5, pady=5)

        # Añadir evento para calcular copago
        self.codigo_ayuda_combobox.bind("<<ComboboxSelected>>", lambda e: self.calculate_copago())

        # Payment method
        ttk.Label(parent, text="Método de pago:").grid(column=0, row=5, sticky=tk.W)
        self.payment_method_var = tk.StringVar(value="Efectivo")
        payment_frame = ttk.Frame(parent)
        payment_frame.grid(column=1, row=5, padx=5, pady=5)
        ttk.Radiobutton(
            payment_frame, 
            text="Efectivo", 
            variable=self.payment_method_var, 
            value="Efectivo"
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(
            payment_frame, 
            text="Banco", 
            variable=self.payment_method_var, 
            value="Banco"
        ).pack(side=tk.LEFT)

    def create_buttons(self, parent):
        """Create action buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(column=0, row=6, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame,
            text="Generar recibí",
            command=self.generate_document
        ).pack(expand=True)

    def prompt_for_titular(self) -> Optional[str]:
        """Prompt user for titular's SIRIA number."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Información del Titular")
        dialog.transient(self.root)
        dialog.grab_set()

        result = tk.StringVar()
        
        ttk.Label(
            dialog,
            text="El beneficiario es menor de edad.\nPor favor, introduce el número de SIRIA del titular:"
        ).pack(pady=10, padx=10)
        
        entry = ttk.Entry(dialog, width=30)
        entry.pack(pady=10, padx=10)

        def on_ok():
            result.set(entry.get())
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        ttk.Button(dialog, text="Aceptar", command=on_ok).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(dialog, text="Cancelar", command=on_cancel).pack(side=tk.RIGHT, padx=10, pady=10)

        # Centrar el diálogo en la pantalla
        dialog.geometry("+%d+%d" % (
            dialog.winfo_screenwidth()/2 - dialog.winfo_reqwidth()/2,
            dialog.winfo_screenheight()/2 - dialog.winfo_reqheight()/2))

        dialog.wait_window()
        return result.get()

    def get_person_data(self, numero_siria: str, is_titular: bool = True) -> Optional[Dict]:
        """Retrieve person data from DataFrame with role-specific field names."""
        personas_filtradas = self.df[self.df['Nº SIRIA BENEFICIARIA/O'] == numero_siria]
        if personas_filtradas.empty:
            return None
        
        persona = personas_filtradas.iloc[0]
        prefix = 'titular_' if is_titular else 'menor_'
        
        # Formatear la fecha de nacimiento
        fecha_nacimiento = persona['FECHA NACIMIENTO']
        if pd.notna(fecha_nacimiento):
            fecha_nacimiento = pd.to_datetime(fecha_nacimiento).strftime('%d-%m-%Y')
        
        # Determinar el tipo de protección
        tipo_proteccion = persona['SITUACIÓN LEGAL/ADMINISTRATIVA ACTUAL']
        
        # Imprimir para depuración
        print(f"\nTipo de protección encontrado: '{tipo_proteccion}'")
        
        data = {
            f'{prefix}nombre': persona['NOMBRE'],
            f'{prefix}apellidos': persona['APELLIDOS'],
            f'{prefix}nie': persona['NÚMERO NIE'],
            f'{prefix}caducidad_nie': persona['CADUCIDAD NIE '],
            f'{prefix}numero_siria_beneficiaria': persona['Nº SIRIA BENEFICIARIA/O'],
            f'{prefix}numero_siria_uc': persona['Nº SIRIA  UNIDAD CONVIVENCIAL (SI APLICA)'],
            f'{prefix}numero_siria_uf': persona['Nº DE SIRIA TITULAR UNIDAD FAMILIAR'],
            f'{prefix}oar': persona['Nº EXPEDIENTE OAR'],
            f'{prefix}fecha_nacimiento': fecha_nacimiento,
            
            # Campos para la tabla de tipo de protección
            'sol_pi': 'X' if tipo_proteccion == 'Solicitante Protección Internacional' else '',
            'ben_pi': 'X' if tipo_proteccion == 'Beneficiario/a Estatuto Refugiado/a' else '',
            'ben_ps': 'X' if tipo_proteccion == 'Beneficiario/a Protección Subsidiaria' else '',
            'sol_ap': 'X' if tipo_proteccion == 'Solicitante Estatuto de Apátrida' else '',
            'apatrida': 'X' if tipo_proteccion == 'Apátrida' else '',
            'sol_ben_pt': 'X' if (tipo_proteccion == 'Solicitante Protección Temporal' or 
                                 tipo_proteccion == 'Beneficiario/a Protección Temporal') else ''
        }
        
        # Añadir el placeholder "Hijo/a" si es menor
        if not is_titular:
            data['relacion_familiar'] = "Hijo/a"
        
        return data

    def validate_input(self) -> Tuple[bool, str]:
        """Validate user input and return (is_valid, error_message)."""
        numero_siria = self.numero_siria_entry.get()
        codigo_ayuda = self.codigo_ayuda_combobox.get()
        cuantia_str = self.cuantia_ayuda_entry.get().replace(',', '.')

        if not all([numero_siria, codigo_ayuda, cuantia_str]):
            return False, "Por favor, introduce todos los datos necesarios."

        try:
            cuantia = float(cuantia_str)
            if codigo_ayuda in self.maximos_ayuda and cuantia > self.maximos_ayuda[codigo_ayuda]:
                return False, f"La cuantía para la ayuda {codigo_ayuda} no puede superar los {self.maximos_ayuda[codigo_ayuda]} euros."
        except ValueError:
            return False, "Por favor, introduce una cuantía válida en euros."

        return True, ""

    def generate_document(self):
        """Generate the document based on user input."""
        is_valid, error_message = self.validate_input()
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return

        # Obtener el número de SIRIA y eliminar espacios
        numero_siria = self.numero_siria_entry.get().strip().replace(" ", "")  # Ignorar espacios
        is_minor, fecha_nacimiento, siria_titular = self.is_minor(numero_siria)
        
        # Preparar los datos del contexto
        context = {}
        
        if is_minor:
            numero_siria_titular = None
            
            # Si hay un número de SIRIA del titular en el Excel
            if pd.notna(siria_titular):
                # Preguntar al usuario si el número es correcto
                if messagebox.askyesno("Confirmar titular", 
                    f"Esta persona es menor de edad.\nSe ha encontrado el número de SIRIA de la titular: {siria_titular}\n¿Es correcto?"):
                    numero_siria_titular = str(siria_titular)
            
            # Si no hay número de SIRIA o el usuario indica que no es correcto, solicitarlo manualmente
            if not numero_siria_titular:
                numero_siria_titular = self.prompt_for_titular()
                
            if not numero_siria_titular:
                messagebox.showerror("Error", "Se requiere el número SIRIA del titular para menores de edad.")
                return
                
            # Obtener datos del titular
            datos_titular = self.get_person_data(numero_siria_titular, is_titular=True)
            if not datos_titular:
                messagebox.showerror("Error", "No se encontraron los datos del titular.")
                return
                
            # Obtener datos del menor
            datos_menor = self.get_person_data(numero_siria, is_titular=False)
            if not datos_menor:
                messagebox.showerror("Error", "No se encontraron los datos del menor.")
                return
                
            # Combinar datos en el contexto
            context.update(datos_titular)
            context.update(datos_menor)
            context['relacion_familiar'] = "Hijo/a"
        else:
            # Si es adulto
            datos_persona = self.get_person_data(numero_siria, is_titular=True)
            if not datos_persona:
                messagebox.showerror("Error", "No se encontraron los datos de la persona.")
                return
            context.update(datos_persona)
            context['relacion_familiar'] = ""

        # Añadir datos adicionales al contexto
        context.update({
            'codigo_ayuda': self.codigo_ayuda_combobox.get(),
            'descripcion_ayuda': self.codigos_ayuda_descripcion[self.codigo_ayuda_combobox.get()],
            'cuantia': self.cuantia_ayuda_entry.get(),
            'profesional': self.valor_combobox.get(),
            'metodo_pago': self.payment_method_var.get(),
            'fecha_actual': datetime.now().strftime("%d de %B de %Y")
        })

        # Calcular el copago si es necesario
        codigo_ayuda = self.codigo_ayuda_combobox.get()
        if codigo_ayuda in ["ATSANGA", "ATSANTDE"]:  # Verifica si la ayuda requiere copago
            try:
                cuantia = float(self.cuantia_ayuda_entry.get().replace(',', '.'))
                copago = cuantia * 0.15
                cuantia_final = cuantia - copago
                context['cuantia'] = f"{cuantia_final:.2f}"  # Actualizar la cuantía en el contexto sin el símbolo 
            except ValueError:
                context['cuantia'] = self.cuantia_ayuda_entry.get()  # Mantener la cuantía original si hay error
        else:
            context['cuantia'] = self.cuantia_ayuda_entry.get()  # Mantener la cuantía original

        # Definir la fecha actual
        fecha_actual = datetime.now().strftime("%Y.%m.%d")  # Formato: YYYY.MM.DD

        # Crear el nombre del archivo usando las dos primeras letras del nombre y apellido del menor
        nombre = context['menor_nombre'][:2].upper()  # Dos primeras letras del nombre del menor
        apellido = context['menor_apellidos'][:2].upper()  # Dos primeras letras del apellido del menor
        output_filename = f"{nombre}.{apellido}_{numero_siria}_{fecha_actual}.docx"

        try:
            # Obtener la ruta del directorio actual donde está el script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(script_dir, "plantilla_recibo.docx")
            
            # Verificar si existe la plantilla
            if not os.path.exists(template_path):
                messagebox.showerror("Error", "No se encuentra el archivo de plantilla 'plantilla_recibo.docx'")
                return
            
            # Cargar la plantilla
            template = DocxTemplate(template_path)
            
            # Renderizar el documento
            template.render(context)
            
            # Guardar el documento generado
            template.save(output_filename)
            
            messagebox.showinfo("Éxito", f"Documento generado correctamente: {output_filename}")
            
            # Abrir el documento generado
            os.startfile(output_filename)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el documento: {str(e)}")

    def calculate_copago(self, event=None):
        """Calculate the copago if applicable."""
        codigo_ayuda = self.codigo_ayuda_combobox.get()
        
        # Verifica si la ayuda requiere copago
        if codigo_ayuda in ["ATSANGA", "ATSANTDE"]:  # Añadido ATSANTDE aquí
            try:
                cuantia = float(self.cuantia_ayuda_entry.get().replace(',', '.'))
                copago = cuantia * 0.15  # Porcentaje del copago
                self.copago_label.config(text=f"Copago (15%): {copago:.2f}€. Introduce total factura.")
            except ValueError:
                self.copago_label.config(text="")
        else:
            # Mostrar la descripción de la ayuda si no hay copago
            descripcion = self.codigos_ayuda_descripcion.get(codigo_ayuda, "")
            self.copago_label.config(text=descripcion if descripcion else "")

    def update_cuantia(self, event=None):
        """Update the cuantía entry based on the selected ayuda."""
        print("Método update_cuantia llamado.")  # Mensaje de depuración
        codigo_ayuda = self.codigo_ayuda_combobox.get()
        print(f"Seleccionado: {codigo_ayuda}")  # Para depuración
        if codigo_ayuda in self.cuantias_predefinidas:
            self.cuantia_ayuda_entry.delete(0, tk.END)  # Limpiar el campo
            self.cuantia_ayuda_entry.insert(0, self.cuantias_predefinidas[codigo_ayuda])  # Insertar la cuantía predefinida
            print(f"Cuantía autocompletada: {self.cuantias_predefinidas[codigo_ayuda]}")  # Mensaje de depuración
        else:
            self.cuantia_ayuda_entry.delete(0, tk.END)  # Limpiar el campo si no hay cuantía predefinida
            print("No se encontr cuantía predefinida para el código de ayuda seleccionado.")  # Mensaje de depuración

    def set_max_cuantia(self):
        """Set the maximum cuantía based on the selected ayuda code."""
        codigo_ayuda = self.codigo_ayuda_combobox.get()
        if codigo_ayuda in self.maximos_ayuda:
            max_cuantia = self.maximos_ayuda[codigo_ayuda]
            self.cuantia_ayuda_entry.delete(0, tk.END)  # Limpiar el campo
            self.cuantia_ayuda_entry.insert(0, max_cuantia)  # Insertar la cuantía máxima
            print(f"Cuantía máxima autocompletada: {max_cuantia}")  # Mensaje de depuración
            
            # Llamar a calculate_copago después de establecer la cuantía máxima
            self.calculate_copago()

if __name__ == "__main__":
    app = DocumentGenerator()
    app.root.mainloop()