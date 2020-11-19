from pynfe.entidades.emitente import Emitente
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoNfse
from pynfe.processamento.serializacao import SerializacaoNfse

'''
****************
Descrição: Este método é responsável por atender aos pedidos de consulta de NF-e / RPS. Seu
acesso é permitido apenas pela chave de identificação da NF-e ou pela chave de identificação
do RPS.
****************
'''

# prestador
emitente = Emitente(
    cnpj='35132740000166',
    inscricao_municipal='64187934'
)

certificado = r"C:\Users\BDR3\Downloads\BDR_INVESTIMENTOS_LTDA_35132740000166_1589478520733321500.pfx"
senha = '1234'
homologacao = False
autorizador = 'saopaulo'

serializador = SerializacaoNfse(autorizador)
nfse = serializador.consultar_nfse(emitente, 11)

a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(nfse, retorna_string=True)

con = ComunicacaoNfse(certificado, senha, autorizador, homologacao)
resposta = con.consultar(xml)

print(resposta)  # funcionando 100%
