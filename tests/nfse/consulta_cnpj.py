from pynfe.entidades.cliente import Cliente
from pynfe.entidades.emitente import Emitente
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoNfse
from pynfe.processamento.serializacao import SerializacaoNfse

'''
****************
Descrição: Este método é responsável por atender aos pedidos de consulta de CNPJ. Este
método possibilita aos tomadores e/ou prestadores de serviços consultarem quais Inscrições
Municipais (CCM) estão vinculadas a um determinado CNPJ e se estes CCM emitem NF-e ou
não.
****************
'''

# remetente
remetente = Emitente(
    cnpj='35132740000166',
)

# contribuinte que se deseja consultar
contribuinte = Cliente(
    tipo_documento='CNPJ',  # somente CNPJ
    numero_documento='23956944000132',  # apenas os numero do CNPJ
)

certificado = r"C:\Users\BDR3\Downloads\BDR_INVESTIMENTOS_LTDA_35132740000166_1589478520733321500.pfx"
senha = '1234'
homologacao = False
autorizador = 'saopaulo'

serializador = SerializacaoNfse(autorizador)
nfse = serializador.consultar_cnpj(remetente, contribuinte)

a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(nfse, retorna_string=True)

con = ComunicacaoNfse(certificado, senha, autorizador, homologacao)
resposta = con.consultar_cnpj(xml)

print(resposta)  # funcionando
