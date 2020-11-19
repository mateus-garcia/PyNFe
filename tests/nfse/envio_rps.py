from datetime import date
from decimal import Decimal

from pynfe.entidades.cliente import Cliente
from pynfe.entidades.emitente import Emitente
from pynfe.entidades.notafiscal import NotaFiscalServico
from pynfe.entidades.rps import RPS
from pynfe.entidades.servico import Servico
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.serializacao import SerializacaoNfse
from pynfe.utils import obter_codigo_por_municipio
from pynfe.utils.flags import CODIGO_BRASIL

# prestador
emitente = Emitente(
    cnpj='99999999999999',
    inscricao_municipal='31000000'
)

# tomador
cliente = Cliente(
    razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
    tipo_documento='CPF',  # CPF ou CNPJ
    numero_documento='13167474254',  # apenas os numero do CPF ou CNPJ
    inscricao_municipal='1234',  # opcional
    endereco_tipo_logradouro='Rua',
    endereco_logradouro='tal',
    endereco_numero='0',
    endereco_complemento='Ao lado de lugar nenhum',  # opcional
    endereco_bairro='Centro',
    endereco_cod_municipio='123',
    endereco_uf='PR',
    endereco_cep='87704000',
    endereco_pais=CODIGO_BRASIL,
    endereco_telefone='12365478945',  # opcional
    email='nome@email.com.br'  # opcional
)

# serviço
servico = Servico(
    valor_servico=Decimal('20500.00'),
    iss_retido=2,  # 1 - Sim; 2 - Não
    item_lista='0101',
    discriminacao='Mensalidade',
    codigo_municipio=obter_codigo_por_municipio('Paranavaí', 'PR'),
    # Dados opcionais
    codigo_cnae=6201501,
    codigo_tributacao_municipio=1234,
    valor_deducoes=Decimal('5000.00'),
    valor_pis=Decimal('10.00'),
    valor_confins=Decimal('10.00'),
    valor_inss=Decimal('10.00'),
    valor_ir=Decimal('10.00'),
    valor_csll=Decimal('10.00'),
    valor_iss=Decimal('10.00'),
    valor_iss_retido=Decimal('10.00'),
    valor_liquido=Decimal('10.00'),
    outras_retencoes=Decimal('10.00'),
    base_calculo=Decimal('10.00'),
    aliquota=Decimal('10.00'),
    desconto_incondicionado=Decimal('10.00'),
    desconto_condicionado=Decimal('10.00')
)

# nota
nota = NotaFiscalServico(
    identificador='50',
    data_emissao=date.today(),
    servico=servico,
    emitente=emitente,
    cliente=cliente,
    # Optante Simples Nacional
    simples=1,  # 1-Sim; 2-Não
    natureza_operacao=1,  # 1 – Tributação no município 2 - Tributação fora do município 3 - Isenção 4 - Imune
    # 5 –Exigibilidade suspensa por decisão judicial 6 – Exigibilidade suspensa por procedimento administrativo
    # regime_especial=1, # Regime Especial de Tributação: 1 – Microempresa municipal 2 - Estimativa
    # 3 – Sociedade de profissionais 4 – Cooperativa 5 - Microempresário Individual (MEI)
    # 6 - Microempresário e Empresa de Pequeno Porte (ME EPP)
    incentivo=2,  # Incentivador Cultural # 1-Sim; 2-Não
    serie='A1',
    tipo='1'
)

rps = RPS(
    emitente=emitente,
    cliente=cliente,
    servico=servico,
    chave_rps_serie='OL03',
    chave_rps_numero=1,
    TipoRPS='RPS',
    DataEmissao=date(2007, 1, 3),
    StatusRPS='N',
    TributacaoRPS='T',
    ValorCargaTributaria=Decimal('20.21'),
    PercenturalCargaTributaria=Decimal('17.14'),
    CodigoServico=2658
)

certificado = r"C:\Users\BDR3\Downloads\BDR_INVESTIMENTOS_LTDA_35132740000166_1589478520733321500.pfx"
senha = '1234'
homologacao = False

# serialização
serializador = SerializacaoNfse('saopaulo')
xml = serializador.envio_rps(rps)

# assinatura

a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar_rps(xml)
xml = a1.assinar(xml)

# envio
# Não testado !!!!!!!!!!!
# con = ComunicacaoNfse(certificado, senha, 'saopaulo', homologacao)
# envio = con.enviar_lote(xml)

print()
