import re


CSC_SERVICE_URLS = (
    "https://csc.gov.in/",
    "https://digitalseva.csc.gov.in/",
    "https://digitalseva.csc.gov.in/web/services",
    "https://register.csc.gov.in/",
    "https://cscregister.csccloud.in/",
    "https://digipay.csccloud.in/",
    "https://www.diginame.in/",
    "https://www.pmgdisha.in/",
    "https://www.culturemap.in/",
    "https://cschealth.in/",
    "https://cscbankmitra.in/",
    "https://cscestore.in/",
    "https://www.tele-law.in/",
    "https://www.cscagri.in/",
    "https://eseva.csccloud.in/",
    "https://www.cscacademy.org/",
    "https://www.cscbalvidyalaya.com/",
    "https://digipaathshala.cscacademy.org/",
    "https://skill.csc-services.in/",
    "https://cscsafar.in/",
    "https://dakmitra.csccloud.in/",
    "https://www.wifichoupal.in/",
    "https://cscolympiad.com/",
    "https://www.digital-village.in/",
    "https://cscudaanacademy.in/",
    "https://www.cscentrepreneur.in/",
    "https://insurance.csccloud.in/",
    "https://cscgraminnaukri.in/",
    "https://cscgjsp.in/",
    "https://www.cscdigisign.in/",
    "https://services.csccloud.in/",
    "https://locator.csccloud.in/",
    "https://jaankari.csccloud.in/important-websites.html",
    "https://support.csc.gov.in/",
    "https://connect.csc.gov.in/",
    "https://developer.csccloud.in/",
    "https://www.incometax.gov.in/iec/foportal/help/all-topics/instant-e-pan/faq",
    "https://www.protean-tinpan.com/services/pan/pan-index.html",
    "https://www.pan.utiitsl.com/PAN/",
    "https://tax2win.in/",
    "https://foscos.fssai.gov.in/",
    "https://www.fssai.gov.in/",
    "https://www.gst.gov.in/",
    "https://services.gst.gov.in/services/login",
    "https://www.passportindia.gov.in/",
    "https://portal2.passportindia.gov.in/",
    "https://www.pmjay.gov.in/",
    "https://beneficiary.nha.gov.in/",
    "https://services.india.gov.in/",
    "https://pmkisan.gov.in/",
    "https://pmfby.gov.in/",
    "https://jeevanpramaan.gov.in/v1.0/",
    "https://npstrust.org.in/",
    "https://enps.nps-proteantech.in/",
    "https://eshram.gov.in/indexmain",
    "https://pmay-urban.gov.in/",
    "https://pmaymis.gov.in/",
    "https://pmayg.nic.in/",
    "https://labour.gov.in/",
    "https://scholarships.gov.in/",
)


