'''
Created on 09/16/2018

@author: alconor
'''
import pyodbc
import sys
import xmlrpclib
from datetime import datetime

#import mi_departamento.mi_departamento
#import mi_jobid
from string import upper, rjust
#from pip._vendor.requests.exceptions import InvalidSchema

def mi_jobid(url, db, uid, password, puesto, desc_puesto, depa):
    import xmlrpclib
     # Calliing methods
    models_job = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    models_job.execute_kw(db, uid, password,
                     'hr.job', 'check_access_rights',
                     ['read'], {'raise_exception': False})
    
    filtro = [[['requirements', '=', puesto], ['company_id', '=', 1],['name','=',desc_puesto]]]  #lista de python
    registros = models_job.execute_kw(db, uid, password, 'hr.job', 'search_count', filtro)
    ids =       models_job.execute_kw(db, uid, password, 'hr.job', 'search',       filtro, {'limit': 1})
    if registros == 0:
         #print("Registro : ",  filtro , "No existe!!!")
         #print("IDS: ", ids)
         ident = models_job.execute_kw(db, uid, password, 'hr.job', 'create', [{ 'name': desc_puesto,
                                                                                 'company_id': 1,
                                                                                 'requirements': puesto,
                                                                                 'department_id': depa}])
         return ident
        #print("id_Odoo: ", ident)
    else: return ids[0]
###########################################################################################################################################
def mi_departamento(url, db, uid, password, depa):
    import xmlrpclib
     # Calliing methods
        
    models_dep = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    models_dep.execute_kw(db, uid, password,
                     'hr.department', 'check_access_rights',
                     ['read'], {'raise_exception': False})
    
    filtro = [[['note', '=', depa], ['company_id', '=', 1],['active','=',1]]]  #lista de python
    registros = models_dep.execute_kw(db, uid, password, 'hr.department', 'search_count', filtro)
    ids =       models_dep.execute_kw(db, uid, password, 'hr.department', 'search',       filtro, {'limit': 1})
    if registros == 0:
         #print("Registro : ",  filtro , "No existe!!!")
         #print("IDS: ", ids)
         ident = models_dep.execute_kw(db, uid, password, 'hr.department', 'create', [{ 'name': depa,
                                                                                        'active': 1,
                                                                                        'company_id': 1,
                                                                                        'note': depa}])
         return ident
        #print("id_Odoo: ", ident)
    else: return ids[0]
#    except Exception:
#    e = sys.exc_info()[1] 
#    print(e.args[0])
#    print(e.args[1])

###########################################################################################################################################
def mis_empleados(url, db, uid, password, empleado, name_related):
    import xmlrpclib
     # Calliing methods
        
    models_emp2 = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    models_emp2.execute_kw(db, uid, password,
                     'resource.resource', 'check_access_rights',
                     ['read'], {'raise_exception': False})
    
    filtro = [[ ['company_id', '=', 1], ['resource_type', '=', "user"], ['code', '=', empleado] ]]  #lista de python
    registros_emp = models_emp2.execute_kw(db, uid, password, 'resource.resource', 'search_count', filtro)
    ids =       models_emp2.execute_kw(db, uid, password, 'resource.resource', 'search',       filtro, {'limit': 1})
    if registros_emp == 0:
         #print("Registro : ",  filtro , "No existe!!!")
         #print("IDS: ", ids)
         ident_r = models_emp2.execute_kw(db, uid, password, 'resource.resource', 'create', [{ 'name': name_related,
                                                                                        'active': 1,
                                                                                        'company_id': 1,
                                                                                        'resource_type': "user",
                                                                                        'time_efficiency': 100,
                                                                                        'code': empleado}])
         return ident_r
    else:
         return ids[0]
    
###########################################################################################################################################

# ODOO 10
#url = "http://server2.alconsoft.net:8071"
url = "http://192.168.0.16:8069"
db = "p10_ININCO"
username = 'soporte@ininco.com'
password = "Cotita2312"

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
print("common version: ")
print(common.version())

