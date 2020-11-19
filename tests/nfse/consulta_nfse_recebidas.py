from datetime import date

from pynfe.entidades.cliente import Cliente
from pynfe.entidades.emitente import Emitente
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoNfse
from pynfe.processamento.serializacao import SerializacaoNfse

'''
*************
Descrição: Este método é responsável por atender aos pedidos de consulta de NF-e Recebidas.
Descrição: Este método é responsável por atender aos pedidos de consulta de NF-e Emitidas.
*************
'''

# prestador
emitente = Emitente(
    cnpj='35132740000166',
    inscricao_municipal='64187934'
)
# tomador
cliente = Cliente(
    tipo_documento='CNPJ',
    numero_documento='35132740000166',
    inscricao_municipal='64187934'
)

certificado = r"C:\Users\BDR3\Downloads\BDR_INVESTIMENTOS_LTDA_35132740000166_1589478520733321500.pfx"
senha = '1234'
homologacao = False
autorizador = 'saopaulo'

serializador = SerializacaoNfse(autorizador)

# utilizar cliente ou emitente geram o mesmo resultado
nfse = serializador.consultar_nfse_emit_recb('35132740000166', cliente=cliente, inicio=date(2020, 10, 1),
                                             fim=date(2020, 11, 1))

a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(nfse, retorna_string=True)

con = ComunicacaoNfse(certificado, senha, autorizador, homologacao)
# para consultar emitidas ou recebidas, utilizar um dos tipos abaixo
emitidas = con.consultar_emitidas(xml)
print(emitidas)
print()
recebidas = con.consultar_recebidas(xml)
print(recebidas)
