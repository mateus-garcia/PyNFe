import io
from importlib import import_module

from lxml import etree
from pyxb import BIND


class InterfaceAutorizador():
    # TODO Colocar raise Exception Not Implemented nos metodos
    def consultar_rps(self):
        pass

    def cancelar(self):
        pass


class SerializacaoBetha(InterfaceAutorizador):
    def __init__(self):
        # importa
        global nfse_schema
        nfse_schema = import_module('pynfe.utils.nfse.betha.nfse_v202')

    def gerar(self, nfse):
        """Retorna string de um XML gerado a partir do
        XML Schema (XSD). Binding gerado pelo modulo PyXB."""

        servico = nfse_schema.tcDadosServico()
        valores_servico = nfse_schema.tcValoresDeclaracaoServico()
        valores_servico.ValorServicos = nfse.servico.valor_servico

        servico.IssRetido = nfse.servico.iss_retido
        servico.ItemListaServico = nfse.servico.item_lista
        servico.Discriminacao = nfse.servico.discriminacao
        servico.CodigoMunicipio = nfse.servico.codigo_municipio
        servico.ExigibilidadeISS = nfse.servico.exigibilidade
        servico.MunicipioIncidencia = nfse.servico.municipio_incidencia
        servico.Valores = valores_servico

        # Prestador
        id_prestador = nfse_schema.tcIdentificacaoPrestador()
        id_prestador.CpfCnpj = nfse.emitente.cnpj
        id_prestador.InscricaoMunicipal = nfse.emitente.inscricao_municipal

        # Cliente
        id_tomador = nfse_schema.tcIdentificacaoTomador()
        id_tomador.CpfCnpj = nfse.cliente.numero_documento
        if nfse.cliente.inscricao_municipal:
            id_tomador.InscricaoMunicipal = nfse.cliente.inscricao_municipal

        endereco_tomador = nfse_schema.tcEndereco()
        endereco_tomador.Endereco = nfse.cliente.endereco_logradouro
        endereco_tomador.Numero = nfse.cliente.endereco_numero
        endereco_tomador.Bairro = nfse.cliente.endereco_bairro
        endereco_tomador.CodigoMunicipio = nfse.cliente.endereco_cod_municipio
        endereco_tomador.Uf = nfse.cliente.endereco_uf
        endereco_tomador.CodigoPais = nfse.cliente.endereco_pais
        endereco_tomador.Cep = nfse.cliente.endereco_cep

        tomador = nfse_schema.tcDadosTomador()
        tomador.IdentificacaoPrestador = id_tomador
        tomador.RazaoSocial = nfse.cliente.razao_social
        tomador.Endereco = endereco_tomador

        id_rps = nfse_schema.tcIdentificacaoRps()
        id_rps.Numero = nfse.identificador
        id_rps.Serie = nfse.serie
        id_rps.Tipo = nfse.tipo

        rps = nfse_schema.tcInfRps()
        rps.IdentificacaoRps = id_rps
        rps.DataEmissao = nfse.data_emissao.strftime('%Y-%m-%d')
        rps.Status = 1

        inf_declaracao_servico = nfse_schema.tcInfDeclaracaoPrestacaoServico()
        inf_declaracao_servico.Competencia = nfse.data_emissao.strftime('%Y-%m-%d')
        inf_declaracao_servico.Servico = servico
        inf_declaracao_servico.Prestador = id_prestador
        inf_declaracao_servico.Tomador = tomador
        inf_declaracao_servico.OptanteSimplesNacional = nfse.simples
        inf_declaracao_servico.IncentivoFiscal = nfse.incentivo
        inf_declaracao_servico.Id = nfse.identificador
        inf_declaracao_servico.Rps = rps

        declaracao_servico = nfse_schema.tcDeclaracaoPrestacaoServico()
        declaracao_servico.InfDeclaracaoPrestacaoServico = inf_declaracao_servico

        gnfse = nfse_schema.GerarNfseEnvio()
        gnfse.Rps = declaracao_servico

        return gnfse.toxml(element_name='GerarNfseEnvio')

    def consultar_rps(self, nfse):
        """Retorna string de um XML gerado a partir do
        XML Schema (XSD). Binding gerado pelo modulo PyXB."""

        # Rps
        id_rps = nfse_schema.tcIdentificacaoRps()
        id_rps.Numero = nfse.identificador
        id_rps.Serie = nfse.serie
        id_rps.Tipo = nfse.tipo

        # Prestador
        id_prestador = nfse_schema.tcIdentificacaoPrestador()
        id_prestador.CpfCnpj = nfse.emitente.cnpj
        id_prestador.InscricaoMunicipal = nfse.emitente.inscricao_municipal

        consulta = nfse_schema.ConsultarNfseRpsEnvio()
        consulta.IdentificacaoRps = id_rps
        consulta.Prestador = id_prestador

        consulta = consulta.toxml(element_name='ConsultarNfseRpsEnvio').replace('ns1:', '').replace(':ns1', '').replace(
            '<?xml version="1.0" ?>', '')

        return consulta

    def consultar_faixa(self, emitente, inicio, fim, pagina):
        """Retorna string de um XML gerado a partir do
        XML Schema (XSD). Binding gerado pelo modulo PyXB."""

        # Prestador
        id_prestador = nfse_schema.tcIdentificacaoPrestador()
        id_prestador.CpfCnpj = emitente.cnpj
        id_prestador.InscricaoMunicipal = emitente.inscricao_municipal

        consulta = nfse_schema.ConsultarNfseFaixaEnvio()
        consulta.Prestador = id_prestador
        consulta.Pagina = pagina
        # É necessário BIND antes de atribuir numero final e numero inicial
        consulta.Faixa = BIND()
        consulta.Faixa.NumeroNfseInicial = inicio
        consulta.Faixa.NumeroNfseFinal = fim

        consulta = consulta.toxml(element_name='ConsultarNfseFaixaEnvio').replace('ns1:', '').replace(':ns1',
                                                                                                      '').replace(
            '<?xml version="1.0" ?>', '')

        return consulta

    def cancelar(self, nfse):
        """Retorna string de um XML gerado a partir do
        XML Schema (XSD). Binding gerado pelo modulo PyXB."""

        # id nfse
        id_nfse = nfse_schema.tcIdentificacaoNfse()
        id_nfse.Numero = nfse.identificador
        id_nfse.CpfCnpj = nfse.emitente.cnpj
        id_nfse.InscricaoMunicipal = nfse.emitente.inscricao_municipal
        id_nfse.CodigoMunicipio = nfse.emitente.endereco_cod_municipio

        # Info Pedido de cancelamento
        info_pedido = nfse_schema.tcInfPedidoCancelamento()
        info_pedido.Id = '1'
        info_pedido.IdentificacaoNfse = id_nfse
        # pedido.CodigoCancelamento =

        # Pedido
        pedido = nfse_schema.tcPedidoCancelamento()
        pedido.InfPedidoCancelamento = info_pedido

        # Cancelamento
        cancelar = nfse_schema.CancelarNfseEnvio()
        cancelar.Pedido = pedido

        return cancelar.toxml(element_name='CancelarNfseEnvio')

    def serializar_lote_sincrono(self, nfse):
        """Retorna string de um XML gerado a partir do
        XML Schema (XSD). Binding gerado pelo modulo PyXB."""

        servico = nfse_schema.tcDadosServico()
        valores_servico = nfse_schema.tcValoresDeclaracaoServico()
        valores_servico.ValorServicos = nfse.servico.valor_servico

        servico.IssRetido = nfse.servico.iss_retido
        servico.ItemListaServico = nfse.servico.item_lista
        servico.Discriminacao = nfse.servico.discriminacao
        servico.CodigoMunicipio = nfse.servico.codigo_municipio
        servico.ExigibilidadeISS = nfse.servico.exigibilidade
        servico.MunicipioIncidencia = nfse.servico.municipio_incidencia
        servico.Valores = valores_servico

        # Prestador
        id_prestador = nfse_schema.tcIdentificacaoPrestador()
        id_prestador.CpfCnpj = nfse.emitente.cnpj
        id_prestador.InscricaoMunicipal = nfse.emitente.inscricao_municipal

        # Cliente
        id_tomador = nfse_schema.tcIdentificacaoTomador()
        id_tomador.CpfCnpj = nfse.cliente.numero_documento
        if nfse.cliente.inscricao_municipal:
            id_tomador.InscricaoMunicipal = nfse.cliente.inscricao_municipal

        endereco_tomador = nfse_schema.tcEndereco()
        endereco_tomador.Endereco = nfse.cliente.endereco_logradouro
        endereco_tomador.Numero = nfse.cliente.endereco_numero
        endereco_tomador.Bairro = nfse.cliente.endereco_bairro
        endereco_tomador.CodigoMunicipio = nfse.cliente.endereco_cod_municipio
        endereco_tomador.Uf = nfse.cliente.endereco_uf
        endereco_tomador.CodigoPais = nfse.cliente.endereco_pais
        endereco_tomador.Cep = nfse.cliente.endereco_cep

        tomador = nfse_schema.tcDadosTomador()
        tomador.IdentificacaoPrestador = id_tomador
        tomador.RazaoSocial = nfse.cliente.razao_social
        tomador.Endereco = endereco_tomador

        id_rps = nfse_schema.tcIdentificacaoRps()
        id_rps.Numero = nfse.identificador
        id_rps.Serie = nfse.serie
        id_rps.Tipo = nfse.tipo

        rps = nfse_schema.tcInfRps()
        rps.IdentificacaoRps = id_rps
        rps.DataEmissao = nfse.data_emissao.strftime('%Y-%m-%d')
        rps.Status = 1

        inf_declaracao_servico = nfse_schema.tcInfDeclaracaoPrestacaoServico()
        inf_declaracao_servico.Competencia = nfse.data_emissao.strftime('%Y-%m-%d')
        inf_declaracao_servico.Servico = servico
        inf_declaracao_servico.Prestador = id_prestador
        inf_declaracao_servico.Tomador = tomador
        inf_declaracao_servico.OptanteSimplesNacional = nfse.simples
        inf_declaracao_servico.IncentivoFiscal = nfse.incentivo
        inf_declaracao_servico.Id = nfse.identificador
        inf_declaracao_servico.Rps = rps

        declaracao_servico = nfse_schema.tcDeclaracaoPrestacaoServico()
        declaracao_servico.InfDeclaracaoPrestacaoServico = inf_declaracao_servico

        lote = nfse_schema.tcLoteRps()
        lote.NumeroLote = 1
        lote.Id = 1
        lote.CpfCnpj = nfse.emitente.cnpj
        lote.InscricaoMunicipal = nfse.emitente.inscricao_municipal
        lote.QuantidadeRps = 1
        if nfse.autorizador.upper() == 'BETHA':
            lote.versao = '2.02'
        lote.ListaRps = BIND(declaracao_servico)

        gnfse = nfse_schema.EnviarLoteRpsSincronoEnvio()
        gnfse.LoteRps = lote

        return gnfse.toxml(element_name='EnviarLoteRpsSincronoEnvio')


