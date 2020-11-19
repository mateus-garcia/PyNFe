from pynfe.entidades.emitente import Emitente
from pynfe.entidades.notafiscal import NotaFiscalServico
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoNfse
from pynfe.processamento.serializacao import SerializacaoNfse

'''
Descrição: Este método é responsável por atender aos pedidos referentes ao cancelamento de
NF-e geradas a partir do método EnvioLoteRPS.
'''

# prestador
emitente = Emitente(
    cnpj='99999997000100',
    inscricao_municipal='39616924'
)

# nota
nota = NotaFiscalServico(
    identificador='17945',  # número da nfs-e
    emitente=emitente
)

certificado = r"C:\Users\BDR3\Downloads\BDR_INVESTIMENTOS_LTDA_35132740000166_1589478520733321500.pfx"
senha = '1234'
homologacao = False

# serialização
serializador = SerializacaoNfse('saopaulo')
xml = serializador.cancelar(nota)

# assinatura

a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar_rps(xml)
xml = a1.assinar(xml, retorna_string=True)

# envio
# não testado
con = ComunicacaoNfse(certificado, senha, 'saopaulo', homologacao)
# envio = con.cancelar(xml)

print()
