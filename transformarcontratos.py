import xml.etree.ElementTree as ET
import csv

# Tu XML (con una etiqueta raíz temporal añadida para parseo)
xml_data = f"""
<limsp-objects>
{'''<contract id='2197' ref='2742225832'>
    <!-- Resto del primer contrato -->
</contract>
<contract id='2146' ref='AIW-CD-10650'>
    <!-- Resto del segundo contrato -->
</contract>'''}
</limsp-objects>
"""

# Reemplaza con tu XML real manteniendo la estructura
xml_data = xml_data.replace('''<contract id='2197' ref='2742225832'>
    <!-- Resto del primer contrato -->
</contract>
<contract id='2146' ref='AIW-CD-10650'>
    <!-- Resto del segundo contrato -->
</contract>''', """[<limsp-objects>
  <list-enterprises>
    <enterprise id='4' login='FICOHSA_GT'>
      <name>FICOHSA_GT</name>
      <nif>FICOHSA_GT</nif>
      <list-contracts>
        <contract id='2159' ref='AnalyticsdeNBA'>
          <refProduct>limspae-nba-analytics</refProduct>
          <description>Analytics de NBA</description>
          <tsIni>1657831535000</tsIni>
          <tsEnd>4080396740000</tsEnd>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2178' ref='COMPRASTC'>
          <refProduct>limspae-msg</refProduct>
          <description>COMPRAS TC</description>
          <tsIni>1657832458000</tsIni>
          <tsEnd>4085847636000</tsEnd>
          <list-clauses>
            <clause id='2331'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Claro-GT</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Claro-GT</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
            <clause id='2332'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Tigo-GT</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Tigo-GT</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
            <clause id='2333'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Unknown</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Unknown</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
          </list-clauses>
          <list-properties>
            <property space='LIMSP' name='CONTENT_TEMPLATE_ENABLE'>APPLICATION</property>
            <property space='LIMSP' name='CUSTOMER_PREFERENCES'>TRUE</property>
          </list-properties>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2160' ref='Catalogodecondiciones'>
          <refProduct>catalog-conditions</refProduct>
          <description>Catalogo de condiciones</description>
          <tsIni>1657831597000</tsIni>
          <tsEnd>4087560937000</tsEnd>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2165' ref='GestionNBA'>
          <refProduct>limspae-mng-campaign</refProduct>
          <description>Gestion de NBA</description>
          <tsIni>1657831862000</tsIni>
          <tsEnd>4080396165000</tsEnd>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2179' ref='RETIROSTC'>
          <refProduct>limspae-msg</refProduct>
          <description>RETIROS TC</description>
          <tsIni>1657832499000</tsIni>
          <tsEnd>4085847636000</tsEnd>
          <list-clauses>
            <clause id='2334'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Claro-GT</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Claro-GT</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
            <clause id='2335'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Tigo-GT</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Tigo-GT</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
            <clause id='2336'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Unknown</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Unknown</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
          </list-clauses>
          <list-properties>
            <property space='LIMSP' name='CONTENT_TEMPLATE_ENABLE'>APPLICATION</property>
            <property space='LIMSP' name='CUSTOMER_PREFERENCES'>TRUE</property>
          </list-properties>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2164' ref='ServiceWS'>
          <refProduct>ServiceAdaptorWS</refProduct>
          <description>Envío SMS</description>
          <tsIni>1657831824000</tsIni>
          <tsEnd>4079449412000</tsEnd>
          <list-clauses>
            <clause id='2310'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Claro-GT</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Claro-GT</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
            <clause id='2311'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Tigo-GT</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Tigo-GT</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
            <clause id='2312'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Unknown</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Unknown</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
          </list-clauses>
          <list-properties>
            <property space='LIMSP' name='ADAPTOR'>WS</property>
            <property space='LIMSP' name='CONTENT_TEMPLATE'>NONE</property>
            <property space='LIMSP' name='CONTENT_TEMPLATE_ENABLE'>NONE</property>
            <property space='LIMSP' name='CUSTOMER_PREFERENCES'>TRUE</property>
          </list-properties>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2190' ref='YNZ-BG-49123'>
          <refProduct>limspae-msg</refProduct>
          <description>Prueba NBA</description>
          <tsIni>1657832877000</tsIni>
          <tsEnd>4080398466000</tsEnd>
          <list-clauses>
            <clause id='2364'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Claro-GT</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Claro-GT</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
            <clause id='2365'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Tigo-GT</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Tigo-GT</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
            <clause id='2366'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Unknown</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Unknown</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
          </list-clauses>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2161' ref='catalogodeoperacionesbancarias'>
          <refProduct>limsp-catalogoper</refProduct>
          <description>catalogo de operaciones bancarias</description>
          <tsIni>1657831680000</tsIni>
          <tsEnd>4087560937000</tsEnd>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2162' ref='customermanagementcenter'>
          <refProduct>wsubscribers</refProduct>
          <description>customer management center</description>
          <tsIni>1657831740000</tsIni>
          <tsEnd>4087560937000</tsEnd>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2166' ref='gestiondeplantillas'>
          <refProduct>wgesttemplate</refProduct>
          <description>gestion de plantillas</description>
          <tsIni>1657831901000</tsIni>
          <tsEnd>4087560937000</tsEnd>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2181' ref='limspae-eventmonitor-gt'>
          <refProduct>limspae-eventmonitor</refProduct>
          <description>Monitorización de eventos GT</description>
          <tsIni>1657832587000</tsIni>
          <tsEnd>4079784263000</tsEnd>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2195' ref='limspae-transfrules'>
          <refProduct>limspae-transfrules</refProduct>
          <description>reglas de transformacion de alertas</description>
          <tsIni>1658180420000</tsIni>
          <tsEnd>4070930400000</tsEnd>
        </contract>
        <contract id='2196' ref='limspinf-cpm'>
          <refProduct>limspinf-cpm</refProduct>
          <description>Gestión de propiedades de clientes</description>
          <tsIni>1658180541000</tsIni>
          <tsEnd>4070930400000</tsEnd>
        </contract>
        <contract id='2180' ref='nba-model'>
          <refProduct>limspae-msg</refProduct>
          <description>Modelo para NBA</description>
          <tsIni>1657832544000</tsIni>
          <tsEnd>4080398466000</tsEnd>
          <list-clauses>
            <clause id='2337'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Claro-GT</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Claro-GT</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
            <clause id='2338'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Tigo-GT</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Tigo-GT</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
            <clause id='2339'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Unknown</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Unknown</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
          </list-clauses>
          <list-properties>
            <property space='LIMSP' name='CONTENT_TEMPLATE'>NONE</property>
            <property space='LIMSP' name='CONTENT_TEMPLATE_ENABLE'>APPLICATION</property>
            <property space='LIMSP' name='CUSTOMER_PREFERENCES'>TRUE</property>
            <property space='LIMSP' name='INOT_MAX_CHN'>2</property>
          </list-properties>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2191' ref='reglasdesuscripciondealertas'>
          <refProduct>limspae-subscrules</refProduct>
          <description>Reglas de suscripcion de alertas</description>
          <tsIni>1657832993000</tsIni>
          <tsEnd>4087560937000</tsEnd>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2192' ref='reglasdetransformaciondealertas'>
          <refProduct>limspae-transfrules</refProduct>
          <description>reglas de transformacion de alertas</description>
          <tsIni>1657833033000</tsIni>
          <tsEnd>4087560937000</tsEnd>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
        <contract id='2193' ref='servicioalertas'>
          <refProduct>limspae-msg</refProduct>
          <description>servicio alertas</description>
          <tsIni>1657833070000</tsIni>
          <tsEnd>4087560937000</tsEnd>
          <list-clauses>
            <clause id='2367'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Claro-GT</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Claro-GT</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
            <clause id='2368'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Tigo-GT</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Tigo-GT</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
            <clause id='2369'>
              <refFormat>sms</refFormat>
              <type>out</type>
              <alias>-----</alias>
              <operatorIn>Unknown</operatorIn>
              <channelOutRef>+502111</channelOutRef>
              <operatorOut>Unknown</operatorOut>
              <channelInRef>MANUAL</channelInRef>
              <refCredit/>
              <order>1</order>
            </clause>
          </list-clauses>
          <list-properties>
            <property space='LIMSP' name='ADAPTOR'>WS</property>
            <property space='LIMSP' name='CONTENT_TEMPLATE'>NONE</property>
            <property space='LIMSP' name='CONTENT_TEMPLATE_ENABLE'>APPLICATION</property>
            <property space='LIMSP' name='CUSTOMER_PREFERENCES'>TRUE</property>
            <property space='LIMSP' name='INOT_CHN_PREF'>CONTRACT</property>
            <property space='LIMSP' name='INOT_MAX_CHN'>1</property>
          </list-properties>
          <list-users>
            <user ref='CCHANG'/>
          </list-users>
        </contract>
      </list-contracts>
    </enterprise>
  </list-enterprises>
</limsp-objects>]""")