class SerializacaoGinfes(InterfaceAutorizador):
    def __init__(self):
        # importa
        global _tipos, servico_consultar_nfse_envio_v03
        global servico_enviar_lote_rps_envio_v03, cabecalho_v03
        global servico_cancelar_nfse_envio_v03
        global servico_consultar_lote_rps_envio_v03
        global servico_consultar_situacao_lote_rps_envio_v03
        global servico_consultar_nfse_rps_envio_v03
        _tipos = import_module('pynfe.utils.nfse.ginfes._tipos')
        servico_consultar_nfse_envio_v03 = import_module('pynfe.utils.nfse.ginfes.servico_consultar_nfse_envio_v03')
        servico_cancelar_nfse_envio_v03 = import_module('pynfe.utils.nfse.ginfes.servico_cancelar_nfse_envio_v03')
        servico_enviar_lote_rps_envio_v03 = import_module('pynfe.utils.nfse.ginfes.servico_enviar_lote_rps_envio_v03')
        cabecalho_v03 = import_module('pynfe.utils.nfse.ginfes.cabecalho_v03')
        servico_consultar_lote_rps_envio_v03 = import_module(
            'pynfe.utils.nfse.ginfes.servico_consultar_lote_rps_envio_v03')
        servico_consultar_situacao_lote_rps_envio_v03 = import_module(
            'pynfe.utils.nfse.ginfes.servico_consultar_situacao_lote_rps_envio_v03')
        servico_consultar_nfse_rps_envio_v03 = import_module(
            'pynfe.utils.nfse.ginfes.servico_consultar_nfse_rps_envio_v03')

    def consultar_rps(self, emitente, numero, serie, tipo):
        """ Retorna string de um XML de consulta por Rps gerado a partir do
            XML Schema (XSD). Binding gerado pelo modulo PyXB.
            servico_consultar_nfse_rps_envio_v03.xsd
        """
        # Rps
        id_rps = _tipos.tcIdentificacaoRps()
        id_rps.Numero = numero
        id_rps.Serie = serie
        id_rps.Tipo = tipo

        # Prestador
        id_prestador = _tipos.tcIdentificacaoPrestador()
        id_prestador.Cnpj = emitente.cnpj
        id_prestador.InscricaoMunicipal = emitente.inscricao_municipal

        consulta = servico_consultar_nfse_rps_envio_v03.ConsultarNfseRpsEnvio()
        consulta.IdentificacaoRps = id_rps
        consulta.Prestador = id_prestador

        return consulta.toxml(element_name='ns1:ConsultarNfseRpsEnvio')

    def consultar_nfse(self, emitente, numero=None, inicio=None, fim=None):
        # Prestador
        id_prestador = _tipos.tcIdentificacaoPrestador()
        id_prestador.Cnpj = emitente.cnpj
        id_prestador.InscricaoMunicipal = emitente.inscricao_municipal

        consulta = servico_consultar_nfse_envio_v03.ConsultarNfseEnvio()
        consulta.Prestador = id_prestador
        # Consulta por Numero
        if numero is not None:
            consulta.NumeroNfse = numero
        else:
            # consulta por Data
            consulta.PeriodoEmissao = BIND()
            consulta.PeriodoEmissao.DataInicial = inicio
            consulta.PeriodoEmissao.DataFinal = fim

        return consulta.toxml(element_name='ns1:ConsultarNfseEnvio')

    def consultar_lote(self, emitente, numero):
        # Prestador
        id_prestador = _tipos.tcIdentificacaoPrestador()
        id_prestador.Cnpj = emitente.cnpj
        id_prestador.InscricaoMunicipal = emitente.inscricao_municipal

        consulta = servico_consultar_lote_rps_envio_v03.ConsultarLoteRpsEnvio()
        consulta.Prestador = id_prestador
        consulta.Protocolo = str(numero)

        return consulta.toxml(element_name='ns1:ConsultarLoteRpsEnvio')

    def consultar_situacao_lote(self, emitente, numero):
        "Serializa lote de envio, baseado no servico_consultar_situacao_lote_rps_envio_v03.xsd"
        # Prestador
        id_prestador = _tipos.tcIdentificacaoPrestador()
        id_prestador.Cnpj = emitente.cnpj
        id_prestador.InscricaoMunicipal = emitente.inscricao_municipal

        consulta = servico_consultar_situacao_lote_rps_envio_v03.ConsultarSituacaoLoteRpsEnvio()
        consulta.Prestador = id_prestador
        consulta.Protocolo = str(numero)

        return consulta.toxml(element_name='ns1:ConsultarSituacaoLoteRpsEnvio')

    def serializar_lote_assincrono(self, nfse):
        "Serializa lote de envio, baseado no servico_enviar_lote_rps_envio_v03.xsd"

        servico = _tipos.tcDadosServico()
        valores_servico = _tipos.tcValores()
        valores_servico.ValorServicos = nfse.servico.valor_servico
        # valores_servico.ValorServicos = str(Decimal(nfse.servico.valor_servico.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)))
        valores_servico.IssRetido = nfse.servico.iss_retido
        # Dados opcionais
        if nfse.servico.valor_deducoes:
            valores_servico.ValorDeducoes = nfse.servico.valor_deducoes
        if nfse.servico.valor_pis:
            valores_servico.ValorPis = nfse.servico.valor_pis
        if nfse.servico.valor_confins:
            valores_servico.ValorCofins = nfse.servico.valor_confins
        if nfse.servico.valor_inss:
            valores_servico.ValorInss = nfse.servico.valor_inss
        if nfse.servico.valor_ir:
            valores_servico.ValorIr = nfse.servico.valor_ir
        if nfse.servico.valor_csll:
            valores_servico.ValorCsll = nfse.servico.valor_csll
        if nfse.servico.valor_iss:
            valores_servico.ValorIss = nfse.servico.valor_iss
        if nfse.servico.valor_iss_retido:
            valores_servico.ValorIssRetido = nfse.servico.valor_iss_retido
        if nfse.servico.valor_liquido:
            valores_servico.ValorLiquidoNfse = nfse.servico.valor_liquido
        if nfse.servico.outras_retencoes:
            valores_servico.OutrasRetencoes = nfse.servico.outras_retencoes
        if nfse.servico.base_calculo:
            valores_servico.BaseCalculo = nfse.servico.base_calculo
        if nfse.servico.aliquota:
            valores_servico.Aliquota = nfse.servico.aliquota
        if nfse.servico.desconto_incondicionado:
            valores_servico.DescontoIncondicionado = nfse.servico.desconto_incondicionado
        if nfse.servico.desconto_condicionado:
            valores_servico.DescontoCondicionado = nfse.servico.desconto_condicionado

        servico.Valores = valores_servico
        servico.ItemListaServico = nfse.servico.item_lista
        # opcionais
        if nfse.servico.codigo_cnae:
            servico.CodigoCnae = nfse.servico.codigo_cnae
        if nfse.servico.codigo_tributacao_municipio:
            servico.CodigoTributacaoMunicipio = nfse.servico.codigo_tributacao_municipio
        # obrigatórios
        servico.Discriminacao = nfse.servico.discriminacao
        servico.CodigoMunicipio = nfse.servico.codigo_municipio

        # endereco tomador
        endereco_tomador = _tipos.tcEndereco()
        endereco_tomador.Endereco = nfse.cliente.endereco_logradouro
        if nfse.cliente.endereco_complemento:
            endereco_tomador.Complemento = nfse.cliente.endereco_complemento
        endereco_tomador.Numero = nfse.cliente.endereco_numero
        endereco_tomador.Bairro = nfse.cliente.endereco_bairro
        if nfse.cliente.endereco_cod_municipio:
            endereco_tomador.CodigoMunicipio = nfse.cliente.endereco_cod_municipio
        endereco_tomador.Uf = nfse.cliente.endereco_uf
        endereco_tomador.Cep = nfse.cliente.endereco_cep
        # identificacao Tomador
        id_tomador = _tipos.tcIdentificacaoTomador()
        id_tomador.CpfCnpj = nfse.cliente.numero_documento
        if nfse.cliente.inscricao_municipal:
            id_tomador.InscricaoMunicipal = nfse.cliente.inscricao_municipal
        # Tomador
        tomador = _tipos.tcDadosTomador()
        tomador.IdentificacaoTomador = id_tomador
        tomador.RazaoSocial = nfse.cliente.razao_social
        tomador.Endereco = endereco_tomador
        # opcional
        if nfse.cliente.endereco_telefone or nfse.cliente.email:
            tomador.Contato = _tipos.tcContato()
            if nfse.cliente.endereco_telefone:
                tomador.Contato.Telefone = nfse.cliente.endereco_telefone
            if nfse.cliente.email:
                tomador.Contato.Email = nfse.cliente.email

        # Prestador
        id_prestador = _tipos.tcIdentificacaoPrestador()
        id_prestador.Cnpj = nfse.emitente.cnpj
        id_prestador.InscricaoMunicipal = nfse.emitente.inscricao_municipal

        # identificacao rps
        id_rps = _tipos.tcIdentificacaoRps()
        id_rps.Numero = nfse.identificador
        id_rps.Serie = nfse.serie
        id_rps.Tipo = nfse.tipo
        # inf rps
        inf_rps = _tipos.tcInfRps()
        inf_rps.IdentificacaoRps = id_rps
        inf_rps.DataEmissao = nfse.data_emissao.strftime('%Y-%m-%dT%H:%M:%S')
        # Natureza da Operação
        # 1 – Tributação no município
        # 2 - Tributação fora do município
        # 3 - Isenção
        # 4 - Imune
        # 5 –Exigibilidade suspensa por decisão judicial
        # 6 – Exigibilidade suspensa por procedimento administrativo
        inf_rps.NaturezaOperacao = nfse.natureza_operacao
        # Regime Especial de Tributação
        # 1 – Microempresa municipal
        # 2 - Estimativa
        # 3 – Sociedade de profissionais
        # 4 – Cooperativa
        # 5 - Microempresário Individual (MEI)
        # 6 - Microempresário e Empresa de Pequeno Porte (ME EPP)
        if nfse.regime_especial:
            inf_rps.RegimeEspecialTributacao = nfse.regime_especial
        inf_rps.OptanteSimplesNacional = nfse.simples  # 1-sim 2-nao
        inf_rps.IncentivadorCultural = nfse.incentivo  # 1-sim 2-nao
        # Código de status da NFS-e
        inf_rps.Status = 1  # 1 – Normal 2 – Cancelado (sempre 1, pois a nota não pode ser enviada como cancelada)
        inf_rps.RpsSubstituido = None  # opcional 
        inf_rps.Servico = servico
        inf_rps.Prestador = id_prestador
        inf_rps.Tomador = tomador
        inf_rps.IntermediarioServico = None  # opcional
        inf_rps.ConstrucaoCivil = None  # opcional
        inf_rps.Id = nfse.identificador

        rps = _tipos.tcRps()
        rps.InfRps = inf_rps

        lote = _tipos.tcLoteRps()
        lote.NumeroLote = 1
        lote.Id = 1
        lote.Cnpj = nfse.emitente.cnpj
        lote.InscricaoMunicipal = nfse.emitente.inscricao_municipal
        lote.QuantidadeRps = 1
        lote.ListaRps = BIND()
        lote.ListaRps.append(rps)

        enviarLote = servico_enviar_lote_rps_envio_v03.EnviarLoteRpsEnvio()
        enviarLote.LoteRps = lote
        return enviarLote.toxml(element_name='ns1:EnviarLoteRpsEnvio')

    def cancelar(self, nfse, codigo):
        """Retorna string de um XML gerado a partir do
        XML Schema (XSD). Binding gerado pelo modulo PyXB."""
        # id nfse
        id_nfse = _tipos.tcIdentificacaoNfse()
        id_nfse.Numero = nfse.identificador
        id_nfse.Cnpj = nfse.emitente.cnpj
        id_nfse.InscricaoMunicipal = nfse.emitente.inscricao_municipal
        id_nfse.CodigoMunicipio = nfse.emitente.endereco_cod_municipio

        # Info Pedido de cancelamento
        info_pedido = _tipos.tcInfPedidoCancelamento()
        info_pedido.Id = '1'
        info_pedido.IdentificacaoNfse = id_nfse
        info_pedido.CodigoCancelamento = codigo

        # Pedido
        pedido = _tipos.tcPedidoCancelamento()
        pedido.InfPedidoCancelamento = info_pedido

        # Cancelamento
        cancelar = servico_cancelar_nfse_envio_v03.CancelarNfseEnvio()
        cancelar.Pedido = pedido

        return cancelar.toxml(element_name='ns1:CancelarNfseEnvio')

    def cancelar_v2(self, nfse):
        ## serialização utilizando lxml
        from lxml import etree
        ns1 = 'http://www.ginfes.com.br/servico_cancelar_nfse_envio'
        ns2 = 'http://www.ginfes.com.br/tipos'
        raiz = etree.Element('{%s}CancelarNfseEnvio' % ns1, nsmap={'ns1': ns1, 'ns2': ns2})
        prestador = etree.SubElement(raiz, '{%s}Prestador' % ns1)
        etree.SubElement(prestador, '{%s}Cnpj' % ns2).text = nfse.emitente.cnpj
        etree.SubElement(prestador, '{%s}InscricaoMunicipal' % ns2).text = nfse.emitente.inscricao_municipal
        etree.SubElement(raiz, '{%s}NumeroNfse' % ns1).text = nfse.identificador
        return etree.tostring(raiz, encoding='unicode')

    def cabecalho(self):
        # info
        cabecalho = cabecalho_v03.cabecalho()
        cabecalho.versao = '3'
        cabecalho.versaoDados = '3'
        return cabecalho.toxml(element_name='ns2:cabecalho')


