from datetime import date
from decimal import Decimal

from pynfe.entidades.cliente import Cliente
from pynfe.entidades.emitente import Emitente
from pynfe.entidades.rps import RPS
from pynfe.entidades.servico import Servico
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoNfse
from pynfe.processamento.serializacao import SerializacaoNfse
from pynfe.utils.flags import CODIGO_BRASIL

# prestador
emitente = Emitente(
    cnpj='99999998000228',
    inscricao_municipal='39617106'
)

# tomador
cliente1 = Cliente(
    razao_social='ANTONIO PRUDENTE',
    tipo_documento='CPF',  # CPF ou CNPJ
    numero_documento='99999999727',  # apenas os numero do CPF ou CNPJ
    inscricao_municipal='1234',  # opcional
    endereco_tipo_logradouro='RUA',
    endereco_logradouro='PEDRO AMERICO',
    endereco_numero='1',
    endereco_complemento='1 ANDAR',  # opcional
    endereco_bairro='CENTRO',
    endereco_cod_municipio='3550308',
    endereco_uf='SP',
    endereco_cep='00001045',
    endereco_pais=CODIGO_BRASIL,
    email='teste@teste.com'  # opcional
)

# serviço
servico1 = Servico(
    valor_servico=Decimal('100.00'),
    iss_retido=2,  # 1 - Sim; 2 - Não
    discriminacao='Nota Fiscal de Teste Emitida por Cliente Web',
    valor_deducoes=Decimal('0.00'),
    valor_pis=Decimal('1.01'),
    valor_confins=Decimal('1.02'),
    valor_inss=Decimal('1.03'),
    valor_ir=Decimal('1.04'),
    valor_csll=Decimal('1.05'),
    aliquota=Decimal('0.05'),
)

rps1 = RPS(
    emitente=emitente,
    cliente=cliente1,
    servico=servico1,
    chave_rps_serie='BB',
    chave_rps_numero=4102,
    TipoRPS='RPS',
    DataEmissao=date(2015, 1, 20),
    StatusRPS='N',
    TributacaoRPS='T',
    ValorCargaTributaria=Decimal('30.25'),
    PercenturalCargaTributaria=Decimal('15.12'),
    CodigoServico=7811
)

# serviço
servico2 = Servico(
    valor_servico=Decimal('101.00'),
    iss_retido=2,  # 1 - Sim; 2 - Não
    discriminacao='Nota Fiscal 2 de Teste Emitida por Cliente Web',
    valor_deducoes=Decimal('0.00'),
    valor_pis=Decimal('2.01'),
    valor_confins=Decimal('2.02'),
    valor_inss=Decimal('2.03'),
    valor_ir=Decimal('2.04'),
    valor_csll=Decimal('2.05'),
    aliquota=Decimal('0.05'),
)

rps2 = RPS(
    emitente=emitente,
    cliente=cliente1,  # mesmo cliente
    servico=servico2,
    chave_rps_serie='BC',
    chave_rps_numero=4103,
    TipoRPS='RPS',
    DataEmissao=date(2015, 1, 21),
    StatusRPS='N',
    TributacaoRPS='F',
    ValorCargaTributaria=Decimal('20.21'),
    PercenturalCargaTributaria=Decimal('17.14'),
    CodigoServico=7811
)

certificado = r"C:\Users\BDR3\Downloads\BDR_INVESTIMENTOS_LTDA_35132740000166_1589478520733321500.pfx"
senha = '1234'
homologacao = False

# serialização
serializador = SerializacaoNfse('saopaulo')
xml = serializador.envio_lote_rps([rps1, rps2], date(2015, 1, 1), date(2015, 1, 26))

# assinatura

a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar_rps(xml)
xml = a1.assinar(xml, retorna_string=True)

# envio
con = ComunicacaoNfse(certificado, senha, 'saopaulo', homologacao)
resposta = con.enviar_lote(xml)  # não funcionando ainda

print()