try:
    # Parsear el XML
    root = ET.fromstring(xml_data)
    
    # Propiedades que queremos extraer (en orden deseado para el CSV)
    properties_to_extract = [
        'CONTENT_TEMPLATE',
        'CONTENT_TEMPLATE_ENABLE',
        'CUSTOMER_PREFERENCES',
        'ADAPTOR',
        'INOT_CHN_PREF',
        'INOT_MAX_CHN'
    ]
    
    with open('contracts_simplified.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Encabezados del CSV
        headers = [
            'contract_id',
            'contract_ref',
            'refProduct',
            'refFormats',
            'description',
            'tsIni',
            'tsEnd'
        ] + properties_to_extract + ['users']
        
        writer.writerow(headers)
        
        # Procesar cada contrato
        for contract in root.findall('.//contract'):
                        # Extraer refFormats de las cláusulas (valores únicos)
            ref_formats = set()
            for clause in contract.findall('.//list-clauses/clause/refFormat'):
                if clause.text:
                    ref_formats.add(clause.text)
            ref_formats_str = ','.join(sorted(ref_formats)) if ref_formats else ''

            # Datos básicos del contrato
            contract_data = [
                contract.get('id'),
                contract.get('ref'),
                contract.find('refProduct').text if contract.find('refProduct') is not None else '',
                ref_formats_str,  # Usamos los formatos concatenados
                contract.find('description').text if contract.find('description') is not None else '',
                contract.find('tsIni').text if contract.find('tsIni') is not None else '',
                contract.find('tsEnd').text if contract.find('tsEnd') is not None else ''
            ]
            
            # Extraer propiedades
            props = {p.get('name'): p.text for p in contract.findall('.//list-properties/property')}
            properties_data = [props.get(prop, '') for prop in properties_to_extract]
            
            # Usuarios (concatenados)
            users = ','.join([u.get('ref') for u in contract.findall('.//list-users/user')])
            
            # Combinar todos los datos
            row = contract_data + properties_data + [users]
            writer.writerow(row)
    
    print("Archivo CSV generado exitosamente: contracts_simplified.csv")

except ET.ParseError as e:
    print(f"Error al parsear XML: {e}")
    print("Asegúrate de que el XML tenga una etiqueta raíz válida")
except Exception as e:
    print(f"Error inesperado: {e}")