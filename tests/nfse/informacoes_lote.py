from pynfe.entidades.emitente import Emitente
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoNfse
from pynfe.processamento.serializacao import SerializacaoNfse

'''
**************
Descrição: Este método é responsável por atender aos pedidos de Consulta de Informações de
Lote de NF-e geradas a partir do método EnvioLoteRPS.
**************
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
numero_lote = 99999  # Opcional. Caso não seja informado o número do lote, serão retornadas informações do último lote gerador de NF-e.

serializador = SerializacaoNfse(autorizador)
nfse = serializador.consultar_situacao_lote(emitente)

a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(nfse, retorna_string=True)

con = ComunicacaoNfse(certificado, senha, autorizador, homologacao)
resposta = con.consultar_situacao_lote(xml)

print(resposta)