class SerializacaoSP(InterfaceAutorizador):
    def __init__(self):
        # importa
        global _tipos, servico_cancela_lote_v01
        global servico_cancela_NFe_v01, servico_consulta_CNPJ_v01
        global servico_consulta_lote_v01
        global servico_consulta_NFe_periodo_v01
        global servico_consulta_NFe_v01
        global servico_envio_lote_RPS_v01
        global servico_envio_RPS_v01
        global servico_informacoes_lote_v01
        _tipos = import_module('pynfe.utils.nfse.sp._tipos')
        servico_cancela_lote_v01 = import_module('pynfe.utils.nfse.sp.servico_cancela_lote_v01')
        servico_cancela_NFe_v01 = import_module('pynfe.utils.nfse.sp.servico_cancela_NFe_v01')
        servico_consulta_CNPJ_v01 = import_module('pynfe.utils.nfse.sp.servico_consulta_CNPJ_v01')
        servico_consulta_lote_v01 = import_module('pynfe.utils.nfse.sp.servico_consulta_lote_v01')
        servico_consulta_NFe_periodo_v01 = import_module('pynfe.utils.nfse.sp.servico_consulta_NFe_periodo_v01')
        servico_consulta_NFe_v01 = import_module('pynfe.utils.nfse.sp.servico_consulta_NFe_v01')
        servico_envio_lote_RPS_v01 = import_module('pynfe.utils.nfse.sp.servico_envio_lote_RPS_v01')
        servico_envio_RPS_v01 = import_module('pynfe.utils.nfse.sp.servico_envio_RPS_v01')
        servico_informacoes_lote_v01 = import_module('pynfe.utils.nfse.sp.servico_informacoes_lote_v01')

    def consultar_nfse(self, emitente, numero=None, inicio=None, fim=None):
        # CPFCNPJ
        CPFCNPJ = _tipos.tpCPFCNPJ()
        CPFCNPJ.CNPJ = emitente.cnpj

        # Cabecalho
        cabecalho = servico_consulta_NFe_v01.CabecalhoType()
        cabecalho.Versao = int(1)
        cabecalho.CPFCNPJRemetente = CPFCNPJ

        # Chave
        chave = _tipos.tpChaveNFeRPS()
        chaveNfe = _tipos.tpChaveNFe()
        chaveNfe.InscricaoPrestador = int(emitente.inscricao_municipal)
        chaveNfe.NumeroNFe = numero
        chave.ChaveNFe = chaveNfe

        # Consulta
        consulta = servico_consulta_NFe_v01.PedidoConsultaNFe()
        consulta.Cabecalho = cabecalho

        consulta.Detalhe.append(chave)
        f_str = io.StringIO()
        consulta.export(f_str, 0,
                        name_='p1:PedidoConsultaNFe',
                        namespacedef_='xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
                        pretty_print=True)
        return etree.fromstring(f_str.getvalue())

    def consultar_nfse_periodo(self, cnpj, emitente, cliente, inicio=None, fim=None):
        # parece ok por enquanto

        # CPFCNPJRementente
        CPFCNPJ = _tipos.tpCPFCNPJ()
        CPFCNPJ.CNPJ = cnpj
        # Cabecalho
        cabecalho = servico_consulta_NFe_periodo_v01.CabecalhoType()
        cabecalho.Versao = int(1)
        cabecalho.CPFCNPJRemetente = CPFCNPJ

        CPF_pedido = _tipos.tpCPFCNPJ()

        if emitente is not None and cliente is None:
            # Pedido de Consulta de NF-e Emitidas (ConsultaNFeEmitidas)
            CPF_pedido.CNPJ = emitente.cnpj
            cabecalho.Inscricao = emitente.inscricao_municipal

        if emitente is None and cliente is not None:
            # Pedido de Consulta de NF-e Recebidas (ConsultaNFeRecebidas)

            if cliente.tipo_documento != 'CNPJ':
                raise ValueError('cliente.tipo_documento != "CNPJ"')
            CPF_pedido.CNPJ = cliente.numero_documento
            cabecalho.Inscricao = int(cliente.inscricao_municipal)
        else:
            raise ValueError('emitente e cliente são None')

        cabecalho.CPFCNPJ = CPF_pedido

        cabecalho.dtInicio = inicio
        cabecalho.dtFim = fim

        # Consulta
        consulta = servico_consulta_NFe_periodo_v01.PedidoConsultaNFePeriodo()
        consulta.Cabecalho = cabecalho

        f_str = io.StringIO()
        consulta.export(f_str, 0,
                        name_='p1:PedidoConsultaNFePeriodo',
                        namespacedef_='xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
                        pretty_print=True)
        return etree.fromstring(f_str.getvalue())

    def consultar_lote(self, emitente, numero=None):
        # CPFCNPJ
        CPFCNPJ = _tipos.tpCPFCNPJ()
        CPFCNPJ.CNPJ = emitente.cnpj

        # Cabecalho
        cabecalho = servico_consulta_lote_v01.CabecalhoType()
        cabecalho.Versao = int(1)
        cabecalho.CPFCNPJRemetente = CPFCNPJ
        cabecalho.NumeroLote = numero

        # Consulta
        consulta = servico_consulta_lote_v01.PedidoConsultaLote()
        consulta.Cabecalho = cabecalho

        f_str = io.StringIO()
        consulta.export(f_str, 0,
                        name_='p1:PedidoConsultaLote',
                        namespacedef_='xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
                        pretty_print=True)
        return etree.fromstring(f_str.getvalue())

    def consultar_situacao_lote(self, emitente, numero):
        # CPFCNPJ
        CPFCNPJ = _tipos.tpCPFCNPJ()
        CPFCNPJ.CNPJ = emitente.cnpj

        # Cabecalho
        cabecalho = servico_informacoes_lote_v01.CabecalhoType()
        cabecalho.Versao = int(1)
        cabecalho.CPFCNPJRemetente = CPFCNPJ
        if numero is not None:
            cabecalho.NumeroLote = numero
        cabecalho.InscricaoPrestador = int(emitente.inscricao_municipal)

        # Consulta
        consulta = servico_informacoes_lote_v01.PedidoInformacoesLote()
        consulta.Cabecalho = cabecalho

        f_str = io.StringIO()
        consulta.export(f_str, 0,
                        name_='p1:PedidoInformacoesLote',
                        namespacedef_='xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
                        pretty_print=True)
        return etree.fromstring(f_str.getvalue())

    def consultar_cnpj(self, remetente, contribuinte):
        # CPFCNPJ
        CPFCNPJ = _tipos.tpCPFCNPJ()
        CPFCNPJ.CNPJ = remetente.cnpj

        # Cabecalho
        cabecalho = servico_consulta_CNPJ_v01.CabecalhoType()
        cabecalho.Versao = int(1)
        cabecalho.CPFCNPJRemetente = CPFCNPJ

        # Consulta
        consulta = servico_consulta_CNPJ_v01.PedidoConsultaCNPJ()
        consulta.Cabecalho = cabecalho
        if contribuinte.tipo_documento != 'CNPJ':
            raise NameError('contribuinte.tipo_documento != "CNPJ"')
        else:
            cnpj_contribuinte = _tipos.tpCPFCNPJ()
            cnpj_contribuinte.CNPJ = contribuinte.numero_documento
            consulta.CNPJContribuinte = cnpj_contribuinte

        f_str = io.StringIO()
        consulta.export(f_str, 0,
                        name_='p1:PedidoConsultaCNPJ',
                        namespacedef_='xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
                        pretty_print=True)
        return etree.fromstring(f_str.getvalue())

    def envio_rps(self, rps):
        # CPFCNPJ
        CPFCNPJ = _tipos.tpCPFCNPJ()
        CPFCNPJ.CNPJ = rps.emitente.cnpj

        # Cabecalho
        cabecalho = servico_envio_RPS_v01.CabecalhoType()
        cabecalho.Versao = int(1)
        cabecalho.CPFCNPJRemetente = CPFCNPJ

        rps_ = self.generate_rps(rps)

        # Pedido
        pedido = servico_envio_RPS_v01.PedidoEnvioRPS()
        pedido.Cabecalho = cabecalho
        pedido.RPS = rps_

        f_str = io.StringIO()
        pedido.export(f_str, 0,
                      name_='PedidoEnvioRPS',
                      namespacedef_='xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://www.prefeitura.sp.gov.br/nfe"',
                      pretty_print=True)
        return etree.fromstring(f_str.getvalue())

    def envio_lote_rps(self, rps_list, inicio, fim, transacao):

        # Pedido
        pedido = servico_envio_lote_RPS_v01.PedidoEnvioLoteRPS()

        valor_total_servicos = 0
        valor_total_deducoes = 0

        for rps in rps_list:
            valor_total_servicos += rps.servico.valor_servico
            valor_total_deducoes += rps.servico.valor_deducoes
            rps_ = self.generate_rps(rps)
            pedido.RPS.append(rps_)

        # CPFCNPJ
        CPFCNPJ = _tipos.tpCPFCNPJ()
        CPFCNPJ.CNPJ = rps_list[0].emitente.cnpj

        # Cabecalho
        cabecalho = servico_envio_lote_RPS_v01.CabecalhoType()
        cabecalho.Versao = int(1)
        cabecalho.CPFCNPJRemetente = CPFCNPJ
        cabecalho.transacao = transacao
        cabecalho.QtdRPS = len(rps_list)
        # transacao = True -> os RPS serão subistituidos por nf se não ocorrer nenhum erro durante o processamento
        # de todod o lote
        # transacao = False -> os RPS válidos serão subistituidos por nf, mesmo que ocorram eventos de erro durante
        # o processamento de outros rps deste lote
        cabecalho.ValorTotalDeducoes = valor_total_deducoes
        cabecalho.ValorTotalServicos = valor_total_servicos
        cabecalho.dtInicio = inicio
        cabecalho.dtFim = fim
        pedido.Cabecalho = cabecalho

        f_str = io.StringIO()
        pedido.export(f_str, 0,
                      name_='PedidoEnvioLoteRPS',
                      namespacedef_='xmlns="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"',
                      pretty_print=True)
        return etree.fromstring(f_str.getvalue())

    def cancelar(self, nfse):
        # CPFCNPJ
        CPFCNPJ = _tipos.tpCPFCNPJ()
        CPFCNPJ.CNPJ = nfse.emitente.cnpj

        # Cabecalho
        cabecalho = servico_cancela_NFe_v01.CabecalhoType()
        cabecalho.Versao = int(1)
        cabecalho.CPFCNPJRemetente = CPFCNPJ

        # Chave
        chave = servico_cancela_NFe_v01.tpChaveNFe()
        chave.InscricaoPrestador = int(nfse.emitente.inscricao_municipal)
        chave.NumeroNFe = int(nfse.identificador)

        # Detalhe
        detalhe = servico_cancela_NFe_v01.DetalheType()
        detalhe.ChaveNFe = chave
        ass = str(nfse.emitente.inscricao_municipal).zfill(8) + str(nfse.identificador).zfill(12)
        detalhe.AssinaturaCancelamento = ass.encode('ASCII', 'ignore')

        # Pedido
        pedido = servico_cancela_NFe_v01.PedidoCancelamentoNFe()
        pedido.Cabecalho = cabecalho
        pedido.Detalhe.append(detalhe)

        f_str = io.StringIO()
        pedido.export(f_str, 0,
                      name_='PedidoCancelamentoNFe',
                      namespacedef_='xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://www.prefeitura.sp.gov.br/nfe"',
                      pretty_print=True)
        return etree.fromstring(f_str.getvalue())

    @staticmethod
    def generate_rps(rps):
        # RPS
        rps_ = _tipos.tpRPS()
        # Chave RPS
        chave = _tipos.tpChaveRPS()
        chave.InscricaoPrestador = int(rps.emitente.inscricao_municipal)  #
        chave.SerieRPS = rps.chave_rps_serie  #
        chave.NumeroRPS = rps.chave_rps_numero  #
        rps_.ChaveRPS = chave

        rps_.TipoRPS = rps.TipoRPS
        rps_.DataEmissao = rps.DataEmissao  #
        rps_.StatusRPS = rps.StatusRPS  #
        rps_.TributacaoRPS = rps.TributacaoRPS  #
        rps_.ValorServicos = rps.servico.valor_servico  #
        rps_.ValorDeducoes = rps.servico.valor_deducoes  #
        rps_.ValorPIS = rps.servico.valor_pis
        rps_.ValorCOFINS = rps.servico.valor_confins
        rps_.ValorINSS = rps.servico.valor_inss
        rps_.ValorIR = rps.servico.valor_ir
        rps_.ValorCSLL = rps.servico.valor_csll
        rps_.CodigoServico = rps.CodigoServico  #
        rps_.AliquotaServicos = rps.servico.aliquota
        if rps.servico.iss_retido == 1:
            rps_.ISSRetido = 'true'  #
            retido = 'S'
        else:
            rps_.ISSRetido = 'false'  #
            retido = 'N'

        CPFCNPJ_tomador = _tipos.tpCPFCNPJ()
        if rps.cliente.tipo_documento == 'CNPJ':
            CPFCNPJ_tomador.CNPJ = rps.cliente.numero_documento  #
            cpfcnpj = '2' + str(rps.cliente.numero_documento).zfill(14)
        else:
            CPFCNPJ_tomador.CPF = rps.cliente.numero_documento  #
            cpfcnpj = '1' + str(rps.cliente.numero_documento).zfill(14)
        rps_.CPFCNPJTomador = CPFCNPJ_tomador

        rps_.InscricaoMunicipalTomador = int(rps.cliente.inscricao_municipal)
        rps_.RazaoSocialTomador = rps.cliente.razao_social

        edereco_tomador = _tipos.tpEndereco()
        edereco_tomador.TipoLogradouro = rps.cliente.endereco_tipo_logradouro
        edereco_tomador.Logradouro = rps.cliente.endereco_logradouro
        edereco_tomador.NumeroEndereco = rps.cliente.endereco_numero
        edereco_tomador.ComplementoEndereco = rps.cliente.endereco_complemento
        edereco_tomador.Bairro = rps.cliente.endereco_bairro
        edereco_tomador.Cidade = int(rps.cliente.endereco_cod_municipio)
        edereco_tomador.UF = rps.cliente.endereco_uf
        edereco_tomador.CEP = int(rps.cliente.endereco_cep)
        rps_.EnderecoTomador = edereco_tomador
        rps_.EmailTomador = rps.cliente.email
        rps_.Discriminacao = rps.servico.discriminacao
        rps_.ValorCargaTributaria = rps.ValorCargaTributaria
        rps_.PercentualCargaTributaria = rps.PercentualCargaTributaria
        try:
            rps_.MunicipioPrestacao = int(rps.servico.codigo_tributacao_municipio)
        except ValueError:
            pass
        rps_.ValorTotalRecebido = rps.servico.valor_liquido

        # não implementado
        # rps_.CPFCNPJIntermediario =
        # rps_.InscricaoMunicipalIntermediario =
        # rps_.ISSRetidoIntermediario =
        # rps_.EmailIntermediario =
        # rps_.CPFCNPJIntermediario =
        # rps_.CodigoCEI =
        # rps_.MatriculaObra =
        # rps_.NumeroEncapsulamento =

        # assinatura

        ass_string = str(rps_.ChaveRPS.InscricaoPrestador) + str(rps_.ChaveRPS.SerieRPS).ljust(5) \
                     + str(rps_.ChaveRPS.NumeroRPS).zfill(12) + rps_.DataEmissao.strftime('%Y%m%d') \
                     + str(rps_.TributacaoRPS) + str(rps_.StatusRPS) + retido \
                     + str(rps_.ValorServicos).replace('.', '').zfill(15) \
                     + str(rps_.ValorDeducoes).replace('.', '').zfill(15) + str(rps_.CodigoServico).zfill(5) \
                     + cpfcnpj
        rps_.Assinatura = ass_string.encode('ASCII', 'ignore')

        return rps_

    def cabecalho(self):
        # info
        cabecalho = servico_informacoes_lote_v01.CabecalhoType()
        cabecalho.versao = '1'
        return cabecalho.toxml(element_name='Cabecalho')
