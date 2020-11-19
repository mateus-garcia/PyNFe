# -*- coding: utf-8 -*-
import signxml
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from signxml import XMLSigner

from pynfe.entidades import CertificadoA1
from pynfe.utils import etree, remover_acentos
from pynfe.utils.flags import NAMESPACE_SIG


class Assinatura(object):
    """Classe abstrata responsavel por definir os metodos e logica das classes
    de assinatura digital."""

    certificado = None
    senha = None

    def __init__(self, certificado, senha, autorizador=None):
        self.certificado = certificado
        self.senha = senha
        self.autorizador = autorizador

    def assinar(self, xml):
        """Efetua a assinatura da nota"""
        pass


class AssinaturaA1(Assinatura):

    def __init__(self, certificado, senha):
        self.key, self.cert = CertificadoA1(certificado).separar_arquivo(senha)

    def assinar(self, xml, retorna_string=False):
        # busca tag que tem id(reference_uri), logo nao importa se tem namespace
        try:
            reference = xml.find(".//*[@Id]").attrib['Id']
        except AttributeError:
            reference = ''

        # retira acentos
        xml_str = remover_acentos(etree.tostring(xml, encoding="unicode", pretty_print=False))
        xml = etree.fromstring(xml_str)

        signer = XMLSigner(
            method=signxml.methods.enveloped, signature_algorithm="rsa-sha1",
            digest_algorithm='sha1',
            c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315')

        ns = {None: signer.namespaces['ds']}
        signer.namespaces = ns

        ref_uri = ('#%s' % reference) if reference else None
        signed_root = signer.sign(
            xml, key=self.key, cert=self.cert, reference_uri=ref_uri)

        ns = {'ns': NAMESPACE_SIG}
        # coloca o certificado na tag X509Data/X509Certificate
        tagX509Data = signed_root.find('.//ns:X509Data', namespaces=ns)
        etree.SubElement(tagX509Data, 'X509Certificate').text = self.cert
        if retorna_string:
            return etree.tostring(signed_root, encoding="unicode", pretty_print=False)
        else:
            return signed_root

    def assinar_rps(self, xml, retorna_string=False):
        """
        Função para gerar a assinatura do rps, seguindo o padrão do werbservice de São Paulo
        @param xml: lxml.etree._Element
        @param retorna_string:
        @return: xml
        """
        pri_key = RSA.importKey(self.key)

        for assinatura in [x for x in xml.xpath('//*') if 'Assinatura' in x.tag]:
            ass_text = assinatura.text
            digest = SHA.new(ass_text.encode('ascii'))
            signature = PKCS1_v1_5.new(pri_key).sign(digest).hex()
            assinatura.text = signature

        if retorna_string:
            return etree.tostring(xml, encoding="unicode", pretty_print=False)
        else:
            return xml