#User Identifier
uid = common.authenticate(db, username, password, {})
print("uid: ")
print(uid)

# Calliing methods
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
models.execute_kw(db, uid, password,
              'res.partner', 'check_access_rights',
              ['read'], {'raise_exception': False})

# SQL SERVER
cadena_conex1 = "DRIVER={SQL Server};server=localhost;database=ININCO;uid=sa;pwd=Sql2012"
conexion1 = pyodbc.connect(cadena_conex1)
cursor1 = conexion1.cursor()

consulta1 = "SELECT [EMPLEADO],[NOMBRE],[SEXO],[TIPO_SANGRE],[ESTADO_EMPLEADO],A.[ACTIVO],[IDENTIFICACION],[FECHA_INGRESO],[FECHA_SALIDA],[DEPARTAMENTO],B.[PUESTO],B.[DESCRIPCION],[NOMINA],[FECHA_NACIMIENTO],[UBICACION],[ESTADO_CIVIL],[ASEGURADO],[CLASE_SEGURO],[PERMISO_CONDUCIR],[PERMISO_SALUD],[NIT],[SALARIO_REFERENCIA],[FORMA_PAGO],[TELEFONO1],[NOTAS_TEL1],[TELEFONO2],[NOTAS_TEL2],[TELEFONO3],[NOTAS_TEL3],[PRIMER_APELLIDO],[SEGUNDO_APELLIDO],[NOMBRE_PILA],[E_MAIL] "
consulta2 = "FROM [ININCO].[ININCO].[EMPLEADO] AS A INNER JOIN [ININCO].[ININCO].[PUESTO] AS B ON A.PUESTO = B.PUESTO "
#consulta3 = "WHERE YEAR(A.[FECHA_INGRESO]) = 2006 "
consulta3 = " "
consulta4 = "ORDER BY A.FECHA_INGRESO DESC"
consulta = consulta1 + consulta2 + consulta3 +consulta4
cursor1.execute(consulta)
# INICIO CICLO DE EMPLEADOS PARA SER ACTUALIZADOS
for row in cursor1:
    empleado = row.EMPLEADO.lstrip()
    nombre_completo = row.NOMBRE
    cedula = row.IDENTIFICACION
    cargo = row.PUESTO + '-' + row.DESCRIPCION
    if row.ACTIVO == 'S': activo = True
    else: activo = False
    ################   
    print  '\t', row.EMPLEADO, '\t', row.NOMBRE.ljust(40), '\t', row.IDENTIFICACION , '\t', row.FECHA_INGRESO, '\b'
    # INSERTAR REGISTROS EN TABLA res_partners
    filtro = [[['ref', '=', empleado], ['employee', '=', True],['active','=',activo]]]  #lista de python
    registros = models.execute_kw(db, uid, password, 'res.partner', 'search_count', filtro)
    ids =       models.execute_kw(db, uid, password, 'res.partner', 'search',       filtro, {'limit': 1})
    if registros == 0:
        #print("Registro : ",  filtro , "No existe!!!")
        #print("IDS: ", ids)
        ident = models.execute_kw(db, uid, password, 'res.partner', 'create', [{ 'name': nombre_completo,
                                                                                'employee': True,
                                                                                'ref': empleado,
                                                                                'function': cargo,
                                                                                'active': activo}])
        #print("id_Odoo: ", ident)
    
                
    #---------------------------------------------------------------------------------------------------------------------------------#
    # INSERTAR REGISTRO EN TABLA hr_employee
    #---------------------------------------------------------------------------------------------------------------------------------#
    # COLOR
    if empleado == 'CH2102':
        StopIteration        
    color = 0
    # ESTADO CIVIL
    if row.ESTADO_CIVIL == 'S':
        marital = "single"
    elif row.ESTADO_CIVIL == 'C':
        marital = "married"
    elif row.ESTADO_CIVIL == 'U':
        marital = "married"
    elif row.ESTADO_CIVIL == 'D':
        marital = "divorced"
    elif row.ESTADO_CIVIL == "V":
        marital = "widower"
    else:
        marital = ""
    # NOMBRE
    name_related = row.NOMBRE            
    # IDENTIFICACION
    identification_id = row.IDENTIFICACION
    # JOB ID COMO NOTES = CARGO
    cargo = cargo
    # RESOURCE_ID
    identif_l = mis_empleados(url, db, uid, password, empleado, name_related)
    # Department
    departa = mi_departamento(url, db, uid, password,row.DEPARTAMENTO)
    departamento = departa
    # TELEFONO1
    mobile_phone = row.TELEFONO1
    # EMPLLEADO
    ssnid = empleado
    notes = ''
    notes = notes + "-CODIGO: " + empleado + '\t' 
    #SEXO
    if row.SEXO == 'M':
        gender = "male"
    elif row.SEXO == 'F':
        gender = "female"
    else:  gender = "other"
    # TIPO_SANGRE
    #print(type(row.TIPO_SANGRE))
    if type(row.TIPO_SANGRE) == 'unicode':
        notes = notes + "-SANGRE: " + row.TIPO_SANGRE + '\t'
    else:
        notes = notes + "-SANGRE: " + 'NO DISPONIBLE' + '\t'
    # PUESTO
    jobid_l = mi_jobid(url, db, uid, password,row.PUESTO,row.DESCRIPCION, departa)
    jobid = jobid_l
    # ESTADO_EMPELADO
    notes = notes + "-ESTADO: " + row.ESTADO_EMPLEADO + '\t'
    # FECHA_INGRESO
    if type(row.FECHA_INGRESO) == 'datetime.datetime':
        fecha_str = datetime.strftime(row.FECHA_INGRESO, '%d/%m/%Y')
    else: fecha_str = '1901-01-01'
    notes = notes + "-INGRESO: " + fecha_str + '\t'
    # FECHA_SALIDA
    if type(row.FECHA_SALIDA) == 'datetime.datetime':
        fecha_str = datetime.strftime(row.FECHA_SALIDA, '%d/%m/%Y')
    else: fecha_str = '1901-01-01'
    notes = notes + "-SALIDA: " + fecha_str + '\t'
    # NOMINA
    notes = notes + "-NOMINA: " + row.NOMINA + '\t'
    # FECHA_NACIMIENTO
    if type(row.FECHA_NACIMIENTO) == 'datetime.datetime':
        birthday = datetime.strftime(row.FECHA_NACIMIENTO, '%d/%m/%Y')
    else:
        birthday = '1901-01-01' 
    # E_MAIL
    work_email = "-" #row.E_MAIL
    
    models_emp = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    models_emp.execute_kw(db, uid, password,
                  'hr.employee', 'check_access_rights',
                  ['read'], {'raise_exception': False})        
    filtro = [[['ssnid', '=', empleado], ['company_id', '=', 1]]]  #lista de python
    registros = models_emp.execute_kw(db, uid, password, 'hr.employee', 'search_count', filtro)
    ids =       models_emp.execute_kw(db, uid, password, 'hr.employee', 'search',       filtro, {'limit': 1})
    
    if registros == 0:
        #print("Registro : ",  filtro , "No existe!!!")
        #print("IDS: ", ids)
        ident = models_emp.execute_kw(db, uid, password, 'hr.employee', 'create', [{'resource_id':      identif_l, 
                                                                                    'color':            color,
                                                                                    'marital':          marital,
                                                                                    'ssnid':            ssnid,
                                                                                    'department_id':    departamento,
                                                                                    'identification_id':identification_id,
                                                                                    'mobile_phone':     mobile_phone,
                                                                                    'name_related':     name_related,
                                                                                    'gender':           gender,
                                                                                    'work_email':       work_email,
                                                                                    'birthday':         birthday,
                                                                                    'notes':            notes,
                                                                                    'job_id':           jobid } ] )
cursor1.close()
conexion1.close()


