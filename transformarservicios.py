import xml.etree.ElementTree as ET
import csv

def extract_services_data(xml_content):
    try:
        # Parsear el XML
        root = ET.fromstring(xml_content)
        
        # Crear archivo CSV
        with open('services_list.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Encabezados del CSV
            headers = [
                'ID',
                'ID Company',
                'ID Service Group',
                'Service Name',  # Nombre específico después de mustRegister
                'Priority',
                'Registered Users',
                'Reference Service',
                'Deleted',
                'Must Register',
                'Reference Frame',
                'Models Count',
                'Model Names',    # Nombres de los modelos
                'Rule References',
                'Channels',
                'Contract SMS',
                'Contract Email',
                'Template Reference'
            ]
            writer.writerow(headers)
            
            # Función para buscar elementos ignorando namespaces
            def find_element(parent, tag):
                return parent.find(f'.//{{*}}{tag}')
            
            def find_all(parent, tag):
                return parent.findall(f'.//{{*}}{tag}')
            
            # Procesar cada servicio
            for service in root.findall('.//{*}return'):
                # Extraer el name específico que está después de mustRegister
                service_name = ''
                must_register = None
                # Iterar manualmente para encontrar el name después de mustRegister
                for elem in service:
                    if elem.tag.endswith('mustRegister'):
                        must_register = elem
                    elif must_register is not None and elem.tag.endswith('name'):
                        service_name = elem.text if elem.text else ''
                        break
                
                # Extraer rule refs y model names de los modelos
                rule_refs = []
                model_names = []
                for model in find_all(service, 'models'):
                    # Nombre del modelo
                    model_name = find_element(model, 'name')
                    if model_name is not None and model_name.text:
                        model_names.append(model_name.text)
                    
                    # Rule ref
                    xml_model = find_element(model, 'xmlModel')
                    if xml_model is not None and xml_model.text:
                        try:
                            model_root = ET.fromstring(xml_model.text)
                            rule_ref = model_root.get('ref')
                            if rule_ref:
                                rule_refs.append(rule_ref)
                        except ET.ParseError:
                            pass
                
                # Datos básicos
                basic_data = [
                    find_element(service, 'id').text if find_element(service, 'id') is not None else '',
                    find_element(service, 'idCompany').text if find_element(service, 'idCompany') is not None else '',
                    find_element(service, 'idServiceGroup').text if find_element(service, 'idServiceGroup') is not None else '',
                    service_name,  # Usamos el name específico que encontramos
                    find_element(service, 'priority').text if find_element(service, 'priority') is not None else '',
                    find_element(service, 'registeredUsers').text if find_element(service, 'registeredUsers') is not None else '',
                    find_element(service, 'refService').text if find_element(service, 'refService') is not None else '',
                    find_element(service, 'deleted').text if find_element(service, 'deleted') is not None else '',
                    must_register.text if must_register is not None else '',  # mustRegister ya lo tenemos
                    find_element(service, 'refFrame').text if find_element(service, 'refFrame') is not None else '',
                    str(len(find_all(service, 'models'))),
                    ','.join(model_names) if model_names else '',  # Nombres de modelos
                    ','.join(rule_refs) if rule_refs else '',
                ]
                
                # Extraer propiedades
                channels = set()
                contract_sms = ''
                contract_email = ''
                template_ref = ''
                
                for prop in find_all(service, 'props'):
                    prop_name_elem = find_element(prop, 'name')
                    prop_name = prop_name_elem.text if prop_name_elem is not None else ''
                    
                    values = [v.text for v in find_all(prop, 'values') if v.text is not None]
                    
                    if prop_name == 'channels':
                        channels.update(values)
                    elif prop_name == 'contratosms':
                        contract_sms = ','.join(values)
                    elif prop_name == 'contratomail':
                        contract_email = ','.join(values)
                    elif prop_name in ['reftemplate', 'template', 'xsellingtemplate']:
                        template_ref = ','.join(values)
                
                # Combinar todos los datos
                row = basic_data + [
                    ','.join(channels) if channels else '',
                    contract_sms,
                    contract_email,
                    template_ref
                ]
                
                writer.writerow(row)
        
        print("Archivo CSV generado exitosamente: services_list.csv")
        return True
    
    except ET.ParseError as e:
        print(f"Error al parsear XML: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

# Ejemplo de uso
if __name__ == "__main__":
    # Aquí debes pegar tu XML completo
    xml_data = """<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
   <S:Body>
      <ns0:getCompanyServicesListResponse xmlns:ns0="http://com.latinia/lsubscribers/provisioner">
         <return>
            <deleted>false</deleted>
            <id>1239</id>
            <idCompany>1219</idCompany>
            <idServiceGroup>14</idServiceGroup>
            <models>
               <allUsers>true</allUsers>
               <id>1243</id>
               <idCompany>1219</idCompany>
               <idService>1239</idService>
               <name>Compras en POS</name>
               <order>1</order>
               <refModel>CompraPOS</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='CompraPOS'>
  <condition optional='false' dataType='TEXT'>
    <description>Alerta por compra exitosa</description>
    <lo>${EV.estado_transaccion}</lo>
    <op>EQUALS</op>
    <ro>00</ro>
  </condition>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto de transacción</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>1.00</ro>
  </condition>
  <condition optional='false' dataType='TEXT'>
    <description>Posee Paf</description>
    <lo>${EV.posee_paf}</lo>
    <op>EQUALS</op>
    <ro>S</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <mustRegister>true</mustRegister>
            <name>COMPRA POS</name>
            <priority>4</priority>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>template</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1245</idProp>
                  <idSource>-1</idSource>
                  <idString>1245</idString>
                  <name>template</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>Plan Alerta Ficohsa</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#priority</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1222</idProp>
                  <idSource>-1</idSource>
                  <idString>1222</idString>
                  <name>#priority</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>4</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>channels</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1247</idProp>
                  <idSource>-1</idSource>
                  <idString>1247</idString>
                  <name>channels</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>EMAIL</values>
               <values>SMS</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>contrato</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1248</idProp>
                  <idSource>-1</idSource>
                  <idString>1248</idString>
                  <name>contrato</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>paf</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#ref_frame</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1225</idProp>
                  <idSource>-1</idSource>
                  <idString>1225</idString>
                  <name>#ref_frame</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>flink</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#name</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1224</idProp>
                  <idSource>-1</idSource>
                  <idString>1224</idString>
                  <name>#name</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>COMPRA POS</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>xselling</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1250</idProp>
                  <idSource>-1</idSource>
                  <idString>1250</idString>
                  <name>xselling</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>false</values>
            </props>
            <refFrame>flink</refFrame>
            <refService>1050020000</refService>
            <registeredUsers>50294</registeredUsers>
         </return>
         <return>
            <deleted>false</deleted>
            <id>1241</id>
            <idCompany>1219</idCompany>
            <idServiceGroup>14</idServiceGroup>
            <models>
               <allUsers>true</allUsers>
               <id>1251</id>
               <idCompany>1219</idCompany>
               <idService>1241</idService>
               <name>Retiro de Efectivo con TC</name>
               <order>1</order>
               <refModel>RetiroEfectivo</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='RetiroEfectivo'>
  <condition optional='false' dataType='TEXT'>
    <description>Alerta por tx exitosa</description>
    <lo>${EV.estado_transaccion}</lo>
    <op>EQUALS</op>
    <ro>00</ro>
  </condition>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto mínimo</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>5</ro>
  </condition>
  <condition optional='false' dataType='TEXT'>
    <description>Moneda</description>
    <lo>${EV.codigo_moneda_original}</lo>
    <op>EQUALS</op>
    <ro>USD</ro>
  </condition>
  <condition optional='false' dataType='TEXT'>
    <description>Posee Paf</description>
    <lo>${EV.posee_paf}</lo>
    <op>EQUALS</op>
    <ro>S</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <mustRegister>true</mustRegister>
            <name>RETIRO TC</name>
            <priority>4</priority>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#priority</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1222</idProp>
                  <idSource>-1</idSource>
                  <idString>1222</idString>
                  <name>#priority</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>4</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>contrato</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1248</idProp>
                  <idSource>-1</idSource>
                  <idString>1248</idString>
                  <name>contrato</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>paf</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#ref_frame</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1225</idProp>
                  <idSource>-1</idSource>
                  <idString>1225</idString>
                  <name>#ref_frame</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>flink</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#name</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1224</idProp>
                  <idSource>-1</idSource>
                  <idString>1224</idString>
                  <name>#name</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>RETIRO TC</values>
            </props>
            <refFrame>flink</refFrame>
            <refService>1050020001</refService>
            <registeredUsers>50294</registeredUsers>
         </return>
         <return>
            <deleted>false</deleted>
            <id>443860</id>
            <idCompany>1219</idCompany>
            <idServiceGroup>14</idServiceGroup>
            <models>
               <allUsers>true</allUsers>
               <id>443861</id>
               <idCompany>1219</idCompany>
               <idService>443860</idService>
               <name>PAGO TC LOCAL</name>
               <order>1</order>
               <refModel>1050020020</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='1050020020 '>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>1</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <mustRegister>true</mustRegister>
            <name>PAGO TC LOCAL</name>
            <priority>4</priority>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#priority</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1222</idProp>
                  <idSource>-1</idSource>
                  <idString>1222</idString>
                  <name>#priority</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>4</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>channels</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1247</idProp>
                  <idSource>-1</idSource>
                  <idString>1247</idString>
                  <name>channels</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>EMAIL</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>contrato</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1248</idProp>
                  <idSource>-1</idSource>
                  <idString>1248</idString>
                  <name>contrato</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>1050020020</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#ref_frame</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1225</idProp>
                  <idSource>-1</idSource>
                  <idString>1225</idString>
                  <name>#ref_frame</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>flink</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#name</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1224</idProp>
                  <idSource>-1</idSource>
                  <idString>1224</idString>
                  <name>#name</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>PAGO TC LOCAL</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>xselling</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1250</idProp>
                  <idSource>-1</idSource>
                  <idString>1250</idString>
                  <name>xselling</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>false</values>
            </props>
            <refFrame>flink</refFrame>
            <refService>1050020020</refService>
            <registeredUsers>50294</registeredUsers>
         </return>
         <return>
            <deleted>false</deleted>
            <id>1339</id>
            <idCompany>1219</idCompany>
            <idServiceGroup>14</idServiceGroup>
            <models>
               <allUsers>true</allUsers>
               <id>1341</id>
               <idCompany>1219</idCompany>
               <idService>1339</idService>
               <name>COMPRA ONLINE</name>
               <order>1</order>
               <refModel>CompraOnline</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='CompraOnline'>
  <condition optional='false' dataType='TEXT'>
    <description>Alerta por compra exitosa</description>
    <lo>${EV.estado_transaccion}</lo>
    <op>EQUALS</op>
    <ro>00</ro>
  </condition>
  <condition optional='false' dataType='TEXT'>
    <description>Moneda USD</description>
    <lo>${EV.codigo_moneda_original}</lo>
    <op>EQUALS</op>
    <ro>USD</ro>
  </condition>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto de transacción</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>1.00</ro>
  </condition>
  <condition optional='false' dataType='TEXT'>
    <description>Posee Paf</description>
    <lo>${EV.posee_paf}</lo>
    <op>EQUALS</op>
    <ro>S</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <mustRegister>true</mustRegister>
            <name>COMPRA ONLINE</name>
            <priority>4</priority>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>template</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1245</idProp>
                  <idSource>-1</idSource>
                  <idString>1245</idString>
                  <name>template</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>Plan Alerta Ficohsa</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#priority</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1222</idProp>
                  <idSource>-1</idSource>
                  <idString>1222</idString>
                  <name>#priority</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>4</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>channels</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1247</idProp>
                  <idSource>-1</idSource>
                  <idString>1247</idString>
                  <name>channels</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>EMAIL</values>
               <values>SMS</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>contrato</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1248</idProp>
                  <idSource>-1</idSource>
                  <idString>1248</idString>
                  <name>contrato</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>paf</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#ref_frame</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1225</idProp>
                  <idSource>-1</idSource>
                  <idString>1225</idString>
                  <name>#ref_frame</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>flink</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#name</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1224</idProp>
                  <idSource>-1</idSource>
                  <idString>1224</idString>
                  <name>#name</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>COMPRA ONLINE</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>xselling</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1250</idProp>
                  <idSource>-1</idSource>
                  <idString>1250</idString>
                  <name>xselling</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>false</values>
            </props>
            <refFrame>flink</refFrame>
            <refService>1050020080</refService>
            <registeredUsers>50294</registeredUsers>
         </return>
         <return>
            <deleted>false</deleted>
            <id>1240</id>
            <idCompany>1219</idCompany>
            <idServiceGroup>14</idServiceGroup>
            <models>
               <allUsers>true</allUsers>
               <id>1252</id>
               <idCompany>1219</idCompany>
               <idService>1240</idService>
               <name>Compras en POS Black regional</name>
               <order>1</order>
               <refModel>CompraPOSREG</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='CompraPOSREG'>
  <condition optional='false' dataType='TEXT'>
    <description>Alerta de Compra exitosa</description>
    <lo>${EV.estado_transaccion}</lo>
    <op>EQUALS</op>
    <ro>00</ro>
  </condition>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto Original</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>1.00</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <mustRegister>true</mustRegister>
            <name>COMPRA POS BLACK REGONAL</name>
            <priority>4</priority>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>template</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1245</idProp>
                  <idSource>-1</idSource>
                  <idString>1245</idString>
                  <name>template</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>HTML_Black_Reg_Compra</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#priority</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1222</idProp>
                  <idSource>-1</idSource>
                  <idString>1222</idString>
                  <name>#priority</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>4</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>channels</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1247</idProp>
                  <idSource>-1</idSource>
                  <idString>1247</idString>
                  <name>channels</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>EMAIL</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>contrato</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1248</idProp>
                  <idSource>-1</idSource>
                  <idString>1248</idString>
                  <name>contrato</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>Envio_Email</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#ref_frame</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1225</idProp>
                  <idSource>-1</idSource>
                  <idString>1225</idString>
                  <name>#ref_frame</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>flink</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#name</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1224</idProp>
                  <idSource>-1</idSource>
                  <idString>1224</idString>
                  <name>#name</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>COMPRA POS BLACK REGONAL</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>xselling</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1250</idProp>
                  <idSource>-1</idSource>
                  <idString>1250</idString>
                  <name>xselling</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>false</values>
            </props>
            <refFrame>flink</refFrame>
            <refService>2050020000</refService>
            <registeredUsers>50294</registeredUsers>
         </return>
         <return>
            <deleted>false</deleted>
            <id>1242</id>
            <idCompany>1219</idCompany>
            <idServiceGroup>14</idServiceGroup>
            <models>
               <allUsers>true</allUsers>
               <id>1253</id>
               <idCompany>1219</idCompany>
               <idService>1242</idService>
               <name>Retiro de Efectivo con TC Black Regional</name>
               <order>1</order>
               <refModel>RetiroEfectivoBlackREG</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='RetiroEfectivoBlackREG'>
  <condition optional='false' dataType='TEXT'>
    <description>Alerta por Tx exitosa</description>
    <lo>${EV.estado_transaccion}</lo>
    <op>EQUALS</op>
    <ro>00</ro>
  </condition>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto mínimo</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>5</ro>
  </condition>
  <condition optional='false' dataType='TEXT'>
    <description>Moneda</description>
    <lo>${EV.codigo_moneda_original}</lo>
    <op>EQUALS</op>
    <ro>USD</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <mustRegister>true</mustRegister>
            <name>RETIRO TC BLACK REGIONAL</name>
            <priority>4</priority>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>template</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1245</idProp>
                  <idSource>-1</idSource>
                  <idString>1245</idString>
                  <name>template</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>HTML_Black_Reg_Retiro</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#priority</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1222</idProp>
                  <idSource>-1</idSource>
                  <idString>1222</idString>
                  <name>#priority</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>4</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>channels</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1247</idProp>
                  <idSource>-1</idSource>
                  <idString>1247</idString>
                  <name>channels</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>EMAIL</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>contrato</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1248</idProp>
                  <idSource>-1</idSource>
                  <idString>1248</idString>
                  <name>contrato</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>Envio_Email</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#ref_frame</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1225</idProp>
                  <idSource>-1</idSource>
                  <idString>1225</idString>
                  <name>#ref_frame</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>flink</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#name</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1224</idProp>
                  <idSource>-1</idSource>
                  <idString>1224</idString>
                  <name>#name</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>RETIRO TC BLACK REGIONAL</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>xselling</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1250</idProp>
                  <idSource>-1</idSource>
                  <idString>1250</idString>
                  <name>xselling</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>false</values>
            </props>
            <refFrame>flink</refFrame>
            <refService>2050020001</refService>
            <registeredUsers>50294</registeredUsers>
         </return>
         <return>
            <deleted>false</deleted>
            <id>443859</id>
            <idCompany>1219</idCompany>
            <idServiceGroup>14</idServiceGroup>
            <models>
               <allUsers>true</allUsers>
               <id>443862</id>
               <idCompany>1219</idCompany>
               <idService>443859</idService>
               <name>Pago TC Black</name>
               <order>1</order>
               <refModel>2050020020</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='2050020020 '>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>1</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <mustRegister>true</mustRegister>
            <name>PAGO TC BLACK</name>
            <priority>4</priority>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#priority</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1222</idProp>
                  <idSource>-1</idSource>
                  <idString>1222</idString>
                  <name>#priority</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>4</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>channels</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1247</idProp>
                  <idSource>-1</idSource>
                  <idString>1247</idString>
                  <name>channels</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>EMAIL</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>contrato</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1248</idProp>
                  <idSource>-1</idSource>
                  <idString>1248</idString>
                  <name>contrato</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>2050020020</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#ref_frame</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1225</idProp>
                  <idSource>-1</idSource>
                  <idString>1225</idString>
                  <name>#ref_frame</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>flink</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#name</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1224</idProp>
                  <idSource>-1</idSource>
                  <idString>1224</idString>
                  <name>#name</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>PAGO TC BLACK</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>xselling</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1250</idProp>
                  <idSource>-1</idSource>
                  <idString>1250</idString>
                  <name>xselling</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>false</values>
            </props>
            <refFrame>flink</refFrame>
            <refService>2050020020</refService>
            <registeredUsers>50294</registeredUsers>
         </return>
         <return>
            <deleted>false</deleted>
            <id>1340</id>
            <idCompany>1219</idCompany>
            <idServiceGroup>14</idServiceGroup>
            <models>
               <allUsers>true</allUsers>
               <id>1342</id>
               <idCompany>1219</idCompany>
               <idService>1340</idService>
               <name>COMPRA ONLINE BLACK REGIONAL</name>
               <order>1</order>
               <refModel>CompraONLREG</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='CompraONLREG'>
  <condition optional='false' dataType='TEXT'>
    <description>Alerta de Compra exitosa</description>
    <lo>${EV.estado_transaccion}</lo>
    <op>EQUALS</op>
    <ro>00</ro>
  </condition>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto Original</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>1.00</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <mustRegister>true</mustRegister>
            <name>COMPRA ONLINE BLACK REGIONAL</name>
            <priority>4</priority>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>template</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1245</idProp>
                  <idSource>-1</idSource>
                  <idString>1245</idString>
                  <name>template</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>HTML_Black_Reg_Compra</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#priority</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1222</idProp>
                  <idSource>-1</idSource>
                  <idString>1222</idString>
                  <name>#priority</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>4</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>channels</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1247</idProp>
                  <idSource>-1</idSource>
                  <idString>1247</idString>
                  <name>channels</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>EMAIL</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>contrato</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1248</idProp>
                  <idSource>-1</idSource>
                  <idString>1248</idString>
                  <name>contrato</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>Envio_Email</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#ref_frame</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1225</idProp>
                  <idSource>-1</idSource>
                  <idString>1225</idString>
                  <name>#ref_frame</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>flink</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#name</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1224</idProp>
                  <idSource>-1</idSource>
                  <idString>1224</idString>
                  <name>#name</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>COMPRA ONLINE BLACK REGIONAL</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>xselling</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1250</idProp>
                  <idSource>-1</idSource>
                  <idString>1250</idString>
                  <name>xselling</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>false</values>
            </props>
            <refFrame>flink</refFrame>
            <refService>2050020080</refService>
            <registeredUsers>50294</registeredUsers>
         </return>
         <return>
            <deleted>false</deleted>
            <id>442059</id>
            <idCompany>1219</idCompany>
            <idServiceGroup>16</idServiceGroup>
            <models>
               <allUsers>true</allUsers>
               <id>442060</id>
               <idCompany>1219</idCompany>
               <idService>442059</idService>
               <name>Credito Cuenta de Ahorro</name>
               <order>1</order>
               <refModel>CreditoCuentaAhorro</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='CreditoCuentaAhorro'>
  <condition optional='false' dataType='TEXT'>
    <description>Moneda Transaccion</description>
    <lo>${EV.codigo_moneda_original}</lo>
    <op>EQUALS</op>
    <ro>USD</ro>
  </condition>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>1</ro>
  </condition>
  <condition optional='false' dataType='TEXT'>
    <description>Codigo de Transaccion</description>
    <lo>${EV.anexo}</lo>
    <op>EQUALS</op>
    <ro>26</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <models>
               <allUsers>true</allUsers>
               <id>442061</id>
               <idCompany>1219</idCompany>
               <idService>442059</idService>
               <name>Credito Interno CTA de Ahorro</name>
               <order>2</order>
               <refModel>CreditoInternoCTAAhorro</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='CreditoInternoCTAAhorro'>
  <condition optional='false' dataType='TEXT'>
    <description>Moneda Transaccion</description>
    <lo>${EV.codigo_moneda_original}</lo>
    <op>EQUALS</op>
    <ro>USD</ro>
  </condition>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>1</ro>
  </condition>
  <condition optional='false' dataType='TEXT'>
    <description>Codigo de Transaccion</description>
    <lo>${EV.anexo}</lo>
    <op>EQUALS</op>
    <ro>70</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <models>
               <allUsers>true</allUsers>
               <id>442063</id>
               <idCompany>1219</idCompany>
               <idService>442059</idService>
               <name>Credito Transferencia Ahorro</name>
               <order>3</order>
               <refModel>CreditoTransferenciaAho</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='CreditoTransferenciaAho'>
  <condition optional='false' dataType='TEXT'>
    <description>Moneda Transaccion</description>
    <lo>${EV.codigo_moneda_original}</lo>
    <op>EQUALS</op>
    <ro>USD</ro>
  </condition>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>1</ro>
  </condition>
  <condition optional='false' dataType='TEXT'>
    <description>Codigo de Transaccion</description>
    <lo>${EV.anexo}</lo>
    <op>EQUALS</op>
    <ro>6012</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <models>
               <allUsers>true</allUsers>
               <id>442064</id>
               <idCompany>1219</idCompany>
               <idService>442059</idService>
               <name>Credito Transferencia GFF</name>
               <order>4</order>
               <refModel>CreditoTransGFF</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='CreditoTransGFF'>
  <condition optional='false' dataType='TEXT'>
    <description>Moneda Transaccion</description>
    <lo>${EV.codigo_moneda_original}</lo>
    <op>EQUALS</op>
    <ro>USD</ro>
  </condition>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>1</ro>
  </condition>
  <condition optional='false' dataType='TEXT'>
    <description>Codigo de Transaccion</description>
    <lo>${EV.anexo}</lo>
    <op>EQUALS</op>
    <ro>6222</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <models>
               <allUsers>true</allUsers>
               <id>442065</id>
               <idCompany>1219</idCompany>
               <idService>442059</idService>
               <name>Credito Transferencia de Cheque</name>
               <order>5</order>
               <refModel>CreditoTransferenciaCHQ</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='CreditoTransferenciaCHQ'>
  <condition optional='false' dataType='TEXT'>
    <description>Moneda Transaccion</description>
    <lo>${EV.codigo_moneda_original}</lo>
    <op>EQUALS</op>
    <ro>USD</ro>
  </condition>
  <condition optional='false' dataType='NUMBER'>
    <description>Monto</description>
    <lo>${EV.monto_original}</lo>
    <op>GREATEREQUAL</op>
    <ro>1</ro>
  </condition>
  <condition optional='false' dataType='TEXT'>
    <description>Codigo de Transaccion</description>
    <lo>${EV.anexo}</lo>
    <op>EQUALS</op>
    <ro>6011</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <mustRegister>true</mustRegister>
            <name>Creditos a Cuentas</name>
            <priority>4</priority>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>template</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1245</idProp>
                  <idSource>-1</idSource>
                  <idString>1245</idString>
                  <name>template</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>CreditoCuenta</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#priority</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1222</idProp>
                  <idSource>-1</idSource>
                  <idString>1222</idString>
                  <name>#priority</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>4</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>channels</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1247</idProp>
                  <idSource>-1</idSource>
                  <idString>1247</idString>
                  <name>channels</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>PNS</values>
               <values>SMS</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>contrato</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1248</idProp>
                  <idSource>-1</idSource>
                  <idString>1248</idString>
                  <name>contrato</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>paf</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#ref_frame</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1225</idProp>
                  <idSource>-1</idSource>
                  <idString>1225</idString>
                  <name>#ref_frame</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>flink</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#name</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1224</idProp>
                  <idSource>-1</idSource>
                  <idString>1224</idString>
                  <name>#name</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>Creditos a Cuentas</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>xselling</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1250</idProp>
                  <idSource>-1</idSource>
                  <idString>1250</idString>
                  <name>xselling</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>false</values>
            </props>
            <refFrame>flink</refFrame>
            <refService>60020002</refService>
            <registeredUsers>50294</registeredUsers>
         </return>
         <return>
            <deleted>false</deleted>
            <id>488888</id>
            <idCompany>1219</idCompany>
            <idServiceGroup>19</idServiceGroup>
            <models>
               <allUsers>true</allUsers>
               <id>488891</id>
               <idCompany>1219</idCompany>
               <idService>488888</idService>
               <name>Compras Debito</name>
               <order>1</order>
               <refModel>Compra_Debito</refModel>
               <type>2</type>
               <xmlModel><![CDATA[<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<rule ref='Compra_Debito'>
  <condition optional='false' dataType='TEXT'>
    <description>Compra debito BIN</description>
    <lo>${EV.bin}</lo>
    <op>EQUALS</op>
    <ro>457529</ro>
  </condition>
</rule>]]></xmlModel>
            </models>
            <mustRegister>false</mustRegister>
            <name>Compras Debito</name>
            <priority>4</priority>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>template</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1245</idProp>
                  <idSource>-1</idSource>
                  <idString>1245</idString>
                  <name>template</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>compra_debito</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#priority</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1222</idProp>
                  <idSource>-1</idSource>
                  <idString>1222</idString>
                  <name>#priority</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>4</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>channels</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1247</idProp>
                  <idSource>-1</idSource>
                  <idString>1247</idString>
                  <name>channels</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>EMAIL</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>contrato</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1248</idProp>
                  <idSource>-1</idSource>
                  <idString>1248</idString>
                  <name>contrato</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>compradebito</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#ref_frame</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1225</idProp>
                  <idSource>-1</idSource>
                  <idString>1225</idString>
                  <name>#ref_frame</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>flink</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>#name</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1224</idProp>
                  <idSource>-1</idSource>
                  <idString>1224</idString>
                  <name>#name</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>Compras Debito</values>
            </props>
            <props>
               <encryptedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <maskedValues xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
               <name>xselling</name>
               <type>
                  <idEncryptionType>-1</idEncryptionType>
                  <idProp>1250</idProp>
                  <idSource>-1</idSource>
                  <idString>1250</idString>
                  <name>xselling</name>
                  <objectType>2</objectType>
                  <preferred>false</preferred>
                  <shared>false</shared>
                  <size>-1</size>
                  <type>0</type>
               </type>
               <values>false</values>
            </props>
            <refFrame>flink</refFrame>
            <refService>comprasdebito</refService>
            <registeredUsers>50294</registeredUsers>
         </return>
      </ns0:getCompanyServicesListResponse>
   </S:Body>
</S:Envelope>"""
    
    extract_services_data(xml_data)