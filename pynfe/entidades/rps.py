import decimal as decimal_

from .base import Entidade


class RPS(Entidade):
    """Tipo que representa um RPS."""

    cliente = None
    emitente = None
    servico = None

    chave_rps_serie = None
    chave_rps_numero = None

    gds_collector_ = None
    gds_elementtree_node_ = None
    original_tagname_ = None
    parent_object_ = None
    ns_prefix_ = None
    Assinatura = None

    TipoRPS = str()

    DataEmissao = None

    StatusRPS = str()

    TributacaoRPS = str()

    ValorServicos = decimal_.Decimal()

    ValorDeducoes = decimal_.Decimal()

    ValorPIS = decimal_.Decimal()

    ValorCOFINS = decimal_.Decimal()

    ValorINSS = decimal_.Decimal()

    ValorIR = decimal_.Decimal()

    ValorCSLL = decimal_.Decimal()

    CodigoServico = int()

    AliquotaServicos = decimal_.Decimal()

    ISSRetido = None

    CPFCNPJTomador = None

    InscricaoMunicipalTomador = None

    InscricaoEstadualTomador = None

    RazaoSocialTomador = str()

    EnderecoTomador = str()

    EmailTomador = str()

    CPFCNPJIntermediario = None

    InscricaoMunicipalIntermediario = None

    ISSRetidoIntermediario = None

    # E-mail do intermediário
    EmailIntermediario = str()

    # Discriminação dos serviços
    Discriminacao = None

    ValorCargaTributaria = decimal_.Decimal()

    PercentualCargaTributaria = decimal_.Decimal()

    FonteCargaTributaria = str()

    CodigoCEI = None

    MatriculaObra = None

    MunicipioPrestacao = None

    NumeroEncapsulamento = None

    ValorTotalRecebido = None
