import html
from app.services.meta.schemas import MetaInput


def strip_data_url(b64: str) -> str:
    prefix = "base64,"
    i = b64.find(prefix)
    return b64[i+len(prefix):] if i != -1 else b64

def xml_escape(s: str) -> str:
    return html.escape(s, quote=True)

def build_xmp(meta: MetaInput) -> bytes:
    # динамически собираем XMP с нужными namespace
    parts = []
    # dc:creator (Seq)
    if meta.creator:
        parts.append(f"""
      <dc:creator>
        <rdf:Seq><rdf:li>{xml_escape(meta.creator)}</rdf:li></rdf:Seq>
      </dc:creator>""")
    # dc:rights (Alt)
    if meta.rights:
        parts.append(f"""
      <dc:rights>
        <rdf:Alt><rdf:li xml:lang="x-default">{xml_escape(meta.rights)}</rdf:li></rdf:Alt>
      </dc:rights>""")
    # dc:title (Alt)
    if meta.title:
        parts.append(f"""
      <dc:title>
        <rdf:Alt><rdf:li xml:lang="x-default">{xml_escape(meta.title)}</rdf:li></rdf:Alt>
      </dc:title>""")
    # dc:description (Alt)
    if meta.description:
        parts.append(f"""
      <dc:description>
        <rdf:Alt><rdf:li xml:lang="x-default">{xml_escape(meta.description)}</rdf:li></rdf:Alt>
      </dc:description>""")
    # photoshop:Credit
    if meta.credit:
        parts.append(f"""
      <photoshop:Credit>{xml_escape(meta.credit)}</photoshop:Credit>""")
    # xmpRights:WebStatement
    if meta.web_statement:
        parts.append(f"""
      <xmpRights:WebStatement>{xml_escape(str(meta.web_statement))}</xmpRights:WebStatement>""")
    # plus:LicensorURL
    if meta.licensor_url:
        parts.append(f"""
      <plus:LicensorURL>{xml_escape(str(meta.licensor_url))}</plus:LicensorURL>""")

    body = "\n".join(parts).strip()
    if not body:
        return b""

    xmp = f"""<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
           xmlns:dc="http://purl.org/dc/elements/1.1/"
           xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"
           xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/"
           xmlns:plus="http://ns.useplus.org/ldf/1.0/">
    <rdf:Description rdf:about="">
{body}
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""
    return xmp.encode("utf-8")