import os
from urllib.parse import urlparse

import streamlit as st


DEFAULT_ALLOWED_DOMAINS = (
    "csc.gov.in",
    "cscspv.in",
    "digitalseva.csc.gov.in",
    "register.csc.gov.in",
    "cscregister.csccloud.in",
    "digipay.csccloud.in",
    "diginame.in",
    "pmgdisha.in",
    "culturemap.in",
    "cschealth.in",
    "cscbankmitra.in",
    "cscestore.in",
    "tele-law.in",
    "cscagri.in",
    "eseva.csccloud.in",
    "cscacademy.org",
    "cscbalvidyalaya.com",
    "digipaathshala.cscacademy.org",
    "skill.csc-services.in",
    "cscsafar.in",
    "dakmitra.csccloud.in",
    "wifichoupal.in",
    "cscolympiad.com",
    "digital-village.in",
    "cscudaanacademy.in",
    "cscentrepreneur.in",
    "insurance.csccloud.in",
    "cscgraminnaukri.in",
    "cscgjsp.in",
    "cscdigisign.in",
    "services.csccloud.in",
    "locator.csccloud.in",
    "jaankari.csccloud.in",
    "support.csc.gov.in",
    "connect.csc.gov.in",
    "developer.csccloud.in",
    "cscprod.my.site.com",
    "incometax.gov.in",
    "eportal.incometax.gov.in",
    "protean-tinpan.com",
    "tinpan.proteantech.in",
    "proteantech.in",
    "onlineservices.nsdl.com",
    "pan.utiitsl.com",
    "utiitsl.com",
    "tax2win.in",
    "fssai.gov.in",
    "foscos.fssai.gov.in",
    "gst.gov.in",
    "services.gst.gov.in",
    "passportindia.gov.in",
    "portal2.passportindia.gov.in",
    "pmjay.gov.in",
    "nha.gov.in",
    "beneficiary.nha.gov.in",
    "services.india.gov.in",
    "pmkisan.gov.in",
    "pmfby.gov.in",
    "jeevanpramaan.gov.in",
    "npstrust.org.in",
    "enps.nps-proteantech.in",
    "nps-proteantech.in",
    "eshram.gov.in",
    "pmay-urban.gov.in",
    "pmaymis.gov.in",
    "pmayg.nic.in",
    "labour.gov.in",
    "scholarships.gov.in",
)


def _secret(name, default=""):

    try:
        value = st.secrets.get(name, None)
    except Exception:
        value = None

    if value:
        return str(value).strip()

    return os.getenv(name, default).strip()


def allowed_domains():

    extra = _secret("CSC_ALLOWED_DOMAINS", "")
    domains = list(DEFAULT_ALLOWED_DOMAINS)
    domains.extend([part.strip().lower() for part in extra.split(",") if part.strip()])

    return tuple(dict.fromkeys(domains))


def setting(name, default=""):

    return _secret(name, default)


def allowed_domains_label():

    return ", ".join(allowed_domains())


def _host(value):

    parsed = urlparse(value if "://" in value else f"https://{value}")
    return (parsed.netloc or parsed.path).split("@")[-1].split(":")[0].lower()


def is_allowed_domain(host):

    clean = _host(host)
    return any(clean == domain or clean.endswith(f".{domain}") for domain in allowed_domains())


def is_allowed_url(url):

    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and is_allowed_domain(parsed.netloc)


def is_allowed_source(source):

    if not source:
        return False

    return is_allowed_url(source)