OFFICIAL_URL_TABLE = (
    {
        "service": "CSC Digital Seva Services",
        "url": "https://digitalseva.csc.gov.in/web/services",
        "keywords": ("digital seva", "digitalseva", "csc service", "csc services", "all forms", "portal services"),
    },
    {
        "service": "DigiPay",
        "url": "https://digipay.csccloud.in/",
        "keywords": ("digipay", "aeps", "cash withdrawal", "micro atm"),
    },
    {
        "service": "PMGDISHA",
        "url": "https://www.pmgdisha.in/",
        "keywords": ("pmgdisha", "digital literacy"),
    },
    {
        "service": "Tele-Law",
        "url": "https://www.tele-law.in/",
        "keywords": ("tele-law", "tele law", "legal"),
    },
    {
        "service": "CSC Health",
        "url": "https://cschealth.in/",
        "keywords": ("health", "telemedicine", "doctor", "jan aushadhi", "ayushman"),
    },
    {
        "service": "CSC Agriculture",
        "url": "https://www.cscagri.in/",
        "keywords": ("agriculture", "farmer", "crop", "agri"),
    },
    {
        "service": "PM-KISAN",
        "url": "https://pmkisan.gov.in/",
        "keywords": ("pm kisan", "pm-kisan", "pmkisan", "farmer registration", "pm kisan status"),
    },
    {
        "service": "Kisan Credit Card",
        "url": "https://services.india.gov.in/",
        "keywords": ("kisan credit card", "kcc", "agriculture credit"),
    },
    {
        "service": "CSC Academy",
        "url": "https://www.cscacademy.org/",
        "keywords": ("education", "academy", "course", "training", "skill", "skills"),
    },
    {
        "service": "CSC Skill Services",
        "url": "https://skill.csc-services.in/",
        "keywords": ("skill", "skills", "training", "tally", "digital unnati", "course"),
    },
    {
        "service": "CSC Travel",
        "url": "https://cscsafar.in/",
        "keywords": ("travel", "bus", "flight", "ticket", "darshan"),
    },
    {
        "service": "CSC Insurance",
        "url": "https://insurance.csccloud.in/",
        "keywords": ("insurance", "bima", "policy", "fasal bima"),
    },
    {
        "service": "PMFBY",
        "url": "https://pmfby.gov.in/",
        "keywords": ("pmfby", "pradhan mantri fasal bima", "crop insurance", "fasal bima"),
    },
    {
        "service": "CSC Bank Mitra",
        "url": "https://cscbankmitra.in/",
        "keywords": ("bank mitra", "banking correspondent", "account opening", "bc service"),
    },
    {
        "service": "PAN Services",
        "url": "https://www.protean-tinpan.com/services/pan/pan-index.html",
        "keywords": ("pan", "pan card", "pancard", "49a", "49aa"),
    },
    {
        "service": "Income Tax Services",
        "url": "https://www.incometax.gov.in/",
        "keywords": ("income tax", "itr", "tax return", "tax filing", "tax2win"),
    },
    {
        "service": "FSSAI Services",
        "url": "https://foscos.fssai.gov.in/",
        "keywords": ("fssai", "foscos", "food license", "food registration"),
    },
    {
        "service": "GST Services",
        "url": "https://www.gst.gov.in/",
        "keywords": ("gst", "gstin", "goods and services tax"),
    },
    {
        "service": "Passport Services",
        "url": "https://www.passportindia.gov.in/",
        "keywords": ("passport", "passport seva", "psk", "popsk"),
    },
    {
        "service": "Ayushman Bharat / PM-JAY",
        "url": "https://www.pmjay.gov.in/",
        "keywords": ("ayushman", "pmjay", "pm-jay", "abha", "beneficiary nha"),
    },
    {
        "service": "Jeevan Pramaan",
        "url": "https://jeevanpramaan.gov.in/v1.0/",
        "keywords": ("jeevan pramaan", "life certificate", "digital life certificate", "pension certificate"),
    },
    {
        "service": "NPS",
        "url": "https://npstrust.org.in/",
        "keywords": ("nps", "national pension system", "national pension scheme"),
    },
    {
        "service": "e-Shram",
        "url": "https://eshram.gov.in/indexmain",
        "keywords": ("e-shram", "eshram", "shram card", "labour card"),
    },
    {
        "service": "PMAY",
        "url": "https://pmay-urban.gov.in/",
        "keywords": ("pmay", "awas yojana", "pradhan mantri awas", "pm awas"),
    },
    {
        "service": "Scholarships",
        "url": "https://scholarships.gov.in/",
        "keywords": ("scholarship", "student scholarship", "nsp scholarship"),
    },
    {
        "service": "CSC Safar",
        "url": "https://cscsafar.in/",
        "keywords": ("flight booking", "bus booking", "darshan booking", "ticket booking"),
    },
    {
        "service": "Government Services",
        "url": "https://services.india.gov.in/",
        "keywords": ("government", "edistrict", "birth", "death", "ration", "scheme", "income certificate", "caste certificate", "domicile certificate", "labour registration"),
    },
)


def service_urls():

    return list(CSC_SERVICE_URLS)


def official_urls_for_query(query, max_results=5):

    text = (query or "").lower()
    matches = []

    for item in OFFICIAL_URL_TABLE:
        score = sum(1 for keyword in item["keywords"] if _keyword_matches(text, keyword))
        if score:
            matches.append((score, item["url"]))

    matches.sort(key=lambda item: item[0], reverse=True)

    urls = []
    for _, url in matches:
        if url not in urls:
            urls.append(url)

    return urls[:max_results]


def _keyword_matches(text, keyword):

    pattern = r"(?<![a-z0-9])" + re.escape(keyword.lower()) + r"(?![a-z0-9])"
    return bool(re.search(pattern, text))
